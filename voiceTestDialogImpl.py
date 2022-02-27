from pydub import AudioSegment
from pydub.playback import play
from PyQt5.QtWidgets import (
    QDialog
)
import tts
from ui.voiceTestDialog import Ui_VoiceTestDialog
from messageBoxImpl import ErrorMessageBox, InfoMessageBox

class VoiceTestDialog(QDialog, Ui_VoiceTestDialog):
    def __init__(self, parent, voice, tts_handler: tts.TTSServiceHandler):
        super().__init__(parent)
        self.setupUi(self)
        self._tts = tts_handler
        self._selected_voice = voice
        self.voice_details_placeholder.setText(str(voice))

    def playVoice(self):
        try:
            text_to_play = self.text_to_play_box.text()
            if len(text_to_play) > 0:
                audio_file = self._tts.synthesizeSpeech(
                    self._selected_voice.provider,
                    text_to_play,
                    self._selected_voice,
                    testonly=True
                )
                speech = AudioSegment.from_wav(audio_file)
                play(speech)
        except Exception:
            ErrorMessageBox(self).exec()
            return

    def synthesizeVoiceAndSaveToFile(self):
        try:
            text_to_play = self.text_to_play_box.text()
            if len(text_to_play) > 0:
                audio_file_dir = self._tts.synthesizeSpeech(
                    self._selected_voice.provider,
                    text_to_play,
                    self._selected_voice,
                    testonly=False
                )
                InfoMessageBox(self, f"Saved file in\r\n{audio_file_dir}").exec()
        except Exception:
            ErrorMessageBox(self).exec()
            return