from google.cloud import texttospeech
from lib.baseTTS import Voice, Gender, TTSProvider

class GoogleTTS(TTSProvider):
    def __init__(self):
        self.__client = None 
        try:
            self.connect()
        except Exception:
            pass

    def connect(self) -> bool:
        self.__client = texttospeech.TextToSpeechClient()

    def getVoices(self) -> list:
        google_voices = self.__client.list_voices().voices

        generic_voices = []
        for g_voice in google_voices:
            generic_voice = Voice(
                self.__class__.__name__, 
                g_voice.name, 
                list(g_voice.language_codes), 
                Gender.MALE if g_voice.ssml_gender.name == 'MALE' else Gender.FEMALE
            )
            generic_voices.append(generic_voice)
        return generic_voices