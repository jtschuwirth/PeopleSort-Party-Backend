import json

from decimal import Decimal
from game_functions.getNewPrompt import getNewPrompt
from game_functions.point_distribution import point_distribution

from auxiliary_functions.get_all_recipients import get_all_recipients
from auxiliary_functions.handle_ws_message import handle_ws_message


def round_end(table, room_id, apig_management_client):

    status_code = 200
    data=[]
    index = 0
    try:
        scan_response = table.scan(
            FilterExpression="room_id = :id",
            ExpressionAttributeValues={
                ":id": room_id   
        })
        for item in scan_response['Items']:
            if item["turn_status"] == "hosting":
                index = int(item["current_index"])
                table.update_item(
                    Key={'connection_id': item["connection_id"]},
                    UpdateExpression = f"ADD current_index :v",
                    ExpressionAttributeValues={
                        ':v': 1
                })
                continue

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
    except:
        return 404

    response_data, correct_order = point_distribution(table, data)
    prompt = getNewPrompt(index, room_id)

    try:
        recipients = get_all_recipients(table, room_id)
        message = json.dumps({"round_end": response_data, "new_prompt": prompt, "correct_order": correct_order})
        handle_ws_message(table, recipients, message, apig_management_client)
    except:
        status_code = 503

    return status_code