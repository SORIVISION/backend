import requests
import os

async def get_tts(context) :
    """
    Input : context (string)
    Output : HTTP response code, mp3 binary data
    """

    speaker = "nara"
    speed = "0"
    pitch = "0"
    emotion = "0"
    format = "mp3"

    val = {
        "speaker": speaker,
        "speed": speed,
        "text": context
    }
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

    headers = {
        "X-NCP-APIGW-API-KEY-ID": os.getenv("CLOVA_TTS_API_ID"),
        "X-NCP-APIGW-API-KEY": os.getenv("CLOVA_TTS_API_KEY"),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=val, headers=headers)
    rescode = response.status_code

    if(rescode == 200):
        return rescode, response.content # binary mp3 response
    else:
        return rescode, None