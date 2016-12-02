import json
import collections
import os
import time
import uuid

from Exceptions import MyPyOptException
from ObjectiveEvaluation import ObjectiveEvaluation
from Optimizer import Optimizer
from ReturnStateEnum import ReturnStateEnum
from SearchReturnType import SearchReturnType
from InputOutput import InputOutputManager


class HeuristicSearch(Optimizer):
    """
    This class implements a heuristic, multi-variable, search optimization technique.
    """
    def __init__(self, project_settings, decision_variable_array, callback_f_of_x,
                 callback_objective, input_output_worker=None, callback_progress=None, callback_completed=None):

        # not really needed, but avoids warnings
        super(Optimizer, self).__init__()

        # store the settings
        self.project = project_settings
        self.dvs = decision_variable_array
        if input_output_worker:
            self.io = input_output_worker
        else:
            self.io = InputOutputManager()

        # store the callback functions, which may be "None" for the progress/completed callbacks
        self.callback_f_of_x = callback_f_of_x
        self.callback_objective = callback_objective
        self.callback_progress = callback_progress
        self.callback_completed = callback_completed

        # the root project name is created/validated by the sim constructor, set up the folder for this particular run
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S')
        dir_name = os.path.join(self.project.output_dir, timestamp + "_" + self.project.project_name +
                                "_" + str(uuid.uuid4())[0:8])

        # so on Windows, as seen in issue #22, when the unit test would try to tell Windows to create a folder in /usr,
        #  it would fail badly, such that I couldn't raise the MyPyOptException at all.  So this is a workaround.
        if dir_name.startswith('/') and os.name == 'nt':
            raise MyPyOptException("Attempted to create Linux folder path on Windows, aborting...")

        try:
            os.mkdir(dir_name)
        except:
            raise MyPyOptException("Couldn't create project folder, check permissions, aborting...")

        # output optimization information so we don't have to look in the source
        project_info_file_name = os.path.join(dir_name, 'project_info.json')
        with open(project_info_file_name, 'w') as f:
            project_info = dict()
            project_info['project_name'] = self.project.project_name
            project_info['timestamp'] = timestamp
            project_info['decision_variables'] = [d.to_dictionary() for d in self.dvs]
            f.write(json.dumps(project_info, indent=2))

        # remove any previous files and open clean versions of the log files
        self.full_output_file = open(os.path.join(dir_name, 'full_output.log'), 'w')
        if os.path.exists(self.io.stopFile):
            try:
                os.remove(self.io.stopFile)
            except OSError:
                raise MyPyOptException("Found stop file, but couldn't remove it, check permissions, aborting...")

        # check the dv array for duplicate names, as this would be invalid
        var_names = [dv.var_name for dv in self.dvs]
        duplicate_names = [i for i, c in collections.Counter(var_names).items() if c > 1]
        if duplicate_names:
            raise MyPyOptException("Found duplicated names within decision variables, give each a unique name.")

    def search(self):
        """
        This is the main driver function for the optimization.
        It walks the parameter space finding a minimum objective function.
        """

        self.io.write_line(True, self.full_output_file, '\n*******Optimization Beginning*******')

        # evaluate starting point
        base_values = {dv.var_name: dv.x_base for dv in self.dvs}
        obj_base = self.f_of_x(base_values)
        j_base = obj_base.value
        if obj_base.return_state == ReturnStateEnum.UserAborted:
            self.io.write_line(True, self.full_output_file,
                               'User aborted simulation via stop signal file...')
            r = SearchReturnType(False, ReturnStateEnum.UserAborted)
            if self.callback_completed:
                self.callback_completed(r)
            return r
        elif not obj_base.return_state == ReturnStateEnum.Successful:
            self.io.write_line(True, self.full_output_file,
                               'Initial point is infeasible or invalid, cannot begin iterations.  Aborting...')
            r = SearchReturnType(False, ReturnStateEnum.InvalidInitialPoint)
            if self.callback_completed:
                self.callback_completed(r)
            return r

        # begin iteration loop
        for iteration in range(1, self.project.max_iterations + 1):

            self.io.write_line(self.project.verbose, self.full_output_file, 'iter = ' + str(iteration))

            if os.path.exists(self.io.stopFile):
                self.io.write_line(True, self.full_output_file,
                                   'Found stop signal file in run directory; stopping now...')
                r = SearchReturnType(False, ReturnStateEnum.UserAborted)
                if self.callback_completed:
                    self.callback_completed(r)
                return r

            # begin DV loop
            for dv in self.dvs:

                # setup a new point
                dv.x_new = dv.x_base + dv.delta_x
                new_values = {dv.var_name: dv.x_new for dv in self.dvs}

                if dv.x_new > dv.value_maximum or dv.x_new < dv.value_minimum:
                    self.io.write_line(True, self.full_output_file,
                                       'infeasible DV, name=' + dv.var_name)
                    r = SearchReturnType(False, ReturnStateEnum.InfeasibleDV)
                    if self.callback_completed:
                        self.callback_completed(r)
                    return r

                # then evaluate the new point
                obj_new = self.f_of_x(new_values)
                j_new = obj_new.value

                w = self.io.write_line
                w(self.project.verbose, self.full_output_file, 'iter=' + str(iteration))
                w(self.project.verbose, self.full_output_file, 'var=' + str(dv))
                w(self.project.verbose, self.full_output_file, 'x_base=' + str([x.x_base for x in self.dvs]))
                w(self.project.verbose, self.full_output_file, 'j_base=' + str(j_base))
                w(self.project.verbose, self.full_output_file, 'x_new=' + str([x.x_new for x in self.dvs]))
                w(self.project.verbose, self.full_output_file, 'j_new=' + str(j_new))

                if obj_new.return_state == ReturnStateEnum.UnsuccessfulOther:
                    self.io.write_line(True, self.full_output_file,
                                       'Optimization ended unexpectedly, check all inputs and outputs')
                    self.io.write_line(True, self.full_output_file,
                                       'Error message: ' + str(obj_new.message))
                    r = SearchReturnType(False, ReturnStateEnum.UnsuccessfulOther)
                    if self.callback_completed:
                        self.callback_completed(r)
                    return r
                elif (not obj_new.return_state == ReturnStateEnum.Successful) or (j_new > j_base):
                    dv.delta_x = -self.project.coefficient_contract * dv.delta_x
                    dv.x_new = dv.x_base
                    self.io.write_line(self.project.verbose, self.full_output_file,
                                       '## Unsuccessful objective evaluation, or worse result, going back ##')
                else:
                    j_base = j_new
                    dv.x_base = dv.x_new
                    dv.delta_x = self.project.coefficient_expand * dv.delta_x
                    self.io.write_line(self.project.verbose, self.full_output_file,
                                       '## Improved result, accepting and continuing forward ##')

            converged = True
            for dv in self.dvs:
                if abs(dv.delta_x) > dv.convergence_criteria:
                    converged = False
                    break

            if converged:
                self.io.write_line(True, self.full_output_file, '*******Converged*******')
                converged_values = {x.var_name: x.x_new for x in self.dvs}
                r = SearchReturnType(True, ReturnStateEnum.Successful, converged_values)
                if self.callback_completed:
                    self.callback_completed(r)
                return r

            if self.callback_progress:
                self.callback_progress(iteration, j_base)

    def f_of_x(self, parameter_hash):
        """
        This function calls the "f_of_x" callback function, getting outputs for the current parameter space;
        then passes those outputs into the objective function callback as an array, which usually returns the SSQE
        between known values and current outputs.
        """

        # run the simulation function
        simulation_results = self.callback_f_of_x(parameter_hash)

        # the sim function should return None if it failed (for now)
        if simulation_results:
            error_to_minimize = self.callback_objective(simulation_results)
            return ObjectiveEvaluation(ReturnStateEnum.Successful, error_to_minimize)
        else:
            return ObjectiveEvaluation(ReturnStateEnum.InfeasibleObj, None,
                                       'Function f(x) failed, probably infeasible output')
