
import os
import boto3
from flask import Blueprint, jsonify

app = Blueprint('scooter', __name__, url_prefix='/scooter')
dynamo_client = boto3.client('dynamodb', region_name='eu-central-1')
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table(os.environ['SCOOTERS_TABLE'])

@app.route('lock/<string:scooter_id>', methods=['POST'])
def lock(scooter_id):
    try:
        response = table.get_item(
            Key = {'scooterId': scooter_id}
    )
    except ClientError as e:
        # Scooter doesn't exist in our database, add it
        response = table.put_item(Item = {'scooterId': scooter_id, 'status': 'locked'})
    else:
        # Scooter already in the database
        scooter = response['Item']
        # Check the status
        if scooter['status'] == 'lock':
            # Scooter is already in use by another user

        else:
            # Scooter is free




    

    return jsonify(response)

@app.route('unlock/<string:scooter_id>', methods=['POST'])
def unlock():
    return 'Scooter unlocked'

@app.route('read', methods=['GET'])
def read():
    return jsonify({'scooters': dynamo_client.scan(TableName=os.environ['SCOOTERS_TABLE'])})

