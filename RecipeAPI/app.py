"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask
from flask_restful import Api
import database_service.api_helper as helper
import Resources


app = Flask(__name__)
api = Api(app)
wsgi_app = app.wsgi_app


api.add_resource(Resources.UnitsAPI, "/api/units")
api.add_resource(Resources.UnitAPI, "/api/units/<int:id>")
api.add_resource(Resources.IngredientsAPI, "/api/ingredients")
api.add_resource(Resources.IngredientAPI, "/api/ingredients/<int:id>")
api.add_resource(Resources.CuisinesAPI, "/api/cuisines")
api.add_resource(Resources.CuisineAPI, "/api/cuisines/<int:id>")
api.add_resource(Resources.RecipesAPI, "/api/recipes")
api.add_resource(Resources.RecipeAPI, "/api/recipes/<int:id>")


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
