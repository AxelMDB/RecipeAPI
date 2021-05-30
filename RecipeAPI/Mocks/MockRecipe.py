from Dtos import *


def MockRecipe():
    recipe = RecipeDto()
    recipe.recipe_name += "test name"
    recipe.recipe_desc += "this is a test recipe"
    recipe.recipe_culture += "test culture"
    for i in range(3):
        ingredient = IngredientDto()
        ingredient.ingredient += "test ingredient"
        ingredient.unit += "test unit"
        recipe_ingredient = RecipeIngredientDto()
        recipe_ingredient.ingredient = ingredient
        quantity += "2"
        recipe.ingredient_list.append(recipe_ingredient)
    for i in range(3):
        procedure = RecipeProcedureDto()
        procedure.text = "test"
        recipe.procedure_list.append(procedure)
    return recipe
