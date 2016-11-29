class ObjectiveEvaluation(object):
    def __init__(self, state, value, message=''):
        self.return_state = state
        self.message = message
        self.value = value
