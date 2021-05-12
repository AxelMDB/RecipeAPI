from sqlalchemy import Column, Integer, ForeignKey, Text, create_engine, insert, select, update, delete, exc
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
    select_all(Ingredients)
    select_all(Units)
    select_all(RecipeNames)
    select_all(Procedures)
    select_all(Quantities)


def result_to_list(table: Model, result):
    '''take a sqlalchemy.result and convert into a list of dictionaries'''
    # check if list is empty
    result = list(result)
    if not result:
        return []
    # get the column names (keys) from the table
    tablekeys = table.__table__.columns.keys()
    # initialize empty list to save the dict with length of result
    l = []
    # for each row in result
    for i in range(len(result)):
        d = {}
        # for comma-separated value inside tuple result[i]
        for key in range(len(result[i])):
            d[tablekeys[key]] = result[i][key]
        l.append(d)
    return l


def select_all(table):
    '''select all registers in a table'''
    sel = select(table)
    with engine.connect() as conn:
        result = conn.execute(sel)
        resultlist = result_to_list(table, result)
        print(resultlist)
    return resultlist


def select_by_ids(table: Model, ids: list):
    '''select all registers in a table that matches a list of ids'''
    sel = select(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = conn.execute(sel)
        resultlist = result_to_list(table, result)
        print(resultlist)
    return resultlist


def insert_into(table: Model, values: list):
    '''insert values into a table'''
    tablekeys = table.__table__.columns.keys()
    # check if values' keys are valid columns
    for i in range(len(values)):
        for key in values[i]:
            if key == 'id':
                return None
            if key != 'id' and key not in tablekeys:
                return None
    ins = insert(table)
    rows = {'ids': []}
    for dict in values:
        try:
            with engine.connect() as conn:
                result = conn.execute(ins, [dict])
                rows['ids'].append(result.inserted_primary_key[0])
        except exc.SQLAlchemyError:
            rows['ids'].append(None)
    return rows


def update_by_ids(table: Model, ids: list, values: list):
    '''update registers in a table that match up with a list of ids with a list of values'''
    if len(ids) != len(values):
        return None
    upd = update(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = conn.execute(upd, values) 


def delete_by_ids(table: Model, ids: list):
    '''delete registers that match up with a list of ids'''
    dlt = delete(table).where(table.id.in_(ids))
    with engine.connect() as conn:
        result = conn.execute(dlt)


def select_ingredients_by_names(ingredients: list):
    '''select ingredients in the Ingredients table that match up with a list of ingredients'''
    table = Ingredients
    sel = select(table).where(table.ingredient.in_(ingredients))
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = result_to_list(table, result)
        print(resultlist)
    return resultlist   
        

def select_recipes_by_names(recipes: list):
    '''select recipes in the Recipes table that match up with a list of recipes'''
    table = RecipeNames
    sel = select(table).where(table.name.in_(recipes))
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = result_to_list(table, result)
        print(resultlist)
    return resultlist


def select_units_by_names(units: list):
    '''select recipes in the Recipes table that match up with a list of recipes'''
    table = Units
    sel = select(table).where(table.unit.in_(units))
    with engine.connect() as conn:
        result = list(conn.execute(sel))
        resultlist = result_to_list(table, result)
        print(resultlist)
    return resultlist     


def insert_jsonlike_recipes(recipes):
    '''insert JSON-like objects of recipes with ingredients and procedures'''
    for r in range(len(recipes)):
        name = recipes[r]['name'].lower()
        recipe_id = insert_into(RecipeNames, [{'name': name}])['ids'][0]
        if not recipe_id:
            return None
        ings = recipes[r]['ingredients']
        ingredients = []
        ingredient_names = []
        units = []
        unit_names = []
        quant = [] 
        for dict in ings:
            for key, value in dict.items():
                if key == 'ingredient':
                    ingredients.append({key: value.lower()})
                    ingredient_names.append(value.lower())
                if key == 'unit':
                    units.append({key: value.lower()})
                    unit_names.append(value.lower())
                if key == 'quantity':
                    quant.append(value)
        ingredient_ids = insert_into(Ingredients, ingredients)['ids']
        unit_ids = insert_into(Units, units)['ids']
        #for row in select_ingredients_by_names(ingredient_names):
        #    ingredient_ids.append(row['id'])
        #for row in select_units_by_names(unit_names):
        #    unit_ids.append(row['id'])
        quantity_insert = []
        for i in range(len(quant)):
            dict = {}
            dict['quantity'] = quant[i]
            if unit_ids[i] != None:
                dict['unit_id'] = unit_ids[i]
            else:
                dict['unit_id'] = select_units_by_names([unit_names[i]])[0]['id']
            dict['recipe_id'] = recipe_id
            if ingredient_ids[i] != None:
                dict['ingredient_id'] = ingredient_ids[i]
            else:
                dict['ingredient_id'] = select_ingredients_by_names([ingredient_names[i]])[0]['id']
            quantity_insert.append(dict)
        insert_into(Quantities, quantity_insert)
        # STEPS
        # number of procedure steps
        proc_length = len(recipes[r]['procedure'])
        steps_to_insert = []
        for p in range(proc_length):
            step = recipes[r]['procedure'][p]
            step_dict = {'recipe_id' : recipe_id,'step': p + 1, 'text': step['text']}
            steps_to_insert.append(step_dict)
        insert_into(Procedures, steps_to_insert)

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
