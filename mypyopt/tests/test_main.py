from pathlib import Path
from tempfile import mkdtemp
import unittest

from mypyopt.project_structure import ProjectStructure
from mypyopt.input_output import InputOutputManager
from mypyopt.decision_variable import DecisionVariable
from mypyopt.optimizer import Optimizer
from mypyopt.optimizer_heuristic_search import HeuristicSearch
from mypyopt.exceptions import MyPyOptException
from mypyopt.return_state_enum import ReturnStateEnum


class TestQuadratic(unittest.TestCase):
    def setUp(self):
        """
        This sets up a 3 coefficient quadratic optimization; each individual test_ cases should override any of
        the default structures set up here, but not modify them directly
        """
        # Initialize list of decision variables
        # DecisionVariable(min, max, initial_value, initial_step_size, convergence_criterion, variable_name)
        self.dvs = list()
        self.dvs.append(DecisionVariable('a', minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                         convergence_criterion=0.000001))  # opt value = 1
        self.dvs.append(DecisionVariable('b', minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                         convergence_criterion=0.000001))  # opt value = 2
        self.dvs.append(DecisionVariable('c', minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                         convergence_criterion=0.000001))  # opt value = 3

        # Initialize the IO manager
        self.io = InputOutputManager()

        # Initialize a project structure
        self.sim = ProjectStructure(expansion=1.2, contraction=.85, max_iterations=2000, project_name='TestProject',
                                    output_dir_path=Path(__file__).resolve().parent.parent.parent / 'projects')

    # Actual "simulation"
    @staticmethod
    def sim_quadratic(parameter_hash):
        x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        return [parameter_hash['a'] + parameter_hash['b'] * x + parameter_hash['c'] * (x ** 2) for x in x_values]

    # Squared Error expression
    @staticmethod
    def sum_squared_error_quadratic(sim_values):
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
        searcher = HeuristicSearch(self.sim, self.dvs, self.sim_quadratic,
                                   self.sum_squared_error_quadratic, self.io, self.progress, self.completed)
        response = searcher.search()
        self.assertTrue(response.success)
        self.assertAlmostEqual(1.0, response.values['a'], 3)
        self.assertAlmostEqual(2.0, response.values['b'], 3)
        self.assertAlmostEqual(3.0, response.values['c'], 3)

    def test_quadratic_bad_folder(self):
        # same settings except output dir changed
        sim2 = self.sim
        sim2.output_dir = '/usr'
        with self.assertRaises(MyPyOptException):
            HeuristicSearch(sim2, self.dvs, self.sim_quadratic,
                            self.sum_squared_error_quadratic, self.io, self.progress, self.completed)

    def test_duplicated_dv_names(self):
        these_dvs = self.dvs
        # same DVs except append a duplicate 'a' variable
        these_dvs.append(DecisionVariable('a', minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                          convergence_criterion=0.000001))
        with self.assertRaises(MyPyOptException):
            HeuristicSearch(self.sim, these_dvs, self.sim_quadratic,
                            self.sum_squared_error_quadratic, self.io, self.progress, self.completed)

    def test_heuristic_bad_init_value(self):
        searcher = HeuristicSearch(self.sim, self.dvs, lambda _: None, self.sum_squared_error_quadratic,
                                   callback_completed=lambda _: None)
        response = searcher.search()
        self.assertFalse(response.success)
        self.assertEqual(ReturnStateEnum.InvalidInitialPoint, response.reason)


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

        def calc_sum_squared_error(sim_values):
            actual = [1 + 2 * x for x in [0, 1, 2]]
            return [(a - b) ** 2 for a, b in zip(actual, sim_values)]

        dvs = [DecisionVariable('a'), DecisionVariable('b')]
        sim = ProjectStructure(verbose=True)
        searcher = HeuristicSearch(sim, dvs, sim_linear, calc_sum_squared_error)
        response = searcher.search()
        self.assertTrue(response.success)
        self.assertAlmostEqual(1.0, response.values['a'], 2)
        self.assertAlmostEqual(2.0, response.values['b'], 2)

    def test_minimal_minimal(self):
        """
        This test is an extremely minimal demonstration, where we are trying to solve for "a", in the equation "a=4"
        This test demonstrates completely default parameters, lambdas instead of explicit functions, and
        returning a single, scalar variable from the sim function instead of an array or other structure
        """
        dvs = [DecisionVariable('a')]
        sim = ProjectStructure()
        searcher = HeuristicSearch(sim, dvs, lambda x: x['a'], lambda x: (x-4)**2)
        response = searcher.search()
        self.assertTrue(response.success)
        self.assertAlmostEqual(4.0, response.values['a'], 3)


class TestDecisionVariables(unittest.TestCase):
    def test_bad_inputs(self):
        with self.assertRaises(MyPyOptException):
            DecisionVariable('var_name', minimum=1.0, maximum=0.0)
        with self.assertRaises(MyPyOptException):
            DecisionVariable('var_name', initial_step_size=-1)
        with self.assertRaises(MyPyOptException):
            DecisionVariable('var_name', convergence_criterion=-1)


class TestBaseOptimizerAbstraction(unittest.TestCase):
    def test_abstraction(self):
        dvs = [DecisionVariable('a'), DecisionVariable('b')]
        sim = ProjectStructure(verbose=True)
        o = Optimizer(sim, dvs, lambda: None, lambda: [1])
        with self.assertRaises(MyPyOptException):
            o.search()
        with self.assertRaises(MyPyOptException):
            o.f_of_x({})


class TestReturnStateEnums(unittest.TestCase):
    def test_all_enums(self):
        all_enums = ReturnStateEnum.all_enums()
        for e in all_enums:
            self.assertIsInstance(ReturnStateEnum.enum_to_string(e), str)


class TestProjectStructureConstruction(unittest.TestCase):
    def test_it_creates_output_folder(self):
        temp_output_dir = Path(mkdtemp())
        temp_output_dir.rmdir()
        self.assertFalse(temp_output_dir.exists())
        ProjectStructure(output_dir_path=temp_output_dir)
        self.assertTrue(temp_output_dir.exists())

    def test_bad_inputs(self):
        with self.assertRaises(MyPyOptException):
            ProjectStructure(expansion=0.5)
        with self.assertRaises(MyPyOptException):
            ProjectStructure(contraction=2.5)
        with self.assertRaises(MyPyOptException):
            ProjectStructure(max_iterations=0)
