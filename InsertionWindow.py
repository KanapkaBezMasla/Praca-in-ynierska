import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
QLineEdit, QInputDialog)

class InsertionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Show Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Input Dialog')
        self.show()

    def showDialog(self):
        notReadedElement = 'x'
        text, ok = QInputDialog.getText(self, 'Błąd zczytywania wartości', 'Nie udało się zczytać wartości parametru "' +
                                        notReadedElement + '".\n Proszę wprowadzić wartość ręcznie:')
        if ok:
            self.le.setText(str(text))