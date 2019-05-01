from lib.db import new_connection, get_all_recipes, initialize_db, create_recipe, get_user_recipes, get_user_data, update_user_image_path, update_user_data, get_comments

# profile get_recipes
# get_recipes(1)
# get_user_data(11)
# get_user_recipes(4, 3, 1)
# get_all_recipes()

result = get_comments(37)

print(result[0]['date'])
