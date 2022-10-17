import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_message(table, connection_id, event_body, apig_management_client):
    """
    Handles messages sent by a participant in the chat. Looks up all connections
    currently tracked in the DynamoDB table, and uses the API Gateway Management API
    to post the message to each other connection.
    When posting to a connection results in a GoneException, the connection is
    considered disconnected and is removed from the table. This is necessary
    because disconnect messages are not always sent when a client disconnects.
    :param table: The DynamoDB connection table.
    :param connection_id: The ID of the connection that sent the message.
    :param event_body: The body of the message sent from API Gateway. This is a
                       dict with a `msg` field that contains the message to send.
    :param apig_management_client: A Boto3 API Gateway Management API client.
    :return: An HTTP status code that indicates the result of posting the message
             to all active connections.
    """
    status_code = 200
    user_name = 'guest'
    try:
        item_response = table.get_item(Key={'connection_id': connection_id})
        user_name = item_response['Item']['user_name']
        logger.info("Got user name %s.", user_name)
    except ClientError:
        logger.exception("Couldn't find user name. Using %s.", user_name)

    connection_ids = []
    try:
        scan_response = table.scan(ProjectionExpression='connection_id')
        connection_ids = [item['connection_id'] for item in scan_response['Items']]
        logger.info("Found %s active connections.", len(connection_ids))
    except ClientError:
        logger.exception("Couldn't get connections.")
        status_code = 404

    message = f"{user_name}: {event_body['msg']}".encode('utf-8')
    logger.info("Message: %s", message)

    for other_conn_id in connection_ids:
        try:
            if other_conn_id != connection_id:
                send_response = apig_management_client.post_to_connection(
                    Data=message, ConnectionId=other_conn_id)
                logger.info(
                    "Posted message to connection %s, got response %s.",
                    other_conn_id, send_response)
        except ClientError:
            logger.exception("Couldn't post to connection %s.", other_conn_id)
        except apig_management_client.exceptions.GoneException:
            logger.info("Connection %s is gone, removing.", other_conn_id)
            try:
                table.delete_item(Key={'connection_id': other_conn_id})
            except ClientError:
                logger.exception("Couldn't remove connection %s.", other_conn_id)

    return status_code