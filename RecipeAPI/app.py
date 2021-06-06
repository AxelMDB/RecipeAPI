"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, request
from flask_restful import Resource, Api
import jsons
import Dtos
import database_service.api_helper as helper


app = Flask(__name__)
api = Api(app)
wsgi_app = app.wsgi_app


class UnitsAPI(Resource):
    """TODO"""
    def get(self):
        AllUnits = helper.GetAllUnits()
        return jsons.dump(AllUnits)

    def post(self):
        if not request.is_json:
            return {"result": "invalid request"}, 400
        try:
            Units = jsons.load(request.get_json(), Dtos.UnitsDto)
        except Exception as e:
            print(e)
            return {"result": "invalid request"}, 400
        if helper.AddUnits(Units):
            return {"result": "created"}, 201
        else:
            return {"result": "conflict"}, 409


api.add_resource(UnitsAPI, "/api/units")


class UnitAPI(Resource):
    def get(self):
        unit_id = request.args.get('id')
        if not unit_id:
            return "error"
        Unit = helper.GetUnitById(unit_id)
        if Unit is not None:
            return jsons.dump(Unit)
        else:
            return "error"

    def post(self):
        if not request.is_json:
            return {"result": "invalid request"}, 400
        try:
            Unit = jsons.load(request.get_json(), Dtos.UnitDto)
        except Exception as e:
            print(e)
            return {"result": "invalid request"}, 400
        if helper.AddUnit(Unit):
            return {"result": "created"}, 201
        else:
            return {"result": "conflict"}, 409


api.add_resource(UnitAPI, "/api/unit")


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
