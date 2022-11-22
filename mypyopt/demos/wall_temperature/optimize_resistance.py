#!/usr/bin/python

from pathlib import Path
import os
import subprocess

from mypyopt.project_structure import ProjectStructure
from mypyopt.input_output import InputOutputManager
from mypyopt.decision_variable import DecisionVariable
from mypyopt.optimizer_heuristic_search import HeuristicSearch


# Actual "simulation"
def sim_wall_heat_transfer(parameter_hash):
    resistance_value = parameter_hash['wall_resistance']
    p = subprocess.Popen(['python', os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                 'calculate_wall_temperature.py'),
                          str(resistance_value)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out_bytes, _ = p.communicate()
    out_string = out_bytes.decode('utf-8').strip()
    return [float(out_string)]


# Squared Error expression
def sum_sq_err_wall_heat_flux(sim_values):
    measured_heat_flux = 0.5
    simulated_heat_flux = sim_values[0]
    sqe = (measured_heat_flux-simulated_heat_flux)**2
    return sqe


def run():
    # Initialize list of decision variables
    dvs = list()
    dvs.append(DecisionVariable('wall_resistance', minimum=0, maximum=100, initial_value=10, initial_step_size=1,
                                convergence_criterion=0.001))  # opt value = 20

    # Initialize the IO manager
    io = InputOutputManager()

    sim = ProjectStructure(expansion=1.2, contraction=0.85, max_iterations=2000, project_name='CalibrateWallResistance',
                           output_dir_path=Path(__file__).resolve().parent.parent.parent / 'projects', verbose=True)
    searcher = HeuristicSearch(sim, dvs, sim_wall_heat_transfer, sum_sq_err_wall_heat_flux, io)
    searcher.search()


if __name__ == "__main__":  # pragma: no cover
    run()
