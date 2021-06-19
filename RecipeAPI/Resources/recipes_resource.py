from flask import request
from flask_restful import Resource, reqparse
import jsons
from Dtos import RecipeDto, RecipesDto
import database_service.api_helper as helper


recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument('recipe_name', type=str, action='append')
recipe_parser.add_argument('recipe_desc', type=str, action='append')
recipe_parser.add_argument('ingredient', type=str, action='append')
recipe_parser.add_argument('recipe_cuisine', type=str, action='append')


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
        Recipe = jsons.load(request.get_json(force=True), RecipeDto, strict=True)
        if helper.AddOrUpdateRecipe(Recipe):
            return {"message": "created"}, 201
        else:
            return {"message": "conflict"}


class RecipeAPI(Resource):
    def get(self, id):
        args = idparser.parse_args()
        Recipe = helper.GetRecipeById(id)
        if Recipe is not None:
            return jsons.dump(Recipe, sort_keys=False)
        else:
            return {"message": "not found"}, 404
   
    def put(self, id):
        Recipe = jsons.load(request.get_json(force=True), cls=RecipeDto, strict=True)
        if helper.AddOrUpdateRecipe(Recipe, id):
            return {"message": "updated"}
        else:
            return {"message": "conflict"}, 409

    def delete(self, id):
        if helper.DeleteRecipe(id):
            return {"message": "deleted"}
        else:
            return {"message": "not allowed"}
