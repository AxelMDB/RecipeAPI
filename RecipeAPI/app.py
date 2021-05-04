"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


con = sqlite3.connect('recipes.db')
cur = con.cursor()


@app.route("/api/SearchByIngredients")
def get():
    ingredient_list = request.args.getlist("ing")
    if not ingredient_list:
        return "invalid request"
    con = sqlite3.connect('recipes.db')
    cur = con.cursor()
    list = cur.execute("SELECT * FROM ingredients").fetchall()
    return jsonify(list)
    

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
