from .recipe_ingredient import RecipeIngredientDto
from .recipe_procedure import RecipeProcedureDto
from .cuisine import CuisineDto
from typing import List


class RecipeDto(object):
    """description of class"""
    def __init__(self, recipe_name: str = None, recipe_desc: str = None, recipe_cuisine: str = None,
                 ingredient_list: List[RecipeIngredientDto] = [], procedure_list: List[RecipeProcedureDto] = []):
        self.recipe_name = recipe_name
        self.recipe_desc = recipe_desc
        self.recipe_cuisine = recipe_cuisine
        self.ingredient_list = ingredient_list
        self.procedure_list = procedure_list



