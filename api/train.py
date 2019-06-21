
from flask import Blueprint

app = Blueprint('train', __name__, url_prefix='/train')


@app.route('enter', methods=['POST'])
def enter():
    return 'You are in!'

@app.route('exit', methods=['POST'])
def exit():
    return 'Trip recorded'