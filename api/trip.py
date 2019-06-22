
import os
import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, Response, jsonify, request

app = Blueprint('trip', __name__, url_prefix='/trip')
# dbclient = boto3.client('dynamodb', region_name='eu-central-1')
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table(os.environ['TRIP_TABLE'])
TRIP_TABLE = os.environ['TRIP_TABLE']

@app.route('total/<string:userid>', methods=['GET'])
def total(userid):
    response = table.get_item(
        Key={'user': str(userid)}
    )
    print(response)
    return response

@app.route('create', methods=['POST'])
def create():
    data = request.get_json(force=True)
    response = table.put_item(
        Item={
            'id': '1234',
            'year': 2012,
            'title': 'title',
            'info': {
                'plot':"Nothing happens at all.",
                'rating': 123
            }
        }
    )