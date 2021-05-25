from .recipe import Recipe
from typing import List


class Recipes(object):
    """description of class"""
    def __init__(self, recipes: List[Recipe] = []):
        self.recipes = recipes

