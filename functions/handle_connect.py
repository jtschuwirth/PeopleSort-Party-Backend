import json
from botocore.exceptions import ClientError

from functions.handle_ws_message import handle_ws_message
from functions.get_all_recipients import get_all_recipients

def handle_connect(user_name, table, connection_id, apig_management_client, is_host, room_id):
    status_code = 200
    turn_status = "waiting"
    if is_host: turn_status="hosting"
    try:
        table.put_item(Item={
            'connection_id': connection_id, 
            'room_id': room_id, 
            'user_name': user_name, 
            "turn_status": turn_status,
            "points":0,
            "lvl":1
        })
        recipients = get_all_recipients(table, room_id)
        message = json.dumps({"new_connection":{"id": connection_id, "user_name": user_name, "points":0}})
        handle_ws_message(table, recipients, message, apig_management_client)
    except ClientError:
        status_code = 503
    return status_code