# Form implementation generated from reading ui file 'choose.ui'
#
# Created by: PyQt6 UI code generator 6.8.0.dev2410211537
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(352, 259)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(60, 20, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.Author = QtWidgets.QPushButton(parent=Form)
        self.Author.setGeometry(QtCore.QRect(20, 60, 111, 51))
        self.Author.setObjectName("Author")
        self.Song = QtWidgets.QPushButton(parent=Form)
        self.Song.setGeometry(QtCore.QRect(180, 60, 111, 51))
        self.Song.setObjectName("Song")
        self.Genre = QtWidgets.QPushButton(parent=Form)
        self.Genre.setGeometry(QtCore.QRect(110, 140, 111, 51))
        self.Genre.setObjectName("Genre")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Выберите, что вы хотите добавить"))
        self.Author.setText(_translate("Form", "Исполнителя"))
        self.Song.setText(_translate("Form", "Песню"))
        self.Genre.setText(_translate("Form", "Жанр"))
