import requests
import random

level=random.randint(1,3)
prompt = requests.get(url=f"https://59fxcxkow4.execute-api.us-east-1.amazonaws.com/dev/nuncanunca/phrases?level={level}")

print(prompt.json()[0]["phrase"])
