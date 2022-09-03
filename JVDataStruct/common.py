"""
共通構造体・メソッド
"""

ENCODE = "shift-jis"


def midb2s(buf: bytes, st: int, length: int):
    """
    文字列(string)を任意に切り出す

    :param buf: 文字列
    :param st: スタート位置
    :param length: 長さ
    :return:
    """
    return buf[st - 1:(st + length - 1)].decode(ENCODE)


def midb2b(buf: bytes, st: int, length: int):
    """
    文字列(bytes)を任意に切り出す

    :param buf:
    :param st:
    :param length:
    :return:
    """
    return buf[st - 1:(st + length - 1)]


class YMD:
    def __init__(self, buf: bytes):
        self.year = midb2s(buf, 1, 4)
        self.month = midb2s(buf, 5, 2)
        self.day = midb2s(buf, 7, 2)


class HMS:
    def __init__(self, buf: bytes):
        self.hour = midb2s(buf, 1, 2)
        self.minute = midb2s(buf, 3, 2)
        self.second = midb2s(buf, 5, 2)


class HM:
    def __init__(self, buf: bytes):
        self.hour = midb2s(buf, 1, 2)
        self.minute = midb2s(buf, 3, 2)


class MDHM:
    def __init__(self, buf: bytes):
        self.month = midb2s(buf, 1, 2)
        self.day = midb2s(buf, 3, 2)
        self.hour = midb2s(buf, 5, 2)
        self.minute = midb2s(buf, 7, 2)


class RecordID:
    def __init__(self, buf: bytes):
        self.record_spec = midb2s(buf, 1, 2)
        self.data_partition = midb2s(buf, 3, 1)
        self.create_date = YMD(midb2b(buf, 4, 8))


class RaceID:
    def __init__(self, buf: bytes):
        self.year = midb2s(buf, 1, 4)
        self.month_day = midb2s(buf, 5, 4)
        self.place_code = midb2s(buf, 9, 2)
        self.racing_times = midb2s(buf, 11, 2)
        self.racing_days = midb2s(buf, 13, 2)
        self.race_number = midb2s(buf, 15, 2)


class RaceID2:
    def __init__(self, buf: bytes):
        self.year = midb2s(buf, 1, 4)
        self.month_day = midb2s(buf, 5, 4)
        self.place_code = midb2s(buf, 9, 2)
        self.racing_times = midb2s(buf, 11, 2)
        self.racing_days = midb2s(buf, 13, 2)


class ResultsOfYear:
    def __init__(self, buf: bytes):
        self.year = midb2s(buf, 1, 4)
        self.prize = midb2s(buf, 5, 10)
        self.add_prize = midb2s(buf, 15, 10)
        self.arrival_frequency = [midb2s(buf, 25 + (6 * i), 6) for i in range(6)]


class ResentMajorAwards:
    def __init__(self, buf: bytes):
        self.race_id = RaceID(midb2b(buf, 1, 16))
        self.title = midb2s(buf, 17, 60)
        self.abbreviation = midb2s(buf, 77, 20)
        self.abbreviation_6 = midb2s(buf, 97, 12)
        self.abbreviation_3 = midb2s(buf, 109, 6)
        self.grade_code = midb2s(buf, 115, 1)
        self.horse_num = midb2s(buf, 116, 2)
        self.sire_id = midb2s(buf, 118, 10)
        self.horse_name = midb2s(buf, 128, 36)


class ArrivalFrequency3:
    def __init__(self, buf: bytes):
        self.arrival_freq = [midb2s(buf, 1 + (3 * i), 3) for i in range(6)]


class ArrivalFrequency4:
    def __init__(self, buf: bytes):
        self.arrival_freq = [midb2s(buf, 1 + (4 * i), 4) for i in range(6)]


class ArrivalFrequency5:
    def __init__(self, buf: bytes):
        self.arrival_freq = [midb2s(buf, 1 + (5 * i), 5) for i in range(6)]


class ArrivalFrequency6:
    def __init__(self, buf: bytes):
        self.arrival_freq = [midb2s(buf, 1 + (6 * i), 6) for i in range(6)]


class ResultsOf2Year:
    def __init__(self, buf: bytes):
        self.year = midb2s(buf, 1, 4)
        self.prize_flat = midb2s(buf, 5, 10)
        self.prize_hurdle = midb2s(buf, 15, 10)
        self.add_prize_flat = midb2s(buf, 25, 10)
        self.add_prize_hurdle = midb2s(buf, 35, 10)
        self.arrival_freq_flat = ArrivalFrequency6(midb2b(buf, 45, 36))
        self.arrival_freq_hurdle = ArrivalFrequency6(midb2b(buf, 81, 36))
        self.arrival_freq_place = [ArrivalFrequency6(midb2b(buf, 117 + 36 * i, 36)) for i in range(20)]
        self.arrival_freq_distance = [ArrivalFrequency6(midb2b(buf, 837 + i * 36, 36)) for i in range(6)]


class RaceInfo:
    def __init__(self, buf: bytes):
        self.day_of_week_id = midb2s(buf, 1, 1)
        self.special_race_num = midb2s(buf, 2, 4)
        self.title = midb2s(buf, 6, 60)
        self.subtitle = midb2s(buf, 66, 60)
        self.sub_subtitle = midb2s(buf, 126, 60)
        self.title_en = midb2s(buf, 186, 120)
        self.subtitle_en = midb2s(buf, 306, 120)
        self.sub_subtitle_en = midb2s(buf, 426, 120)
        self.abbreviation = midb2s(buf, 546, 20)
        self.abbreviation_6 = midb2s(buf, 566, 12)
        self.abbreviation_3 = midb2s(buf, 578, 6)
        self.name_classification = midb2s(buf, 584, 1)
        self.racing_times = midb2s(buf, 585, 3)


class ConditionInfo:
    def __init__(self, buf: bytes):
        self.weather = midb2s(buf, 1, 1)
        self.condition_turf = midb2s(buf, 2, 1)
        self.condition_dirt = midb2s(buf, 3, 1)


class RaceTerms:
    def __init__(self, buf: bytes):
        self.race_class_code = midb2s(buf, 1, 2)
        self.race_symbol_code = midb2s(buf, 3, 3)
        self.race_weight_code = midb2s(buf, 6, 1)
        self.race_term_code = [midb2s(buf, 7 + 3 * i, 3) for i in range(5)]
