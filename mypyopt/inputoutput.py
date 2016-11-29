class IOErrorReturnValues(object):
    Err_InvalidInitialPoint = 601
    Err_UnexpectedError = 602
    Err_FoundStopFile = 603
    Err_InvalidDVarray = 604
    Err_FileWritingProblem = 605
    Success = 0


class InputOutputManager(object):
    def __init__(self):
        self.stopFile = 'stop.stop'

    @staticmethod
    def write_line(console, full_output, string):
        if console:
            print(string)
        if not string.endswith('\n'):
            string += '\n'
        if full_output:
            full_output.write(string)
        return
