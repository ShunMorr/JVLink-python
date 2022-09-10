"""
馬毎レース情報
JV_SE_RACE_UMA
"""

from .common import *


class WinnerData:
    def __init__(self, buf: bytes):
        self.sire_id = midb2s(buf, 1, 10)
        self.horse_name = midb2s(buf, 11, 36)


class IFHorseRaceInfo:
    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.id = RaceID(midb2b(buf, 12, 16))
        self.gate_number = midb2s(buf, 28, 1)
        self.horse_number = midb2s(buf, 29, 2)
        self.sire_id = midb2s(buf, 31, 10)
        self.horse_name = midb2s(buf, 41, 36)
        self.horse_symbol_code = midb2s(buf, 77, 2)
        self.sex_code = midb2s(buf, 79, 1)
        self.breed_code = midb2s(buf, 80, 1)
        self.color_code = midb2s(buf, 81, 2)
        self.old = midb2s(buf, 83, 2)
        self.ew_code = midb2s(buf, 85, 1)
        self.trainer_code = midb2s(buf, 86, 5)
        self.trainer_name = midb2s(buf, 91, 8)
        self.owner_code = midb2s(buf, 99, 6)
        self.owner_name = midb2s(buf, 105, 64)
        self.cloth_color = midb2s(buf, 169, 60)
        self.reserved1 = midb2s(buf, 229, 60)
        self.weight = midb2s(buf, 289, 3)
        self.weight_bf = midb2s(buf, 292, 3)
        self.blinker = midb2s(buf, 295, 1)
        self.reserved2 = midb2s(buf, 296, 1)
        self.jockey_code = midb2s(buf, 297, 5)
        self.jockey_code_bf = midb2s(buf, 302, 5)
        self.jockey_name = midb2s(buf, 307, 8)
        self.jockey_name_bf = midb2s(buf, 315, 8)
        self.ap_jockey_code = midb2s(buf, 323, 1)
        self.ap_jockey_code_bf = midb2s(buf, 324, 1)
        self.horse_weight = midb2s(buf, 325, 3)
        self.fluctuation_sign = midb2s(buf, 328, 1)
        self.fluctuation = midb2s(buf, 329, 3)
        self.anomaly_code = midb2s(buf, 332, 1)
        self.pending_order = midb2s(buf, 333, 2)
        self.order = midb2s(buf, 335, 2)
        self.with_order = midb2s(buf, 337, 1)
        self.with_horse_num = midb2s(buf, 338, 1)
        self.time = midb2s(buf, 339, 4)
        self.time_differ_code = midb2s(buf, 343, 3)
        self.time_differ_code_p = midb2s(buf, 346, 3)
        self.time_differ_code_pp = midb2s(buf, 349, 3)
        self.corner_seating1 = midb2s(buf, 352, 2)
        self.corner_seating2 = midb2s(buf, 354, 2)
        self.corner_seating3 = midb2s(buf, 356, 2)
        self.corner_seating4 = midb2s(buf, 358, 2)
        self.odds = midb2s(buf, 360, 4)
        self.popularity = midb2s(buf, 364, 2)
        self.prize = midb2s(buf, 366, 8)
        self.add_prize = midb2s(buf, 374, 7)
        self.reserved3 = midb2s(buf, 382, 3)
        self.reserved4 = midb2s(buf, 385, 3)
        self.furlong_time4 = midb2s(buf, 388, 3)
        self.furlong_time3 = midb2s(buf, 391, 3)
        self.winner_info = [WinnerData(midb2b(buf, 394 + 46 * i, 46)) for i in range(3)]
        self.time_differ = midb2s(buf, 532, 4)
        self.new_recode_code = midb2s(buf, 536, 1)
        self.dm_code = midb2s(buf, 537, 1)
        self.dm_time = midb2s(buf, 538, 5)
        self.dm_error_p = midb2s(buf, 543, 4)
        self.dm_error_m = midb2s(buf, 547, 4)
        self.dm_order = midb2s(buf, 551, 2)
        self.style = midb2s(buf, 553, 1)
        self.crlf = midb2s(buf, 554, 2)