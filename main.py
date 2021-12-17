from PyQt5.QtWidgets import QApplication
import sys
from MyApp import MyApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget{
            font-size: 30px;
        }
    ''')
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
