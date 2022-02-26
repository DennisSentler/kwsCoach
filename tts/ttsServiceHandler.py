import tts._googleTTS as _googleTTS
import tts._watsonTTS as _watsonTTS
import tts._azureTTS as _azureTTS
from . import myTypes

class TTSServiceHandler():
    def __init__(self) -> None:
        pass

    def connect(self, provider: myTypes.Provider) -> bool:
        switcher = {
            myTypes.Provider.GOOGLE: _googleTTS.connect,
            myTypes.Provider.WATSON: _watsonTTS.connect,
            myTypes.Provider.AZURE: _azureTTS.connect,
        }

        connect = switcher.get(provider, lambda: "Service not found")
        return connect()

    def getVoices(self, provider: myTypes.Provider) -> list[myTypes.Voice]:
        switcher = {
            myTypes.Provider.GOOGLE: _googleTTS.getVoices,
            myTypes.Provider.WATSON: _watsonTTS.getVoices,
            myTypes.Provider.AZURE: _azureTTS.getVoices,
        }

        getVoices = switcher.get(provider, lambda: "Service not found")
        return getVoices()

    def synthesizeSpeech(self, provider: myTypes.Provider, text: str, voice: myTypes.Voice, testonly: bool=False) -> str:
        switcher = {
            myTypes.Provider.GOOGLE: _googleTTS.synthesizeSpeech,
            myTypes.Provider.WATSON: _watsonTTS.synthesizeSpeech,
            myTypes.Provider.AZURE: _azureTTS.synthesizeSpeech,
        }
        synthesizeSpeech = switcher.get(provider, lambda: "Service not found")
        if testonly:
            synthesis_path = f".app_cache/{text}_{str(voice)}.wav"
        else:
            synthesis_path = f"synthesis/{text}_{str(voice)}.wav"

        synthesizeSpeech(text, voice, synthesis_path)
        return synthesis_path
