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

# ============================================================================== SIGN UP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', pageTitle='Sign Up', navBar=True, logged_in=user_logged_in())
    elif request.method == 'POST':
        # Get form params
        firstname = request.form.get('firstname', None)
        lastname = request.form.get('lastname', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        # Check if password or email is present
        if password == '' or email == '':
            print('no email or password found')
            return jsonify(message='password and/or email required', status='failed')

        # !! Hash password with unsecure MD5, DO NOT USE IN PRODUCTION!!
        password_hash = hashlib.md5(password.encode())

        # New connection to database
        connection = new_connection()

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = '''
                        INSERT INTO `users` (`firstname`, `lastname`, `email`, `password`) VALUES (%s, %s, %s, %s)
                    '''
                cursor.execute(sql, (firstname, lastname,
                                     email, password_hash.hexdigest()))

                # Commit the save actions
                connection.commit()

                # Get new user id
                sql = 'SELECT LAST_INSERT_ID()'
                cursor.execute(sql)
                result = cursor.fetchone()
                user_id = result['LAST_INSERT_ID()']

        except Exception as err:
            print(err)
            return jsonify(message='Failed to submit new user', status='failed')
        finally:
            connection.close()

        # Set session variables
        session['email'] = email
        session['logged_in'] = True
        session['user_id'] = user_id

        # Return json reponse
        return jsonify(message='Record saved!', status='ok')

# ============================================================================== LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', pageTitle='Login', navBar=True, logged_in=user_logged_in())
    elif request.method == 'POST':
        # Delete user seesion
        session.pop('logged_in', None)

        # Get login parameters
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        # Get data from database
        connection = new_connection()

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT `password`, `id` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, (email))

                # Get result
                result = cursor.fetchone()

                if result is None:
                    print('Incorrect email')
                    return jsonify(message='Incorrect password or email', status='failed')

                # Hash password
                hashed_password = hashlib.md5(password.encode()).hexdigest()

                # Compare passwords
                if hashed_password == result['password']:
                    # Set session
                    session['email'] = email
                    session['logged_in'] = True
                    session['user_id'] = result['id']

                    # Logs
                    print('User logged in')
                    print(session)

                    return redirect(url_for('dashboard'))
                else:
                    print('Incorrect password')
                    return jsonify(message='Incorrect password or email', status='failed')
        except Exception as err:
            print(err)
        finally:
            connection.close()

# ============================================================================== LOGOUT
@app.route('/logout')
def logout():
    # Remove logged_in key
    session.pop('logged_in', None)

    # Logs
    print('User logged out')
    print(session)

    return redirect(url_for('index'))

# ============================================================================== DASHBOARD
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', pageTitle='My Dashboard', navBar=True, logged_in=user_logged_in())

# ============================================================================== DRINKS
@app.route('/drinks', methods=['GET'])
def drinks():
    return render_template('drinks.html', pageTitle='Drinks', navBar=True, logged_in=user_logged_in())


@app.route('/drinks/recipes', methods=['GET'])
def drinks_recipes():
    try:
        page = int(request.args.get('page'))
    except:
        return abort(404)

    # Check if query params exists
    if page is None:
        page = 1

    # Fetch recipe data
    results_per_page = 8
    recipes = get_all_recipes(results_per_page, page)
    # recipes = [convert_datetime(item) for item in recipes]
    total_number = count_all_recipes()

    # Construct response
    page_range = math.ceil(total_number[0] / results_per_page)
    response = {
        'pages': [{'active': True if page == i+1 else False, 'index': i+1} for i in range(page_range)],
        'recipes': recipes,
        'previous': page - 1 if page > 1 else False,
        'next': page + 1 if page < page_range else False
    }

    return jsonify(response)


# ============================================================================== RECIPE

@app.route('/recipe', methods=['GET', 'POST'])
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
                return redirect(url_for('get_recipe_page', recipe_id=db_operation['recipe_id']))
            else:
                return jsonify(message='Something went wrong during database operation', status='failed')
        else:
            return jsonify(message='Please provide json request', status='failed')


@app.route('/recipe/user/<user_id>')
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


@app.route('/recipe/user', methods=['GET'])
def redirect_to_user_recipes():
    # Get query params
    page = request.args.get('page')

    # Check if query params exists
    if page is None:
        page = 1

    # Redirect
    return redirect(url_for('get_recipes', user_id=session['user_id']) + '?page=' + str(page))


@app.route('/recipe/<recipe_id>', methods=['GET', 'PATCH', 'DELETE'])
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

            recipe_data = check_owner(recipe_data, session['user_id'])

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
                # Check favorite
                favorite = get_favorite(recipe_id, session['user_id'])
                if len(favorite) == 0:
                    recipe_data['favorite'] = False
                else:
                    recipe_data['favorite'] = True

                # Get ratings
                rating_data = get_ratings(recipe_id, session['user_id'])

                # Get comments and check if user is owner
                comments = get_comments(recipe_id)
                comments = [check_owner(
                    comment, session['user_id']) for comment in comments]
                commentsAvailable = True if len(comments) > 0 else False

                return render_template('recipe.html', pageTitle='Recipe', navBar=True, logged_in=user_logged_in(),
                                       title=recipe_data['title'], description=recipe_data[
                                           'description'], recipe=recipe_data['recipe'], views=recipe_data['views'],
                                       image_path=recipe_data['image_path'], date=recipe_data['date_created'].strftime(
                    '%d %b, %Y'), firstname=recipe_data['firstname'], lastname=recipe_data['lastname'], ingredients=recipe_data['ingredients'], owner=recipe_data['owner'],
                    favorite=recipe_data['favorite'], id=recipe_id, comments=comments, rating=rating_data,
                    commentsAvailable=commentsAvailable, labels=label_data)

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
                db_operation_labels = add_labels_to_recipe(recipe_id, recipe_data['labels'])


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

# ============================================================================== COMMENTS
@app.route('/comment/<recipe_id>', methods=['POST'])
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
        return redirect(url_for('get_recipe_page', recipe_id=recipe_id))
    else:
        return redirect(url_for('index'))


@app.route('/comment/<comment_id>', methods=['DELETE'])
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


# ============================================================================== FAVORITES
@app.route('/favorite/<recipe_id>', methods=['POST', 'DELETE'])
def recipe_favorite(recipe_id):
    if request.method == 'POST':
        # Check if favorite already present
        favorite = get_favorite(recipe_id, session['user_id'])

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


# ============================================================================== RATING
@app.route('/rating/', methods=['PATCH'])
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


# ============================================================================== USER
@app.route('/user/<user_id>', methods=['GET'])
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


@app.route('/user', methods=['GET', 'POST'])
def redirect_to_user_info():
    if request.method == 'GET':
        return redirect(url_for('get_user_info', user_id=session['user_id']))
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


@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    # Get all user favorites
    favorites = get_all_favorites(session['user_id'])

    # Check if error occured
    if favorites is False:
        return jsonify(message='An error occured during database operation', status='failed')

    return jsonify(status='success', favorites=favorites)


@app.route('/user/image', methods=['POST'])
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
