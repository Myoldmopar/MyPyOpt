import json
import collections
import os
import time
from typing import Callable, Any, Dict, List, Optional
import uuid

from mypyopt.decision_variable import DecisionVariable
from mypyopt.exceptions import MyPyOptException
from mypyopt.objective_evaluation import ObjectiveEvaluation
from mypyopt.optimizer import Optimizer
from mypyopt.return_state_enum import ReturnStateEnum
from mypyopt.search_return_type import SearchReturnType
from mypyopt.input_output import InputOutputManager
from mypyopt.project_structure import ProjectStructure


class HeuristicSearch(Optimizer):
    """
    This class implements a heuristic, multi-variable, search optimization technique.
    The process is:

    1. Evaluate an objective value at the initial point :math:`j_0 = f\\left(x_0\\right)`

    2. Loop over each decision variable, perturb it in the current direction, and evaluate a new objective value with
       all other variables at their current position :math:`j_{i} = f\\left(\\tilde{x}\\right)`

    3. If the objective value reduced, which is the goal, move in the current direction and continue looping.  If the
       objective value increased, reverse directions and contract.

    4. Continue looping until all decision variables are converged between the current and prior iteration, or maximum
       iterations is reached.

    """
    def __init__(
            self, project_settings: ProjectStructure, decision_variable_array: List[DecisionVariable],
            callback_f_of_x: Callable[[Dict[str, float]], Any],
            callback_objective: Callable[[Any], List[float]],
            input_output_worker: Optional[InputOutputManager] = None,
            callback_progress: Optional[Callable[[int, float], None]] = None,
            callback_completed: Optional[Callable[[SearchReturnType], None]] = None
    ):

        super().__init__(project_settings, decision_variable_array, callback_f_of_x, callback_objective,
                         input_output_worker, callback_progress, callback_completed)

        # the root project name is created/validated by the sim constructor, set up the folder for this particular run
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S')
        dir_name = os.path.join(self.project.output_dir, timestamp + "_" + self.project.project_name +
                                "_" + str(uuid.uuid4())[0:8])

        try:
            os.mkdir(dir_name)
        except OSError:  # pragma: no cover -- not trying to catch this
            raise MyPyOptException("Couldn't create project folder, check permissions, aborting...")

        # output optimization information, so we don't have to look in the source
        project_info_file_name = os.path.join(dir_name, 'project_info.json')
        with open(project_info_file_name, 'w') as f:
            project_info = dict()
            project_info['project_name'] = self.project.project_name
            project_info['timestamp'] = timestamp
            project_info['decision_variables'] = [d.to_dictionary() for d in self.dvs]
            f.write(json.dumps(project_info, indent=2))

        # remove any previous files and open clean versions of the log files
        self.full_output_file = open(os.path.join(dir_name, 'full_output.log'), 'w')
        if os.path.exists(self.io.stopFile):  # pragma: no cover -- stop file usage is possibly slated for failure
            try:
                os.remove(self.io.stopFile)
            except OSError:  # pragma: no cover -- not trying to catch this
                raise MyPyOptException("Found stop file, but couldn't remove it, check permissions, aborting...")

        # check the dv array for duplicate names, as this would be invalid
        var_names = [dv.var_name for dv in self.dvs]
        duplicate_names = [i for i, c in collections.Counter(var_names).items() if c > 1]
        if duplicate_names:
            raise MyPyOptException("Found duplicated names within decision variables, give each a unique name.")

    def search(self) -> SearchReturnType:
        """
        This is the main driver function for the optimization.
        It walks the parameter space finding a minimum objective function.
        """

        self.io.write_line(True, self.full_output_file, '\n*******Optimization Beginning*******')

        # evaluate starting point
        base_values = {dv.var_name: dv.x_base for dv in self.dvs}
        obj_base = self.f_of_x(base_values)
        j_base = obj_base.value
        if obj_base.return_state == ReturnStateEnum.UserAborted:  # pragma: no cover -- stop file may be deprecated
            self.io.write_line(True, self.full_output_file,
                               'User aborted simulation via stop signal file...')
            r = SearchReturnType(False, ReturnStateEnum.UserAborted)
            if self.callback_completed:
                self.callback_completed(r)
            self.full_output_file.close()
            return r
        elif not obj_base.return_state == ReturnStateEnum.Successful:
            self.io.write_line(True, self.full_output_file,
                               'Initial point is infeasible or invalid, cannot begin iterations.  Aborting...')
            r = SearchReturnType(False, ReturnStateEnum.InvalidInitialPoint)
            if self.callback_completed:
                self.callback_completed(r)
            self.full_output_file.close()
            return r

        # begin iteration loop
        for iteration in range(1, self.project.max_iterations + 1):

            self.io.write_line(self.project.verbose, self.full_output_file, 'iter = ' + str(iteration))

            if os.path.exists(self.io.stopFile):  # pragma: no cover -- not covering stop file stuff
                self.io.write_line(True, self.full_output_file,
                                   'Found stop signal file in run directory; stopping now...')
                r = SearchReturnType(False, ReturnStateEnum.UserAborted)
                if self.callback_completed:
                    self.callback_completed(r)
                self.full_output_file.close()
                return r

            # begin DV loop
            for dv in self.dvs:

                # set up a new point
                dv.x_new = dv.x_base + dv.delta_x
                new_values = {dv.var_name: dv.x_new for dv in self.dvs}

                if dv.x_new > dv.value_maximum or dv.x_new < dv.value_minimum:  # pragma: no cover
                    # arranging the unit test to cover this condition is too much for now
                    # if we wanted to do it, we could have the objective function be a generator that yields a bad value
                    self.io.write_line(True, self.full_output_file,
                                       'infeasible DV, name=' + dv.var_name)
                    r = SearchReturnType(False, ReturnStateEnum.InfeasibleDV)
                    if self.callback_completed:
                        self.callback_completed(r)
                    self.full_output_file.close()
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

                if obj_new.return_state == ReturnStateEnum.UnsuccessfulOther:  # pragma: no cover
                    # not covering this either, this is kind of a dumping ground for unexpected errors to fail nicely
                    self.io.write_line(True, self.full_output_file,
                                       'Optimization ended unexpectedly, check all inputs and outputs')
                    self.io.write_line(True, self.full_output_file,
                                       'Error message: ' + str(obj_new.message))
                    r = SearchReturnType(False, ReturnStateEnum.UnsuccessfulOther)
                    if self.callback_completed:
                        self.callback_completed(r)
                    self.full_output_file.close()
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
                self.full_output_file.close()
                return r

            if self.callback_progress:
                self.callback_progress(iteration, j_base)

    def f_of_x(self, parameter_hash: Dict[str, float]):
        """
        This function calls the "f_of_x" callback function, getting outputs for the current parameter space;
        then passes those outputs into the objective function callback as an array, which usually returns the sum-sq-err
        between known values and current outputs.
        """

        # run the simulation function
        simulation_results = self.callback_f_of_x(parameter_hash)

        # the sim function should return None if it failed (for now)
        if simulation_results:
            error_to_minimize = self.callback_objective(simulation_results)
            return ObjectiveEvaluation(ReturnStateEnum.Successful, error_to_minimize)
        else:
            return ObjectiveEvaluation(ReturnStateEnum.InfeasibleObj, -999999,
                                       'Function f(x) failed, probably infeasible output')
