from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from db import get_connection
from user_window import UserWindow
from admin_window import AdminWindow
from PyQt5.QtCore import Qt
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.open_register)

    def login(self):
        login = self.loginInput.text()
        password = self.passwordInput.text()

        if login == "admin" and password == "admin123":
            self.open_admin()
            return

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s", (login, password))
            user = cursor.fetchone()

        if user:
            print(f"User found: {user['id']}")  # Выводим ID пользователя
            self.open_user(user["id"])
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_user(self, user_id):
        self.user_window = UserWindow(user_id)
        self.user_window.show()
        self.close()

    def open_admin(self):
        self.admin_window = AdminWindow()
        self.admin_window.show()
        self.close()

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)
        self.registerButton.clicked.connect(self.register)

    def register(self):
        login = self.loginInput.text()
        password = self.passwordInput.text()
        name = self.nameInput.text()
        surname = self.surnameInput.text()

        if not all([login, password, name, surname]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        conn = get_connection()
        with conn.cursor() as cursor:
            # Проверка на уникальность логина
            cursor.execute("SELECT * FROM users WHERE login=%s", (login,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Ошибка", "Логин уже занят.")
                return

            cursor.execute(
                "INSERT INTO users (login, password, name, surname) VALUES (%s, %s, %s, %s)",
                (login, password, name, surname)
            )
            conn.commit()

        QMessageBox.information(self, "Успех", "Регистрация прошла успешно.")
        self.close()