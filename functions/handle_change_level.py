import json
from botocore.exceptions import ClientError

from functions.get_all_recipients import get_all_recipients
from functions.handle_ws_message import handle_ws_message
from functions.getNewPrompt import getNewPrompt

def handle_change_level(table, level, connection_id):
    status_code = 200

    try:
        table.update_item(
            Key={'connection_id': connection_id},
            UpdateExpression = "SET lvl = :lvl",
            ExpressionAttributeValues={
                ':lvl': level
        })
        
    except ClientError:
        status_code=503
    

    return status_code