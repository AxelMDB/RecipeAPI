import Dtos
import Models
from sqlalchemy import exc
import database_service.sql_commands as db
import database_service.converters as conv

unit_types = {"volume", "mass"}
unit_numbers = {"integer", "decimal", "fraction"}

#region Units
def GetUnitsWithArguments(filters: dict):
    Units = Dtos.UnitsDto(units = [])
    Session = db.start_database()
    with Session() as session:
        session = db.GetLike(Models.UnitsModel, filters, session)
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
            return None
        Unit = conv.UnitsModelToDto(query)
        return Unit

def AddUnit(unit: Dtos.UnitDto):
    Session = db.start_database()
    with Session() as session:
        Unit = conv.UnitDtoToModel(unit)
        if Unit is None:
            return False
        session = db.Add(Unit, session)
        try: 
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False

def AddUnits(units: Dtos.UnitsDto):
    AllUnits = []
    for unit in units.units:
        Unit = conv.UnitDtoToModel(unit)
        if Unit is None:
            return False
        AllUnits.append(Unit)
    Session = db.start_database()
    with Session() as session:
        session = db.AddAll(AllUnits, session)
        try: 
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False

def UpdateUnit(unit: Dtos.UnitDto, id: int):
    Session = db.start_database()
    with Session() as session:
        Unit = db.GetById(Models.UnitsModel, id, session)
        if Unit is None:
            return False
        Unit = conv.UnitDtoToModel(unit, Unit)
        try:
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False

def DeleteUnit(id: int):
    Session = db.start_database()
    with Session() as session:
        Unit = db.GetById(Models.UnitsModel, id, session)
        if Unit is None:
            return False
        try:
            session.delete(Unit)
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False
#endregion 

#region Ingredients
def GetIngredientsWithArguments(filters: dict):
    Ingredients = Dtos.IngredientsDto(ingredients = [])
    Session = db.start_database()
    with Session() as session:
        session = db.GetLike(Models.IngredientsModel, filters, session)
        if not session:
            return Ingredients
        for row in session:
            Ingredient = conv.IngredientsModelToDto(row)
            Ingredients.ingredients.append(Ingredient)
    return Ingredients

def GetIngredientById(id: int):
    Ingredient = Dtos.IngredientDto()
    Session = db.start_database()
    with Session() as session:
        query = db.GetById(Models.IngredientsModel, id, session)
        if query is None:
            return None
        Ingredient = conv.IngredientsModelToDto(query)
        return Ingredient

def AddIngredient(ingredient: Dtos.IngredientDto):
    Session = db.start_database()
    with Session() as session:
        Ingredient = conv.IngredientDtoToModel(ingredient)
        if Ingredient is None:
            return False
        session =  db.Add(Ingredient, session)
        try: 
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False

def AddIngredients(ingredients: Dtos.IngredientsDto):
    AllIngredients = []
    for ingredient in ingredients.ingredients:
        Ingredient = conv.IngredientDtoToModel(ingredient)
        if Ingredient is None:
            return False
        AllIngredients.append(Ingredient)
    Session = db.start_database()
    with Session() as session:
        session = db.AddAll(AllIngredients, session)
        try: 
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False

def UpdateIngredient(ingredient: Dtos.IngredientDto, id: int):
    Session = db.start_database()
    with Session() as session:
        Ingredient = db.GetById(Models.IngredientsModel, id, session)
        if Ingredient is None:
            return False
        Ingredient = conv.IngredientDtoToModel(ingredient, Ingredient)
        try:
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False

def DeleteIngredient(id: int):
    Session = db.start_database()
    with Session() as session:
        Ingredient = db.GetById(Models.IngredientsModel, id, session)
        if Ingredient is None:
            return False
        try:
            session.delete(Ingredient)
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False
#endregion 

#region Cuisines
def GetCuisinesWithArguments(filters: dict):
    Cuisines = Dtos.CuisinesDto(cuisines = [])
    Session = db.start_database()
    with Session() as session:
        session = db.GetLike(Models.CuisinesModel, filters, session)
        if not session:
            return Cuisines
        for row in session:
            Cuisine = conv.CuisinesModelToDto(row)
            Cuisines.cuisines.append(Cuisine)
    return Cuisines

def GetCuisineById(id: int):
    Cuisine = Dtos.CuisineDto()
    Session = db.start_database()
    with Session() as session:
        query = db.GetById(Models.CuisinesModel, id, session)
        if query is None:
            return None
        Cuisine = conv.CuisinesModelToDto(query)
        return Cuisine

def AddCuisine(cuisine: Dtos.CuisineDto):
    Session = db.start_database()
    with Session() as session:
        Cuisine = conv.CuisineDtoToModel(cuisine)
        if Cuisine is None:
            return False
        session =  db.Add(Cuisine, session)
        try: 
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False

def AddCuisines(cuisines: Dtos.CuisinesDto):
    AllCuisines = []
    for ingredient in cuisines.cuisines:
        Cuisine = conv.CuisineDtoToModel(ingredient)
        if Cuisine is None:
            return False
        AllCuisines.append(Cuisine)
    Session = db.start_database()
    with Session() as session:
        session = db.AddAll(AllCuisines, session)
        try: 
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False

def UpdateCuisine(cuisine: Dtos.CuisineDto, id: int):
    Session = db.start_database()
    with Session() as session:
        Cuisine = db.GetById(Models.CuisinesModel, id, session)
        if Cuisine is None:
            return False
        Cuisine = conv.CuisineDtoToModel(cuisine, Cuisine)
        try:
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False

def DeleteCuisine(id: int):
    Session = db.start_database()
    with Session() as session:
        Cuisine = db.GetById(Models.CuisinesModel, id, session)
        if Cuisine is None:
            return False
        try:
            session.delete(Cuisine)
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False
#endregion 