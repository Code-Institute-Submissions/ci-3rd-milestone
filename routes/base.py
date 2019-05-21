from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
import hashlib
import pymysql
from lib.db import new_connection
from lib.scripts import user_logged_in

base_pages = Blueprint('base_pages', __name__, template_folder='templates')

# ============================================================================== INDEX
@base_pages.route('/')
def index():
    return render_template('index.html',
                           pageTitle='Home',
                           navBar=False, logged_in=user_logged_in())

# ============================================================================== SIGN UP
@base_pages.route('/signup', methods=['GET', 'POST'])
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
@base_pages.route('/login', methods=['GET', 'POST'])
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

                    return redirect(url_for('base_pages.dashboard'))
                else:
                    print('Incorrect password')
                    return jsonify(message='Incorrect password or email', status='failed')
        except Exception as err:
            print(err)
        finally:
            connection.close()

# ============================================================================== DASHBOARD
@base_pages.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', pageTitle='My Dashboard', navBar=True, logged_in=user_logged_in())

# ============================================================================== ABOUT
@base_pages.route('/about', methods=['GET'])
def about():
    return render_template('about.html', pageTitle='About', navBar=True, logged_in=user_logged_in())

# ============================================================================== LOGOUT
@base_pages.route('/logout')
def logout():
    # Remove logged_in key
    session.pop('logged_in', None)
    session.pop('user_id')

    # Logs
    print('User logged out')
    print(session)

    return redirect(url_for('base_pages.index'))
