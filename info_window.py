from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QMessageBox, QHeaderView, QVBoxLayout
from functools import partial
from PyQt5.QtGui import QPixmap, QIcon, QImage 
from io import BytesIO
from PIL import Image
import io

class Change_window(object):
   
    num = 0
    image = ""
    
    
    def setupChange(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(774, 559)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(30, 70, 711, 361))
        self.tableWidget.setObjectName("tableWidget")
        self.pushButton0 = QtWidgets.QPushButton(Dialog)
        self.pushButton0.setGeometry(QtCore.QRect(30, 20, 50, 28))
        self.pushButton0.setObjectName("pushButton0")
        self.pushButton_1 = QtWidgets.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(300, 20, 131, 28))
        self.pushButton_1.setObjectName("pushButton0")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(602, 20, 131, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 20, 131, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 470, 131, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setGeometry(QtCore.QRect(450, 470, 131, 28))
        self.pushButton_4.setObjectName("pushButton_4")
    
        self.retranslateChange(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.show_info(self.image)
        
    def retranslateChange(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton0.setText(_translate("Dialog", "+"))
        self.pushButton_1.setText(_translate("Dialog", "Изменить"))
        self.pushButton.setText(_translate("Dialog", "Удалить"))
        self.pushButton_2.setText(_translate("Dialog", "Добавить"))
        self.pushButton_3.setText(_translate("Dialog", "Отменить"))
        self.pushButton_4.setText(_translate("Dialog", "Применить"))
        
        # self.pushButton0.clicked.connect(partial(self.plus))
        # self.pushButton_1.clicked.connect(partial(self.change, self.table_name, self.column_names))
        # self.pushButton.clicked.connect(partial(self.delete, self.table_name))
        # self.pushButton_2.clicked.connect(partial(self.add, self.table_name, self.column_names))
        # self.pushButton_3.clicked.connect(partial(self.cancel))
        # self.pushButton_4.clicked.connect(partial(self.apply)) 
        
    def show_info(self, image):
        print(image)
        image = BytesIO(image)
        image_bytes = image.read()
        image = QtGui.QImage.fromData(image_bytes)
        image = image.scaled(400, 300, QtCore.Qt.KeepAspectRatio)
        image_dialog = QtWidgets.QDialog()
        image_dialog.setWindowTitle("Изображение")
        label = QtWidgets.QLabel(image_dialog)
        label.setPixmap(QtGui.QPixmap.fromImage(image))
        label.setScaledContents(True)
        layout = QtWidgets.QVBoxLayout(image_dialog)
        layout.addWidget(label)
        image_dialog.exec_()

          
        
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Change_window()
    ui.setupChange(Dialog)
    Dialog.show()
    sys.exit(app.exec_())