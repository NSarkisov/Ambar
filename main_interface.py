from PyQt5 import QtCore, QtWidgets
import dialog_table
from dialog_table import Ui_Dialog
from functools import partial
from io import BytesIO


class Ui_MainWindow(object):
    def __init__(self):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)

    def setupUi(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(800, 603)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton.setGeometry(QtCore.QRect(40, 50, 231, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2.setGeometry(QtCore.QRect(40, 150, 231, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3.setGeometry(QtCore.QRect(40, 250, 231, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4.setGeometry(QtCore.QRect(40, 350, 231, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5.setGeometry(QtCore.QRect(40, 450, 231, 51))
        self.pushButton_5.setObjectName("pushButton_5")

        main_window.setStyleSheet(
            "background-image: url(28.jpg); background-repeat: no-repeat; background-position: center;")
        main_window.setCentralWidget(self.centralwidget)

        self.pushButton.setStyleSheet("background: #0d6e79; font: bold large serif;")
        self.pushButton_2.setStyleSheet("background: #0d6e79; font: bold large serif;")
        self.pushButton_3.setStyleSheet("background: #0d6e79; font: bold large serif;")
        self.pushButton_4.setStyleSheet("background: #0d6e79; font: bold large serif;")
        self.pushButton_5.setStyleSheet("background: #0d6e79; font: bold large serif;")

        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")

        file_menu = self.menubar.addMenu("Файл")
        edit_menu = self.menubar.addMenu("Правка")
        help_menu = self.menubar.addMenu("Помощь")
        new_action = QtWidgets.QAction("Новый", file_menu)
        open_action = QtWidgets.QAction("Открыть", file_menu)
        save_action = QtWidgets.QAction("Сохранить", file_menu)
        exit_action = QtWidgets.QAction("Выход", file_menu)
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # Добавление разделителя
        file_menu.addAction(exit_action)
        cut_action = QtWidgets.QAction("Вырезать", edit_menu)
        copy_action = QtWidgets.QAction("Копировать", edit_menu)
        paste_action = QtWidgets.QAction("Вставить", edit_menu)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        about_action = QtWidgets.QAction("О программе", help_menu)
        help_menu.addAction(about_action)
        # exit_action.triggered.connect(main_window.close())
        # about_action.triggered.connect(self.show_about_dialog)

        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):

        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Manager"))

        self.pushButton.setText(_translate("MainWindow", "Склады 🏭 🏚"))
        self.pushButton_2.setText(_translate("MainWindow", "Товары"))
        self.pushButton_3.setText(_translate("MainWindow", "Заказы 🛒🛍"))
        self.pushButton_4.setText(_translate("MainWindow", "Клиенты 👩‍💼🧑‍💼"))
        self.pushButton_5.setText(_translate("MainWindow", "Товары на складе 🏭🛒"))

        self.pushButton.clicked.connect(partial(self.table_dialog, "Склады"))
        self.pushButton_2.clicked.connect(partial(self.table_dialog, "Товары"))
        self.pushButton_3.clicked.connect(partial(self.table_dialog, "Заказы"))
        self.pushButton_4.clicked.connect(partial(self.table_dialog, "Клиенты"))
        self.pushButton_5.clicked.connect(partial(self.table_dialog, "Товар_на_складе"))

    def table_dialog(self, table_name):
        Dialog = QtWidgets.QDialog()
        ui_table = Ui_Dialog()
        ui_table.table_name = table_name
        ui_table.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
