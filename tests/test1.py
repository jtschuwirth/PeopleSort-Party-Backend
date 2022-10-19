import json
import os
import boto3
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

my_session = boto3.session.Session(
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_KEY"),
    region_name = "us-east-1",
)
table_name = os.environ['TABLE_NAME']
table = my_session.resource('dynamodb').Table(table_name)

data=[]
scan_response = table.scan()
for item in scan_response['Items']:
    Item={}
    for key, attribute in item.items():
        if isinstance(attribute, Decimal):
            Item[key] = int(attribute)
        else:
            Item[key] = attribute
    data.append(Item)

print(json.dumps(data))