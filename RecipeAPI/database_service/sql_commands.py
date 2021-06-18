from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import database_service.base
from database_service.base import Base
from Models import RecipeInfoModel, QuantitiesModel, IngredientsModel, CuisinesModel


def start_database():
    db_name = "sqlite:///recipes.db"
    engine = create_engine(db_name, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session

def Add(entry, session):
    session.add(entry)
    return session

def AddAll(entries: list, session):
    session.add_all(entries)
    return session

def GetAll(table: Base, session):
    return session.query(table) 

def GetById(table: Base, id: int, session):
    return session.query(table).filter(table.id == id).first()

def GetWithArguments(table: Base, filters: dict, session):
    statement = session.query(table)
    for key, value in filters.items():
        if value is not list:
            statement = statement.filter(getattr(table, key) == value)
        else:
            statement = statement.filter(getattr(table, key).in_(value))
    return statement

def GetRecipeWithArguments(filters: dict, session):
    statement = session.query(RecipeInfoModel)
    for key, value in filters.items():
        if key == "ingredient":
           statement = statement.join(QuantitiesModel).join(IngredientsModel)\
               .filter(IngredientsModel.ingredient.in_(value)) 
        elif key == "recipe_cuisine":
            statement = statement.join(CuisinesModel)\
                .filter(CuisinesModel.cuisine.in_(value))
        else:
            statement = statement.filter(getattr(RecipeInfoModel, key).in_(value))
    return statement

