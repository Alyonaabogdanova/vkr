import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QLabel,QWidget,QDateEdit, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QTableWidget,QHBoxLayout, QTableWidgetItem, QMessageBox,QInputDialog
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
class AuthorizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Авторизация")
        self.setGeometry(300, 300, 300, 100)
        layout = QVBoxLayout()

        self.loginEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

        loginButton = QPushButton("Войти")
        loginButton.clicked.connect(self.checkAuthorization)

        layout.addWidget(self.loginEdit)
        layout.addWidget(self.passwordEdit)
        layout.addWidget(loginButton)

        self.setLayout(layout)

    def checkAuthorization(self):
        login = self.loginEdit.text()
        password = self.passwordEdit.text()

        if login == "alena" and password == "admin":
            self.mainWindow = MainWindow()
            self.mainWindow.show()
            self.close()
        else:
            print("Неверный логин или пароль")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Главное меню")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        clientsButton = QPushButton("Клиенты")
        clientsButton.clicked.connect(self.openClientsWindow)

        scheduleButton = QPushButton("Расписание занятий")
        scheduleButton.clicked.connect(self.openScheduleWindow)

        salesButton = QPushButton("Продажи")
        salesButton.clicked.connect(self.openSalesWindow)

        storageButton = QPushButton("Склад")
        storageButton.clicked.connect(self.openStorageWindow)

        reportsButton = QPushButton("Документы")
        reportsButton.clicked.connect(self.openReportsWindow)

        layout.addWidget(clientsButton)
        layout.addWidget(scheduleButton)
        layout.addWidget(salesButton)
        layout.addWidget(storageButton)
        layout.addWidget(reportsButton)

        self.setLayout(layout)

    def openClientsWindow(self):
        self.clientsWindow = ClientsWindow()
        self.clientsWindow.show()

    def openScheduleWindow(self):
        self.scheduleWindow = ScheduleWindow()
        self.scheduleWindow.show()

    def openSalesWindow(self):
        self.salesWindow = SalesWindow()
        self.salesWindow.show()

    def openStorageWindow(self):
        self.storageWindow = StorageWindow()
        self.storageWindow.show()

    def openReportsWindow(self):
        self.reportsWindow = ReportsWindow()
        self.reportsWindow.show()

class ClientsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Клиенты")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.clientsTable = QTableWidget()
        self.clientsTable.setRowCount(0)
        self.clientsTable.setColumnCount(5)
        self.clientsTable.setHorizontalHeaderItem(0, QTableWidgetItem("ФИО"))
        self.clientsTable.setHorizontalHeaderItem(1, QTableWidgetItem("Номер телефона"))
        self.clientsTable.setHorizontalHeaderItem(2, QTableWidgetItem("Дата рождения"))
        self.clientsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Логин"))
        self.clientsTable.setHorizontalHeaderItem(4, QTableWidgetItem("Пароль"))

        layout.addWidget(self.clientsTable)

        buttonLayout = QHBoxLayout()
        addButton = QPushButton("Добавить")
        addButton.clicked.connect(self.addClient)
        buttonLayout.addWidget(addButton)

        deleteButton = QPushButton("Удалить")
        deleteButton.clicked.connect(self.deleteClient)
        buttonLayout.addWidget(deleteButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.loadClients()


    def loadClients(self):
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("mydatabase.db")
            query = QSqlQuery("SELECT * FROM clients", db)
            row = 0
            while query.next():
                self.clientsTable.insertRow(row)
                self.clientsTable.setItem(row, 0, QTableWidgetItem(query.value(0).toString()))
                self.clientsTable.setItem(row, 1, QTableWidgetItem(query.value(1).toString()))
                self.clientsTable.setItem(row, 2, QTableWidgetItem(query.value(2).toString()))
                self.clientsTable.setItem(row, 3, QTableWidgetItem(query.value(3).toString()))
                self.clientsTable.setItem(row, 4, QTableWidgetItem(query.value(4).toString()))
                row += 1
            db.close()



    def addClient(self):
        fio, ok = QInputDialog.getText(self, "Добавить ФИО", "Введите ФИО:")
        if not ok or not fio:
            return

        phone, ok = QInputDialog.getText(self, "Добавить номер", "Введите номер:")
        if not ok or not phone:
            return

        birth_date, ok = QInputDialog.getText(self, "Добавить день рождения", "Введите день рождения:")
        if not ok or not birth_date:
            return

        login, ok = QInputDialog.getText(self, "Добавить логин", "Введите логин:")
        if not ok or not login:
            return

        password, ok = QInputDialog.getText(self, "Добавить пароль", "Введите пароль:")
        if not ok or not password:
            return
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("mydatabase.db")
        if not db.open():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return
        query = QSqlQuery("INSERT INTO clients (fio,phone,birth_date,login, password) VALUES (?,?,?,?,?)", db)
        query.addBindValue(fio)
        query.addBindValue(phone)
        query.addBindValue(birth_date)
        query.addBindValue(login)
        query.addBindValue(password)
        if query.exec():
            row = self.clientsTable.rowCount()
            self.clientsTable.insertRow(row)
            self.clientsTable.setItem(row, 0, QTableWidgetItem(fio))
            self.clientsTable.setItem(row, 1, QTableWidgetItem(phone))
            self.clientsTable.setItem(row, 2, QTableWidgetItem(birth_date))
            self.clientsTable.setItem(row, 3, QTableWidgetItem(login))
            self.clientsTable.setItem(row, 4, QTableWidgetItem(password))
            QMessageBox.information(self, "Информация", "Клиент добавлен.")
        else:
            error_message = query.lastError().text()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить элемент расписания: {error_message}")

        db.close()

    def deleteClient(self):
        selected_row = self.clientsTable.currentRow()
        if selected_row != -1:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("mydatabase.db")
            if not db.open():
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
                return

            # Убедитесь, что типы данных параметров соответствуют типу данных в базе данных
            query = QSqlQuery("DELETE FROM clients WHERE fio =? AND phone =? AND birth_date =? AND login =? AND password =?", db)
            query.addBindValue(self.clientsTable.item(selected_row, 0).text())
            query.addBindValue(self.clientsTable.item(selected_row, 1).text())
            query.addBindValue(self.clientsTable.item(selected_row, 2).text())  # Проверьте, что birth_date имеет правильный формат
            query.addBindValue(self.clientsTable.item(selected_row, 3).text())
            query.addBindValue(self.clientsTable.item(selected_row, 4).text())

            if query.exec():
                self.clientsTable.removeRow(selected_row)
                QMessageBox.information(self, "Информация", "Клиент удален.")
            else:
                error_message = query.lastError().text()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить клиента: {error_message}")

            db.close()


class ScheduleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Расписание занятий")
        self.setGeometry(300, 300, 400, 250)

        layout = QVBoxLayout()

        self.scheduleTable = QTableWidget()
        self.scheduleTable.setRowCount(0)
        self.scheduleTable.setColumnCount(3)
        self.scheduleTable.setHorizontalHeaderItem(0, QTableWidgetItem("День"))
        self.scheduleTable.setHorizontalHeaderItem(1, QTableWidgetItem("Время"))
        self.scheduleTable.setHorizontalHeaderItem(2, QTableWidgetItem("Активность"))

        layout.addWidget(self.scheduleTable)

        buttonLayout = QHBoxLayout()
        addButton = QPushButton("Добавить")
        addButton.clicked.connect(self.addScheduleItem)
        buttonLayout.addWidget(addButton)

        deleteButton = QPushButton("Удалить")
        deleteButton.clicked.connect(self.deleteScheduleItem)
        buttonLayout.addWidget(deleteButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.loadSchedule()

    def loadSchedule(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("mydatabase.db")
        query = QSqlQuery("SELECT * FROM schedule", db)
        row = 0
        while query.next():
            self.scheduleTable.insertRow(row)
            self.scheduleTable.setItem(row, 0, QTableWidgetItem(query.value(0).toString()))
            self.scheduleTable.setItem(row, 1, QTableWidgetItem(query.value(1).toString()))
            self.scheduleTable.setItem(row, 2, QTableWidgetItem(query.value(2).toString()))
            row += 1
        db.close()
    def addScheduleItem(self):
        day, ok = QInputDialog.getText(self, "Добавить день", "Введите день:")
        if not ok or not day:
            return

        time, ok = QInputDialog.getText(self, "Добавить время", "Введите время:")
        if not ok or not time:
            return

        activity, ok = QInputDialog.getText(self, "Добавить активность", "Введите активность:")
        if not ok or not activity:
            return

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("mydatabase.db")
        if not db.open():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        query = QSqlQuery("INSERT INTO schedule (day, time, activity) VALUES (?,?,?)", db)
        query.addBindValue(day)
        query.addBindValue(time)
        query.addBindValue(activity)

        if query.exec():
            row = self.scheduleTable.rowCount()
            self.scheduleTable.insertRow(row)
            self.scheduleTable.setItem(row, 0, QTableWidgetItem(day))
            self.scheduleTable.setItem(row, 1, QTableWidgetItem(time))
            self.scheduleTable.setItem(row, 2, QTableWidgetItem(activity))
            QMessageBox.information(self, "Информация", "Элемент расписания добавлен.")
        else:
            error_message = query.lastError().text()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить элемент расписания: {error_message}")

        db.close()

    def deleteScheduleItem(self):
        selected_row = self.scheduleTable.currentRow()
        if selected_row != -1:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("mydatabase.db")
            if not db.open():
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
                return

            query = QSqlQuery("DELETE FROM schedule WHERE day =? AND time =? AND activity =?", db)
            query.addBindValue(self.scheduleTable.item(selected_row, 0).text())
            query.addBindValue(self.scheduleTable.item(selected_row, 1).text())
            query.addBindValue(self.scheduleTable.item(selected_row, 2).text())

            if query.exec():
                self.scheduleTable.removeRow(selected_row)
                QMessageBox.information(self, "Информация", "Элемент расписания удален.")
            else:
                error_message = query.lastError().text()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить элемент расписания: {error_message}")

            db.close()

class StorageWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Склад")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.storageTable = QTableWidget()
        self.storageTable.setRowCount(0)
        self.storageTable.setColumnCount(4)
        self.storageTable.setHorizontalHeaderItem(0, QTableWidgetItem("День"))
        self.storageTable.setHorizontalHeaderItem(1, QTableWidgetItem("Название"))
        self.storageTable.setHorizontalHeaderItem(2, QTableWidgetItem("Количество"))
        self.storageTable.setHorizontalHeaderItem(3, QTableWidgetItem("Цена"))

        addButton = QPushButton("Добавить товар")
        addButton.clicked.connect(self.addGood)

        deleteButton = QPushButton("Удалить товар")
        deleteButton.clicked.connect(self.deleteGood)

        layout.addWidget(self.storageTable)
        layout.addWidget(addButton)
        layout.addWidget(deleteButton)

        self.setLayout(layout)

        self.loadGoods()

    def loadGoods(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("mydatabase.db")
        db.open()

        query = QSqlQuery("SELECT * FROM goods", db)
        while query.next():
            row = self.storageTable.rowCount()
            self.storageTable.insertRow(row)
            self.storageTable.setItem(row, 0, QTableWidgetItem(query.value(1)))
            self.storageTable.setItem(row, 1, QTableWidgetItem(str(query.value(2))))
            self.storageTable.setItem(row, 2, QTableWidgetItem(str(query.value(3))))
            self.storageTable.setItem(row, 3, QTableWidgetItem(str(query.value(4))))

        db.close()

    def addGood(self):
        day, ok = QInputDialog.getText(self, "Добавить день", "Введите день:")
        if not ok or not day:
            return

        name, ok = QInputDialog.getText(self, "Добавить название", "Введите название:")
        if not ok or not name:
            return

        quantity, ok = QInputDialog.getText(self, "Добавить количество", "Введите количество:")
        if not ok or not quantity:
            return
        try:
            quantity = int(quantity)
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Количество должно быть числом.")
            return

        price, ok = QInputDialog.getText(self, "Добавить цену", "Введите цену:")
        if not ok or not price:
            return
        try:
            price = int(price)
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Цена должна быть числом.")
            return

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("mydatabase.db")
        if not db.open():
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return

        query = QSqlQuery("INSERT INTO goods (day, name, quantity, price) VALUES (?,?,?,?)", db)
        query.addBindValue(day)
        query.addBindValue(name)
        query.addBindValue(quantity)
        query.addBindValue(price)

        if query.exec():
            row = self.storageTable.rowCount()
            self.storageTable.insertRow(row)
            self.storageTable.setItem(row, 0, QTableWidgetItem(day))
            self.storageTable.setItem(row, 1, QTableWidgetItem(name))
            self.storageTable.setItem(row, 2, QTableWidgetItem(str(quantity)))
            self.storageTable.setItem(row, 3, QTableWidgetItem(str(price)))
            QMessageBox.information(self, "Информация", "Элемент расписания добавлен.")
        else:
            error_message = query.lastError().text()
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить элемент расписания: {error_message}")
            return

        db.close()

    def deleteGood(self):
        selected_row = self.storageTable.currentRow()
        if selected_row != -1:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("mydatabase.db")
            if not db.open():
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
                return

            id = self.storageTable.item(selected_row, 0).text()
            query = QSqlQuery("SELECT id FROM goods WHERE name =?", db)
            query.bindValue(0, id)
            if not query.exec():
                QMessageBox.critical(self, "Ошибка", "Не удалось найти товар по имени.")
                return

            if query.next():
                good_id = query.value(0)
                delete_query = QSqlQuery("DELETE FROM goods WHERE id =?", db)
                delete_query.bindValue(0, good_id)
                if not delete_query.exec():
                    QMessageBox.critical(self, "Ошибка", "Не удалось удалить товар.")
                else:
                    QMessageBox.information(self, "Информация", "Товар успешно удален.")
                    self.loadGoods()  # Refresh the table after deletion
            else:
                QMessageBox.critical(self, "Ошибка", "Товар с таким именем не найден.")
            db.close()
class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Документы")
        self.setGeometry(300, 300, 400, 250)

        layout = QVBoxLayout()

        dateLayout = QHBoxLayout()
        self.dateFromEdit = QDateEdit()
        self.dateFromEdit.setCalendarPopup(True)
        self.dateToEdit = QDateEdit()
        self.dateToEdit.setCalendarPopup(True)

        dateLayout.addWidget(QLabel("Дата с:"))
        dateLayout.addWidget(self.dateFromEdit)
        dateLayout.addWidget(QLabel("Дата по:"))
        dateLayout.addWidget(self.dateToEdit)

        layout.addLayout(dateLayout)

        servicesButton = QPushButton("Отчёт об услугах")
        servicesButton.clicked.connect(self.generateservicesReport)

        clientReportButton = QPushButton("Складской учёт")
        clientReportButton.clicked.connect(self.generateWarehouseReport)

        salesReportButton = QPushButton("Отчет о продажах")
        salesReportButton.clicked.connect(self.generateSalesReport)

        layout.addWidget(servicesButton)
        layout.addWidget(clientReportButton)
        layout.addWidget(salesReportButton)

        self.setLayout(layout)

    def generateservicesReport(self):
        try:
            with sqlite3.connect('mydatabase.db') as conn:
                cursor = conn.cursor()

                start_date = self.dateFromEdit.date().toPyDate()
                end_date = self.dateToEdit.date().toPyDate()

                query = """
                        SELECT day, item, quantity, price
                        FROM sales
                        WHERE category = 'Услуга' AND day BETWEEN? AND?
                        """
                cursor.execute(query, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                items = cursor.fetchall()

                doc = SimpleDocTemplate("sales_report_usluga.pdf", pagesize=A4)
                story = []

                total_sum = 0
                from reportlab.pdfbase import pdfmetrics
                from reportlab.pdfbase.ttfonts import TTFont


                pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))


                russian_style = ParagraphStyle(name='Russian', fontName='DejaVuSans', fontSize=12, leading=15)

                for item in items:
                    day, item_name, quantity, price = item
                    total_price = int(quantity) * int(price)
                    total_sum += total_price
                    para = Paragraph(
                        f"{day}: {item_name}, Количество: {quantity}, Цена: {price} руб., Общая сумма: {total_price} руб.",
                        russian_style)
                    story.append(para)
                    story.append(Spacer(1, 10))

                para = Paragraph(f"Общая стоимость за период: {total_sum} руб.", russian_style)
                story.append(para)

                doc.build(story)

                print("Отчет успешно сгенерирован.")
        except sqlite3.Error as e:
            print(f"Ошибка при генерации отчета: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def generateWarehouseReport(self):
        try:
            with sqlite3.connect('mydatabase.db') as conn:
                cursor = conn.cursor()
                start_date = self.dateFromEdit.date().toPyDate()
                end_date = self.dateToEdit.date().toPyDate()
                query = """
                            SELECT day, name, quantity, price
                            FROM goods
                            WHERE day BETWEEN ? AND ?
                            """
                cursor.execute(query, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                items = cursor.fetchall()
                doc = SimpleDocTemplate("goods_report.pdf", pagesize=A4)
                story = []
                total_sum = 0
                from reportlab.pdfbase import pdfmetrics
                from reportlab.pdfbase.ttfonts import TTFont
                pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
                russian_style = ParagraphStyle(name='Russian', fontName='Arial', fontSize=12, leading=15)
                for item in items:
                    day, item_name, quantity, price = item
                    total_price = int(quantity) * int(price)
                    total_sum += total_price
                    para = Paragraph(
                        f"{day}: {item_name}, Количество: {quantity}, Цена: {price} руб., Общая сумма: {total_price} руб.",
                        russian_style)
                    story.append(para)
                    story.append(Spacer(1, 10))
                para = Paragraph(f"Общая стоимость за период: {total_sum} руб.", russian_style)
                story.append(para)
                doc.build(story)
                print("Отчет успешно сгенерирован.")
        except sqlite3.Error as e:
            print(f"Ошибка при генерации отчета: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")
    def generateSalesReport(self):
        try:
            with sqlite3.connect('mydatabase.db') as conn:
                cursor = conn.cursor()

                start_date = self.dateFromEdit.date().toPyDate()
                end_date = self.dateToEdit.date().toPyDate()

                query = """
                        SELECT day, item, quantity, price
                        FROM sales
                        WHERE category = 'Товар' AND day BETWEEN ? AND ?
                        """
                cursor.execute(query, (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                items = cursor.fetchall()

                doc = SimpleDocTemplate("sales_report.pdf", pagesize=A4)
                story = []

                total_sum = 0
                from reportlab.pdfbase import pdfmetrics
                from reportlab.pdfbase.ttfonts import TTFont

                # Register the Arial font
                pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

                # Use the Arial font in your ParagraphStyle

                russian_style = ParagraphStyle(name='Russian', fontName='Arial', fontSize=12, leading=15)

                for item in items:
                    day, item_name, quantity, price = item
                    total_price = int(quantity) * int(price)
                    total_sum += total_price
                    para = Paragraph(
                        f"{day}: {item_name}, Количество: {quantity}, Цена: {price} руб., Общая сумма: {total_price} руб.",russian_style)
                    story.append(para)
                    story.append(Spacer(1, 10))

                para = Paragraph(f"Общая стоимость за период: {total_sum} руб.", russian_style)
                story.append(para)

                doc.build(story)

                print("Отчет успешно сгенерирован.")
        except sqlite3.Error as e:
            print(f"Ошибка при генерации отчета: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

class SalesWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Продажи")
        self.setGeometry(300, 300, 400, 250)

        layout = QVBoxLayout()

        self.salesTable = QTableWidget()
        self.salesTable.setRowCount(0)
        self.salesTable.setColumnCount(4)
        self.salesTable.setHorizontalHeaderItem(0, QTableWidgetItem("День"))
        self.salesTable.setHorizontalHeaderItem(1, QTableWidgetItem("Категория"))
        self.salesTable.setHorizontalHeaderItem(2, QTableWidgetItem("Товар"))
        self.salesTable.setHorizontalHeaderItem(3, QTableWidgetItem("Количество"))
        self.salesTable.setHorizontalHeaderItem(4, QTableWidgetItem("Цена"))

        layout.addWidget(self.salesTable)

        buttonLayout = QHBoxLayout()
        addButton = QPushButton("Добавить")
        addButton.clicked.connect(self.addSale)
        buttonLayout.addWidget(addButton)

        deleteButton = QPushButton("Удалить")
        deleteButton.clicked.connect(self.deleteSale)
        buttonLayout.addWidget(deleteButton)


        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.loadSales()

    def loadSales(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("mydatabase.db")
        query = QSqlQuery("SELECT * FROM sales", db)
        row = 0
        while query.next():
            self.salesTable.insertRow(row)
            self.salesTable.setItem(row, 0, QTableWidgetItem(query.value(0).toString()))
            self.salesTable.setItem(row, 1, QTableWidgetItem(query.value(1).toString()))
            self.salesTable.setItem(row, 2, QTableWidgetItem(query.value(2).toString()))
            self.salesTable.setItem(row, 3, QTableWidgetItem(query.value(3).toString()))
            self.salesTable.setItem(row, 4, QTableWidgetItem(query.value(4).toString()))
            row += 1
        db.close()

    def addSale(self):
        try:
            day, ok = QInputDialog.getText(self, "Добавить день", "Введите день:")
            if not ok or not day:
                return

            category, ok = QInputDialog.getItem(self, "Добавить категорию", "Выберите кате��орию:", ["Товар", "Услуга"])
            if not ok:
                return

            if category == "Товар":
                item, ok = QInputDialog.getText(self, "Добавить товар", "Введите название товара:")
                if not ok or not item:
                    return
            elif category == "Услуга":
                item, ok = QInputDialog.getText(self, "Добавить услугу", "Введите название услуги:")
                if not ok or not item:
                    return

            quantity, ok = QInputDialog.getText(self, "Добавить количество", "Введите количество:")
            if not ok or not quantity:
                return
            price, ok = QInputDialog.getText(self, "Добавить цену", "Введите цену:")
            if not ok or not price:
                return

            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("mydatabase.db")
            if not db.open():
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
                return

            query = QSqlQuery("INSERT INTO sales (day, category, item, quantity,price) VALUES (?,?,?,?,?)", db)
            query.addBindValue(day)
            query.addBindValue(category)
            query.addBindValue(item)
            query.addBindValue(quantity)
            query.addBindValue(price)

            if query.exec():
                row = self.salesTable.rowCount()
                self.salesTable.insertRow(row)
                self.salesTable.setItem(row, 0, QTableWidgetItem(day))
                self.salesTable.setItem(row, 1, QTableWidgetItem(category))
                self.salesTable.setItem(row, 2, QTableWidgetItem(item))
                self.salesTable.setItem(row, 3, QTableWidgetItem(quantity))
                self.salesTable.setItem(row, 4, QTableWidgetItem(price))
                QMessageBox.information(self, "Информация", "Элемент добавлен.")
            else:
                error_message = query.lastError().text()
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить элемент : {error_message}")

            db.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def deleteSale(self):
        selected_row = self.salesTable.currentRow()
        if selected_row != -1:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("mydatabase.db")
            if not db.open():
                QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
                return

            query = QSqlQuery("DELETE FROM sales WHERE day =? AND category=? AND item =? AND quantity =? AND price=?", db)
            query.addBindValue(self.salesTable.item(selected_row, 0).text())
            query.addBindValue(self.salesTable.item(selected_row, 1).text())
            query.addBindValue(self.salesTable.item(selected_row, 2).text())
            query.addBindValue(self.salesTable.item(selected_row, 3).text())
            query.addBindValue(self.salesTable.item(selected_row, 4).text())

            if query.exec():
                self.salesTable.removeRow(selected_row)
                QMessageBox.information(self, "Информация", "Элемент расписания удален.")
            else:
                error_message = query.lastError().text()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить элемент расписания: {error_message}")

            db.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    authWindow = AuthorizationWindow()
    authWindow.show()

    sys.exit(app.exec())
