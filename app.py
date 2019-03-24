import os
import pymysql
import hashlib
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from lib.db import new_connection, initialize_db
from lib.scripts import user_logged_in

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.urandom(32)

# Initialize db
# initialize_db()

# ============================================================================== INDEX
@app.route('/')
def index():

    return render_template('index.html',
                           pageTitle='Home - Tasting Experience',
                           navBar=False, logged_in=user_logged_in())

# ============================================================================== SIGN UP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', pageTitle='Sign Up - Tasting Experience', navBar=True, logged_in=user_logged_in())
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
        return render_template('login.html', pageTitle='Login - Tasting Experience', navBar=True, logged_in=user_logged_in())
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
                sql = "SELECT `password` FROM `users` WHERE `email`=%s"
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

    return redirect(url_for('index'))

# ============================================================================== DASHBOARD
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', pageTitle='My Dashboard - Tasting Experience', navBar=True, logged_in=user_logged_in())


# ============================================================================== NOT FOUND
@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html', pageTitle='Not Found - Tasting Experience', navBar=True, logged_in=user_logged_in()), 404


# Run the webserver
if __name__ == '__main__':
    settings = {
        'DEBUG': True
    }

    app.config.update(settings)

    app.run(os.environ.get('IP'),
            port=int('8080'))
