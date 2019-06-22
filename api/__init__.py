
from flask import Flask
from api import train, scooter

def create_app():
    app = Flask(__name__)
    app.register_blueprint(train.app)
    app.register_blueprint(scooter.app)
    # app.register_error_handler(Exception, handle_error)
    return app

def handle_error(e):
    return 'error'
