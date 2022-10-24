import requests

def getNewPrompt(level):
    if not level: level = 1
    response = requests.get(url=f"https://59fxcxkow4.execute-api.us-east-1.amazonaws.com/dev/nuncanunca/phrases?level={level}")
    if response.status_code == 200:
        return response.json()[0]
    else:
        return 0