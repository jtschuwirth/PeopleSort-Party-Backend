import json
import logging
from botocore.exceptions import ClientError

from functions.get_all_recipients import get_all_recipients

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_ws_message(table, recipients, message, apig_management_client):
    status_code = 200
    for connection in recipients:
        try:
            apig_management_client.post_to_connection(Data=message, ConnectionId=connection)
        except ClientError:
            logger.exception("Couldn't post to connection %s.", connection)
        except apig_management_client.exceptions.GoneException:
            logger.info("Connection %s is gone, removing.", connection)
            try:
                table.delete_item(Key={'connection_id': connection})
                recipients = get_all_recipients(table)
                message = json.dumps({"disconnected": connection})
                apig_management_client.post_to_connection(Data=message, ConnectionId=connection)
            except ClientError:
                logger.exception("Couldn't remove connection %s.", connection)

    return status_code