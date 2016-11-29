from Exceptions import MyPyOptException


class DecisionVariable(object):
    def __init__(self, minimum, maximum, initial_value, initial_step_size, convergence_criterion, variable_name):
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
        d = dict()
        d['value_minimum'] = self.value_minimum
        d['value_maximum'] = self.value_maximum
        d['value_initial'] = self.value_initial
        d['step_size_initial'] = self.step_size_initial
        d['convergence_criteria'] = self.convergence_criteria
        d['var_name'] = self.var_name
        return d
