from flask import Blueprint
from controllers.menu_controller import home, pet_plan, care_cost_support, about, sign_in

menu_bp = Blueprint('menu', __name__)

# Routes for rendering templates
@menu_bp.route('/')
def home_route():
    return home()

@menu_bp.route('/pet-plan')
def pet_plan_route():
    return pet_plan()

@menu_bp.route('/care_cost_support')
def care_cost_support_route():
    return care_cost_support()

@menu_bp.route('/about')
def about_route():
    return about()

@menu_bp.route('/sign-in')
def sign_in_route():
    return sign_in()