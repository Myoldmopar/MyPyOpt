from mypyopt.exceptions import MyPyOptException


class DecisionVariable:
    """
    A structure for defining a single dimension in the optimization parameter space
    """
    def __init__(self,
                 variable_name: str, minimum: float = -10000, maximum: float = 10000,
                 initial_value: float = 1, initial_step_size: float = 0.1, convergence_criterion: float = 0.001
                 ):
        """
        The constructor for this class, which does all initialization, at a minimum, the user should
        define the variable_name, the others can be left defaulted if desired

        :param variable_name: A required string ID for this variable that is used in callback functions
        :param minimum: The minimum value allowed for this decision variable during the optimization process
        :param maximum: The maximum value allowed for this decision variable during the optimization process
        :param initial_value: The initial value of this decision variable for creating the initial point
        :param initial_step_size: The initial step size when walking this decision variable around the parameter space
        :param convergence_criterion: The maximum change between two iterations to specify this variable as converged
        :raises MyPyOptException: If the numeric conditions given in the arguments are invalid
        """
        if minimum > maximum or initial_step_size <= 0 or convergence_criterion <= 0:
            raise MyPyOptException("Invalid parameters in DV definition for DV with name: " + str(variable_name))
        self.value_minimum = minimum
        self.value_maximum = maximum
        self.value_initial = initial_value
        self.step_size_initial = initial_step_size
        self.convergence_criteria = convergence_criterion
        self.var_name = variable_name
        self.x_base = initial_value
        self.x_new = initial_value
        self.delta_x = initial_step_size

    def to_dictionary(self) -> dict:
        """
        Converts the meaningful parts of this decision variable into a dictionary for project summary reports

        :return: Dictionary of decision variable information
        """
        d = dict()
        d['value_minimum'] = self.value_minimum
        d['value_maximum'] = self.value_maximum
        d['value_initial'] = self.value_initial
        d['step_size_initial'] = self.step_size_initial
        d['convergence_criteria'] = self.convergence_criteria
        d['var_name'] = self.var_name
        return d
