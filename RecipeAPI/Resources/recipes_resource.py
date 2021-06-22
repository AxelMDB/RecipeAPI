from flask import request
from flask_restful import Resource, reqparse
import werkzeug.exceptions as w_exc
import jsons
from Dtos import RecipeDto, RecipesDto
import database_service.api_helper as helper


recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument('recipe_name', type=str, action='append')
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
        try:
            Recipe = jsons.load(request.get_json(force=True), RecipeDto, strict=True)
        except:
            raise w_exc.BadRequest()
        helper.AddOrUpdateRecipe(Recipe)
        return {"message": "created"}, 201


class RecipeAPI(Resource):
    def get(self, id):
        Recipe = helper.GetRecipeById(id)
        return jsons.dump(Recipe, sort_keys=False)
   
    def put(self, id):
        try:
            Recipe = jsons.load(request.get_json(force=True), cls=RecipeDto, strict=True)
        except:
            raise w_exc.BadRequest()
        helper.AddOrUpdateRecipe(Recipe, id)
        return {"message": "updated"}

    def delete(self, id):
        helper.DeleteRecipe(id)
        return {"message": "deleted"}

