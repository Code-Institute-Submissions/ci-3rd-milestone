from flask import Blueprint, request, session, jsonify
from lib.db import get_favorite, create_favorite, delete_favorite

favorite_pages = Blueprint('favorite_pages', __name__)


@favorite_pages.route('/<recipe_id>', methods=['POST', 'DELETE'])
def recipe_favorite(recipe_id):
    if request.method == 'POST':
        # Check if favorite already present
        if session['user_id'] in session:
            favorite = get_favorite(recipe_id, session['user_id'])
        else:
            favorite = []

        if len(favorite) == 0:
            db_operation = create_favorite(recipe_id, session['user_id'])
            if db_operation is not True:
                return jsonify(message='Database error occured while trying to add the favorite', status='failed')

        return jsonify(message='Favorite successfully added!', status='success')

    elif request.method == 'DELETE':
        db_operation = delete_favorite(recipe_id, session['user_id'])
        if db_operation:
            return jsonify(message='Favorite successfully deleted!', status='success')
        else:
            return jsonify(message='Database error occured while trying to delete the favorite', status='failed')
