import os
import librosa
from PyQt5.QtWidgets import (
    QFileSystemModel
)

from PyQt5 import QtCore

class DatasetFileModel(QFileSystemModel):
    def __init__(self):
        super(DatasetFileModel, self).__init__()
        self._custom_columns = {4:"Files", 5:"Length"}

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Folder Name"
            if section in self._custom_columns:
                return self._custom_columns[section]

        return super(DatasetFileModel, self).headerData(section, orientation, role)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return super(DatasetFileModel, self).columnCount() + len(self._custom_columns)

    def data(self, index, role):
        c = index.column()
        if c in self._custom_columns and self._custom_columns[c] == "Files":
            if role == QtCore.Qt.DisplayRole:
                if self.isDir(index):
                    dir_path = self.fileInfo(index).filePath()
                    file_count = len([name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))])
                    return file_count
                else:
                    return 1

        if c in self._custom_columns and self._custom_columns[c] == "Length":
            if role == QtCore.Qt.DisplayRole:
                if self.isDir(index):
                    dir_path = self.fileInfo(index).filePath()
                    durations = []
                    for root_dir, category_dirs, files in os.walk(dir_path):
                        for file in files:
                            file_dur_sec = librosa.get_duration(filename=f"{root_dir}/{file}")
                            durations.append(file_dur_sec)
                    return f"{int(min(durations)*1000)}ms - {int(max(durations)*1000)}ms"
                else:
                    file_path = self.fileInfo(index).filePath()
                    return f"{int(librosa.get_duration(filename=file_path)*1000)}ms"

        return super(DatasetFileModel, self).data(index, role)
