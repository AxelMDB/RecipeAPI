from typing import List


class UnitDto(object):
    """description of class"""
    def __init__(self, unit: str = None, type: str = None, number : str = None,
                 toSI : float = 1.0, SIto : float = 1.0, offset : float = 0):
        self.unit = unit
        self.type = type
        self.number = number
        self.toSI = toSI
        self.SIto = SIto
        self.offset = offset
