from database_service.base import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship


class RecipeInfoModel(Model):
    __tablename__ = 'recipe_info'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_name = Column(Text, unique=True)
    recipe_desc = Column(Text, unique=True)
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'))

    procedures = relationship("ProceduresModel", back_populates="recipe")
    quantities = relationship("QuantitiesModel", back_populates="recipe")

    cuisine = relationship("CuisinesModel")