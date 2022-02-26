#foreign modules
import traceback
from PyQt5.QtWidgets import QMessageBox

class ErrorMessageBox(QMessageBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Internal Error")
        self.setText("Error occurred!")
        self.setDetailedText(traceback.format_exc())
        self.setIcon(QMessageBox.Warning)

class InfoMessageBox(QMessageBox):
    def __init__(self, parent, text: str):
        super().__init__(parent)
        self.setWindowTitle("Info")
        self.setText(text)
        self.setIcon(QMessageBox.Information)