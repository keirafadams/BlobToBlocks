import pyfiemap
import extent

class VirtualObject(object):
    def __init__(self, fpath, blk_sz, input=True):
        # TODO elise said something something error checking dont blow up the system or put
        # your toaster in the bathtub meh meh meh
        self.input = input
        self.nr_exts = 0
        self.ext_list = []
        self.blk_sz = blk_sz

        self._convert_to_exts(fpath)

    def _convert_to_exts(self, fpath):
        """
        :param fpath: python string, full path to file we wish to create a virtual object out of.

        :return:
        """

        raw_ext_list = pyfiemap.get_ext_list(fpath)

        for ext in raw_ext_list:
            lba = ext[2]/self.blk_sz
            nr_blks = ext[3]/self.blk_sz
            new_ext = extent.Extent(lba, nr_blks) # Hooray! A successful autocomplete that totally needed a nuclear reactor and an LLM!
            self.ext_list.append(new_ext)
            self.nr_exts += 1


    def serialize(self):
        """
        Convert virtual object to a python byte array

        :return:
        """
        pass


def deserialize(serialized_bytes):
    """
    Converts a seralized virtual object into a python virtual object

    :param serialized_bytes:
    :return:
    """
    pass
