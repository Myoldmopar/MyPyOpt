import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from mypyopt.ProjectStructure import ProjectStructure
from mypyopt.InputOutput import InputOutputManager
from mypyopt.DecisionVariable import DecisionVariable
from mypyopt.Optimizer import HeuristicSearch
from mypyopt.Exceptions import MyPyOptException
from mypyopt.ReturnStateEnum import ReturnStateEnum


class TestQuadratic(unittest.TestCase):

    def setUp(self):

        # Initialize list of decision variables
        # DecisionVariable(min, max, initial_value, initial_step_size, convergence_criterion, variable_name)
        self.dvs = list()
        self.dvs.append(DecisionVariable(-5, 5, 0.5, 0.1, 0.000001, 'a'))  # opt value = 1
        self.dvs.append(DecisionVariable(-5, 5, 0.5, 0.1, 0.000001, 'b'))  # opt value = 2
        self.dvs.append(DecisionVariable(-5, 5, 0.5, 0.1, 0.000001, 'c'))  # opt value = 3

        # Initialize the IO manager
        self.io = InputOutputManager()

    # Actual "simulation"
    @staticmethod
    def sim_quadratic(parameter_hash):
        x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        return [parameter_hash['a'] + parameter_hash['b'] * x + parameter_hash['c'] * (x ** 2) for x in x_values]

    # Squared Error expression
    @staticmethod
    def ssqe_quadratic(sim_values):
        x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        actual_values = [1 + 2 * x + 3 * (x ** 2) for x in x_values]
        sqe = [(a - b) ** 2 for a, b in zip(actual_values, sim_values)]
        return sum(sqe)

    # exercise the callbacks
    @staticmethod
    def completed(return_value):
        print("COMPLETED CALLBACK: DONE; reason=" + ReturnStateEnum.enum_to_string(return_value.reason))

    @staticmethod
    def progress(completed_iteration_number):
        print("PROGRESS CALLBACK: COMPLETED ITERATION #" + str(completed_iteration_number))

    def test_quadratic1(self):
        self.sim = ProjectStructure(1.2, 0.85, 2000, 'TestProject', 'projects')
        searcher = HeuristicSearch(self.sim, self.dvs, self.io, self.sim_quadratic,
                                   self.ssqe_quadratic, self.progress, self.completed)
        response = searcher.search()
        self.assertTrue(response.success)
        self.assertAlmostEqual(1.0, response.values[0], 3)
        self.assertAlmostEqual(2.0, response.values[1], 3)
        self.assertAlmostEqual(3.0, response.values[2], 3)

    def test_quadratic_bad_folder(self):
        self.sim = ProjectStructure(1.2, 0.85, 2000, 'CantWriteToUsr', '/usr')
        with self.assertRaises(MyPyOptException):
            HeuristicSearch(self.sim, self.dvs, self.io, self.sim_quadratic,
                            self.ssqe_quadratic, self.progress, self.completed)

# allow execution directly as python tests/test_solar.py
if __name__ == '__main__':
    unittest.main()
