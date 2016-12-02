#!/usr/bin/python

import sys
import os
import subprocess

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from mypyopt.ProjectStructure import ProjectStructure
from mypyopt.InputOutput import InputOutputManager
from mypyopt.DecisionVariable import DecisionVariable
from mypyopt.OptimizerHeuristicSearch import HeuristicSearch


# Actual "simulation"
def sim_wall_heat_transfer(parameter_hash):
    resistance_value = parameter_hash['wall_resistance']
    p = subprocess.Popen([os.path.join(os.path.dirname(os.path.realpath(__file__)), 'calculate_wall_temperature.py'),
                          str(resistance_value)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate()
    return [float(str(out).strip())]


# Squared Error expression
def ssqe_wall_heat_flux(sim_values):
    measured_heat_flux = 0.5
    simulated_heat_flux = sim_values[0]
    sqe = (measured_heat_flux-simulated_heat_flux)**2
    return sqe


# Initialize list of decision variables
dvs = list()
dvs.append(DecisionVariable('wall_resistance', minimum=0, maximum=100, initial_value=10, initial_step_size=1,
                            convergence_criterion=0.001))  # opt value = 20

# Initialize the IO manager
io = InputOutputManager()

sim = ProjectStructure(expansion=1.2, contraction=0.85, max_iterations=2000, project_name='CalibrateWallResistance',
                       output_dir='projects', verbose=True)
searcher = HeuristicSearch(sim, dvs, sim_wall_heat_transfer, ssqe_wall_heat_flux, io)
searcher.search()
