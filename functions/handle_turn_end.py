import json
from botocore.exceptions import ClientError

from functions.get_all_recipients import get_all_recipients
from functions.handle_ws_message import handle_ws_message

def handle_turn_end(table, connection_id, apig_management_client):
    status_code = 200

    try:
        item_response = table.get_item(Key={'connection_id': connection_id})
        user_name = item_response['Item']['user_name']

        recipients = get_all_recipients(table)
        message = json.dumps({"ended_turn":{"id": connection_id, "user_name": user_name}})
        handle_ws_message(table, recipients, message, apig_management_client)
    except ClientError:
        status_code=503

    return status_code