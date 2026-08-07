from flask import session
from functools import wraps

def auth_check(func):
    """
    Decorator to check if the user is authenticated.
    If not, it redirects to the login page.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> object:
        if 'user_id' not in session:
            return "Unauthorized", 401  # Or redirect to login page
        return func(*args, **kwargs)
    return wrapper