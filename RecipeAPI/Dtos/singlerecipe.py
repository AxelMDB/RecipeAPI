from .recipe_ingredient import RecipeIngredient
from .recipe_procedure import RecipeProcedure
from typing import List


class Recipe(object):
    """description of class"""
    def __init__(self, recipe_name: str = "", recipe_desc: str = "", recipe_culture: str = "",
                 ingredient_list: List[RecipeIngredient] = [], procedure_list: List[RecipeProcedure] = []):
        self.recipe_name = recipe_name
        self.recipe_desc = recipe_desc
        self.recipe_culture = recipe_culture
        self.ingredient_list = ingredient_list
        self.procedure_list = procedure_list



