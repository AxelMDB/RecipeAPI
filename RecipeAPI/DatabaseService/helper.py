from sqlalchemy import exc, create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseService.DeclarativeBase import Base
from Models import *
from Dtos import *
from Mocks.MockRecipe import MockRecipe


class SessionHelper:
    def start_session(self):
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
        self.start_session()
        info = RecipeInfoModel()
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
            Quantity = QuantitiesModel()
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
            Procedure = ProceduresModel()
            Procedure.text = recipe.procedure[i].text
            Procedure.recipe_id = info.id
            Procedure.step = i + 1
            AllProcedures.append(Procedure)
        if self.AddOrUpdateAll(AllQuantities) and self.AddOrUpdateAll(AllProcedures):
            self.session_close()
            return True


    def get_recipes_by_names(self, names: list):
        self.start_session()
        Recipes = RecipesDto()
        recipes = self.session.query(RecipeInfoModel).filter(RecipeInfoModel.name.in_(names))
        for recipe in recipes:
            Recipe = RecipeDto()
            Recipe.recipe_name = recipe.recipe_name
            Recipe.recipe_desc = recipe.recipe_desc
            Recipe.recipe_culture = self.session.query(CulturesModel.culture).filter(CulturesModel.id == recipe.culture_id)
            result = self.session.query(
                IngredientsModel.ingredient, UnitsModel.unit, ProceduresModel.text,
                QuantitiesModel.quantity, QuantitiesModel.recipe_id).\
                    filter(QuantitiesModel.recipe_id == recipe.id).\
                    filter(IngredientsModel.id == QuantitiesModel.ingredient_id).\
                    filter(UnitsModel.id == QuantitiesModel.unit_id).\
                    filter(ProceduresModel.recipe_id == RecipeName.id).\
                    group_by(QuantitiesModel.id)
            for row in result:
                ingredient = RecipeIngredientDto()
                ingredient.ingredient += row.ingredient
                ingredient.quantity += row.quantity
                ingredient.unit += row.unit
                Recipe.ingredient_list.append(ingredient)
                procedure = RecipeProcedureDto()
                procedure.text += row.text
                Recipe.procedure_list.append(procedure)
            Recipes.recipes.append(Recipe)
        self.close_session()
        return Recipes

if __name__ == "__main__":
    mockrecipe = MockRecipe()
    helper.insert_recipe(mockrecipe)