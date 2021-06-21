from flask import jsonify
from flask_restful import Resource

class SIUnitsAPI(Resource):
    def get(self):
        SIUnits = {}
        SIUnits["mass"] = "kilogram"
        SIUnits["volume"] = "cubic meter"
        SIUnits["temperature"] = "kelvin"
        return jsonify(SIUnits)
