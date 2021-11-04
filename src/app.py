import boto3
from datetime import datetime
import json
import traceback

ddb = boto3.resource('dynamodb')
sns = boto3.client('sns')
table = ddb.Table('stocking-orders')


def lambda_handler(event, context):
    print(event)
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

    resp = pub_to_topic(order)

    print(json.dumps(resp))

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

def pub_to_topic(order):
    # construct message attributes
    msgatt = dict()
    for att in order:
        msgatt[att] = {
            'DataType': 'String',
            'StringValue': str(order[att])
        }

    response = sns.publish(
        TargetArn='arn:aws:sns:us-east-1:943275084484:StockingOrderNotification',
        Message=f'New stokcing order from {order["email"]}',
        Subject='Stocking order submitted',
        MessageAttributes=msgatt
    )

    return response
