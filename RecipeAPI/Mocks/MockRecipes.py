from Dtos import *


class MockRecipes(object):
    """description of class"""
    def __init__(self):
        self.recipes = []
        recipe = Recipe()
        recipe.name += "arepa"
        for i in range(3):
            procedure = Procedure()
            procedure.text += "hello"
            recipe.procedure.append(procedure)
        for i in range(3):
            ingredient = Ingredient()
            ingredient.ingredient += "cornflour"
            ingredient.unit += "cup"
            ingredient.quantity += "2 1/2"
            recipe.ingredients.append(ingredient)
        self.recipes.append(recipe)
