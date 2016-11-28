class DecisionVariable(object):
    def __init__(self, minimum, maximum, initial_value, initial_step_size, convergence_criterion, variable_name):
        self.value_minimum = minimum
        self.value_maximum = maximum
        self.value_initial = initial_value
        self.step_size_initial = initial_step_size
        self.convergence_criteria = convergence_criterion
        self.var_name = variable_name


class SimulationStructure(object):
    def __init__(self, expansion, contraction, max_iterations):
        self.coeff_expand = expansion
        self.coeff_contract = contraction
        self.max_iterations = max_iterations


class ReturnStateEnum(object):
    Return_state_infeasibleDV = -1
    Return_state_infeasibleObj = -2
    Return_state_unsuccessfulOther = -3
    Return_state_successful = -4
    Return_state_useraborted = -5


class ObjectiveEvaluation(object):
    def __init__(self):
        self.return_state = 0
        self.message = ''
        self.value = 0.0
