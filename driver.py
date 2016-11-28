from mypyopt.structures import DecisionVariable, SimulationStructure
from mypyopt.inputoutput import InputOutputManager
from mypyopt.optimizer import HeuristicSearch

# Initialize simulation structure
# SimulationStructure(expansion, contraction, max_iterations)
sim = SimulationStructure(1.2, 0.85, 2000)

# Initialize list of decision variables
# DecisionVariable(min, max, initial_value, initial_step_size, convergence_criterion, variable_name)
dvs = list()
dvs.append(DecisionVariable(-5, 5, 0.5, 0.1, 0.0000000001, 'a'))  # opt value = 1
dvs.append(DecisionVariable(-5, 5, 0.5, 0.1, 0.0000000001, 'b'))  # opt value = 2
dvs.append(DecisionVariable(-5, 5, 0.5, 0.1, 0.0000000001, 'c'))  # opt value = 3

# Initialize the IO manager
io = InputOutputManager()


# Actual "simulation"
def sim_quadratic(parameter_hash):
    x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    return [parameter_hash['a'] + parameter_hash['b']*x + parameter_hash['c']*(x**2) for x in x_values]


# Squared Error expression
def ssqe_quadratic(sim_values):
    x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    actual_values = [1 + 2*x + 3*(x**2) for x in x_values]
    sqe = [(a - b)**2 for a, b in zip(actual_values, sim_values)]
    return sum(sqe)


# run the optimizer
searcher = HeuristicSearch(sim, dvs, io, sim_quadratic, ssqe_quadratic)
