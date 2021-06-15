from database_service.base import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

class ProceduresModel(Model):
    __tablename__ = 'procedures'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipe_info.id'))
    step = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)

    recipe = relationship("RecipeInfoModel", back_populates="procedures")