from typing import List
from .unit import UnitDto


class UnitsDto(object):
    """description of class"""
    def __init__(self, units : List[UnitDto] = []):
        self.units = units

