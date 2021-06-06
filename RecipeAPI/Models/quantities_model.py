from database_service.base import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text

class QuantitiesModel(Model):
    __tablename__ = 'quantities'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True,autoincrement=True)
    quantity = Column(Text)
    unit_id = Column(Integer, ForeignKey('units.id'))
    recipe_id = Column(Integer, ForeignKey('recipe_info.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))

