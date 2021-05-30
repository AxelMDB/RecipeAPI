from DatabaseService.DeclarativeBase import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text


class RecipeInfo(Model):
    __tablename__ = 'recipe_info'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_name = Column(Text, unique=True)
    recipe_desc = Column(Text, unique=True)
    culture_id = Column(Integer, ForeignKey('culture.id'))
