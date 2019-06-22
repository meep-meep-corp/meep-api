
import os
import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, Response, jsonify, request

app = Blueprint('vehicle', __name__, url_prefix='/vehicle')
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table(os.environ['VEHICLE_TABLE'])

@app.route('create/<string:id>', methods=['POST'])
def createVehicle(id):
    response = table.put_item(Item = {'id': id, 'status': 'locked'})
    return 'created'

@app.route('lock/<string:code>', methods=['POST'])
def lock(code):
    try:
        vehicletype, provider, id = code.split(":", 3)
        data = request.get_json(force=True)
        userid = data['user']
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
                return jsonify({'error':'You are not using this vehicle'}), 409
            else:
                # All right, lock the vehicle
                # TODO: Check this using Blockchain
                response = table.update_item(
                    Key={'id': str(id)},
                    UpdateExpression='SET #st = :val',
                    ExpressionAttributeValues={":val": "AVAILABLE"},
                    ExpressionAttributeNames={"#st": "status"},
                    ReturnValues="UPDATED_NEW"
                )
                return jsonify({'message':'Trip finished!'}), 200
        else:
            return jsonify({'error':'You are not using this vehicle'}), 409

@app.route('unlock/<string:code>', methods=['POST'])
def unlock(code):
    try:
        vehicletype, provider, id = code.split(":", 3)
        print(request.get_json(force=True))
        response = table.get_item(
            Key={'id': str(id)}
        )
        print(response)
    except ClientError as e:
        # Vehicle doesn't exist in our database
        return jsonify({'error':'This vehicle cannot be recognized'}), 404
    else:
        # Vehicle found
        vehicle = response['Item']
        # Check the status
        print(vehicle['status'])
        if vehicle['status'] != 'AVAILABLE':
            # Vehicle is not available for use
            return jsonify({'error':'This vehicle is not available to use'}), 409
        else:
            # Vehicle can be used. Call provider's api to check the status
            # (Mocked response from provider)
            # TODO: Check this using Blockchain
            providerResponse = {'id': id, 'status': 'AVAILABLE'}
            if providerResponse['status'] != 'AVAILABLE':
                return jsonify({'error':'This vehicle is not available to use'}), 409
            else:
                response = table.update_item(
                    Key={'id': str(id)},
                    UpdateExpression='SET #st = :val',
                    ExpressionAttributeValues={":val": "LOCKED"},
                    ExpressionAttributeNames={"#st": "status"},
                    ReturnValues="UPDATED_NEW"
                )
                return jsonify({'message':'Vehicle unlocked, enjoy your trip!'}), 200

