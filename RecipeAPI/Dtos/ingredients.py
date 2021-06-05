from typing import List
from .ingredient import IngredientDto


class IngredientsDto(object):
    """description of class"""
    def __init__(self, ingredients: List[IngredientDto] = []):
        self.ingredients = ingredients
