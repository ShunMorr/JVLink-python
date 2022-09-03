from .common import *


class HorseWeightInfo:
    def __init__(self, buf: bytes):
        self.horse_number = midb2s(buf, 1, 2)
        self.name = midb2s(buf, 3, 36)
        self.weight = midb2s(buf, 39, 3)
        self.fluctuation_sign = midb2s(buf, 42, 1)
        self.fluctuation = midb2s(buf, 43, 3)


class IFHorseWeight:
    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.race_id = RaceID(midb2b(buf, 12, 16))
        self.anno_time = MDHM(midb2b(buf, 28, 8))
        self.horse_weight_info = [HorseWeightInfo(midb2b(buf, 36 + 45 * i, 45)) for i in range(18)]
        self.crlf = midb2s(buf, 846, 2)
