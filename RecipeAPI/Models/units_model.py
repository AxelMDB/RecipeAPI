from database_service.base import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text, Float
from sqlalchemy.orm import relationship


class UnitsModel(Model):
    __tablename__ = 'units'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    unit = Column(Text, unique=True, nullable=False)
    type = Column(Text, nullable=False)
    number = Column(Text, nullable=False)
    toSI = Column(Float)
    SIto = Column(Float)
    offset = Column(Float)