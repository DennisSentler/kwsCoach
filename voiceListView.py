from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.Qt import Qt

from PyQt5.QtGui import QStandardItem
from lib.baseTTS import Voice


class VoiceListView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(VoiceListView, self).__init__(parent)
        self.parent = parent
        self.headers = ["Provider", "Name", "Language", "Gender"]

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

        self.doubleClicked.connect(self.slotDoubleClicked)
        self.clicked.connect(self.slotClicked)

    def slotDoubleClicked(self, mi):
        mi = self.proxyModel.mapToSource(mi)
        row = mi.row()
        sel = self.selectionModel().selectedIndexes()
        voice = Voice(sel[0].data() ,sel[1].data() ,sel[2].data() ,sel[3].data())

        self.parent.openVoiceTestDialog(voice)

        
        print(f"double clicked on row {row}")

    def slotClicked(self, mi):
        mi = self.proxyModel.mapToSource(mi)
        row = mi.row()
        sel = self.selectionModel().selectedIndexes()
        for s in sel:
            print(s.data())
        print(f"clicked on row {row}")

    def addVoices(self, voices: list[Voice]):
        for v in voices:
            providerAttribute = QStandardItem(str(v.provider))
            providerAttribute.setCheckable(True)
            self.model.appendRow([
                providerAttribute,
                QStandardItem(str(v.name)),
                QStandardItem(str(v.language)),
                QStandardItem(str(v.gender.name))
            ])
