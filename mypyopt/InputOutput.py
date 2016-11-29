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
