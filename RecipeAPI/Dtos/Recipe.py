from .ingredient import Ingredient
from .procedure import Procedure
from typing import List


class Recipe(object):
    """description of class"""
    def __init__(self, name: str = "", ingredients: List[Ingredient] = [], procedure: List[Procedure] = []):
        self.name = name
        self.ingredients = ingredients 
        self.procedure = procedure



