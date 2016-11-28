import os
import time
import subprocess

from structures import ReturnStateEnum, ObjectiveEvaluation
from inputoutput import IOErrorReturnValues


class HeuristicSearch(object):

    def __init__(self, sim, dvs, io, sim_function, ssqe_function):

        # store the settings
        self.sim = sim
        self.dvs = dvs
        self.io = io
        self.sim_func = sim_function
        self.ssqe = ssqe_function

        # set this flag for later inspection
        self.status = IOErrorReturnValues.Success

        # validate DV array, it must have upper bound <= 9 because of the sed operation and format statement
        if len(dvs) > 9:
            print('DV array upper bound > 9, aborting...')
            self.status = IOErrorReturnValues.Err_InvalidDVarray
            return

        # validate DV array, use the convergence criterion init value as a flag for non-initialized array items
        if any([x.convergence_criteria == 0 for x in dvs]):
            print('DV array contains an item with zero convergence criteria, verify numDVs parameter, aborting...')
            self.status = IOErrorReturnValues.Err_InvalidDVarray
            return

        # output optimization information so we don't have to look in the source
        with open('OptimizationProjectInformation.txt', 'w') as f:
            f.writeline("Variable Name, Min Value, Max Value, Initial Value, Initial Step Size, Convergence Criterion")
            for dv in dvs:
                f.writeline(','.join(str(x) for x in [dv.var_name, dv.value_minimum, dv.value_maximum, dv.value_initial,
                                  dv.step_size_initial, dv.convergence_criteria]))

        timestamp = time.strftime('%Y-%m-%d-%H:%M:%S')
        full_output_file_name = 'FullOutput_' + timestamp + '.log'
        opt_output_file_name = 'OptimizationProgress_' + timestamp + '.log'

        # remove any previous files and open clean versions of the log files
        self.full_output_file = open(full_output_file_name, 'w')
        self.opt_output_file = open(opt_output_file_name, 'w')
        if os.path.exists(io.stopFile):
            os.remove(io.stopFile)

        # start iterating!
        self.perform_iteration_loop()

    def perform_iteration_loop(self):

        # initialize arrays according to incoming DV structure
        x_base = [x.value_initial for x in self.dvs]
        x_new = [x.value_initial for x in self.dvs]
        delta_x = [x.step_size_initial for x in self.dvs]

        self.io.write_line(True, self.full_output_file, self.opt_output_file, '*******Optimization Beginning*******')

        # evaluate starting point
        obj_base = self.f_of_x(x_base)
        j_base = obj_base.value
        if obj_base.return_state == ReturnStateEnum.Return_state_useraborted:
            self.io.write_line(True, self.full_output_file, self.opt_output_file,
                               'User aborted simulation via stop signal file...')
        elif not obj_base.return_state == ReturnStateEnum.Return_state_successful:
            self.io.write_line(True, self.full_output_file, self.opt_output_file,
                               'Initial point is infeasible or invalid, cannot begin iterations.  Aborting...')
            return IOErrorReturnValues.Err_InvalidInitialPoint

        # begin iteration loop
        for iteration in range(1, self.sim.max_iterations+1):

            self.io.write_line(True, self.full_output_file, self.opt_output_file, '*****')
            self.io.write_line(True, self.full_output_file, self.opt_output_file, 'iter = ' + str(iteration))

            if os.path.exists(self.io.stopFile):
                self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                   'Found stop signal file in run directory; stopping now...')
                return IOErrorReturnValues.Err_FoundStopFile

            # begin DV loop
            ctr = -1
            for dv in self.dvs:
                ctr += 1

                # evaluate a new point
                x_new[ctr] = x_base[ctr] + delta_x[ctr]
                obj_new = self.f_of_x(x_new)
                j_new = obj_new.value

                self.io.write_line(True, self.full_output_file, self.opt_output_file, 'iter=' + str(iteration))
                self.io.write_line(True, self.full_output_file, self.opt_output_file, 'var=' + str(dv))
                self.io.write_line(True, self.full_output_file, self.opt_output_file, 'x_base=' + str(x_base))
                self.io.write_line(True, self.full_output_file, self.opt_output_file, 'j_base=' + str(j_base))
                self.io.write_line(True, self.full_output_file, self.opt_output_file, 'x_new=' + str(x_new))
                self.io.write_line(True, self.full_output_file, self.opt_output_file, 'j_new=' + str(j_new))

                if obj_new.return_state == ReturnStateEnum.Return_state_unsuccessfulOther:
                    self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                       'Optimization ended unexpectedly, check all inputs and outputs')
                    self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                       'Error message: ' + str(obj_new.message))
                    return IOErrorReturnValues.Err_UnexpectedError
                elif (not obj_new.return_state == ReturnStateEnum.Return_state_successful) or (j_new > j_base):
                    delta_x[ctr] = -self.sim.coeff_contract * delta_x[ctr]
                    x_new[ctr] = x_base[ctr]
                    self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                       '## Unsuccessful objective evaluation, or worse result, going back ##')
                else:
                    j_base = j_new
                    x_base[ctr] = x_new[ctr]
                    delta_x[ctr] = self.sim.coeff_expand * delta_x[ctr]
                    self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                       '## Improved result, accepting and continuing forward ##')

            converged = True
            ctr = -1
            for dv in self.dvs:
                ctr += 1
                if abs(delta_x[ctr]) > dv.convergence_criteria:
                    converged = False
                    break

            if converged:
                self.io.write_line(True, self.full_output_file, self.opt_output_file, 'converged')
                break

    # raw data sum of square error
    def f_of_x(self, par):

        # return value
        obj = ObjectiveEvaluation()

        # check that each variable is within the range
        ctr = -1
        for dv in self.dvs:
            ctr += 1
            if par[ctr] > dv.value_maximum or par[ctr] < dv.value_minimum:
                obj.return_state = ReturnStateEnum.Return_state_infeasibleDV
                obj.message = 'infeasible DV, name=' + dv.var_name
                return

        # run the simulation engine on the file
        current_f = self.sim_func(par)

        # for now assume everything went OK?
        if not current_f:
            obj.return_state = ReturnStateEnum.Return_state_infeasibleObj
            obj.message = 'infeasible simulation result'
            return

        # so everything has run OK so far...calculate the ssqe and leave
        obj.return_state = ReturnStateEnum.Return_state_successful
        obj.value = self.ssqe(current_f)

        return obj
