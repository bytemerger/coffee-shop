from logging import exception
import os
from pkg_resources import require
from sqlalchemy.exc import IntegrityError
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES
@app.route('/drinks')
def get_drinks(payload=''):
    drinks = Drink.query.all()
    format_drinks = [x.short() for x in drinks]
    return jsonify({
        'success': True,
        'drinks':format_drinks
    })

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    drinks = Drink.query.all()
    format_drinks = [x.long() for x in drinks]
    return jsonify({
        'success': True,
        'drinks':format_drinks
    })


@app.route('/drinks', methods=["POST"])
@requires_auth('post:drinks')
def post_drink(payload):
    new_drink = request.get_json()
    title = new_drink.get('title', None)
    recipeJson = new_drink.get('recipe', None)
    recipe = json.dumps(recipeJson) if recipeJson else abort(400, 'The recipe param is required')
    if not title:
        abort(400, 'The title param is required')
    
    drink = Drink(title=title, recipe=recipe)
    
    try:
        drink.insert()
        return jsonify({
            'success': 'true',
            'drinks': [drink.long()]
        })
    except IntegrityError:
        abort(400, 'The title already exist')
    except Exception:
        abort(500)

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload, id):
    body = request.get_json()
    title = body.get('title', None) or abort(400, 'The title parameter does exist')
    drink = Drink.query.get(id)
    if not drink:
        abort(404, f'The drink with the ID {id} does not exist')
    try:
        drink.title = title
        drink.update()
        return jsonify({
            'sucess': True,
            'drinks': [drink.long()]
        })
    except Exception:
        abort(500)

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404, f'The drink with the ID {id} does not exist')
    try:
        drink.delete()
        return jsonify({
            'sucess': True,
            'delete': id
        })
    except Exception:
        abort(500)

# Error Handling
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

@app.errorhandler(404)
def ressource_not_found(error):
    return jsonify({
        "success": False, 
        "status": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def ressource_not_found(error):
    return jsonify({
        "success": False, 
        "status": 400,
        "message": error.description or 'Bad Request'
    }), 400

@app.errorhandler(500)
def ressource_not_found(error):
    return jsonify({
        "success": False, 
        "status": 500,
        "message": "Internal server error"
    }), 500

@app.errorhandler(AuthError)
def auth_error(error):
   return jsonify({
        "success": False, 
        "status": error.status_code,
        "message": error.error['description']
    }), error.status_code
