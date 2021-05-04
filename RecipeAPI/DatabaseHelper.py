from sqlalchemy import Column, Integer, ForeignKey, Text, create_engine, insert, select
from sqlalchemy.orm import declarative_base, relationship


Model = declarative_base()
db_name = "sqlite:///recipes.db"
engine = create_engine(db_name, echo=True)


def main():
    Model.metadata.create_all(engine)
    select_all_ingredients()


def select_all_ingredients():
    sel = select(Ingredients)
    conn = engine.connect()
    result = conn.execute(sel)
    print(result.fetchall())


def insert_ingredients(ingredients):
    engine = create_engine(db_name, echo=True)
    for i in range(len(ingredients)):
        ins = insert(Ingredients).values(ingredient_name=ingredients[i])
        conn = engine.connect()
        result = conn.execute(ins)
        print(result.inserted_primary_key)


def insert_procedures():
    RecipeExample = [
                        {
                            'recipe_name': 'arepa',
                            'ingredients': 
                            [
                                {
                                    'ingredient': 'cornflour',
                                    'quantity': '2',
                                    'unit': 'cup'
                                },
                                {
                                    'ingredient': 'water',
                                    'quantity': '2 1/2',
                                    'unit': 'cup'
                                },
                                {
                                    'ingredient': 'salt',
                                    'quantity': 'a',
                                    'unit': 'pinch'
                                },
                            ],
                            'procedure': 'text'
                        } 
                    ]


class Ingredients(Model):
    __tablename__ = 'ingredients'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    ingredient_name = Column(Text)


class Measures(Model):
    __tablename__ = 'measures'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    unit = Column(Text)


class Procedures(Model):
    __tablename__ = 'procedures'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    recipe_name = Column(Text)
    procedure = Column(Text)


class RecipeIndex(Model):
    __tablename__ = 'recipe_index'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    procedure_id = Column(Integer, ForeignKey('procedures.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    quantity = Column(Text)
    measure_id = Column(Integer, ForeignKey('measures.id'))


if __name__ == '__main__':
    main()