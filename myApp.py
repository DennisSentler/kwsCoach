# system modules
from locale import normalize
from logging import root
import sys, os
from numpy import average
from pyparsing import col
# foreign modules
import librosa
import qdarkstyle
from ast import literal_eval

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QFileDialog, QTreeWidgetItem, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QIcon
from augmentationDialogImpl import AugmentationDialog
from tts.myTypes import Augmentation, AugmentationType
# qt designer modules
from ui.mainWindow import Ui_myApp
# own modules
from synthesisDialogImpl import SynthesisDialog
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
        QIcon.setThemeName("ubuntu-mono-dark")
        #create voice list view
        default_directory = os.path.abspath(os.path.dirname(__file__))
        self.path_input_text.setText(default_directory)
        self.dataset_path_input_text.setText(str(default_directory)+"/synthesis")
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
            self.dataset_path_input_text.setText(str(dir)+"/synthesis")
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

    def getWordsFromList(self) -> list[tts.Word]:
        words = []
        for row in range(self.words_list_widget.topLevelItemCount()):
            word_widget_item = self.words_list_widget.topLevelItem(row)
            word_name = word_widget_item.data(1,0)
            word_languages = literal_eval(word_widget_item.data(2,0))
            words.append(tts.Word(word_name, word_languages))
        return words

    def openSynthesisDialog(self):
        self.status_bar.showMessage("checking synthesis requirements ...")
        voices = self.voice_list_view.getCheckedVoices()
        words = self.getWordsFromList()
        self.status_bar.clearMessage()
        if (len(words) == 0 or len(voices) == 0):
            self.status_bar.showMessage("condition not met! please select at least one voice and one word!", 5000)
            return
        synthesis = SynthesisDialog(self, words, voices, self._tts)
        synthesis.exec()

    # augmentation page
    def openDatasetDirectorySelectDialog(self):
        dir = QFileDialog.getExistingDirectory(self, 'Select Dataset Directory')
        if dir != "":
            self.dataset_path_input_text.setText(str(dir))

    def toggleNormalization(self, state):
        if state > 0:
            self.normalization_dial.setEnabled(True)
        else:
            self.normalization_dial.setEnabled(False)

    def toggleRandTimeShift(self, state):
        if state > 0:
            self.time_shift_dial.setEnabled(True)
        else:
            self.time_shift_dial.setEnabled(False)

    def toggleRandBackgroundNoise(self, state):
        if state > 0:
            self.path_background_input.setEnabled(True)
            self.path_background_button.setEnabled(True)
        else:
            self.path_background_input.setEnabled(False)
            self.path_background_button.setEnabled(False)

    def toggleTrimSilence(self, state):
        if state > 0:
            self.trim_silence_db_threshhold_dial.setEnabled(True)
        else:
            self.trim_silence_db_threshhold_dial.setEnabled(False)

    def writeDatasetInfo(self):
        self.status_bar.showMessage("reading dataset information ...")
        dataset_dir = self.dataset_path_input_text.text()
        if (dataset_dir == ""):
            self.status_bar.showMessage("no dataset directory selected! please select a parent directory, with subfolders for each category.", 5000)
            return
        number_files = 0
        number_categories = 0
        durations = []
        try:
            for root_dir, category_dirs, files in os.walk(dataset_dir):
                if len(category_dirs) != 0:
                    if number_categories == 0:
                        number_categories = len(category_dirs)
                    else:
                        raise Exception("Wrong directory structure, please use only a root directory and subdirectories for each category")
                
                for file in files:
                    file_dur_sec = librosa.get_duration(filename=f"{root_dir}/{file}")
                    durations.append(file_dur_sec)

                number_files += len(files)
        except Exception:
            ErrorMessageBox(self).exec()
        self.num_files_label.setText(str(number_files))
        self.num_categories_label.setText(str(number_categories))
        longest_audio = int(max(durations) * 1000)
        self.longest_audio_length_label.setText(str(longest_audio) + "ms")
        shortest_audio = int(min(durations) * 1000)
        self.shortest_audio_length_label.setText(str(shortest_audio) + "ms")
        average_audio = int(sum(durations) / len(durations) * 1000)
        self.average_audio_length_label.setText(str(average_audio) + "ms")
        self.status_bar.clearMessage()

    def openAugmentationDialog(self):
        augmentations = []
        if self.trim_silence_checkBox.isChecked():
            db_threshold = self.trim_silence_db_threshhold_dial.value()
            augmentations.append(Augmentation(AugmentationType.TRIM_SILENCE, [db_threshold]))
        if self.normalization_checkBox.isChecked():
            normalize_duration_ms = self.normalization_dial.value()
            augmentations.append(Augmentation(AugmentationType.NORMALIZE_DURATION, [normalize_duration_ms]))
        if self.time_shift_checkBox.isChecked():
            shift_ms = self.time_shift_dial.value()
            augmentations.append(Augmentation(AugmentationType.TIME_SHIFT, [shift_ms]))

        if len(augmentations) == 0:
            self.status_bar.showMessage("no data augmentations selected", 5000)
            return

        user_info = """
        Your audio records will be permanently changed by this operation, there is no way to undo the adjustments.\r\n
        Please backup your dataset before continue.
        """
        if InfoMessageBox(self, user_info).exec() == QMessageBox.Ok:
            try:
                dataset_dir = self.dataset_path_input_text.text()
                if (dataset_dir == ""):
                    self.status_bar.showMessage("no dataset directory selected! please select a parent directory, with subfolders for each category.", 5000)
                    return
                file_paths = []
                for root_dir, _, files in os.walk(dataset_dir):
                    for file in files:
                        file_paths.append(f"{root_dir}/{file}")
            except Exception:
                ErrorMessageBox(self).exec()
            
            if AugmentationDialog(self, file_paths, augmentations).exec():
                self.writeDatasetInfo()
            
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

