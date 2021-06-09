import Dtos
import Models
from sqlalchemy import exc
import database_service.sql_commands as db


def GetAllUnits():
    Units = Dtos.UnitsDto(units = [])
    Session = db.start_database()
    with Session() as session:
        for row in db.GetAll(Models.UnitsModel, session):
            Unit = Dtos.UnitDto()
            Unit.unit = row.unit
            Unit.type = row.type
            Units.units.append(Unit)
    return Units

def GetUnitById(id: int):
    Unit = Dtos.UnitDto()
    Session = db.start_database()
    with Session() as session:
        query = db.GetById(Models.UnitsModel, id, session)
        if query is not None:
            Unit.unit = query.unit
            Unit.type = query.type
        else:
            Unit = None
        return Unit

def AddUnit(unit: Dtos.UnitDto):
    Unit = Models.UnitsModel()
    Unit.unit = unit.unit.lower()
    Unit.type = unit.type.lower()
    Session = db.start_database()
    with Session() as session:
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
        Unit = Models.UnitsModel()
        Unit.unit = unit.unit
        Unit.type = unit.type
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


if __name__=="__main__":
    Session = db.start_database()
    with Session() as session:
        Recipe = Models.RecipeInfoModel()
        Recipe.recipe_name = "arepa"
        Procedure = Models.ProceduresModel()
        Procedure.step = 1
        Procedure.text = "hello"
        Quantity = Models.QuantitiesModel()
        Quantity.quantity = 1
        Quantity.unit = session.query(Models.UnitsModel).filter(Models.UnitsModel.unit == "cup").first()
        Quantity.ingredient = session.query(Models.IngredientsModel).filter(Models.IngredientsModel.ingredient == "arepa").first()
        Recipe.quantities.append(Quantity)
        Recipe.procedures.append(Procedure)
        session = db.Add(Recipe, session)
        try: 
            session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()