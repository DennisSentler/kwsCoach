from itertools import count
from signal import raise_signal
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

    def config(self, words: list[Word], voices: list[Voice], tts_handler: TTSServiceHandler):
        """ATTENTION, please call this config function before calling "runt"

        Args:
            words (list[Word]): _description_
            voices (list[Voice]): _description_
            tts_handler (TTSServiceHandler): _description_
        """
        self.words = words
        self.voices = voices
        self.tts = tts_handler

    finished = pyqtSignal()
    progress = pyqtSignal(int)
    logs = pyqtSignal(str)
    exception = pyqtSignal(Exception)

    def run(self):
        try:
            call_counter = 0
            for word in self.words:
                self.logs.emit(f" + starting with word '{word.text}'")
                for voice in self.voices:
                    if voice.language in word.languages: 
                        call_counter += 1
                        self.logs.emit(f" + getting voice '{voice.name}' from {voice.provider.name}")
                        path = self.tts.synthesizeSpeech(voice.provider, word.text, voice)
                        self.logs.emit(f" + saved voice to '{path}'")
                        self.progress.emit(call_counter)
            self.finished.emit()
        except Exception as exc:
            self.exception.emit(exc)
            self.finished.emit()


class SynthesisDialog(QDialog, Ui_SynthesisDialog):
    def __init__(self, parent, words: list[Word], voices: list[Voice], ttsHandler: TTSServiceHandler):
        super().__init__(parent)
        self.setupUi(self)
        self.total_calls = self._calculateCalls(words, voices)
        self.progress_bar.setMaximum(self.total_calls)
        self.log_textedit.appendPlainText(f"starting download for {len(words)} words")

        # create own thread for synthesizer for parallel downloads
        self.thread = QThread()
        self.downloader = Downloader()
        self.downloader.config(words, voices, ttsHandler)
        self.downloader.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.downloader.run)
        self.downloader.finished.connect(self.thread.quit)
        self.downloader.finished.connect(self.downloader.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.downloader.progress.connect(self._updateProgressBar)
        self.downloader.logs.connect(self._printLogsOnTextEdit)
        self.downloader.exception.connect(self._receiveExceptionFromDownloader)
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

    def _printLogsOnTextEdit(self, log_line: str):
        self.log_textedit.appendPlainText(log_line)

    def _updateProgressBar(self, job_number: int):
        self.progress_bar.setValue(job_number)

    def _receiveExceptionFromDownloader(self, exception: Exception):
        try: 
            raise exception
        except Exception:
            ErrorMessageBox(self).exec()