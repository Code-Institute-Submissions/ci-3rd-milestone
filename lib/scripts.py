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
