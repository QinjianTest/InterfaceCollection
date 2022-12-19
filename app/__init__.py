from flask import Flask
from .views.acc import acc_bp
from .views.user import user_bp

def create_app():
    my_app = Flask(__name__)
    my_app.register_blueprint(acc_bp)
    my_app.register_blueprint(user_bp)

    return my_app

app/__init__.py