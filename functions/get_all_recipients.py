

def get_all_recipients(table):
    connection_ids = []
    scan_response = table.scan(ProjectionExpression='connection_id')
    connection_ids = [item['connection_id'] for item in scan_response['Items']]
    
    return connection_ids