import os
import pymysql
import hashlib
import base64
import datetime
import math
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort
from lib.scripts import user_logged_in, convert_datetime, check_owner, check_active_labels
from lib.db import new_connection, initialize_db, create_recipe, get_user_recipes, get_user_data, \
    update_user_image_path, update_user_data, get_recipe_data, delete_recipe, count_user_recipes, \
    get_all_recipes, count_all_recipes, update_recipe, create_comment, get_comments, delete_comment, \
    add_view, get_favorite, create_favorite, delete_favorite, get_all_favorites, get_ratings, \
    add_rating, update_rating, get_labels, add_labels_to_recipe, delete_labels

from routes.base import base_pages
from routes.drinks import drinks_pages
from routes.recipe import recipe_pages
from routes.comment import comment_pages
from routes.favorite import favorite_pages
from routes.rating import rating_pages
from routes.user import user_pages

# Initialize Flask
app = Flask(__name__)
# app.secret_key = os.urandom(32)
app.secret_key = 'KbHRUcjZmYTrfieBoO4185IeJodq41sA'


# Initialize db
# initialize_db()

# ============================================================================== INDEX
@app.route('/')
def index():
    return render_template('index.html',
                           pageTitle='Home',
                           navBar=False, logged_in=user_logged_in())


# ============================================================================== BLUEPRINTS
app.register_blueprint(base_pages)
app.register_blueprint(drinks_pages, url_prefix='/drinks')
app.register_blueprint(recipe_pages, url_prefix='/recipe')
app.register_blueprint(comment_pages, url_prefix='/comment')
app.register_blueprint(favorite_pages, url_prefix='/favorite')
app.register_blueprint(rating_pages, url_prefix='/rating')
app.register_blueprint(user_pages, url_prefix='/user')


# ============================================================================== NOT FOUND
@app.errorhandler(404)
def not_found(error):
    return render_template('not-found.html', pageTitle='Not Found', navBar=True, logged_in=user_logged_in()), 404


@app.errorhandler(500)
def server_error(error):
    print(error)
    return render_template('server-error.html', pageTitle='Not Found', navBar=True, logged_in=user_logged_in()), 500


# Run the webserver
if __name__ == '__main__':
    settings = {
        'DEBUG': True
    }

    app.config.update(settings)

    app.run(os.environ.get('IP'),
            port=int('8080'))
