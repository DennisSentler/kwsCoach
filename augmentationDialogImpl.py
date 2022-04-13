import librosa
import soundfile
import numpy as np
import math

from PyQt5.QtWidgets import (
    QDialog
)
from PyQt5.QtCore import (
    QObject, QThread, pyqtSignal
)
from messageBoxImpl import ErrorMessageBox
from tts.myTypes import Augmentation, AugmentationType


from ui.progressDialog import Ui_ProgressDialog

class AugmentationWorker(QObject):

    def config(self, file_paths: list[str], augmentations: list[Augmentation]):
        self.file_paths = file_paths
        self.augmentations = augmentations
        self.augmentations.sort()

    finished = pyqtSignal()
    progress = pyqtSignal(int)
    logs = pyqtSignal(str)
    exception = pyqtSignal(Exception)

    def run(self):
        ops_counter = 0
        try:
            for file_path in self.file_paths:
                self.logs.emit(f"loading file: '{file_path}'")
                audio, sample_rate = librosa.load(file_path, sr=None)
                for augmentation in self.augmentations:
                    self.logs.emit(f" + performing {augmentation}")
                    if augmentation.type == AugmentationType.TRIM_SILENCE:
                        audio, _ = librosa.effects.trim(audio, top_db=augmentation.parameter[0])

                    if augmentation.type == AugmentationType.NORMALIZE_DURATION:
                        normalized_duration_sec = augmentation.parameter[0] / 1000
                        audio = self._padOrTrimToSize(audio, int(sample_rate * normalized_duration_sec))

                    if augmentation.type == AugmentationType.TIME_SHIFT:
                        shift_ms = augmentation.parameter[0]


                    ops_counter = ops_counter + 1
                    self.progress.emit(ops_counter)

                soundfile.write(file_path, data=audio, samplerate=sample_rate)
            self.finished.emit()
        except Exception as exc:
            self.exception.emit(exc)
            self.finished.emit()

    def _padOrTrimToSize(self, audio: np.ndarray, norm_size: int):
        if audio.size < norm_size:
            padding_size = norm_size - audio.size
            left_pad_size = math.floor(padding_size/2)
            right_pad_size = math.ceil(padding_size/2)
            audio = np.pad(audio, (left_pad_size, right_pad_size))
        elif audio.size > norm_size:
            shrink_size = audio.size - norm_size
            left_shrink_size = math.floor(shrink_size/2)
            right_shrink_size = math.ceil(shrink_size/2)
            audio = audio[left_shrink_size : -right_shrink_size]

        if audio.size == norm_size:
            return audio
        else:
            raise Exception(f"Your audio file was not normalized correctly.")

class AugmentationDialog(QDialog, Ui_ProgressDialog):
    def __init__(self, parent, file_paths: list[str], augmentations: list[Augmentation]):
        super().__init__(parent)
        self.setupUi(self)
        total_ops = len(file_paths) * len(augmentations)
        self.progress_bar.setMaximum(total_ops)
        self.log_textedit.appendPlainText(f"starting augmentations on dataset")

        # create own thread for parallel augmentations
        self.thread = QThread()
        self.aug_worker = AugmentationWorker()
        self.aug_worker.config(file_paths, augmentations)
        self.aug_worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.aug_worker.run)
        self.aug_worker.finished.connect(self.thread.quit)
        self.aug_worker.finished.connect(self.aug_worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.aug_worker.progress.connect(self._updateProgressBar)
        self.aug_worker.logs.connect(self._printLogsOnTextEdit)
        self.aug_worker.exception.connect(self._receiveExceptionFromWorker)
        # Start the thread
        self.thread.start()

        self.thread.finished.connect(
            lambda: self.ok_button.setEnabled(True)
        )

    def _printLogsOnTextEdit(self, log_line: str):
        self.log_textedit.appendPlainText(log_line)

    def _updateProgressBar(self, job_number: int):
        self.progress_bar.setValue(job_number)

    def _receiveExceptionFromWorker(self, exception: Exception):
        try: 
            raise exception
        except Exception:
            ErrorMessageBox(self).exec()