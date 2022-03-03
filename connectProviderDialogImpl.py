# system modules
from os import environ
from abc import ABC, abstractmethod
# foreign modules
from PyQt5.QtWidgets import (
    QDialog, QStatusBar
)
import json
from tts.myTypes import Provider
# qt designer modules
from ui.connectProviderDialog import Ui_ConnectProviderDialog
# own modules
from messageBoxImpl import ErrorMessageBox, InfoMessageBox
import tts

class ConnectProviderDialog(QDialog, Ui_ConnectProviderDialog):
    """Base class (abstract) for specific provider

    Args:
        QDialog (_type_): _description_
        Ui_ConnectProviderDialog (_type_): _description_
    """
    def __init__(
            self, 
            parent, 
            provider: Provider, 
            tts_handler: tts.TTSServiceHandler, 
            credentials_path: str
        ):
        super().__init__(parent)
        self.setupUi(self)
        self.voices = []
        self._provider = provider
        self._tts = tts_handler
        self._credentials_path = credentials_path
        self.status_bar = QStatusBar(self)
        self.status_bar_layout.addWidget(self.status_bar)

    def isConnected(self) -> bool:
        return self._tts.connect(self._provider)

    def testConnection(self):
        self.status_bar.showMessage(f"testing connection to {self._provider.name}...")
        self.repaint()
        try:
            self.isConnected()
        except Exception:
            ErrorMessageBox(self).exec()
            self.status_bar.clearMessage()
            return
        InfoMessageBox(self, "Connected succesfully!").exec()
        self.status_bar.clearMessage()

    def saveCredentials(self):
        self.status_bar.showMessage(f"started saving credentials to '{self._credentials_path}' ...")
        self.repaint()
        credentials = self.credentials_textedit.toPlainText()
        try:
            with open(self._credentials_path, 'w') as f:
                f.write(credentials)
            self.exportCredentials()
        except Exception:
            ErrorMessageBox(self).exec()
            self.status_bar.clearMessage()
            return
        InfoMessageBox(self, "Saved succesfully!").exec()
        self.status_bar.clearMessage()
        return

    def loadVoices(self):
        self.status_bar.showMessage("started loading voices...")
        self.repaint()
        voices = []
        try:
            voices = self._tts.getVoices(self._provider)
        except Exception:
            ErrorMessageBox(self).exec()
            self.status_bar.clearMessage()
            return
        InfoMessageBox(self, f"Loaded {len(voices)} succesfully!").exec()
        self.voices.extend(voices)
        self.load_voices_button.setEnabled(False)
        self.status_bar.clearMessage()
        return

class ConnectGoogleDialog(ConnectProviderDialog):
    def __init__(self, parent, tts_handler: tts.TTSServiceHandler):
        super().__init__(
            parent, 
            Provider.GOOGLE, 
            tts_handler=tts_handler,
            credentials_path='credentials/google_iam_credentials.json'
        )
        self.provider_label_placeholder.setText("Google Cloud TTS")
        help_link = "https://cloud.google.com/docs/authentication/getting-started"
        self.help_link_placeholder.setText(f"<a href=\"{help_link}\">{help_link}</a>")
        self.place_here_your_placeholder.setText("Paste JSON IAM:")
        try:
            with open(self._credentials_path, 'r') as f:
                credentials = f.read()
                self.credentials_textedit.setText(prettyJson(credentials))
            self.exportCredentials()
        except:
            pass
    
    def exportCredentials(self):
        environ['GOOGLE_APPLICATION_CREDENTIALS'] = self._credentials_path


class ConnectWatsonDialog(ConnectProviderDialog):
    def __init__(self, parent, tts_handler: tts.TTSServiceHandler):
        super().__init__(
            parent, 
            Provider.WATSON, 
            tts_handler=tts_handler,
            credentials_path='credentials/watson_iam_credentials.env'
        )
        self.provider_label_placeholder.setText("Watson TTS")
        help_link = "https://cloud.ibm.com/docs/account?topic=account-serviceidapikeys"
        self.help_link_placeholder.setText(f"<a href=\"{help_link}\">{help_link}</a>")
        self.place_here_your_placeholder.setText("Paste ENV IAM:")
        try:
            with open(self._credentials_path, 'r') as f:
                credentials = f.read()
                self.credentials_textedit.setText(credentials)
            self.exportCredentials()
        except:
            pass
        
    def exportCredentials(self):
        environ['IBM_CREDENTIALS_FILE'] = self._credentials_path

class ConnectAzureDialog(ConnectProviderDialog):
    def __init__(self, parent, tts_handler: tts.TTSServiceHandler):
        super().__init__(
            parent, 
            Provider.AZURE,
            tts_handler=tts_handler,
            credentials_path='credentials/azure_key.json'
        )
        self.provider_label_placeholder.setText("Azure TTS")
        help_link = "https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account"
        self.help_link_placeholder.setText(f"<a href=\"{help_link}\">{help_link}</a>")
        self.place_here_your_placeholder.setText("Paste Key:")
        json_file_template = prettyJson('{"key":"place-your-key-here","location":"place-server-location-here"}')
        self.credentials_textedit.setText(json_file_template)
        try:
            credentials = ""
            with open(self._credentials_path, 'r') as f:
                credentials = f.read()
                self.credentials_textedit.setText(prettyJson(credentials))
                self._tts.connect(Provider.AZURE)
        except:
            pass

    def exportCredentials(self):
        pass # just for the sake of abstraction

def prettyJson(json_string: str):
        json_string = json.loads(json_string)
        json_string = json.dumps(json_string, indent=2)
        return json_string