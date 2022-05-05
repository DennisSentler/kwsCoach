# system modules
from logging import root
import sys
import os
import re
import yaml
from pyparsing import col
# foreign modules
import qdarkstyle

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QFileDialog, QTreeWidgetItem, QSizePolicy, QMessageBox, QFileSystemModel, QMenu, QAction
)
from qtwidgets import Toggle
from PyQt5.QtGui import QIcon
from PyQt5.Qt import Qt
from augmentationDialogImpl import AugmentationDialog
from datasetFileModel import DatasetFileModel
from tts.myTypes import AugmentationType, Word
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
from trainingScriptWrapper import TrainingScriptWrapper
from voiceTestDialogImpl import VoiceTestDialog
import tts


class kwsCoachApp(QMainWindow, Ui_myApp):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        QIcon.setThemeName("ubuntu-mono-dark")
        # setup synthesis page
        # create voice list view
        default_directory = os.path.abspath(os.path.dirname(__file__))
        self.path_input_text.setText(default_directory)
        self.dataset_src_path_input_text.setText(
            str(default_directory)+"/synthesis")
        self.dataset_dest_path_input_text_2.setText(
            str(default_directory)+"/synthesis")
        self.voice_list_view = VoiceListView(parent=self)
        self.voice_list_view.setObjectName("voice_list_view")
        self.gridLayout_4.addWidget(self.voice_list_view, 1, 0, 1, 5)
        # create tts service handler
        self._voices = []
        self._tts = tts.TTSServiceHandler(default_directory)
        self._words_to_synthesize = []

        # setup argumentation page
        # create toggle slider
        self.slider_dataset = Toggle(parent=self)
        self.slider_dataset.stateChanged['int'].connect(
            self.toggleDatasetDirectory)
        self.horizontalLayout_10.insertWidget(1, self.slider_dataset)

        # setup training page
        self.trainer = None
        self._words_to_train = []
        # load architectures from config file
        self.architectures = self.loadModelArchitectures()
        for architecture in self.architectures:
            self.model_architecture_combobox.addItem(
                architecture["display_name"])

    # menu bar
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
            self.status_label_google.setText(
                "Connected" if diag.isConnected() else "Dicsonnected")
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
            self.status_label_watson.setText(
                "Connected" if diag.isConnected() else "Dicsonnected")
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
            self.status_label_azure.setText(
                "Connected" if diag.isConnected() else "Dicsonnected")
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
            self.dataset_src_path_input_text.setText(str(dir)+"/synthesis")
            self.dataset_dest_path_input_text_2.setText(str(dir)+"/synthesis")
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
            self._words_to_synthesize.append(
                Word(dialog.word,
                     dialog.selected_languages,
                     is_random=dialog.random_word_radioButton.isChecked(),
                     quantity=dialog.random_word_quantity_dial.value()
                     )
            )
            self.refreshWordListWidget()

    def removeWordFromList(self):
        items = self.words_list_widget.selectedItems()
        for item in items:
            index = self.words_list_widget.indexOfTopLevelItem(item)
            del self._words_to_synthesize[index]
        self.refreshWordListWidget()

    def refreshWordListWidget(self):
        self.words_list_widget.clear()
        for index, word in enumerate(self._words_to_synthesize):
            word_item = QTreeWidgetItem(self.words_list_widget)
            word_item.setData(0, 0, index+1)
            if word.is_random:
                word_item.setData(
                    1, 0, f"...{word.text[-15:]} (qty: {word.quantity})")
            else:
                word_item.setData(1, 0, word.text)
            word_item.setData(2, 0, str(word.languages))
            self.words_list_widget.addTopLevelItem(word_item)

        for column in range(self.words_list_widget.columnCount()):
            self.words_list_widget.resizeColumnToContents(column)

    def openSynthesisDialog(self):
        self.status_bar.showMessage("checking synthesis requirements ...")
        voices = self.voice_list_view.getCheckedVoices()
        words = self._words_to_synthesize
        self.status_bar.clearMessage()
        if (len(words) == 0 or len(voices) == 0):
            self.status_bar.showMessage(
                "condition not met! please select at least one voice and one word!", 5000)
            return
        synthesis = SynthesisDialog(self, words, voices, self._tts)
        synthesis.exec()

    # augmentation page
    def openSrcDatasetDirectorySelectDialog(self):
        dir = QFileDialog.getExistingDirectory(
            self, 'Select Source Dataset Directory')
        if dir != "":
            self.dataset_src_path_input_text.setText(str(dir))
            # workaround, for making sure, that the state changes
            self.slider_dataset.setCheckState(Qt.Checked)
            self.slider_dataset.setCheckState(Qt.Unchecked)

    def openDestDatasetDirectorySelectDialog(self):
        dir = QFileDialog.getExistingDirectory(
            self, 'Select Target Dataset Directory')
        if dir != "":
            self.dataset_dest_path_input_text_2.setText(str(dir))
            # workaround, for making sure, that the state changes
            self.slider_dataset.setCheckState(Qt.Unchecked)
            self.slider_dataset.setCheckState(Qt.Checked)

    def setFilesViewContent(self, path: str):
        model = DatasetFileModel()
        model.setRootPath(path)
        self.files_view.setModel(model)
        self.files_view.setRootIndex(model.index(path))
        self.files_view.hideColumn(1)
        self.files_view.hideColumn(3)
        # resize columns
        for i in range(model.columnCount()):
            self.files_view.resizeColumnToContents(i)

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

    def toggleReplicationFaktor(self, state):
        if state > 0:
            self.replication_dial.setEnabled(True)
        else:
            self.replication_dial.setEnabled(False)

    def togglePitch(self, state):
        if state > 0:
            self.pitch_dial.setEnabled(True)
        else:
            self.pitch_dial.setEnabled(False)

    def toggleTimeStretch(self, state):
        if state > 0:
            self.time_stretch_min_dial.setEnabled(True)
            self.time_stretch_max_dial.setEnabled(True)
        else:
            self.time_stretch_min_dial.setEnabled(False)
            self.time_stretch_max_dial.setEnabled(False)

    def toggleVolume(self, state):
        if state > 0:
            self.volume_dial.setEnabled(True)
        else:
            self.volume_dial.setEnabled(False)

    def toggleGaussianNoise(self, state):
        if state > 0:
            self.gaussian_noise_dial.setEnabled(True)
        else:
            self.gaussian_noise_dial.setEnabled(False)

    def toggleShortNoise(self, state):
        if state > 0:
            self.path_short_noises_button.setEnabled(True)
            self.path_short_noises_input.setEnabled(True)
        else:
            self.path_short_noises_button.setEnabled(False)
            self.path_short_noises_input.setEnabled(False)

    def writeDatasetInfo(self, dataset_dir: str):
        self.status_bar.showMessage("reading dataset information ...")
        number_files = 0
        number_categories = 0
        durations = []
        try:
            self.setFilesViewContent(dataset_dir)
            for root_dir, category_dirs, files in os.walk(dataset_dir):
                if len(category_dirs) != 0:
                    if number_categories == 0:
                        number_categories = len(category_dirs)
                    else:
                        raise Exception(
                            "Wrong directory structure, please use only a root directory and subdirectories for each category")
                number_files += len(files)
        except Exception:
            ErrorMessageBox(self).exec()
        self.num_files_label.setText(str(number_files))
        self.num_categories_label.setText(str(number_categories))
        self.status_bar.clearMessage()

    def toggleDatasetDirectory(self, state):
        dataset_dir = ""
        if state > 0:
            dataset_dir = self.dataset_dest_path_input_text_2.text()
            if (dataset_dir == ""):
                self.status_bar.showMessage(
                    "no source dataset directory selected! please select a parent directory, with subfolders for each category.", 5000)
                return
        else:
            dataset_dir = self.dataset_src_path_input_text.text()
            if (dataset_dir == ""):
                self.status_bar.showMessage(
                    "no destination dataset directory selected! please select a parent directory, with subfolders for each category.", 5000)
                return
        self.writeDatasetInfo(dataset_dir)

    def openAugmentationDialog(self):
        augmentations = {}
        augmentations[AugmentationType.TRIM_SILENCE] = {"use": self.trim_silence_checkBox.isChecked(
        ), "db_threshold": self.trim_silence_db_threshhold_dial.value()}
        augmentations[AugmentationType.NORMALIZE_DURATION] = {
            "use": self.normalization_checkBox.isChecked(), "norm_duration_ms": self.normalization_dial.value()}
        augmentations[AugmentationType.REPLICATION_FACTOR] = {
            "use": self.replication_checkBox.isChecked(), "factor": self.replication_dial.value()}
        augmentations[AugmentationType.TIME_SHIFT] = {
            "use": self.time_shift_checkBox.isChecked(), "max_shift": self.time_shift_dial.value()}
        augmentations[AugmentationType.PITCH] = {
            "use": self.pitch_checkBox.isChecked(), "semitones": self.pitch_dial.value()}
        augmentations[AugmentationType.TIME_STRETCH] = {"use": self.time_stretch_checkBox.isChecked(
        ), "min": self.time_stretch_min_dial.value(), "max": self.time_stretch_max_dial.value()}
        augmentations[AugmentationType.VOLUME] = {
            "use": self.volume_checkBox.isChecked(), "volume_gain": self.volume_dial.value()}

        user_info = """
        Your audio records will be permanently changed by this operation, there is no way to undo the adjustments.\r\n
        Please backup your dataset before continue.
        """
        if InfoMessageBox(self, user_info).exec() == QMessageBox.Ok:
            try:
                src_dataset_dir = self.dataset_src_path_input_text.text()
                if (src_dataset_dir == ""):
                    self.status_bar.showMessage(
                        "no source dataset directory selected! please select a parent directory, with subfolders for each category.", 5000)
                    return
                dest_dataset_dir = self.dataset_dest_path_input_text_2.text()
                if (dest_dataset_dir == ""):
                    self.status_bar.showMessage(
                        "no destination dataset directory selected! please select a parent directory, with subfolders for each category.", 5000)
                    return
                file_paths = []
                for root_dir, _, files in os.walk(src_dataset_dir):
                    for file in files:
                        category_dir = re.search("\/[^\/]*$", root_dir).group()
                        file_paths.append(f"{category_dir}/{file}")
            except Exception:
                ErrorMessageBox(self).exec()

            if AugmentationDialog(self, file_paths, src_dataset_dir, dest_dataset_dir, augmentations).exec():
                self.toggleDatasetDirectory(2)

    # training page
    def loadModelArchitectures(self):
        architectures = None
        try:
            with open("model_size_info.yaml", "r") as config_yaml:
                architectures = yaml.load(config_yaml, Loader=yaml.FullLoader)
                config_yaml.close()
        except Exception:
            ErrorMessageBox(self).exec()
        return architectures

    def openTrainingDatasetSelectDialog(self):
        dir = QFileDialog.getExistingDirectory(
            self, 'Select Training Dataset Directory')
        if dir != "":
            self.train_dataset_path_input.setText(str(dir))
            self._words_to_train = self._readTrainingDatasetFolders(dir)
            self.showTrainingWordsList(self._words_to_train)

    def openModelDestinationSelectDialog(self):
        dir = QFileDialog.getExistingDirectory(
            self, 'Select Model Destination')
        if dir != "":
            self.model_destination_input.setText(str(dir))

    def startTraining(self):
        try:
            model = self.architectures[self.model_architecture_combobox.currentIndex(
            )]
            self.trainer = TrainingScriptWrapper(
                textbox = self.training_log_textedit,
                progressbar_epochs=self.progressBar_epochs,
                progressbar_steps=self.progressBar_steps,
                dataset_path = self.train_dataset_path_input.text(),
                destination_path = self.model_destination_input.text(),
                wanted_words = self._words_to_train,
                audio_length_ms = str(self.audio_length_dial.value()),
                dataset_silence_percentage = str(self.silence_percentage_dial.value()),
                dataset_unknown_percentage = str(self.unknown_percentage_dial.value()),
                mfcc_features = str(self.mfcc_features_dial.value()),
                mfcc_window_size_ms = str(self.mfcc_window_size_dial.value()),
                mfcc_window_stride_ms = str(self.mfcc_window_stride_dial.value()),
                model_architecture = model['technical_name'],
                model_size = model['model_size'],
                sample_rate = str(self.sample_rate_dial.value())
            )
            self.stop_training_button.setEnabled(True)
            self.trainer.start_process()
        except Exception:
            ErrorMessageBox(self).exec()

    def stopTraining(self):
        self.progressBar_epochs.setValue(0)
        self.progressBar_epochs.setFormat("")
        self.progressBar_steps.setFormat("")
        self.progressBar_steps.setValue(0)
        try:
            if self.trainer is not None:
                self.trainer.kill_process()
                self.stop_training_button.setEnabled(False)
        except Exception:
            ErrorMessageBox(self).exec()

    def _readTrainingDatasetFolders(self, dir: str):
        try:
            sub_folders = [name for name in os.listdir(dir) 
                if os.path.isdir(os.path.join(dir, name)) and not name.startswith("_")]
            return sub_folders
        except Exception:
            ErrorMessageBox(self).exec()

    def showTrainingWordsList(self, words):
        self.train_words_list.clear()
        words.sort()
        self.train_words_list.addItems(words)


def clearApplicationCache(workingDirectory: str):
    dir = f"{workingDirectory}/.app_cache"
    for f in os.listdir(dir):
        if f != ".gitkeep":
            os.remove(os.path.join(dir, f))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    win = kwsCoachApp()
    win.show()
    app.exec()

    # delete app cache, from working directory
    try:
        clearApplicationCache(win.path_input_text.text())
    except Exception:
        pass
    sys.exit()
