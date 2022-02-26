# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/qtDesigner/connectProviderDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectProviderDialog(object):
    def setupUi(self, ConnectProviderDialog):
        ConnectProviderDialog.setObjectName("ConnectProviderDialog")
        ConnectProviderDialog.resize(567, 646)
        self.gridLayout_5 = QtWidgets.QGridLayout(ConnectProviderDialog)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.provider_label_placeholder = QtWidgets.QLabel(ConnectProviderDialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.provider_label_placeholder.setFont(font)
        self.provider_label_placeholder.setObjectName("provider_label_placeholder")
        self.gridLayout_2.addWidget(self.provider_label_placeholder, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(ConnectProviderDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.help_link_placeholder = QtWidgets.QLabel(self.frame)
        self.help_link_placeholder.setOpenExternalLinks(True)
        self.help_link_placeholder.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.help_link_placeholder.setObjectName("help_link_placeholder")
        self.verticalLayout.addWidget(self.help_link_placeholder)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.place_here_your_placeholder = QtWidgets.QLabel(ConnectProviderDialog)
        self.place_here_your_placeholder.setObjectName("place_here_your_placeholder")
        self.gridLayout_2.addWidget(self.place_here_your_placeholder, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.credentials_textedit = QtWidgets.QTextEdit(ConnectProviderDialog)
        self.credentials_textedit.setObjectName("credentials_textedit")
        self.gridLayout_3.addWidget(self.credentials_textedit, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.save_config_button = QtWidgets.QPushButton(ConnectProviderDialog)
        self.save_config_button.setObjectName("save_config_button")
        self.horizontalLayout_2.addWidget(self.save_config_button)
        self.ping_connection_button = QtWidgets.QPushButton(ConnectProviderDialog)
        self.ping_connection_button.setObjectName("ping_connection_button")
        self.horizontalLayout_2.addWidget(self.ping_connection_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 3)
        self.line = QtWidgets.QFrame(ConnectProviderDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 1, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 2, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.load_voices_button = QtWidgets.QPushButton(ConnectProviderDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_voices_button.sizePolicy().hasHeightForWidth())
        self.load_voices_button.setSizePolicy(sizePolicy)
        self.load_voices_button.setMinimumSize(QtCore.QSize(200, 0))
        self.load_voices_button.setObjectName("load_voices_button")
        self.gridLayout.addWidget(self.load_voices_button, 0, 0, 1, 2)
        self.close_button = QtWidgets.QPushButton(ConnectProviderDialog)
        self.close_button.setObjectName("close_button")
        self.gridLayout.addWidget(self.close_button, 2, 1, 1, 1)
        self.confirm_button = QtWidgets.QPushButton(ConnectProviderDialog)
        self.confirm_button.setObjectName("confirm_button")
        self.gridLayout.addWidget(self.confirm_button, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 2, 2, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.retranslateUi(ConnectProviderDialog)
        self.close_button.clicked.connect(ConnectProviderDialog.reject) # type: ignore
        self.save_config_button.clicked.connect(ConnectProviderDialog.saveCredentials) # type: ignore
        self.ping_connection_button.clicked.connect(ConnectProviderDialog.testConnection) # type: ignore
        self.load_voices_button.clicked.connect(ConnectProviderDialog.loadVoices) # type: ignore
        self.confirm_button.clicked.connect(ConnectProviderDialog.accept) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ConnectProviderDialog)

    def retranslateUi(self, ConnectProviderDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectProviderDialog.setWindowTitle(_translate("ConnectProviderDialog", "Connect Provider Dialog"))
        self.provider_label_placeholder.setText(_translate("ConnectProviderDialog", "provider_placeholder"))
        self.label_3.setText(_translate("ConnectProviderDialog", "Get your credentials: "))
        self.help_link_placeholder.setText(_translate("ConnectProviderDialog", "<html><head/><body><p><a href=\"http://dummy.com\"><span style=\" text-decoration: underline; color:#0000ff;\">help_link_placeholder</span></a></p></body></html>"))
        self.place_here_your_placeholder.setText(_translate("ConnectProviderDialog", "paste_here_your_placeholder:"))
        self.save_config_button.setText(_translate("ConnectProviderDialog", "Save Credentials"))
        self.ping_connection_button.setText(_translate("ConnectProviderDialog", "Test Connection"))
        self.load_voices_button.setText(_translate("ConnectProviderDialog", "Load Voices"))
        self.close_button.setText(_translate("ConnectProviderDialog", "Close"))
        self.confirm_button.setText(_translate("ConnectProviderDialog", "Confirm"))
