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
            Unit.number = row.number
            Units.units.append(Unit)
    return Units

def GetUnitById(id: int):
    Unit = Dtos.UnitDto()
    Session = db.start_database()
    with Session() as session:
        query = db.GetById(Models.UnitsModel, id, session)
        if query is None:
            return None
        Unit.unit = query.unit
        Unit.type = query.type
        Unit.number = query.number
        return Unit

def AddUnit(unit: Dtos.UnitDto):
    Unit = Models.UnitsModel()
    Unit.unit = unit.unit.lower()
    Unit.type = unit.type.lower()
    Unit.number = unit.number.lower()
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

def UpdateUnit(unit: Dtos.UnitDto, id: int):
    Session = db.start_database()
    with Session() as session:
        Unit = db.GetById(Models.UnitsModel, id, session)
        if Unit is None:
            return false
        Unit.unit = unit.unit
        Unit.type = unit.type
        Unit.number = unit.number
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
            return false
        try:
            session.delete(Unit)
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print(e)
            session.rollback()
            return False