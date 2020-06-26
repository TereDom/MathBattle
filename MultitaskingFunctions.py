from PyQt5.QtCore import Qt
from requests import get, post, put

# from client import USER, PreviewWindow


def set_settings(window):
    """Функция подгоняет клиент под текущие настройки"""
    window.setStyleSheet("background-color: rgb(90, 90, 90);" if window.settings[0] == 'Тёмная&2'
                         else "background-color: rgb(230, 230, 230);")
    window.update()


def num_operation(self, button=''):
    """Функция записывает введённые цифры в number_board"""
    button = self.sender().text() if not button else button
    self.number_board += button
    self.number_board = str(int(self.number_board)) \
        if '.' not in self.number_board else str(float(self.number_board))
    self.labelCalcNums.setText(nice_view(self.number_board))


def arithmetic_operation(self, button=''):
    """Функция обрабатывает арифметические знаки и точку"""
    button = self.sender().text() if not button else button
    if button == '.':
        try:
            eval(self.number_board + '.')
            self.number_board += button
            self.labelCalcNums.setText(nice_view(self.number_board))
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
        self.labelCalcNums.setText(nice_view(self.number_board))


def special_operation(self, button=''):
    """Функция обрабатывает """
    button = self.sender().text() if not button else button
    if button == '⌫':
        self.number_board = self.number_board[:-1] if len(self.number_board) != 0 else ''
        self.labelCalcNums.setText(nice_view(self.number_board))
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


def nice_view(string):
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


def keyPressEvent(self, event):
    if event.text() in map(str, range(0, 10)):
        num_operation(self, event.text())

    if event.text() in ['+', '-', '*', '/']:
        arithmetic_operation(self, event.text())

    if event.key() == Qt.Key_Enter:
        special_operation(self, '=')

    if event.key() == Qt.Key_Backspace:
        special_operation(self, '⌫')


def exit_from_account(self, USER):
    if self.settings[-1] == USER['login']:
        self.write_settings = open("data/settings.txt", "w")
        self.settings.remove(USER['login'])
        self.settings.append("'")
        self.write_settings.write('\n'.join(self.settings))
        self.write_settings.close()
