
from flask import Blueprint

app = Blueprint('scooter', __name__, url_prefix='/scooter')


@app.route('lock', methods=['POST'])
def enter():
    return 'Scooter locked'

@app.route('unlock', methods=['POST'])
def exit():
    return 'Scooter unlocked'