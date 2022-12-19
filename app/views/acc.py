from flask import Blueprint

acc_bp = Blueprint('acc', __name__)

@acc_bp.route("/acc")
def accfunc():
    return "my_app.acc"

views/acc.py