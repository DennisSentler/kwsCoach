# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_myApp(object):
    def setupUi(self, myApp):
        myApp.setObjectName("myApp")
        myApp.setEnabled(True)
        myApp.resize(1102, 737)
        myApp.setDocumentMode(False)
        myApp.setDockOptions(QtWidgets.QMainWindow.GroupedDragging)
        self.centralwidget = QtWidgets.QWidget(myApp)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.words_box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.words_box.sizePolicy().hasHeightForWidth())
        self.words_box.setSizePolicy(sizePolicy)
        self.words_box.setFlat(False)
        self.words_box.setCheckable(False)
        self.words_box.setObjectName("words_box")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.words_box)
        self.gridLayout_6.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.words_list_view = QtWidgets.QTreeWidget(self.words_box)
        self.words_list_view.setIndentation(0)
        self.words_list_view.setRootIsDecorated(False)
        self.words_list_view.setUniformRowHeights(True)
        self.words_list_view.setItemsExpandable(False)
        self.words_list_view.setObjectName("words_list_view")
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.words_list_view.headerItem().setFont(1, font)
        item_0 = QtWidgets.QTreeWidgetItem(self.words_list_view)
        item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_0 = QtWidgets.QTreeWidgetItem(self.words_list_view)
        self.words_list_view.header().setCascadingSectionResizes(False)
        self.words_list_view.header().setDefaultSectionSize(51)
        self.words_list_view.header().setHighlightSections(False)
        self.words_list_view.header().setStretchLastSection(True)
        self.gridLayout_6.addWidget(self.words_list_view, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.words_box, 0, 2, 2, 1)
        self.tts_services_box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tts_services_box.sizePolicy().hasHeightForWidth())
        self.tts_services_box.setSizePolicy(sizePolicy)
        self.tts_services_box.setMaximumSize(QtCore.QSize(651, 16777215))
        self.tts_services_box.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tts_services_box.setObjectName("tts_services_box")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tts_services_box)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.provider_frame_2 = QtWidgets.QFrame(self.tts_services_box)
        self.provider_frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.provider_frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.provider_frame_2.setObjectName("provider_frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.provider_frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.provider_text_2 = QtWidgets.QLabel(self.provider_frame_2)
        self.provider_text_2.setObjectName("provider_text_2")
        self.gridLayout_2.addWidget(self.provider_text_2, 0, 0, 1, 1)
        self.status_text_2 = QtWidgets.QLabel(self.provider_frame_2)
        self.status_text_2.setObjectName("status_text_2")
        self.gridLayout_2.addWidget(self.status_text_2, 0, 1, 1, 1)
        self.provider_name_2 = QtWidgets.QLabel(self.provider_frame_2)
        self.provider_name_2.setObjectName("provider_name_2")
        self.gridLayout_2.addWidget(self.provider_name_2, 1, 0, 1, 1)
        self.status_label_2 = QtWidgets.QLabel(self.provider_frame_2)
        self.status_label_2.setObjectName("status_label_2")
        self.gridLayout_2.addWidget(self.status_label_2, 1, 1, 1, 1)
        self.connect_button_2 = QtWidgets.QPushButton(self.provider_frame_2)
        self.connect_button_2.setObjectName("connect_button_2")
        self.gridLayout_2.addWidget(self.connect_button_2, 2, 0, 1, 2)
        self.gridLayout_7.addWidget(self.provider_frame_2, 0, 1, 1, 1)
        self.provider_frame = QtWidgets.QFrame(self.tts_services_box)
        self.provider_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.provider_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.provider_frame.setObjectName("provider_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.provider_frame)
        self.gridLayout.setObjectName("gridLayout")
        self.provider_text = QtWidgets.QLabel(self.provider_frame)
        self.provider_text.setObjectName("provider_text")
        self.gridLayout.addWidget(self.provider_text, 0, 0, 1, 1)
        self.status_text = QtWidgets.QLabel(self.provider_frame)
        self.status_text.setObjectName("status_text")
        self.gridLayout.addWidget(self.status_text, 0, 1, 1, 1)
        self.provider_name = QtWidgets.QLabel(self.provider_frame)
        self.provider_name.setObjectName("provider_name")
        self.gridLayout.addWidget(self.provider_name, 1, 0, 1, 1)
        self.status_label = QtWidgets.QLabel(self.provider_frame)
        self.status_label.setObjectName("status_label")
        self.gridLayout.addWidget(self.status_label, 1, 1, 1, 1)
        self.connect_button_google = QtWidgets.QPushButton(self.provider_frame)
        self.connect_button_google.setObjectName("connect_button_google")
        self.gridLayout.addWidget(self.connect_button_google, 2, 0, 1, 2)
        self.gridLayout_7.addWidget(self.provider_frame, 0, 0, 1, 1)
        self.provider_frame_3 = QtWidgets.QFrame(self.tts_services_box)
        self.provider_frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.provider_frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.provider_frame_3.setObjectName("provider_frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.provider_frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.provider_text_3 = QtWidgets.QLabel(self.provider_frame_3)
        self.provider_text_3.setObjectName("provider_text_3")
        self.gridLayout_3.addWidget(self.provider_text_3, 0, 0, 1, 1)
        self.status_text_3 = QtWidgets.QLabel(self.provider_frame_3)
        self.status_text_3.setObjectName("status_text_3")
        self.gridLayout_3.addWidget(self.status_text_3, 0, 1, 1, 1)
        self.provider_name_3 = QtWidgets.QLabel(self.provider_frame_3)
        self.provider_name_3.setObjectName("provider_name_3")
        self.gridLayout_3.addWidget(self.provider_name_3, 1, 0, 1, 1)
        self.status_label_3 = QtWidgets.QLabel(self.provider_frame_3)
        self.status_label_3.setObjectName("status_label_3")
        self.gridLayout_3.addWidget(self.status_label_3, 1, 1, 1, 1)
        self.connect_button_3 = QtWidgets.QPushButton(self.provider_frame_3)
        self.connect_button_3.setObjectName("connect_button_3")
        self.gridLayout_3.addWidget(self.connect_button_3, 2, 0, 1, 2)
        self.gridLayout_7.addWidget(self.provider_frame_3, 0, 2, 1, 1)
        self.gridLayout_8.addWidget(self.tts_services_box, 0, 0, 1, 2)
        self.dir_box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dir_box.sizePolicy().hasHeightForWidth())
        self.dir_box.setSizePolicy(sizePolicy)
        self.dir_box.setObjectName("dir_box")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.dir_box)
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.path_text = QtWidgets.QLabel(self.dir_box)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.path_text.setFont(font)
        self.path_text.setObjectName("path_text")
        self.gridLayout_5.addWidget(self.path_text, 0, 0, 1, 1)
        self.path_input_text = QtWidgets.QLineEdit(self.dir_box)
        self.path_input_text.setObjectName("path_input_text")
        self.gridLayout_5.addWidget(self.path_input_text, 0, 1, 1, 1)
        self.select_path_button = QtWidgets.QPushButton(self.dir_box)
        self.select_path_button.setObjectName("select_path_button")
        self.gridLayout_5.addWidget(self.select_path_button, 0, 2, 1, 1)
        self.gridLayout_8.addWidget(self.dir_box, 2, 0, 1, 3)
        self.voices_box = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voices_box.sizePolicy().hasHeightForWidth())
        self.voices_box.setSizePolicy(sizePolicy)
        self.voices_box.setObjectName("voices_box")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.voices_box)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.refresh_button = QtWidgets.QPushButton(self.voices_box)
        self.refresh_button.setDefault(False)
        self.refresh_button.setFlat(False)
        self.refresh_button.setObjectName("refresh_button")
        self.gridLayout_4.addWidget(self.refresh_button, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.voices_box, 1, 0, 1, 2)
        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        myApp.setCentralWidget(self.centralwidget)
        self.menu = QtWidgets.QToolBar(myApp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())
        self.menu.setSizePolicy(sizePolicy)
        self.menu.setMovable(False)
        self.menu.setOrientation(QtCore.Qt.Vertical)
        self.menu.setFloatable(False)
        self.menu.setObjectName("menu")
        myApp.addToolBar(QtCore.Qt.LeftToolBarArea, self.menu)
        self.statusBar = QtWidgets.QStatusBar(myApp)
        self.statusBar.setObjectName("statusBar")
        myApp.setStatusBar(self.statusBar)
        self.actionData_Sythesis = QtWidgets.QAction(myApp)
        self.actionData_Sythesis.setObjectName("actionData_Sythesis")
        self.actionAudio_Augmentation = QtWidgets.QAction(myApp)
        self.actionAudio_Augmentation.setObjectName("actionAudio_Augmentation")
        self.actionTraining = QtWidgets.QAction(myApp)
        self.actionTraining.setObjectName("actionTraining")
        self.menu.addAction(self.actionData_Sythesis)
        self.menu.addSeparator()
        self.menu.addAction(self.actionAudio_Augmentation)
        self.menu.addSeparator()
        self.menu.addAction(self.actionTraining)
        self.provider_text.setBuddy(self.provider_text)
        self.provider_name.setBuddy(self.provider_name)

        self.retranslateUi(myApp)
        self.connect_button_google.clicked.connect(myApp.openConnectGoogleDialog) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(myApp)

    def retranslateUi(self, myApp):
        _translate = QtCore.QCoreApplication.translate
        myApp.setWindowTitle(_translate("myApp", "MainWindow"))
        self.words_box.setTitle(_translate("myApp", "Words"))
        self.words_list_view.headerItem().setText(0, _translate("myApp", "ID"))
        self.words_list_view.headerItem().setText(1, _translate("myApp", "Word"))
        self.words_list_view.headerItem().setText(2, _translate("myApp", "Lang."))
        __sortingEnabled = self.words_list_view.isSortingEnabled()
        self.words_list_view.setSortingEnabled(False)
        self.words_list_view.topLevelItem(0).setText(0, _translate("myApp", "1"))
        self.words_list_view.topLevelItem(0).setText(1, _translate("myApp", "Husky"))
        self.words_list_view.topLevelItem(0).setText(2, _translate("myApp", "de-DE"))
        self.words_list_view.topLevelItem(1).setText(0, _translate("myApp", "2"))
        self.words_list_view.topLevelItem(1).setText(1, _translate("myApp", "Stop"))
        self.words_list_view.topLevelItem(1).setText(2, _translate("myApp", "de-DE"))
        self.words_list_view.setSortingEnabled(__sortingEnabled)
        self.tts_services_box.setTitle(_translate("myApp", "Text-to-speach services"))
        self.provider_text_2.setText(_translate("myApp", "provider"))
        self.status_text_2.setText(_translate("myApp", "status"))
        self.provider_name_2.setText(_translate("myApp", "Azure"))
        self.status_label_2.setText(_translate("myApp", "N/A"))
        self.connect_button_2.setText(_translate("myApp", "Connect"))
        self.provider_text.setText(_translate("myApp", "provider"))
        self.status_text.setText(_translate("myApp", "status"))
        self.provider_name.setText(_translate("myApp", "Google"))
        self.status_label.setText(_translate("myApp", "N/A"))
        self.connect_button_google.setText(_translate("myApp", "Connect"))
        self.provider_text_3.setText(_translate("myApp", "provider"))
        self.status_text_3.setText(_translate("myApp", "status"))
        self.provider_name_3.setText(_translate("myApp", "IBM"))
        self.status_label_3.setText(_translate("myApp", "N/A"))
        self.connect_button_3.setText(_translate("myApp", "Connect"))
        self.dir_box.setTitle(_translate("myApp", "Working Directory"))
        self.path_text.setText(_translate("myApp", "Path:"))
        self.select_path_button.setText(_translate("myApp", "..."))
        self.voices_box.setTitle(_translate("myApp", "Voices"))
        self.refresh_button.setText(_translate("myApp", "Refresh"))
        self.menu.setWindowTitle(_translate("myApp", "toolBar"))
        self.actionData_Sythesis.setText(_translate("myApp", "Data Sythesis"))
        self.actionAudio_Augmentation.setText(_translate("myApp", "Audio Augmentation"))
        self.actionTraining.setText(_translate("myApp", "Training"))