
import os
import boto3
from flask import Blueprint, jsonify

app = Blueprint('train', __name__, url_prefix='/train')
dynamo_client = boto3.client('dynamodb', region_name='eu-central-1')

@app.route('enter/<string:train_id>', methods=['POST'])
def enter():
    return 'You are in!'

@app.route('exit/<string:train_id>', methods=['POST'])
def exit():
    return 'Trip recorded'

@app.route('read', methods=['GET'])
def read():
    return jsonify({'trains': dynamo_client.scan(TableName='train-table')})
