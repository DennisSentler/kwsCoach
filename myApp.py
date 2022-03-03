# system modules
import sys, os
# foreign modules
import qdarkstyle

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QFileDialog, QTreeWidgetItem, QSizePolicy
)
# qt designer modules

from ui.mainWindow import Ui_myApp
# own modules
from voiceListViewImpl import VoiceListView
from messageBoxImpl import ErrorMessageBox, InfoMessageBox
from addNewWordDialogImpl import AddNewWordDialog
from connectProviderDialogImpl import (
    ConnectGoogleDialog, ConnectWatsonDialog, ConnectAzureDialog
)
from voiceTestDialogImpl import VoiceTestDialog
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
        
    # menu
    def switchToSynthesis(self):
        self.stackedWidget.setCurrentIndex(0)
        self.menu_action_sythesis.setChecked(True)
        self.menu_action_dataset.setChecked(False)
        self.menu_action_training.setChecked(False)
        self.menu_action_about.setChecked(False)

    def switchToDataset(self):
        self.stackedWidget.setCurrentIndex(1)
        self.menu_action_sythesis.setChecked(False)
        self.menu_action_dataset.setChecked(True)
        self.menu_action_training.setChecked(False)
        self.menu_action_about.setChecked(False)

    def switchToTraining(self):
        self.stackedWidget.setCurrentIndex(2)
        self.menu_action_sythesis.setChecked(False)
        self.menu_action_dataset.setChecked(False)
        self.menu_action_training.setChecked(True)
        self.menu_action_about.setChecked(False)

    def switchToAbout(self):
        self.stackedWidget.setCurrentIndex(3)
        self.menu_action_sythesis.setChecked(False)
        self.menu_action_dataset.setChecked(False)
        self.menu_action_training.setChecked(False)
        self.menu_action_about.setChecked(True)

    # synthesis page
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
        self.ifSynthesisReadyActivateButton()

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
        self.ifSynthesisReadyActivateButton()

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
        self.ifSynthesisReadyActivateButton()

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
        self.ifSynthesisReadyActivateButton()

    def removeWordFromList(self):
        items = self.words_list_widget.selectedItems()
        for item in items:
            index = self.words_list_widget.indexOfTopLevelItem(item)
            self.words_list_widget.takeTopLevelItem(index)
        self.ifSynthesisReadyActivateButton()

    def ifSynthesisReadyActivateButton(self):
        words_ready = True if self.words_counter > 0 else False
        #TODO: call getCheckVoices, if ready
        voices_ready = True if len(self.voice_list_view.getCheckedVoices()) > 0 else False
        self.start_synthesis_button.setEnabled(words_ready)


    # augmentation page

    # training page


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
    try:
        clearApplicationCache(win.path_input_text.text())
    except Exception:
        pass
    sys.exit()

