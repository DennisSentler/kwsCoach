# system modules
from os import environ
# foreign modules
from PyQt5.QtWidgets import (
    QDialog
)
import json
# qt designer modules
from ui.connectProviderDialog import Ui_ConnectProviderDialog
# own modules
from messageBoxImpl import ErrorMessageBox, InfoMessageBox
import tts

class ConnectGoogleDialog(QDialog, Ui_ConnectProviderDialog):
    def __init__(self, parent, tts_handler: tts.TTSServiceHandler):
        super().__init__(parent)
        self.setupUi(self)
        self.voices = []
        self._tts = tts_handler
        self.provider_label_placeholder.setText("Google Cloud TTS")
        help_link = "https://cloud.google.com/docs/authentication/getting-started"
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
        try:
            
            with open(self.__credentials_path, 'w') as f:
                f.write(credentials)
            self.exportCredentials()
        except Exception:
            ErrorMessageBox(self).exec()
            return
        InfoMessageBox(self, "Saved succesfully!").exec()
        return

    def testConnection(self):
        try:
            self._tts.connect(tts.Provider.GOOGLE)
        except Exception:
            ErrorMessageBox(self).exec()
            return
        InfoMessageBox(self, "Connected succesfully!").exec()

    def loadVoices(self):
        voices = []
        try:
            voices = self._tts.getVoices(tts.Provider.GOOGLE)
        except Exception:
            ErrorMessageBox(self).exec()
            return
        InfoMessageBox(self, f"Loaded {len(voices)} succesfully!").exec()
        self.voices.extend(voices)
        return


class ConnectWatsonDialog(QDialog, Ui_ConnectProviderDialog):
    def __init__(self, parent, tts_handler: tts.TTSServiceHandler):
        super().__init__(parent)
        self.setupUi(self)
        self.voices = []
        self._tts = tts_handler
        self.provider_label_placeholder.setText("Watson TTS")
        help_link = "https://cloud.ibm.com/docs/account?topic=account-serviceidapikeys"
        self.help_link_placeholder.setText(f"<a href=\"{help_link}\">{help_link}</a>")
        self.place_here_your_placeholder.setText("Paste ENV IAM:")
        self.__credentials_path = 'credentials/watson_iam_credentials.env'
        try:
            with open(self.__credentials_path, 'r') as f:
                credentials = f.read()
                self.credentials_textedit.setText(credentials)
            self.exportCredentials()
        except:
            pass
        
    
    def exportCredentials(self):
        environ['IBM_CREDENTIALS_FILE'] = self.__credentials_path

    def saveCredentials(self):
        credentials = self.credentials_textedit.toPlainText()
        try:
            
            with open(self.__credentials_path, 'w') as f:
                f.write(credentials)
            self.exportCredentials()
        except Exception:
            ErrorMessageBox(self).exec()
            return
        InfoMessageBox(self, "Saved succesfully!").exec()
        return

    def testConnection(self):
        try:
            self._tts.connect(tts.Provider.WATSON)
        except Exception:
            ErrorMessageBox(self).exec()
            return
        InfoMessageBox(self, "Connected succesfully!").exec()

    def loadVoices(self):
        voices = []
        try:
            voices = self._tts.getVoices(tts.Provider.WATSON)
        except Exception:
            ErrorMessageBox(self).exec()
            return
        InfoMessageBox(self, f"Loaded {len(voices)} succesfully!").exec()
        self.voices.extend(voices)
        return

class ConnectAzureDialog(QDialog, Ui_ConnectProviderDialog):
    def __init__(self, parent, tts_handler: tts.TTSServiceHandler):
        super().__init__(parent)
        self.setupUi(self)
        self.voices = []
        self._tts = tts_handler
        self.provider_label_placeholder.setText("Azure TTS")
        help_link = "https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account"
        self.help_link_placeholder.setText(f"<a href=\"{help_link}\">{help_link}</a>")
        self.place_here_your_placeholder.setText("Paste Key:")
        self.__credentials_path = 'credentials/azure_key.json'
        json_file_template = '{"key":"place-your-key-here","location":"place-server-location-here"}'
        json_file_template = json.loads(json_file_template)
        json_file_template = json.dumps(json_file_template, indent=2)
        self.credentials_textedit.setText(json_file_template)
        try:
            credentials = ""
            with open(self.__credentials_path, 'r') as f:
                credentials = f.read()
                self.credentials_textedit.setText(credentials)
        except:
            pass

    def saveCredentials(self):
        credentials = self.credentials_textedit.toPlainText()
        try:
            json_credentials = json.loads(credentials)
            credentials = json.dumps(json_credentials)
            with open(self.__credentials_path, 'w') as f:
                f.write(credentials)
        except Exception:
            ErrorMessageBox(self).exec()
            return
        InfoMessageBox(self, "Saved succesfully!").exec()
        return

    def testConnection(self):
        try:
            self._tts.connect(tts.Provider.AZURE)
        except Exception:
            ErrorMessageBox(self).exec()
            return
        InfoMessageBox(self, "Connected succesfully!").exec()

    def loadVoices(self):
        voices = []
        try:
            voices = self._tts.getVoices(tts.Provider.AZURE)
        except Exception:
            ErrorMessageBox(self).exec()
            return
        InfoMessageBox(self, f"Loaded {len(voices)} succesfully!").exec()
        self.voices.extend(voices)
        return