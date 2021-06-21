from flask import request
from flask_restful import Resource, reqparse
import werkzeug.exceptions as w_exc
import jsons
from Dtos import IngredientsDto, IngredientDto
import database_service.api_helper as helper

ingredients_parser = reqparse.RequestParser()
ingredients_parser.add_argument('ingredient', type=str, action='append')
ingredients_parser.add_argument('description', type=str, action='append')


class IngredientsAPI(Resource):
    def get(self):
        """GET a collection of ingredients"""
        allargs = ingredients_parser.parse_args()
        args = {}
        for key, value in allargs.items():
            if value is not None:
                args[key] = value
        Ingredients = helper.GetIngredientsWithArguments(args)
        return jsons.dump(Ingredients, sort_keys=False)

    def post(self):
        """POST a collection of ingredients or a single ingredient item"""
        #try loading the collection
        try:
            Ingredients = jsons.load(request.get_json(), cls=IngredientsDto, strict=True)
            iscollection = True
        except:
            iscollection = False
        #if not a collection load a single item, returns 404 when error
        if not iscollection:
            try:
                Ingredient = jsons.load(request.get_json(), cls=IngredientDto, strict=True)
            except:
                raise w_exc.BadRequest()
        if iscollection:
            helper.AddIngredients(Ingredients)
            return {"message": "created"}, 201
        else:
            helper.AddIngredient(Ingredient)
            return {"message": "created"}, 201


class IngredientAPI(Resource):
    def get(self, id):
        """GET a single item by id"""
        Ingredient = helper.GetIngredientById(id)
        return jsons.dump(Ingredient, sort_keys=False)
        
    def put(self, id):
        """PUT(update) a single item by id"""
        try:
            Ingredient = jsons.load(request.get_json(), cls=IngredientDto, strict=True)
        except:
            raise w_exc.BadRequest()
        helper.UpdateIngredient(Ingredient, id)
        return {"message": "updated"}, 

    def delete(self, id):
        """DELETE a single item by id"""
        helper.DeleteIngredient(id)
        return {"message": "deleted"}


