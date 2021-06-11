from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_service.base import Base


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

def Delete(entry, id: int, session):
    return session.delete(entry)