from flask import request
from flask_restful import Resource, reqparse
import werkzeug.exceptions as w_exc
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
            Units = jsons.load(request.get_json(), cls=UnitsDto, strict=True)
            iscollection = True
        except:
            iscollection = False
        #if not a collection load a single item, returns 404 as error
        if not iscollection:
            try:
                Unit = jsons.load(request.get_json(), cls=UnitDto, strict=True)
            except:
                raise w_exc.BadRequest()
        if iscollection:
            helper.AddUnits(Units)
            return {"message": "created"}, 201
        else:
            helper.AddUnit(Unit)
            return {"message": "created"}, 201


class UnitAPI(Resource):
    def get(self, id):
        """GET a single item by id"""
        Unit = helper.GetUnitById(id)
        return jsons.dump(Unit, sort_keys=False)

    def put(self, id):
        """PUT(update) a single item by id"""
        Unit = jsons.load(request.get_json(), cls=UnitDto, strict=True)
        helper.UpdateUnit(Unit, id)
        return {"message": "updated"}

    def delete(self, id):
        """DELETE a single item by id"""
        helper.DeleteUnit(id)
        return {"message": "deleted"}

