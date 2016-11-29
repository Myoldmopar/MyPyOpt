class SearchReturnType(object):
    def __init__(self, success, error_reason, values=None):
        self.success = success
        self.reason = error_reason
        self.values = values
