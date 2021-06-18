import Dtos
import Models
from fractions import Fraction

unit_types = {"volume", "mass"}
unit_numbers = ["integer", "decimal", "fraction"]


def UnitsModelToDto(row):
    Unit = Dtos.UnitDto()
    Unit.unit = row.unit
    Unit.type = row.type
    Unit.number = row.number
    Unit.toSI = row.toSI
    Unit.SIto = row.SIto
    return Unit

def UnitDtoToModel(unit: Dtos.UnitDto, Unit: Models.UnitsModel = Models.UnitsModel()):
    global unit_types
    global unit_numbers
    if unit.unit is None:
        return None
    Unit.unit = unit.unit.lower()
    if unit.type.lower() not in unit_types or unit.number.lower() not in unit_numbers:
        return None
    Unit.type = unit.type.lower()
    Unit.number = unit.number.lower()
    Unit.toSI = unit.toSI
    Unit.SIto = unit.SIto
    Unit.offset = unit.offset
    return Unit

def IngredientsModelToDto(row):
    Ingredient = Dtos.IngredientDto()
    Ingredient.ingredient = row.ingredient
    Ingredient.description = row.description
    return Ingredient

def IngredientDtoToModel(ingredient: Dtos.IngredientDto,
                        Ingredient: Models.IngredientsModel = Models.IngredientsModel()):
    if ingredient.ingredient is None:
        return None
    Ingredient.ingredient = ingredient.ingredient.lower()
    Ingredient.description = ingredient.description
    return Ingredient

def CuisinesModelToDto(row):
    Cuisine = Dtos.CuisineDto()
    Cuisine.cuisine = row.cuisine
    Cuisine.description = row.description
    return Cuisine

def CuisineDtoToModel(cuisine: Dtos.CuisineDto,
                      Cuisine: Models.CuisinesModel = Models.CuisinesModel()):
    if cuisine.cuisine is None:
        return None
    Cuisine.cuisine = cuisine.cuisine.lower()
    Cuisine.description = cuisine.description
    return Cuisine

def NumberChecker(quantity: str):
    numbers = []
    try: 
        int(str)
        numbers.append(unit_numbers[0])
    except: 
        pass
    try:
        float(str)
        numbers.append(unit_numbers[1])
    except:
        pass
    try:
        Fraction(quantity)
        numbers.append(unit_numbers[2])
    except:
        pass
    return numbers

def RecipeInfoModelToDto(row):
    Recipe = Dtos.RecipeDto(ingredient_list = [], procedure_list = [])
    Recipe.recipe_name = row.recipe_name
    Recipe.recipe_desc = row.recipe_desc
    Recipe.recipe_cuisine = row.cuisine.cuisine
    for quantity in row.quantities:
        Ingredient = Dtos.RecipeIngredientDto()
        Ingredient.ingredient = quantity.ingredient.ingredient
        Ingredient.quantity = quantity.quantity
        Ingredient.unit = quantity.unit.unit
        Recipe.ingredient_list.append(Ingredient)
    for procedure in row.procedures:
        Procedure = Dtos.RecipeProcedureDto()
        Procedure.text = procedure.text
        Recipe.procedure_list.append(Procedure)
    return Recipe