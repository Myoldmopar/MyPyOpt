import os
import time
import json

from Enums import ReturnStateEnum
from ObjectiveEvaluation import ObjectiveEvaluation
from SearchReturnType import SearchReturnType
from Exceptions import MyPyOptException


class HeuristicSearch(object):
    def __init__(self, sim, dvs, io, sim_function, ssqe_function):

        # store the settings
        self.sim = sim
        self.dvs = dvs
        self.io = io
        self.sim_func = sim_function
        self.ssqe = ssqe_function

        # the root project name is created/validated by the sim constructor, set up the folder for this particular run
        timestamp = time.strftime('%Y-%m-%d-%H:%M:%S')
        dir_name = os.path.join(self.sim.output_dir, timestamp + self.sim.project_name)
        os.mkdir(dir_name)

        # output optimization information so we don't have to look in the source
        project_info_file_name = os.path.join(dir_name, 'project_info.json')
        with open(project_info_file_name, 'w') as f:
            project_info = dict()
            project_info['project_name'] = self.sim.project_name
            project_info['timestamp'] = timestamp
            project_info['decision_variables'] = [d.to_dictionary() for d in self.dvs]
            f.write(json.dumps(project_info, indent=2))

        # remove any previous files and open clean versions of the log files
        self.full_output_file = open(os.path.join(dir_name, 'full_output.log'), 'w')
        if os.path.exists(io.stopFile):
            try:
                os.remove(io.stopFile)
            except OSError:
                raise MyPyOptException("Found stop file, but couldn't remove it, check permissions, aborting...")

    def search(self):

        self.io.write_line(True, self.full_output_file, '*******Optimization Beginning*******')

        # evaluate starting point
        base_values = {dv.var_name: dv.x_base for dv in self.dvs}
        obj_base = self.f_of_x(base_values)
        j_base = obj_base.value
        if obj_base.return_state == ReturnStateEnum.UserAborted:
            self.io.write_line(True, self.full_output_file,
                               'User aborted simulation via stop signal file...')
            return SearchReturnType(False, ReturnStateEnum.UserAborted)
        elif not obj_base.return_state == ReturnStateEnum.Successful:
            self.io.write_line(True, self.full_output_file,
                               'Initial point is infeasible or invalid, cannot begin iterations.  Aborting...')
            return SearchReturnType(False, ReturnStateEnum.InvalidInitialPoint)

        # begin iteration loop
        for iteration in range(1, self.sim.max_iterations + 1):

            self.io.write_line(True, self.full_output_file, '*****')
            self.io.write_line(True, self.full_output_file, 'iter = ' + str(iteration))

            if os.path.exists(self.io.stopFile):
                self.io.write_line(True, self.full_output_file,
                                   'Found stop signal file in run directory; stopping now...')
                return SearchReturnType(False, ReturnStateEnum.UserAborted)

            # begin DV loop
            for dv in self.dvs:

                # setup a new point
                dv.x_new = dv.x_base + dv.delta_x
                new_values = {dv.var_name: dv.x_new for dv in self.dvs}

                if dv.x_new > dv.value_maximum or dv.x_new < dv.value_minimum:
                    self.io.write_line(True, self.full_output_file,
                                       'infeasible DV, name=' + dv.var_name)
                    return SearchReturnType(False, ReturnStateEnum.InfeasibleDV)

                # then evaluate the new point
                obj_new = self.f_of_x(new_values)
                j_new = obj_new.value

                self.io.write_line(True, self.full_output_file, 'iter=' + str(iteration))
                self.io.write_line(True, self.full_output_file, 'var=' + str(dv))
                self.io.write_line(True, self.full_output_file, 'x_base=' + str([x.x_base for x in self.dvs]))
                self.io.write_line(True, self.full_output_file, 'j_base=' + str(j_base))
                self.io.write_line(True, self.full_output_file, 'x_new=' + str([x.x_new for x in self.dvs]))
                self.io.write_line(True, self.full_output_file, 'j_new=' + str(j_new))

                if obj_new.return_state == ReturnStateEnum.UnsuccessfulOther:
                    self.io.write_line(True, self.full_output_file,
                                       'Optimization ended unexpectedly, check all inputs and outputs')
                    self.io.write_line(True, self.full_output_file,
                                       'Error message: ' + str(obj_new.message))
                    return SearchReturnType(False, ReturnStateEnum.UnsuccessfulOther)
                elif (not obj_new.return_state == ReturnStateEnum.Successful) or (j_new > j_base):
                    dv.delta_x = -self.sim.coefficient_contract * dv.delta_x
                    dv.x_new = dv.x_base
                    self.io.write_line(True, self.full_output_file,
                                       '## Unsuccessful objective evaluation, or worse result, going back ##')
                else:
                    j_base = j_new
                    dv.x_base = dv.x_new
                    dv.delta_x = self.sim.coefficient_expand * dv.delta_x
                    self.io.write_line(True, self.full_output_file,
                                       '## Improved result, accepting and continuing forward ##')

            converged = True
            for dv in self.dvs:
                if abs(dv.delta_x) > dv.convergence_criteria:
                    converged = False
                    break

            if converged:
                self.io.write_line(True, self.full_output_file, 'converged')
                converged_values = [x.x_new for x in self.dvs]
                return SearchReturnType(True, ReturnStateEnum.Successful, converged_values)

    # raw data sum of square error
    def f_of_x(self, parameter_hash):

        # run the simulation function
        current_f = self.sim_func(parameter_hash)

        # the sim function should return None if it failed (for now)
        if current_f:
            sum_squares_error = self.ssqe(current_f)
            return ObjectiveEvaluation(ReturnStateEnum.Successful, sum_squares_error)
        else:
            return ObjectiveEvaluation(ReturnStateEnum.InfeasibleObj, None,
                                       'Function f(x) failed, probably infeasible output')
