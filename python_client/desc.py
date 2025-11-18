class Descriptor:
    def __init__(self, operation, arg_list, infile_list=[], outfile_list=[]):
        """


        :param operation:
        :param arg_list:
        :param infile_list:
        :param outfile_list:
        """

        #TODO move to internal calls for creating objects
        self.arg_list = arg_list
        self.operation = operation
        self.input_objs = infile_list
        self.output_objs = outfile_list
        self.desc_bin_sz = -1 # calculated at serialization
        self.nr_args = len(arg_list)
        self.serialized_obj = None
        self.nr_input_objs = len(infile_list)
        self.nr_output_objs = len(outfile_list)

        pass

    def _add_vobj(self, fpath, input=True):
        """

        :param path:
        :param input:
        :return:
        """
        pass

    def _add_arg(self, arg):
        """

        :param arg:
        :return:
        """
        pass


