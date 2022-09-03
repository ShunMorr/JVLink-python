"""
票数に関する構造体
JV_H1_HYOSU_ZENKAKE
JV_H6_HYOSU_SANRENTAN
"""

from .common import *


class VoteInfo1:
    """
    単勝、複勝、枠連
    """

    def __init__(self, buf: bytes):
        self.horse_number = midb2s(buf, 1, 2)
        self.vote = midb2s(buf, 3, 11)
        self.popularity = midb2s(buf, 14, 2)


class VoteInfo2:
    """
    馬連、ワイド、馬単
    """

    def __init__(self, buf: bytes):
        self.pair = midb2s(buf, 1, 4)
        self.vote = midb2s(buf, 5, 11)
        self.popularity = midb2s(buf, 16, 3)


class VoteInfo3:
    """
    三連複
    """

    def __init__(self, buf: bytes):
        self.pair = midb2s(buf, 1, 6)
        self.vote = midb2s(buf, 7, 11)
        self.popularity = midb2s(buf, 18, 3)


class VoteInfo4:
    """
    三連単
    """

    def __init__(self, buf: bytes):
        self.pair = midb2s(buf, 1, 6)
        self.vote = midb2s(buf, 7, 11)
        self.popularity = midb2s(buf, 18, 4)


class IFVoteAll:
    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.race_id = RaceID(midb2b(buf, 12, 16))
        self.register_num = midb2s(buf, 28, 2)
        self.enter_num = midb2s(buf, 30, 2)
        self.launch_flag = [midb2s(buf, 32 + i, 1) for i in range(7)]
        self.place_flag = midb2s(buf, 39, 1)
        self.return_horse_number = [midb2s(buf, 40 + i, i) for i in range(28)]
        self.return_gate_number = [midb2s(buf, 68 + i, i) for i in range(8)]
        self.return_same_gate = [midb2s(buf, 76 + i, i) for i in range(8)]
        self.vote_win = [VoteInfo1(midb2b(buf, 84 + 15 * i, 15)) for i in range(28)]
        self.vote_place = [VoteInfo1(midb2b(buf, 504 + 15 * i, 15)) for i in range(28)]
        self.vote_gate_quinella = [VoteInfo1(midb2b(buf, 924 + 15 * i, 15)) for i in range(36)]
        self.vote_quinella = [VoteInfo2(midb2b(buf, 1464 + 18 * i, 18)) for i in range(153)]
        self.vote_place_quinella = [VoteInfo2(midb2b(buf, 4218 + 18 * i, 18)) for i in range(153)]
        self.vote_exacta = [VoteInfo2(midb2b(buf, 6972 + 18 * i, 18)) for i in range(306)]
        self.vote_trio = [VoteInfo3(midb2b(buf, 12480 + 20 * i, 20)) for i in range(816)]
        self.vote_total = [midb2s(buf, 28800 + 11 * i, 11) for i in range(14)]
        self.crlf = midb2s(buf, 28954, 2)


class IFVoteTriefecta:
    def __init__(self, buf_str: str):
        buf = buf_str.encode(ENCODE)
        self.header = RecordID(midb2b(buf, 1, 11))
        self.race_id = RaceID(midb2b(buf, 12, 16))
        self.register_num = midb2s(buf, 28, 2)
        self.enter_num = midb2s(buf, 30, 2)
        self.launch_flag = midb2s(buf, 32, 1)
        self.return_horse_number = [midb2s(buf, 33 + i, i) for i in range(18)]
        self.vote_triefecta = [VoteInfo4(midb2b(buf, 51 + 21 * i, 21)) for i in range(4896)]
        self.vote_total = [midb2s(buf, 102867 + 11 * i, 11) for i in range(2)]
        self.crlf = midb2s(buf, 28954, 2)
