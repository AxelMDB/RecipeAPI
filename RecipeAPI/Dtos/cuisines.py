from typing import List
from .cuisine import CuisineDto


class CuisinesDto(object):
    """description of class"""
    def __init__(self, cuisines: List[CuisineDto] = []):
        self.cuisines = cuisines

