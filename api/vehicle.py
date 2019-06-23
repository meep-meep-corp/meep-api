
import os
import boto3
import requests
import time
import json
from botocore.exceptions import ClientError
from flask import Blueprint, Response, jsonify, request
from utils import distanceInKmBetweenCoordinates, carbonFootprint, costOfTransport

app = Blueprint('vehicle', __name__, url_prefix='/vehicle')
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
vehicleTable = dynamodb.Table(os.environ['VEHICLE_TABLE'])
tripTable = dynamodb.Table(os.environ['TRIP_TABLE'])

@app.route('lock/<string:code>', methods=['POST'])
def lock(code):
    try:
        vehicletype, provider, id = code.split(":", 3)
        data = request.get_json(force=True)
        userid = data['user']
        response = vehicleTable.get_item(Key = {'id': id})
    except ClientError as e:
        # Vehicle doesn't exist in our database
        return jsonify({'error':'This vehicle cannot be recognized'}), 404
    else:
        # Vehicle found
        vehicle = response['Item']
        # Check the status
        if vehicle['status'] == 'LOCKED':
            # Vehicle is not locked, lock the vehicle and register the operation in the blockchain
            requests.post(os.environ['BLOCKCHAIN_URL'], json=json.dumps({
                "donorUserName": time.time(),
                "vehicle": {
                    "id": id, 
                    "type": vehicle['type']
                },
                "coords": vehicle['location'],
                "time": int(time.time()),
                "user": userid,
                "provider": provider}), headers={'content-type': 'application/json'})
            
            response = vehicleTable.update_item(
                Key={'id': str(id)},
                UpdateExpression='SET #st = :val, #us = :user',
                ExpressionAttributeValues={":val": "AVAILABLE", ":user": userid},
                ExpressionAttributeNames={"#st": "status", "#us": "user"},
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
        response = vehicleTable.get_item(
            Key={'id': str(id)}
        )
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
            # Call blockchain to register the operation
            requests.post(os.environ['BLOCKCHAIN_URL'], json=json.dumps({
                "donorUserName": time.time(),
                "vehicle": {
                    "id": id, 
                    "type": vehicle['type']
                },
                "coords": vehicle['location'],
                "time": int(time.time()),
                "user": userid,
                "provider": provider}), headers={'content-type': 'application/json'})

            providerResponse = {'id': id, 'status': 'AVAILABLE'}
            if providerResponse['status'] != 'AVAILABLE':
                return jsonify({'error':'This vehicle is not available to use'}), 409
            else:
                response = vehicleTable.update_item(
                    Key={'id': str(id)},
                    UpdateExpression='SET #st = :val',
                    ExpressionAttributeValues={":val": "LOCKED"},
                    ExpressionAttributeNames={"#st": "status"},
                    ReturnValues="UPDATED_NEW"
                )
                return jsonify({'message':'Vehicle unlocked, enjoy your trip!'}), 200

def createTrip(id, user, startCoords, endCoords, startTime, endTime, vehicleType):
    data = request.get_json(force=True)

    distance = distanceInKmBetweenCoordinates(startCoords, endCoords)
    cost = costOfTransport(distance, minutes, vehicleType)
    carbon = carbonFootprint(distance, vehicleType)
    score = (distance / carbon) * 1000

    response = tripTable.put_item(
        Item={
            'id': id,
            'carbon': carbon,
            'cost': cost,
            'distance': distance,
            'score': score,
            'tripUser': user,
            'endCoords': endCoords,
            'startCoords': startCoords,
            'endTime': endCoords,
            'startTime': startTime
        }
    )

