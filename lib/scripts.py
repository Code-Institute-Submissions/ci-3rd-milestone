from flask import session
import datetime


# Check if user is logged in


def user_logged_in():
    if 'logged_in' in session:
        return True
    else:
        return False


def convert_datetime(item):
    item['date'] = item['date_created'].strftime('%d %b, %Y')
    return item


def convert_datetime_comments(item):
    item['date'] = item['date_created'].strftime('%d %b, %Y at %H:%M')
    return item


def check_owner(item, session):
    if 'user_id' in session:
        user_id = session['user_id']

        if item['user_id'] == user_id:
            item['owner'] = True
        elif user_id == 1:
            item['owner'] = True
        else:
            item['owner'] = False
    else:
        item['owner'] = False
    return item


def check_active_labels(label, recipe_labels):

    if label['id'] in recipe_labels:
        label['active'] = True
    else:
        label['active'] = False
    return label
