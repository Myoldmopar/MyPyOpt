from Exceptions import MyPyOptException


class Optimizer(object):
    """
    This is a base class of an Optimizer to define the interface
    """

    def __init__(self, project_settings, decision_variable_array, input_output_worker, callback_f_of_x,
                 callback_objective,
                 callback_progress=None, callback_completed=None):
        """
        The constructor for the class.

        :param project_settings: A ProjectStructure instance defining the high level project settings
        :param decision_variable_array: An array of DecisionVariable instances defining the parameter space
        :param input_output_worker: An InputOutput instance to allow easy access to IO operations
        :param callback_f_of_x: A Python function that accepts a dictionary of parameters where each key is the name
                                defined in the decision variable instance, and the value is the current value of that
                                variable.  The function return value is completely user defined, and will be passed
                                into the objective callback function.  A typical object would be an array of hourly
                                output values, or possibly a hash of values.
        :param callback_objective: A Python function that accepts a single argument.
                                   This argument is exactly what comes out of the simulation (f_of_x) function.
                                   The user can choose to return an array, a hash, whatever.
                                   simulation run, to be used in comparing to some baseline
        :param callback_progress: An optional callback function that gets called each iteration and passed in an
                                   iteration number and the latest objective value (for now -- will add more info later)
        :param callback_completed: An optional callback function that gets called at the end of the optimization search,
                                   with a SearchReturnType instance as the only argument
        """
        pass

    def search(self):
        """
        This is the main driver function for the optimization.
        It walks the parameter space finding a minimum objective function.
        Requirements: call callback_progress and callback_completed as needed
        Call f(x) with a hash of parameter names and values
        """
        raise MyPyOptException(
            "Tried to use search() on the Optimizer base class; verify derived class overrides this method")

    def f_of_x(self, parameter_hash):
        """
        This function calls the "f_of_x" callback function, getting outputs for the current parameter space;
        then passes those outputs into the objective function callback as an array, which usually returns the SSQE
        between known values and current outputs.

        :param parameter_hash: A dictionary of parameters with keys as the variable names, and current variable values
        """
        raise MyPyOptException(
            "Tried to use f_of_x() on the Optimizer base class; verify derived class overrides this method")
