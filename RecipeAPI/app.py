"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, render_template, request, jsonify, Response
from DatabaseService.helper import SessionHelper
import jsons
import requests
from Dtos import *


app = Flask(__name__)
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route("/")
def get():
    return "Hello"


@app.route("/postrecipe", methods = ["POST"])
def post():
    if request.is_json:
        try:
            recipe = jsons.load(request.json, Recipe)
        except:
            result = {'result': 'bad request'}
            return jsonify(result), 400
        insert_recipe_result = helper.insert_recipe(recipe)
        if insert_recipe_result:
            result = {'result': 'recipe added successfully'}
            return jsonify(result), 201
        else:
            result = {'result': 'error adding recipe'}
            return jsonify(result), 400


if __name__ == '__main__':
    app.run()
