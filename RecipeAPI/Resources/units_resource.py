from flask import request
from flask_restful import Resource, reqparse
import jsons
from Dtos import UnitDto, UnitsDto
import database_service.api_helper as helper


units_parser = reqparse.RequestParser()
units_parser.add_argument('unit', type=str, action='append')
units_parser.add_argument('type', type=str, action='append')
units_parser.add_argument('number', type=str, action='append')


class UnitsAPI(Resource):
    def get(self):
        """GET a collection of units"""
        allargs = units_parser.parse_args()
        args = {}
        for key, value in allargs.items():
            if value is not None:
                args[key] = value
        Units = helper.GetUnitsWithArguments(args)
        return jsons.dump(Units, sort_keys=False)

    def post(self):
        """POST a collection of units or a single unit item"""
        #try loading the collection
        try:
            Units = jsons.load(request.get_json(force=True), cls=UnitsDto, strict=True)
            iscollection = True
        except:
            iscollection = False
        #if not a collection load a single item, returns 404 as error
        if not iscollection:
            Unit = jsons.load(request.get_json(force=True), cls=UnitDto, strict=True)
        if iscollection:
            if helper.AddUnits(Units):
                return {"message": "created"}, 201
            else:
                return {"message": "conflict"}, 409
        else:
            if helper.AddUnit(Unit):
                return {"message": "created"}, 201
            else:
                return {"message": "conflict"}, 409


class UnitAPI(Resource):
    def get(self, id):
        """GET a single item by id"""
        Unit = helper.GetUnitById(id)
        if Unit is not None:
            return jsons.dump(Unit, sort_keys=False)
        else:
            return {"message": "not found"}, 404

    def put(self, id):
        """PUT(update) a single item by id"""
        Unit = jsons.load(request.get_json(force=True), cls=UnitDto, strict=True)
        if helper.UpdateUnit(Unit, id):
            return {"message": "updated"}
        else:
            return {"message": "conflict"}, 409

    def delete(self, id):
        """DELETE a single item by id"""
        if helper.DeleteUnit(id):
            return {"message": "deleted"}
        else:
            return {"message": "not allowed"}

