from sqlalchemy import Column, Integer, String
from module1 import Model

class Ingredients(Model):
    def __init__(self):
        self.__tablename__ = 'ingredients'

        self.id = Column(Integer, primary_key=True)
        self.description = Column(String)