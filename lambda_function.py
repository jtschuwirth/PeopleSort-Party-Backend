
import os
import boto3
import logging
import json

from functions.handle_connect import handle_connect
from functions.handle_disconnect import handle_disconnect
from functions.handle_message import handle_message

my_session = boto3.session.Session(
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_KEY"),
    region_name = "us-east-1",
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    route_key = event.get('requestContext', {}).get('routeKey')
    connection_id = event.get('requestContext', {}).get('connectionId')

    if table_name is None or route_key is None or connection_id is None:
        return {'statusCode': 400}
    
    table = my_session.resource('dynamodb').Table(table_name)
    logger.info("Request: %s, use table %s.", route_key, table.name)

    response = {'statusCode': 200}
    if route_key == '$connect':
        user_name = event.get('queryStringParameters', {'name': 'guest'}).get('name')
        response['statusCode'] = handle_connect(user_name, table, connection_id)
    elif route_key == '$disconnect':
        response['statusCode'] = handle_disconnect(table, connection_id)
    elif route_key == 'sendmessage':
        body = event.get('body')
        body = json.loads(body if body is not None else '{"msg": ""}')
        domain = event.get('requestContext', {}).get('domainName')
        stage = event.get('requestContext', {}).get('stage')
        if domain is None or stage is None:
            logger.warning(
                "Couldn't send message. Bad endpoint in request: domain '%s', "
                "stage '%s'", domain, stage)
            response['statusCode'] = 400
        else:
            apig_management_client = my_session.client(
                'apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')
            response['statusCode'] = handle_message(table, connection_id, body, apig_management_client)
    else:
        response['statusCode'] = 404

    return response