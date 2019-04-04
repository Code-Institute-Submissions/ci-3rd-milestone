import os
import pymysql

'''
Gives a new database connection

'''


def new_connection():
    return pymysql.connect(
        host='db4free.net',
        user=os.environ['DB_USER_NAME'],
        password=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        port=int(os.environ['DB_PORT']))


'''
This function initializes a new MySQL database with all the required tables and columns

TABLES
- users
- comments
- recipes
- ratings
- labels
- label_recipe
- favorites
'''


def initialize_db():
    connection = new_connection()

    # Users table
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''CREATE TABLE `users` (
                        `id` int NOT NULL AUTO_INCREMENT,
                        `firstname` varchar(20) DEFAULT NULL,
                        `lastname` varchar(20) DEFAULT NULL,
                        `password` varchar(32) NOT NULL,
                        `email` varchar(50) NOT NULL UNIQUE,
                        `image_path` varchar(256),
                        PRIMARY KEY (id)
                        )'''

            cursor.execute(sql)

        # Commit the save actions
        # connection.commit()
    except Exception as err:
        print(err)

    # Recipes table
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''CREATE TABLE `recipes` (
                        `id` int NOT NULL AUTO_INCREMENT,
                        `user_id` int NOT NULL,
                        `title` varchar(32) NOT NULL,
                        `description` varchar(256) NOT NULL,
                        `recipe` varchar(256) NOT NULL,
                        `views` int DEFAULT 0,
                        `image_path` varchar(256),
                        `date_created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id),
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        )'''

            cursor.execute(sql)

        # Commit the save actions
        # connection.commit()
    except Exception as err:
        print(err)

    # Comments table
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''CREATE TABLE `comments` (
                        `id` int NOT NULL AUTO_INCREMENT,
                        `user_id` int NOT NULL,
                        `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        `message` varchar(500) NOT NULL,
                        `recipe_id` int NOT NULL,
                        PRIMARY KEY (id),
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
                        )'''

            cursor.execute(sql)

        # Commit the save actions
        # connection.commit()
    except Exception as err:
        print(err)

    # Ratings table
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''CREATE TABLE `ratings` (
                        `id` int NOT NULL AUTO_INCREMENT,
                        `user_id` int NOT NULL,
                        `recipe_id` int NOT NULL,
                        `rating` int NOT NULL DEFAULT 0,
                        PRIMARY KEY (id),
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (recipe_id) REFERENCES recipes(id)
                        )'''

            cursor.execute(sql)

        # Commit the save actions
        # connection.commit()
    except Exception as err:
        print(err)

    # Labels table
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''CREATE TABLE `labels` (
                        `id` int NOT NULL AUTO_INCREMENT,
                        `name` varchar(20) NOT NULL,
                        PRIMARY KEY (id)
                        )'''

            cursor.execute(sql)

        # Commit the save actions
        # connection.commit()
    except Exception as err:
        print(err)

    # Labels_recipe table
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''CREATE TABLE `label_recipe` (
                        `id` int NOT NULL AUTO_INCREMENT,
                        `recipe_id` int NOT NULL,
                        `label_id` int NOT NULL,
                        PRIMARY KEY (id),
                        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                        FOREIGN KEY (label_id) REFERENCES labels(id)
                        )'''

            cursor.execute(sql)

        # Commit the save actions
        # connection.commit()
    except Exception as err:
        print(err)

    # Favories table
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''CREATE TABLE `favorites` (
                        `id` int NOT NULL AUTO_INCREMENT,
                        `recipe_id` int NOT NULL,
                        `user_id` int NOT NULL,
                        PRIMARY KEY (id),
                        FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        )'''

            cursor.execute(sql)

        # Commit the save actions
        # connection.commit()
    except Exception as err:
        print(err)
    # Close the connection
    connection.close()


'''
This function creates a new recipe in the database

'''


def create_recipe(recipe_data):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''INSERT INTO `recipes` (`user_id`, `title`, `description`, `recipe`, `image_path`)
                    VALUES (%s, %s, %s, %s, %s)'''

            # Execute query
            cursor.execute(sql, (recipe_data['user_id'], recipe_data['title'],
                                 recipe_data['description'], recipe_data['recipe'], recipe_data['image_path']))

            # Commit to database
            connection.commit()

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()
        return True


'''
This function gets all recipes from a specific user

'''


def get_recipes(user_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''SELECT `title`, `description`, `recipe`, `views`, `image_path` 
                    FROM `recipes` WHERE `user_id`=%s'''

            # Execute command
            cursor.execute(sql, (user_id))

            # Get all results
            result = cursor.fetchall()
            return result
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function gets personal user data

'''


def get_user_data(user_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'SELECT `firstname`, `lastname`, `email`, `image_path` FROM `users` WHERE `id`=%s'

            # Execute command
            cursor.execute(sql, (user_id))

            # Get all results
            result = cursor.fetchone()
            return result
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()
