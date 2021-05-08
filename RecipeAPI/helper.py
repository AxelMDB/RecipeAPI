from sqlalchemy import Column, Integer, ForeignKey, Text, create_engine, insert, select, update, delete
from sqlalchemy.orm import declarative_base


Model = declarative_base()
db_name = "sqlite:///:memory:"
engine = create_engine(db_name, echo=True)

recipe_example = [
    {
        'recipe_name': 'arepa', 
        'ingredients': [
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
                'quantity': '1',
                'unit': 'teaspoon'
            },
        ],
        'procedure': [
            {
                'step': 1,
                'text': 'something'
            },
            {
                'step': 2,
                'text': 'something'
            },
            {
                'step': 3,
                'text': 'something'
            }
        ]
    } 
]


def dbtests():
    Model.metadata.create_all(engine)
    insert_jsonlike_recipe(recipe_example)
    select_all(Recipes)
    select_all(Ingredients)
    select_all(Procedures)


def to_list(table: Model, result: list, getid = False):
    '''take a sqlalchemy.result list and convert into a list of dictionaries'''
    # check if list is empty
    if not result:
        return None
    # get the column names (keys) from the table
    tablekeys = table.__table__.columns.keys()
    # initialize empty list to save the dict with length of result
    resultlist = [None] * len(result)
    # for each row in result
    for i in range(len(result)):
        # value of resultlist[i] is None, initialize to dict
        resultlist[i] = {}
        # for comma-separated value inside tuple result[i]
        for key in range(len(result[i])):
            # check if should return ids (default is false)
            if getid and tablekeys[key] == 'id':
                resultlist[i][tablekeys[key]] = result[i][key]
            elif tablekeys[key] != 'id':
                resultlist[i][tablekeys[key]] = result[i][key]
    return resultlist


#region Generic
def select_all(table, getid = False):
    '''select all registers in a table'''
    sel = select(table)
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = to_list(table, result, getid)
        print(resultlist)
    return resultlist


def select_by_ids(table: Model, ids: list, getid = False):
    '''select all registers in a table that matches a list of ids'''
    sel = select(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = to_list(table, result, getid)
        print(resultlist)
    return resultlist


def insert_into(table: Model, values: list):
    '''insert values into a table'''
    tablekeys = table.__table__.columns.keys()
    # check if values' keys are valid columns
    for i in range(len(values)):
        for key in values[i]:
            if key == 'id':
                return {'error': 1}
            if key != 'id' and key not in tablekeys:
                return {'error': 2}
    ins = insert(table)
    with engine.connect() as conn:
        result = conn.execute(ins, values)
        return result.inserted_primary_key_rows[0]


def update_by_ids(table: Model, ids: list, values: list):
    '''update registers in a table that match up with a list of ids with a list of values'''
    if len(ids) != len(values):
        return {'error': 3}
    upd = update(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = conn.execute(upd, values) 


def delete_by_ids(table: Model, ids: list):
    '''delete registers that match up with a list of ids'''
    dlt = delete(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = conn.execute(dlt)
#endregion


#region singular queries
def select_ingredients_by_names(ingredients: list, getid = False):
    '''select ingredients in the Ingredients table that match up with a list of ingredients'''
    table = Ingredients
    sel = select(table).where(table.ingredient.in_(ingredients))
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = to_list(table, result, getid)
        print(resultlist)
    return resultlist   
        

def select_recipes_by_names(recipes: list, getid = False):
    '''select recipes in the Recipes table that match up with a list of recipes'''
    table = Recipes
    sel = select(table).where(table.recipe_name.in_(recipes))
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = to_list(table, result, getid)
        print(resultlist)
    return resultlist     
#endregion


#region Recipe query
def insert_jsonlike_recipe(recipe):
    '''insert JSON-like objects of recipes with ingredients and procedures'''
    for r in range(len(recipe)):
        # get all the ingredients
        all_ingredients = select_all(Ingredients)
        # get the name of the current recipe
        recipe_name = recipe[r]['recipe_name']
        # insert into the Recipes table
        recipe_id = insert_into(Recipes, [{'recipe_name': recipe_name}])[0]
        # number of ingredients
        ing_length = len(recipe[r]['ingredients'])
        ings_to_insert = [None] * ing_length
        ing_list = []
        for i in range(ing_length):
            # get current ingredient
            ingredient = recipe[r]['ingredients'][i]['ingredient']
            ing_list.append(ingredient)
            ings_to_insert[i] = {}
            # check if there are ingredients in the table
            if all_ingredients != None:
                if not any(d['ingredient'] == ingredient for d in all_ingredients):
                    ings_to_insert[i]['ingredient'] = ingredient
            else:
                ings_to_insert[i]['ingredient'] = ingredient
        insert_into(Ingredients, ings_to_insert)
        # get the ids of the ingredients just inserted
        ing_ids = []
        for row in select_ingredients_by_names(ing_list, True):
            ing_ids.append(row['id'])
        # number of procedure steps
        proc_length = len(recipe[r]['procedure'])
        steps_to_insert = [None] * proc_length
        for p in range(proc_length):
            steps_to_insert[p] = {}
            step = recipe[r]['procedure'][p]
            steps_to_insert[p] = {'recipe_id' : recipe_id,'step': step['step'], 'text': step['text']}
        insert_into(Procedures, steps_to_insert)
#endregion


#region Models
class Ingredients(Model):
    __tablename__ = 'ingredients'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient = Column(Text)


class Measures(Model):
    __tablename__ = 'measures'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    unit = Column(Text)


class Recipes(Model):
    __tablename__ = 'recipes'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_name = Column(Text)
    

class Procedures(Model):
    __tablename__ = 'procedures'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    step = Column(Integer)
    text = Column(Text)


class RecipeIndex(Model):
    __tablename__ = 'recipe_index'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True,autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    quantity = Column(Text)
    measure_id = Column(Integer, ForeignKey('measures.id'))
#endregion


if __name__ == '__main__':
    dbtests()
