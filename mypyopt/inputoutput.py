class IOErrorReturnValues(object):
    Err_InvalidInitialPoint = 601
    Err_UnexpectedError = 602
    Err_FoundStopFile = 603
    Err_InvalidDVarray = 604
    Success = 0


class InputOutputManager(object):
    def __init__(self):
        self.numDVs = 0
        self.FullOutputFileName = ''
        self.optimizationOutputFileName = ''
        self.stopFile = 'stop.stop'
        self.uFullOutput = 80
        self.uOptOutput = 81

    @staticmethod
    def write_line(console, full_output, opt_output, string):
        if console:
            print(string)
        if not string.endswith('\n'):
            string += '\n'
        if full_output:
            full_output.write(string)
        if opt_output:
            opt_output.write(string)
        return
