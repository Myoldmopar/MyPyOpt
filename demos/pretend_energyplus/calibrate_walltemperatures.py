#!/usr/bin/python

import sys
import os
import csv
import subprocess

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_dir, '../..'))

from mypyopt.SimulationStructure import SimulationStructure
from mypyopt.InputOutput import InputOutputManager
from mypyopt.DecisionVariable import DecisionVariable
from mypyopt.Optimizer import HeuristicSearch


# Actual "simulation"
def sim_pretend_energyplus(parameter_hash):
    resistance_value = parameter_hash['wall_resistance']
    min_outdoor_temp = parameter_hash['min_outdoor_temp']
    template_contents = open(os.path.join(this_dir, 'in_template.json')).read()
    new_contents = template_contents.replace('{wall_resistance}',
                                             str(resistance_value)).replace('{min_outdoor_temp}', str(min_outdoor_temp))
    open(os.path.join(this_dir, 'in.json'), 'w').write(new_contents)
    subprocess.call([os.path.join(this_dir, 'pretend_energyplus.py'),
                    str(resistance_value)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    f = open(os.path.join(this_dir, 'out.csv'))
    reader = csv.reader(f)
    surface_temps = list()
    for row in reader:
        surface_temps.append(float(row[1]))
    return surface_temps


# Squared Error expression
def ssqe_pretend_energyplus(sim_values):
    measured_temps = [22.790, 22.519, 22.789, 22.736, 22.948, 22.827, 22.988, 22.921,
                      23.204, 23.211, 23.351, 23.678, 24.236, 24.062, 24.319, 24.535,
                      24.735, 23.987, 23.947, 23.436, 23.465, 23.094, 22.904, 22.532]
    sqe = [(a - b) ** 2 for a, b in zip(measured_temps, sim_values)]
    return sum(sqe)


# Initialize list of decision variables
dvs = list()
dvs.append(DecisionVariable(-10, 10, 1, 1, 0.0001, 'wall_resistance'))  # opt value = 2
dvs.append(DecisionVariable(-100, 100, 10, 1, 0.0001, 'min_outdoor_temp'))  # opt value = 20

# Initialize the IO manager
io = InputOutputManager()

sim = SimulationStructure(1.2, 0.85, 2000, 'RunPretendEnergyPlus', 'projects', True)
searcher = HeuristicSearch(sim, dvs, io, sim_pretend_energyplus, ssqe_pretend_energyplus)
response = searcher.search()