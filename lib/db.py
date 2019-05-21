import os
import pymysql
from lib.scripts import convert_datetime_comments

'''
Gives a new database connection

'''


def new_connection():
    try:
        return pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER_NAME'],
            password=os.environ['DB_PASSWORD'],
            db=os.environ['DB_NAME'],
            charset='utf8',
            port=int(os.environ['DB_PORT']))
    except Exception as err:
        print(err)
        return False


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
                        `recipe` varchar(500) NOT NULL,
                        `ingredients` varchar(500) NOT NULL,
                        `views` int DEFAULT 0,
                        `avg_rating` float  DEFAULT 0,
                        `nr_ratings` int DEFAULT 0,
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
                        ON DELETE CASCADE
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
                        ON DELETE CASCADE
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
                        ON DELETE CASCADE
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
                        ON DELETE CASCADE
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

            sql = '''SELECT LAST_INSERT_ID() AS recipe_id'''
            cursor.execute(sql)
            result = cursor.fetchone()
            return result

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


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
                recipes.id AS id, recipes.user_id AS user_id, recipes.title AS title,
                recipes.description AS description, recipes.recipe AS recipe,
                recipes.views AS views, recipes.image_path AS image_path,
                recipes.date_created AS date_created, recipes.ingredients AS ingredients,
                recipes.avg_rating AS avg_rating, recipes.nr_ratings as nr_ratings,
                users.firstname AS firstname, users.lastname AS lastname
            FROM `recipes`
            INNER JOIN `users` ON users.id=recipes.user_id
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

            # Update rating data string
            result['avg_rating'] = str(
                round(result['avg_rating'], 1)) + ' out of 5 stars'
            result['nr_ratings'] = str(
                result["nr_ratings"]) + ' ratings' if result["nr_ratings"] != 1 else str(result["nr_ratings"]) + ' rating'

            return result
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function gets all recipe data for the drinks page

'''


def get_all_recipes(results_per_page, page, labels, rating):
    # Determine start
    start_results = results_per_page * (int(page) - 1)

    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # When no search query
            if labels is None and rating is None:
                sql = '''
                SELECT
                    id, title, description, views, image_path, date_created, avg_rating,
                    nr_ratings
                FROM recipes
                ORDER BY date_created DESC
                LIMIT %s, %s
                '''

                # Execute command
                cursor.execute(sql, (start_results, results_per_page))

            elif labels is None and rating is not None:
                # Get recipes with specific rating
                sql = '''
                SELECT
                    id, title, description, views, image_path, date_created, avg_rating,
                    nr_ratings
                FROM recipes
                WHERE avg_rating >= %s
                ORDER BY avg_rating DESC
                LIMIT %s, %s
                '''

                # Execute command
                cursor.execute(
                    sql, (rating-0.2, start_results, results_per_page))

            elif rating is None and labels is not None:
                # Get recipes with specific rating
                sql = '''
                SELECT
                    recipes.id, title, description, views, image_path, date_created, avg_rating,
                    nr_ratings
                FROM recipes
                INNER JOIN label_recipe ON recipes.id = label_recipe.recipe_id
                WHERE '''

                for i in range(len(labels)):
                    if i < len(labels)-1:
                        sql += 'label_recipe.label_id = %s OR '
                    else:
                        sql += 'label_recipe.label_id = %s'

                sql += '''
                ORDER BY recipes.avg_rating DESC
                LIMIT %s, %s
                '''

                # Execute command
                sqlParams = labels.copy()
                sqlParams.extend([start_results, results_per_page])

                cursor.execute(sql, sqlParams)

            elif rating is not None and labels is not None:
                # Get recipes with specific rating
                sql = '''
                SELECT
                    recipes.id, title, description, views, image_path, date_created, avg_rating,
                    nr_ratings
                FROM recipes
                INNER JOIN label_recipe ON recipes.id = label_recipe.recipe_id
                WHERE ('''

                for i in range(len(labels)):
                    if i < len(labels)-1:
                        sql += 'label_recipe.label_id = %s OR '
                    else:
                        sql += 'label_recipe.label_id = %s) AND avg_rating >= %s'

                sql += '''
                ORDER BY recipes.avg_rating DESC
                LIMIT %s, %s
                '''

                # Execute command
                sqlParams = labels.copy()
                sqlParams.extend([rating-0.2, start_results, results_per_page])

                cursor.execute(sql, sqlParams)

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


def count_all_recipes(labels, rating):
    connection = new_connection()

    try:
        with connection.cursor() as cursor:
            # When no search query
            if labels is None and rating is None:
                sql = '''
                    SELECT COUNT(*) FROM recipes
                    '''
                # Execute command
                cursor.execute(sql)

            elif labels is None and rating is not None:
                sql = '''
                    SELECT COUNT(*) 
                    FROM recipes
                    WHERE avg_rating >= %s
                    '''
                # Execute command
                cursor.execute(sql, rating-0.2)

            elif rating is None and labels is not None:
                sql = '''
                    SELECT COUNT(*) 
                    FROM recipes
                    INNER JOIN label_recipe ON recipes.id = label_recipe.recipe_id
                    WHERE
                    '''
                for i in range(len(labels)):
                    if i < len(labels)-1:
                        sql += 'label_recipe.label_id = %s OR '
                    else:
                        sql += 'label_recipe.label_id = %s'

                # Execute command
                cursor.execute(sql, labels)

            elif rating is not None and labels is not None:
                # Get recipes with specific rating
                sql = '''
                SELECT COUNT(*)
                FROM recipes
                INNER JOIN label_recipe ON recipes.id = label_recipe.recipe_id
                WHERE ('''

                for i in range(len(labels)):
                    if i < len(labels)-1:
                        sql += 'label_recipe.label_id = %s OR '
                    else:
                        sql += 'label_recipe.label_id = %s) AND avg_rating >= %s'

                # Execute command
                sqlParams = labels.copy()
                sqlParams.extend([rating-0.2])

                cursor.execute(sql, sqlParams)

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
            return True

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


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


'''
This function gets a favorite of a user in the database

'''


def get_favorite(recipe_id, user_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
            SELECT
                favorites.recipe_id AS recipe_id, favorites.id AS id, 
                favorites.user_id AS user_id, recipes.title AS title, 
                recipes.description AS description
            FROM favorites
            INNER JOIN recipes ON favorites.recipe_id = recipes.id
            WHERE favorites.recipe_id = %s AND favorites.user_id = %s'''

            # Execute query
            cursor.execute(
                sql, (recipe_id, user_id))

            # Get results
            results = cursor.fetchall()

            return results
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function gets all favorites of a user in the database

'''


def get_all_favorites(user_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
            SELECT
                favorites.recipe_id AS recipe_id, favorites.id AS id, 
                favorites.user_id AS user_id, recipes.title AS title, 
                recipes.description AS description
            FROM favorites
            INNER JOIN recipes ON favorites.recipe_id = recipes.id
            WHERE favorites.user_id = %s'''

            # Execute query
            cursor.execute(
                sql, (user_id))

            # Get results
            results = cursor.fetchall()

            return results
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function creates a new favorite in the database

'''


def create_favorite(recipe_id, user_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''INSERT INTO favorites (recipe_id, user_id)
                    VALUES (%s, %s)'''

            # Execute query
            cursor.execute(
                sql, (recipe_id, user_id))

            # Commit to database
            connection.commit()

            return True

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function deletes all favorites for a recipe for a specific user in the database

'''


def delete_favorite(recipe_id, user_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
                    DELETE FROM favorites 
                    WHERE recipe_id = %s AND user_id = %s 
                    '''

            # Execute query
            cursor.execute(
                sql, (recipe_id, user_id))

            # Commit to database
            connection.commit()

            return True

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function adds a new rating for a recipe

'''


def add_rating(recipe_id, user_id, rating):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''INSERT INTO ratings (recipe_id, user_id, rating)
                    VALUES (%s, %s, %s)'''

            # Execute query
            cursor.execute(
                sql, (recipe_id, user_id, rating))

            # Commit to database
            connection.commit()

            # Update rating on recipe
            ratings = get_ratings(recipe_id)
            sql = '''
                    UPDATE recipes
                    SET avg_rating = %s, nr_ratings = %s
                    WHERE id = %s
                '''
            # Execute query
            cursor.execute(
                sql, (ratings["average"], ratings["total"], recipe_id))

            # Commit to database
            connection.commit()

            return True

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function updates a rating for a recipe

'''


def update_rating(recipe_id, user_id, rating):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
                    UPDATE ratings
                    SET rating = %s
                    WHERE recipe_id = %s AND user_id = %s
                '''

            # Execute query
            cursor.execute(
                sql, (rating, recipe_id, user_id))

            # Commit to database
            connection.commit()

            # Update rating on recipe
            ratings = get_ratings(recipe_id)
            sql = '''
                    UPDATE recipes
                    SET avg_rating = %s, nr_ratings = %s
                    WHERE id = %s
                '''
            # Execute query
            cursor.execute(
                sql, (ratings["average"], ratings["total"], recipe_id))

            # Commit to database
            connection.commit()

            return True

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function gets a rating from a recipe. When user_id is filled in, the rating
of the user will be fetched as well

'''


def get_ratings(recipe_id, user_id=None):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = '''
                    SELECT id, rating, user_id 
                    FROM ratings
                    WHERE recipe_id = %s
                '''

            # Execute query
            cursor.execute(
                sql, recipe_id)

            # Get results from database
            ratings = cursor.fetchall()

            if len(ratings) > 0:
                # Calculate average rating
                sumRating = 0
                for rating in ratings:
                    sumRating += rating["rating"]

                averageRating = sumRating / len(ratings)
            else:
                averageRating = 0.0

            result = {
                "ratings": ratings,
                "average": averageRating,
                "total": len(ratings),
                "user_rating": None
            }

            if user_id is not None:
                # If user id is filled, get user rating
                sql = '''
                        SELECT id, rating, user_id 
                        FROM ratings
                        WHERE recipe_id = %s AND user_id = %s
                    '''

                # Execute query
                cursor.execute(sql, (recipe_id, user_id))

                user_rating = cursor.fetchone()

                result["user_rating"] = user_rating
                result["active"] = True

            return result

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function gets all labels for recipes

'''


def get_labels(recipe_id=None):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            if recipe_id is None:
                sql = '''
                    SELECT * FROM labels ORDER BY name ASC
                    '''
                # Execute query
                cursor.execute(sql)
            else:
                sql = '''
                    SELECT label_recipe.id AS id, label_recipe.recipe_id AS recipe_id, 
                    label_recipe.label_id AS label_id, labels.name AS name 
                    FROM label_recipe
                    INNER JOIN labels ON label_recipe.label_id = labels.id 
                    WHERE recipe_id = %s
                    ORDER BY name ASC
                    '''
                # Execute query
                cursor.execute(sql, recipe_id)

            # Get results
            results = cursor.fetchall()

            return results
    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function adds labels to a recipe

'''


def add_labels_to_recipe(recipe_id, labels):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # construct sql code
            sql = '''INSERT INTO label_recipe (recipe_id, label_id)
                    VALUES '''

            for i in range(len(labels)):
                if i != len(labels)-1:
                    sql += ' (' + str(recipe_id) + ',' + str(labels[i]) + '), '
                else:
                    sql += ' (' + str(recipe_id) + ',' + str(labels[i]) + ')'

            # Execute query
            cursor.execute(sql)

            # Commit to database
            connection.commit()

            return True

    except Exception as err:
        print(err)
        return False
    finally:
        connection.close()


'''
This function deletes all labels for a recipe

'''


def delete_labels(recipe_id):
    connection = new_connection()

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = 'DELETE FROM label_recipe WHERE recipe_id=%s'

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
