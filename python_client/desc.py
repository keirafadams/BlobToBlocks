from vobj import VirtualObject
from desc_arg import DescArg

class Descriptor:
    #TODO Blocksize specifier
    def __init__(self, operation, arg_list, infile_list=None, outfile_list=None):
        """
        Create a descriptor object for later serialization for transport

        :param operation: Operation, python string, effectively the name of the desired
        function to call
        :param arg_list: python list of arguments to encode into the descriptor
        :param infile_list: list of strings (filepaths) that detail the locations
        of the files to create virual objects out of
        :param outfile_list: list of strings (filepaths) that detail the locations of possible
        output file locations.

        :raises: exception if no input or output locations are specified
        """

        if infile_list is None and outfile_list is None:
            raise Exception("Must specify at least one input or output location")

        #TODO move to internal calls for creating objects
        # UPDATE: wish I new WTF I meant here by internal calls....
        self.arg_list = arg_list
        self.arg_list_instances = []
        self.operation = operation
        self.input_objs = infile_list
        self.output_objs = outfile_list
        self.desc_bin_sz = -1 # calculated at serialization
        self.nr_args = len(arg_list)
        self.serialized_obj = None
        self.nr_input_objs = len(infile_list)
        self.nr_output_objs = len(outfile_list)
        self.input_obj_instances = []
        self.output_obj_instances = []

        if infile_list is not None:
            for input_fpath in infile_list:
                self._add_vobj(input_fpath,True)

        if outfile_list is not None:
            for output_fpath in outfile_list:
                self._add_vobj(output_fpath,False)

        if len(arg_list) > 0:
            for arg in arg_list:
                self._add_arg(arg)


    def _add_vobj(self, fpath, blk_sz=4096, input=True):
        """
        Creates a virtual object instance from a specified filepath

        :param path: python string, path to file to turn into the relevant python object
        :param blk_sz:  integer, size in bytes of the storage block being specified
        :param input: boolean, whether or not the specified file is intended to be an input or
        output object
        :return: None
        """

        new_vobj = VirtualObject(fpath, blk_sz, input=input)

        if input is True:
            self.input_obj_instances.append(new_vobj)
        else:
            self.output_obj_instances.append(new_vobj)


    def _add_arg(self, arg):
        """
        Creates an argument object instance from the specified arg being handed in
        :param arg: pythons string or bytes object
        :return:
        """
        new_arg = DescArg(arg)
        self.arg_list_instances.append(new_arg)

    def serialize(self):
        """
        serialize entire descriptor including all virtual objects

        :return: serialized byte object
        """
        nr_args = len(self.arg_list)
        nr_input_objs = len(self.input_obj_instances)
        nr_output_objs = len(self.output_obj_instances)

        desc_length = 0

        ser_in_vobj_list = []
        ser_out_vobj_list = []
        ser_arg_list = []

        arg_bin_length = 0
        in_vobj_bin_length = 0
        out_vobj_bin_length = 0

        # Get serialized args and length estimate
        for arg in self.arg_list:
            ser_arg = arg.serialize()
            ser_arg_list.append(ser_arg)
            arg_bin_length += len(ser_arg)

        # Get serialized in virtual objects and  estimated length
        for in_vobj in self.input_obj_instances:
            ser_vobj = in_vobj.serialize()
            ser_in_vobj_list.append(ser_vobj)
            in_vobj_bin_length += len(ser_vobj)

        # Get serialized out virtual objects and estimated length
        for out_vobj in self.output_obj_instances:
            ser_vobj = out_vobj.serialize()
            ser_out_vobj_list.append(ser_vobj)
            out_vobj_bin_length += len(ser_vobj)

        # calculate descriptor length in bytes, dynamic portion
        desc_length = arg_bin_length + in_vobj_bin_length + out_vobj_bin_length

        # Now we add in the fixed portion (an additional 4 64 bit integers)
        desc_length += (8*4)

        # now we convert lengths to binary
        ser_nr_args = len(ser_arg_list).to_bytes(8, byteorder='little', signed=False)
        ser_in_nr_vobjs =  len(ser_in_vobj_list).to_bytes(8, byteorder='little', signed=False)
        ser_out_nr_vobjs = len(ser_out_vobj_list).to_bytes(8, byteorder='little', signed=False)
        ser_desc_length = desc_length.to_bytes(8, byteorder='little', signed=False)

        #and concatenate the whole mess together

        # first concantenate serialized args
        total_ser_args = bytes()
        total_ser_in_vobjs = bytes()
        total_ser_out_vobjs = bytes()

        for ser_arg in ser_arg_list:
            total_ser_args += ser_arg

        # then input vobjs
        for ser_vobj  in ser_in_vobj_list:
            total_ser_in_vobjs += ser_vobj

        # then output objs
        for ser_vobj in ser_in_vobj_list:
            total_ser_out_vobjs += ser_vobj

        final_ser_desc = (ser_desc_length + ser_nr_args + total_ser_args
                          + ser_in_nr_vobjs + total_ser_in_vobjs
                          + ser_out_nr_vobjs + total_ser_out_vobjs)

        return final_ser_desc






def deserialize(ser_desc):
    pass




