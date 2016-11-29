class ReturnStateEnum(object):
    Successful = 0
    InfeasibleDV = -1
    InfeasibleObj = -2
    UnsuccessfulOther = -3
    InvalidInitialPoint = -4
    UserAborted = -9

    @staticmethod
    def enum_to_string(enum):
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
