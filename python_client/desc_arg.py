class DescArg(object):
    def __init__(self, arg):
        """

        :param arg:
        """
        self.arg = arg
        self.bin_sz = -1 # set on serialization
        self.serialized = None

    def serialize(self):
        """

        :return:
        """
        pass