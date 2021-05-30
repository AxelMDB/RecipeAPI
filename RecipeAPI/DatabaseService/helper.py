from sqlalchemy import exc, create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseService.DeclarativeBase import Base
from Models import *
from Dtos import *
from Mocks.MockRecipe import MockRecipe


class SessionHelper:
    def __init__(self):
        self.db_name = "sqlite:///:memory:"
        self.engine = create_engine(self.db_name, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()


    def close_session(self):
        self.session.close()


    def AddOrUpdateAll(self, tables: list):
        for table in tables:
            self.session.add(table)
            try:
                self.session.commit()
            except exc.SQLAlchemyError as e:
                self.session.rollback()
                return False
        return True


    def GetAll(self, table):
        return self.session.query(table) 


    def get_ingredient_by_name(self, ingredient: str):
        string = "%" + ingredient + "%"
        return self.session.query(Ingredients).filter(Ingredients.ingredient.like(string)).first()


    def get_unit_by_name(self, unit: str):
        string = "%" + unit + "%"
        return self.session.query(Units).filter(Units.unit.like(string)).first()


    def get_culture_by_name(self, culture: str):
        string = "%" + culture + "%"
        return self.session.query(Cultures).filter(Cultures.culture.like(string)).first()


    def insert_recipe(self, recipe: Recipe):
        info = RecipeInfo()
        info.recipe_name = recipe.recipe_name.lower()
        info.recipe_desc = recipe.recipe_desc
        culture = self.get_culture_by_name(recipe.recipe_culture)
        if culture == None:
            return False
        info.recipe_cult = culture.culture
        if not self.AddOrUpdateAll([info]):
            return False
        AllQuantities = []
        for ingredient in ingredient_list:
            Quantity = Quantities()
            Quantity.quantity = ingredient.quantity
            unit = self.get_unit_by_name(ingredient.unit)
            if unit == None:
                return False
            Quantity.unit_id = unit.id
            Quantity.recipe_id = info.id
            ingredient = self.get_ingredient_by_name(ingredient.ingredient)
            if ingredient == None:
                return False
            Quantity.ingredient_id = ingredient_id
            AllQuantities.append(Quantity)
        AllProcedures = []
        for i in range(len(recipe.procedure)):
            Procedure = Procedures()
            Procedure.text = recipe.procedure[i].text
            Procedure.recipe_id = info.id
            Procedure.step = i + 1
            AllProcedures.append(Procedure)
        if self.AddOrUpdateAll(AllQuantities) and self.AddOrUpdateAll(AllProcedures):
            return True


    def get_recipes_by_names(self, names: list):
        Recipes = Recipes()
        recipes = self.session.query(RecipeInfo).filter(RecipeInfo.name.in_(names))
        for recipe in recipes:
            Recipe = Recipe()
            Recipe.recipe_name = recipe.recipe_name
            Recipe.recipe_desc = recipe.recipe_desc
            Recipe.recipe_culture = self.session.query(Cultures.culture).filter(Cultures.id == recipe.culture_id)
            result = self.session.query(
                Ingredients.ingredient, Units.unit, Procedures.text,
                Quantities.quantity, Quantities.recipe_id).\
                    filter(Quantities.recipe_id == recipe.id).\
                    filter(Ingredients.id == Quantities.ingredient_id).\
                    filter(Units.id == Quantities.unit_id).\
                    filter(Procedures.recipe_id == RecipeName.id).\
                    group_by(Quantities.id)
            for row in result:
                ingredient = RecipeIngredient()
                ingredient.ingredient += row.ingredient
                ingredient.quantity += row.quantity
                ingredient.unit += row.unit
                Recipe.ingredient_list.append(ingredient)
                procedure = RecipeProcedure()
                procedure.text += row.text
                Recipe.procedure_list.append(procedure)
            Recipes.recipes.append(Recipe)


if __name__ == "__main__":
    helper = SessionHelper()
    mockrecipe = MockRecipe()
    helper.insert_recipe(mockrecipe)