from PyQt5.QtWidgets import (
    QDialog, QListWidgetItem
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
        self.word = self.new_word_textedit.text()
        if self.word == "": 
            return

        for row in range(self.language_list_view.count()):
            item = self.language_list_view.item(row)
            if item.checkState() == Qt.Checked:
                self.selected_languages.append(item.data(0))

        if len(self.selected_languages) == 0:
            return

        self.accept()
        