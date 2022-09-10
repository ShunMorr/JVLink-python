from JVDataStruct import race_info, horse_race_info, horse_info
import math

import table_struct


def race_data(data: race_info.IFRaceInfo) -> table_struct.Race:
    """
    レースデータをSQL Insert用のタプルに整形する

    :param data:
    :return: Tuple
    """
    race_id = data.id.get_id()
    _track_code_sign = 1 if int(data.track_code) < 23 else -1  # トラックコードが22以下なら芝、それ以上ならダート判定
    _condition = int(data.condition.condition_turf) if _track_code_sign == 1 else int(data.condition.condition_dirt)
    field = round(_track_code_sign * (4 - _condition) / 3, 3)
    _grade = data.grade_code
    if _grade == "A":
        race_level = 1.4
    elif _grade in ["B", "F"]:
        race_level = 1.3
    elif _grade in ["C", "G"]:
        race_level = 1.2
    elif _grade in ["D", "E", "H", "L"]:
        race_level = 1.1
    else:
        _prize = max(int(data.prize_bf[0]) / 10000, int(data.prize[0]) / 10000)
        race_level = round(0.45 + 0.22 * math.log(_prize), 3)
    racecourse = int(data.id.place_code)
    distance = int(data.distance)
    return table_struct.Race(race_id, field, race_level, racecourse, distance)


def horse_race_data(data: horse_race_info.IFHorseRaceInfo) -> table_struct.Record:
    name = data.horse_name.strip()
    race_id = data.id.get_id()
    style = int(data.style)
    running_time = int(data.time[0]) * 60 + int(data.time[1:]) / 10
    order = int(data.order)
    fluctuation = int(data.fluctuation) if data.fluctuation.isdigit() else 0
    horse_number = int(data.horse_number)
    weight = int(data.weight) / 10
    return table_struct.Record(0, name, race_id, 0, horse_number, weight, fluctuation,
                               0, order, 0, style, running_time, 0)


def horse_data(data: horse_info.IFHorseInfo) -> table_struct.Horse:
    return table_struct.Horse(0, data.name.strip(), 0)
