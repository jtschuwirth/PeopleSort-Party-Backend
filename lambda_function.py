import os, boto3

from handlers.routes import routes
from handlers.handle_connect import handle_connect
from handlers.handle_disconnect import handle_disconnect


def lambda_handler(event, context):
    route_key = event.get('requestContext', {}).get('routeKey')
    connection_id = event.get('requestContext', {}).get('connectionId')
    domain = event.get('requestContext', {}).get('domainName')
    stage = event.get('requestContext', {}).get('stage')

    my_session = boto3.session.Session(
        aws_access_key_id=os.environ.get("ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("SECRET_KEY"),
        region_name = "us-east-1",
    )

    table_name = os.environ['TABLE_NAME']
    table = my_session.resource('dynamodb').Table(table_name)

    response = {'statusCode': 200}

    if table_name is None or route_key is None or connection_id is None:
        return {'statusCode': 400}
    
    if domain is None or stage is None:
        return {'statusCode': 400}

    apig_management_client = my_session.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')


    if route_key == '$connect':
        response['statusCode'] = handle_connect(table, event, connection_id, apig_management_client)
    
    elif route_key == '$disconnect':
        response['statusCode'] = handle_disconnect(table, event, connection_id, apig_management_client)

    else:
        response['statusCode'] = routes(route_key, table, event, connection_id, apig_management_client)

    return response
