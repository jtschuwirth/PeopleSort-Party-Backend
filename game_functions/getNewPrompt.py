import requests

def getNewPrompt(index, room_id):
    maximum_recon_tries = 3
    reconnection_tries = 0

    while reconnection_tries < maximum_recon_tries:
        try:
            response = requests.get(url=f"https://59fxcxkow4.execute-api.us-east-1.amazonaws.com/dev/peoplesort/phrases/room?index={index}&room_id={room_id}")
            
            if response.status_code == 200:
                prompt = response.json()[0]
            else:
                prompt = 0

            if prompt["max"]:
                break
            else:
                prompt = 0
        except:
            prompt = 0
        reconnection_tries+=1

    if not prompt:
        prompt = {"max": "Error fetching prompt", "min":""}
    
    return prompt
