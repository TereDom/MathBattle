import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from requests import get, post, put

task_id = 1
USER_ID = 1


class MathBattle(QMainWindow):
    def __init__(self):
        global current_task
        super().__init__()

        uic.loadUi('data/ui/client.ui', self)
        current_task = get(f'http://127.0.0.1:5000/api/get_task/{task_id}').json()
        self.post_task()

        self.ButtonNextTask.clicked.connect(self.get_next_task)
        self.ButtonPrevTask.clicked.connect(self.get_prev_task)
        self.ButtonSendAnswer.clicked.connect(self.check_answer)

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

        self.calc_board = ''
        self.labelCalc.setText(self.nice_view(self.calc_board))
        self.number = '0'

    # Калькулятор
    def num_operation(self):
        self.number += self.sender().text()
        self.calc_board += self.sender().text()
        self.labelCalc.setText(self.nice_view(self.calc_board))

    def arithmetic_operation(self):
        self.calc_board = '0' if len(self.calc_board) == 0 else self.calc_board
        if self.sender().text() == '.' and '.' not in self.number:
            self.number += self.sender().text()
            self.calc_board += self.sender().text()
        elif self.sender().text() in ['+', '-', '*', '/']:
            if self.calc_board[-1] in ['+', '-', '*', '/']:
                self.calc_board = self.calc_board[:-1] + self.sender().text()
            else:
                self.calc_board += self.sender().text()
                self.number = '0'
        self.labelCalc.setText(self.nice_view(self.calc_board))

    def special_operation(self):
        if self.sender().text() == '⌫':
            self.calc_board = self.calc_board[:-1]
            self.labelCalc.setText(self.nice_view(self.calc_board))
        if self.sender().text() == '=':
            try:
                self.calc_board = str(eval(self.calc_board))
                self.labelCalc.setText(self.calc_board)
            except:
                self.labelCalc.setText('Error')
                self.calc_board = ''

    def nice_view(self, string):
        return '0' if string == '' else string

    def get_next_task(self):
        global task_id, current_task
        max_id = get('http://127.0.0.1:5000/api/get_count_of_task').json()
        if task_id == max_id:
            task_id = 1
        else:
            task_id += 1
        if str(task_id) in str(
                get(f'http://127.0.0.1:5000/api/user_information/{USER_ID}').json()['decided_tasks']).split('%'):
            self.get_next_task()
        current_task = get(f'http://127.0.0.1:5000/api/get_task/{task_id}').json()
        self.post_task()

    def get_prev_task(self):
        global task_id, current_task
        max_id = get('http://127.0.0.1:5000/api/get_count_of_task').json()
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
        if self.lineAnswer.text() == current_task['answer']:
            self.labelAnswStatus.setText('✓')
            put(f'http://127.0.0.1:5000/api/change_count_of_decided_tasks/{USER_ID}/{task_id}')
        else:
            self.labelAnswStatus.setText('✕')

    def post_task(self):
        self.TextTask.setPlainText(current_task['content'])
        self.labelTitle.setText(current_task['name'])
        self.labelID.setText(f'ID: {current_task["id"]}')
        self.labelAnswStatus.setText('')
        self.lineAnswer.setText('')


app = QApplication(sys.argv)
ex = MathBattle()
ex.show()
sys.exit(app.exec_())
