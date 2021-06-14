import Dtos
import Models
from sqlalchemy import exc
import database_service.sql_commands as db

unit_types = {"volume", "mass"}
unit_numbers = {"integer", "decimal", "fraction"}


def GetUnitsWithArguments(filters: dict):
    Units = Dtos.UnitsDto(units = [])
    Session = db.start_database()
    with Session() as session:
        result = db.GetWithArguments(Models.UnitsModel, filters, session)
        for row in result:
            Unit = UnitsModelToDto(row)
            Units.units.append(Unit)
    return Units

def GetUnitById(id: int):
    Unit = Dtos.UnitDto()
    Session = db.start_database()
    with Session() as session:
        query = db.GetById(Models.UnitsModel, id, session)
        if query is None:
            return None
        Unit = UnitsModelToDto(query)
        return Unit

def AddUnit(unit: Dtos.UnitDto):
    Session = db.start_database()
    with Session() as session:
        Unit = UnitDtoToModel(unit)
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
        Unit = UnitDtoToModel(unit)
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
        Unit = UnitDtoToModel(unit, Unit)
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

def UnitsModelToDto(row):
    Unit = Dtos.UnitDto()
    Unit.unit = row.unit
    Unit.type = row.type
    Unit.number = row.number
    Unit.toSI = row.toSI
    Unit.SIto = row.SIto
    return Unit

def UnitDtoToModel(unit: Dtos.UnitsDto, Unit: Models.UnitsModel = Models.UnitsModel()):
    global unit_types
    global unit_numbers
    Unit.unit = unit.unit.lower()
    if unit.type.lower() not in unit_types or unit.number.lower() not in unit_numbers:
        return None
    Unit.type = unit.type.lower()
    Unit.number = unit.number.lower()
    Unit.toSI = unit.toSI
    Unit.SIto = unit.SIto
    Unit.offset = unit.offset
    return Unit