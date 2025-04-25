from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QInputDialog, QTableView, QMessageBox
from db import get_connection
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/admin_window.ui", self)
        self.load_all_docs()
        self.load_user_docs()
        self.load_users()

        # Подключение кнопок
        self.addDocButton.clicked.connect(self.add_doc)
        self.editDocButton.clicked.connect(self.edit_doc)
        self.deleteDocButton.clicked.connect(self.delete_doc)

        self.addUserButton.clicked.connect(self.add_user)
        self.editUserButton.clicked.connect(self.edit_user)
        self.deleteUserButton.clicked.connect(self.delete_user)

        self.addUserDocButton.clicked.connect(self.add_user_doc)

    def load_all_docs(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM all_docs")
            data = cursor.fetchall()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "Название", "Цена"])

        for doc in data:
            items = [
                QStandardItem(str(doc['id'])),
                QStandardItem(doc['name']),
                QStandardItem(str(doc['price']))
            ]
            model.appendRow(items)

        self.allDocsTable.setModel(model)

    def load_user_docs(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT ud.id, u.name as user_name, ad.name as doc_name, ud.date_start, ud.date_end 
                FROM user_docs ud
                JOIN users u ON u.id = ud.id_user
                JOIN all_docs ad ON ad.id = ud.id_docs
            """)
            data = cursor.fetchall()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "Пользователь", "Договор", "Начало", "Конец"])

        for doc in data:
            items = [
                QStandardItem(str(doc['id'])),
                QStandardItem(doc['user_name']),
                QStandardItem(doc['doc_name']),
                QStandardItem(str(doc['date_start'])),
                QStandardItem(str(doc['date_end']))
            ]
            model.appendRow(items)

        self.userDocsTable.setModel(model)

    def load_users(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            data = cursor.fetchall()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "Логин", "Имя", "Фамилия", "Роль"])

        for user in data:
            items = [
                QStandardItem(str(user['id'])),
                QStandardItem(user['login']),
                QStandardItem(user['name']),
                QStandardItem(user['surname']),
                QStandardItem(user['role'])
            ]
            model.appendRow(items)

        self.usersTable.setModel(model)

    def add_doc(self):
        name, ok = QInputDialog.getText(self, "Добавление договора", "Название договора:")
        if not ok: return
        price, ok = QInputDialog.getDouble(self, "Добавление договора", "Цена договора:")
        if not ok: return

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO all_docs (name, price) VALUES (%s, %s)", (name, price))
        conn.commit()
        self.load_all_docs()

    def edit_doc(self):
        row = self.allDocsTable.currentIndex().row()
        if row == -1: return
        doc_id = int(self.allDocsTable.model().item(row, 0).text())
        new_name, ok = QInputDialog.getText(self, "Изменение договора", "Новое название:")
        if not ok: return
        new_price, ok = QInputDialog.getDouble(self, "Изменение договора", "Новая цена:")
        if not ok: return

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE all_docs SET name=%s, price=%s WHERE id=%s", (new_name, new_price, doc_id))
        conn.commit()
        self.load_all_docs()

    def delete_doc(self):
        row = self.userDocsTable.currentIndex().row()
        if row == -1: return
        doc_id = int(self.userDocsTable.model().item(row, 0).text())

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM user_docs WHERE id=%s", (doc_id,))
        conn.commit()
        self.load_user_docs()

    def add_user(self):
        login, ok = QInputDialog.getText(self, "Добавление пользователя", "Логин:")
        if not ok: return
        password, ok = QInputDialog.getText(self, "Добавление пользователя", "Пароль:")
        if not ok: return
        name, ok = QInputDialog.getText(self, "Добавление пользователя", "Имя:")
        if not ok: return
        surname, ok = QInputDialog.getText(self, "Добавление пользователя", "Фамилия:")
        if not ok: return
        role, ok = QInputDialog.getText(self, "Добавление пользователя", "Роль (client/admin):")
        if not ok: return

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (login, password, name, surname, role) VALUES (%s, %s, %s, %s, %s)",
                           (login, password, name, surname, role))
        conn.commit()
        self.load_users()

    def edit_user(self):
        row = self.usersTable.currentIndex().row()
        if row == -1: return
        user_id = int(self.usersTable.model().item(row, 0).text())
        new_login, ok = QInputDialog.getText(self, "Редактирование пользователя", "Новый логин:")
        if not ok: return
        new_name, ok = QInputDialog.getText(self, "Редактирование пользователя", "Новое имя:")
        if not ok: return
        new_surname, ok = QInputDialog.getText(self, "Редактирование пользователя", "Новая фамилия:")
        if not ok: return
        new_role, ok = QInputDialog.getText(self, "Редактирование пользователя", "Новая роль:")
        if not ok: return

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE users SET login=%s, name=%s, surname=%s, role=%s WHERE id=%s",
                           (new_login, new_name, new_surname, new_role, user_id))
        conn.commit()
        self.load_users()

    def delete_user(self):
        row = self.usersTable.currentIndex().row()
        if row == -1: return
        user_id = int(self.usersTable.model().item(row, 0).text())

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        self.load_users()

    def add_user_doc(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            # Получаем всех пользователей
            cursor.execute("SELECT id, name FROM users")
            users = cursor.fetchall()
            if not users:
                QMessageBox.warning(self, "Ошибка", "Нет пользователей в базе.")
                return

            user_names = [str(u['name']) for u in users]
            user_name, ok = QInputDialog.getItem(self, "Пользователь", "Выберите пользователя:", user_names,
                                                 editable=False)
            if not ok:
                return
            id_user = users[user_names.index(user_name)]['id']

            # Получаем все договоры
            cursor.execute("SELECT id, name FROM all_docs")
            docs = cursor.fetchall()
            if not docs:
                QMessageBox.warning(self, "Ошибка", "Нет договоров в базе.")
                return

            doc_names = [str(d['name']) for d in docs]
            doc_name, ok = QInputDialog.getItem(self, "Договор", "Выберите договор:", doc_names, editable=False)
            if not ok:
                return
            id_doc = docs[doc_names.index(doc_name)]['id']

            # Даты начала и окончания
            date_start, ok = QInputDialog.getText(self, "Дата начала", "Введите дату начала (ГГГГ-ММ-ДД):")
            if not ok: return
            date_end, ok = QInputDialog.getText(self, "Дата окончания", "Введите дату окончания (ГГГГ-ММ-ДД):")
            if not ok: return

            # Получаем статусы
            cursor.execute("SELECT id, name FROM status")
            statuses = cursor.fetchall()
            if not statuses:
                QMessageBox.warning(self, "Ошибка", "Нет статусов в базе.")
                return

            # Важно: приводим к строке для сравнения с ENUM
            status_names = [str(s['name']) for s in statuses]
            status_name, ok = QInputDialog.getItem(self, "Статус", "Выберите статус:", status_names, editable=False)
            if not ok:
                return
            id_status = statuses[status_names.index(status_name)]['id']

            # Добавляем запись
            cursor.execute("""
                INSERT INTO user_docs (id_user, id_docs, date_start, date_end, id_status)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_user, id_doc, date_start, date_end, id_status))
            conn.commit()
        self.load_user_docs()
