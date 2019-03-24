from flask import session

# Check if user is logged in


def user_logged_in():
    if 'logged_in' in session:
        return True
    else:
        return False
