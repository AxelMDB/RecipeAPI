from DatabaseService.DeclarativeBase import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text


class Cultures(Model):
    __tablename__ = 'culture'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    culture = Column(Text, unique=True)