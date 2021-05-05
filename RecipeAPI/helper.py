from sqlalchemy import Column, Integer, ForeignKey, Text, create_engine, insert, select
from sqlalchemy.orm import declarative_base


Model = declarative_base()
db_name = "sqlite:///recipes.db"
engine = create_engine(db_name, echo=True)


def main():
    Model.metadata.create_all(engine)
    select_all(Ingredients)

#region Generic
def select_all(table):
    tablekeys = table.__table__.columns.keys()
    sel = select(table)
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = [1] * len(result)
        for i in range(len(result)):
            resultlist[i] = {}
            for key in range(len(result[i])):
                resultlist[i][tablekeys[key]] = result[i][key]
        print(resultlist)
#endregion

#region Ingredient queries
def select_ingredients_by_name(ingredient_name):
    ingredient_list = []
    sel = select(Ingredients).where(Ingredients.ingredient_name.in_(ingredient_name))
    with engine.connect() as conn:
        result = conn.execute(sel)
        for row in result:
            ingredient_list.append({'ingredient_name': row.ingredient_name})
    print(ingredient_list)


def select_all_ingredients():
    ingredient_list = []
    sel = select(Ingredients)
    with engine.connect() as conn:
        result = conn.execute(sel)
        for row in result:
            ingredient_list.append({'ingredient_name': row.ingredient_name})
    print(ingredient_list)


def insert_ingredients(ingredients):
    with engine.connect() as conn:
        for i in range(len(ingredients)):
            ins = insert(Ingredients).values(ingredient_name=ingredients[i])
            result = conn.execute(ins)
    print(result.inserted_primary_key)
#endregion

#region Measures
#endregion

def insert_recipes():
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

#region Models
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
#endregion

if __name__ == '__main__':
    main()
