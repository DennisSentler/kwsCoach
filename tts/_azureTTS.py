from email import header
import os
import json
import requests
from . import myTypes

def _prettyJson(json_string: str):
        json_string = json.loads(json_string)
        json_string = json.dumps(json_string, indent=2)
        return json_string

__subscription_key = None 
__location = None
__service_url = None

def connect() -> bool:
    global __subscription_key
    global __location
    global __service_url
    with open('credentials/azure_key.json', 'r') as f:
                credentials = f.read()
                credentials = json.loads(credentials)
                __subscription_key = credentials["key"]
                __location = credentials["location"]
                __service_url = f"https://{__location}.tts.speech.microsoft.com/cognitiveservices"
                response = requests.post(
                    url=f"https://{__location}.api.cognitive.microsoft.com/sts/v1.0/issueToken", 
                    headers={"Ocp-Apim-Subscription-Key": __subscription_key})
                response.raise_for_status()
    return True

def getVoices() -> list[myTypes.Voice]:
    voices_response = requests.get(
        url=f"{__service_url}/voices/list",
        headers={"Ocp-Apim-Subscription-Key": __subscription_key}
    )
    voices_response.raise_for_status()
    voices = json.loads(voices_response.text)
    generic_voices = []
    for voice in voices:
        generic_voice = myTypes.Voice(
            myTypes.Provider.AZURE, 
            voice["ShortName"], 
            voice["Locale"],
            myTypes.Gender(voice["Gender"].upper())
        )
        generic_voices.append(generic_voice)
    return generic_voices

def synthesizeSpeech(text: str, voice: myTypes.Voice, path: str):
    gender = voice.gender.capitalize()
    req_body = f"""
        <speak version='1.0' xml:lang='{voice.language}'>
        <voice xml:lang='{voice.language}' xml:gender='{gender}' name='{voice.name}'>{text}</voice></speak>"""
    headers = {
                "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
                "Ocp-Apim-Subscription-Key": __subscription_key,
                "Content-Type": "application/ssml+xml",
            }
    response = requests.post(
        url=f"{__service_url}/v1",
        headers=headers,
        data=req_body
        )
    response.raise_for_status()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(response.content)