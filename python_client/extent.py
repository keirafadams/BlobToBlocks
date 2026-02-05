class Extent(object):
    def __init__(self,lba,ext_len):
        """
        :param lba: integer, logical block address
        :param len: length in number of blocks
        """
        self.lba = lba
        self.ext_len = ext_len

    def serialize(self):
        """
        Returns a binary serialized version of the extent data.

        :return: serialized byte object
        """
        serialized_lba = self.lba.to_bytes(8, byteorder='little', signed=False)
        serialized_ext_len = self.ext_len.to_bytes(8, byteorder='little', signed=False)
        ser_bytes =(serialized_lba + serialized_ext_len)

        return ser_bytes

def deserialize(ser_bytes):
    """
    Returns a new extent object from the provided serialized bytes.

    :param ser_bytes: serialized extent bytes, should be 16 bytes long
    :return: extent object
    """
    lba = int.from_bytes(ser_bytes[0:8], byteorder='little', signed=False)
    ext_len = int.from_bytes(ser_bytes[8:16], byteorder='little', signed=False)

    new_ext = Extent(lba,ext_len)

    return new_ext
