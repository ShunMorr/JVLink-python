import win32com.client
import datetime
import time
from typing import List
import pandas as pd
import numpy as np

from JVDataStruct import race_info, horse_race_info, horse_info
import modify
from database_io import MysqlIO
import table_struct


class JVLink:
    def __init__(self, mysql_io: MysqlIO):
        self.jvlink = win32com.client.Dispatch("JVDTLab.JVLink")
        self.init_jvlink()
        self.mysql = mysql_io

    def init_jvlink(self):
        ret = self.jvlink.JVInit('UNKNOWN')
        if ret != 0:
            raise ValueError

    def get_race_data(self, option: int, from_time: datetime.datetime,
                      to_time=datetime.datetime.now()):
        """
        Download data

        :param option:
        :param from_time:
        :param to_time:
        :return:
        """
        datetime_format = "%Y%m%d%H%M%S"
        data_period = f"{from_time.strftime(datetime_format)}-{to_time.strftime(datetime_format)}"
        ret_code, read_count, dl_count, last_timestamp = self.jvlink.JVOpen("RACE", data_period, option, 0, 0, 0)
        if ret_code < 0:
            raise ValueError(ret_code)
        if read_count == 0:
            raise ValueError
        if dl_count > 0:
            while True:
                status = self.jvlink.JVStatus()
                print(f"{status}/{dl_count}")
                if dl_count == status:
                    break
                else:
                    time.sleep(1)

        race_data = []
        race_horse_data = []
        race_ids = []
        while True:

            ret = self.jvlink.JVRead("", 1000000, "")
            if ret[0] == 0:
                break
            elif ret[0] == -1:
                continue
            elif ret[0] < -1:
                raise ValueError
            else:
                _record_type = ret[1][:2]
                if _record_type == "RA":
                    data = race_info.IFRaceInfo(ret[1])
                    if not data.id.place_code.isdigit():
                        continue
                    elif int(data.id.place_code) > 10:
                        continue
                    modified_data = modify.race_data(data)
                    race_data.append((modified_data.get_key(), *modified_data.get_value()))
                    race_ids.append(modified_data.get_key())

                elif _record_type == "SE":
                    data = horse_race_info.IFHorseRaceInfo(ret[1])
                    if not data.id.place_code.isdigit():
                        continue
                    elif int(data.id.place_code) > 10:
                        continue
                    race_horse_data.append(modify.horse_race_data(data).get_value())

                else:
                    self.jvlink.JVSkip()
        self.mysql.insert(table_struct.Race.get_table(),
                          [table_struct.Race.get_columns()[1], *table_struct.Race.get_columns()[0]],
                          race_data)
        self.mysql.insert(table_struct.Record.get_table(),
                          table_struct.Record.get_columns()[0],
                          race_horse_data)
        self.jvlink.JVClose()

        return sorted(race_ids)

    def get_horse_data(self, from_time: datetime.datetime):
        """
        Download data

        :return:
        """
        dataspec = "DIFF"
        option = 4
        datetime_format = "%Y%m%d%H%M%S"
        data_period = from_time.strftime(datetime_format)
        ret_code, read_count, dl_count, last_timestamp = self.jvlink.JVOpen(dataspec, data_period, option, 0, 0, 0)
        if ret_code < 0:
            raise ValueError(ret_code)
        if read_count == 0:
            raise ValueError
        if dl_count > 0:
            while True:
                status = self.jvlink.JVStatus()
                print(f"{status}/{dl_count}")
                if dl_count == status:
                    break
                else:
                    time.sleep(1)
        horse_data = []
        while True:
            ret = self.jvlink.JVRead("", 1000000, "")

            if ret[0] == 0:
                break
            elif ret[0] == -1:
                continue
            elif ret[0] < -1:
                raise ValueError
            else:
                record_type = ret[1][:2]
                if record_type == "UM":
                    data = horse_info.IFHorseInfo(ret[1])
                    horse_data.append(modify.horse_data(data).get_value())
                else:
                    self.jvlink.JVSkip()
        self.mysql.insert(table_struct.Horse.get_table(),
                          table_struct.Horse.get_columns()[0],
                          horse_data)
        self.jvlink.JVClose()

    def get_race_data_by_year(self, from_time: datetime.datetime, to_time=datetime.datetime.now()):
        from_year = from_time.year
        to_year = to_time.year
        temp_to_time = from_time
        for y in range(from_year, to_year - 1):
            print(f"Loading {y} - {y + 1} data")
            temp_from_time = from_time.replace(year=y)
            temp_to_time = from_time.replace(year=y + 1)
            race_id_list = self.get_race_data(4, temp_from_time, temp_to_time)
            self.update_records(race_id_list)
        race_id_list = self.get_race_data(4, temp_to_time, to_time)
        self.update_records(race_id_list)

    def update_records(self, race_id_list: List[int]):

        horse_data_columns = [table_struct.Record.get_columns()[1], *table_struct.Record.get_columns()[0]]
        for race_id in race_id_list:
            horse_list = []
            tmp_race_info = table_struct.Race(*(self.mysql.select(
                table_struct.Race.get_table(),
                table_struct.Race.get_columns()[1],
                race_id)[0]))

            tmp_horse_data = self.mysql.select(table_struct.Record.get_table(), "race_id", race_id)
            h_df = pd.DataFrame(tmp_horse_data, columns=horse_data_columns)
            h_df = h_df[h_df["order"] != 0]

            _wcol = h_df["weight"]
            if _wcol.max() - _wcol.min() == 0:
                _weight_ad = 0
            else:
                _weight_ad = (_wcol - _wcol.mean()) / (_wcol.max() - _wcol.min()) * 4800 / (
                        7000 - tmp_race_info.distance)
            h_df["advantage"] = round(np.sign(tmp_race_info.field) * (1 - 2 * h_df["horse_number"] / len(h_df)) * h_df[
                "style"] / 4 - _weight_ad, 3)
            h_df["corrected_time"] = round(h_df["time"] * (500 + h_df["advantage"]) / 500, 3)
            _cor_time = h_df['corrected_time']
            _std = _cor_time.std(ddof=0)
            _mean = _cor_time.mean()
            h_df['inner_level'] = round(_cor_time.map(lambda x: -(x - _mean) / _std * 10 + 50), 3)

            h_df["record_id_bf"] = h_df["horse_name"].map(self._get_race_id_func)
            horse_data_list = [(*table_struct.Record(*x).get_value(), x["id"]) for _, x in h_df.iterrows()]

            for _, row in h_df.iterrows():
                horse_name = row["horse_name"]
                style = row["style"]
                level_this = row["inner_level"] * (1 + row["advantage"] / 10) * tmp_race_info.race_level
                if row["record_id_bf"] == 0:
                    level = level_this
                    opt_distance = tmp_race_info.distance
                    opt_field = tmp_race_info.field
                else:
                    _level, _opt_distance, _opt_field = self._get_record(row["record_id_bf"])
                    level = (_level + row["inner_level"] * (1 + row["advantage"] / 20) * tmp_race_info.race_level) / 2
                    opt_distance = (_opt_distance * _level + tmp_race_info.distance * level_this) / (
                            _level + level_this)
                    opt_field = (_opt_field * _level + tmp_race_info.field * level_this) / (_level + level_this)
                try:
                    tmp_horse_record = table_struct.HorseRecord(
                        0, horse_name, race_id, round(level, 3), style, int(opt_distance), round(opt_field, 3)
                    )
                except ValueError:
                    print(2)
                record_id = self.mysql.insert_one(tmp_horse_record.get_table(),
                                                  tmp_horse_record.get_columns()[0],
                                                  tmp_horse_record.get_value())
                horse_list.append((record_id, horse_name))
            self.mysql.update(
                table_struct.Record.get_table(),
                table_struct.Record.get_columns()[0],
                table_struct.Record.get_columns()[1],
                horse_data_list
            )
            self.mysql.update(
                table_struct.Horse.get_table(),
                ["record_id"],
                "name",
                horse_list
            )

    def _get_record(self, _record_id: int):
        record = table_struct.HorseRecord(*(self.mysql.select(
            table_struct.HorseRecord.get_table(),
            table_struct.HorseRecord.get_columns()[1],
            _record_id
        )[0]))
        return record.level, record.opt_distance, record.opt_field

    def _get_race_id_func(self, x):
        return table_struct.Horse(*(self.mysql.select(table_struct.Horse.get_table(), "name", x)[0])).record_id


if __name__ == "__main__":
    mysql = MysqlIO()
    jvlink = JVLink(mysql)
    from_day = datetime.datetime.strptime("20210101", "%Y%m%d")
    jvlink.get_horse_data(from_day)
    jvlink.get_race_data_by_year(from_day)
