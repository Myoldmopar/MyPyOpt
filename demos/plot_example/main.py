#!/usr/bin/env python
import sys
import threading
import Tkinter
import collections
import os

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_dir, '..', '..'))

from mypyopt.ProjectStructure import ProjectStructure
from mypyopt.InputOutput import InputOutputManager
from mypyopt.DecisionVariable import DecisionVariable
from mypyopt.OptimizerHeuristicSearch import HeuristicSearch


# stuff for the plot
max_length = 60
xvar = collections.deque(maxlen=max_length)
yvar = collections.deque(maxlen=max_length)


# callbacks for the optimization
def progress(completed_iteration_number, latest_objective_function_value):
    xvar.append(completed_iteration_number)
    yvar.append(latest_objective_function_value)


# Actual "simulation"
def sim_quadratic(parameter_hash):
    x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    for i in range(0, 100000):
        j = i**2
    return [parameter_hash['a'] + parameter_hash['b'] * x + parameter_hash['c'] * (x ** 2) for x in x_values]


# Squared Error expression
def ssqe_quadratic(sim_values):
    x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    actual_values = [1 + 2 * x + 3 * (x ** 2) for x in x_values]
    sqe = [(a - b) ** 2 for a, b in zip(actual_values, sim_values)]
    return sum(sqe)


class MyApp(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.wm_title("Embedding in TK")
        self.parent = parent
        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        fig_sub_plot = fig.add_subplot(111)
        self.line1, = fig_sub_plot.plot([0], [0], 'r-')
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.resizable(True, False)
        self.update_plot()

        # optimization stuff
        dvs = list()
        dvs.append(DecisionVariable('a', minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                    convergence_criterion=0.000001))  # opt value = 1
        dvs.append(DecisionVariable('b', minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                    convergence_criterion=0.000001))  # opt value = 2
        dvs.append(DecisionVariable('c', minimum=-5, maximum=5, initial_value=0.5, initial_step_size=0.1,
                                    convergence_criterion=0.000001))  # opt value = 3
        io = InputOutputManager()
        sim = ProjectStructure(expansion=1.2, contraction=0.85, max_iterations=2000,
                               project_name='TestProject', output_dir='projects')
        searcher = HeuristicSearch(sim, dvs, sim_quadratic, ssqe_quadratic, io, progress)
        self.thread1 = threading.Thread(target=searcher.search)
        # I know...I know this is bad; thread1 is going to make callbacks that eventually
        # hit the main GUI thread.  Tk isn't as simple as gtk and wx for transferring ownership to the
        # main thread, but after() seems to work, so I'm leaving it.
        self.thread1.start()

    def update_plot(self):
        if list(xvar) and list(yvar):
            self.line1.set_data(list(xvar), list(yvar))
            ax = self.canvas.figure.axes[0]
            ax.set_xlim(min(list(xvar)), max(list(xvar)))
            ax.set_ylim(min(list(yvar)), max(list(yvar)))
            self.canvas.draw()
        self.after(10, self.update_plot)


a = MyApp(None)
Tkinter.mainloop()


