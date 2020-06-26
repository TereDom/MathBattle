from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from requests import get

from MultitaskingFunctions import nice_view, onClicked, accept, search, num_operation, arithmetic_operation, \
    special_operation, exit_from_account, keyPressEvent, set_settings


class DeveloperClient(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/ui/developer_client.ui', self)
        self.settings = open('data/settings.txt', 'r').read().split('\n')
        set_settings(self)

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

        self.ButtonAccept.clicked.connect(self.accept)

        self.Button_1_1.toggled.connect(self.onClicked)
        self.Button_1_2.toggled.connect(self.onClicked)

        self.new_settings = {}

        self.ButtonExit.clicked.connect(self.exit_from_account)

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
        txt = open('data/settings.txt', 'r').read().split('\n')
        if str(txt[-1]) != "'":
            self.close()
            return exit_from_account(self, get(f'http://127.0.0.1:8080/api/user_information/{txt[-1]}').json())
        self.close()
        return

    def keyPressEvent(self, event):
        return keyPressEvent(self, event)
