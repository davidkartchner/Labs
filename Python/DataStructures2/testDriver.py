# solutions.py
"""Volume II Lab 5: Data Structures II (Trees). Test Driver."""

from matplotlib import pyplot as plt
from numpy.random import choice
from time import time
import inspect

from solutions import iterative_search
from solutions import SinglyLinkedList, BST

def test(student_module):
    """Test script. You must import the student's 'solutions.py' as a module.
    
     5 points for problem 1
    15 points for problem 2
    30 points for problem 3
    10 points for problem 4
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 80.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""

    # Constructor
    def __init__(self):
        self.feedback = ""

    # Main routine
    def test_all(self, student_module):
        self.feedback = ""
        score = 0

        try:    # Problem 1: 5 points
            self.feedback += "\n\nProblem 1 (5 points):"
            points = self.problem1(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 2: 15 points
            self.feedback += "\n\nProblem 2 (15 points):"
            points = self.problem2(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 3: 30 points
            self.feedback += "\n\nProblem 3 (30 points):"
            points = self.problem3(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 4: 10 points
            self.feedback += "\n\nProblem 4 (10 points):"
            points = self.problem4(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message

        # Report final score.
        total = 60
        percentage = (100.0 * score) / total
        self.feedback += "\n\nTotal score: " + str(score) + "/"
        self.feedback += str(total) + " = " + str(percentage) + "%"
        if   percentage >=  98.0: self.feedback += "\n\nExcellent!"
        elif percentage >=  90.0: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print self.feedback
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t' + comments
        self.score = score

    # Helper Function
    def strTest(self, x, y, message):
        """Test to see if x and y have the same string representation."""
        if str(x) == str(y):
            return 1
        else:
            self.feedback += message
            self.feedback += "\nCorrect response:\n" + str(x)
            self.feedback += "\nStudent response:\n" + str(y)
            return 0

    # Problems
    def problem1(self, s):
        """Test recursive_search(). 5 points."""

        points = 0

        lls = SinglyLinkedList()
        # Check recursive_search on empty list (1 point)
        try:
            s.recursive_search(lls, 1)
            self.feedback += "\n\trecursive_search() failed on empty list"
        except ValueError:
            points += 1

        # Check recursive_search for items in list (3 points)
        lls.append(1)
        lls.append('a')
        lls.append(2)
        points += self.strTest(iterative_search(lls,1),
                               s.recursive_search(lls, 1),
                               "\n\trecursive_search(x) failed for x in list")
        points += self.strTest(iterative_search(lls, 'a'),
                               s.recursive_search(lls, 'a'),
                               "\n\trecursive_search(x) failed for x in list")
        points += self.strTest(iterative_search(lls, 2),
                               s.recursive_search(lls, 2),
                               "\n\trecursive_search(x) failed for x in list")

        # Check recursive_search for items not in list (1 point)
        try:
            s.recursive_search(lls, 3)
            self.feedback += "\n\trecursive_search(x) failed for x not in list"
        except ValueError:
            points += 1

        # Check that recursion is used somewhere
        text = inspect.getsourcelines(s.recursive_search)[0]; code = ""
        text = text[len(s.recursive_search.__doc__.splitlines()) + 1 :]
        for line in text: code += line
        print "\nStudent Code (check for recursion):\n", code
        credit = -1
        while credit > 1 or credit < 0:
            try:
                credit = int(input("\nScore out of 1: "))
            except:
                credit = -1
        if credit != 1:
            self.feedback += "\n\trecursive_search() must use recursion!"
        points *= credit

        return points

    def problem2(self, s):
        """Test BST.insert(). 15 Points."""

        points = 0

        # Empty tree (0 pts)
        tree1, tree2 = BST(), s.BST()
        self.strTest(tree1, tree2, "\n\tBST() failed initially!")

        # Inserting root (2 pts)
        tree1.insert(4); tree2.insert(4)
        points += 2*self.strTest(tree1, tree2, "\n\tBST.insert(4) failed "
                                 "on root insertion.\nPrevious tree:\n[]")

        def test_insert(value, solTree, stuTree):
            oldTree = str(solTree)
            solTree.insert(value); stuTree.insert(value)
            p = self.strTest(tree1, tree2, "\n\tBST.insert(" + str(value)
                            + ") failed.\nPrevious tree:\n" + oldTree)
            return p, solTree, stuTree

        # Inserting nonroot (9 pts)
        p, tree1, tree2 = test_insert( 2, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 1, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 3, tree1, tree2); points += p
        p, tree1, tree2 = test_insert(10, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 5, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 6, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 9, tree1, tree2); points += p
        p, tree1, tree2 = test_insert( 7, tree1, tree2); points += p
        p, tree1, tree2 = test_insert(11, tree1, tree2); points += p

        # Inserting already existing value (4 pts)
        def test_duplicate(value, stuTree):
            try:
                stuTree.insert(value)
                self.feedback += "\n\tBST.insert(" + str(value) + ") failed "
                self.feedback += "for " + str(value) + " already in tree"
                return 0
            except ValueError:
                return 1

        points +=   test_duplicate(4, tree2)
        points +=   test_duplicate(1, tree2)
        points += 2*test_duplicate(7, tree2)
        
        if points < 11:
            self.feedback += "\n\tAll BST.remove() tests are likely to fail"
            self.feedback += "\n\tunless all BST.insert() tests pass!"
        return points

    def problem3(self, s):
        """Test BST.remove(). 30 points."""

        points = 0

        def load_trees():
            solutions_tree, student_tree = BST(), s.BST()
            solutions_tree.insert( 4); student_tree.insert( 4)
            solutions_tree.insert( 2); student_tree.insert( 2)
            solutions_tree.insert( 1); student_tree.insert( 1)
            solutions_tree.insert( 3); student_tree.insert( 3)
            solutions_tree.insert(10); student_tree.insert(10)
            solutions_tree.insert( 5); student_tree.insert( 5)
            solutions_tree.insert( 6); student_tree.insert( 6)
            solutions_tree.insert( 9); student_tree.insert( 9)
            solutions_tree.insert( 7); student_tree.insert( 7)
            solutions_tree.insert(11); student_tree.insert(11)
            solutions_tree.insert(15); student_tree.insert(15)
            solutions_tree.insert(14); student_tree.insert(14)
            solutions_tree.insert(16); student_tree.insert(16)
            solutions_tree.insert(12); student_tree.insert(12)
            if str(solutions_tree) != str(student_tree):
                raise NotImplementedError("BST.remove() cannot be tested "
                                          "until BST.insert() is correct.")
            return solutions_tree, student_tree

        def test_remove(value, solTree, stuTree):
            oldTree = str(solTree)
            try:
                solTree.remove(value); stuTree.remove(value)
                p = self.strTest(tree1, tree2, "\n\tBST.remove(" + str(value)
                            + ") failed.\nPrevious tree:\n" + oldTree)
            except Exception as e:
                self.feedback += "\n\tError while removing " + str(value)
                self.feedback += ": " + str(e) + "\nPrevious tree:\n" + oldTree
                p = 0
            finally:
                return p, solTree, stuTree

        tree2 = s.BST()

        # Remove from empty tree (1 points)
        try:
            tree2.remove(5)
            self.feedback += "\n\tBST.remove() failed for empty tree"
        except ValueError:
            points += 1

        # Remove leaf (5 points)
        tree1, tree2 = load_trees()
        p, tree1, tree2 = test_remove( 1, tree1, tree2); points += p
        p, tree1, tree2 = test_remove( 7, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(12, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(16, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(14, tree1, tree2); points += p
        
        # Remove non-root with 1 child (5 points)
        tree1, tree2 = load_trees()
        p, tree1, tree2 = test_remove( 9, tree1, tree2); points += p
        p, tree1, tree2 = test_remove( 6, tree1, tree2); points += p
        p, tree1, tree2 = test_remove( 5, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(11, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(14, tree1, tree2); points += p

        # Remove non-root with 2 children (5 points)
        tree1, tree2 = load_trees()
        p, tree1, tree2 = test_remove( 2, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(15, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(10, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(11, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(12, tree1, tree2); points += p
        
        # Remove root with no children (2 point)
        tree1, tree2 = BST(), s.BST()
        tree1.insert(10); tree2.insert(10)
        p, tree1, tree2 = test_remove(10, tree1, tree2); points += p*2

        # Remove root with one child (5 points)
        tree1, tree2 = BST(), s.BST()
        tree1.insert(1); tree2.insert(1)
        tree1.insert(2); tree2.insert(2)
        tree1.insert(3); tree2.insert(3)
        tree1.insert(4); tree2.insert(4)
        tree1.insert(5); tree2.insert(5)
        tree1.insert(6); tree2.insert(6)
        p, tree1, tree2 = test_remove(1, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(2, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(3, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(4, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(5, tree1, tree2); points += p

        # Remove root with two children (5 points)
        tree1, tree2 = BST(), s.BST()
        tree1.insert(2); tree2.insert(2)
        tree1.insert(1); tree2.insert(1)
        tree1.insert(7); tree2.insert(7)
        tree1.insert(6); tree2.insert(6)
        tree1.insert(5); tree2.insert(5)
        tree1.insert(4); tree2.insert(4)
        tree1.insert(3); tree2.insert(3)
        p, tree1, tree2 = test_remove(2, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(3, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(4, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(5, tree1, tree2); points += p
        p, tree1, tree2 = test_remove(6, tree1, tree2); points += p

        # Remove nonexistent (2 points)
        tree1, tree2 = load_trees()
        try:
            tree2.remove(0)
            self.feedback += "\n\tBST.remove(0) failed for 0 not in tree"
            self.feedback += "\nPrevious tree:\n" + str(tree1)
        except ValueError:
            points += 1

        try:
            tree2.remove(12.5)
            self.feedback += "\n\tBST.remove(12.5) failed for 12.5 not in tree"
            self.feedback += "\nPrevious tree:\n" + str(tree1)
        except ValueError:
            points += 1

        return points

    def problem4(self, s):
        """Test time_structures(). 10 points."""

        print("Running time_structures()...")
        s.time_structures("English.txt", 1000, 4000, 1000)
        points = -1
        while points > 10 or points < 0:
            try:
                points = int(input("\nScore out of 10: "))
            except:
                points  = -1
        if points != 10:
            self.feedback += "\n\t" + raw_input("Problem 4 feedback: ")

        return points


if __name__ == '__main__':
    import solutions as sol
    score, feedback = test(sol)
