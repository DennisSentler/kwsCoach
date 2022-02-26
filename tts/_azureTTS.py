# import azure.cognitiveservices.speech as speechsdk
# import json
# from . import myTypes


# __config = None 

# def connect() -> bool:
#     global __client
#     key = ""
#     location = ""
#     with open('credentials/azure_key.json', 'r') as f:
#                 credentials = f.read()
#                 credentials = json.loads(credentials)
#                 key = credentials["key"]
#                 location = credentials["location"]
    
#     __config = speechsdk.SpeechConfig(subscription=key, region=location)
#     return True

# def getVoices() -> list[myTypes.Voice]:
#     global __client
#     google_voices = __client.list_voices().voices

#     generic_voices = []
#     for g_voice in google_voices:
#         generic_voice = myTypes.Voice(
#             myTypes.Provider.GOOGLE, 
#             g_voice.name, 
#             g_voice.language_codes[0], 
#             myTypes.Gender.MALE if g_voice.ssml_gender.name == 'MALE' else myTypes.Gender.FEMALE
#         )
#         generic_voices.append(generic_voice)
#     return generic_voices

# def synthesizeSpeech(text: str, voice: myTypes.Voice, path: str):
#     input_text = texttospeech.SynthesisInput(text=text)
#     voice_config = texttospeech.VoiceSelectionParams(
#                 language_code=voice.language, name=voice.name
#             )
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.LINEAR16
#     )
#     response = __client.synthesize_speech(input=input_text, voice=voice_config, audio_config=audio_config)
#     with open(path, "wb") as f:
#                 f.write(response.audio_content)