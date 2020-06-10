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


    def get_next_task(self):
        global task_id, current_task
        max_id = get('http://127.0.0.1:5000/api/get_count_of_task').json()
        if task_id == max_id:
            task_id = 1
        else:
            task_id += 1
        if str(task_id) in str(get(f'http://127.0.0.1:5000/api/user_information/{USER_ID}').json()['decided_tasks']).split('%'):
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