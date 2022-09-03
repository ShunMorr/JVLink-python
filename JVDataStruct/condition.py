from .common import *


class IFCondition:
    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.race_id = RaceID2(midb2b(buf, 12, 14))
        self.anno_time = MDHM(midb2b(buf, 26, 8))
        self.change_code = midb2s(buf, 34, 1)
        self.condition = ConditionInfo(midb2b(buf, 35, 3))
        self.condition_bf = ConditionInfo(midb2b(buf, 38, 3))
        self.crlf = midb2s(buf, 41, 2)
