from flask import request
from flask_restful import Resource, reqparse
import werkzeug.exceptions as w_exc
import jsons
from Dtos import CuisinesDto, CuisineDto
import database_service.api_helper as helper


cuisines_parser = reqparse.RequestParser()
cuisines_parser.add_argument('cuisine', type=str, action='append')


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
            try:
                Cuisine = jsons.load(request.get_json(force=True), cls=CuisineDto, strict=True)
            except:
                raise w_exc.BadRequest()
        if iscollection:
            helper.AddCuisines(Cuisines)
            return {"message": "created"}, 201
        else:
            helper.AddCuisine(Cuisine)
            return {"message": "created"}, 201


class CuisineAPI(Resource):
    def get(self, id):
        Cuisine = helper.GetCuisineById(id)
        return jsons.dump(Cuisine, sort_keys=False)
        
    def put(self, id):
        try:
            Cuisine = jsons.load(request.get_json(force=True), cls=Dtos.CuisineDto, strict=True)
        except:
            raise w_exc.BadRequest()
        helper.UpdateCuisine(Cuisine, id)
        return {"message": "updated"}

    def delete(self):
        helper.DeleteCuisine(id)
        return {"message": "deleted"}

