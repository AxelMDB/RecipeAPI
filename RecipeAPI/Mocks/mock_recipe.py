import Dtos


def MockRecipe():
    Recipe = Dtos.RecipeDto(ingredient_list=[], procedure_list=[])
    Recipe.recipe_name = "test"
    Recipe.recipe_desc = "this is a test recipe"
    Recipe.recipe_cuisine = "italian test"
    Ing_1 = Dtos.RecipeIngredientDto(ingredient="ingredient 1", quantity="1/2", unit="cup")
    Ing_2 = Dtos.RecipeIngredientDto(ingredient="ingredient 2", quantity="1/2", unit="cup")
    Ing_3 = Dtos.RecipeIngredientDto(ingredient="ingredient 3", quantity="300", unit="grams")
    Recipe.ingredient_list.append(Ing_1)
    Recipe.ingredient_list.append(Ing_2)
    Recipe.ingredient_list.append(Ing_3)
    Procedure_1 = Dtos.RecipeProcedureDto(text="step 1")
    Procedure_2 = Dtos.RecipeProcedureDto(text="step 2")
    Procedure_3 = Dtos.RecipeProcedureDto(text="step 3")
    Recipe.procedure_list.append(Procedure_1)
    Recipe.procedure_list.append(Procedure_2)
    Recipe.procedure_list.append(Procedure_3)
    return Recipe