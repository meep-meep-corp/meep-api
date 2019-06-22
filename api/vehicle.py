
import os
import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, Response, jsonify, request

app = Blueprint('vehicle', __name__, url_prefix='/vehicle')
dbclient = boto3.client('dynamodb', region_name='eu-central-1')
# dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
# table = dynamodb.Table(os.environ['VEHICLE_TABLE'])
VEHICLE_TABLE = os.environ['VEHICLE_TABLE']

@app.route('create/<string:id>', methods=['POST'])
def createVehicle(id):
    response = table.put_item(Item = {'id': id, 'status': 'locked'})
    return 'created'

@app.route('lock/<string:code>', methods=['POST'])
def lock(code):
    try:
        vehicletype, provider, id = code.split(":", 3)
        print(vehicletype)
        print(provider)
        print(id)
        print(request.get_json(force=True))
        response = dbclient.get_item(TableName=VEHICLE_TABLE, Key={'id': id})
    except ClientError as e:
        # Vehicle doesn't exist in our database
        return jsonify({'error':'This vehicle cannot be recognized'}), 404
    else:
        # Vehicle found
        vehicle = response['Item']
        # Check the status
        if vehicle['status'] != 'AVAILABLE':
            # Vehicle is not available for use
            return jsonify({'error':'This vehicle is not available to use'}), 409
        else:
            # Vehicle can be rent. Call provider's api to check the status
            # (Mocked response from provider)
            response = {'id': id, 'status': 'AVAILABLE'}
            if response['status'] != 'AVAILABLE':
                return jsonify({'error':'This vehicle is not available to use'}), 409
            else:
                return jsonify({'message':'Vehicle unlocked, enjoy your trip!'}), 200

    return jsonify({'message':'Vehicle unlocked, enjoy your trip!'}), 400

@app.route('unlock/<string:id>', methods=['POST'])
def unlock(id):
    try:
        response = table.get_item(Key = {'id': id})
    except ClientError as e:
        # Vehicle doesn't exist in our database
        return jsonify({'error':'This vehicle cannot be recognized'}), 404
    else:
        # Vehicle found
        vehicle = response['Item']
        # Check the status
        if vehicle['status'] != 'LOCKED':
            # Vehicle is not locked
            if (vehicle['user'] != userid):
                # Vehicle is not being currently used by this user
                return 0
            else:
                # All right, lock the vehicle
                return 0
        else:

            return 0


@app.route('test', methods=['GET'])
def test():
    return jsonify({'scooters': dbclient.scan(VEHICLE_TABLE)})

