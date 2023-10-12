from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QMessageBox, QHeaderView, QVBoxLayout
from functools import partial
from PyQt5.QtGui import QPixmap
from io import BytesIO
import sqlite3 as sl

con = sl.connect('Manager.db')

class Change_window(object):
   
    num = 0
    image = ""
    name = ""
    table_name = ""
    id_image = ""
    querys = []
   
    
    def setupChange(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(774, 559)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 70, 711, 361))
        self.label.setObjectName("label")
        
        self.pushButton_1 = QtWidgets.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(450, 20, 131, 28))
        self.pushButton_1.setObjectName("pushButton0")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(602, 20, 131, 28))
        self.pushButton_2.setObjectName("pushButton")
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
        Dialog.setWindowTitle(_translate("Dialog", self.name))
        self.pushButton_1.setText(_translate("Dialog", "Изменить"))
        self.pushButton_2.setText(_translate("Dialog", "Удалить"))
        self.pushButton_3.setText(_translate("Dialog", "Отменить"))
        self.pushButton_4.setText(_translate("Dialog", "Применить"))
        
        self.pushButton_1.clicked.connect(partial(self.open_file_explorer, self.table_name, self.id_image))
        self.pushButton_2.clicked.connect(partial(self.delete, self.table_name, self.id_image))
        self.pushButton_3.clicked.connect(partial(self.cancel))
        self.pushButton_4.clicked.connect(partial(self.apply)) 
        
    def show_info(self, image):
        image_bytes = image.read()
        image = QtGui.QImage.fromData(image_bytes)
        image = image.scaled(400, 300, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label.setScaledContents(True)
       
    def open_file_explorer(self, table_name, id_image):
        file_dialog = QtWidgets.QFileDialog()
        file_path = file_dialog.getOpenFileName(self.label, 'Выберите файл', '', 'Все файлы (*.*);;Изображения (*.png *.jpg *.jpeg)')
        #print(file_path)   #('D:/ITYUIT/Proj2 Warehouses/Ambar/28.jpg', 'All Files (*)')
        if file_path:
            with open(file_path[0], 'rb') as file:
                image_data = file.read()
            image = QtGui.QImage.fromData(image_data)
            pixmap = QPixmap(image)
            self.label.setPixmap(pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            file_dialog.close()
        self.querys.append([f'UPDATE OR IGNORE {table_name} SET картинка = ? WHERE id = {id_image}', BytesIO(image_data)])
    
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)        
    
    def delete(self, table_name, id_image):
        self.querys.append([f'UPDATE OR IGNORE {table_name} SET "картинка" = NULL WHERE id = {id_image}'])    
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
    
    def apply(self):
        for query in self.querys:
            print(query)
            if len(query) > 1:
                with con:
                    con.execute(query[0], [sl.Binary(query[1].read())])
            else:
                with con:
                    con.execute(query[0])           
        self.querys = []   
        # Получение родительского окна (диалогового окна) метки
        dialog = self.label.window()
        # Закрытие диалогового окна
        dialog.close()
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        
    def cancel(self):
        self.querys = []
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Change_window()
    ui.setupChange(Dialog)
    Dialog.show()
    sys.exit(app.exec_())