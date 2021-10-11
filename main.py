from PyQt5.QtWidgets import QApplication
import sys
import PIL.ImageGrab
from ImageProcessing import ImageProcessing
from Preprocessing import Preprocessing
from InsertionWindow import InsertionWindow
from MyApp import MyApp


if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #ex = InsertionWindow()
    #sys.exit(app.exec_())
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget{
            font-size: 30px;
        }
    ''')
    myApp = MyApp()
    myApp.mmPerPix = Preprocessing.readNumber(43, 96, 120, 120, myApp, 'x')
    #Pixels betweet chanells
    myApp.chanY = Preprocessing.readNumber(220, 96, 262, 120, myApp, 'chanY')
    myApp.compYPix = Preprocessing.readNumber(355, 96, 397, 120, myApp, 'compY Pixels')
    Preprocessing.findBeltX()
    #compYZoom = Preprocessing.readNumber(415, 96, 457, 120)

    #im = PIL.ImageGrab.grab()
    ##im = im.crop((20, 157+(compYPix-1)*3, 100, 278+(compYPix-1)*3))
    #chanNumber = 2
    #chanNumber -= 1
    #y = 157 + (compYPix - 1) * 3 + chanNumber*(chanY-1)*2
    #im = im.crop((20, y, 100, 278 + (compYPix - 1) * 3))
    #im.save("testy.png")
    #im.show()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
