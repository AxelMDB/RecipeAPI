from Dtos import *


def MockRecipe():
    recipe = Recipe()
    recipe.recipe_name += "test name"
    recipe.recipe_desc += "this is a test recipe"
    recipe.recipe_culture += "test culture"
    for i in range(3):
        ingredient = RecipeIngredient()
        ingredient.ingredient += "test ingredient"
        ingredient.unit += "test unit"
        ingredient.quantity += "2"
        recipe.ingredient_list.append(ingredient)
    for i in range(3):
        procedure = RecipeProcedure()
        procedure.text = "test"
        recipe.procedure_list.append(procedure)
    return recipe
