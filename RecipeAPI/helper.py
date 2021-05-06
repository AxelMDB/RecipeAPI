from sqlalchemy import Column, Integer, ForeignKey, Text, create_engine, insert, select, update, delete
from sqlalchemy.orm import declarative_base


Model = declarative_base()
db_name = "sqlite:///:memory:"
engine = create_engine(db_name, echo=True)


def test():
    Model.metadata.create_all(engine)
    ingredients = [{'ingredient':'cornflour'}, {'ingredient':'water'},{'ingredient':'salt'}, {'ingredient':'butter'}]
    insert_into(Ingredients, ingredients)
    select_all(Ingredients)
    select_by_ids(Ingredients, [1,3,4])
    update_by_ids(Ingredients, [4], [{'ingredient':'oil'}])
    select_all(Ingredients)
    delete_by_ids(Ingredients, [4])
    select_all(Ingredients)


def to_dict(table, result, tablekeys):
    tablename = table.__tablename__
    if not result:
        return None
    resultdict = {tablename: 1} 
    resultdict[tablename] = [1] * len(result)
    for i in range(len(result)):
        resultdict[tablename][i] = {}
        for key in range(len(result[i])):
            if tablekeys[key] != 'id':
                resultdict[tablename][i][tablekeys[key]] = result[i][key]
    return resultdict


#region Generic
def select_all(table):
    tablekeys = table.__table__.columns.keys()
    sel = select(table)
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        print(to_dict(table, result, tablekeys))


def select_by_ids(table, ids):
    tablekeys = table.__table__.columns.keys()
    sel = select(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        print(to_dict(table, result, tablekeys))


def insert_into(table, values):
    tablekeys = table.__table__.columns.keys()
    for i in range(len(values)):
        for key in values[i]:
            if key == 'id':
                return {'error': 1}
            if key != 'id' and key not in tablekeys:
                return {'error': 2}
    ins = insert(table)
    with engine.connect() as conn:
        result = conn.execute(ins, values) 


def update_by_ids(table, ids, values):
    if len(ids) != len(values):
        return {'error': 3}
    upd = update(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = conn.execute(upd, values) 


def delete_by_ids(table, ids):
    dlt = delete(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = conn.execute(dlt)
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

def insert_ingredients(ingredients):
    with engine.connect() as conn:
        for i in range(len(ingredients)):
            ins = insert(Ingredients).values(ingredient_name=ingredients[i])
            result = conn.execute(ins)
    print(result.inserted_primary_key_rows)
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
    ingredient = Column(Text)


class Measures(Model):
    __tablename__ = 'measures'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    unit = Column(Text)


class Recipes(Model):
    __tablename__ = 'recipes'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    recipe_name = Column(Text)
    

class Procedures(Model):
    __tablename__ = 'procedures'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    step = Column(Integer)


class RecipeIndex(Model):
    __tablename__ = 'recipe_index'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    quantity = Column(Text)
    measure_id = Column(Integer, ForeignKey('measures.id'))
#endregion


if __name__ == '__main__':
    test()
