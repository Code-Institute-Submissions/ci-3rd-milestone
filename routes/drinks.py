from flask import Blueprint, render_template, request, jsonify, abort
import math
from lib.db import get_labels, get_all_recipes, count_all_recipes
from lib.scripts import user_logged_in

drinks_pages = Blueprint('drinks_pages', __name__, template_folder='templates')


@drinks_pages.route('/', methods=['GET'])
def drinks():
    labels = get_labels()
    return render_template('drinks.html', pageTitle='Drinks', navBar=True, logged_in=user_logged_in(), labels=labels)


@drinks_pages.route('/recipes', methods=['GET'])
def drinks_recipes():
    try:
        page = request.args.get('page')
        labels = request.args.get('labels')
        rating = request.args.get('rating')

        # Check if empty
        if labels == '':
            labels = None
        if rating == '':
            rating = None

        # Try to convert to int when not None
        if page != None:
            page = int(page)
        if rating != None:
            rating = int(rating)
        if labels != None:
            labels = labels.split(' ')
    except:
        return abort(404)

    # Fetch recipe data
    results_per_page = 8
    recipes = get_all_recipes(results_per_page, page, labels, rating)

    # recipes = [convert_datetime(item) for item in recipes]
    total_number = count_all_recipes(labels, rating)

    # Construct response
    page_range = math.ceil(total_number[0] / results_per_page)
    response = {
        'pages': [{'active': True if page == i+1 else False, 'index': i+1} for i in range(page_range)],
        'recipes': recipes,
        'previous': page - 1 if page > 1 else False,
        'next': page + 1 if page < page_range else False
    }

    return jsonify(response)
