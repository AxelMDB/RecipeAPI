from flask import request
from flask_restful import Resource, reqparse
import jsons
from Dtos import CuisinesDto, CuisineDto
import database_service.api_helper as helper


cuisines_parser = reqparse.RequestParser()
cuisines_parser.add_argument('cuisine', type=str, action='append')
cuisines_parser.add_argument('description', type=str, action='append')


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
        """POST a collection of units or a single unit item"""
        #try loading the collection
        try:
            Cuisines = jsons.load(request.get_json(force=True), cls=CuisinesDto, strict=True)
            iscollection = True
        except:
            iscollection = False
        #if not a collection, load a single item, returns 404 as error
        if not iscollection:
            Cuisine = jsons.load(request.get_json(force=True), cls=CuisineDto, strict=True)
        if iscollection:
            if helper.AddCuisines(Cuisines):
                return {"message": "created"}, 201
            else:
                return {"message": "conflict"}, 409
        else:
            if helper.AddCuisine(Cuisine):
                return {"message": "created"}, 201
            else:
                return {"message": "conflict"}, 409


class CuisineAPI(Resource):
    def get(self, id):
        Cuisine = helper.GetCuisineById(id)
        if Cuisine is not None:
            return jsons.dump(Cuisine, sort_keys=False)
        else:
            return 404
        
    def put(self, id):
        Cuisine = jsons.load(request.get_json(force=True), cls=Dtos.CuisineDto, strict=True)
        if helper.UpdateCuisine(Cuisine, id):
            return {"message": "updated"}, 
        else:
            return {"message": "conflict"}, 409

    def delete(self):
        if helper.DeleteCuisine(id):
            return {"message": "deleted"}
        else:
            return {"message": "not allowed"}
