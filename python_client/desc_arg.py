class DescArg(object):
    def __init__(self, arg):
        """
        Convenience object for getting arguments out

        :param arg: python string or bytes object.
        """
        self.arg = arg
        self.arg_sz = len(arg)
        self.bin_sz = -1 # set on serialization
        self.serialized = None

    def serialize(self):
        """
        Returns a serialized bytes object for use in higher
        level serialized routines

        :return: bytes object
        """

        serialized_arg = bytes(self.arg, 'utf-8')
        self.bin_sz = len(serialized_arg)
        ser_len = self.bin_sz.to_bytes(8, byteorder='little', signed=False)

        total_ser = (ser_len + serialized_arg)

        return total_ser

def deserialize(self, ser_arg):
    """
    Takes the serialized bytes object and returns a DescArg object

    :return: instantiated DescArg object
    """
    arg_str = ser_arg.decode("utf-8")
    new_desc_arg = DescArg(arg_str)

    return new_desc_arg
