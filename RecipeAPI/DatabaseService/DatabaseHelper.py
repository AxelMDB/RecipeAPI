from sqlalchemy import create_engine, insert, select, update, delete, exc
from sqlalchemy.orm import sessionmaker
from DatabaseService.DeclarativeBase import Base
from Models import *
from Dtos import *


db_name = "sqlite:///:memory:"
engine = create_engine(db_name, echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()


def dbtests():
    recipes = []
    recipe = Recipe()
    recipe.name += "Arepa"
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
    recipes.append(recipe)
    insert_recipes(recipes)
    print(Get(RecipeName).first().name)


def AddOrUpdateAll(tables: Base):
    try: 
        session.add_all(tables)
        session.flush()
    except exc.IntegrityError:
        session.rollback()
    finally:
        session.commit()


def Get(table):
    return session.query(table) 


def get_ingredients_by_names(names: list):
    return session.query(Ingredients).filter(Ingredients.ingredient.in_(names))

    
def insert_recipes(recipes):
    for recipe in recipes:
        name = RecipeName()
        name.name = recipe.name.lower()
        AllIngredients = []
        AllUnits = []
        AllQuantities = []
        AllProcedures = []
        for ing in recipe.ingredients:
            Ingredient = Ingredients()
            Ingredient.ingredient = ing.ingredient.lower()
            AllIngredients.append(Ingredient)
            AllQuantities.append(ing.quantity)
            Unit = Units()
            Unit.unit = ing.unit.lower()
            AllUnits.append(Unit)
        AddOrUpdateAll([name])
        for i in range(len(recipe.procedure)):
            Procedure = Procedures()
            Procedure.text = recipe.procedure[i].text
            Procedure.recipe_id = name.id
            Procedure.step = i
            AllProcedures.append(Procedure)
        AddOrUpdateAll(AllIngredients)
        AddOrUpdateAll(AllUnits)
        AddOrUpdateAll(AllProcedures)
        quantities = []
        for i in range(len(AllIngredients)):
            Quantity = Quantities()
            if AllIngredients[i].id == None and i != 0:
               AllIngredients[i] = AllIngredients[i - 1]
            Quantity.ingredient_id = AllIngredients[i].id
            Quantity.quantity = AllQuantities[i]
            Quantity.recipe_id = name.id
            if AllUnits[i].id == None and i != 0:
                AllUnits[i] = AllUnits[i - 1]
            Quantity.unit_id = AllUnits[i].id
            quantities.append(Quantity)
        AddOrUpdateAll(quantities)
            

if __name__ == '__main__':
    dbtests()
