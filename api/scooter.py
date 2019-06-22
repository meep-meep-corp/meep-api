
import os
import boto3
from flask import Blueprint, jsonify

app = Blueprint('scooter', __name__, url_prefix='/scooter')
dynamo_client = boto3.client('dynamodb', region_name='eu-central-1')

@app.route('lock/<string:scooter_id>', methods=['POST'])
def enter():
    return 'Scooter locked'

@app.route('unlock/<string:scooter_id>', methods=['POST'])
def exit():
    return 'Scooter unlocked'

@app.route('read', methods=['GET'])
def read():
    return jsonify({'scooters': dynamo_client.scan(TableName='scooter-table')})

