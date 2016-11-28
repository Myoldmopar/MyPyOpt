# This file exhaustively tests the entirety of lib/solar.py

import sys
import os
import unittest

# add the source directory to the path so the unit test framework can find it
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'mypyopt'))

from structures import DecisionVariable, SimulationStructure
from inputoutput import InputOutputManager
from optimizer import HeuristicSearch


class TestQuadratic(unittest.TestCase):
    def test_quadratic1(self):
        # Initialize simulation structure
        # SimulationStructure(expansion, contraction, max_iterations)
        sim = SimulationStructure(1.2, 0.85, 2000)

        # Initialize list of decision variables
        # DecisionVariable(min, max, initial_value, initial_step_size, convergence_criterion, variable_name)
        dvs = list()
        dvs.append(DecisionVariable(-5, 5, 0.5, 0.1, 0.000001, 'a'))  # opt value = 1
        dvs.append(DecisionVariable(-5, 5, 0.5, 0.1, 0.000001, 'b'))  # opt value = 2
        dvs.append(DecisionVariable(-5, 5, 0.5, 0.1, 0.000001, 'c'))  # opt value = 3

        # Initialize the IO manager
        io = InputOutputManager()

        # Actual "simulation"
        def sim_quadratic(parameter_hash):
            x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
            return [parameter_hash['a'] + parameter_hash['b'] * x + parameter_hash['c'] * (x ** 2) for x in x_values]

        # Squared Error expression
        def ssqe_quadratic(sim_values):
            x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
            actual_values = [1 + 2 * x + 3 * (x ** 2) for x in x_values]
            sqe = [(a - b) ** 2 for a, b in zip(actual_values, sim_values)]
            return sum(sqe)

        # run the optimizer
        searcher = HeuristicSearch(sim, dvs, io, sim_quadratic, ssqe_quadratic)
        self.assertTrue(searcher.converged)
        self.assertAlmostEqual(1.0, searcher.converged_values[0], 3)
        self.assertAlmostEqual(2.0, searcher.converged_values[1], 3)
        self.assertAlmostEqual(3.0, searcher.converged_values[2], 3)

# allow execution directly as python tests/test_solar.py
if __name__ == '__main__':
    unittest.main()