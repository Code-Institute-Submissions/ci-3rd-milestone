import os
import pymysql
import hashlib
import base64
import datetime
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from lib.db import new_connection, initialize_db, create_recipe, get_recipes, get_user_data, update_user_image_path, update_user_data
from lib.scripts import user_logged_in

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
                sql = "INSERT INTO `users` (`firstname`, `lastname`, `email`, `password`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (firstname, lastname,
                                     email, password_hash.hexdigest()))

            # Commit the save actions
            connection.commit()
        except Exception as err:
            print(err)
            return jsonify(message='Failed to submit new user', status='failed')
        finally:
            connection.close()

        # Set session variables
        session['email'] = email
        session['logged_in'] = True

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


# ============================================================================== RECIPE
@app.route('/recipe', methods=['GET', 'POST'])
def recipe():
    if request.method == 'GET':
        return render_template('recipe.html', pageTitle='Add Recipe', navBar=True, logged_in=user_logged_in())
    elif request.method == 'POST':
        if request.is_json:
            recipe_data = request.get_json()
            date_string = datetime.datetime.now().strftime('%c')

            # Get and process image data
            img_data = base64.b64decode(recipe_data['image_base64'])
            image_path = 'static/images/upload/recipe-' + \
                date_string.replace(' ', '-') + '.jpg'
            with open(image_path, 'wb') as f:
                f.write(img_data)

            recipe_data['user_id'] = session['user_id']
            recipe_data['image_path'] = image_path

            # Create new recipe
            db_operation = create_recipe(recipe_data)

            if db_operation:
                return redirect(url_for('dashboard'))
            else:
                return jsonify(message='Something went wrong during database operation', status='failed')
        else:
            return jsonify(message='Please provide json request', status='failed')


@app.route('/recipe/user/<user_id>')
def get_user_recipes(user_id):
    if user_id.isdigit():
        recipes = get_recipes(user_id)
        return jsonify(recipes)
    else:
        return redirect(url_for('index'))


@app.route('/recipe/user', methods=['GET'])
def redirect_to_user_recipes():
    return redirect(url_for('get_user_recipes', user_id=session['user_id']))

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
    return render_template('not_found.html', pageTitle='Not Found', navBar=True, logged_in=user_logged_in()), 404


# Run the webserver
if __name__ == '__main__':
    settings = {
        'DEBUG': True
    }

    app.config.update(settings)

    app.run(os.environ.get('IP'),
            port=int('8080'))
