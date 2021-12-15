import PIL
import cv2
from PyQt5.QtWidgets import QApplication
import sys
from Preprocessing import Preprocessing
from MyApp import MyApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget{
            font-size: 30px;
        }
    ''')
    myApp = MyApp()
    #myApp.mmPerPix = Preprocessing.readNumber(43, 96, 120, 120, myApp, 'x')
    #Pixels betweet chanells
    #myApp.chanY = Preprocessing.readNumber(220, 96, 262, 120, myApp, 'chanY')
    #myApp.compYPix = Preprocessing.readNumber(355, 96, 397, 120, myApp, 'compY Pixels')
    #myApp.x_scale_val, myApp.x_scale_pos = Preprocessing.findBeltX()
    #myApp.markedChannel, myApp.pixOfMChan = Preprocessing.findBeltChan()
    #compYZoom = Preprocessing.readNumber(415, 96, 457, 120)

    #im = PIL.ImageGrab.grab()
    ##im = im.crop((20, 157+(compYPix-1)*3, 100, 278+(compYPix-1)*3))
    #chanNumber = 1
    #chanNumber -= 1
    #y = 157 + (myApp.compYPix - 1) * 3 + chanNumber*(myApp.chanY-1)*2
    #print(str(myApp.markedChannel) + ";  " + str(myApp.pixOfMChan) + ";  " + str(y))
    #im = im.crop((20, y, 100, 278 + (compYPix - 1) * 3))
    #im.save("testy.png")
    #img = cv2.imread("testy.png")
    #cv2.line(img, (10, y), (700, y), (0, 255, 0), 1)
    #y2 = y+myApp.chanY*2-1
    #cv2.line(img, (10, y2), (700, y2), (0, 255, 0), 1)

    #cv2.imshow('res', img)
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
