
from flask import session, render_template, redirect, url_for
from functools import wraps

def is_customer_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'customer_logged_in' in session:
            return f(*args, **kwargs)
        return redirect(url_for('customer_login'))

    return wrapper

"""
def not_customer_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'customer_logged_in' in session:
            return f(*args, **kwargs)
        return redirect(url_for('website'))

    return wrapper
"""