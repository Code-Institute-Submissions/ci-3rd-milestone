from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, abort
import math
import os
import base64
import datetime
from lib.scripts import user_logged_in, convert_datetime, check_owner, check_active_labels
from lib.db import get_labels, create_recipe, add_labels_to_recipe, get_user_recipes, count_user_recipes, \
    get_recipe_data, get_favorite, get_ratings, get_comments, delete_recipe, update_recipe, delete_labels, \
    add_view

recipe_pages = Blueprint('recipe_pages', __name__, template_folder='templates')


@recipe_pages.route('/', methods=['GET', 'POST'])
def recipe():
    if request.method == 'GET':
        labels = get_labels()
        return render_template('new-recipe.html', pageTitle='Add Recipe', navBar=True, logged_in=user_logged_in(), labels=labels)
    elif request.method == 'POST':
        if request.is_json:
            recipe_data = request.get_json()
            date_string = datetime.datetime.now().strftime('%c')

            # Get and process image data
            img_data = base64.b64decode(recipe_data['image_base64'])
            image_path = 'static/images/upload/recipe-' + \
                date_string.replace(' ', '-').replace(':', '') + '.jpg'
            with open(image_path, 'wb') as f:
                f.write(img_data)

            recipe_data['user_id'] = session['user_id']
            recipe_data['image_path'] = image_path

            # Create new recipe
            db_operation = create_recipe(recipe_data)

            # Update labels
            if db_operation is not False:
                db_operation_labels = add_labels_to_recipe(
                    db_operation['recipe_id'], recipe_data['labels'])

                if db_operation_labels:
                    return redirect(url_for('recipe_pages.get_recipe_page', recipe_id=db_operation['recipe_id']))
                else:
                    return jsonify(message='Something went wrong during database operation', status='failed')
        else:
            return jsonify(message='Please provide json request', status='failed')


@recipe_pages.route('/user/<user_id>')
def get_recipes(user_id):
    if user_id.isdigit():
        # Get query params
        try:
            page = int(request.args.get('page'))
        except:
            return abort(404)

        # Check if query params exists
        if page is None:
            page = 1

        results_per_page = 3
        recipes = get_user_recipes(user_id, results_per_page, page)
        recipes = [convert_datetime(item) for item in recipes]
        total_number = count_user_recipes(user_id)

        # Construct response
        page_range = math.ceil(total_number[0] / results_per_page)
        response = {
            'pages': [{'active': True if page == i+1 else False, 'index': i+1} for i in range(page_range)],
            'recipes': recipes,
            'previous': page - 1 if page > 1 else False,
            'next': page + 1 if page < page_range else False
        }
        return jsonify(response)
    else:
        return redirect(url_for('index'))


@recipe_pages.route('/user', methods=['GET'])
def redirect_to_user_recipes():
    # Get query params
    page = request.args.get('page')

    # Check if query params exists
    if page is None:
        page = 1

    # Redirect
    return redirect(url_for('recipe_pages.get_recipes', user_id=session['user_id']) + '?page=' + str(page))


@recipe_pages.route('/<recipe_id>', methods=['GET', 'PATCH', 'DELETE'])
def get_recipe_page(recipe_id):
    if recipe_id.isdigit():
        # GET REQUEST
        if request.method == 'GET':

            # Get arguments from url to determine edit mode
            editMode = request.args.get('edit')

            # Get recipe data
            recipe_data = get_recipe_data(recipe_id)
            if recipe_data is None:
                return abort(404)

            recipe_data = check_owner(recipe_data, session)

            # Get labels in recipe
            label_data = get_labels(recipe_id)

            # When in edit mode, return edit-recipe.html
            if editMode == 'true':
                # Get list of label ids that are present in the recipe
                recipe_labels = []
                for label in label_data:
                    recipe_labels.append(label['label_id'])

                # Get all labels present in the tasting experience site
                all_labels = get_labels()

                # Check labels active in recipe
                all_labels = [check_active_labels(
                    label, recipe_labels) for label in all_labels]

                # print(all_labels)
                return render_template('edit-recipe.html', pageTitle='Edit recipe', navBar=True, logged_in=user_logged_in(),
                                       title=recipe_data['title'], description=recipe_data[
                                           'description'], recipe=recipe_data['recipe'], image_path=recipe_data['image_path'],
                                       ingredients=recipe_data['ingredients'], id=recipe_id, labels=all_labels)
            else:

                if 'user_id' in session:
                    favorite = get_favorite(recipe_id, session['user_id'])

                    # Check favorite
                    recipe_data['favorite_active'] = True
                    recipe_data['comments_active'] = True
                    if len(favorite) == 0:
                        recipe_data['favorite'] = False
                    else:
                        recipe_data['favorite'] = True
                else:
                    recipe_data['favorite_active'] = False
                    recipe_data['comments_active'] = False

                # Get ratings
                if 'user_id' in session:
                    rating_data = get_ratings(recipe_id, session['user_id'])
                else:
                    rating_data = {
                        'user_rating': {'rating': 0},
                        'active': False
                    }

                # Get comments and check if user is owner
                comments = get_comments(recipe_id)
                comments = [check_owner(
                    comment, session) for comment in comments]
                commentsAvailable = True if len(comments) > 0 else False

                return render_template('recipe.html', pageTitle='Recipe', navBar=True, logged_in=user_logged_in(),
                                       date=recipe_data['date_created'].strftime('%d %b, %Y'), id=recipe_id, comments=comments, rating=rating_data,
                                       commentsAvailable=commentsAvailable, labels=label_data, data=recipe_data)

        # DELETE REQUEST
        elif request.method == 'DELETE':
            # Detele recipe image from server
            recipe_data = get_recipe_data(recipe_id)

            # Delete recipe from database
            db_operation = delete_recipe(recipe_id)

            # Check if operation was successfull
            if db_operation:
                # Delete image from server
                try:
                    os.remove(recipe_data['image_path'])
                except Exception as err:
                    print(err)

                return jsonify(message='Recipe successfully deleted!', status='ok')
            else:
                return jsonify(message='Something went wrong during database operation', status='failed')

        # PATCH REQUEST
        elif request.method == 'PATCH':
            if request.is_json:
                # Get new and old recipe data
                recipe_data = request.get_json()
                old_recipe_data = get_recipe_data(recipe_id)

                # Do following when image has been changed
                if recipe_data['image_base64'] != '':
                    date_string = datetime.datetime.now().strftime('%c')

                    # Get and process image data
                    img_data = base64.b64decode(recipe_data['image_base64'])
                    image_path = 'static/images/upload/recipe-' + \
                        date_string.replace(' ', '-').replace(':', '') + '.jpg'
                    with open(image_path, 'wb') as f:
                        f.write(img_data)

                    recipe_data['image_path'] = image_path

                    # remove old image
                    try:
                        os.remove(old_recipe_data['image_path'])
                    except Exception as err:
                        print(err)

                # Update the recipe
                db_operation = update_recipe(recipe_data, recipe_id)

                # Update labels by deleting and creating them
                delete_labels(recipe_id)
                db_operation_labels = add_labels_to_recipe(
                    recipe_id, recipe_data['labels'])

                if db_operation and db_operation_labels:
                    return jsonify(message='Recipe successfully updated!', status='success')
                else:
                    return jsonify(message='Something went wrong during database operation', status='failed')

            elif request.content_type == 'application/x-www-form-urlencoded':

                if request.form['view'] == 'true':
                    # Update views by one
                    recipe_data = get_recipe_data(recipe_id)
                    views = int(recipe_data['views']) + 1

                    # Update database
                    db_operation = add_view(recipe_id, views)

                    if db_operation:
                        return jsonify(message='Recipe view successfully updated!', status='success')
                    else:
                        return jsonify(message='Something went wrong during database operation', status='failed')
                else:
                    return jsonify(message='Could not understand patch request', status='failed')
    else:
        return abort(404)
