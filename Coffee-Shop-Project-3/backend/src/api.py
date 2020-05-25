import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks",methods=["GET"])
def getDrinks():
    all_drinks = Drink.query.all()
    return jsonify({
        "success" : True,
        "drinks" : [drink.short() for drink in all_drinks]
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail" , methods=["GET"])
def getDrinksDetails():
    all_drinks = Drink.query.all()
    return jsonify({
        "success" : True,
        "drinks" : [drink.long() for drink in all_drinks]
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks",methods=["POST"])
def postDrinks():
    try:
        data_json = request.get_json()

        if not ("title" in data_json and "recipe" in data_json):
            abort(400)

        new_title = data_json["title"]
        new_recipe = data_json["recipe"]

        new_drink = Drink(title = new_title, recipe = json.dumps(new_recipe) )
        new_drink.insert()

        return jsonify({"success": True, "drinks": [new_drink.long()] } )

    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:id>",methods=["PATCH"])
def editDrink(id):
    try:
        edited_drink = Drink.query.get(id)
        if not edited_drink:
            abort(404)
        
        data_json = request.get_json()
        if "title" in data_json:
            edited_drink.title = data_json["title"]
        if "recipe" in data_json:
            edited_drink.recipe = data_json["recipe"]

        edited_drink.update()

        return jsonify ({
            "success" : True,
            "drinks" : [edited_drink.long()]
        })


    except :
        abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int::id>",methods=["DELETE"])
def deleteDrink(id):
    try:
        deleted_drink = Drink.query.get(id)
        if not deleteDrink:
            abort(404)

        deleted_drink.delete()

        return jsonify ({"success": True, "delete": id})
    except:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
      "success" : False,
      "error" : 400,
      "message" : "Error Bad Request, you may forgot to send the json"
    }) , 400
    
@app.errorhandler(404)
def not_found(error):
    return jsonify({
      "success" : False,
      "error" : 404,
      "message" : "Error Not Found"
    }) , 404

@app.errorhandler(AuthError)
def handle_auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        'message': error.error
    }), 401