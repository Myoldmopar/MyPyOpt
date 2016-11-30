class SearchReturnType(object):
    """
    This class defines a response structure for a given project search
    """
    def __init__(self, success, error_reason, values=None):
        """
        This is the constructor for this class

        :param success: A boolean value specifying whether the search was successful or not
        :param error_reason: A descriptive message of the search response
        :param values: An array of converged parameter values, if successful, or None -- this should be a hash later
        """
        self.success = success
        self.reason = error_reason
        self.values = values
