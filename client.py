import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt, QPoint, QCoreApplication
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QTableWidgetItem
from requests import get, post, put

from MultitaskingFunctions import set_settings, search, num_operation, arithmetic_operation, special_operation, \
    nice_view, accept, onClicked, exit_from_account, keyPressEvent

from data.__all_models import *
from data import db_session

task_id = 1
USER = ''
task_diff = {'A': 10, 'B': 15, 'C': 20, 'D': 25, 'E': 30, 'F': 35}


from developer_client import DeveloperClient


class RegisterWindow(QWidget):
    """Форма регистрации нового пользователя"""
    def __init__(self):
        super().__init__()
        uic.loadUi('data/ui/Register.ui', self)

        self.RegButton.clicked.connect(self.reg)
        self.return_home_Button.clicked.connect(self.go_back)

    def reg(self):
        global USER
        if self.create_Password_lineEdit.text() == self.prove_Password_lineEdit.text():
            if self.create_Nickname_lineEdit.text() and self.create_Email_lineEdit.text() and \
                    self.create_Password_lineEdit.text():
                if self.create_Email_lineEdit.text() != "'":
                    user = dict()
                    user['nickname'] = self.create_Nickname_lineEdit.text()
                    user['login'] = self.create_Email_lineEdit.text()
                    user['password'] = self.create_Password_lineEdit.text()
                    user['birthday'] = str(self.dateEdit.text())
                    user['status'] = 'student'
                    post('http://127.0.0.1:8080/api/create_user', json=user)
                    USER = get(f'http://127.0.0.1:8080/api/user_information/{self.create_Email_lineEdit.text()}').json()
                    self.open_form = MainWindow()
                    self.open_form.show()
                    self.hide()
                else:
                    self.error_label.setText('Данные некорректны')

            else:
                self.error_label.setText('Обязательное поле не заполнено')
        else:
            self.error_label.setText('Пароли не совпадают')
        pass

    def go_back(self):
        """Возвращает на PreviewWindow"""
        self.preview_win = PreviewWindow()
        self.preview_win.show()
        self.hide()


class LoginWindow(QWidget):
    def __init__(self):
        """Форма авторизации уже существующего пользователя"""
        super().__init__()

        uic.loadUi('data/ui/Login.ui', self)

        self.remembrMe_checkBox.stateChanged.connect(self.rememberMe)
        self.LoginButton.clicked.connect(self.login)
        self.return_home_Button.clicked.connect(self.go_back)
        self.remember = False

    def login(self):
        """Алогоритм входа в программу"""
        global USER
        try:
            USER = get(f'http://127.0.0.1:8080/api/user_information/{self.login_lineEdit.text()}').json()
            if USER['hashed_password'] == self.password_lineEdit.text():
                if self.remember:
                    txt = open('data/settings.txt', 'r').read().split('\n')
                    txt.remove("'")
                    txt.append(USER['login'])

                    self.settings = open('data/settings.txt', 'w')

                    self.settings.write('\n'.join(txt))
                    self.settings.close()

                self.main_form = MainWindow() if USER['status'] != 'Разработчик' else DeveloperClient()
                self.main_form.show()
                self.close()
            else:
                raise ValueError()
        except:
            self.error_label.setText('Ошибка: данные некорректны')

    def rememberMe(self, state):
        if state == Qt.Checked:
            self.remember = True

    def go_back(self):
        """Возвращает на PreviewWindow"""
        self.preview_win = PreviewWindow()
        self.preview_win.show()
        self.hide()


class PreviewWindow(QWidget):
    """Форма приветственного окна"""
    def __init__(self):
        global USER
        super().__init__()
        uic.loadUi('data/ui/PreviewRegisterWindow.ui', self)
        self.RegButton.clicked.connect(self.open_reg_form)
        self.LoginButton.clicked.connect(self.open_login_form)

        txt = open('data/settings.txt', 'r').read().split('\n')
        if str(txt[-1]) != "'":
            USER = get(f'http://127.0.0.1:8080/api/user_information/{txt[-1]}').json()
            self.open_form = MainWindow() if USER['status'] != 'Разработчик' else DeveloperClient()
        else:
            self.open_form = LoginWindow()

    def open_reg_form(self):
        self.reg_form = RegisterWindow()
        self.reg_form.show()
        self.hide()

    def open_login_form(self):
        self.open_form.show()
        self.hide()


class MainWindow(QMainWindow):
    """Форма главного окна"""
    def __init__(self):
        global current_task
        super().__init__()

        uic.loadUi('data/ui/client.ui', self)
        current_task = get(f'http://127.0.0.1:8080/api/get_task/{task_id}').json()
        self.settings = open('data/settings.txt', 'r').read().split('\n')
        set_settings(self)
        self.post_task()

        self.decidedTasks.setColumnCount(3)
        self.decidedTasks.setHorizontalHeaderLabels(['ID', 'Название задачи', 'Получено баллов'])
        self.decidedTasks.horizontalHeader().setDefaultSectionSize(143)
        n_tasks = USER['decided_tasks'].split('%')[1:]
        self.decidedTasks.setRowCount(len(n_tasks))
        i = 0
        for j in n_tasks:
            if j != '':
                task = get(f'http://127.0.0.1:8080/api/get_task/{j}').json()
                self.update_decidedTasks(i, task)
                i += 1

        self.ButtonNextTask.clicked.connect(self.get_next_task)
        self.ButtonPrevTask.clicked.connect(self.get_prev_task)
        self.ButtonSendAnswer.clicked.connect(self.check_answer)
        self.ButtonFindTask.clicked.connect(self.search)
        self.reportButton.clicked.connect(self.report)

        self.OneCalcButton.clicked.connect(self.num_operation)
        self.TwoCalcButton.clicked.connect(self.num_operation)
        self.ThreeCalcButton.clicked.connect(self.num_operation)
        self.FourCalcButton.clicked.connect(self.num_operation)
        self.FiveCalcButton.clicked.connect(self.num_operation)
        self.SixCalcButton.clicked.connect(self.num_operation)
        self.SevenCalcButton.clicked.connect(self.num_operation)
        self.EightCalcButton.clicked.connect(self.num_operation)
        self.NineCalcButton.clicked.connect(self.num_operation)
        self.ZeroCalcButton.clicked.connect(self.num_operation)

        self.PlusCalcButton.clicked.connect(self.arithmetic_operation)
        self.MinusCalcButton.clicked.connect(self.arithmetic_operation)
        self.MultiplyCalcButton.clicked.connect(self.arithmetic_operation)
        self.DivideCalcButton.clicked.connect(self.arithmetic_operation)
        self.DotCalcButton.clicked.connect(self.arithmetic_operation)

        self.DelCalcButton.clicked.connect(self.special_operation)
        self.EqualCalcButton.clicked.connect(self.special_operation)

        self.expr_board = ''
        self.number_board = ''

        self.labelCalcNums.setText(nice_view(self.number_board))
        self.update_profile()

        self.ButtonAccept.clicked.connect(self.accept)

        self.Button_1_1.toggled.connect(self.onClicked)
        self.Button_1_2.toggled.connect(self.onClicked)

        self.new_settings = {}

        self.ButtonExit.clicked.connect(self.exit_from_account)

        self.add_task_pushButton.clicked.connect(self.add_task)

        for i in range(1, 2):
            eval(f'self.Button_{i}_{self.settings[i - 1].split("&")[1]}.setChecked(True)')

    def update_decidedTasks(self, last_section, current_task):
        self.decidedTasks.setRowCount(last_section + 1)
        self.decidedTasks.setItem(last_section, 0, QTableWidgetItem(str(current_task['id'])))
        self.decidedTasks.setItem(last_section, 1, QTableWidgetItem(current_task['name']))
        self.decidedTasks.setItem(last_section, 2, QTableWidgetItem("+" + str(current_task['points'])))

    def update_profile(self):
        """Функция обновления профиля"""
        global USER

        USER = get(f'http://127.0.0.1:8080/api/user_information/{USER["login"]}').json()
        self.labelCalcNums.setText(nice_view(self.number_board))
        self.Nickname.setText(USER['name'])
        self.Nickname_small.setText(USER['name'])
        self.Status.setText(USER['status'])
        self.Points.setText(str(USER['points']))
        self.Email.setText(USER["login"])
        self.labelBD.setText(USER['birthday'])

        if USER['points'] < 150:
            self.AddTaskPage.setEnabled(False)
            self.permission_label.setText('Для доступа к добавлению задач необходимо набрать 150 баллов')
        else:
            self.AddTaskPage.setEnabled(True)
            self.permission_label.clear()

    # Работа с сервером

    def get_next_task(self):
        global task_id, current_task
        max_id = get('http://127.0.0.1:8080/api/get_count_of_task').json()
        decided_tasks = get(f'http://127.0.0.1:8080/api/user_information/{USER["login"]}').json()['decided_tasks'].split('%')
        if (len(set(decided_tasks)) - 2) != max_id:
            if task_id == max_id:
                task_id = 1
            else:
                task_id += 1
            if str(task_id) in str(decided_tasks):
                self.get_next_task()
            current_task = get(f'http://127.0.0.1:8080/api/get_task/{task_id}').json()
            self.post_task()

    def report(self):
        global USER, current_task
        if str(current_task['id']) not in get(f'http://127.0.0.1:8080/api/user_information/{USER["login"]}').json()['reports'].split('%'):
            put(f'http://127.0.0.1:8080/api/change_reported_tasks/{USER["login"]}/{current_task["id"]}')

    def get_prev_task(self):
        global task_id, current_task
        decided_tasks = get(f'http://127.0.0.1:8080/api/user_information/{USER["login"]}').json()['decided_tasks'].split('%')
        max_id = get('http://127.0.0.1:8080/api/get_count_of_task').json()
        if (len(set(decided_tasks)) - 2) != max_id:
            if task_id == 1:
                task_id = max_id
            else:
                task_id -= 1
            if str(task_id) in str(get(f'http://127.0.0.1:8080/api/user_information/{USER["login"]}').json()['decided_tasks']):
                self.get_prev_task()
            current_task = get(f'http://127.0.0.1:8080/api/get_task/{task_id}').json()
            self.post_task()

    def run(self):
        self.label.setText('OK')

    def check_answer(self):
        global task_id, current_task

        decided_tasks = get(f'http://127.0.0.1:8080/api/user_information/{USER["login"]}').json()['decided_tasks'].split('%')
        if current_task["user_id"] != USER["id"]:
            if str(current_task["id"]) not in decided_tasks:
                if self.lineAnswer.text() == current_task['answer']:
                    self.labelAnswStatus.setText('✓')
                    self.labelAnswStatus.setToolTip('Статус: зачтено')
                    put(f'http://127.0.0.1:8080/api/change_count_of_decided_tasks/{USER["login"]}/{task_id}')
                    put(f'http://127.0.0.1:8080/api/change_points/{USER["login"]}/{current_task["points"]}')
                    self.update_profile()
                    self.update_decidedTasks(len(USER['decided_tasks'].split('%')) - 2, current_task)
                else:
                    self.labelAnswStatus.setText('✕')
                    self.labelAnswStatus.setToolTip('Статус: неправельное решение')
            else:
                self.warningLabel.setText("Вы уже решили эту задачу")
        else:
            self.warningLabel.setText("Вы не можете решить свою же задачу")

    def post_task(self):
        self.TextTask.setPlainText(current_task['content'])
        self.labelTitle.setText(current_task['name'])
        self.labelID.setText(f'ID: {current_task["id"]}')
        self.ScoreLabel.setText(f'{current_task["points"]} баллов')
        self.labelAuthor.setText('Автор: ' + get(f'http://127.0.0.1:8080/api/author_information/{current_task["user_id"]}').json()["name"])
        self.labelAnswStatus.setText('')
        self.warningLabel.setText('')
        self.lineAnswer.setText('')

    def add_task(self):
        dct = {'name': self.title_lineEdit.text(), 'user_id': USER['id'],
               'points': task_diff[self.difficult_lvl_comboBox.currentText()],
               'content': self.task_text_TextEdit.toPlainText(), 'answer': self.answer_lineEdit.text()}
        try:
            if not (self.title_lineEdit.text() and
                    self.task_text_TextEdit.toPlainText() and self.answer_lineEdit.text()):
                raise NameError()
            float(dct['answer'])
        except ValueError:
            self.error_label.setStyleSheet('color: rgb(200, 0, 0);')
            self.error_label.setText('Некорректный ответ (ответ должен быть представлен числом)')
            return
        except NameError:
            self.error_label.setStyleSheet('color: rgb(200, 0, 0);')
            self.error_label.setText('Все поля должны быть заполнены')
            return

        self.error_label.setStyleSheet('color: rgb(0, 200, 0);')
        self.error_label.setText('Задача успешно добавлена!')
        post('http://127.0.0.1:8080/api/post_task', json=dct)

    def onClicked(self):
        return onClicked(self)

    def accept(self):
        return accept(self)

    def search(self):
        return search(self)

    def num_operation(self):
        return num_operation(self)

    def arithmetic_operation(self):
        return arithmetic_operation(self)

    def special_operation(self):
        return special_operation(self)

    def exit_from_account(self):
        self.preview = PreviewWindow()
        self.preview.show()
        self.hide()
        return exit_from_account(self, USER)

    def keyPressEvent(self, event):
        return keyPressEvent(self, event)


app = QApplication(sys.argv)
ex = PreviewWindow()
ex.show()
sys.exit(app.exec_())
