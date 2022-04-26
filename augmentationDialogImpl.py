import librosa
import soundfile
import numpy as np
import math
import random
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift, Gain
#import ptvsd
from pathlib import Path

from PyQt5.QtWidgets import (
    QDialog
)
from PyQt5.QtCore import (
    QObject, QThread, pyqtSignal
)
from messageBoxImpl import ErrorMessageBox
from tts.myTypes import AugmentationType as t


from ui.progressDialog import Ui_ProgressDialog

class AugmentationWorker(QObject):

    def config(self, file_paths: list[str], source_path: str, destination_path: str, augmentations: dict):
        self.source_path = source_path
        self.destination_path = destination_path
        self.file_paths = file_paths
        self.augmentations = augmentations

    finished = pyqtSignal()
    progress = pyqtSignal(int)
    logs = pyqtSignal(str)
    exception = pyqtSignal(Exception)

    def run(self):
        #ptvsd.debug_this_thread()
        ops_counter = 0
        try:
            for file_path in self.file_paths:
                self.logs.emit(f"loading file: '{self.source_path}{file_path}'")
                audio, sample_rate = librosa.load(f"{self.source_path}{file_path}", sr=None)

                trim = self.augmentations[t.TRIM_SILENCE]
                if trim["use"]:
                    self.logs.emit(f" + performing {trim}")
                    audio, _ = librosa.effects.trim(audio, top_db=trim["db_threshold"])

                normalize = self.augmentations[t.NORMALIZE_DURATION]
                if normalize["use"]:
                    self.logs.emit(f" + performing {normalize}")
                    normalized_duration_sec = normalize["norm_duration_ms"] / 1000
                    audio = self._padOrTrimToSize(audio, int(sample_rate * normalized_duration_sec))

                replicate = self.augmentations[t.REPLICATION_FACTOR]
                if replicate["use"]:
                    for replication in range(replicate["factor"]):
                        self.logs.emit(f" + performing replication no.: {replication+1}")
                        audio_replica = audio
                        replica_path = f"{file_path.replace('.wav', '')}_rep{replication+1}"

                        time_shift = self.augmentations[t.TIME_SHIFT]
                        if time_shift["use"]:
                            max_shift = time_shift["max_shift"] / 100
                            shift_op = Shift(-max_shift, max_shift, rollover=False, fade=True, p=1)
                            audio_replica = shift_op(audio_replica, sample_rate)
                            shifted = shift_op.serialize_parameters()["num_places_to_shift"]
                            replica_path = f"{replica_path}_sh{shifted}"

                        pitch = self.augmentations[t.PITCH]
                        if pitch["use"]:
                            pitch_op = PitchShift(-pitch["semitones"], pitch["semitones"], p=1)
                            audio_replica = pitch_op(audio_replica, sample_rate)
                            pitched = pitch_op.serialize_parameters()["num_semitones"]
                            replica_path = f"{replica_path}_str{pitched:.3f}"

                        time_stretch = self.augmentations[t.TIME_STRETCH]
                        if time_stretch["use"]:
                            time_stretch_op = TimeStretch(time_stretch["min"]/100, time_stretch["max"]/100, p=1)
                            audio_replica = time_stretch_op(audio_replica, sample_rate)
                            stretched = time_stretch_op.serialize_parameters()["rate"]
                            replica_path = f"{replica_path}_str{stretched:.3f}"
                        
                        volume = self.augmentations[t.VOLUME]
                        if volume["use"]:
                            volume_op = Gain(-volume["volume_gain"], volume["volume_gain"], p=1)
                            audio_replica = volume_op(audio_replica, sample_rate)
                            gained = volume_op.serialize_parameters()["amplitude_ratio"]
                            replica_path = f"{replica_path}_vol{gained:.3f}"

                        audio_dest = f"{self.destination_path}{replica_path}.wav"
                        self._writeFileToDirectory(audio_dest, audio_replica, sample_rate)
                
                audio_dest = f"{self.destination_path}{file_path}"
                self._writeFileToDirectory(audio_dest, audio, sample_rate)
                ops_counter = ops_counter + 1
                self.progress.emit(ops_counter)

            self.finished.emit()
        except Exception as exc:
            self.exception.emit(exc)
            self.finished.emit()

    def _writeFileToDirectory(self, path, audio, sample_rate):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        soundfile.write(path, data=audio, samplerate=sample_rate)


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
    def __init__(self, parent, file_paths: list[str], source_path: str, destination_path: str, augmentations: dict):
        super().__init__(parent)
        self.setupUi(self)
        total_ops = len(file_paths)
        self.progress_bar.setMaximum(total_ops)
        self.log_textedit.appendPlainText(f"starting augmentations on dataset")

        # create own thread for parallel augmentations
        self.thread = QThread()
        self.aug_worker = AugmentationWorker()
        self.aug_worker.config(file_paths, source_path, destination_path, augmentations)
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