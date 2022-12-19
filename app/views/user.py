from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route("/login")
def user_login():
    return "my_app.user"

views/user.py