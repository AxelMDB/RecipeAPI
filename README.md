# RecipeAPI

This is a final project for CS50. It consists of a web API programmed in python using flask, the extension flask-restful, jsons and SQLAlchemy. It's meant for storing, manipulating and retrieving culinary recipes as well as the units, ingredients, and cuisines.

The reason for using SQLAlchemy was due to its Object Relational Mapping feature, which allows retrieving objects instead of dictionaries, and executing sql with pythonic statements instead of a raw string.

The mappings were declared in the RecipeAPI/Models folder so that they could be imported as an user-defined package. Some of the tables required using the sqlalchemy.orm relationship to create one to many or one to one relationships.

With flask-restful, I could create each endpoint as a separate class, which meant each resource could be a module inside a package, which then could be imported. The files for those classes are in RecipeAPI/Resources.

The resources then call functions in RecipeAPI/database_service/api_helper.py, which then calls sql_commands to execute certain functions.
 
Since the creator wanted the JSON response to be different than the models, it was decided to define objects in RecipeAPI/Dtos, which would then *recursively* be converted to JSON with the jsons package, not the built-in json package. And the submitted jsons are expected to match the dto object so it can be properly loaded.

the main endpoints are:

* <b>/api/units</b>: all the units, GET supports optional parameters: *unit*, *type*, *number*
* <b>/api/ingredients</b>: all the ingredients, GET supports optional parameter *ingredient*
* <b>/api/cuisines</b>: all the cuisines, GET supports optional parameter *cuisine*
* <b>/api/recipes</b>: all the recipes, GET supports optional parameters: *recipe_name*, *ingredient*, *recipe_cuisine*
* <b>/api/SI_Units</b>: a few units in the International System of Units

all of them support HTTP GET, POST, UPDATE, and DELETE (the last two with /id), except <b>/api/SI_Units</b>, which only supports GET
