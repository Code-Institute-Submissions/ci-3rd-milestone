import os
import pymysql
from lib.scripts import convert_datetime_comments

'''
Gives a new database connection

'''


def new_connection():
    return pymysql.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER_NAME'],
        password=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        charset='utf8',
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
                        `ingredients` varchar(256) NOT NULL,
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
            sql = '''INSERT INTO `recipes` (`user_id`, `title`, `description`, `recipe`, `image_path`, `ingredients`)
                    VALUES (%s, %s, %s, %s, %s, %s)'''

            # Execute query
            cursor.execute(sql, (recipe_data['user_id'], recipe_data['title'],
                                 recipe_data['description'], recipe_data['recipe'], recipe_data['image_path'], recipe_data['ingredients']))

            # Commit to database
            connection.commit()

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()
        return True


'''
This function updates recipe in the database

'''


def update_recipe(recipe_data, recipe_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            # Check if image has to be updated
            if recipe_data['image_base64'] != '':
                sql = '''UPDATE recipes
                         SET title = %s, description = %s, recipe = %s, ingredients = %s, image_path = %s
                         WHERE id = %s
                         '''
                # Execute query
                cursor.execute(sql, (recipe_data['title'], recipe_data['description'],
                                     recipe_data['recipe'], recipe_data['ingredients'], recipe_data['image_path'], recipe_id))
            else:
                sql = '''UPDATE recipes
                         SET title = %s, description = %s, recipe = %s, ingredients = %s
                         WHERE id = %s
                         '''
                # Execute query
                cursor.execute(sql, (recipe_data['title'], recipe_data['description'],
                                     recipe_data['recipe'], recipe_data['ingredients'], recipe_id))

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


def get_user_recipes(user_id, results_per_page, page):
    # Determine start
    start_results = results_per_page * (int(page) - 1)

    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
                SELECT
                    `title`, `description`, `recipe`, `views`, `image_path`, `id`, `date_created`
                FROM `recipes`
                WHERE `user_id`=%s
                ORDER BY date_created DESC
                LIMIT %s, %s
                '''

            # Execute command
            cursor.execute(sql, (user_id, start_results, results_per_page))

            # Get all results
            result = cursor.fetchall()
            return result
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function counts all recipes from a specific user

'''


def count_user_recipes(user_id):
    connection = new_connection()

    try:
        with connection.cursor() as cursor:
            sql = '''
                SELECT COUNT(*) FROM `recipes`
                WHERE `user_id`=%s
                '''

            # Execute command
            cursor.execute(sql, user_id)

            # Get all results
            result = cursor.fetchone()
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
            sql = 'SELECT `id`, `firstname`, `lastname`, `email`, `image_path` FROM `users` WHERE `id`=%s'

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


'''
This function updates personal user profile picture path

'''


def update_user_image_path(image_path, user_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'UPDATE `users` SET `image_path`=%s WHERE `id`=%s'

            # Execute command
            cursor.execute(sql, (image_path, user_id))

            # Get all results
            connection.commit()

            return True
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function updates personal user data

'''


def update_user_data(user_data, user_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'UPDATE `users` SET `firstname`=%s, `lastname`=%s, `email`=%s WHERE `id`=%s'

            # Execute command
            cursor.execute(
                sql, (user_data['firstname'], user_data['lastname'], user_data['email'], user_id))

            # Get all results
            connection.commit()

            return True
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function gets all recipe data for viewing the recipe page

'''


def get_recipe_data(recipe_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
            SELECT
                recipes.user_id AS user_id, recipes.title AS title,
                recipes.description AS description, recipes.recipe AS recipe,
                recipes.views AS views, recipes.image_path AS image_path,
                recipes.date_created AS date_created, recipes.ingredients AS ingredients,
                users.firstname AS firstname, users.lastname AS lastname
            FROM `recipes`
            INNER JOIN `users` ON recipes.user_id=users.id
            WHERE recipes.id = %s'''

            # Execute command
            cursor.execute(sql, recipe_id)

            # Get all results
            result = cursor.fetchone()

            # Process ingredients
            ingredientSplit = result['ingredients'].split('</in>')
            del ingredientSplit[-1]
            ingredients = [
                item[item.find('<in>')+len('<in>'):] for item in ingredientSplit]

            # Add ingredients to result
            result['ingredients'] = ingredients

            return result
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function gets all recipe data for the drinks page

'''


def get_all_recipes(results_per_page, page):
    # Determine start
    start_results = results_per_page * (int(page) - 1)

    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
            SELECT
                id, title, description, views, image_path, date_created
            FROM `recipes`
            ORDER BY date_created DESC
            LIMIT %s, %s
            '''

            # Execute command
            cursor.execute(sql, (start_results, results_per_page))

            # Get all results
            results = cursor.fetchall()

            return results
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function counts all recipes

'''


def count_all_recipes():
    connection = new_connection()

    try:
        with connection.cursor() as cursor:
            sql = '''
                SELECT COUNT(*) FROM `recipes`
                '''

            # Execute command
            cursor.execute(sql)

            # Get all results
            result = cursor.fetchone()
            return result
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function deletes a recipe

'''


def delete_recipe(recipe_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'DELETE FROM `recipes` WHERE `id`=%s'

            # Execute command
            cursor.execute(
                sql, recipe_id)

            # Get all results
            connection.commit()

            return True
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function creates a new comment in the database

'''


def create_comment(comment_data):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''INSERT INTO comments (user_id, recipe_id, message)
                    VALUES (%s, %s, %s)'''

            # Execute query
            cursor.execute(
                sql, (comment_data['user_id'], comment_data['recipe_id'], comment_data['message']))

            # Commit to database
            connection.commit()

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()
        return True


'''
This function gets all comments from a recipe page

'''


def get_comments(recipe_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
            SELECT
                comments.id AS id, comments.user_id AS user_id, comments.message AS message,
                comments.date AS date_created, users.firstname AS firstname,
                users.lastname AS lastname, users.image_path AS image_path
            FROM comments
            INNER JOIN users ON comments.user_id = users.id
            WHERE recipe_id = %s'''

            # Execute command
            cursor.execute(sql, recipe_id)

            # Get all results
            result = cursor.fetchall()

            # Transform date string
            result = [convert_datetime_comments(item) for item in result]

            return result
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function deletes a recipe

'''


def delete_comment(comment_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'DELETE FROM comments WHERE id=%s'

            # Execute command
            cursor.execute(sql, comment_id)

            # Get all results
            connection.commit()

            return True
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function adds a view on a recipe

'''


def add_view(recipe_id, views):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'UPDATE recipes SET views = %s WHERE id = %s'

            # Execute command
            cursor.execute(sql, (views, recipe_id))

            # Get all results
            connection.commit()

            return True
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()
