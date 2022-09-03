"""
特別登録場情報
JV_TK_TOKUUMA
"""


from .common import *


class MajorRegisterHorseInfo:
    def __init__(self, buf: bytes):
        self.id = midb2s(buf, 1, 3)
        self.sire_id = midb2s(buf, 4, 10)
        self.name = midb2s(buf, 14, 36)
        self.symbol_code = midb2s(buf, 50, 2)
        self.sex_code = midb2s(buf, 52, 1)
        self.trainer_ew_code = midb2s(buf, 53, 1)
        self.trainer_code = midb2s(buf, 54, 5)
        self.trainer_name = midb2s(buf, 59, 8)
        self.weight = midb2s(buf, 67, 3)
        self.exchange = midb2s(buf, 70, 1)


class IFMajorRegisterInfo:

    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.id = RaceID(midb2b(buf, 12, 16))
        self.race_info = RaceInfo(midb2b(buf, 28, 587))
        self.grade_code = midb2s(buf, 615, 1)
        self.race_terms = RaceTerms(midb2b(buf, 616, 21))
        self.distance = midb2s(buf, 637, 4)
        self.track_code = midb2s(buf, 641, 2)
        self.course_division = midb2s(buf, 643, 2)
        self.handi_date = YMD(midb2b(buf, 645, 8))
        self.register_num = midb2s(buf, 653, 3)
        self.horse_info = [MajorRegisterHorseInfo(midb2b(buf, 656 + 70 * i, 70)) for i in range(300)]
        self.crlf = midb2s(buf, 21656, 2)
