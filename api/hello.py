
from flask import Blueprint

app = Blueprint('hello', __name__, url_prefix='/hello')


@app.route('', methods=['GET'])
def get_deposits():
    return 'hi there!'
