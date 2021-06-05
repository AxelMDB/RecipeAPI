from typing import List
from .culture import CultureDto


class CulturesDto(object):
    """description of class"""
    def __init__(self, cultures: List[CultureDto] = []):
        self.cultures = cultures

