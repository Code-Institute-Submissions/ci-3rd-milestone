import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for, jsonify
from lib.db import new_connection

# Initialize Flask
app = Flask(__name__)

# Index page
@app.route('/')
def index():
    return render_template('index.html', pageTitle='Home - Tasting Experience', navBar=False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', pageTitle='Sign Up - Tasting Experience', navBar=True)
    elif request.method == 'POST':
        # Get form params
        firstname = request.form.get('firstname', None)
        lastname = request.form.get('lastname', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        connection = new_connection()

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "INSERT INTO `users` (`firstname`, `lastname`, `email`, `password`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (firstname, lastname, email, password))

            # Commit the save actions
            connection.commit()
        finally:
            connection.close()

        return jsonify(message='Record saved!', status='ok')


@app.route('/db')
def hello():
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'SELECT * from users'
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    finally:
        connection.close()

    return str(result)


# Run the webserver
if __name__ == '__main__':
    settings = {
        'DEBUG': True
    }

    app.config.update(settings)

    app.run(os.environ.get('IP'),
            port=int('8080'))
