from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, abort
from lib.db import create_comment, delete_comment

comment_pages = Blueprint('comment_pages', __name__,
                          template_folder='templates')


@comment_pages.route('/<recipe_id>', methods=['POST'])
def post_comment_recipe(recipe_id):
    # Construct comment data
    comment_data = {
        "message": request.form['comment'],
        "recipe_id": recipe_id,
        "user_id": session['user_id']
    }

    # Create comments
    db_operation = create_comment(comment_data)

    if db_operation:
        return redirect(url_for('recipe_pages.get_recipe_page', recipe_id=recipe_id))
    else:
        return redirect(url_for('index'))


@comment_pages.route('/<comment_id>', methods=['DELETE'])
def delete_comment_recipe(comment_id):
    if comment_id.isdigit():
        # Create comments
        db_operation = delete_comment(comment_id)

        if db_operation:
            return jsonify(message='Comment successfully deleted!', status='success')
        else:
            return jsonify(message='Database error occured while trying to delete the comment', status='failed')
    else:
        return abort(500)
