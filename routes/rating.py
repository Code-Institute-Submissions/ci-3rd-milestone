from flask import Blueprint, request, session, jsonify
from lib.db import get_ratings, add_rating, update_rating

rating_pages = Blueprint('rating_pages', __name__)


@rating_pages.route('/', methods=['PATCH'])
def update_rating_recipe():
    if request.is_json:
        # Get json data
        rating_data = request.get_json()

        # Check if rating exists for user
        rating = get_ratings(rating_data['recipe_id'], session['user_id'])

        if rating['user_rating'] == None:
            db_operation = add_rating(
                rating_data['recipe_id'], session['user_id'], rating_data['rating'])
        else:
            db_operation = update_rating(
                rating_data['recipe_id'], session['user_id'], rating_data['rating'])

        # Check if db operation was successful
        if db_operation:
            return jsonify(message='Rating updated!', status='success')
        else:
            return jsonify(message='Something went wrong :/', status='failed')

    return jsonify(message='Request is not JSON', status='failed')
