# foreign modules
import stat
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import Qt
from PyQt5.QtGui import QStandardItem
# own modules
from tts import Voice


class VoiceListView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(VoiceListView, self).__init__(parent)
        self.parent = parent
        self.selection_counter = 0
        self.headers = ["Use", "Provider", "Name", "Language", "Gender"]

        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)

        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.headers)
        self.proxyModel.setSourceModel(self.model)

        self.setAlternatingRowColors(True)
        self.setModel(self.proxyModel)
        self.setSortingEnabled(True)
        
        self.sortByColumn(3, Qt.AscendingOrder)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.clicked.connect(self.slotClicked)

    def slotClicked(self, mi):
        mi = self.proxyModel.mapToSource(mi)
        if mi.column() != 0:        
            sel = self.selectionModel().selectedIndexes()
            voice = _rowToVoice(sel)
            self.parent.openVoiceTestDialog(voice)

    def addVoices(self, voices: list[Voice]):
        for v in voices:
            checkbox = QStandardItem()
            checkbox.setData("checkbox")
            checkbox.setCheckable(True)
            self.model.appendRow([
                checkbox,
                QStandardItem(str(v.provider.name)),
                QStandardItem(str(v.name)),
                QStandardItem(str(v.language)),
                QStandardItem(str(v.gender.name))
            ])
        self.parent.total_voices_placeholder.setText(str(self.model.rowCount()))
        for i,h in enumerate(self.headers):
            self.resizeColumnToContents(i)

    def getCheckedVoices(self) -> list[Voice]:
        voices = []
        for row in range(self.model.rowCount()):
            item_checkbox = self.model.item(row)
            if item_checkbox.checkState() == Qt.Checked:
                items_from_row = []
                for header in range(len(self.headers)):
                    items_from_row += self.model.item(row, header)
                voice = _rowToVoice(items_from_row)
                voices += voice


def _rowToVoice(row: list) -> Voice:
    return Voice(row[1].data(), row[2].data(), row[3].data(), row[4].data())