from .recipe import RecipeDto
from typing import List


class RecipesDto(object):
    """description of class"""
    def __init__(self, recipes: List[RecipeDto] = []):
        self.recipes = recipes

