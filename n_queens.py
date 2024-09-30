"""
Developer: Prem
Date: 2024-02-27
Source: Google OR-Tools Constraint Optimization
https://developers.google.com/optimization/cp
This module provides a solution to the N-queens problem using OR-Tools.
"""

import sys
import time
from ortools.sat.python import cp_model


class NQueenSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Prints intermediate solutions for the N-Queens problem."""

    def __init__(self, queens):
        """
        Initializes the NQueenSolutionPrinter Constructor.
        Parameters:
        queens (list): A list of integer variables representing the queens'
        positions.
        __init__ method of the CpSolverSolutionCallback class from cp_model.
        Parameters:
        attribute self has the parameter:
        queens is object it can accessed the class,
        attribute self has the parameter: solution_count(int)is 0
        this can track number of solution found,
        attribute self has the parameter:  start_time this can
        used to measure the time it takes to find solution.
        """
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__queens = queens
        self.__solution_count = 0
        self.__start_time = time.time()

    def solution_count(self):
        """
        Solves the N-Queens problem and prints solutions.
        the number of queens to place and it will return the solutinon count.
        """
        return self.__solution_count

    def on_solution_callback(self):
        """
        on_solution_callback is likely part of a class that's
        used as a callback during the solving process of a constraint
        programming problem and it has one paramete self.
        It prints the current solution number and the time elapsed since the
        start of the solving process.
        Then, it increments the solution count.
        It also prints the current state of the board. For each position on
        the board, it prints "Q" if there
        is a queen at that position, and "_" otherwise. Each row of the board
        is printed on a new line, and
        different boards are separated by an empty line.

        """
        current_time = time.time()
        print(
            f"Solution {self.__solution_count}, "
            f"time = {current_time - self.__start_time} s"
        )
        self.__solution_count += 1

        all_queens = range(len(self.__queens))
        for i in all_queens:
            for j in all_queens:
                if self.Value(self.__queens[j]) == i:
                    # There is a queen in column j, row i.
                    print("Q", end=" ")
                else:
                    print("_", end=" ")
            print()
        print()


def main(board_size):
    """
    Solves the N-Queens problem and prints solutions.

    Parameters:
    board_size (int): The size of the chessboard and the number of queens.
    The main function takes one parameter board size.
    Creating solver model is a constraint programming model using the OR-Tools
    CP-SAT solver.
    Creating variables is a list of integer variables representing the queens'
    positions.
    The value of each variable is the row that the queen is in each column.
    Adding constraints  All rows must be different. and no two queens can be
    on the same diagonal.
    Ensures that no queens share the two diagonals by creating the variables
    queens_plus_i representing the
    sum of column index and row index and queens_minus_i representing
    the difference of the column index and row index.


    """
    # Creates the solver.
    model = cp_model.CpModel()

    # Creates the variables.
    # There are `board_size` number of variables, one for a queen in  column
    # of the board. The value of each variable is the row that the queen is in.
    queens = []
    for i in range(board_size):
        queens.append(model.NewIntVar(0, board_size - 1, "x_" + str(i)))

    # Creates the constraints.
    # All rows must be different.
    model.AddAllDifferent(queens)

    # No two queens can be on the same diagonal.
    queens_plus_i = []
    for i in range(board_size):
        queens_plus_i.append(queens[i] + i)
    model.AddAllDifferent(queens_plus_i)
    queens_minus_i = []
    for i in range(board_size):
        queens_minus_i.append(queens[i] - i)
    model.AddAllDifferent(queens_minus_i)

    # Solve the model.
    solver = cp_model.CpSolver()
    solution_printer = NQueenSolutionPrinter(queens)
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solution_printer)

    # Statistics.
    print("\nStatistics")
    print(f"  conflicts      : {solver.NumConflicts()}")
    print(f"  branches       : {solver.NumBranches()}")
    print(f"  wall time      : {solver.WallTime()} s")
    print(f"  solutions found: {solution_printer.solution_count()}")


if __name__ == "__main__":
    # By default, solve the 8x8 problem.
    size = 8
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    main(size)
