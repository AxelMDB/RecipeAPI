from typing import List
from .equivalence import EquivalenceDto


class UnitDto(object):
    """description of class"""
    def __init__(self, unit: str = "", equivalence_units: List[EquivalenceDto] = []):
        self.unit = unit
        self.equivalence_units = equivalence_units
