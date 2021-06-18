"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import jsons
import Dtos
import database_service.api_helper as helper
import Mocks.mock_recipe as mr


app = Flask(__name__)
api = Api(app)
wsgi_app = app.wsgi_app

#region parsers
idparser = reqparse.RequestParser()
idparser.add_argument('id', type=int, help="Please provide an id", required=True)

units_parser = reqparse.RequestParser()
units_parser.add_argument('unit', type=str, action='append')
units_parser.add_argument('type', type=str, action='append')
units_parser.add_argument('number', type=str, action='append')

ingredients_parser = reqparse.RequestParser()
ingredients_parser.add_argument('ingredient', type=str, action='append')
ingredients_parser.add_argument('description', type=str, action='append')

cuisines_parser = reqparse.RequestParser()
cuisines_parser.add_argument('cuisine', type=str, action='append')
cuisines_parser.add_argument('description', type=str, action='append')

recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument('recipe_name', type=str, action='append')
recipe_parser.add_argument('recipe_desc', type=str, action='append')
recipe_parser.add_argument('ingredient', type=str, action='append')
recipe_parser.add_argument('recipe_cuisine', type=str, action='append')
#endregion

#region Units
class UnitsAPI(Resource):
    def get(self):
        allargs = units_parser.parse_args()
        args = {}
        for key, value in allargs.items():
            if value is not None:
                args[key] = value
        Units = helper.GetUnitsWithArguments(args)
        return jsons.dump(Units, sort_keys=False)

    def post(self):
        Units = jsons.load(request.get_json(force=True), cls=Dtos.UnitsDto, strict=True)
        if helper.AddUnits(Units):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409

class UnitAPI(Resource):
    def get(self):
        args = idparser.parse_args()
        Unit = helper.GetUnitById(args['id'])
        if Unit is not None:
            return jsons.dump(Unit, sort_keys=False)
        else:
            return 404

    def post(self):
        Unit = jsons.load(request.get_json(force=True), cls=Dtos.UnitDto, strict=True)
        if helper.AddUnit(Unit):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409
        
    def put(self):
        args = idparser.parse_args()
        Unit = jsons.load(request.get_json(force=True), cls=Dtos.UnitDto, strict=True)
        if helper.UpdateUnit(Unit, args['id']):
            return {"message": "updated"}
        else:
            return {"message": "conflict"}, 409

    def delete(self):
        args = idparser.parse_args()
        if helper.DeleteUnit(args['id']):
            return {"message": "deleted"}
        else:
            return {"message": "not allowed"}

api.add_resource(UnitsAPI, "/api/units")

api.add_resource(UnitAPI, "/api/unit")
#endregion

#region Ingredients
class IngredientsAPI(Resource):
    def get(self):
        allargs = ingredients_parser.parse_args()
        args = {}
        for key, value in allargs.items():
            if value is not None:
                args[key] = value
        Ingredients = helper.GetIngredientsWithArguments(args)
        return jsons.dump(Ingredients, sort_keys=False)

    def post(self):
        Ingredients = jsons.load(request.get_json(force=True), cls=Dtos.IngredientsDto, strict=True)
        if helper.AddIngredients(Ingredients):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409

class IngredientAPI(Resource):
    def get(self):
        args = idparser.parse_args()
        Ingredient = helper.GetIngredientById(args['id'])
        if Ingredient is not None:
            return jsons.dump(Ingredient, sort_keys=False)
        else:
            return 404

    def post(self):
        Ingredient = jsons.load(request.get_json(force=True), cls=Dtos.IngredientDto, strict=True)
        if helper.AddIngredient(Ingredient):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409
        
    def put(self):
        args = idparser.parse_args()
        Ingredient = jsons.load(request.get_json(force=True), cls=Dtos.IngredientDto, strict=True)
        if helper.UpdateIngredient(Ingredient, args['id']):
            return {"message": "updated"}, 
        else:
            return {"message": "conflict"}, 409

    def delete(self):
        args = idparser.parse_args()
        if helper.DeleteIngredient(args['id']):
            return {"message": "deleted"}
        else:
            return {"message": "not allowed"}

api.add_resource(IngredientsAPI, "/api/ingredients")

api.add_resource(IngredientAPI, "/api/ingredient")
#endregion

#region Cuisines
class CuisinesAPI(Resource):
    def get(self):
        allargs = cuisines_parser.parse_args()
        args = {}
        for key, value in allargs.items():
            if value is not None:
                args[key] = value
        Cuisines = helper.GetCuisinesWithArguments(args)
        return jsons.dump(Cuisines, sort_keys=False)

    def post(self):
        Cuisines = jsons.load(request.get_json(force=True), cls=Dtos.CuisinesDto, strict=True)
        if helper.AddCuisines(Cuisines):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409

class CuisineAPI(Resource):
    def get(self):
        rgs = idparser.parse_args()
        Cuisine = helper.GetCuisineById(args['id'])
        if Cuisine is not None:
            return jsons.dump(Cuisine, sort_keys=False)
        else:
            return 404

    def post(self):
        Cuisine = jsons.load(request.get_json(force=True), cls=Dtos.CuisineDto, strict=True)
        if helper.AddCuisine(Cuisine):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409
        
    def put(self):
        args = idparser.parse_args()
        Cuisine = jsons.load(request.get_json(force=True), cls=Dtos.CuisineDto, strict=True)
        if helper.UpdateCuisine(Cuisine, args['id']):
            return {"message": "updated"}, 
        else:
            return {"message": "conflict"}, 409

    def delete(self):
        args = idparser.parse_args()
        if helper.DeleteCuisine(args['id']):
            return {"message": "deleted"}
        else:
            return {"message": "not allowed"}

api.add_resource(CuisinesAPI, "/api/cuisines")

api.add_resource(CuisineAPI, "/api/cuisine")
#endregion

#region Recipes
class RecipesAPI(Resource):
    def get(self):
        allargs = recipe_parser.parse_args()
        args = {}
        for key, value in allargs.items():
            if value is not None:
                args[key] = value
        Recipes = helper.GetRecipesWithArguments(args)
        return jsons.dump(Recipes, sort_keys=False)

    def post(self):
        Recipe = jsons.load(request.get_json(force=True), Dtos.RecipeDto, strict=True)
        if helper.AddOrUpdateRecipe(Recipe):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}

class RecipeAPI(Resource):
    def get(self):
        args = idparser.parse_args()
        Recipe = helper.GetRecipeById(args['id'])
        if Recipe is not None:
            return jsons.dump(Recipe, sort_keys=False)
        else:
            return 404
    
    def post(self):
        Recipe = jsons.load(request.get_json(force=True), cls=Dtos.RecipeDto, strict=True)
        if helper.AddOrUpdateRecipe(Recipe):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409

    def put(self):
        Recipe = jsons.load(request.get_json(force=True), cls=Dtos.RecipeDto, strict=True)
        args = idparser.parse_args()
        if helper.AddOrUpdateRecipe(Recipe, args['id']):
            return {"message": "updated"}
        else:
            return {"message": "conflict"}, 409

    def delete(self):
        args = idparser.parse_args()
        if helper.DeleteRecipe(args['id']):
            return {"message": "deleted"}
        else:
            return {"message": "not allowed"}

api.add_resource(RecipesAPI, "/api/recipes")

api.add_resource(RecipeAPI, "/api/recipe")
#endregion

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
