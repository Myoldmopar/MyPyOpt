import os
from Exceptions import MyPyOptException


class SimulationStructure(object):
    def __init__(self, expansion, contraction, max_iterations, project_name, output_dir):
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except os.error:
                raise MyPyOptException("Couldn't create root folder, aborting...")
        self.coefficient_expand = expansion
        self.coefficient_contract = contraction
        self.max_iterations = max_iterations
        self.project_name = project_name
        self.output_dir = output_dir
