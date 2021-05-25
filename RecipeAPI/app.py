"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, render_template, request, jsonify, Response
from DatabaseService import DatabaseHelper as DH
import jsons
import requests
from Dtos import *
from Mocks.MockRecipes import MockRecipes

app = Flask(__name__)
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route("/")
def get():
    print(request.base_url)
    r = requests.post(request.base_url + "postrecipe", json=jsons.dump(MockRecipes()))
    return r.json()


@app.route("/postrecipe", methods = ["POST"])
def post():
    if request.is_json:
        recipes = jsons.load(request.json, Recipes)
        helper = DH.helper()
        insert_recipe_result = helper.insert_recipes(recipes)
        if insert_recipe_result:
            result = {'result': 'recipe(s) added successfully'}
            return jsonify(result), 201


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
