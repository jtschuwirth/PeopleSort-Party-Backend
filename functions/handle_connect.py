import json
from botocore.exceptions import ClientError

from functions.handle_ws_message import handle_ws_message
from functions.get_all_recipients import get_all_recipients

def handle_connect(user_name, table, connection_id, apig_management_client):
    status_code = 200
    try:
        table.put_item(Item={'connection_id': connection_id, 'user_name': user_name, "turn_status": "playing"})
        recipients = get_all_recipients(table)
        message = json.dumps({"connected": connection_id, "user_name": user_name})
        handle_ws_message(table, recipients, message, apig_management_client)
    except ClientError:
        status_code = 503
    return status_code