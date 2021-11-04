from datetime import datetime
import json
import pytest

from src.app import parse_order, add_order_timestamp, lambda_handler


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{"firstName": "Bruce", "lastName": "Wayne", "phone": "1234567890", "email": "batman@gmail.com", "stockingCount": 2, "pickup": "house", "message": "hello world"}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }


def test_parse_order(apigw_event):

    order = parse_order(apigw_event)

    assert order["firstName"] == 'Bruce'
    assert order['lastName'] == 'Wayne'
    assert order['phone'] == '1234567890'
    assert order['email'] == 'batman@gmail.com'
    assert order['stockingCount'] == 2
    assert order['pickup'] == 'house'
    assert order['message'] == "hello world"

def test_order_ts():
    order = {}
    ts_start = datetime.now()
    add_order_timestamp(order)
    ts_end = datetime.now()
    print(ts_start)
    print(order.get('order_ts'))
    print(ts_end)
    assert order.get('order_ts', None) is not None
    assert ts_start < datetime.strptime(order.get('order_ts', 0), '%Y-%m-%d %H:%M:%S.%f') < ts_end

def test_signup(apigw_event):
    response = lambda_handler(apigw_event, None)
    assert 'body' in response
    body = json.loads(response['body'])
    assert 'message' in body
    assert 'success' == body['message']
