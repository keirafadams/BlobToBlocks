from python_client.vobj import VirtualObject
from python_client.vobj import deserialize as deserialize_vobj
from python_client.desc_arg import DescArg

class Descriptor:
    #TODO Blocksize specifier
    def __init__(self, operation, arg_list, infile_list=None, outfile_list=None, bypass=False):
        """
        Create a descriptor object for later serialization for transport

        :param operation: Operation, python string, effectively the name of the desired
        function to call
        :param arg_list: python list of arguments to encode into the descriptor
        :param infile_list: list of strings (filepaths) that detail the locations
        of the files to create virual objects out of
        :param outfile_list: list of strings (filepaths) that detail the locations of possible
        output file locations.
        :param bypass: boolean, whether or not to bypass input/output locations checks
        used in deserialization for targets as they do not operate on target paths

        :raises: exception if no input or output locations are specified
        """

        if infile_list is None and outfile_list is None and bypass is False:
            raise Exception("Must specify at least one input or output location")


        #TODO CHECK AND UPDATE FOR 8 CHARACTER STRING FOR OPERATION
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

        if infile_list is not None:
            self.nr_input_objs = len(infile_list)
        else:
            self.nr_input_objs = 0

        if outfile_list is not None:
            self.nr_output_objs = len(outfile_list)
        else:
            self.nr_output_objs = 0

        self.input_obj_instances = []
        self.output_obj_instances = []

        if infile_list is not None:
            for input_fpath in infile_list:
                self._add_vobj(input_fpath,input=True)

        if outfile_list is not None:
            for output_fpath in outfile_list:
                self._add_vobj(output_fpath,input=False)

        if len(arg_list) > 0:
            for arg in arg_list:
                self._add_arg(arg)

    def __str__(self):

        print("---Descriptor Contents---")
        print("*Operation: %s" % self.operation)
        print("*Args:")
        for arg in self.arg_list:
            print(arg)

        print("*Input Virtual Objects: ")
        for vobj in self.input_obj_instances:
            print(vobj)

        print("*Output Virtual Objects:")
        for vobj in self.output_obj_instances:
            print(vobj)

        return ""

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

        test_desc_length = 0
        desc_length = 0

        ser_in_vobj_list = []
        ser_out_vobj_list = []
        ser_arg_list = []

        arg_bin_length = 0
        in_vobj_bin_length = 0
        out_vobj_bin_length = 0

        # Get serialized args and length estimate
        for arg in self.arg_list_instances:
            ser_arg = arg.serialize()
            ser_arg_list.append(ser_arg)
            arg_bin_length += len(ser_arg)
            test_desc_length += len(ser_arg)

        # Get serialized in virtual objects and  estimated length
        for in_vobj in self.input_obj_instances:
            ser_vobj = in_vobj.serialize()
            ser_in_vobj_list.append(ser_vobj)
            in_vobj_bin_length += len(ser_vobj)
            test_desc_length += len(ser_vobj)

        # Get serialized out virtual objects and estimated length
        for out_vobj in self.output_obj_instances:
            ser_vobj = out_vobj.serialize()
            ser_out_vobj_list.append(ser_vobj)
            out_vobj_bin_length += len(ser_vobj)
            test_desc_length += len(ser_vobj)


        # now we convert lengths to binary
        ser_nr_args = len(ser_arg_list).to_bytes(8, byteorder='little', signed=False)
        ser_in_nr_vobjs =  len(ser_in_vobj_list).to_bytes(8, byteorder='little', signed=False)
        ser_out_nr_vobjs = len(ser_out_vobj_list).to_bytes(8, byteorder='little', signed=False)
        test_desc_length += (8*3)

        #ser_desc_length = desc_length.to_bytes(8, byteorder='little', signed=False)

        # Serialize operation
        serialized_operation = bytes(self.operation, 'utf-8')
        op_len = len(serialized_operation)
        ser_op_len = op_len.to_bytes(8, byteorder='little', signed=False)
        total_op_ser = (ser_op_len + serialized_operation)
        test_desc_length += len(total_op_ser)

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
        for ser_vobj in ser_out_vobj_list:
            total_ser_out_vobjs += ser_vobj

        # Adding a magic number to make something match has NEVER gone poorly
        test_desc_length += 8
        ser_test_desc_length = test_desc_length.to_bytes(8, byteorder='little', signed=False)

        final_ser_desc = (ser_test_desc_length + total_op_ser + ser_nr_args + total_ser_args
                          + ser_in_nr_vobjs + total_ser_in_vobjs
                          + ser_out_nr_vobjs + total_ser_out_vobjs)

        return final_ser_desc

def deserialize(ser_desc):
    """
    Takes serialized descriptor and unpacks it into the various
    objects

    :param ser_desc:
    :return:
    """

    start_offset = 0

    # grab total descriptor length
    desc_byte_slice = ser_desc[start_offset:start_offset+8]
    #TODO check against entire serialized length
    desc_len = int.from_bytes(desc_byte_slice, byteorder='little', signed=False)
    start_offset += 8

    #Grab operation
    op_len_serialized = ser_desc[start_offset:start_offset+8]
    op_len = int.from_bytes(op_len_serialized, byteorder='little', signed=False)
    start_offset += 8
    operation = ser_desc[start_offset:start_offset+op_len].decode('utf-8')
    start_offset += op_len

    # grab number of arguments
    nr_arg_byte_slice = ser_desc[start_offset:start_offset+8]
    total_args = int.from_bytes(nr_arg_byte_slice, byteorder='little', signed=False)
    start_offset += 8

    # grab args
    cur_arg_ctr = 0
    arg_str_lists = []
    while cur_arg_ctr < total_args:
        #grab arg length
        arg_length = int.from_bytes(ser_desc[start_offset:start_offset+8], byteorder='little', signed=False)
        start_offset += 8

        #extract string
        argstring = ser_desc[start_offset:start_offset+arg_length].decode('utf-8')
        arg_str_lists.append(argstring)

        # adjust count and descriptor offset
        cur_arg_ctr += 1
        start_offset += arg_length


    # grab input objects
    cur_vobj_ctr = 0
    nr_vobjs_ser = ser_desc[start_offset:start_offset+8]
    nr_vobjs = int.from_bytes(nr_vobjs_ser, byteorder='little', signed=False)
    start_offset += 8
    in_vobj_list = []
    while cur_vobj_ctr < nr_vobjs:
        new_vobj = deserialize_vobj(ser_desc[start_offset:])
        nr_exts = len(new_vobj.ext_list)
        in_vobj_list.append(new_vobj)
        # 3 fixed metadata int64s per vobj
        start_offset += 24
        # and 2 per extent
        start_offset += (nr_exts * 16)
        cur_vobj_ctr +=1

    # grab output objects
    cur_vobj_ctr = 0
    nr_vobjs_ser = ser_desc[start_offset:start_offset + 8]
    nr_vobjs = int.from_bytes(nr_vobjs_ser, byteorder='little', signed=False)
    start_offset += 8
    out_vobj_list = []
    while cur_vobj_ctr < nr_vobjs:
        new_vobj = deserialize_vobj(ser_desc[start_offset:])
        nr_exts = len(new_vobj.ext_list)
        out_vobj_list.append(new_vobj)
        # 3 fixed metadata int64s per vobj
        start_offset += 24
        # and 2 per extent
        start_offset += (nr_exts * 16)
        cur_vobj_ctr += 1

    # dump everything in a new descriptor
    new_desc = Descriptor(operation, arg_str_lists, bypass=True)
    new_desc.input_obj_instances = in_vobj_list
    new_desc.output_obj_instances = out_vobj_list

    return new_desc


