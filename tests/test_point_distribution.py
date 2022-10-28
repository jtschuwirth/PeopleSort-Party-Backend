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

data = [{"Item":{
    'connection_id': "strin feo", 
    'room_id': "AAAA", 
    'user_name': "Neca", 
    "turn_status": "waiting",
    "points":0,
    "last_turn_points":0,
    "answer": [
        {"user_name": "Bracox"}, 
        {"user_name": "Neca"}, 
        {"user_name": "Otro"}]
    }},
    {"Item":{
    'connection_id': "strin feo", 
    'room_id': "AAAA", 
    'user_name': "Bracox", 
    "turn_status": "waiting",
    "points":0,
    "last_turn_points":0,
    "answer": [
        {"user_name": "Neca"}, 
        {"user_name": "Bracox"}, 
        {"user_name": "Otro"}]
    }},
    {"Item":{
    'connection_id': "strin feo", 
    'room_id': "AAAA", 
    'user_name': "Otro", 
    "turn_status": "waiting",
    "points":0,
    "last_turn_points":0,
    "answer": [
        {"user_name": "Neca"},
        {"user_name": "Bracox"}, 
        {"user_name": "Otro"}]
    }}
]

response_data, correct_order = point_distribution(data)
prompt = getNewPrompt(0, "AAAA")

message = json.dumps({"round_end": response_data, "new_prompt": prompt, "correct_order": correct_order})
print(message)