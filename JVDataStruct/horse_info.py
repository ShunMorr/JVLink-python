"""
競走馬データ
JV_UM_UMA
"""

from .common import *


class SireInfo:
    def __init__(self, buf: bytes):
        self.breeding_num = midb2s(buf, 1, 8)
        self.name = midb2s(buf, 9, 36)


class IFHorseInfo:
    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.sire_id = midb2s(buf, 12, 10)
        self.active_code = midb2s(buf, 22, 1)
        self.register_date = YMD(midb2b(buf, 23, 8))
        self.delete_date = YMD(midb2b(buf, 31, 8))
        self.birthday = YMD(midb2b(buf, 39, 8))
        self.name = midb2s(buf, 47, 36)
        self.name_jp = midb2s(buf, 83, 36)
        self.name_en = midb2s(buf, 119, 60)
        self.in_stable_flag = midb2s(buf, 179, 1)
        self.reserved = midb2s(buf, 180, 19)
        self.horse_symbol_code = midb2s(buf, 199, 2)
        self.sex_code = midb2s(buf, 201, 1)
        self.breed_code = midb2s(buf, 202, 1)
        self.color_code = midb2s(buf, 203, 2)
        self.sire_info = [SireInfo(midb2b(buf, 205 + 44 * i, 44)) for i in range(14)]
        self.ew_code = midb2s(buf, 821, 1)
        self.trainer_code = midb2s(buf, 822, 5)
        self.trainer_name = midb2s(buf, 827, 8)
        self.invite_code = midb2s(buf, 835, 20)
        self.breeder_code = midb2s(buf, 855, 6)
        self.breeder_name = midb2s(buf, 861, 70)
        self.birthplace = midb2s(buf, 931, 20)
        self.owner_code = midb2s(buf, 951, 6)
        self.owner_name = midb2s(buf, 957, 64)
        self.earned_money_flat = midb2s(buf, 1021, 9)
        self.earned_money_hurdle = midb2s(buf, 1030, 9)
        self.earned_add_money_flat = midb2s(buf, 1039, 9)
        self.earned_add_money_hurdle = midb2s(buf, 1048, 9)
        self.earned_all_money_flat = midb2s(buf, 1057, 9)
        self.earned_all_money_hurdle = midb2s(buf, 1066, 9)
        self.ranked_times = ArrivalFrequency3(midb2b(buf, 1075, 18))
        self.ranked_times_central = ArrivalFrequency3(midb2b(buf, 1093, 18))
        self.ranked_times_race_type = [ArrivalFrequency3(midb2b(buf, 1111 + 18 * i, 18)) for i in range(7)]
        self.ranked_times_condition = [ArrivalFrequency3(midb2b(buf, 1237 + 18 * i, 18)) for i in range(12)]
        self.ranked_times_distance = [ArrivalFrequency3(midb2b(buf, 1453 + 18 * i, 18)) for i in range(6)]
        self.style = [midb2s(buf, 1561, 3 * i, 3) for i in range(4)]
        self.race_count = midb2s(buf, 1573.3)
        self.crlf = midb2s(buf, 1576, 2)
       