"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, render_template, request, jsonify, Response
from flask_restful import Resource, Api
import jsons
from Dtos import *
from Mocks.mock_unit import MockUnit
import DatabaseService.api_helper as helper


app = Flask(__name__)
api = Api(app)
wsgi_app = app.wsgi_app


class UnitsAPI(Resource):
    """TODO"""
    def get(self):
        AllUnits = helper.GetAllUnits()
        return jsons.dump(AllUnits)

    def post(self):
        if request.is_json:
            try:
                Unit = jsons.load(request.get_json(), UnitDto)
            except Exception as e:
                print(e)
                return "error", 400
            if helper.AddUnit(Unit):
                return "success", 201
            else:
                return "error", 400
        return "error", 400

api.add_resource(UnitsAPI, "/Units")

class UnitByIdAPI(Resource):
    def get(self, unit_id):
        Unit = helper.GetUnitById(unit_id)
        if Unit is not None:
            return jsons.dump(Unit)
        else:
            return "error"

api.add_resource(UnitByIdAPI, "/Units/<int:unit_id>")


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
