import tts._googleTTS as _googleTTS
from . import myTypes

class TTSServiceHandler():
    def __init__(self) -> None:
        pass

    def connect(self, provider: myTypes.Provider) -> bool:
        switcher = {
            myTypes.Provider.GOOGLE: _googleTTS.connect
        }

        connect = switcher.get(provider, lambda: "Service not found")
        return connect()

    def getVoices(self, provider: myTypes.Provider) -> list[myTypes.Voice]:
        switcher = {
            myTypes.Provider.GOOGLE: _googleTTS.getVoices
        }

        getVoices = switcher.get(provider, lambda: "Service not found")
        return getVoices()

    def synthesizeSpeech(self, provider: myTypes.Provider, text: str, voice: myTypes.Voice) -> bytes:
        switcher = {
            myTypes.Provider.GOOGLE: _googleTTS.synthesizeSpeech
        }

        synthesizeSpeech = switcher.get(provider, lambda: "Service not found")
        return synthesizeSpeech(text, voice)
