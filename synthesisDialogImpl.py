from itertools import count
from time import sleep
from PyQt5.QtWidgets import (
    QDialog, QListWidgetItem
)
from PyQt5.QtCore import (
    Qt, QTimer, QObject, QThread, pyqtSignal
)
from messageBoxImpl import ErrorMessageBox

from tts.ttsServiceHandler import TTSServiceHandler 

from ui.synthesisDialog import Ui_SynthesisDialog
from tts.myTypes import Voice, Word

class Downloader(QObject):
    def __init__(self, parent, words: list[Word], voices: list[Voice], tts_handler: TTSServiceHandler):
        super().__init__(parent)
        self.words = words
        self.voices = voices
        self.tts = tts_handler
        self.owner = parent

    finished = pyqtSignal()
    progress = pyqtSignal(int)
    logs = pyqtSignal(str)

    def run(self):
        try:
            call_counter = 0
            for word in self.words:
                self.logs.emit(f"starting with word '{word.text}'")
                for voice in self.voices:
                    if voice.language in word.languages: 
                        call_counter += 1
                        path = self.tts.synthesizeSpeech(voice.provider, word.text, voice)
                        self.progress.emit(call_counter)
                        sleep(0.1)
            self.finished.emit()
        except Exception:
            self.finished.emit()
            ErrorMessageBox(self.owner).exec()


class SynthesisDialog(QDialog, Ui_SynthesisDialog):
    def __init__(self, parent, words: list[Word], voices: list[Voice], ttsHandler: TTSServiceHandler):
        super().__init__(parent)
        self.setupUi(self)
        self.total_calls = self._calculateCalls(words, voices)
        self.progress_bar.setMaximum(self.total_calls)
        self.log_textedit.appendPlainText(f"starting download for {len(words)} words")

        # create own thread for synthesizer for parallel downloads
        self.thread = QThread()
        self.downloader = Downloader(self, words, voices, ttsHandler)
        self.downloader.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.downloader.run)
        self.downloader.finished.connect(self.thread.quit)
        self.downloader.finished.connect(self.downloader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.downloader.progress.connect(self.updateProgressBar)
        self.downloader.logs.connect(self.printLogsOnTextEdit)
        # Start the thread
        self.thread.start()

        self.thread.finished.connect(
            lambda: self.ok_button.setEnabled(True)
        )

    def _calculateCalls(self, words: list[Word], voices: list[Voice]) -> int: 
        counter = 0
        for word in words:
            for voice in voices:
                if voice.language in word.languages: counter += 1
        return counter

    def printLogsOnTextEdit(self, log_line: str):
        self.log_textedit.appendPlainText(log_line)

    def updateProgressBar(self, job_number: int):
        self.progress_bar.setValue(job_number)
