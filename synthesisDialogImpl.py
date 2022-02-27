
from PyQt5.QtWidgets import (
    QDialog, QListWidgetItem
)
from PyQt5.QtCore import Qt
from tts.ttsServiceHandler import TTSServiceHandler 

from ui.synthesisDialog import Ui_SynthesisDialog
from tts.myTypes import Voice, Word

class SynthesisDialog(QDialog, Ui_SynthesisDialog):
    def __init__(self, parent, words: list[Word], voices: list[Voice], ttsHandler: TTSServiceHandler):
        super().__init__(parent)
        self.setupUi(self)
        total_calls = len(words) * len(voices)
        # TODO imlement loading alle requests data
        