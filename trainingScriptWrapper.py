from PyQt5.QtWidgets import (QPlainTextEdit, QProgressBar,)                        
from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QFont
import re

class TrainingScriptWrapper():

    def __init__(self,
                 textbox: QPlainTextEdit,
                 progressbar_steps: QProgressBar,
                 progressbar_epochs: QProgressBar,
                 dataset_path: str,
                 destination_path: str,
                 wanted_words: list[str],
                 sample_rate: str,
                 audio_length_ms: str,
                 dataset_unknown_percentage: str,
                 dataset_silence_percentage: str,
                 model_architecture: str,
                 model_size: list[str],
                 mfcc_features: str,
                 mfcc_window_size_ms: str,
                 mfcc_window_stride_ms: str
                 ):
        self.progressbar_steps = progressbar_steps
        self.progressbar_epochs = progressbar_epochs
        self.progressbar_steps.setValue(0)
        self.progressbar_epochs.setValue(0)
        
        # make a comma seperated list string
        words_string = ','.join([str(item) for item in wanted_words]) 
        self.script_args = ["/home/dsentler/ARM-software/ds_cnn/train.py",
                            "--model_architecture", model_architecture,
                            "--model_size_info"]
        self.script_args.extend(model_size)
        self.script_args.extend(["--dct_coefficient_count", mfcc_features,
                                 "--window_size_ms", mfcc_window_size_ms,
                                 "--window_stride_ms", mfcc_window_stride_ms,
                                 "--learning_rate", "0.0005,0.0001,0.00002",
                                 "--how_many_training_steps", "1000,1000,1000",
                                 "--summaries_dir", f"{destination_path}/{model_architecture}/retrain_logs",
                                 "--train_dir", f"{destination_path}/{model_architecture}/training",
                                 "--time_shift_ms", "0",
                                 "--sample_rate", sample_rate,
                                 "--clip_duration_ms", audio_length_ms,
                                 "--wanted_words", words_string,
                                 "--data_dir", dataset_path,
                                 "--unknown_percentage", dataset_unknown_percentage,
                                 "--silence_percentage", dataset_silence_percentage]
                                 )
        self.p = None
        self.text = textbox
        self.text.setFont(QFont("Courier New"))
        self.text.setReadOnly(True)
        self.text.clear()

    def message(self, s: str):
        # filter backspaces
        if "\b" in s:
            s = s.replace('\b', '')

        lines = s.splitlines(keepends=False)
        for line in lines:
            if len(line) > 1:
                parsed = self._parseOutputLine(line)
                if not parsed:
                    self.text.appendPlainText(line)

    def _parseOutputLine(self, line : str) -> bool:
        regex_epoch = 'Epoch ([\d]{1,3})/([\d]{1,3})\r?'
        regex_steps = "[\s]{0,4}([\d]{1,3})/([\d]{1,3})\W*ETA: ([\d:smh]*)\W*loss: ([\d.]*)\W*accuracy: ([\d.]*)\r?"
        match = re.match(regex_steps, line)
        if match:
            self.progressbar_steps.setValue(int(match[1]))
            self.progressbar_steps.setMaximum(int(match[2]))
            self.progressbar_steps.setFormat(f"Step: {match[1]}/{match[2]} - remaining: {match[3]} - loss: {match[4]} - acc: {match[5]}")
            return True
        match = re.match(regex_epoch, line)
        if match:
            self.progressbar_epochs.setValue(int(match[1]))
            self.progressbar_epochs.setMaximum(int(match[2]))
            self.progressbar_epochs.setFormat(f"Epoch: {match[1]}/{match[2]}")
            return True

        return False


    def kill_process(self):
        if self.p is not None:
            self.p.kill()

    def start_process(self):
        if self.p is None:  # No process running.
            self.message("Executing process")
            # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            # Clean up once complete.
            self.p.finished.connect(self.process_finished)
            self.p.start("python3", self.script_args)

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None
