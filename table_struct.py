from dataclasses import dataclass


@dataclass
class Horse:
    """
    id: int
    name: str
    race_id: int
    """
    id: int
    name: str
    record_id: int

    def get_value(self):
        return self.name, self.record_id

    def get_key(self):
        return self.id

    @staticmethod
    def get_columns():
        return ("name", "record_id"), "id"

    @staticmethod
    def get_table():
        return "t_horse"


@dataclass
class HorseRecord:
    """
    id: int
    horse_name: str
    race_id: int
    level: float
    style: float
    opt_distance: int
    opt_field: float
    """
    id: int
    horse_name: str
    race_id: int
    level: float
    style: float
    opt_distance: int
    opt_field: float

    def get_value(self):
        return self.horse_name, self.race_id, self.level, self.style, self.opt_distance, self.opt_field

    def get_key(self):
        return self.id

    @staticmethod
    def get_columns():
        return ("horse_name", "race_id", "level", "style", "optimal_distance", "optimal_field"), "id"

    @staticmethod
    def get_table():
        return "t_horserecord"


@dataclass
class Race:
    """
    id: int
    field: float
    race_level: float
    place: int
    distance: int
    """
    id: int
    field: float
    race_level: float
    place: int
    distance: int

    def get_value(self):
        return self.field, self.race_level, self.place, self.distance

    def get_key(self):
        return self.id

    @staticmethod
    def get_columns():
        return ("field", "race_level", "place", "distance"), "id"

    @staticmethod
    def get_table():
        return "t_race"


@dataclass
class Record:
    """
    id: int
    horse_name: str
    race_id: int
    race_id_bf: int
    horse_number: int
    weight: float
    fluctuation: int
    advantage: float
    order: int
    inner_level: float
    style: int
    time: float
    corrected_time: float
    """
    id: int
    horse_name: str
    race_id: int
    record_id_bf: int
    horse_number: int
    weight: float
    fluctuation: int
    advantage: float
    order: int
    inner_level: float
    style: int
    time: float
    corrected_time: float

    def get_value(self):
        return self.horse_name, self.race_id, self.record_id_bf, self.horse_number, self.weight, self.fluctuation, \
               self.advantage, self.order, self.inner_level, self.style, self.time, self.corrected_time

    def get_key(self):
        return self.id

    @staticmethod
    def get_columns():
        return ("horse_name", "race_id", "record_id_bf", "horse_number", "weight", "fluctuation", "advantage", "order",
                "inner_level", "style", "time", "corrected_time"), "id"

    @staticmethod
    def get_table():
        return "t_record"
