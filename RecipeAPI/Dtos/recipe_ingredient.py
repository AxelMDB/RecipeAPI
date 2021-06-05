from .ingredient import IngredientDto


class RecipeIngredientDto(object):
    """description of class"""
    def __init__(self, ingredient: IngredientDto, quantity: str = ""):
        self.ingredient = ingredient
        self.quantity = quantity

