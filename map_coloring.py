"""
Developer: Prem
Date: 2024-03-01
Source: Google OR-Tools Constraint Optimization
(https://developers.google.com/optimization/cp)
This module solves the map coloring problem using constraint programming.
"""

import time
from ortools.sat.python import cp_model


class MapColoringSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions for the Map Coloring problem."""

    def __init__(self, states, colors):
        """
        __init__ Initializes the MapColoringSolutionPrinter constructor.
        attribute self has the parameter
        Parameters:
        attribute self has the parameter states (dict): A dictionary
        containing the states and their corresponding color variables.
        attribute self has the parameter colors (list): A list of
        available colors.
        attribute self has the parameter solution_count (int):
        The number of solutions found.
        attribute self has the parameter start_time (float):
        This is likely used to measure the time it takes to find solutions.
        """
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__states = states
        self.__colors = colors
        self.__solution_count = 0
        self.__start_time = time.time()

    def solution_count(self):
        """
        Prints the current solution and increments the solution count.
        It prints each state along with its assigned color.
        """
        return self.__solution_count

    def on_solution_callback(self):
        """
        on_solution_callback is likely part of a class that's
        used as a callback during the solving process of a constraint
        programming problem
        the current_time(float)  variable stores the current time using
        the time.time() function.
        It is used to calculate the elapsed time since the start of
        the solving process.
        print() # statements:Purpose: These print statements output
        information about the current solution.
        the self.__solution_count(int) variable is incremented by 1.
        and self.__states.items(Dict) is used to iterate through the states
        self.Value(color_var(int)) is used to get the value of
        the color variable.
        and finally, the print() statement is used to print
        the state and its color.
        """
        current_time = time.time()
        print(
            f"Solution {self.__solution_count}, "
            f"time = {current_time - self.__start_time} s"
        )
        self.__solution_count += 1

        for state, color_var in self.__states.items():
            color = self.Value(color_var)
            print(state + ": " + self.__colors[color])
        print()


def main():
    """
    Solves the Map Coloring problem and prints solutions.

    The function defines Australia's mainland states and their neighbors,
    creates variables for each state and adds constraints to ensure
    neighboring states.
    mainland_states: A dictionary representing Australia's mainland states and
    their neighboring states. Each key is a state, and its corresponding value
    is a list of neighboring states.
    colors: A list representing the available colors that can be used to color,
    the states Each element of the list a colors(RGB).
    model: An instance of the CpModel class, representing
    the constraint programming model used to solve the map coloring problem.
    state_colors: A dictionary mapping each state to its corresponding color.
    solver: An instance of the CpSolver class, representing the constraint
    solver used to find solutions to the map coloring problem.
    solution_printer: An instance of the MapColoringSolutionPrinter class,
    used to print intermediate solutions found during the solving process.
    solver.parameters.enumerate_all_solutions: A boolean parameter of the
    solver that specifies whether to enumerate
    all solutions found during the solving process.
    solver.Solve(model, solution_printer): Solves the model using the solver,
    and prints the statistics about the solutions found.

    """
    # Define Australia's mainland states and their neighbors
    mainland_states = {
        "WA": ["NT", "SA"],
        "NT": ["WA", "SA", "Q"],
        "SA": ["WA", "NT", "Q", "NSW", "V"],
        "Q": ["NT", "SA", "NSW"],
        "NSW": ["Q", "SA", "V"],
        "V": ["SA", "NSW"],
    }

    # Define the available colors
    colors = ["Red", "Green", "Blue"]

    # Create the solver
    model = cp_model.CpModel()

    # Create variables for each state
    state_colors = {
        state: model.NewIntVar(0, len(colors) - 1, state)
        for state in mainland_states
    }

    # Add constraints
    for state, neighbors in mainland_states.items():
        for neighbor in neighbors:
            model.Add(state_colors[state] != state_colors[neighbor])

    # Create the solver and solution printer
    solver = cp_model.CpSolver()
    solution_printer = MapColoringSolutionPrinter(state_colors, colors)
    solver.parameters.enumerate_all_solutions = True

    # Solve the model
    solver.Solve(model, solution_printer)

    # Statistics
    print("\nStatistics")
    print(f"  conflicts      : {solver.NumConflicts()}")
    print(f"  branches       : {solver.NumBranches()}")
    print(f"  wall time      : {solver.WallTime()} s")
    print(f"  solutions found: {solution_printer.solution_count()}")


if __name__ == "__main__":
    main()
