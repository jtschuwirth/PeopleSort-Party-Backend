import json
from botocore.exceptions import ClientError
from decimal import Decimal

from functions.get_all_recipients import get_all_recipients
from functions.handle_ws_message import handle_ws_message
from functions.getNewPrompt import getNewPrompt

def handle_round_end(table, room_id, apig_management_client):

    status_code = 200
    data=[]
    total_answer=0
    try:
        scan_response = table.scan(
            FilterExpression="room_id = :id",
            ExpressionAttributeValues={
                ":id": room_id   
        })
        for item in scan_response['Items']:
            if item["turn_status"] == "hosting": 
                continue
            Item={}
            for key, attribute in item.items():
                if isinstance(attribute, Decimal):
                    Item[key] = int(attribute)
                    if key == "answer":
                        total_answer+=Item[key]
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
        return 404

    response_data=[]
    for item in data:
        points=0
        if item["guess"] == total_answer:
            points=100
        elif item["guess"] == total_answer+1 or item["guess"] == total_answer-1:
            points=50
        table.update_item(
            Key={'connection_id': item["connection_id"]},
            UpdateExpression = "ADD points :p",
            ExpressionAttributeValues={
                ':p': points
        })

        if not "points" in item:
            item["last_turn_points"] = 0
            item["points"] = points
        else:
            item["last_turn_points"] = item["points"]
            item["points"]+= points

        response_data.append(item)
    try:
        prompt = getNewPrompt()
        recipients = get_all_recipients(table, room_id)
        message = json.dumps({"round_end": response_data, "new_prompt": prompt})
        handle_ws_message(table, recipients, message, apig_management_client)
    except ClientError:
        status_code = 503

    return status_code