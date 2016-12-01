from Exceptions import MyPyOptException


class DecisionVariable(object):
    """
    A structure for defining a single dimension in the optimization parameter space
    """
    def __init__(self, minimum=-10000, maximum=10000, initial_value=1, initial_step_size=0.1,
                 convergence_criterion=0.001, variable_name='dummy_dv_name'):
        """
        The constructor for this class, which does all initialization, at a minimum, the user should
        define the variable_name, the others can be left defaulted if desired

        :param minimum: The minimum value allowed for this decision variable during the optimization process
        :param maximum: The maximum value allowed for this decision variable during the optimization process
        :param initial_value: The initial value of this decision variable for creating the initial point
        :param initial_step_size: The initial step size when walking this decision variable around the parameter space
        :param convergence_criterion: The maximum change between two iterations to specify this variable as converged
        :param variable_name: A string ID for this variable that is used in callback functions
        :raises MyPyOptException: If the numeric conditions given in the arguments are invalid
        """
        if not variable_name:
            variable_name = "BLANK DV NAME"
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

    def to_dictionary(self):
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
