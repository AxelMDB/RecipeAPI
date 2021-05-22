from DatabaseService.DeclarativeBase import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text


class RecipeName(Model):
    __tablename__ = 'recipe_names'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True)