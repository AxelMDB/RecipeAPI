from .unit import UnitDto


class IngredientDto:
    """description of class"""
    def __init__(self, ingredient: str = None, description: str = None):
        self.ingredient = ingredient
        self.description = description
