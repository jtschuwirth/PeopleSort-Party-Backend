import requests

def getNewPrompt():
    response = requests.get(url="https://59fxcxkow4.execute-api.us-east-1.amazonaws.com/dev/nuncanunca/phrases")
    return response.json()[0]
