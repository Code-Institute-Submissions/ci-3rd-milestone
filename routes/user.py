from flask import Blueprint, request, session, redirect, url_for, jsonify
import hashlib
import datetime
import os
import base64
from lib.db import get_user_data, update_user_data, get_all_favorites, update_user_image_path

user_pages = Blueprint('user_pages', __name__)


@user_pages.route('/<user_id>', methods=['GET'])
def get_user_info(user_id):
    if user_id.isdigit():
        user_info = get_user_data(user_id)

        # Check for profile photo
        if user_info['image_path'] is None:
            user_info['image_path'] = url_for(
                'static', filename='images/placeholder.png')

        return jsonify(user_info)
    else:
        return redirect(url_for('index'))


@user_pages.route('/', methods=['GET', 'POST'])
def redirect_to_user_info():
    if request.method == 'GET':
        return redirect(url_for('user_pages.get_user_info', user_id=session['user_id']))
    elif request.method == 'POST':
        if request.is_json:
            user_data = request.get_json()

            # Update user image
            db_operation = update_user_data(
                user_data, session['user_id'])

            if db_operation:
                return jsonify(message='Successfully updated in database', status='ok')
            else:
                return jsonify(message='Something went wrong during database operation', status='failed')
        else:
            return jsonify(message='Please provide json request', status='failed')


@user_pages.route('/favorites', methods=['GET'])
def get_user_favorites():
    # Get all user favorites
    favorites = get_all_favorites(session['user_id'])

    # Check if error occured
    if favorites is False:
        return jsonify(message='An error occured during database operation', status='failed')

    return jsonify(status='success', favorites=favorites)


@user_pages.route('/image', methods=['POST'])
def update_user_image():
    if session['user_id'] is not None:
        if request.is_json:
            image_data = request.get_json()
            date_string = datetime.datetime.now().strftime('%c')
            unique_hash = hashlib.md5(date_string.encode())

            # Get and process image data
            img_data = base64.b64decode(image_data['image_base64'])
            image_path = 'static/images/upload/profile-picture-user-' + \
                str(session['user_id']) + '-' + \
                unique_hash.hexdigest() + '.jpg'
            with open(image_path, 'wb') as f:
                f.write(img_data)

            # Update user image
            db_operation = update_user_image_path(
                image_path, session['user_id'])

            if db_operation:
                # remove old image
                try:
                    os.remove(image_data['old_image_path'])
                except Exception as err:
                    print(err)

                return jsonify(message='Successfully updated in database', status='ok', new_image_path=image_path)
            else:
                return jsonify(message='Something went wrong during database operation', status='failed')

    else:
        return jsonify(message='No user found', status='failed')
