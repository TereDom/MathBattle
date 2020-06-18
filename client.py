import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt, QPoint, QCoreApplication
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from requests import get, post, put

task_id = 1
USER_ID = 1


def set_settings(window):
    window.setStyleSheet("background-color: rgb(90, 90, 90);" if window.settings[0] == 'Тёмная&2'
                         else "background-color: rgb(230, 230, 230);")
    window.update()


class MathBattle(QMainWindow):
    def __init__(self):
        global current_task
        super().__init__()

        uic.loadUi('data/ui/client.ui', self)
        current_task = get(f'http://127.0.0.1:5000/api/get_task/{task_id}').json()
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
        user = get(f'http://127.0.0.1:5000/api/user_information/{USER_ID}').json()
        self.Nickname.setText(user['name'])
        self.Status.setText(user['status'])
        self.Email.setText(user['login'])

        self.ButtonAccept.clicked.connect(self.accept)

        self.Button_1_1.toggled.connect(self.onClicked)
        self.Button_1_2.toggled.connect(self.onClicked)

        self.new_settings = {}

        for i in range(1, 2):
            eval(f'self.Button_{i}_{self.settings[i - 1].split("&")[1]}.setChecked(True)')

    # Калькулятор

    def num_operation(self, button=''):
        button = self.sender().text() if not button else button
        self.number_board += button
        self.number_board = str(int(self.number_board)) \
            if '.' not in self.number_board else str(float(self.number_board))
        self.labelCalcNums.setText(self.nice_view(self.number_board))

    def arithmetic_operation(self, button=''):

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

    def search(self):
        global current_task, task_id
        text = self.lineSearch.text()
        try:
            current_task = get(f'http://127.0.0.1:5000/api/get_task/{int(text)}').json()
            self.post_task()
            task_id = int(text)


        except:
            pass

    def special_operation(self, button=''):
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

    # Работа с сервером

    def get_next_task(self):
        global task_id, current_task
        max_id = get('http://127.0.0.1:5000/api/get_count_of_task').json()
        decided_tasks = get(f'http://127.0.0.1:5000/api/user_information/{USER_ID}').json()['decided_tasks'].split('%')
        if (len(set(decided_tasks)) - 2) != max_id:
            if task_id == max_id:
                task_id = 1
            else:
                task_id += 1
            if str(task_id) in str(decided_tasks):
                self.get_next_task()
            current_task = get(f'http://127.0.0.1:5000/api/get_task/{task_id}').json()
            self.post_task()

    def get_prev_task(self):
        global task_id, current_task
        decided_tasks = get(f'http://127.0.0.1:5000/api/user_information/{USER_ID}').json()['decided_tasks'].split('%')
        max_id = get('http://127.0.0.1:5000/api/get_count_of_task').json()
        if (len(set(decided_tasks)) - 2) != max_id:
            if task_id == 1:
                task_id = max_id
            else:
                task_id -= 1
            if str(task_id) in str(get(f'http://127.0.0.1:5000/api/user_information/{USER_ID}').json()['decided_tasks']):
                self.get_prev_task()
            current_task = get(f'http://127.0.0.1:5000/api/get_task/{task_id}').json()
            self.post_task()

    def run(self):
        self.label.setText('OK')

    def check_answer(self):
        global task_id, current_task
        decided_tasks = get(f'http://127.0.0.1:5000/api/user_information/{USER_ID}').json()['decided_tasks'].split('%')
        if not str(task_id) in decided_tasks:
            if self.lineAnswer.text() == current_task['answer']:
                self.labelAnswStatus.setText('✓')
                self.labelAnswStatus.setToolTip('Статус: зачтено')
                put(f'http://127.0.0.1:5000/api/change_count_of_decided_tasks/{USER_ID}/{task_id}')
            else:
                self.labelAnswStatus.setText('✕')
                self.labelAnswStatus.setToolTip('Статус: неправельное решение')

    def post_task(self):
        self.TextTask.setPlainText(current_task['content'])
        self.labelTitle.setText(current_task['name'])
        self.labelID.setText(f'ID: {current_task["id"]}')
        self.labelAnswStatus.setText('')
        self.lineAnswer.setText('')

    # Настройки

    def accept(self):
        new_settings_list = open("data/settings.txt", "w")
        new_settings_list.write('\n'.join(self.new_settings.values()))
        new_settings_list.close()
        self.settings = open("data/settings.txt", "r").read().split('\n')
        set_settings(self)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            txt = radioButton.objectName().split('_')
            self.new_settings[txt[1]] = radioButton.text() + '&' + txt[2]

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

# Можно попробовать сделать визуальное отображение нажатий кнопок на калькуляторе
# При кнопки на клавиатуре она как бы нажималась и в калькуляторе


def main():
    app = QApplication(sys.argv)
    ex = MathBattle()
    ex.show()
    sys.exit(app.exec_())


main()
