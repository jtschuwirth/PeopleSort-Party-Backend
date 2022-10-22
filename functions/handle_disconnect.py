import json
from botocore.exceptions import ClientError

from functions.handle_ws_message import handle_ws_message
from functions.get_all_recipients import get_all_recipients

def handle_disconnect(table, connection_id, apig_management_client):
    status_code = 200
    try:
        query = table.query(
            KeyConditionExpression = "connection_id = :id",
            ExpressionAttributeValues={
            ":id": { "S": connection_id }
        })
        for i in query["Items"]:
            room_id = i["room_id"]
            table.delete_item(Key={'connection_id': connection_id, 'room_id': room_id})
            recipients = get_all_recipients(table)
            message = json.dumps({"disconnected": connection_id})
            handle_ws_message(table, recipients, message, apig_management_client)
        
    except ClientError:
        status_code = 503
    return status_code
