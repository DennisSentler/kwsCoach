import sys
import qdarkstyle
import traceback
from os import environ
from pydub import AudioSegment
from pydub.playback import play

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QMessageBox
)
from tts.myTypes import Provider
from ui.mainWindow import Ui_myApp
from ui.connectProviderDialog import Ui_ConnectProviderDialog
from ui.voiceTestDialog import Ui_VoiceTestDialog
from voiceListView import VoiceListView
import tts

class Window(QMainWindow, Ui_myApp):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #create voice list view
        self.voice_list_view = VoiceListView(self)
        self.voice_list_view.setObjectName("voice_list_view")
        self.gridLayout_4.addWidget(self.voice_list_view, 1, 0, 1, 1)

        # create tts service handler
        self._voices = []
        self._tts = tts.TTSServiceHandler()
        
    def openConnectGoogleDialog(self):
        diag = ConnectGoogleDialog(self, self._tts)
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
        text_to_play = self.text_to_play_box.text()
        audio = self._tts.synthesizeSpeech(
            Provider.GOOGLE,
            text_to_play,
            self._selected_voice,
            testonly=True
        )
        speech = AudioSegment.from_wav(audio)
        play(speech)



class ConnectGoogleDialog(QDialog, Ui_ConnectProviderDialog):
    def __init__(self, parent, tts_handler: tts.TTSServiceHandler):
        super().__init__(parent)
        self.setupUi(self)
        self.voices = []
        self._tts = tts_handler
        self.provider_label_placeholder.setText("Google Cloud TTS")
        help_link = "http://example.com/"
        self.help_link_placeholder.setText(f"<a href=\"{help_link}\">{help_link}</a>")
        self.place_here_your_placeholder.setText("Paste JSON IAM:")
        self.__credentials_path = 'credentials/google_iam_credentials.json'
        try:
            with open(self.__credentials_path, 'r') as f:
                credentials = f.read()
                self.credentials_textedit.setText(credentials)
            self.exportCredentials()
        except:
            pass
        
    
    def exportCredentials(self):
        environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.__credentials_path

    def saveCredentials(self):
        credentials = self.credentials_textedit.toPlainText()
        msg = QMessageBox(self)
        try:
            
            with open(self.__credentials_path, 'w') as f:
                f.write(credentials)
            self.exportCredentials()
        except Exception:
            msg.setWindowTitle("Saving ...")
            msg.setText("Error occurred!")
            msg.setDetailedText(traceback.format_exc())
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return

        msg.setWindowTitle("Saving ...")
        msg.setText("Saved succesfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        return

    def testConnection(self):
        msg = QMessageBox(self)
        try:
            self._tts.connect(tts.Provider.GOOGLE)
        except Exception:
            msg.setWindowTitle("Connecting ...")
            msg.setText("Error occurred!")
            msg.setDetailedText(traceback.format_exc())
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return

        msg.setWindowTitle("Connecting ...")
        msg.setText("Connected succesfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec()

    def loadVoices(self):
        msg = QMessageBox(self)
        voices = []
        try:
            voices = self._tts.getVoices(tts.Provider.GOOGLE)
        except Exception:
            msg.setWindowTitle("Loading Voices ...")
            msg.setText("Error occurred!")
            msg.setDetailedText(traceback.format_exc())
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return

        msg.setWindowTitle("Loading Voices ...")
        msg.setText(f"Loaded {len(voices)} succesfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec()
        self.voices.extend(voices)
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    win = Window()
    win.show()
    sys.exit(app.exec())
