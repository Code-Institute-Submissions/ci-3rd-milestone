from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort
import os
from lib.scripts import user_logged_in

# Import Blueprints
from routes.base import base_pages
from routes.drinks import drinks_pages
from routes.recipe import recipe_pages
from routes.comment import comment_pages
from routes.favorite import favorite_pages
from routes.rating import rating_pages
from routes.user import user_pages
from routes.error import not_found, server_error

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']


# BLUEPRINTS
app.register_blueprint(base_pages)
app.register_blueprint(drinks_pages, url_prefix='/drinks')
app.register_blueprint(recipe_pages, url_prefix='/recipe')
app.register_blueprint(comment_pages, url_prefix='/comment')
app.register_blueprint(favorite_pages, url_prefix='/favorite')
app.register_blueprint(rating_pages, url_prefix='/rating')
app.register_blueprint(user_pages, url_prefix='/user')

# Error handlers
app.register_error_handler(404, not_found)
app.register_error_handler(500, server_error)


# Run the webserver
if __name__ == '__main__':
    settings = {
        'DEBUG': True
    }

    app.config.update(settings)

    app.run(os.environ.get('IP'),
            port=int('8080'))
