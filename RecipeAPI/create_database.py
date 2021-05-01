from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


Model = declarative_base(name='Model')


def main():
    engine = create_engine('sqlite:///recipes.db', echo=True)
    Model.metadata.create_all(engine)


class Ingredients(Model):
        __tablename__ = 'ingredients'

        id = Column(Integer, primary_key=True)
        description = Column(String)


if __name__ == '__main__':
    main()