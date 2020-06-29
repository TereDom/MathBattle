from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox

from requests import get, post, put, delete


def set_settings(window):
    """Функция подгоняет клиент под текущие настройки"""
    window.setStyleSheet("background-color: rgb(90, 90, 90);" if window.settings[0] == 'Тёмная&2'
                         else "background-color: rgb(230, 230, 230);")
    window.update()


class DeveloperClient(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/ui/developer_client.ui', self)
        self.settings = open('data/settings.txt', 'r').read().split('\n')
        set_settings(self)
        self.tasks_list = get("http://127.0.0.1:8080/api/tasks/'").json()['tasks']

        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название задачи', 'Условие', 'Ответ', 'Логин пользователя', 'Кол-во репортов'])
        self.tableWidget.resizeRowsToContents()

        self.del_task_button.clicked.connect(self.del_task)
        self.open_user_tasks_button.clicked.connect(self.open_user_tasks)
        self.del_user_button.clicked.connect(self.del_user)
        self.update_tasks_button.clicked.connect(self.get_reported_tasks)
        self.ButtonExit.clicked.connect(self.exit_from_account)

        self.get_reported_tasks()

    def get_reported_tasks(self):
        self.tasks_list = get("http://127.0.0.1:8080/api/tasks/'").json()['tasks']
        self.update_tasks()
        self.labelStatus.setText("Все задачи")

    def del_task(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if rows:
            valid = QMessageBox.question(self, 'Предупреждение',
                                         "Вы действительно удалить выбранные задачи?\n" +
                                         f"ID задач: {list(map(lambda i: int(self.tableWidget.item(i, 0).text()), rows))}",
                                         QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                for i in rows:
                    delete(f"http://127.0.0.1:8080/api/task/{int(self.tableWidget.item(i, 0).text())}")
                if len(self.labelStatus.text()) > 10:
                    self.tasks_list = get(f"http://127.0.0.1:8080/api/tasks/{self.labelStatus.text().split()[-1]}").json()['tasks']
                    self.update_tasks()
                else:
                    self.get_reported_tasks()
        else:
            warWindow = QMessageBox.warning(self, 'Предупреждение',
                                            'Отметьте задачи для удаления!')

    def open_user_tasks(self):
        row = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if len(row) == 1:
            self.tasks_list = get(f"http://127.0.0.1:8080/api/tasks/{str(self.tableWidget.item(row[0], 4).text())}").json()['tasks']
            self.labelStatus.setText(f"Все задачи пользователя {str(self.tableWidget.item(row[0], 4).text())}")
            self.update_tasks()
        else:
            warWindow = QMessageBox.warning(self, 'Предупреждение',
                                            'Отметьте только одного пользователя!')

    def del_user(self):
        row = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if len(row) == 1:
            valid = QMessageBox.question(self, 'Предупреждение',
                                         f"Вы действительно хотите удалить пользователя {str(self.tableWidget.item(row[0], 4).text())}?",
                                         QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                delete(f"http://127.0.0.1:8080/api/tasks/{str(self.tableWidget.item(row[0], 4).text())}")
                delete(f"http://127.0.0.1:8080/api/users/{str(self.tableWidget.item(row[0], 4).text())}")
                self.get_reported_tasks()
        else:
            warWindow = QMessageBox.warning(self, 'Предупреждение',
                                            'Отметьте только одного пользователя!')

    def update_tasks(self):
        for j in range(len(self.tasks_list)):
            self.tableWidget.setRowCount(j + 1)
            task = self.tasks_list[j]
            self.tableWidget.setItem(j, 0, QTableWidgetItem(str(task['id'])))
            self.tableWidget.setItem(j, 1, QTableWidgetItem(str(task['name'])))
            self.tableWidget.setItem(j, 2, QTableWidgetItem(str(task['content'])))
            self.tableWidget.setItem(j, 3, QTableWidgetItem(str(task['answer'])))
            self.tableWidget.setItem(j, 4, QTableWidgetItem(str(task['user_login'])))
            self.tableWidget.setItem(j, 5, QTableWidgetItem(str(task['reports'])))

        self.tableWidget.resizeColumnsToContents()

    def exit_from_account(self):
        valid = QMessageBox.question(self, 'Предупреждение',
                                     "Вы действительно хотите выйти из аккаунта?",
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            if self.settings[-2] != "'":
                self.settings.remove(self.settings[-2])
                self.settings.insert(1, "'")

                self.write_settings = open("data/settings.txt", "w")
                self.write_settings.write('\n'.join(self.settings))
                self.write_settings.close()

            self.close()
