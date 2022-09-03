"""
払い戻し情報
JV_HR_PAY
"""


from .common import *


class PayInfo1:
    """
    単勝、複勝、枠連
    """

    def __init__(self, buf: bytes):
        self.horse_number = midb2s(buf, 1, 2)
        self.pay = midb2s(buf, 3, 9)
        self.popularity = midb2s(buf, 12, 2)


class PayInfo2:
    """
    馬連、ワイド、予備、馬単
    """

    def __init__(self, buf: bytes):
        self.pair = midb2s(buf, 1, 4)
        self.pay = midb2s(buf, 5, 9)
        self.popularity = midb2s(buf, 14, 3)


class PayInfo3:
    """
    三連複
    """

    def __init__(self, buf: bytes):
        self.pair = midb2s(buf, 1, 6)
        self.pay = midb2s(buf, 7, 9)
        self.popularity = midb2s(buf, 16, 3)


class PayInfo4:
    """
    三連複
    """

    def __init__(self, buf: bytes):
        self.pair = midb2s(buf, 1, 6)
        self.pay = midb2s(buf, 7, 9)
        self.popularity = midb2s(buf, 16, 4)


class IFPayment:
    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.race_id = RaceID(midb2b(buf, 12, 16))
        self.register_num = midb2s(buf, 28, 2)
        self.enter_num = midb2s(buf, 30, 2)
        self.not_establish_flag = [midb2s(buf, 32 + i, 1) for i in range(9)]
        self.sp_payment_flag = [midb2s(buf, 41 + i, 1) for i in range(9)]
        self.return_flag = [midb2s(buf, 50 + i, 1) for i in range(9)]
        self.return_horse_number = [midb2s(buf, 59 + i, 1) for i in range(28)]
        self.return_gate_number = [midb2s(buf, 87 + i, 1) for i in range(8)]
        self.return_same_gate = [midb2s(buf, 95 + i, 1) for i in range(8)]
        self.pay_win = [PayInfo1(midb2b(buf, 103 + 13 * i, 13)) for i in range(3)]
        self.pay_place = [PayInfo1(midb2b(buf, 142 + 13 * i, 13)) for i in range(5)]
        self.pay_gate_quinella = [PayInfo1(midb2b(buf, 207 + 13 * i, 13)) for i in range(3)]
        self.pay_quinella = [PayInfo2(midb2b(buf, 246 + 16 * i, 16)) for i in range(3)]
        self.pay_quinella_place = [PayInfo2(midb2b(buf, 294 + 16 * i, 16)) for i in range(7)]
        self.pay_reserved1 = [PayInfo2(midb2b(buf, 406 + 16 * i, 16)) for i in range(3)]
        self.pay_exacta = [PayInfo2(midb2b(buf, 454 + 16 * i, 16)) for i in range(6)]
        self.pay_trio = [PayInfo3(midb2b(buf, 550 + 18 * i, 18)) for i in range(3)]
        self.pay_triefecta = [PayInfo3(midb2b(buf, 604 + 19 * i, 19)) for i in range(6)]
        self.crlf = midb2s(buf, 718, 2)
