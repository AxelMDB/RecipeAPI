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
    Unit.unit = unit.unit
    Unit.type = unit.type
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
    Recipe = Models.RecipeInfoModel(recipe_name="Arepa")
    procedure = Models.ProceduresModel(step=1, text="hello")
    Recipe.procedures.append(procedure)
    Session = db.start_database()
    with Session() as session:
        session = db.Add(Recipe, session)
        try: 
            session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
    # actually works!
    """INSERT INTO recipe_info (recipe_name, recipe_desc, cuisine_id) VALUES (?, ?, ?)
       [generated in 0.00173s] ('Arepa', None, None)
       INSERT INTO procedures (recipe_id, step, text) VALUES (?, ?, ?)
       [generated in 0.00188s] (1, 1, 'hello')
       COMMIT"""