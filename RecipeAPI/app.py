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

UnitsParser = reqparse.RequestParser()
UnitsParser.add_argument('unit', type=str)
UnitsParser.add_argument('type', type=str)
UnitsParser.add_argument('number', type=str)


class UnitsAPI(Resource):
    """TODO"""
    def get(self):
        allargs = UnitsParser.parse_args()
        args = {}
        for key, value in allargs.items():
            if value is not None:
                args[key] = value
        AllUnits = helper.GetUnitsWithArguments(args)
        return jsons.dump(AllUnits)

    def post(self):
        try:
            Units = jsons.load(request.get_json(force=True), Dtos.UnitsDto)
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
            return jsons.dump(Unit)
        else:
            return "error"

    def post(self):
        try:
            Unit = jsons.load(request.get_json(force=True), Dtos.UnitDto)
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
            Unit = jsons.load(request.get_json(force=True), Dtos.UnitDto)
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

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
