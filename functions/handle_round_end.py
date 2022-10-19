import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle_round_end(table, apig_management_client):

    status_code = 200
    connection_ids = []
    data=[]
    try:
        scan_response = table.scan()
        for item in scan_response['Items']:
            connection_ids.append(item['connection_id'])
            data.append(item)

            table.update_item(
                Key={'connection_id': item["connection_id"]},
                UpdateExpression = "SET turn_status = :status",
                ExpressionAttributeValues={
                    ':status': "playing"
        }) 
        logger.info("Found %s active connections.", len(connection_ids))
    except ClientError:
        logger.exception("Couldn't get connections.")
        status_code = 404

    message = "Round Ended"
    logger.info("Message: %s", message)

    for other_conn_id in connection_ids:
        try:
            send_response = apig_management_client.post_to_connection(
                Data=message, ConnectionId=other_conn_id)
            logger.info(
                "Posted message to connection %s, got response %s.",
                other_conn_id, send_response)
        except ClientError:
            logger.exception("Couldn't post to connection %s.", other_conn_id)
        except apig_management_client.exceptions.GoneException:
            logger.info("Connection %s is gone, removing.", other_conn_id)
            try:
                table.delete_item(Key={'connection_id': other_conn_id})
            except ClientError:
                logger.exception("Couldn't remove connection %s.", other_conn_id)

    return status_code