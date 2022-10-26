def get_all_recipients(table, room_id):
    connection_ids = []
    scan_response = table.scan(
        ProjectionExpression='connection_id',
        FilterExpression="room_id = :id",
        ExpressionAttributeValues={
            ":id": room_id   
        })
    connection_ids = [item['connection_id'] for item in scan_response['Items']]
    
    return connection_ids