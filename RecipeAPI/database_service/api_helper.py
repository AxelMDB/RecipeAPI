from sqlalchemy import exc
import werkzeug.exceptions as w_exc
import Dtos
import Models
import database_service.sql_commands as db
import database_service.converters as conv


#region Units
def GetUnitsWithArguments(filters: dict):
    Units = Dtos.UnitsDto(units = [])
    Session = db.start_database()
    with Session() as session:
        session = db.GetWithArguments(Models.UnitsModel, filters, session)
        if not session:
            return Units
        for row in session:
            Unit = conv.UnitsModelToDto(row)
            Units.units.append(Unit)
    return Units

def GetUnitById(id: int):
    Session = db.start_database()
    with Session() as session:
        query = db.GetById(Models.UnitsModel, id, session)
        if query is None:
            raise w_exc.NotFound()
        Unit = conv.UnitsModelToDto(query)
        return Unit

def AddUnit(unit: Dtos.UnitDto):
    Session = db.start_database()
    with Session() as session:
        Unit = conv.UnitDtoToModel(unit)
        if Unit is None:
            raise w_exc.BadRequest()
        session = db.Add(Unit, session)
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()

def AddUnits(units: Dtos.UnitsDto):
    AllUnits = []
    for unit in units.units:
        Unit = conv.UnitDtoToModel(unit)
        if Unit is None:
            raise w_exc.BadRequest()
        AllUnits.append(Unit)
    Session = db.start_database()
    with Session() as session:
        session = db.AddAll(AllUnits, session)
        try: 
            session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()

def UpdateUnit(unit: Dtos.UnitDto, id: int):
    Session = db.start_database()
    with Session() as session:
        Unit = db.GetById(Models.UnitsModel, id, session)
        if Unit is None:
            raise w_exc.BadRequest()
        Unit = conv.UnitDtoToModel(unit, Unit)
        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()

def DeleteUnit(id: int):
    Session = db.start_database()
    with Session() as session:
        Unit = db.GetById(Models.UnitsModel, id, session)
        if Unit is None:
            raise w_exc.NotFound()
        try:
            session.delete(Unit)
            session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.HTTPException()
#endregion 

#region Ingredients
def GetIngredientsWithArguments(filters: dict):
    Ingredients = Dtos.IngredientsDto(ingredients = [])
    Session = db.start_database()
    with Session() as session:
        session = db.GetWithArguments(Models.IngredientsModel, filters, session)
        if not session:
            return Ingredients
        for row in session:
            Ingredient = conv.IngredientsModelToDto(row)
            Ingredients.ingredients.append(Ingredient)
    return Ingredients

def GetIngredientById(id: int):
    Session = db.start_database()
    with Session() as session:
        query = db.GetById(Models.IngredientsModel, id, session)
        if query is None:
            raise w_exc.NotFound()
        Ingredient = conv.IngredientsModelToDto(query)
        return Ingredient

def AddIngredient(ingredient: Dtos.IngredientDto):
    Session = db.start_database()
    with Session() as session:
        Ingredient = conv.IngredientDtoToModel(ingredient)
        if Ingredient is None:
            raise w_exc.BadRequest()
        session =  db.Add(Ingredient, session)
        try: 
            session.commit()
            return
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()

def AddIngredients(ingredients: Dtos.IngredientsDto):
    AllIngredients = []
    for ingredient in ingredients.ingredients:
        Ingredient = conv.IngredientDtoToModel(ingredient)
        if Ingredient is None:
            raise w_exc.BadRequest()
        AllIngredients.append(Ingredient)
    Session = db.start_database()
    with Session() as session:
        session = db.AddAll(AllIngredients, session)
        try: 
            session.commit()
            return
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()

def UpdateIngredient(ingredient: Dtos.IngredientDto, id: int):
    Session = db.start_database()
    with Session() as session:
        Ingredient = db.GetById(Models.IngredientsModel, id, session)
        if Ingredient is None:
            raise w_exc.NotFound()
        Ingredient = conv.IngredientDtoToModel(ingredient, Ingredient)
        try:
            session.commit()
            return
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()

def DeleteIngredient(id: int):
    Session = db.start_database()
    with Session() as session:
        Ingredient = db.GetById(Models.IngredientsModel, id, session)
        if Ingredient is None:
            raise w_exc.NotFound()
        try:
            session.delete(Ingredient)
            session.commit()
            return
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.HTTPException()
#endregion 

#region Cuisines
def GetCuisinesWithArguments(filters: dict):
    Cuisines = Dtos.CuisinesDto(cuisines = [])
    Session = db.start_database()
    with Session() as session:
        session = db.GetWithArguments(Models.CuisinesModel, filters, session)
        if not session:
            return Cuisines
        for row in session:
            Cuisine = conv.CuisinesModelToDto(row)
            Cuisines.cuisines.append(Cuisine)
    return Cuisines

def GetCuisineById(id: int):
    Session = db.start_database()
    with Session() as session:
        query = db.GetById(Models.CuisinesModel, id, session)
        if query is None:
            raise w_exc.NotFound()
        Cuisine = conv.CuisinesModelToDto(query)
        return Cuisine

def AddCuisine(cuisine: Dtos.CuisineDto):
    Session = db.start_database()
    with Session() as session:
        Cuisine = conv.CuisineDtoToModel(cuisine)
        if Cuisine is None:
            raise w_exc.BadRequest()
        session =  db.Add(Cuisine, session)
        try: 
            session.commit()
            return
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()

def AddCuisines(cuisines: Dtos.CuisinesDto):
    AllCuisines = []
    for ingredient in cuisines.cuisines:
        Cuisine = conv.CuisineDtoToModel(ingredient)
        if Cuisine is None:
            raise w_exc.BadRequest()
        AllCuisines.append(Cuisine)
    Session = db.start_database()
    with Session() as session:
        session = db.AddAll(AllCuisines, session)
        try: 
            session.commit()
            return
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()

def UpdateCuisine(cuisine: Dtos.CuisineDto, id: int):
    Session = db.start_database()
    with Session() as session:
        Cuisine = db.GetById(Models.CuisinesModel, id, session)
        if Cuisine is None:
            raise w_exc.NotFound()
        Cuisine = conv.CuisineDtoToModel(cuisine, Cuisine)
        try:
            session.commit()
            return
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()

def DeleteCuisine(id: int):
    Session = db.start_database()
    with Session() as session:
        Cuisine = db.GetById(Models.CuisinesModel, id, session)
        if Cuisine is None:
            raise w_exc.NotFound()
        try:
            session.delete(Cuisine)
            session.commit()
            return
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.HTTPException()
#endregion 

#region Recipes
def GetRecipesWithArguments(filters: dict):
    Recipes = Dtos.RecipesDto(recipes = [])
    Session = db.start_database()
    with Session() as session:
        session = db.GetRecipeWithArguments(filters, session)
        if not session:
            return Recipes
        for row in session:
            Recipe = conv.RecipeInfoModelToDto(row)
            Recipes.recipes.append(Recipe)
    return Recipes

def GetRecipeById(id: int):
    Session = db.start_database()
    with Session() as session:
        query = db.GetById(Models.RecipeInfoModel, id, session)
        if query is None:
            raise w_exc.NotFound()
        Recipe = conv.RecipeInfoModelToDto(query)
        return Recipe

def AddOrUpdateRecipe(recipe: Dtos.RecipeDto, id: int = None):
    if id is None:
        RecipeDtoToModelAndAdd(recipe)
    else:
        RecipeDtoToModelAndAdd(recipe, id)

def DeleteRecipe(id: int):
    Session = db.start_database()
    with Session() as session:
        Recipe = db.GetById(Models.RecipeInfoModel, id, session)
        if Recipe is None:
            raise w_exc.NotFound()
        try:
            session.delete(Recipe)
            session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.HTTPException()

# needs session to bind the parameters
def RecipeDtoToModelAndAdd(recipe: Dtos.RecipeDto, id: int = None):
    Session = db.start_database()
    with Session() as session:
        if id is not None:
            Recipe = session.get(Models.RecipeInfoModel, id)
            if Recipe is None:
                raise w_exc.NotFound()
            for quantity in Recipe.quantities:
                session.delete(quantity)
            for procedure in Recipe.procedures:
                session.delete(procedure)
        else:
            Recipe = Models.RecipeInfoModel()
        Recipe.recipe_name = recipe.recipe_name
        Recipe.recipe_desc = recipe.recipe_desc
        Cuisine = session.query(Models.CuisinesModel).filter_by(cuisine=recipe.recipe_cuisine).first()
        if Cuisine is None:
            raise w_exc.BadRequest()
        Recipe.cuisine = Cuisine
        for ingredient in recipe.ingredient_list:
            Quantity = Models.QuantitiesModel()
            Quantity.ingredient = session.query(Models.IngredientsModel).\
                filter_by(ingredient=ingredient.ingredient).first()
            if Quantity.ingredient is None:
                raise w_exc.BadRequest()
            Quantity.unit = session.query(Models.UnitsModel).filter_by(unit=ingredient.unit).first()
            if Quantity.unit is None:
                raise w_exc.BadRequest()
            numbers = conv.NumberChecker(ingredient.quantity)
            if Quantity.unit.number not in numbers:
                raise w_exc.BadRequest()
            Quantity.quantity = ingredient.quantity
            Recipe.quantities.append(Quantity)
        count = 1
        for procedure in recipe.procedure_list:
            Procedure = Models.ProceduresModel()
            Procedure.text = procedure.text
            Procedure.step = count
            Recipe.procedures.append(Procedure)
            count += 1
        if id is None:
            session = db.Add(Recipe, session)
        try: 
            session.commit()
            return
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise w_exc.Conflict()
#endregion