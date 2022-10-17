import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_disconnect(table, connection_id):
    """
    Handles disconnections by removing the connection record from the DynamoDB table.
    :param table: The DynamoDB connection table.
    :param connection_id: The websocket connection ID of the connection to remove.
    :return: An HTTP status code that indicates the result of removing the connection
             from the DynamoDB table.
    """
    status_code = 200
    try:
        table.delete_item(Key={'connection_id': connection_id})
        logger.info("Disconnected connection %s.", connection_id)
    except ClientError:
        logger.exception("Couldn't disconnect connection %s.", connection_id)
        status_code = 503
    return status_code