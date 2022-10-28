import sys, os
import boto3
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

from game_functions.getNewPrompt import getNewPrompt

room_id = "AAAA"
index = 0
while index != 5:
    print(getNewPrompt(index, "AAAA"))
    index+=1