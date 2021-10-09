from PyQt5.QtWidgets import QMessageBox


class WarningWindow:
    def __init__(self, text: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Ostrzeżenie!")
        msg.setInformativeText(text)
        x = msg.exec_()