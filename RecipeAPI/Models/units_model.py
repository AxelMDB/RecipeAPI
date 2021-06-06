from database_service.base import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text


class UnitsModel(Model):
    __tablename__ = 'units'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    unit = Column(Text, unique=True)
    type = Column(Text)