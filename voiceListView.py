from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.Qt import Qt

from PyQt5.QtGui import QStandardItem
from tts import Voice


class VoiceListView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(VoiceListView, self).__init__(parent)
        self.parent = parent
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
            voice = Voice(sel[1].data() ,sel[2].data() ,sel[3].data() ,sel[4].data())
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
        for i,h in enumerate(self.headers):
            self.resizeColumnToContents(i)
