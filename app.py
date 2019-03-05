import os
import pymysql
import json
from flask import Flask, render_template, request, redirect, url_for

# Import config file
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except:
    config = None

# Set environment variables
if 'PORT' not in os.environ and config is not None:
    os.environ['PORT'] = config['PORT']
if 'DB_USER_NAME' not in os.environ and config is not None:
    os.environ['DB_USER_NAME'] = config['DB_USER_NAME']
if 'DB_PASSWORD' not in os.environ and config is not None:
    os.environ['DB_PASSWORD'] = config['DB_PASSWORD']
if 'DB_NAME' not in os.environ and config is not None:
    os.environ['DB_NAME'] = config['DB_NAME']
if 'DB_PORT' not in os.environ and config is not None:
    os.environ['DB_PORT'] = config['DB_PORT']

# Initialize Flask
app = Flask(__name__)

# Index page
@app.route('/')
def index():
    return render_template('index.html', pageTitle='Home - Tasting Experience')

# Test db route
@app.route('/db')
def hello():
    connection = pymysql.connect(
        host='db4free.net', user=os.environ['DB_USER_NAME'], password=os.environ['DB_PASSWORD'], db=os.environ['DB_NAME'], port=int(os.environ['DB_PORT']))

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
    app.run(os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
