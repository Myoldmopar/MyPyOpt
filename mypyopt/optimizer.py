import os
import time

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
        self.converged = False
        self.converged_values = None

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
            f.write("Variable Name, Min Value, Max Value, Initial Value, Initial Step Size, Convergence Criterion\n")
            for dv in dvs:
                f.write(','.join(str(x) for x in [dv.var_name, dv.value_minimum, dv.value_maximum, dv.value_initial,
                                  dv.step_size_initial, dv.convergence_criteria]) + '\n')

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

        self.io.write_line(True, self.full_output_file, self.opt_output_file, '*******Optimization Beginning*******')

        # evaluate starting point
        base_vals = {dv.var_name: dv.x_base for dv in self.dvs}
        obj_base = self.f_of_x(base_vals)
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
            for dv in self.dvs:

                # setup a new point
                dv.x_new = dv.x_base + dv.delta_x
                new_vals = {dv.var_name: dv.x_new for dv in self.dvs}

                if dv.x_new > dv.value_maximum or dv.x_new < dv.value_minimum:
                    self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                       'infeasible DV, name=' + dv.var_name)
                    return ReturnStateEnum.Return_state_infeasibleDV

                # then evaluate the new point
                obj_new = self.f_of_x(new_vals)
                j_new = obj_new.value

                self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                   'iter=' + str(iteration))
                self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                   'var=' + str(dv))
                self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                   'x_base=' + str([x.x_base for x in self.dvs]))
                self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                   'j_base=' + str(j_base))
                self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                   'x_new=' + str([x.x_new for x in self.dvs]))
                self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                   'j_new=' + str(j_new))

                if obj_new.return_state == ReturnStateEnum.Return_state_unsuccessfulOther:
                    self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                       'Optimization ended unexpectedly, check all inputs and outputs')
                    self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                       'Error message: ' + str(obj_new.message))
                    return IOErrorReturnValues.Err_UnexpectedError
                elif (not obj_new.return_state == ReturnStateEnum.Return_state_successful) or (j_new > j_base):
                    dv.delta_x = -self.sim.coeff_contract * dv.delta_x
                    dv.x_new = dv.x_base
                    self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                       '## Unsuccessful objective evaluation, or worse result, going back ##')
                else:
                    j_base = j_new
                    dv.x_base = dv.x_new
                    dv.delta_x = self.sim.coeff_expand * dv.delta_x
                    self.io.write_line(True, self.full_output_file, self.opt_output_file,
                                       '## Improved result, accepting and continuing forward ##')

                # check if we went out of range

            converged = True
            for dv in self.dvs:
                if abs(dv.delta_x) > dv.convergence_criteria:
                    converged = False
                    break

            if converged:
                self.io.write_line(True, self.full_output_file, self.opt_output_file, 'converged')
                self.converged = True
                self.converged_values = [x.x_new for x in self.dvs]
                break

    # raw data sum of square error
    def f_of_x(self, parameter_hash):

        # return value
        obj = ObjectiveEvaluation()

        # run the simulation function
        current_f = self.sim_func(parameter_hash)

        # for now assume everything went OK?
        if not current_f:
            obj.return_state = ReturnStateEnum.Return_state_infeasibleObj
            obj.message = 'infeasible simulation result'
            return

        # so everything has run OK so far...calculate the ssqe and leave
        obj.return_state = ReturnStateEnum.Return_state_successful
        obj.value = self.ssqe(current_f)

        return obj
