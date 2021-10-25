import boto3
from datetime import datetime
import json
import traceback

ddb = boto3.resource('dynamodb')
table = ddb.Table('stocking-orders')


def lambda_handler(event, context):
    # parse order from event
    order = parse_order(event)
    if order is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Bad attribute"}),
        }

    add_order_timestamp(order)

    # Add entry to table
    table.put_item(
        Item = order
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps({"message": "success"}),
    }


def parse_order(event):
    # check incoming values and create order
    try:
        body = json.loads(event['body'])
        return {
            'firstName': body['firstName'],
            'lastName': body['lastName'],
            'phone': body['phone'],
            'email': body['email'],
            'stockingCount': body['stockingCount'],
            'pickup': body['pickup'],
            'message': body.get('message', '')
        }
    except Exception as e:
        print('Failed to get all required attributes', e)
        print(traceback.format_exc())
        return None

def add_order_timestamp(order):
    order['order_ts'] = str(datetime.now())