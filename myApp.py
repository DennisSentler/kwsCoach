import sys
import qdarkstyle
import traceback
from os import environ

from PyQt5.QtWidgets import (
    QTreeView, QApplication, QMainWindow, QDialog, QMessageBox, QTextEdit, QLabel, QTreeWidget, QTreeWidgetItem
)
from PyQt5.Qt import Qt

from test import Ui_myApp
from connectProviderDialog import Ui_ConnectProviderDialog
from lib import googleTTS, baseTTS
from voiceListView import VoiceListView
from voiceTestDialog import Ui_VoiceTestDialog

class Window(QMainWindow, Ui_myApp):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.__voices = []
        self.voice_list_view = VoiceListView(self)
        self.voice_list_view.setObjectName("voice_list_view")
        self.gridLayout_4.addWidget(self.voice_list_view, 1, 0, 1, 1)
        
    def openConnectGoogleDialog(self):
        diag = ConnectGoogleDialog(self)
        if diag.exec_():
            self.__voices.extend(diag.voices)
            self.voice_list_view.addVoices(diag.voices)

    def openVoiceTestDialog(self, voice):
        print("open voice test for", str(voice))
        dialog = VoiceTestDialog(voice,parent=self)
        dialog.exec()



class VoiceTestDialog(QDialog, Ui_VoiceTestDialog):
    def __init__(self, voice, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.voice_details_placeholder.setText(str(voice))
        

class ConnectGoogleDialog(QDialog, Ui_ConnectProviderDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.voices = []
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
        self.__g_tts = googleTTS.GoogleTTS()
    
    def exportCredentials(self):
        environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.__credentials_path

    def saveCredentials(self):
        credentials = self.credentials_textedit.toPlainText()
        msg = QMessageBox()
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
            self.__g_tts.connect()
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
            voices = self.__g_tts.getVoices()
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
