from lib.db import create_favorite, get_favorite, add_rating, update_rating, get_ratings

# profile get_recipes
# get_recipes(1)
# get_user_data(11)
# get_user_recipes(4, 3, 1)
# get_all_recipes()

# result = get_comments(37)
# result = create_favorite(38, 1)
# result = get_favorite(38, 2)


db_operation = update_rating('38', '1', 4)

print(db_operation)


# print(len(result))
# print(result)
