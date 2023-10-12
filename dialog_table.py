from info_window import Change_window
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QHeaderView, QVBoxLayout, QLabel, QComboBox, QTableWidgetItem
from functools import partial
import sqlite3 as sl
from PyQt5.QtGui import QPixmap, QIcon, QImage
from io import BytesIO
import io

con = sl.connect('Manager.db')


class Ui_Dialog(object):
    TABLE = ""
    num = 0
    table_name = ""
    column_names = ""
    querys = []

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(774, 559)

        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(30, 70, 711, 361))
        self.tableWidget.setObjectName("tableWidget")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(602, 20, 131, 28))
        self.pushButton.setObjectName("pushButton")

        self.pushButton0 = QtWidgets.QPushButton(Dialog)
        self.pushButton0.setGeometry(QtCore.QRect(30, 20, 50, 28))
        self.pushButton0.setObjectName("pushButton0")

        self.pushButton_1 = QtWidgets.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(300, 20, 131, 28))
        self.pushButton_1.setObjectName("pushButton0")

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

        if self.table_name == "Товар_на_складе":
            Dialog.resize(1000, 800)
            self.tableWidget.setGeometry(QtCore.QRect(10, 60, 980, 731))
            self.pushButton0.setGeometry(QtCore.QRect(10, 20, 50, 28))  # +
            self.pushButton_1.setGeometry(QtCore.QRect(470, 20, 131, 28))  # Изменить
            self.pushButton_2.setGeometry(QtCore.QRect(600, 20, 131, 28))  # Добавить
            self.pushButton.setGeometry(QtCore.QRect(730, 20, 131, 28))  # Удалить
            self.pushButton_4.setGeometry(QtCore.QRect(340, 20, 131, 28))  # Применить
            self.pushButton_3.setGeometry(QtCore.QRect(860, 20, 131, 28))  # Отменить
            self.pushButton_3.setEnabled(True)
            self.comboBox = QtWidgets.QComboBox(Dialog)
            self.comboBox.setGeometry(QtCore.QRect(60, 20, 280, 28))

        self.show_table(self.table_name)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", self.table_name))
        self.pushButton0.setText(_translate("Dialog", "+"))
        self.pushButton_1.setText(_translate("Dialog", "Изменить"))
        self.pushButton.setText(_translate("Dialog", "Удалить"))
        self.pushButton_2.setText(_translate("Dialog", "Добавить"))
        self.pushButton_3.setText(_translate("Dialog", "Отменить"))
        self.pushButton_4.setText(_translate("Dialog", "Применить"))

        self.pushButton0.clicked.connect(partial(self.plus, self.table_name))
        self.pushButton_1.clicked.connect(partial(self.change, self.table_name, self.column_names))
        self.pushButton.clicked.connect(partial(self.delete, self.table_name))
        self.pushButton_2.clicked.connect(partial(self.add, self.table_name, self.column_names))
        self.pushButton_3.clicked.connect(partial(self.cancel))
        self.pushButton_4.clicked.connect(partial(self.apply))

    def show_table(self, table_name):
        with con:
            if table_name == "Товар_на_складе":
                column_names = ["id", "Склад", "Название", "Количество", "Дата приёма", "Поставщик", "Продано",
                                "Перемещено", "Cписано"]
                inf = con.execute('SELECT Товар_на_складе.id, название, имя_товара, количество, '
                                  'дата_приёма, поставщик, продано, перемещено, списано FROM '
                                  'Товар_на_складе '
                                  'INNER JOIN Склады ON Товар_на_складе.id_склада = Склады.id '
                                  'INNER JOIN Товары ON Товар_на_складе.id_товара = Товары.id').fetchall()
                column = ', '.join(column_names)
                inf = [list(x) for x in inf]
            elif table_name == 'Заказы':
                column_names = ['Номер заказа', 'Клиенты', 'Товары', 'Количество', 'Дата заказа']
                inf = con.execute(
                    f'SELECT Заказы.id, Клиенты.имя_клиента, Товары.имя_товара, Заказы.количество, '
                    f'Заказы.дата_заказа FROM "Заказы" JOIN "Клиенты" ON Заказы.id_клиента = Клиенты.id '
                    f'JOIN "Товары" ON Заказы.id_товара = Товары.id').fetchall()
                print(inf)
                inf = [list(x) for x in inf]
                column = ', '.join(column_names)
            else:
                header = con.execute(f'PRAGMA table_info({table_name})').fetchall()
                column_names = [column[1] for column in header]
                column = ', '.join(column_names)
                inf = con.execute(f'SELECT {column} FROM {table_name}').fetchall()
                inf = [list(x) for x in inf]
                if table_name == 'Товары':
                    for i in inf:
                        i[4] = BytesIO(i[4])
        table = [column_names] + inf
        self.column_names = column
        self.tableWidget.setRowCount(len(table))
        self.tableWidget.setColumnCount(len(table[0]))

        # Заполнение таблицы данными
        info_dict = {}

        for row, data in enumerate(table):
            if row not in info_dict.keys():
                info_dict[row] = data
            for col, value in enumerate(data):
                if isinstance(value, io.BytesIO):
                    item = QtWidgets.QTableWidgetItem("Картинка")
                    item.setData(Qt.UserRole, value)  # Сохраняем байты изображения в пользовательском роле
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                else:
                    item = QtWidgets.QTableWidgetItem(str(value))

                self.tableWidget.setItem(row, col, item)

        if table_name == "Заказы":
            self.tableWidget.setColumnHidden(0, False)
        elif table_name == "Товар_на_складе":
            self.tableWidget.setColumnHidden(0, True)
            self.tableWidget.setColumnHidden(1, True)
            storages = []
            for index, storage in info_dict.items():
                if storage[1] not in storages and index != 0:
                    storages.append(storage[1])
            for storage in storages:
                self.comboBox.addItem(storage)
            self.on_combobox_changed()
            self.comboBox.currentIndexChanged.connect(partial(self.on_combobox_changed))
        else:
            self.tableWidget.setColumnHidden(0, True)  # скрытый столбец id от пользователя
        # Handle_cell_clicked, который вызывается при клике на ячейку таблицы. Обработчик получает индексы нажатой
        # ячейки и затем использует метод setSelected(True) для каждой ячейки в столбце, чтобы выделить весь столбец.
        # Растягивание всех столбцов
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.vertical_header_labels = [str(i) for i in range(self.tableWidget.rowCount())]
        self.tableWidget.setVerticalHeaderLabels(self.vertical_header_labels)
        empty_box = QTableWidgetItem('')
        self.tableWidget.setVerticalHeaderItem(0, empty_box)
        self.tableWidget.cellClicked.connect(partial(self.handle_cell_clicked, table_name, info_dict))

    def vertical_header(self):
        table = self.tableWidget
        self.vertical_header_labels.append(str(table.rowCount() - 1))
        table.setVerticalHeaderLabels(self.vertical_header_labels)
        empty_box = QTableWidgetItem('')
        table.setVerticalHeaderItem(0, empty_box)

    def on_combobox_changed(self):
        selected_value = self.comboBox.currentText()
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 1)
            if item is not None and item.text() == selected_value:
                self.tableWidget.showRow(row)
            else:
                if row != 0:
                    self.tableWidget.hideRow(row)

    def handle_cell_clicked(self, table_name, info_dict, row, column):
        if column == 4 and row != 0 and table_name != "Товар_на_складе":
            Dialog = QtWidgets.QDialog()
            change_window = Change_window()
            for el in info_dict:
                if row == el:
                    id = info_dict[el][0]
                    name_cell = info_dict[el][1]
                    image = con.execute(f'SELECT "картинка" FROM {table_name} WHERE id = {id}').fetchall()[0][0]
            change_window.image = BytesIO(image)
            change_window.name = name_cell
            change_window.table_name = table_name
            change_window.id_image = id
            change_window.setupChange(Dialog)
            Dialog.show()
            Dialog.exec_()
        if row == 0:
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row, column)
                if item:
                    item.setSelected(True)

    def plus(self, table_name):
        if table_name == 'Заказы':
            self.Dialog_add_order = QtWidgets.QDialog()
            self.Dialog_add_order.setObjectName("Dialog_add_order")
            self.Dialog_add_order.resize(450, 350)
            self.Dialog_add_order.setWindowTitle("Добавление заказа")
            self.label = QtWidgets.QLabel(self.Dialog_add_order)
            self.label.setGeometry(QtCore.QRect(20, 80, 100, 16))
            self.label.setObjectName("label")
            self.label.setText("Выберите товар")
            self.label_1 = QtWidgets.QLabel(self.Dialog_add_order)
            self.label_1.setGeometry(QtCore.QRect(20, 120, 120, 28))
            self.label_1.setObjectName("label_1")
            self.label_1.setText("Количество")
            self.label_2 = QtWidgets.QLabel(self.Dialog_add_order)
            self.label_2.setGeometry(QtCore.QRect(20, 40, 120, 28))
            self.label_2.setObjectName("label_2")
            self.label_2.setText("Имя клиента")
            self.label_3 = QtWidgets.QLabel(self.Dialog_add_order)
            self.label_3.setGeometry(QtCore.QRect(20, 160, 120, 28))
            self.label_3.setObjectName("label_3")
            self.label_3.setText("Доступно")
            self.label_4 = QtWidgets.QLabel(self.Dialog_add_order)
            self.label_4.setGeometry(QtCore.QRect(20, 200, 120, 28))
            self.label_4.setObjectName("label_4")
            self.label_4.setText("Дата")
            self.dateEdit = QtWidgets.QDateEdit(self.Dialog_add_order)
            self.dateEdit.setGeometry(QtCore.QRect(130, 200, 255, 28))
            self.dateEdit.setObjectName("dateEdit")
            self.comboBox = QtWidgets.QComboBox(self.Dialog_add_order)
            self.comboBox.setGeometry(QtCore.QRect(130, 80, 255, 28))
            self.comboBox.setObjectName("comboBox")
            self.comboBox_1 = QtWidgets.QComboBox(self.Dialog_add_order)
            self.comboBox_1.setGeometry(QtCore.QRect(130, 40, 255, 28))
            self.comboBox_1.setObjectName("comboBox_1")
            self.textEdit = QtWidgets.QTextEdit(self.Dialog_add_order)
            self.textEdit.setGeometry(QtCore.QRect(130, 160, 255, 28))
            self.textEdit.setObjectName("textEdit")
            self.textEdit_1 = QtWidgets.QTextEdit(self.Dialog_add_order)
            self.textEdit_1.setGeometry(QtCore.QRect(130, 120, 255, 28))
            self.textEdit_1.setObjectName("textEdit_1")
            self.pushButton_6 = QtWidgets.QPushButton(self.Dialog_add_order)
            self.pushButton_6.setGeometry(QtCore.QRect(90, 250, 131, 28))
            self.pushButton_6.setObjectName("pushButton0")
            self.pushButton_6.setText("Ok")
            self.pushButton_7 = QtWidgets.QPushButton(self.Dialog_add_order)
            self.pushButton_7.setGeometry(QtCore.QRect(230, 250, 131, 28))
            self.pushButton_7.setObjectName("pushButton_1")
            self.pushButton_7.setText("Отмена")
            self.comboBox.currentIndexChanged.connect(self.updateAmount)
            with con:
                goods = con.execute(f'SELECT имя_товара FROM Товары').fetchall()
                customers = con.execute(f'SELECT имя_клиента FROM Клиенты').fetchall()

                for good in goods:
                    self.comboBox.addItem(good[0])
                for customer in customers:
                    self.comboBox_1.addItem(customer[0])
                column_names = con.execute(f'PRAGMA table_info({table_name})').fetchall()
                column = [column[1] for column in column_names]
            self.pushButton_6.clicked.connect(partial(self.add_in_table, self.table_name, column))
            self.pushButton_7.clicked.connect(partial(self.close))
            self.Dialog_add_order.exec_()
        else:
            # # Получаем текущее количество строк в таблице
            table = self.tableWidget
            rowCount = table.rowCount()
            # Вставляем новую строку в таблицу
            table.insertRow(rowCount)
            if table_name == "Товар_на_складе":
                table.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(self.comboBox.currentText()))
                self.cell_combobox = QtWidgets.QComboBox()
                with con:
                    products = con.execute("SELECT имя_товара FROM Товары").fetchall()
                    products = [product[0] for product in products]
                    self.cell_combobox.addItems(products)
                table.setCellWidget(rowCount, 2, self.cell_combobox)
            self.vertical_header()

    def updateAmount(self):
        selected_good = self.comboBox.currentText()
        if selected_good:
            with con:
                info_amount = con.execute(f'SELECT количество, продано, перемещено, '
                                          f'списано FROM "Товар_на_складе" INNER JOIN Товары ON '
                                          f'Товар_на_складе.id_товара = Товары.id'
                                          f' WHERE Товары.имя_товара = "{selected_good}"').fetchall()
                for el in info_amount:
                    amount = el[0]
                    sold = el[1]
                    moved = el[2]
                    written_off = el[3]
                available = amount - sold - moved - written_off
                self.textEdit.setPlainText(str(available))
        else:
            self.textEdit.clear()

    def add_in_table(self, table_name, column):
        column = [i for i in column if
                  i != 'id']  # названия столбцов, кот необх добавить в запрос для внесения изменений в бд
        column = ', '.join(column)
        print(column)
        name = self.comboBox_1.currentText()
        good = self.comboBox.currentText()
        amount = self.textEdit_1.toPlainText()
        date = self.dateEdit.date().toString('yyyy-MM-dd')

        with con:
            con.execute(f'INSERT INTO {table_name} ({column}) '
                        f'VALUES ((SELECT id FROM Клиенты WHERE имя_клиента = "{name}"), '
                        f'(SELECT id FROM Товары WHERE имя_товара = "{good}"), {amount}, "{date}")')
            # !!!!!Нужно добавить логику обработки столбца продано в табл Товары_на_складе
        print(table_name)
        self.show_table(table_name)
        self.close()

    def close(self):
        self.Dialog_add_order.close()

    def is_data(self, table):  # забираю информацию из выделенных ячеек,
        # возвращает список объектов QTableWidgetSelectionRange, представляющих выбранные диапазоны строк и столбцов
        # в таблице.
        selected_model = table.selectionModel()
        selected_ranges = selected_model.selectedRows()
        data = []
        for line in selected_ranges:
            row_data = []
            for column in range(table.columnCount()):
                item = table.item(line.row(), column)
                if isinstance(table.cellWidget(line.row(), column), QComboBox):
                    row_data.append(table.cellWidget(line.row(), column).currentText())
                elif item is not None:
                    cell_data = item.text()
                    row_data.append(cell_data)
                else:
                    row_data.append("")
            data.append(row_data)
        return data

    def change(self, table_name, column_names):
        table = self.tableWidget
        selected_model = table.selectionModel()
        selected_line = selected_model.selectedRows()
        if selected_line:
            data = self.is_data(table)
            column = column_names
            for sublist in data:
                # repr() возвращает строковое представление объекта, включая кавычки, если это строка, чтоб ? в
                # запросе передавался в ""
                if table_name == "Товар_на_складе":
                    with con:
                        storage_index = con.execute(f"SELECT id FROM Склады "
                                                    f" WHERE название = '{sublist[1]}'").fetchall()[0][0]
                        product_index = con.execute(f"SELECT id FROM Товары "
                                                    f"WHERE имя_товара = '{sublist[2]}'").fetchall()[0][0]
                        sublist[1] = storage_index
                        sublist[2] = product_index
                        header = con.execute(f'PRAGMA table_info({table_name})').fetchall()
                        column_names = [column[1] for column in header]
                        column = ', '.join(column_names[1:-1])
                    for i in range(len(sublist)):
                        if isinstance(sublist[i], str) and sublist[i].isdigit():
                            sublist[i] = int(sublist[i])
                val = ', '.join(repr(item) for item in sublist[1:])
                self.querys.append(f'UPDATE OR IGNORE {table_name} SET ({column}) = ({val}) WHERE id = {sublist[0]}')
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
        else:
            # Если нет выделенных диапазонов, выводим сообщение пользователю
            QMessageBox.information(table, 'Внимание!', 'Пожалуйста, выделите строку.')

    def add(self, table_name, column_names):
        table = self.tableWidget
        selected_model = table.selectionModel()
        selected_line = selected_model.selectedRows()
        if selected_line:
            data = self.is_data(table)
            for sublist in data:
                # repr() возвращает строковое представление объекта, включая кавычки, если это строка, чтоб ? в
                # запросе передавался в ""
                if table_name == "Товар_на_складе":
                    with con:
                        storage_index = con.execute(f"SELECT id FROM Склады "
                                                    f"WHERE название = '{sublist[1]}'").fetchall()[0][0]
                        sublist[2] = self.cell_combobox.currentText()
                        product_index = con.execute(f"SELECT id FROM Товары "
                                                    f"WHERE имя_товара = '{sublist[2]}'").fetchall()[0][0]
                        sublist[1] = storage_index
                        sublist[2] = product_index
                        header = con.execute(f'PRAGMA table_info({table_name})').fetchall()
                        column_names = [column[1] for column in header]
                        column = ', '.join(column_names[1:-1])
                    for i in range(len(sublist)):
                        if isinstance(sublist[i], str) and sublist[i].isdigit():
                            sublist[i] = int(sublist[i])
                else:
                    column_names = column_names.split(',')
                    column = [i for i in column_names if
                              i != 'id']  # названия столбцов, кот необх добавить в запрос для внесения изменений в бд
                    column = ', '.join(column)
                val = ', '.join(repr(item) for item in sublist[1:])
                self.querys.append(f'INSERT INTO {table_name} ({column}) VALUES ({val})')
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
        else:
            # Если нет выделенных диапазонов, выводим сообщение пользователю
            QMessageBox.information(table, 'Внимание!', 'Пожалуйста, выделите строку.')

    def delete(self, table_name):
        table = self.tableWidget
        selected_model = table.selectionModel()
        selected_lines = selected_model.selectedRows()
        selected_rows = []
        for line in selected_lines:
            selected_rows.append(line.row())
        if selected_lines:
            data = self.is_data(table)
            for sublist in data:
                id = sublist[0]
                if id != "":
                    # возвращает список объектов QTableWidgetSelectionRange, представляющих выбранные диапазоны строк и
                    # столбцов в таблице.
                    self.querys.append(f'DELETE FROM {table_name} WHERE id = {id}')
                    # Активировать кнопки "Применить"
                    self.pushButton_4.setEnabled(True)
        else:
            QMessageBox.information(table, 'Внимание!', 'Пожалуйста, выделите строку.')
        for row in sorted(selected_rows, reverse=True):
            table.removeRow(row)
        self.vertical_header()

    def apply(self):
        print(self.querys)
        for query in self.querys:
            # print(query)
            with con:
                con.execute(query)
        self.querys.clear()  # очищаю список запросов на удаление после нажатия кнопки применить
        self.pushButton_4.setEnabled(False)
        table = self.tableWidget
        selected_model = table.selectionModel()
        selected_lines = selected_model.selectedRows()
        for line in selected_lines:
            for column in range(table.columnCount()):
                if isinstance(table.cellWidget(line.row(), column), QComboBox):
                    cell_widget = table.cellWidget(line.row(), column)
                    current_text = cell_widget.currentText()
                    table.removeCellWidget(line.row(), column)
                    new_item = QTableWidgetItem(current_text)
                    table.setItem(line.row(), column, new_item)
        self.show_table(self.table_name)

    def cancel(self):
        self.querys.clear()
        dialog = self.tableWidget.window()
        dialog.close()
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
