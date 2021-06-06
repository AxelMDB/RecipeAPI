from typing import List
from .conversion import ConversionDto


class UnitDto(object):
    """description of class"""
    def __init__(self, unit: str = "", type: str = "", conversions: List[ConversionDto] = []):
        self.unit = unit
        self.type = type
        self.conversions = conversions
