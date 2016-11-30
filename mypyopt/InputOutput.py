class InputOutputManager(object):
    """
    This class defines some input/output-related conveniences
    """
    def __init__(self):
        """
        The constructor for this class.  Currently it only defines the name of the stop file trigger (stop.stop)
        """
        self.stopFile = 'stop.stop'

    @staticmethod
    def write_line(console, full_output, string):
        """
        A static method in the class used for convenience when printing out information.

        :param console: A boolean for whether to report the string to standard output
        :param full_output: A file stream, which if not None, will be written to with the string
        :param string: The string to report; a newline is appended to the end if it doesn't have one already
        """
        if console:
            print(string)
        if not string.endswith('\n'):
            string += '\n'
        if full_output:
            full_output.write(string)
