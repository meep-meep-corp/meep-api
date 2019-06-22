
from flask import Flask
from api import vehicle, trip
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(vehicle.app)
    app.register_blueprint(trip.app)
    # app.register_error_handler(Exception, handle_error)
    return app

def handle_error(e):
    return 'error'
