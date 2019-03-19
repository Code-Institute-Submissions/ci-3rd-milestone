import os
import pymysql


def new_connection():
    return pymysql.connect(
        host='db4free.net',
        user=os.environ['DB_USER_NAME'],
        password=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        port=int(os.environ['DB_PORT']))
