import sys, os
import boto3
import json
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

from game_functions.point_distribution import point_distribution
from game_functions.getNewPrompt import getNewPrompt

data = [{
    'connection_id': "strin feo", 
    'room_id': "AAAA", 
    'user_name': "Neca", 
    "turn_status": "waiting",
    "points":0,
    "last_turn_points":0,
    },
    {
    'connection_id': "strin feo", 
    'room_id': "AAAA", 
    'user_name': "Bracox", 
    "turn_status": "waiting",
    "points":0,
    "last_turn_points":0,
    "answer": [
        {"user_name": "Bracox"}, 
        {"user_name": "Otro"}]
    },
    {
    'connection_id': "strin feo", 
    'room_id': "AAAA", 
    'user_name': "Otro", 
    "turn_status": "waiting",
    "points":100,
    "last_turn_points":0,
    "answer": [
        {"user_name": "Bracox"}, 
        {"user_name": "Otro"}]
    }
]

my_session = boto3.session.Session(
        aws_access_key_id=os.environ.get("ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("SECRET_KEY"),
        region_name = "us-east-1",
    )

table_name = os.environ['TABLE_NAME']
table = my_session.resource('dynamodb').Table(table_name)

response_data, correct_order = point_distribution(table, data)
prompt = getNewPrompt(0, "AAAA")

message = json.dumps({"round_end": response_data, "new_prompt": prompt, "correct_order": correct_order})
print(message)