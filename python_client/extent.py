class Extent(object):
    def __init__(self,lba,len):
        """

        :param lba:
        :param len:
        """
        self.lba=lba
        self.len=len

    def serialize(self):
        """

        :return:
        """
        pass