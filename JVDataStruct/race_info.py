"""
レース詳細
JV_RA_Race
"""
from .common import *


class CornerInfo:
    def __init__(self, buf: bytes):
        self.corner = midb2s(buf, 1, 1)
        self.turns = midb2s(buf, 2, 1)
        self.order = midb2s(buf, 3, 70)


class IFRaceInfo:
    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.id = RaceID(midb2b(buf, 12, 16))
        self.race_info = RaceInfo(midb2b(buf, 28, 587))
        self.grade_code = midb2s(buf, 615, 1)
        self.grade_code_bf = midb2s(buf, 616, 1)
        self.race_terms = RaceTerms(midb2b(buf, 617, 21))
        self.term_name = midb2s(buf, 638, 60)
        self.distance = midb2s(buf, 698, 4)
        self.distance_bf = midb2s(buf, 702, 4)
        self.track_code = midb2s(buf, 706, 2)
        self.track_code_bf = midb2s(buf, 708, 2)
        self.course_division = midb2s(buf, 710, 2)
        self.course_division_bf = midb2s(buf, 712, 2)
        self.prize = [midb2s(buf, 714 + 8 * i, 8) for i in range(7)]
        self.prize_bf = [midb2s(buf, 770 + 8 * i, 8) for i in range(5)]
        self.add_prize = [midb2s(buf, 810 + 8 * i, 8) for i in range(5)]
        self.add_prize_bf = [midb2s(buf, 850 + 8 * i, 8) for i in range(3)]
        self.starting_time = midb2s(buf, 874, 4)
        self.starting_time_bf = midb2s(buf, 878, 4)
        self.register_num = midb2s(buf, 882, 2)
        self.enter_num = midb2s(buf, 884, 2)
        self.goal_num = midb2s(buf, 886, 2)
        self.condition = ConditionInfo(midb2b(buf, 888, 3))
        self.lap_time = [midb2s(buf, 891 + 3 * i, 3) for i in range(25)]
        self.mile_time_hurdle = midb2s(buf, 966, 4)
        self.furlong_time_s3 = midb2s(buf, 970, 3)
        self.furlong_time_s4 = midb2s(buf, 973, 3)
        self.furlong_time_l3 = midb2s(buf, 976, 3)
        self.furlong_time_l4 = midb2s(buf, 979, 3)
        self.corner_info = [CornerInfo(midb2b(buf, 982 + 72 * i, 72)) for i in range(4)]
        self.new_record_code = midb2s(buf, 1270, 1)
        self.crlf = midb2s(buf, 1271, 2)
