import pyfiemap
import extent

class VirtualObject(object):
    def __init__(self, fpath, blk_sz, input=True):
        # TODO elise said something something error checking dont blow up the system or put
        # your toaster in the bathtub meh meh meh
        if input is True:
            self.flg = 1
        else:
            self.flg = 0

        self.nr_exts = 0
        self.blk_sz = blk_sz
        self.ext_list = []

        #TODO check valid path as well as path existence (probably looking for exceptions)
        if fpath is None:
            return
        else:
            self._convert_to_exts(fpath)

    def _convert_to_exts(self, fpath):
        """
        :param fpath: python string, full path to file we wish to create a virtual object out of.

        :return:
        """

        raw_ext_list = pyfiemap.get_ext_list(fpath)

        for ext in raw_ext_list:
            lba = int(ext[2]/self.blk_sz)
            nr_blks = int(ext[3]/self.blk_sz)
            new_ext = extent.Extent(lba, nr_blks) # Hooray! A successful autocomplete that totally needed a nuclear reactor and an LLM!
            self.ext_list.append(new_ext)
            self.nr_exts += 1


    def serialize(self):
        """
        Convert virtual object to a python byte array

        :return:
        """

        ser_blk_sz = self.blk_sz.to_bytes(8, byteorder='little')
        ser_nr_exts =  self.nr_exts.to_bytes(8, byteorder='little')
        ser_flg = self.flg.to_bytes(8, byteorder='little')
        ser_exts = bytearray()

        for ext_obj in self.ext_list:
            ser_ext = ext_obj.serialize()
            ser_exts += ser_ext

        aggregate_serialized_obj = ser_nr_exts + ser_blk_sz + ser_flg + ser_exts

        return aggregate_serialized_obj

def deserialize(serialized_bytes):
    """
    Converts a seralized virtual object into a python virtual object

    :param serialized_bytes:
    :return:
    """
    nr_exts = int.from_bytes(serialized_bytes[0:7], byteorder='little')
    blk_sz = int.from_bytes(serialized_bytes[8:15], byteorder='little')
    flg = int.from_bytes(serialized_bytes[16:23], byteorder='little')
    ser_exts = serialized_bytes[24:]
    ext_list = []


    #8 byte iterator
    for ext_nr in range(nr_exts):
        beg_ext_byte = ext_nr * 8
        end_ext_byte = ext_nr + 7

        ext_obj = extent.deserialize(serialized_bytes[beg_ext_byte:end_ext_byte])
        ext_list.append(ext_obj)

    if flg == 1:
        input = True
    else:
        input = False

    new_vobj = VirtualObject(None, blk_sz, input)
    new_vobj.ext_list = ext_list

    return new_vobj


if __name__ == '__main__':

    fpath = "../README.md"
    new_vobj = VirtualObject(fpath, 4096)
    ser_obj = new_vobj.serialize()
    test_obj = deserialize(ser_obj)