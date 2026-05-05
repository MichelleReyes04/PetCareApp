from flask import Blueprint
from controllers.auth_controller import google_login, google_callback, logout

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def google_login_route():
    return google_login()

@auth_bp.route('/auth/callback')
def google_callback_route():
    return google_callback()

@auth_bp.route('/logout')
def logout_route():
    return logout()