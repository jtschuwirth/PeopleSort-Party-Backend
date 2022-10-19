import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_connect(user_name, table, connection_id):
    """
    Handles new connections by adding the connection ID and user name to the
    DynamoDB table.
    :param user_name: The name of the user that started the connection.
    :param table: The DynamoDB connection table.
    :param connection_id: The websocket connection ID of the new connection.
    :return: An HTTP status code that indicates the result of adding the connection
             to the DynamoDB table.
    """
    status_code = 200
    try:
        table.put_item(
            Item={'connection_id': connection_id, 'user_name': user_name, "turn_status": "playing"})
        logger.info(
            "Added connection %s for user %s.", connection_id, user_name)
    except ClientError:
        logger.exception(
            "Couldn't add connection %s for user %s.", connection_id, user_name)
        status_code = 503
    return status_code