import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt, QPoint, QCoreApplication
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from requests import get, post, put

from data.__all_models import *
from data import db_session

task_id = 1
USER = ''
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
                self.main_form = MainWindow()
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
            self.open_form = MainWindow()
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

        self.ButtonNextTask.clicked.connect(self.get_next_task)
        self.ButtonPrevTask.clicked.connect(self.get_prev_task)
        self.ButtonSendAnswer.clicked.connect(self.check_answer)
        self.ButtonFindTask.clicked.connect(self.search)

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

        self.new_settings = {}

        self.ButtonExit.clicked.connect(self.exit_from_account)

        self.add_task_pushButton.clicked.connect(self.add_task)

        for i in range(1, 2):
            eval(f'self.Button_{i}_{self.settings[i - 1].split("&")[1]}.setChecked(True)')

    # Калькулятор

    def num_operation(self, button=''):
        """Функция записывает введённые цифры в number_board"""
        button = self.sender().text() if not button else button
        self.number_board += button
        self.number_board = str(int(self.number_board)) \
            if '.' not in self.number_board else str(float(self.number_board))
        self.labelCalcNums.setText(self.nice_view(self.number_board))

    def update_profile(self):
        """Функция обновления профиля"""
        global USER

        USER = get(f'http://127.0.0.1:8080/api/user_information/{USER["login"]}').json()
        self.labelCalcNums.setText(self.nice_view(self.number_board))
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

    def arithmetic_operation(self, button=''):
        """Функция обрабатывает арифметические знаки и точку"""
        button = self.sender().text() if not button else button
        if button == '.':
            try:
                test = eval(self.number_board + '.')
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
        global current_task, task_id
        text = self.lineSearch.text()
        try:
            current_task = get(f'http://127.0.0.1:8080/api/get_task/{int(text)}').json()
            self.post_task()
            task_id = int(text)
        except:
            pass

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
        if not str(task_id) in decided_tasks:
            if self.lineAnswer.text() == current_task['answer']:
                self.labelAnswStatus.setText('✓')
                self.labelAnswStatus.setToolTip('Статус: зачтено')
                put(f'http://127.0.0.1:8080/api/change_count_of_decided_tasks/{USER["login"]}/{task_id}')
                put(f'http://127.0.0.1:8080/api/change_points/{USER["login"]}/{current_task["points"]}')
                self.update_profile()

            else:
                self.labelAnswStatus.setText('✕')
                self.labelAnswStatus.setToolTip('Статус: неправельное решение')

    def post_task(self):
        self.TextTask.setPlainText(current_task['content'])
        self.labelTitle.setText(current_task['name'])
        self.labelID.setText(f'ID: {current_task["id"]}')
        self.ScoreLabel.setText(f'{current_task["points"]} баллов')
        self.labelAnswStatus.setText('')
        self.lineAnswer.setText('')

    # Настройки

    def accept(self):
        for elem in self.new_settings.keys():
            self.settings[int(elem) - 1] = list(self.new_settings.values())[0]

        self.write_settings = open("data/settings.txt", "w")
        self.write_settings.write('\n'.join(self.settings))
        self.write_settings.close()
        set_settings(self)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            txt = radioButton.objectName().split('_')
            self.new_settings[txt[1]] = radioButton.text() + '&' + txt[2]

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
        if self.settings[-1] == USER['login']:
            self.write_settings = open("data/settings.txt", "w")
            self.settings.remove(USER['login'])
            self.settings.append("'")
            self.write_settings.write('\n'.join(self.settings))
            self.write_settings.close()
        self.preview = PreviewWindow()
        self.preview.show()
        self.hide()


app = QApplication(sys.argv)
ex = PreviewWindow()
ex.show()
sys.exit(app.exec_())
