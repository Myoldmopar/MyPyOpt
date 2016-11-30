from Exceptions import MyPyOptException


class Optimizer(object):
    """
    This is a base class of an Optimizer to define the interface
    """

    def __init__(self, project_settings, decision_variable_array, input_output_worker, cb_f_of_x, cb_objective,
                 cb_progress=None, cb_completed=None):
        pass

    def search(self):
        """
        This is the main driver function for the optimization.
        It walks the parameter space finding a minimum objective function.
        Requirements: call cb_progress and cb_completed as needed
        Call f(x) with a hash of parameter names and values
        """
        raise MyPyOptException("Tried to use search() on the Optimizer base class; verify derived class overrides this method")

    def f_of_x(self, parameter_hash):
        """
        This function calls the "f_of_x" callback function, getting outputs for the current parameter space;
        then passes those outputs into the objective function callback as an array, which usually returns the SSQE
        between known values and current outputs.
        """
        raise MyPyOptException("Tried to use f_of_x() on the Optimizer base class; verify derived class overrides this method")