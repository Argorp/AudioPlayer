# Form implementation generated from reading ui file 'author.ui'
#
# Created by: PyQt6 UI code generator 6.8.0.dev2410211537
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Author_Form(object):
    def setupUi(self, Author_Form):
        Author_Form.setObjectName("Author_Form")
        Author_Form.resize(516, 378)
        self.label = QtWidgets.QLabel(parent=Author_Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 441, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(parent=Author_Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 60, 321, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(parent=Author_Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 120, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Author_Form)
        QtCore.QMetaObject.connectSlotsByName(Author_Form)

    def retranslateUi(self, Author_Form):
        _translate = QtCore.QCoreApplication.translate
        Author_Form.setWindowTitle(_translate("Author_Form", "Form"))
        self.label.setText(_translate("Author_Form", "Введите имя исполнителя:"))
        self.pushButton.setText(_translate("Author_Form", "Готово!"))