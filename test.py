from lib.db import new_connection, get_user_recipes, count_user_recipes, get_user_data, \
    get_recipe_data, get_comments, get_favorite, get_all_favorites, get_ratings, get_labels

# Parameters
user_id = 1
results_per_page = 2
page = 1
recipe_id = 18

# Try connecting new database instance
assert new_connection() != False, 'New database connection failed!'

# Try fetching user recipes
assert get_user_recipes(user_id, results_per_page,
                        page) != False, 'Could not retrieve user recipes!'

# Count all the user recipes
assert count_user_recipes(
    user_id) != False, 'Could not count the user recipes!'

# Get user data
assert get_user_data(user_id) != False, 'Could not retrieve user data!'

# Get recipe data
assert get_recipe_data(recipe_id) != False, 'Could not retrieve recipe data!'

# Get comments
assert get_comments(recipe_id) != False, 'Could not retrieve comments!'

# Get favorite
assert get_favorite(recipe_id, user_id) != False, 'Could not get favorite!'

# Get all favorites
assert get_all_favorites(
    user_id) != False, 'Could not get all favorites for user!'

# Get ratings with no user id
assert get_ratings(
    recipe_id) != False, 'Could not get rating when no user id is provided!'

# Get ratings with user id
assert get_ratings(
    recipe_id, user_id) != False, 'Could not get rating when user id is provided!'

# Get all labels
assert get_labels() != False, 'Could not retrieve all labels!'

# Get all labels for recipe
assert get_labels(
    recipe_id) != False, 'Could not retrieve labels for a given recipe!'

print('Database tests executed successfully!')
