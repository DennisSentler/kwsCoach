# system modules
import sys
# foreign modules
import qdarkstyle
from pydub import AudioSegment
from pydub.playback import play
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog
)
# qt designer modules
from ui.voiceTestDialog import Ui_VoiceTestDialog
from ui.mainWindow import Ui_myApp
# own modules
from tts.myTypes import Provider
from voiceListViewImpl import VoiceListView
from messageBoxImpl import ErrorMessageBox, InfoMessageBox
from connectProviderDialogImpl import (
    ConnectGoogleDialog, ConnectWatsonDialog, ConnectAzureDialog
)
import tts

class MyApp(QMainWindow, Ui_myApp):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #create voice list view
        self.voice_list_view = VoiceListView(parent=self)
        self.voice_list_view.setObjectName("voice_list_view")
        self.gridLayout_4.addWidget(self.voice_list_view, 1, 0, 1, 5)

        # create tts service handler
        self._voices = []
        self._tts = tts.TTSServiceHandler()
        
    def openConnectGoogleDialog(self):
        diag = ConnectGoogleDialog(self, self._tts)
        if diag.exec_():
            self._voices.extend(diag.voices)
            self.voice_list_view.addVoices(diag.voices)

    def openConnectWatsonDialog(self):
        diag = ConnectWatsonDialog(self, self._tts)
        if diag.exec_():
            self._voices.extend(diag.voices)
            self.voice_list_view.addVoices(diag.voices)

    def openConnectAzureDialog(self):
        diag = ConnectAzureDialog(self, self._tts)
        if diag.exec_():
            self._voices.extend(diag.voices)
            self.voice_list_view.addVoices(diag.voices)

    def openVoiceTestDialog(self, voice):
        print("open voice test for", str(voice))
        dialog = VoiceTestDialog(self, voice, self._tts)
        dialog.exec()

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
                    Provider.GOOGLE,
                    text_to_play,
                    self._selected_voice,
                    testonly=True
                )
                speech = AudioSegment.from_wav(audio_file)
                play(speech)
        except Exception:
            ErrorMessageBox(self).exec()
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    win = MyApp()
    win.show()
    sys.exit(app.exec())
