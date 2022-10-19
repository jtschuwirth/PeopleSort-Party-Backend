import json
from botocore.exceptions import ClientError
from decimal import Decimal

from functions.get_all_recipients import get_all_recipients
from functions.handle_ws_message import handle_ws_message

def handle_round_end(table, apig_management_client):

    status_code = 200
    data=[]
    try:
        scan_response = table.scan()
        for item in scan_response['Items']:
            Item={}
            for key, attribute in item.items():
                if isinstance(attribute, Decimal):
                    Item[key] = int(attribute)
                else:
                    Item[key] = attribute
            data.append(Item)

            table.update_item(
                Key={'connection_id': item["connection_id"]},
                UpdateExpression = "SET turn_status = :status",
                ExpressionAttributeValues={
                    ':status': "playing"
        }) 
    except ClientError:
        status_code = 404

    try:
        recipients = get_all_recipients(table)
        message = json.dumps({"turn_stats":data})
        handle_ws_message(table, recipients, message, apig_management_client)
    except ClientError:
        status_code = 503

    return status_code