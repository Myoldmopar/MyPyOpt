from pathlib import Path
from typing import Optional
import os

from mypyopt.exceptions import MyPyOptException


class ProjectStructure:
    """
    This class defines high level project-wide settings
    """
    def __init__(
            self, expansion: float = 1.2, contraction: float = 0.85, max_iterations: int = 2000,
            project_name: str = 'project_name', output_dir_path: Optional[Path] = None, verbose: bool = False
    ):
        """
        Constructor for this class

        :param expansion: The expansion coefficient for walking through the parameter space in a favorable direction
        :param contraction: The contraction coefficient for walking through the parameter space in a poor direction
        :param max_iterations: The maximum number of iterations to sweep the entire parameter space
        :param project_name: A descriptive name for this project
        :param output_dir_path: The root output directory to use for writing output data as a pathlib.Path
        :param verbose: A boolean to decide whether to write a lot to the command line or not
        """
        if output_dir_path is None:
            output_dir = Path(__file__).resolve().parent.parent / 'projects'
        else:
            output_dir = str(output_dir_path)
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except os.error:  # pragma: no cover -- not trying to catch this
                raise MyPyOptException("Couldn't create root folder, aborting...")
        if expansion <= 1.0:
            raise MyPyOptException("Expansion coefficient is less than or equal to 1 (={0}), must be greater than 1.")
        if contraction >= 1.0:
            raise MyPyOptException("Contraction coefficient is greater than or equal to 1 (={0}), must be less than 1.")
        if max_iterations < 1:
            raise MyPyOptException("Max iterations is extremely small, likely an erroneous condition, aborting...")
        self.coefficient_expand = expansion
        self.coefficient_contract = contraction
        self.max_iterations = max_iterations
        self.project_name = project_name
        self.output_dir = output_dir
        self.verbose = verbose
