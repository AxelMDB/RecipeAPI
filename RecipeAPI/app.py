"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import jsons
import Dtos
import database_service.api_helper as helper


app = Flask(__name__)
api = Api(app)
wsgi_app = app.wsgi_app


idparser = reqparse.RequestParser()
idparser.add_argument('id', type=int, help="Please provide an id", required=True)

units_parser = reqparse.RequestParser()
units_parser.add_argument('unit', type=str)
units_parser.add_argument('type', type=str)
units_parser.add_argument('number', type=str)

ingredients_parser = reqparse.RequestParser()
ingredients_parser.add_argument('ingredient', type=str)
ingredients_parser.add_argument('description', type=str)

cuisines_parser = reqparse.RequestParser()
cuisines_parser.add_argument('cuisine', type=str)
cuisines_parser.add_argument('description', type=str)


#region Units
class UnitsAPI(Resource):
    def get(self):
        allargs = units_parser.parse_args()
        args = {}
        for key, value in allargs.items():
            if value is not None:
                args[key] = value
        Units = helper.GetUnitsWithArguments(args)
        return jsons.dump(Units, sorted=False)

    def post(self):
        try:
            Units = jsons.load(request.get_json(force=True), cls=Dtos.UnitsDto, strict=True)
        except Exception as e:
            print(e)
            return {"message": "invalid request"}, 400
        if helper.AddUnits(Units):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409

api.add_resource(UnitsAPI, "/api/units")

class UnitAPI(Resource):
    def get(self):
        args = idparser.parse_args()
        Unit = helper.GetUnitById(args['id'])
        if Unit is not None:
            return jsons.dump(Unit, sorted=False)
        else:
            return {"message": "not found"}, 204

    def post(self):
        try:
            Unit = jsons.load(request.get_json(force=True), cls=Dtos.UnitDto, strict=True)
        except Exception as e:
            print(e)
            return {"message": "invalid request"}, 400
        if helper.AddUnit(Unit):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409
        
    def put(self):
        args = idparser.parse_args()
        try:
            Unit = jsons.load(request.get_json(force=True), cls=Dtos.UnitDto, strict=True)
        except Exception as e:
            print(e)
            return {"message": "invalid request"}, 400
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
        return jsons.dump(Ingredients, sorted=False)

    def post(self):
        try:
            Ingredients = jsons.load(request.get_json(force=True), cls=Dtos.IngredientsDto, strict=True)
        except Exception as e:
            print(e)
            return {"message": "invalid request"}, 400
        if helper.AddIngredients(Ingredients):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409

api.add_resource(IngredientsAPI, "/api/ingredients")

class IngredientAPI(Resource):
    def get(self):
        args = idparser.parse_args()
        Ingredient = helper.GetIngredientById(args['id'])
        if Ingredient is not None:
            return jsons.dump(Ingredient, sorted=False)
        else:
            return 404

    def post(self):
        try:
            Ingredient = jsons.load(request.get_json(force=True), cls=Dtos.IngredientDto, strict=True)
        except Exception as e:
            print(e)
            return {"message": "invalid request"}, 400
        if helper.AddIngredient(Ingredient):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409
        
    def put(self):
        args = idparser.parse_args()
        try:
            Ingredient = jsons.load(request.get_json(force=True), cls=Dtos.IngredientDto, strict=True)
        except Exception as e:
            print(e)
            return {"message": "invalid request"}, 400
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
        return jsons.dump(Cuisines, sorted=False)

    def post(self):
        try:
            Cuisines = jsons.load(request.get_json(force=True), cls=Dtos.CuisinesDto, strict=True)
        except Exception as e:
            print(e)
            return {"message": "invalid request"}, 400
        if helper.AddCuisines(Cuisines):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409

api.add_resource(CuisinesAPI, "/api/cuisines")

class CuisineAPI(Resource):
    def get(self):
        args = idparser.parse_args()
        Cuisine = helper.GetCuisineById(args['id'])
        if Cuisine is not None:
            return jsons.dump(Cuisine, sorted=False)
        else:
            return 404

    def post(self):
        try:
            Cuisine = jsons.load(request.get_json(force=True), cls=Dtos.CuisineDto, strict=True)
        except Exception as e:
            print(e)
            return {"message": "invalid request"}, 400
        if helper.AddCuisine(Cuisine):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}, 409
        
    def put(self):
        args = idparser.parse_args()
        try:
            Cuisine = jsons.load(request.get_json(force=True), cls=Dtos.CuisineDto, strict=True)
        except Exception as e:
            print(e)
            return {"message": "invalid request"}, 400
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

api.add_resource(CuisineAPI, "/api/cuisine")
#endregion

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
