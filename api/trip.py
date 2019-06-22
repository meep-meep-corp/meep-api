
import os
import boto3
import decimal
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from flask import Blueprint, Response, jsonify, request

app = Blueprint('trip', __name__, url_prefix='/trip')
# dbclient = boto3.client('dynamodb', region_name='eu-central-1')
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table(os.environ['TRIP_TABLE'])
userTable = dynamodb.Table(os.environ['USER_TABLE'])
TRIP_TABLE = os.environ['TRIP_TABLE']

@app.route('total/<string:userid>', methods=['GET'])
def total(userid):
    response = table.query(
        IndexName="gsi-UserTrips",
        KeyConditionExpression=Key('tripUserId').eq(str(userid))
    )

    totalKm = 0
    totalCost = 0
    totalCarbon = 0
    totalScore = 0
    print(response)
    for trip in response['Items']:
        print(trip)
        if 'distance' in trip:
            totalKm += trip['distance']
        if 'cost' in trip:
            totalCost += trip['cost']
        if 'carbon' in trip:
            totalCarbon += trip['carbon']
        if 'score' in trip:
            totalScore += trip['score']

    return json.dumps({'carbon': totalCarbon, 'cost': totalCost, 'distance': totalKm, 'score': totalScore}, cls=DecimalEncoder), 200

@app.route('ranking', methods=['GET'])
def ranking():
    response = table.scan()
    result = dict()

    print(response)
    for trip in response['Items']:
        print(trip)
        if 'tripUserId' in trip:
            response = userTable.get_item(Key = {'id': trip['tripUserId']})
            print(response)
            user = response['Item']['name']
            if user in result:
                result[user] += trip['score']
            else:
                result[user] = trip['score']

    return json.dumps({'ranking': list(result.items())}, cls=DecimalEncoder), 200

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

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)