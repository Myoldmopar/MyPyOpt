#!/usr/bin/env python

from pathlib import Path
import threading
from tkinter import Tk, TOP, BOTH
import collections

from mypyopt.project_structure import ProjectStructure
from mypyopt.input_output import InputOutputManager
from mypyopt.decision_variable import DecisionVariable
from mypyopt.optimizer_heuristic_search import HeuristicSearch

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# stuff for the plot
max_length = 60
x_var = collections.deque(maxlen=max_length)
y_var = collections.deque(maxlen=max_length)


# callbacks for the optimization
def progress(completed_iteration_number, latest_objective_function_value):
    x_var.append(completed_iteration_number)
    y_var.append(latest_objective_function_value)


# Actual "simulation"
def sim_quadratic(parameter_hash):
    x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    # for i in range(0, 100000):
    #     j = i**2
    return [parameter_hash['a'] + parameter_hash['b'] * x + parameter_hash['c'] * (x ** 2) for x in x_values]


# Squared Error expression
def sum_sq_err_quadratic(sim_values):
    x_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    actual_values = [1 + 2 * x + 3 * (x ** 2) for x in x_values]
    sqe = [(q - r) ** 2 for q, r in zip(actual_values, sim_values)]
    return sum(sqe)


class MyApp(Tk):

    def __init__(self, parent):
        super().__init__()
        self.wm_title("Embedding in TK")
        self.parent = parent
        fig = Figure(figsize=(5, 4), dpi=100)
        fig_sub_plot = fig.add_subplot(111)
        self.line1, = fig_sub_plot.plot([0], [0], 'r-')
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
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
                               project_name='TestProject',
                               output_dir_path=Path(__file__).resolve().parent.parent.parent / 'projects')
        searcher = HeuristicSearch(sim, dvs, sim_quadratic, sum_sq_err_quadratic, io, progress)
        self.thread1 = threading.Thread(target=searcher.search)
        # I know...I know this is bad; thread1 is going to make callbacks that eventually
        # hit the main GUI thread.  Tk isn't as simple as gtk and wx for transferring ownership to the
        # main thread, but after() seems to work, so I'm leaving it.
        self.thread1.start()

    def update_plot(self):
        if list(x_var) and list(y_var):
            self.line1.set_data(list(x_var), list(y_var))
            ax = self.canvas.figure.axes[0]
            ax.set_xlim(min(list(x_var)), max(list(x_var)))
            ax.set_ylim(min(list(y_var)), max(list(y_var)))
            self.canvas.draw()
        self.after(10, self.update_plot)


def run():
    a = MyApp(None)
    a.mainloop()


if __name__ == "__main__":
    run()
