import requests

def getNewPrompt(level):
    response = requests.get(url=f"https://59fxcxkow4.execute-api.us-east-1.amazonaws.com/dev/nuncanunca/phrases?level={level}")
    return response.json()[0]
