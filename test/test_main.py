import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from mypyopt.ProjectStructure import ProjectStructure
from mypyopt.InputOutput import InputOutputManager
from mypyopt.DecisionVariable import DecisionVariable
from mypyopt.OptimizerHeuristicSearch import HeuristicSearch
from mypyopt.Exceptions import MyPyOptException
from mypyopt.ReturnStateEnum import ReturnStateEnum


class TestQuadratic(unittest.TestCase):
    def setUp(self):
        """
        This sets up a 3 coefficient quadratic optimization; each individual test_ cases should override any of
        the default structures set up here, but not modify them directly
        """
        # Initialize list of decision variables
        # DecisionVariable(min, max, initial_value, initial_step_size, convergence_criterion, variable_name)
        self.dvs = list()
        self.dvs.append(DecisionVariable(minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                         convergence_criterion=0.000001, variable_name='a'))  # opt value = 1
        self.dvs.append(DecisionVariable(minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                         convergence_criterion=0.000001, variable_name='b'))  # opt value = 2
        self.dvs.append(DecisionVariable(minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                         convergence_criterion=0.000001, variable_name='c'))  # opt value = 3

        # Initialize the IO manager
        self.io = InputOutputManager()

        # Initialize a project structure
        self.sim = ProjectStructure(expansion=1.2, contraction=.85, max_iterations=2000, project_name='TestProject',
                                    output_dir='projects')

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
    def progress(completed_iteration_number, latest_objective_function_value):
        increment = 25.0
        if completed_iteration_number / increment == int(completed_iteration_number / increment):
            print("PROGRESS CALLBACK: COMPLETED ITERATION #" + str(completed_iteration_number) + " - J=" +
                  str(latest_objective_function_value))

    def test_quadratic1(self):
        searcher = HeuristicSearch(self.sim, self.dvs, self.io, self.sim_quadratic,
                                   self.ssqe_quadratic, self.progress, self.completed)
        response = searcher.search()
        self.assertTrue(response.success)
        self.assertAlmostEqual(1.0, response.values[0], 3)
        self.assertAlmostEqual(2.0, response.values[1], 3)
        self.assertAlmostEqual(3.0, response.values[2], 3)

    def test_quadratic_bad_folder(self):
        # same settings except output dir changed
        sim2 = self.sim
        sim2.output_dir = '/usr'
        with self.assertRaises(MyPyOptException):
            HeuristicSearch(sim2, self.dvs, self.io, self.sim_quadratic,
                            self.ssqe_quadratic, self.progress, self.completed)

    def test_duplicated_dv_names(self):
        these_dvs = self.dvs
        # same DVs except append a duplicate 'a' variable
        these_dvs.append(DecisionVariable(minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                          convergence_criterion=0.000001, variable_name='a'))
        with self.assertRaises(MyPyOptException):
            HeuristicSearch(self.sim, these_dvs, self.io, self.sim_quadratic,
                            self.ssqe_quadratic, self.progress, self.completed)


class TestDefaults(unittest.TestCase):
    """
    This unit test class is about testing out the default initializations of parameters passed into constructors
    """
    def test_minimal_two_var(self):
        """
        This test is a realistic, but quite minimal project setup where we are solving for a, b in a+bx
        """

        def sim_linear(parameter_hash):
            a, b = [parameter_hash[x] for x in ['a', 'b']]
            return [a + b * x for x in [0, 1, 2]]

        def calc_ssqe(sim_values):
            actual = [1 + 2 * x for x in [0, 1, 2]]
            return [(a - b) ** 2 for a, b in zip(actual, sim_values)]

        dvs = [DecisionVariable(variable_name='a'), DecisionVariable(variable_name='b')]
        io = InputOutputManager()
        sim = ProjectStructure(verbose=True)
        searcher = HeuristicSearch(sim, dvs, io, sim_linear, calc_ssqe)
        response = searcher.search()
        self.assertTrue(response.success)
        self.assertAlmostEqual(1.0, response.values[0], 2)
        self.assertAlmostEqual(2.0, response.values[1], 2)

    def test_minimal_minimal(self):
        """
        This test is an extremely minimal demonstration, where we are trying to solve for a, in the equation "a=4"
        This test demonstrates completely default parameters, lambdas instead of explicit functions, and
        returning a single, scalar variable from the sim function instead of an array or other structure
        """
        dvs = [DecisionVariable(variable_name='a')]
        io = InputOutputManager()
        sim = ProjectStructure()
        searcher = HeuristicSearch(sim, dvs, io, lambda x: x['a'], lambda x: (x-4)**2)
        response = searcher.search()
        self.assertTrue(response.success)
        self.assertAlmostEqual(4.0, response.values[0], 3)

# allow execution directly as python tests/test_main.py
if __name__ == '__main__':
    unittest.main()
