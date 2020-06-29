from PyQt5.uic.properties import QtWidgets, QtGui

USER = ''
import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt, QPoint, QCoreApplication
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox
from requests import get, post, put
from werkzeug.security import generate_password_hash, check_password_hash

from data.__all_models import *
from data import db_session
from developer_client import DeveloperClient


def set_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


def check_password(self, password):
    return check_password_hash(self.hashed_password, password)


task_diff = {'A': 10, 'B': 15, 'C': 20, 'D': 25, 'E': 30, 'F': 35}


def set_settings(window):
    """Функция подгоняет клиент под текущие настройки"""
    window.setStyleSheet("background-color: rgb(90, 90, 90);" if window.settings[0] == 'Тёмная&2'
                         else "background-color: rgb(230, 230, 230);")
    window.update()


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
                    if not get(f'http://127.0.0.1:8080//api/users/{self.create_Email_lineEdit.text()}'):
                        user = dict()
                        user['nickname'] = self.create_Nickname_lineEdit.text()
                        user['login'] = self.create_Email_lineEdit.text()
                        user['hashed_password'] = set_password(self.create_Password_lineEdit.text())
                        user['birthday'] = str(self.dateEdit.text())
                        user['status'] = 'student'
                        post('http://127.0.0.1:8080/api/user', json=user)
                        USER = get(f'http://127.0.0.1:8080/api/users/{self.create_Email_lineEdit.text()}').json()
                        self.open_form = MainWindow()
                        self.open_form.show()
                        self.hide()
                    else:
                        self.error_label.setText('Данный логин уже занят')
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
            USER = get(f'http://127.0.0.1:8080/api/users/{self.login_lineEdit.text()}').json()
            if check_password_hash(USER['hashed_password'], self.password_lineEdit.text()):
                if self.remember:
                    txt = open('data/settings.txt', 'r').read().split('\n')
                    txt.remove("'")
                    txt.insert(1, USER['login'])

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
        # USER = get(f'http://127.0.0.1:8080/api/users/{txt[-2]}').json()
        # self.open_form = MainWindow() if USER['status'] != 'Разработчик' else DeveloperClient()
        if str(txt[-2]) != "'":
            USER = get(f'http://127.0.0.1:8080/api/users/{txt[-2]}').json()
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
        global current_task, task_id
        super().__init__()

        self.settings = open('data/settings.txt', 'r').read().split('\n')
        uic.loadUi('data/ui/client.ui', self)
        current_task = get(f'http://127.0.0.1:8080/api/task/{self.settings[-1]}').json()
        task_id = current_task['id']
        set_settings(self)
        self.post_task()

        self.decidedTasks.setColumnCount(3)
        self.decidedTasks.setHorizontalHeaderLabels(['ID', 'Название задачи', 'Получено баллов'])
        self.decidedTasks.horizontalHeader().setDefaultSectionSize(146)
        n_tasks = USER['decided_tasks'].split('%')[2:]
        i = 0
        for j in n_tasks:
            task = get(f'http://127.0.0.1:8080/api/task/{j}')
            if task:
                self.decidedTasks.setRowCount(i + 1)
                task = task.json()
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

        self.labelCalcNums.setText(self.nice_view(self.number_board))
        self.update_profile()

        self.ButtonAccept.clicked.connect(self.accept)

        self.Button_1_1.toggled.connect(self.onClicked)
        self.Button_1_2.toggled.connect(self.onClicked)
        # self.Button_2_1.toggled.connect(self.onClicked)

        self.new_settings = {}

        self.ButtonExit.clicked.connect(self.exit_from_account)

        self.add_task_pushButton.clicked.connect(self.add_task)

        for i in range(1, 2):
            eval(f'self.Button_{i}_{self.settings[i - 1].split("&")[1]}.setChecked(True)')
        # self.Button_2_1.setChecked(self.settings[2] == 'Отображать решённые задачи')

    # Калькулятор

    def num_operation(self, button=''):
        """Функция записывает введённые цифры в number_board"""
        button = self.sender().text() if not button else button
        self.number_board += button
        self.number_board = str(int(self.number_board)) \
            if '.' not in self.number_board else str(float(self.number_board))
        self.labelCalcNums.setText(self.nice_view(self.number_board))

    def update_decidedTasks(self, last_section, current_task):

        self.decidedTasks.setRowCount(last_section + 1)
        self.decidedTasks.setItem(last_section, 0, QTableWidgetItem(str(current_task['id'])))
        self.decidedTasks.setItem(last_section, 1, QTableWidgetItem(current_task['name']))
        self.decidedTasks.setItem(last_section, 2, QTableWidgetItem("+" + str(current_task['points'])))

    def update_profile(self):
        """Функция обновления профиля"""
        global USER

        USER = get(f'http://127.0.0.1:8080/api/users/{USER["login"]}').json()
        self.labelCalcNums.setText(self.nice_view(self.number_board))
        self.Nickname.setText(USER['nickname'])
        self.Nickname_small.setText(USER['nickname'])
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

    def arithmetic_operation(self, button=''):
        """Функция обрабатывает арифметические знаки и точку"""
        button = self.sender().text() if not button else button
        if button == '.':
            try:
                eval(self.number_board + '.')
                self.number_board += button
                self.labelCalcNums.setText(self.nice_view(self.number_board))
            except:
                pass
        else:
            self.expr_board += self.number_board
            if self.expr_board:
                if self.expr_board[-1] in ['+', '-', '*', '/']:
                    self.expr_board = self.expr_board[:-1] + button
                else:
                    self.expr_board += button
            else:
                self.expr_board += '0' + button

            self.number_board = ''
            self.labelExprCalc.setText(self.expr_board)
            self.labelCalcNums.setText(self.nice_view(self.number_board))

    def special_operation(self, button=''):
        """Функция обрабатывает """
        button = self.sender().text() if not button else button
        if button == '⌫':
            self.number_board = self.number_board[:-1] if len(self.number_board) != 0 else ''
            self.labelCalcNums.setText(self.nice_view(self.number_board))
        if button == '=':
            try:
                self.expr_board += self.number_board
                self.number_board = str(eval(self.expr_board))
                self.labelCalcNums.setText(self.number_board)
                self.labelExprCalc.setText(self.expr_board + '=')
                self.expr_board = ''
            except:
                self.labelCalcNums.setText('Error')
                self.number_board, self.expr_board = '', ''

    def nice_view(self, string):
        return '0' if string == '' else string

    def search(self):
        """Функция ищет задачу по id, который ввёл пользователь"""
        global current_task
        text = self.lineSearch.text()
        try:
            current_task = get(f'http://127.0.0.1:8080/api/task/{int(text)}').json()
            self.post_task()
        except:
            pass

    # Работа с сервером

    def get_next_task(self):
        global current_task, task_id
        max_id = get("http://127.0.0.1:8080/api/task/0").json()['count']
        decided_tasks = get(f'http://127.0.0.1:8080/api/users/{USER["login"]}').json()['decided_tasks'].split('%')
        if (len(set(decided_tasks)) - 2) != max_id:
            if task_id == max_id:
                task_id = 1
            else:
                task_id += 1
            if get(f'http://127.0.0.1:8080/api/task/{task_id}'):
                current_task = get(f'http://127.0.0.1:8080/api/task/{task_id}').json()
                self.post_task()
            else:
                self.get_next_task()

    def report(self):
        global USER, current_task
        if str(current_task['id']) not in get(f'http://127.0.0.1:8080/api/users/{USER["login"]}').json()['reports'].split('%'):
            put(f'http://127.0.0.1:8080/api/users/{USER["login"]}', data={'decided': 0, 'reported': current_task["id"], 'points': 0})
            put(f'http://127.0.0.1:8080/api/task/{current_task["id"]}')

    def get_prev_task(self):
        global current_task, task_id
        decided_tasks = get(f'http://127.0.0.1:8080/api/users/{USER["login"]}').json()['decided_tasks'].split()
        max_id = get('http://127.0.0.1:8080/api/task/0').json()['count']

        if (len(set(decided_tasks)) - 2) != max_id:
            if task_id == 1:
                task_id = max_id
            else:
                task_id -= 1
            if get(f'http://127.0.0.1:8080/api/task/{task_id}'):
                current_task = get(f'http://127.0.0.1:8080/api/task/{task_id}').json()
                self.post_task()
            else:
                self.get_prev_task()

    def run(self):
        self.label.setText('OK')

    def check_answer(self):
        global task_id, current_task

        decided_tasks = get(f'http://127.0.0.1:8080/api/users/{USER["login"]}').json()['decided_tasks'].split('%')[2:]
        if current_task["user_login"] != USER["login"]:
            if str(current_task["id"]) not in decided_tasks:
                if self.lineAnswer.text() == current_task['answer']:
                    self.labelAnswStatus.setText('✓')
                    self.labelAnswStatus.setToolTip('Статус: зачтено')
                    put(f"http://127.0.0.1:8080/api/users/{USER['login']}",
                        data={'decided': current_task['id'], 'reported': 0, 'points': current_task['points']})
                    self.update_profile()
                    self.update_decidedTasks(len(USER['decided_tasks'].split('%')) - 3, current_task)
                else:
                    self.labelAnswStatus.setText('✕')
                    self.labelAnswStatus.setToolTip('Статус: неправельное решение')
            else:
                self.warningLabel.setText("Вы уже решили эту задачу")
        else:
            self.warningLabel.setText("Вы не можете решить свою же задачу")

    def post_task(self):
        global current_task
        txt = open('data/settings.txt', 'r').read().split('\n')
        txt.remove(txt[-1])
        txt.insert(3, str(current_task["id"]))

        new_settings = open('data/settings.txt', 'w')
        new_settings.write('\n'.join(txt))
        new_settings.close()

        self.TextTask.setPlainText(current_task['content'])
        self.labelTitle.setText(current_task['name'])
        self.labelID.setText(f'ID: {current_task["id"]}')
        self.ScoreLabel.setText(f'{current_task["points"]} баллов')
        self.labelAuthor.setText('Автор: ' + get(f'http://127.0.0.1:8080/api/users/{current_task["user_login"]}').json()["nickname"])
        if str(current_task["id"]) in str(USER['decided_tasks']):
            self.lineAnswer.setText(current_task['answer'])
            self.labelAnswStatus.setText('✓')
            self.labelAnswStatus.setToolTip('Статус: зачтено')
        else:
            self.lineAnswer.setText('')
            self.labelAnswStatus.setText('')
            self.labelAnswStatus.setToolTip('Статус')

    # Настройки

    def accept(self):
        for elem in self.new_settings.keys():
            self.settings[int(elem) - 1] = list(self.new_settings.values())[0]

        self.write_settings = open("data/settings.txt", "w")
        self.write_settings.write('\n'.join(self.settings))
        self.write_settings.close()
        set_settings(self)

    def onClicked(self):
        Button = self.sender()
        if Button.isChecked():
            txt = Button.objectName().split('_')
            self.new_settings[txt[1]] = Button.text() + '&' + txt[2]

    def add_task(self):
        print(USER)
        dct = {'name': self.title_lineEdit.text(), 'user_login': USER['login'],
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
        post(f'http://127.0.0.1:8080/api/tasks/{current_task["user_login"]}', json=dct)

    # обработка кнопок клавиатуры

    def keyPressEvent(self, event):
        if event.text() in map(str, range(0, 10)):
            self.num_operation(event.text())

        if event.text() in ['+', '-', '*', '/']:
            self.arithmetic_operation(event.text())

        if event.key() == Qt.Key_Enter:
            self.special_operation('=')

        if event.key() == Qt.Key_Backspace:
            self.special_operation('⌫')

    def exit_from_account(self):
        valid = QMessageBox.question(self, 'Предупреждение',
                                     "Вы действительно хотите выйти из аккаунта?",
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            if self.settings[-2] == USER['login']:
                self.settings.remove(USER['login'])
                self.settings.remove(self.settings[-1])
                self.settings.insert(2, "'")
                self.settings.insert(3, str(current_task['id']))
                self.write_settings = open("data/settings.txt", "w")
                self.write_settings.write('\n'.join(self.settings))
                self.write_settings.close()

            self.preview = PreviewWindow()
            self.preview.show()
            self.hide()


app = QApplication(sys.argv)
# txt = open('data/settings.txt', 'r').read().split('\n')
# USER = get(f'http://127.0.0.1:8080/api/users/{txt[-2]}').json()
# ex = MainWindow() if USER['status'] != 'Разработчик' else DeveloperClient()
ex = PreviewWindow()
ex.show()
sys.exit(app.exec_())
