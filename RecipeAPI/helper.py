from sqlalchemy import Column, Integer, ForeignKey, Text, create_engine, insert, select, update, delete
from sqlalchemy.orm import declarative_base


Model = declarative_base()
db_name = "sqlite:///:memory:"
engine = create_engine(db_name, echo=True)

recipe_example = [
    {
        'name': 'arepa', 
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
                'text': 'something'
            },
            {
                'text': 'something'
            },
            {
                'text': 'something'
            }
        ]
    } 
]


def dbtests():
    Model.metadata.create_all(engine)
    insert_jsonlike_recipes(recipe_example)
    select_all(RecipeNames)
    select_all(Ingredients)
    select_all(Procedures)
    select_all(Units)
    select_all(Quantities)


def result_to_list(table: Model, result, getid = False):
    '''take a sqlalchemy.result and convert into a list of dictionaries'''
    # check if list is empty
    result = list(result)
    if not result:
        return None
    # get the column names (keys) from the table
    tablekeys = table.__table__.columns.keys()
    # initialize empty list to save the dict with length of result
    l = []
    # for each row in result
    for i in range(len(result)):
        d = {}
        # for comma-separated value inside tuple result[i]
        for key in range(len(result[i])):
            # check if should return ids (default is false)
            if getid and tablekeys[key] == 'id':
                d[tablekeys[key]] = result[i][key]
            elif tablekeys[key] != 'id':
                d[tablekeys[key]] = result[i][key]
        l.append(d)
    return l


#region Generic
def select_all(table, getid = False):
    '''select all registers in a table'''
    sel = select(table)
    with engine.connect() as conn:
        result = conn.execute(sel)
        resultlist = result_to_list(table, result, getid)
        print(resultlist)
    return resultlist


def select_by_ids(table: Model, ids: list, getid = False):
    '''select all registers in a table that matches a list of ids'''
    sel = select(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = conn.execute(sel)
        resultlist = result_to_list(table, result, getid)
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
        resultlist = result_to_list(table, result, getid)
        print(resultlist)
    return resultlist   
        

def select_recipes_by_names(recipes: list, getid = False):
    '''select recipes in the Recipes table that match up with a list of recipes'''
    table = RecipeNames
    sel = select(table).where(table.name.in_(recipes))
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = result_to_list(table, result, getid)
        print(resultlist)
    return resultlist


def select_units_by_names(units: list, getid = False):
    '''select recipes in the Recipes table that match up with a list of recipes'''
    table = Units
    sel = select(table).where(table.unit.in_(units))
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = result_to_list(table, result, getid)
        print(resultlist)
    return resultlist     
#endregion


#region Recipe queries
def insert_jsonlike_recipes(recipes):
    '''insert JSON-like objects of recipes with ingredients and procedures'''
    for r in range(len(recipes)):
        # RECIPE NAME
        # get the name of the current recipe
        recipe_name = recipes[r]['name']
        all_recipes = select_all(RecipeNames)
        # insert into the Recipes table if not in the database, return error otherwise
        if all_recipes != None:
            if not any(d['name'] == recipe_name for d in all_recipes):
                recipe_id = insert_into(RecipeNames, [{'name': recipe_name}])[0]
            else:
                return {'error': 'some recipe with that name already exists in the database'}
        else:
            recipe_id = insert_into(RecipeNames, [{'name': recipe_name}])[0]
        # INGREDIENTS
        # get all the ingredients
        all_ingredients = select_all(Ingredients)
        # number of ingredients
        ings_length = len(recipes[r]['ingredients'])
        ings_to_insert = []
        ing_list = []
        for i in range(ings_length):
            # get current ingredient
            ing = recipes[r]['ingredients'][i]['ingredient']
            if ing not in ing_list:
                ing_list.append(ing)
            # check if ingredient in the database
        for ingredient in ing_list:
            ing_dict = None
            if all_ingredients != None:
                if not any(d['ingredient'] == ingredient for d in all_ingredients):
                    ing_dict = {'ingredient': ingredient}
            else:
                ing_dict = {'ingredient': ingredient}
            if ing_dict != None:
                ings_to_insert.append(ing_dict)
        insert_into(Ingredients, ings_to_insert)
        # UNITS
        units_to_insert = []
        # get all units
        all_units = select_all(Units)
        unit_list = []
        for i in range(ings_length):
            unit = recipes[r]['ingredients'][i]['unit']
            if unit not in unit_list:
                unit_list.append(unit)
        for u in unit_list:
            unit_dict = None
            if all_units != None:
                if not any(d['unit'] == u for d in all_units):
                    unit_dict = {'unit': u}
            else:
                unit_dict = {'unit': u}
            if unit_dict != None:
                units_to_insert.append(unit_dict)
        insert_into(Units, units_to_insert)
        # QUANTITIES
        quantities_to_insert = []
        for i in range(ings_length):
            ing = recipes[r]['ingredients'][i]['ingredient']
            ing_id = select_ingredients_by_names([ing], True)[0]['id']
            quantity = recipes[r]['ingredients'][i]['quantity']
            unit = recipes[r]['ingredients'][i]['unit']
            unit_id = select_units_by_names([unit], True)[0]['id']
            quant_dict = {
                'quantity': quantity,
                'unit_id': unit_id,
                'recipe_id': recipe_id,
                'ingredient_id': ing_id
            }
            quantities_to_insert.append(quant_dict)
        insert_into(Quantities, quantities_to_insert)
        # STEPS
        # number of procedure steps
        proc_length = len(recipes[r]['procedure'])
        steps_to_insert = []
        for p in range(proc_length):
            step = recipes[r]['procedure'][p]
            step_dict = {'recipe_id' : recipe_id,'step': p + 1, 'text': step['text']}
            steps_to_insert.append(step_dict)
        insert_into(Procedures, steps_to_insert)
#endregion


#region Models
class Ingredients(Model):
    __tablename__ = 'ingredients'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient = Column(Text, unique=True)


class Units(Model):
    __tablename__ = 'units'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    unit = Column(Text, unique=True)


class RecipeNames(Model):
    __tablename__ = 'recipe_names'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, unique=True)
    

class Procedures(Model):
    __tablename__ = 'procedures'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipe_names.id'))
    step = Column(Integer)
    text = Column(Text)


class Quantities(Model):
    __tablename__ = 'quantities'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True,autoincrement=True)
    quantity = Column(Text)
    unit_id = Column(Integer, ForeignKey('units.id'))
    recipe_id = Column(Integer, ForeignKey('recipe_names.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
#endregion


if __name__ == '__main__':
    dbtests()
