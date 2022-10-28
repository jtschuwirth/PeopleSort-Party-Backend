import sys, os
import boto3
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

from handlers.round_end import round_end

my_session = boto3.session.Session(
        aws_access_key_id=os.environ.get("ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("SECRET_KEY"),
        region_name = "us-east-1",
    )

table_name = os.environ['TABLE_NAME']
table = my_session.resource('dynamodb').Table(table_name)

print(round_end(table, "UFDD", ""))