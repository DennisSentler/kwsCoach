from PyQt5.QtWidgets import (
    QDialog, QListWidgetItem, QFileDialog
)
from PyQt5.QtCore import Qt 
from ui.addNewWordDialog import Ui_AddNewWordDialog

class AddNewWordDialog(QDialog, Ui_AddNewWordDialog):
    def __init__(self, parent, languages: list[str]):
        super().__init__(parent)
        self.setupUi(self)
        self.selected_languages = []
        self.word = ""
        for language in languages:
            item = QListWidgetItem(language)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.language_list_view.addItem(item)

    def confirmSelection(self):
        for row in range(self.language_list_view.count()):
                item = self.language_list_view.item(row)
                if item.checkState() == Qt.Checked:
                    self.selected_languages.append(item.data(0))
        if len(self.selected_languages) == 0:
            return

        if self.single_word_radioButton.isChecked():
            self.word = self.new_word_textedit.text()
            if self.word == "": 
                return
        else:
            self.word = self.wordlist_path_input.text()
            if self.word == "":
                return
        self.accept()
        
    def toggleWordRadioButtonSelected(self):
        self.wordlist_path_input.setEnabled(False)
        self.random_word_quantity_dial.setEnabled(False)
        self.wordlist_path_select_button.setEnabled(False)
        self.new_word_textedit.setEnabled(True)

    def toggleRandomWordRadioButtonSelected(self):
        self.wordlist_path_input.setEnabled(True)
        self.random_word_quantity_dial.setEnabled(True)
        self.wordlist_path_select_button.setEnabled(True)
        self.new_word_textedit.setEnabled(False)

    def openWordlistSelectDialog(self):
        dir = QFileDialog.getOpenFileName(self, 'Select Wordlist', filter="*.txt")[0]
        if dir != "":
            self.wordlist_path_input.setText(str(dir))