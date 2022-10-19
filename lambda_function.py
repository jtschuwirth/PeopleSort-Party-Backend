
import os
import boto3
import logging
import json

from functions.handle_connect import handle_connect
from functions.handle_disconnect import handle_disconnect
from functions.handle_message import handle_message
from functions.check_if_all_passed import check_if_all_passed
from functions.handle_turn_end import handle_turn_end
from functions.handle_round_end import handle_round_end

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
    response = {'statusCode': 200}

    domain = event.get('requestContext', {}).get('domainName')
    stage = event.get('requestContext', {}).get('stage')
    if domain is None or stage is None:
        response['statusCode'] = 400
        return response
    else:
        apig_management_client = my_session.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')

    if route_key == '$connect':
        user_name = event.get('queryStringParameters', {'name': 'guest'}).get('name')
        is_host = event.get('queryStringParameters', {'host': 0}).get("host")
        response['statusCode'] = handle_connect(user_name, table, connection_id, apig_management_client, is_host)
    
    elif route_key == '$disconnect':
        response['statusCode'] = handle_disconnect(table, connection_id, apig_management_client)

    elif route_key == 'sendmessage':
        body = event.get('body')
        body = json.loads(body if "msg" in body  else '{"msg": ""}')
        response['statusCode'] = handle_message(table, connection_id, body, apig_management_client)
    
    elif route_key == "endturn":
        body = event.get('body')
        body = json.loads(body)

        table.update_item(
            Key={'connection_id': connection_id},
            UpdateExpression = "SET turn_status = :status",
            ExpressionAttributeValues={
                ':status': "done"
        })

        table.update_item(
            Key={'connection_id': connection_id},
            UpdateExpression = "SET answer = :answer",
            ExpressionAttributeValues={
                ':answer': body["answer"]
        }) 

        table.update_item(
            Key={'connection_id': connection_id},
            UpdateExpression = "SET guess = :guess",
            ExpressionAttributeValues={
                ':guess': body["guess"]
        }) 
        if check_if_all_passed(table):
            response["statusCode"]=handle_round_end(table, apig_management_client)
        else:
            response["statusCode"]=handle_turn_end(table, connection_id, apig_management_client)

    else:
        response['statusCode'] = 404

    return response