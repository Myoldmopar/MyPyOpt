#!/usr/bin/python
from pathlib import Path

from mypyopt.project_structure import ProjectStructure
from mypyopt.input_output import InputOutputManager
from mypyopt.decision_variable import DecisionVariable
from mypyopt.optimizer_heuristic_search import HeuristicSearch
from mypyopt.demos.pretend_energyplus.pretend_energyplus import pretend_e_plus

this_dir = Path(__file__).resolve().parent


# Actual "simulation"
def sim_pretend_energyplus(parameter_hash):
    resistance_value = parameter_hash['wall_resistance']
    min_outdoor_temp = parameter_hash['min_outdoor_temp']
    template_contents = (this_dir / 'in_template.json').read_text()
    new_contents = template_contents.replace('{wall_resistance}',
                                             str(resistance_value)).replace('{min_outdoor_temp}', str(min_outdoor_temp))
    # pretend we are writing new_contents to a real IDF/EpJSON file
    # pretend we are doing a subprocess call out to EnergyPlus.exe
    csv_data = pretend_e_plus(new_contents)
    surface_temps = [x[1] for x in csv_data]
    return surface_temps


# Squared Error expression
def sum_sq_err_pretend_energyplus(sim_values):
    measured_temps = [22.790, 22.519, 22.789, 22.736, 22.948, 22.827, 22.988, 22.921,
                      23.204, 23.211, 23.351, 23.678, 24.236, 24.062, 24.319, 24.535,
                      24.735, 23.987, 23.947, 23.436, 23.465, 23.094, 22.904, 22.532]
    sqe = [(a - b) ** 2 for a, b in zip(measured_temps, sim_values)]
    return sum(sqe)


def run():
    # Initialize list of decision variables
    dvs = list()
    dvs.append(DecisionVariable('wall_resistance', minimum=-10, maximum=10, initial_value=1, initial_step_size=1,
                                convergence_criterion=0.0001))  # opt value = 2
    dvs.append(DecisionVariable('min_outdoor_temp', minimum=-100, maximum=100, initial_value=10, initial_step_size=1,
                                convergence_criterion=0.0001))  # opt value = 20

    # Initialize the IO manager
    io = InputOutputManager()

    sim = ProjectStructure(expansion=1.2, contraction=0.85, max_iterations=2000,
                           project_name='RunPretendEnergyPlus',
                           output_dir_path=Path(__file__).resolve().parent.parent.parent / 'projects', verbose=True
                           )
    searcher = HeuristicSearch(sim, dvs, sim_pretend_energyplus, sum_sq_err_pretend_energyplus, io)
    searcher.search()


if __name__ == "__main__":  # pragma: no cover
    run()
