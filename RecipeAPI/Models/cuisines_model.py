from database_service.base import Base as Model
from sqlalchemy import Column, Integer, Text


class CuisinesModel(Model):
    __tablename__ = 'cuisine'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    cuisine = Column(Text, unique=True)