from Dtos import *
from Models import *
from sqlalchemy import exc
import DatabaseService.sql_commands as sql


def AddUnit(unit: UnitDto):
    Unit = UnitsModel()
    Unit.unit = unit.unit
    Session = sql.start_database()
    with Session() as session:
        session = sql.Add(Unit, session)
        try: 
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False


def GetAllUnits():
    Units = UnitsDto(units = [])
    Session = sql.start_database()
    with Session() as session:
        for row in sql.GetAll(UnitsModel, session):
            Unit = UnitDto()
            Unit.unit = row.unit
            Units.units.append(Unit)
    return Units


def GetUnitById(id: int):
    Unit = UnitDto()
    Session = sql.start_database()
    with Session() as session:
        query = sql.GetById(UnitsModel, id, session)
        if query is not None:
            Unit.unit = query.unit
        else:
            Unit = None
        return Unit