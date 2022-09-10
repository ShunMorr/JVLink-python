from .common import *


class IFSire:
    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.breed_num = midb2s(buf, 12, 8)
        self.sireline_id = midb2s(buf, 20, 30)
        self.sireline_name = midb2s(buf, 50, 36)
        self.sireline_ex = midb2s(buf, 86, 6800)
        self.crlf = midb2s(buf, 6886, 2)
