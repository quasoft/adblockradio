# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_text_item_editor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TextItemEditor(object):
    def setupUi(self, TextItemEditor):
        TextItemEditor.setObjectName(_fromUtf8("TextItemEditor"))
        TextItemEditor.setWindowModality(QtCore.Qt.WindowModal)
        TextItemEditor.resize(500, 390)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TextItemEditor.sizePolicy().hasHeightForWidth())
        TextItemEditor.setSizePolicy(sizePolicy)
        TextItemEditor.setMinimumSize(QtCore.QSize(500, 300))
        TextItemEditor.setSizeGripEnabled(True)
        TextItemEditor.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(TextItemEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.list_favourites = QtGui.QListView(TextItemEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_favourites.sizePolicy().hasHeightForWidth())
        self.list_favourites.setSizePolicy(sizePolicy)
        self.list_favourites.setAlternatingRowColors(True)
        self.list_favourites.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.list_favourites.setObjectName(_fromUtf8("list_favourites"))
        self.verticalLayout.addWidget(self.list_favourites)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btn_add = QtGui.QPushButton(TextItemEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)
        self.btn_add.setObjectName(_fromUtf8("btn_add"))
        self.horizontalLayout.addWidget(self.btn_add)
        self.btn_edit = QtGui.QPushButton(TextItemEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_edit.sizePolicy().hasHeightForWidth())
        self.btn_edit.setSizePolicy(sizePolicy)
        self.btn_edit.setObjectName(_fromUtf8("btn_edit"))
        self.horizontalLayout.addWidget(self.btn_edit, QtCore.Qt.AlignLeft)
        self.btn_delete = QtGui.QPushButton(TextItemEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_delete.sizePolicy().hasHeightForWidth())
        self.btn_delete.setSizePolicy(sizePolicy)
        self.btn_delete.setObjectName(_fromUtf8("btn_delete"))
        self.horizontalLayout.addWidget(self.btn_delete)
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TextItemEditor)
        QtCore.QMetaObject.connectSlotsByName(TextItemEditor)

    def retranslateUi(self, TextItemEditor):
        TextItemEditor.setWindowTitle(_translate("TextItemEditor", "Text Item Editor", None))
        self.btn_add.setText(_translate("TextItemEditor", "Add", None))
        self.btn_edit.setText(_translate("TextItemEditor", "Edit", None))
        self.btn_delete.setText(_translate("TextItemEditor", "Delete", None))

