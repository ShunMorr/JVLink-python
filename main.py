import win32com.client
import datetime
import time

from JVDataStruct import race_info


class JVLink:
    def __init__(self):
        self.jvlink = win32com.client.Dispatch("JVDTLab.JVLink")
        self.init_jvlink()

    def init_jvlink(self):
        ret = self.jvlink.JVInit('UNKNOWN')
        if ret != 0:
            raise ValueError
        # ret = self.jvlink.JVSetUIProperties()
        # if not ret:
        #     raise ValueError

    def get_data(self, dataspec: str, option: int, from_time: datetime.datetime, to_time=datetime.datetime.now()):
        """
        Download data

        :param dataspec:
        :param option:
        :param from_time:
        :param to_time:
        :return:
        """
        datetime_format = "%Y%m%d%H%M%S"
        data_period = f"{from_time.strftime(datetime_format)}-{to_time.strftime(datetime_format)}"
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
                # print(ret[1])
                if record_type == "RA":
                    # print(ret[1])
                    race_data=race_info.IFRaceInfo(ret[1])
                    print(race_data)
                # else:
                #     self.jvlink.JVSkip()

    # def _read_data(self,filename):
    #     """
    #
    #     :return:
    #     """
    #     with open()


if __name__ == "__main__":
    jvlink = JVLink()
    last_monday = datetime.datetime.now() - datetime.timedelta(days=7)
    print(last_monday)
    jvlink.get_data("RACE", 1, last_monday)
