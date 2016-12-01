import os

from Exceptions import MyPyOptException


class ProjectStructure(object):
    """
    This class defines high level project-wide settings
    """
    def __init__(self, expansion=1.2, contraction=0.85, max_iterations=2000, project_name='project_name',
                 output_dir='projects', verbose=False):
        """
        Constructor for this class

        :param expansion: The expansion coefficient for walking through the parameter space in a favorable direction
        :param contraction: The contraction coefficient for walking through the parameter space in a poor direction
        :param max_iterations: The maximum number of iterations to sweep the entire parameter space
        :param project_name: A descriptive name for this project
        :param output_dir: The root output directory to use for writing output data
        :param verbose: A boolean to decide whether to write a lot to the command line or not
        """
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
        self.verbose = verbose
