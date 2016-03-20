# solutions.py
"""Volume II: Interior Point II (Quadratic Optimization). Solutions file."""
import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt
from cvxopt import matrix, solvers
import math
from scipy import sparse as spar
from mpl_toolkits.mplot3d import axes3d

def startingPoint(G, c, A, b, guess):
    """
    Obtain an appropriate initial point for solving the QP
    .5 x^T Gx + x^T c s.t. Ax >= b.
    Inputs:
        G -- symmetric positive semidefinite matrix shape (n,n)
        c -- array of length n
        A -- constraint matrix shape (m,n)
        b -- array of length m
        guess -- a tuple of arrays (x, y, mu) of lengths n, m, and m, resp.
    Returns:
        a tuple of arrays (x0, y0, l0) of lengths n, m, and m, resp.
    """
    m,n = A.shape
    x0, y0, l0 = guess

    # initialize linear system
    N = np.zeros((n+m+m, n+m+m))
    N[:n,:n] = G
    N[:n, n+m:] = -A.T
    N[n:n+m, :n] = A
    N[n:n+m, n:n+m] = -np.eye(m)
    N[n+m:, n:n+m] = np.diag(l0)
    N[n+m:, n+m:] = np.diag(y0)
    rhs = np.empty(n+m+m)
    rhs[:n] = -(G.dot(x0) - A.T.dot(l0)+c)
    rhs[n:n+m] = -(A.dot(x0) - y0 - b)
    rhs[n+m:] = -(y0*l0)

    sol = la.solve(N, rhs)
    dx = sol[:n]
    dy = sol[n:n+m]
    dl = sol[n+m:]

    y0 = np.maximum(1, np.abs(y0 + dy))
    l0 = np.maximum(1, np.abs(l0+dl))

    return x0, y0, l0

def qInteriorPoint(Q, c, A, b, guess, niter=20, tol=1e-16, verbose=False):
    """Solve the Quadratic program min .5 x^T Q x +  c^T x, Ax >= b
    using an Interior Point method.

    Parameters:
        Q ((n,n) ndarray): Positive semidefinite objective matrix.
        c ((n, ) ndarray): linear objective vector.
        A ((m,n) ndarray): Inequality constraint matrix.
        b ((m, ) ndarray): Inequality constraint vector.
        guess (3-tuple of arrays of lengths n, m, and m): Initial guesses for
            the solution x and lagrange multipliers y and eta, respectively.
        niter (int > 0): The maximum number of iterations to execute.
        tol (float > 0): The convergence tolerance.

    Returns:
        x ((n, ) ndarray): The optimal point.
        val (float): The minimum value of the objective function.
    """
    m,n = A.shape
    def F(x_, y_, m_):
        """The almost-linear function that accounts for the KKT conditions."""
        return np.hstack((
                            np.dot(Q, x_) - np.dot(A.T, y_) + c,
                            np.dot(A, x_) - y_ - b,
                            m_*y_                                   ))

    DF = np.vstack((
            np.hstack((Q, np.zeros((n,m)), -A.T)),
            np.hstack((A, -np.eye(m), np.zeros((m,m)))),
            np.zeros((m,2*m+n))
                    ))

    # Get the initial point and verify the dimensions.
    x, y, mu = startingPoint(Q, c, A, b, guess)
    assert len(x) == len(c) == n
    assert len(y) == len(mu) == len(b) == m

    e = np.ones_like(mu)
    sigma = .1
    tau = .95

    i = 0
    nu = 1 + tol
    while i < niter and nu >= tol:
        i += 1

        # Search Direction.
        DF[-m:,n:-m] = np.diag(mu)
        DF[-m:,-m:] = np.diag(y)

        nu = np.dot(y, mu) / m
        nu_vec = np.hstack((np.zeros(n+m), e*nu*sigma))
        lu_piv = la.lu_factor(DF)
        direct = la.lu_solve(lu_piv, nu_vec - F(x,y,mu))

        # Step Length.
        dx, dy, dmu = direct[:n], direct[n:-m], direct[-m:]

        mask = dmu < 0
        bmin = np.min(-mu[mask]/dmu[mask])
        beta = min(1, tau*min(1, bmin)) if np.any(mask) else tau

        mask = dy < 0
        dmin = np.min(-y[mask]/dy[mask]).min()
        delta = min(1, tau*min(1, dmin)) if np.any(mask) else tau

        alpha = min(beta, delta)

        # Proceed to the next iterate.
        x += alpha*dx
        y += alpha*dy
        mu += alpha*dmu

        if verbose:
            print("Iteration {:0>2} nu = {}".format(i, nu))
    if i < niter and verbose:
        print("Converged in {} iterations".format(i))
    elif verbose:
        print("Maximum iterations reached")
    return x, .5*x.dot(Q).dot(x) + c.dot(x)

def test_qip():
    Q = np.array([[1,-1.],[-1,2]])
    c = np.array([-2,-6.])
    A = np.array([[-1, -1], [1, -2.], [-2, -1], [1, 0], [0,1]])
    b = np.array([-2, -2, -3., 0, 0])
    x0 = np.array([.5, .5])
    y0 = np.ones(5)
    m0 = np.ones(5)
    point, value = qInteriorPoint(Q, c, A, b, (x0,y0,m0), verbose=True)
    return np.allclose(point, [2/3., 4/3.])

if __name__ == '__main__':
    test_qip()

def qInteriorPoint_old(G, c, A, b, guess, niter=20, verbose=False):
    '''
    Solve min .5x^T Gx + x^T c s.t. Ax >= b using a Predictor-Corrector
    Interior Point method.
    Inputs:
        G -- symmetric positive semidefinite matrix shape (n,n)
        A -- constraint matrix size (m,n)
        b -- array of length m
        c -- array of length n
        niter -- integer, giving number of iterations to run
        verbose -- boolean, indicating whether to output print statements
        guess -- tuple of three arrays (x, y, l) of length n, m, and m, an initial estimate
    Returns:
        x -- an array of length n, the minimizer of the quadratic program.
    '''
    # initialize variables
    m,n = A.shape
    x, y, l = startingPoint(G,c,A,b,guess)

    # initialize linear system
    N = np.zeros((n+m+m, n+m+m))
    N[:n,:n] = G
    N[:n, n+m:] = -A.T
    N[n:n+m, :n] = A
    N[n:n+m, n:n+m] = -np.eye(m)
    sol = np.empty(n+m+m)
    rhs = np.empty(n+m+m)

    for i in xrange(niter):
        # finish initializing linear system
        N[n+m:, n:n+m] = np.diag(l)
        N[n+m:, n+m:] = np.diag(y)
        rhs[:n] = -(G.dot(x) - A.T.dot(l)+c)
        rhs[n:n+m] = -(A.dot(x) - y - b)
        rhs[n+m:] = -(y*l)

        # solve dx_aff, dy_aff, dl_aff using LU decomposition
        lu_piv = la.lu_factor(N)
        sol[:] = la.lu_solve(lu_piv, rhs)
        dx_aff = sol[:n]
        dy_aff = sol[n:n+m]
        dl_aff = sol[n+m:]

        # calculate centering parameter
        mu = y.dot(l)/m
        ahat_aff1 = stepSize(y, dy_aff)
        ahat_aff2 = stepSize(l, dl_aff)
        ahat_aff = min(ahat_aff1,ahat_aff2)
        mu_aff = (y+ahat_aff*dy_aff).dot(l+ahat_aff*dl_aff)/m
        sig = (mu_aff/mu)**3

        # calculate dx, dy, dl
        rhs[n+m:] -= dl_aff*dy_aff - sig*mu
        sol[:] = la.lu_solve(lu_piv, rhs)
        dx = sol[:n]
        dy = sol[n:n+m]
        dl = sol[n+m:]

        # calculate step size
        t = 0.9 # there are other ways to choose this parameter
        ap = stepSize(t*y, dy)
        ad = stepSize(t*l, dl)
        a = min(ap, ad)

        # calculate next point
        x += a*dx
        y += a*dy
        l += a*dl

        if verbose:
            print '{0:f} {1:f}'.format(.5*(x* G.dot(x)).sum() + (x*c).sum(), mu)
    return x


def laplacian(n):
    """
    Construct the discrete Dirichlet energy matrix H for an n x n grid.
    Inputs:
        n -- side length of grid
    Returns:
        dense array of shape n^2 x n^2
    """
    n = n+2
    data = -1*np.ones((5, (n-2)**2))
    data[2,:] = 4
    data[1, n-3::n-2] = 0
    data[3, ::n-2] = 0
    diags = np.array([-n+2, -1, 0, 1, n-2])
    return spar.spdiags(data, diags, (n-2)**2, (n-2)**2).todense()

    
def portfolio():
    # Markowitz portfolio optimization
    data = np.loadtxt('portfolio.txt')
    data = data[:,1:]
    n = data.shape[1]
    mu = 1.13
    
    # calculate covariance matrix
    Q = np.cov(data .T)
    
    # calculate returns
    R = data.mean(axis=0)
    
    P = matrix(Q)
    q = matrix(np.zeros(n))
    b = matrix(np.array([1., mu]))
    A = np.ones((2,n))
    A[1,:] = R
    A = matrix(A)
    
    # calculate optimal portfolio with short selling.
    sol1 = solvers.qp(P,q,A=A,b=b)
    x1 = np.array(sol1['x']).flatten()
    
    # calculate optimal portfolio without short selling.
    G = matrix(-np.eye(n))
    h = matrix(np.zeros(n))
    sol2 = solvers.qp(P,q,G, h,A, b)
    x2 = np.array(sol2['x']).flatten()
    
    return x1, x2
