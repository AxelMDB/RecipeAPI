from database_service.base import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship


class RecipeInfoModel(Model):
    __tablename__ = 'recipe_info'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    recipe_name = Column(Text, unique=True, nullable=False)
    recipe_desc = Column(Text)
    cuisine_id = Column(Integer, ForeignKey('cuisine.id'))

    cuisine = relationship("CuisinesModel")
    procedures = relationship("ProceduresModel", back_populates="recipe",
                              cascade = "all, delete, delete-orphan", order_by="ProceduresModel.step")
    quantities = relationship("QuantitiesModel", back_populates="recipe",
                              cascade = "all, delete, delete-orphan")

