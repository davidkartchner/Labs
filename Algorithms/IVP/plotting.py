# import matplotlib
# matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
import solution

def Fig1(): 
# Plot #1: The solution of y'=y-2x+4, y(0)=0, is 
# y(x) = -2 + 2x + (ya + 2)e^x. This code plots the solution for 0<x<2,
# and then plots the approximation given by Euler's method
# Text Example (f1).
	a, b, ya = 0.0, 2.0, 0.0
	def f1(x,ya): return -2. + 2.*x + (ya + 2.)*np.exp(x)
	
	def ode_f1(x,y): return np.array([1.*y -2.*x + 4.])
	
	
	x = np.linspace(a,b,11)
	Y_E = solution.Euler(ode_f1,a,b,10,ya) 
	plt.plot(x, Y_E, 'b-',label="h = 0.2")
	
	x = np.linspace(a,b,21)
	Y_E = solution.Euler(ode_f1,a,b,20,ya) 
	plt.plot(x, Y_E, 'g-',label="h = 0.1")
	
	x = np.linspace(a,b,41)
	Y_E = solution.Euler(ode_f1,a,b,40,ya) 
	plt.plot(x, Y_E, 'r-',label="h = 0.05")
	
	x1 = np.linspace(0,2,200); k =int(200/40)
	
	plt.plot(x1[::k], solution.function(x1,f1,0.0)[::k], 'k*-',label="Solution") # The solution 
	plt.plot(x1[k-1::k], solution.function(x1,f1,0.0)[k-1::k], 'k-') # The solution 
	
	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('Fig1.pdf')
	plt.clf()
	return 


def Fig2(): 
# Plot #2: Integral curves for f1(x). Text Example (f1).
	a , b, n = 0.0,  1.6,  200
	h, k, x = (b-a)/n, int(n/40), np.linspace(a,b,n+1)
	def f1(x,ya): return -2. + 2.*x + (ya + 2.)*np.exp(x)
	
	plt.plot(x, solution.function(x,f1,0.0), 'k-')
	plt.plot(x, solution.function(x,f1,-1.0), 'k-')
	plt.plot(x[::k], solution.function(x,f1,-2.0)[::k], 'k*-', label='Particular solution for 'r"$y'-y=-2x+4 $.")
	plt.plot(x, solution.function(x,f1,-3.0), 'k-')
	plt.plot(x, solution.function(x,f1,-4.0), 'k-')
	plt.plot(x, solution.function(x,f1,-5.0), 'k-')
	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('Fig2.pdf')
	# plt.show()
	plt.clf()
	return


def Fig3(): 
# Plot #3: Integral curves for f2(x).
	a , b, n = 0.0,  1.6,  200
	k, x = int(n/20), np.linspace(a,b,n+1)
	def f2(x,ya): return 4. + 2.*x + (ya - 4.)*np.exp(-x)
	
	
	plt.plot(x, solution.function(x,f2,0.0), 'k-')
	plt.plot(x, solution.function(x,f2,2.0), 'k-')
	plt.plot(x[::k], solution.function(x,f2,4.0)[::k], 'k*-', label='Particular solution for 'r"$y' +y =  - 2x + 2 $.")
	plt.plot(x, solution.function(x,f2,6.0), 'k-')
	plt.plot(x, solution.function(x,f2,8.0), 'k-')
	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	# plt.show()
	plt.savefig('Fig3.pdf')
	plt.clf()
	return 


def Fig4():
# Plot #4: Integral curves for y' = sin y using dopri5 
	a, b, n = 0.0, 5.0, 50
	k, x= n//10, np.linspace(a,b,n+1)
	def ode_f3(x,y): return np.array([np.sin(y)])
	
	
	def dopri5_integralcurves(ya): 
		test1 = ode(ode_f3).set_integrator('dopri5',atol=1e-7,rtol=1e-8,nsteps=500) 
		y0 = ya; x0 = a; test1.set_initial_value(y0,x0) 
		Y = np.zeros(x.shape); Y[0] = y0
		for j in range(1,len(x)): 
			test1.integrate(x[j])
			Y[j]= test1.y
		return Y
	
	plt.plot(x[::k], dopri5_integralcurves(5.0*np.pi/2.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(3.0*np.pi/2.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(7.0*np.pi/4.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(0.0*np.pi/2.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(-np.pi)[::k], 'k*-',label='Equilibrium solutions')
	plt.plot(x[::k], dopri5_integralcurves(np.pi)[::k], 'k*-')
	plt.plot(x[::k], dopri5_integralcurves(2*np.pi)[::k], 'k*-')
	plt.plot(x[::k], dopri5_integralcurves(3*np.pi)[::k], 'k*-')
	plt.plot(x[::k], dopri5_integralcurves(np.pi/4.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(np.pi/2.0)[::k], 'k-')
	plt.plot(x[::k], dopri5_integralcurves(-np.pi/2.0)[::k], 'k-')
	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('Fig4.pdf')
	plt.clf()
	return 


def HOFig1(): 
	a, b, ya = 0.0, 50.0, np.array([2., 0.])		# Parameters
	
	m , gamma, k, F = 1, .125, 1,lambda x: 0
	func = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y = solution.Runge_Kutta_4(func,a,b,600,ya,2) # 2 dimensional system
	plt.plot(np.linspace(a,b,601), Y[:,0], 'k',linestyle='-')
	
	m , gamma, k, F = 1., 0., 1.,lambda x: 0.
	func = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y = solution.Runge_Kutta_4(func,a,b,600,ya,2)
	plt.plot(np.linspace(a,b,601), Y[:,0], 'k-',linestyle='--')
	
	plt.axhline(color='k',linestyle='-')
# 	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('HOFig1.pdf')
	plt.clf()
	return 


def HOFig2(): 
	a, b, n, ya = 0.0, 20.0, 100,np.array([2., 0.])		# Parameters
	
	m , gamma, k, F = 1., 0., 1.,lambda x: 0.
	func = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y = solution.Runge_Kutta_4(func,a,b,n,ya,2)
	plt.plot(np.linspace(a,b,n+1), Y[:,0], 'k-')#,linestyle='--')
	###################################################
	#	Computing relative error of approximation     #
	Y_coarse = solution.Runge_Kutta_4(func,a,b,n/2,ya,2)
	
	Relative_Error = np.abs(Y_coarse[-1,0] - Y[-1,0])/np.abs(Y[-1,0])
	print "Relative Error = ", Relative_Error
	###################################################
	
	plt.axhline(color='k',linestyle='-')
	plt.axvline(color='k',linestyle='-')
# 	plt.legend(loc='best')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('HOFig2.pdf')
	plt.clf()
	return 


def HOProb1(): 
# Parameters
	a, b, ya = 0.0, 20.0, np.array([2., -1.])
	
	m , gamma, k, F = 3., 0., 1.,lambda x: 0.
	func1 = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y1 = solution.Runge_Kutta_4(func1,a,b,800,ya,2) # 2 dimensional system
	plt.plot(np.linspace(a,b,801), Y1[:,0], 'k',linestyle='-')
	
	m , gamma, k, F = 1, 0, 1,lambda x: 0
	func2 = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y2 = solution.Runge_Kutta_4(func2,a,b,800,ya,2)
	plt.plot(np.linspace(a,b,801), Y2[:,0], 'k-',linestyle='--')
	
	###################################################
	#	Computing relative error of approximation     #
	m , gamma, k, F = 3., 0., 1.,lambda x: 0.
	Y_coarse = solution.Runge_Kutta_4(func1,a,b,400,ya,2)
	
	Relative_Error = np.abs(Y_coarse[-1,0] - Y1[-1,0])/np.abs(Y1[-1,0])
	print "Relative Error = ", Relative_Error
	###################################################
	plt.axhline(color='k',linestyle='-')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('HOProb1.pdf')
	plt.clf()
	return 


def HOProb2(): 
# Parameters
	a, b, ya = 0.0, 20.0, np.array([1., -1.])
	
# Damped Oscillator
	m , gamma, k, F = 1., .5, 1.,lambda x: 0.
	func1 = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y1 = solution.Runge_Kutta_4(func1,a,b,800,ya,2) # 2 dimensional system
	plt.plot(np.linspace(a,b,801), Y1[:,0], '-k')#,linestyle='-')
	
###################################################
#	Computing relative error of approximation     #
	
	Y_coarse = solution.Runge_Kutta_4(func1,a,b,400,ya,2)
	Relative_Error = np.abs(Y_coarse[-1,0] - Y1[-1,0])/np.abs(Y1[-1,0])
	print "Relative Error = ", Relative_Error
###################################################
	plt.axhline(color='k',linestyle='-')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('HOProb2.pdf')
	plt.clf()
	return


def HOProb3(): 
# Parameters
	a, b, ya = 0.0, 20.0, np.array([2., -4.])
	
# Damped Oscillator
	
	m , gamma, k, F = 1., 2.1, 1.,lambda x: 0.
	func1 = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y1 = solution.Runge_Kutta_4(func1,a,b,800,ya,2) # 2 dimensional system
	plt.plot(np.linspace(a,b,801), Y1[:,0], 'k',linestyle='-')
###################################################
#	Computing relative error of approximation     #
	
	Y_coarse = solution.Runge_Kutta_4(func1,a,b,400,ya,2)
	Relative_Error = np.abs(Y_coarse[-1,0] - Y1[-1,0])/np.abs(Y1[-1,0])
	print "Relative Error = ", Relative_Error
###################################################
	plt.axhline(color='k',linestyle='-')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('HOProb3.pdf')
	plt.clf()
	return


def HOProb4(): 
# Parameters: Interval = [a,b], n = number of subintervals, ya = y(a) 
	a, b, n, ya = 0.0, 200.0, 4000, np.array([2., -1.])
	
# Eqn for a Forced Oscillator without Damping: m*y'' + k*y = F(x)
	
	m , gamma, k, omega, F = 2., .00, 2.,1.,lambda x: 2.*np.cos(omega*x)
	func1 = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y1 = solution.Runge_Kutta_4(func1,a,b,n,ya,2) # 2 dimensional system
	plt.plot(np.linspace(a,b,n+1), Y1[:,0], 'k',linestyle='-')
###################################################
#	Computing relative error of approximation     #
	
	Y_coarse = solution.Runge_Kutta_4(func1,a,b,n/2,ya,2)
	Relative_Error = np.abs(Y_coarse[-1,0] - Y1[-1,0])/np.abs(Y1[-1,0])
	print "Relative Error = ", Relative_Error
###################################################
	plt.axhline(color='k',linestyle='-')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('HOProb4.pdf')
	plt.clf()
	return

 
def HOProb5(): 
# Parameters: Interval = [a,b], n = number of subintervals, ya = y(a) 
	a, b, n, ya = 0.0, 200.0, 4000, np.array([2., -1.])
	
# Eqn a for a Forced Oscillator with Damping: m*y'' + gamma*y' + k*y = F(x)
	
	m , gamma, k, omega, F = 2., .1, 2.,1.1,lambda x: 2.*np.cos(omega*x)
	func1 = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y1 = solution.Runge_Kutta_4(func1,a,b,n,ya,2) # 2 dimensional system
	plt.plot(np.linspace(a,b,n+1), Y1[:,0], 'k',linestyle='-')
###################################################
#	Computing relative error of approximation     #
	
	Y_coarse = solution.Runge_Kutta_4(func1,a,b,n/2,ya,2)
	Relative_Error = np.abs(Y_coarse[-1,0] - Y1[-1,0])/np.abs(Y1[-1,0])
	print "Relative Error = ", Relative_Error
###################################################
	plt.axhline(color='k',linestyle='-')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('HOProb5a.pdf')
	plt.clf()
	
# Eqn b for a Forced Oscillator with Damping: m*y'' + gamma*y' + k*y = F(x)
	n = 10000
	m , gamma, k, omega, F = 2., .01, 2.,1.01,lambda x: 2.*np.cos(omega*x)
	func1 = lambda x,y: solution.harmonic_oscillator_ode(x,y,m,gamma,k,F)
	Y1 = solution.Runge_Kutta_4(func1,a,b,n,ya,2) # 2 dimensional system
	plt.plot(np.linspace(a,b,n+1), Y1[:,0], 'k',linestyle='-')
###################################################
#	Computing relative error of approximation     #
	
	Y_coarse = solution.Runge_Kutta_4(func1,a,b,n/2,ya,2)
	Relative_Error = np.abs(Y_coarse[-1,0] - Y1[-1,0])/np.abs(Y1[-1,0])
	print "Relative Error = ", Relative_Error
###################################################
	plt.axhline(color='k',linestyle='-')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.savefig('HOProb5b.pdf')
	plt.clf()
	return 




	
Fig1()
# Fig2()
# Fig3()
Fig4()

# HOProb1()
# HOProb2()
# HOProb3()
# HOProb4()
# HOProb5()
# 
# HOFig1()
# HOFig2()

