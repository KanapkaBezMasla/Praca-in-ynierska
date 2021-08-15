from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDesktopWidget, QMessageBox
import sys
import PIL.ImageGrab
from PIL import Image
import cv2


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        screen = QDesktopWidget().screenGeometry()
        #app1 = QtWidgets.QApplication(sys.argv)
        #size = app1.primaryScreen().size()
        self.window_width, self.window_height = screen.width(), screen.height()-76
        self.setMinimumSize(self.window_width, self.window_height-35)
        self.setGeometry(0, 76, self.window_width, self.window_height-35)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.darkGray)
        self.setWindowOpacity(.20)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.begin, self.destination = QPoint(), QPoint()
        self.xBeg, self.yBeg = 0, 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.red)
        painter.drawPixmap(QPoint(), self.pix)
        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin, self.destination)
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.xBeg = event.globalX()
            self.yBeg = event.globalY()
            self.begin = event.pos()
            self.destination = self.begin
            self.update()
        elif event.buttons() & Qt.RightButton:
            exit(0)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if 76 < event.globalY() < self.window_height+39:
                self.destination = event.pos()
                self.update()
            #else:
            #    self.destination.setLocalPos

    #Przy puszczeniu myszki robiony jest zrzut ekranu, który jest przycinany do zaznaczonych wymiarów i zapisywany
    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            im = PIL.ImageGrab.grab()
            if self.xBeg < event.globalX():
                if self.yBeg < event.globalY():
                    cropped = im.crop((self.xBeg*2+1, self.yBeg*2+1, event.globalX()*2, event.globalY()*2))
                else:
                    cropped = im.crop((self.xBeg*2+1, event.globalY()*2+1, event.globalX()*2, self.yBeg*2))
            else:
                if self.yBeg < event.globalY():
                    cropped = im.crop((event.globalX() * 2 + 1, self.yBeg * 2 + 1, self.xBeg * 2, event.globalY() * 2))
                else:
                    cropped = im.crop((event.globalX() * 2 + 1, event.globalY() * 2 + 1, self.xBeg * 2, self.yBeg * 2))
            cropped.save("markedArea.png")
            #cropped.show()
            imProc = ImageProcessing()
            imProc.binarizationMIN()
            imProc.binarization('markedArea.png', 'binarizated.png', 200)
            imProc.measurement()
            # część do nie wymazywania prostokątów
    #        rect = QRect(self.begin, self.destination)
    #        painter = QPainter(self.pix)
    #        painter.drawRect(rect.normalized())

    #        self.begin, self.destination = QPoint(), QPoint()
    #        self.update()
##################################################################################################


class ImageProcessing:
    #def __init__(self):
        #self.emptyRows = []
        #for y in range(height):
        #    self.emptyRows.append(False)
        #self.imgProcessed = Image.new('RGB', [width, height], 0x000000)
    @staticmethod
    def binarization(openFile: str, savingFile: str, threshold: int):
        img = cv2.imread(openFile)
        th, im_th = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        cv2.imwrite(savingFile, im_th)

    @staticmethod
    def measurement():
        binarizated = Image.open('binarizated.png')
        width, height = binarizated.size
        for y in range(height):
            yellow = True
            countingOn = False
            baseThreshold = 15
            damageLen = 0
            showedWarning = False
            #Jeżeli poprzedni wiersz kończył się w pasku, a nie w "szarej strefie"
            if countingOn == True:
                if yellow == True:
                    print('| z ' + str(damageLen) + ' |')
                else:
                    print('| n ' + str(damageLen) + ' |')
                damageLen = 0
                countingOn = False
                if showedWarning == False:
                    print('Możliwe ucięcie paska! Możliwie źle zapisane dane!')
                    showedWarning = True
                #Dodać ostrzeżenie
            print(str(y) + '  ')
            for x in range(width):
                p = binarizated.getpixel((x, y))
                if p[1] == 255:
                    #Jeśli kolor żółty
                    if p[0] == 255 and p[2] == 0:
                        #Przed żółtym jest też piksel żółty
                        if countingOn == True and yellow == True:
                            damageLen += 1
                        #Przed żółtym jest niebieski
                        elif countingOn == True and yellow == False:
                            print('| n '+str(damageLen)+' |')
                            damageLen = 1
                            yellow = True
                        #Przed żółtym jest szary
                        elif countingOn == False:
                            countingOn = True
                            damageLen=1
                            yellow = True
                    #Jeśli kolor niebieski
                    elif p[0] == 0 and p[2] == 255:
                        #Przed niebieskim jest też piksel niebieski
                        if countingOn == True and yellow == False:
                            damageLen += 1
                        #Przed niebieskim jest żółty
                        elif countingOn == True and yellow == True:
                            print('| z '+str(damageLen)+' |')
                            damageLen = 1
                            yellow = False
                        #Przed niebieskim jest szary
                        elif countingOn == False:
                            countingOn = True
                            damageLen=1
                            yellow = False
                    #kolor zielony
                    #else:

                #kolor szary (lub jakiś błąd koloru czerwonego/niebieskiego)
                else:
                    #kolor czerwony
                    if p[0] == 255 and showedWarning == False:
                        #DODAĆ POWIADOMIENIE O BŁĘDZIE!!!!!!!!!!!!!!!!!!!!
                        print('Usun czerwony wskaznik z zaznaczonego pola! Możliwe błędne zapisanie danych!')
                        showedWarning = True
                    #zakończenie paska...
                    if countingOn == True:
                        countingOn = False
                        #...żółtego
                        if yellow == True:
                            print('| z ' + str(damageLen) + ' |')
                            damageLen = 0
                        #...niebieskiego
                        else:
                            print('| n ' + str(damageLen) + ' |')
                            damageLen = 0

    @staticmethod
    def binarizationMIN():
        img = Image.open('markedArea.png')
        width, height = img.size
        black_white = Image.new(mode="L", size=(width, height))

        for y in range(height):
            for x in range(width):
                p = img.getpixel((x, y))
                min_val = min(p[0], p[1], p[2])
                if min_val < 150:
                    min_val = 0
                else:
                    min_val = 255
                black_white.putpixel((x, y), min_val)
        black_white.save('chanels.png')





    #def canalCounting(self):


    #def binarization(self):
        #redTh = 150
        #blueTh = 150
        #width, height = self.img.size
        #print('tu jeszcze dziala')
        #for y in range(height):
        #    self.emptyRows[y] = True
        #    for x in range(width):
        #        p = self.img.getpixel((x, y))
        #        print(p)
        #        np = []
        #        np.append(int(0))
        #        np.append(int(0))
        #        print('gggg')
        #        if p[0] > redTh:
        #            print('jjjjj')
        #            np[0] = 255
        #            print('oooooo')
        #            np.append(int(0))
        #            self.emptyRows[y] = False
        #        elif p[2] > blueTh:
        #            np[0] = 0
        #            np.append(255)
        #            self.emptyRows[y] = False
        #        else:
        #            np[0] = 0
        #            np.append(int(0))
        #        print(np)
        #        npTuple = (int(np[0]), int(np[1]), int(np[2]))
        #        print(npTuple)
        #        self.imgProcessed.putpixel((x, y), npTuple)
        #print('sidjasid')
        #self.img.save("binarizated.png")


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
