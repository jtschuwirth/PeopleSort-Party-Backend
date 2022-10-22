from botocore.exceptions import ClientError

from functions.get_all_recipients import get_all_recipients
from functions.handle_ws_message import handle_ws_message

def handle_message(table, connection_id, event_body, apig_management_client):
    status_code = 200
    user_name = 'guest'
    try:
        item_response = table.get_item(Key={'connection_id': connection_id})
        user_name = item_response['Item']['user_name']
        room_id = item_response["Item"]["room_id"]
        
        recipients = get_all_recipients(table, room_id)
        message = f"{user_name}: {event_body['msg']}".encode('utf-8')
        handle_ws_message(table, recipients, message, apig_management_client)
    except ClientError:
        status_code=503

    return status_code