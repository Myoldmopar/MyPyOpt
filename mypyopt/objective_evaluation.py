from typing import Any


class ObjectiveEvaluation:
    """
    This class defines the return type from an evaluation of the objective function.

    The objective function is generally intended to be minimized by the optimizer search() function,
    so it is often a sum of squares error between some known quantity and the current outputs
    """
    def __init__(self, state: int, value: Any, message: str = ''):
        """
        The constructor for the class

        :param state: One of the ReturnStateEnum enumerated constants
        :param value: A single value representing the current objective function evaluation, often sum-squared-error
        :param message: An optional message to add additional info for the user
        """
        self.return_state = state
        self.message = message
        self.value = value
