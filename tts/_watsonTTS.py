from ibm_watson import TextToSpeechV1
from . import myTypes

__client = None 
try:
    __client = TextToSpeechV1()
except Exception:
    pass


def connect() -> bool:
    global __client
    __client = TextToSpeechV1()
    return True

def getVoices() -> list[myTypes.Voice]:
    global __client
    watson_voices = __client.list_voices().get_result()["voices"]

    generic_voices = []
    for w_voice in watson_voices:
        generic_voice = myTypes.Voice(
            myTypes.Provider.WATSON, 
            w_voice["name"], 
            w_voice["language"], 
            myTypes.Gender.MALE if w_voice["gender"] == 'male' else myTypes.Gender.FEMALE
        )
        generic_voices.append(generic_voice)
    return generic_voices

def synthesizeSpeech(text: str, voice: myTypes.Voice, path: str):
    response = __client.synthesize(text=text, voice=voice.name, accept="audio/wav")
    with open(path, "wb") as f:
                f.write(response.audio_content)