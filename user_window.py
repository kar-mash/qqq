from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from db import get_connection
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from PyQt5.QtCore import Qt
class UserWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("ui/user_window.ui", self)
        self.user_id = user_id
        print(f"UserWindow initialized with user_id: {self.user_id}")  # Проверим передаваемый user_id
        self.load_docs()
        self.refreshButton.clicked.connect(self.load_docs)

    def load_docs(self):
        try:
            print(f"Loading documents for user_id: {self.user_id}")
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT ad.name, ad.price, ud.date_start, ud.date_end, s.name as status
                    FROM user_docs ud
                    JOIN all_docs ad ON ad.id = ud.id_docs
                    JOIN status s ON s.id = ud.id_status
                    WHERE ud.id_user = %s
                """, (self.user_id,))
                data = cursor.fetchall()

            if not data:
                print("No documents found for user.")
                return  # Прекращаем выполнение, если нет документов

            # Создаем модель данных для QTableView
            model = QStandardItemModel(len(data), 5)  # 5 столбцов
            model.setHorizontalHeaderLabels(["Договор", "Цена", "Начало", "Конец", "Статус"])

            for row, doc in enumerate(data):
                for col, val in enumerate(doc.values()):
                    item = QStandardItem(str(val) if val is not None else "")
                    model.setItem(row, col, item)

            # Устанавливаем модель в QTableView
            self.userContractsTable.setModel(model)

        except Exception as e:
            print(f"Error loading documents: {str(e)}")