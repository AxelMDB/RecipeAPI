from .ingredient import IngredientDto


class RecipeIngredientDto(object):
    """description of class"""
    def __init__(self, ingredient: str = None, quantity: str = None, unit: str = None):
        self.ingredient = ingredient
        self.quantity = quantity
        self.unit = unit
