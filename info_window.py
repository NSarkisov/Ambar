from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QHeaderView, QVBoxLayout, QWidget, QApplication
from functools import partial
from PyQt5.QtGui import QPixmap, QIcon, QImage
from io import BytesIO
import sqlite3 as sl
from urllib import request

con = sl.connect('Manager.db')


class Change_window(object):
    num = 0
    image = ""
    name = ""
    table_name = ""
    id_image = ""
    querys = []

    def __init__(self):
        self.accept_deleting = QtWidgets.QDialog()
        self.accept_deleting.resize(350, 150)
        self.accept_deleting.setWindowTitle("Подтвердите действие")

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
        self.pushButton_3.setEnabled(True)
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
        self.pushButton_2.clicked.connect(partial(self.delete, self.table_name, self.id_image, "confirm"))
        self.pushButton_3.clicked.connect(partial(self.cancel))
        self.pushButton_4.clicked.connect(partial(self.apply))

    def show_info(self, image):
        if image is not None:
            image_bytes = image.read()
            picture = QImage.fromData(image_bytes)
            picture = picture.scaled(400, 300, Qt.KeepAspectRatio)
            self.label.setPixmap(QPixmap.fromImage(picture))
            self.label.setScaledContents(True)
        self.label.setStyleSheet("border: 1px solid black;")

    def open_file_explorer(self, table_name, id_image):
        # print(f'id-im = {id_image}')
        file_dialog = QtWidgets.QFileDialog()
        file_path = file_dialog.getOpenFileName(self.label, 'Выберите файл', '',
                                                'Все файлы (*.*);;Изображения (*.png *.jpg *.jpeg)')
        # print(file_path)   #('D:/ITYUIT/Proj2 Warehouses/Ambar/28.jpg', 'All Files (*)')
        file = file_path[0]
        if file != '':
            print(file_path)
            print("открылся проводник")
            with open(file, 'rb') as file:
                image_data = file.read()
            image = QtGui.QImage.fromData(image_data)
            Change_window.image = image
            pixmap = QPixmap(image)
            self.label.setPixmap(pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio))
            if id_image == None:
                QMessageBox.information(file_dialog, 'Внимание!', 'Изображение успешно добавлено.')
                self.label.window().close()
            else:
                self.querys.append(
                [f'UPDATE OR IGNORE {table_name} SET картинка = ? WHERE id = {id_image}', BytesIO(image_data)])
                self.pushButton_3.setEnabled(True)
                self.pushButton_4.setEnabled(True)

    def delete(self, table_name, id_image, operation):

        if operation == "confirm":
            text = QtWidgets.QLabel(self.accept_deleting)
            text.setGeometry(30, 40, 291, 21)
            text.setText("Вы действительно хотите удалить изображение?")

            yes_btn = QtWidgets.QPushButton(self.accept_deleting)
            yes_btn.setText("Да")
            yes_btn.setGeometry(190, 80, 141, 41)
            yes_btn.setStyleSheet("QPushButton { background:"
                                  " qlineargradient(x1:0, y1:0, x2:1, y2:1,"
                                  " stop:0 #FF5722, stop:1 #E64A19);"
                                  " color: white; border: none; padding: 10px 20px; border-radius: 5px; }"
                                  "QPushButton:hover { background:"
                                  " qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F4511E, stop:1 #D84315); }"
                                  "QPushButton:pressed { background:"
                                  " qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E64A19, stop:1 #BF360C); }")

            no_btn = QtWidgets.QPushButton(self.accept_deleting)
            no_btn.setGeometry(20, 80, 141, 41)
            no_btn.setText("Нет")

            yes_btn.clicked.connect(partial(self.delete, table_name, id_image, "yes"))
            no_btn.clicked.connect(partial(self.delete, table_name, id_image, "no"))
            self.accept_deleting.exec_()

        elif operation == "yes":
            self.querys.append([f'UPDATE OR IGNORE {table_name} SET "картинка" = NULL WHERE id = {id_image}'])
            # Активировать кнопки "Применить" и "Отменить"
            self.label.clear()
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.accept_deleting.close()

        elif operation == "no":
            self.accept_deleting.close()

    def apply(self):
        for query in self.querys:
            if len(query) > 1:
                with con:
                    con.execute(query[0], [sl.Binary(query[1].read())])
            else:
                with con:
                    con.execute(query[0])
        self.querys.clear()
        # Получение родительского окна (диалогового окна) метки
        dialog = self.label.window()
        # Закрытие диалогового окна
        dialog.close()
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        # QMessageBox.information(self.label, 'Внимание!', 'Картинка удалена.')

    def cancel(self):
        self.querys.clear()
        dialog = self.label.window()
        dialog.close()
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
