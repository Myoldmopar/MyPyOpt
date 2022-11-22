class SearchReturnType(object):
    """
    This class defines a response structure for a given project search
    """
    def __init__(self, success, error_reason, values=None):
        """
        This is the constructor for this class

        :param success: A boolean value specifying whether the search was successful or not
        :param error_reason: A descriptive message of the search response
        :param values: A hash of converged values where the keys are the original variable_names from the DVs
        """
        self.success = success
        self.reason = error_reason
        self.values = values
