from sqlalchemy import exc, create_engine
from sqlalchemy.orm import sessionmaker
from .DeclarativeBase import Base
from Models import *
from Dtos import *


class helper:
    def __init__(self):
        self.db_name = "sqlite:///:memory:"
        self.engine = create_engine(self.db_name, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


    def dbtests(self):
        AllRecipes = self.MockRecipes()
        self.insert_recipes(AllRecipes)
        return self.get_recipes_by_names(["arepa", "hello"])


    def AddOrUpdateAll(self, tables: list):
        for table in tables:
            self.session.add(table)
            try:
                self.session.commit()
            except exc.SQLAlchemyError as e:
                self.session.rollback()


    def Get(self, table):
        return self.session.query(table) 


    def get_ingredients_by_names(self, names: list):
        return self.session.query(Ingredients).filter(Ingredients.ingredient.in_(names))


    def insert_recipes(self, recipes: Recipes):
        recipes = recipes.recipes
        for recipe in recipes:
            name = RecipeName()
            name.name = recipe.name.lower()
            self.AddOrUpdateAll([name])
            AllIngredients = []
            AllUnits = []
            AllQuantities = []
            AllProcedures = []
            for ing in recipe.ingredients:
                Ingredient = Ingredients()
                Ingredient.ingredient = ing.ingredient.lower()
                AllIngredients.append(Ingredient)
                AllQuantities.append(ing.quantity)
                Unit = Units()
                Unit.unit = ing.unit.lower()
                AllUnits.append(Unit)
            for i in range(len(recipe.procedure)):
                Procedure = Procedures()
                Procedure.text = recipe.procedure[i].text
                Procedure.recipe_id = name.id
                Procedure.step = i + 1
                AllProcedures.append(Procedure)
            self.AddOrUpdateAll(AllIngredients)
            self.AddOrUpdateAll(AllUnits)
            self.AddOrUpdateAll(AllProcedures)
            quantities = []
            for i in range(len(AllIngredients)):
                Quantity = Quantities()
                if AllIngredients[i].id == None and i != 0:
                   AllIngredients[i] = AllIngredients[i - 1]
                Quantity.ingredient_id = AllIngredients[i].id
                Quantity.quantity = AllQuantities[i]
                Quantity.recipe_id = name.id
                if AllUnits[i].id == None and i != 0:
                    AllUnits[i] = AllUnits[i - 1]
                Quantity.unit_id = AllUnits[i].id
                quantities.append(Quantity)
            self.AddOrUpdateAll(quantities)
            return True

    def get_recipes_by_names(self, names: list):
        RecipesObj = Recipes()
        recipenames = self.session.query(RecipeName).filter(RecipeName.name.in_(names))
        for recipe in recipenames:
            RecipeObj = Recipe()
            RecipeObj.name = recipe.name
            result = self.session.query(
                Ingredients.ingredient, Units.unit, Procedures.text,
                Quantities.quantity, Quantities.recipe_id).\
                    filter(Quantities.recipe_id == recipe.id).\
                    filter(Ingredients.id == Quantities.ingredient_id).\
                    filter(Units.id == Quantities.unit_id).\
                    filter(Procedures.recipe_id == RecipeName.id).\
                    group_by(Quantities.id)
            print(result.count())
            for row in result:
                ing = Ingredient()
                ing.ingredient += row.ingredient
                ing.quantity += row.quantity
                ing.unit += row.unit
                RecipeObj.ingredients.append(ing)
                print(len(RecipeObj.ingredients))
                proc = Procedure()
                proc.text += row.text
                RecipeObj.procedure.append(proc)
                print(len(RecipeObj.procedure))
            RecipesObj.recipes.append(RecipeObj)
        return self.serialize_recipes(RecipesObj)



if __name__ == '__main__':
    DH = helper()
    print(DH.dbtests())
