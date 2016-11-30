class ReturnStateEnum(object):
    """
    This class simply defines some constants for how functions return
    """

    Successful = 0
    """Search returned successfully"""

    InfeasibleDV = -1
    """Search failed because the decision variable went out of the valid parameter space range"""

    InfeasibleObj = -2
    """Search failed because the objective function could not be calculated, probably a failed simulation call"""

    UnsuccessfulOther = -3
    """Search failed for an unknown reason"""

    InvalidInitialPoint = -4
    """Search failed because the initial point was invalid"""

    UserAborted = -9
    """Search was stopped because the user forced it to stop"""

    @staticmethod
    def enum_to_string(enum):
        """
        This static function converts an enum integer into a string representation

        :param enum: An enum as defined in this class
        :return: A string description of the enum
        """
        if enum == ReturnStateEnum.Successful:
            return "Successful"
        elif enum == ReturnStateEnum.InfeasibleDV:
            return "InfeasibleDV"
        elif enum == ReturnStateEnum.InfeasibleObj:
            return "InfeasibleObj"
        elif enum == ReturnStateEnum.UnsuccessfulOther:
            return "UnsuccessfulOther"
        elif enum == ReturnStateEnum.InvalidInitialPoint:
            return "InvalidInitialPoint"
        elif enum == ReturnStateEnum.UserAborted:
            return "UserAborted"
