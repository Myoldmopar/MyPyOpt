class IOErrorReturnValues(object):
    Err_InvalidInitialPoint = 601
    Err_UnexpectedError = 602
    Err_FoundStopFile = 603
    Err_InvalidDVarray = 604
    Err_FileWritingProblem = 605
    Success = 0


class ReturnStateEnum(object):
    Return_state_infeasibleDV = -1
    Return_state_infeasibleObj = -2
    Return_state_unsuccessfulOther = -3
    Return_state_successful = -4
    Return_state_useraborted = -5
