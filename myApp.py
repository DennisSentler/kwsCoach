# system modules
import sys, os
# foreign modules
import qdarkstyle
from pydub import AudioSegment
from pydub.playback import play
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QFileDialog, QTreeWidgetItem
)
# qt designer modules
from ui.voiceTestDialog import Ui_VoiceTestDialog
from ui.mainWindow import Ui_myApp
# own modules
from tts.myTypes import Provider
from voiceListViewImpl import VoiceListView
from messageBoxImpl import ErrorMessageBox, InfoMessageBox
from addNewWordDialogImpl import AddNewWordDialog
from connectProviderDialogImpl import (
    ConnectGoogleDialog, ConnectWatsonDialog, ConnectAzureDialog
)
import tts

class MyApp(QMainWindow, Ui_myApp):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #create voice list view
        default_directory = os.path.abspath(os.path.dirname(__file__))
        self.path_input_text.setText(default_directory)
        self.voice_list_view = VoiceListView(parent=self)
        self.voice_list_view.setObjectName("voice_list_view")
        self.gridLayout_4.addWidget(self.voice_list_view, 1, 0, 1, 5)

        # create tts service handler
        self._voices = []
        self._tts = tts.TTSServiceHandler(default_directory)
        self.words_counter = 0
        
    def openConnectGoogleDialog(self):
        try:
            diag = ConnectGoogleDialog(self, self._tts)
            if diag.exec_():
                self._voices.extend(diag.voices)
                self.voice_list_view.addVoices(diag.voices)
                if len(diag.voices) > 0:
                    self.connect_button_google.setEnabled(False)
            self.status_label_google.setText("Connected" if diag.isConnected() else "Dicsonnected")
        except Exception:
            ErrorMessageBox(self).exec()

    def openConnectWatsonDialog(self):
        try:
            diag = ConnectWatsonDialog(self, self._tts)
            if diag.exec_():
                self._voices.extend(diag.voices)
                self.voice_list_view.addVoices(diag.voices)
                if len(diag.voices) > 0:
                    self.connect_button_watson.setEnabled(False)
            self.status_label_watson.setText("Connected" if diag.isConnected() else "Dicsonnected")
        except Exception:
            ErrorMessageBox(self).exec()

    def openConnectAzureDialog(self):
        try:
            diag = ConnectAzureDialog(self, self._tts)
            if diag.exec_():
                self._voices.extend(diag.voices)
                self.voice_list_view.addVoices(diag.voices)
                if len(diag.voices) > 0:
                    self.connect_button_azure.setEnabled(False)
            self.status_label_azure.setText("Connected" if diag.isConnected() else "Dicsonnected")
        except Exception:
            ErrorMessageBox(self).exec()

    def openVoiceTestDialog(self, voice):
        print("open voice test for", str(voice))
        dialog = VoiceTestDialog(self, voice, self._tts)
        dialog.exec()

    def openDirectorySelectDialog(self):
        dir = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir != "":
            self.path_input_text.setText(str(dir))
            self._tts.changeDirectory(dir)

    def openAddNewWordListDialog(self):
        all_languages = []
        for voice in self._voices:
            all_languages.append(voice.language)
        all_languages = set(all_languages)
        all_languages = list(all_languages)
        all_languages.sort()
        dialog = AddNewWordDialog(self, all_languages)
        if dialog.exec():
            self.words_counter += 1
            word_item = QTreeWidgetItem(self.words_list_widget)
            word_item.setData(0, 0, self.words_counter)
            word_item.setData(1, 0, dialog.word)
            word_item.setData(2, 0, str(dialog.selected_languages))
            self.words_list_widget.addTopLevelItem(word_item)
            for column in range(self.words_list_widget.columnCount()):
                self.words_list_widget.resizeColumnToContents(column)

    def removeWordFromList(self):
        items = self.words_list_widget.selectedItems()
        for item in items:
            index = self.words_list_widget.indexOfTopLevelItem(item)
            self.words_list_widget.takeTopLevelItem(index)


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

def clearApplicationCache(workingDirectory: str):
    dir = f"{workingDirectory}/.app_cache"
    for f in os.listdir(dir):
        if f != ".gitkeep":
            os.remove(os.path.join(dir, f))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    win = MyApp()
    win.show()
    app.exec()

    # delete app cache, from working directory
    clearApplicationCache(win.path_input_text.text())
    sys.exit()

