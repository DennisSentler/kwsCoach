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
    global __subscription_key
    global __service_url
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
    input_text = texttospeech.SynthesisInput(text=text)
    voice_config = texttospeech.VoiceSelectionParams(
                language_code=voice.language, name=voice.name
            )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    response = __client.synthesize_speech(input=input_text, voice=voice_config, audio_config=audio_config)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(response.audio_content)