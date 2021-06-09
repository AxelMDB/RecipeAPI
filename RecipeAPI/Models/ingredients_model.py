from database_service.base import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship


class IngredientsModel(Model):
    __tablename__ = 'ingredients'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient = Column(Text, unique=True)
    main_unit_id = Column(Integer, ForeignKey('units.id'))

    main_unit = relationship("UnitsModel")