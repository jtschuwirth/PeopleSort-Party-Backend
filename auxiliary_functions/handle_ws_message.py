import json
from botocore.exceptions import ClientError

def handle_ws_message(table, recipients, message, apig_management_client):
    status_code = 200
    for connection in recipients:
        try:
            apig_management_client.post_to_connection(Data=message, ConnectionId=connection)
        except ClientError:
            print("Couldn't post connection")
        except apig_management_client.exceptions.GoneException:
            try:
                table.delete_item(Key={'connection_id': connection})
                message = json.dumps({"disconnected": connection})
                apig_management_client.post_to_connection(Data=message, ConnectionId=connection)
            except ClientError:
                print("Failed to disconnect connection")


    return status_code