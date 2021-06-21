from database_service.base import Base as Model
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship


class IngredientsModel(Model):
    __tablename__ = 'ingredients'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    ingredient = Column(Text, unique=True, nullable=False)
    description = Column(Text)