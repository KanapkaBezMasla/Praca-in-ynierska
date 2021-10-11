from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDesktopWidget
import sys
import PIL.ImageGrab
from ImageProcessing import ImageProcessing
import Preprocessing
from InsertionWindow import InsertionWindow


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        screen = QDesktopWidget().screenGeometry()
        # app1 = QtWidgets.QApplication(sys.argv)
        # size = app1.primaryScreen().size()
        self.window_width, self.window_height = screen.width(), screen.height() - 76
        self.setMinimumSize(self.window_width, self.window_height - 35)
        self.setGeometry(0, 76, self.window_width, self.window_height - 35)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.darkGray)
        self.setWindowOpacity(.20)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.begin, self.destination = QPoint(), QPoint()
        self.xBeg, self.yBeg = 0, 0
        self.xdest, self.ydest = 0, 0
        self.mmPerPix = -1
        # Pixels betweet chanells
        self.chanY = -1
        self.compYPix = -1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.red)
        painter.drawPixmap(QPoint(), self.pix)
        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin, self.destination)
            #rect = QRect(self.xBeg, self.yBeg, 100, 100)
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.xBeg = event.globalX()
            self.yBeg = event.globalY()
            self.begin = event.pos()
            self.ydest = event.globalY()
            self.xdest = event.globalX()
            self.destination = self.begin
            self.update()
            print(str(self.xBeg) + "; " + str(self.yBeg))
        elif event.buttons() & Qt.RightButton:
            exit(0)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if 76 < event.globalY() < self.window_height + 39:
                self.destination = event.pos()
                self.update()
                self.ydest = event.globalY()
                self.xdest = event.globalX()
            #else:
            #    self.xdest = event.globalX()
            #    if 76 > event.globalY():
            #        self.ydest = 77
            #    else:
            #        self.ydest = self.window_height + 38
    # Przy puszczeniu myszki robiony jest zrzut ekranu, który jest przycinany do zaznaczonych wymiarów i zapisywany
    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            im = PIL.ImageGrab.grab()
            if self.xBeg < event.globalX():
                if self.yBeg < event.globalY():
                    #cropped = im.crop((self.xBeg * 2 + 1, self.yBeg * 2 + 1, self.xdest * 2, self.ydest * 2))
                    self.xBeg, self.yBeg, self.xdest, self.ydest = self.xBeg * 2 + 1, self.yBeg * 2 + 1, self.xdest * 2, self.ydest * 2
                else:
                    #cropped = im.crop((self.xBeg * 2 + 1, event.globalY() * 2 + 1, self.xdest * 2, self.yBeg * 2))
                    self.xBeg, self.yBeg, self.xdest, self.ydest = self.xBeg * 2 + 1, event.globalY() * 2 + 1, self.xdest * 2, self.yBeg * 2
            else:
                if self.yBeg < event.globalY():
                    #cropped = im.crop((self.xdest * 2 + 1, self.yBeg * 2 + 1, self.xBeg * 2, self.ydest * 2))
                    self.xBeg, self.yBeg, self.xdest, self.ydest = self.xdest * 2 + 1, self.yBeg * 2 + 1, self.xBeg * 2, self.ydest * 2
                else:
                    #cropped = im.crop((self.xdest * 2 + 1, self.ydest * 2 + 1, self.xBeg * 2, self.yBeg * 2))
                    self.xBeg, self.yBeg, self.xdest, self.ydest = self.xdest * 2 + 1, self.ydest * 2 + 1, self.xBeg * 2, self.yBeg * 2

            cropped = im.crop((self.xBeg, self.yBeg, self.xdest, self.ydest))
            cropped.save("markedArea.png")
            # cropped.show()
            imProc = ImageProcessing()
            imProc.binarizationMIN()
            imProc.binarization('markedArea.png', 'binarizated.png', 200)
            imProc.measurement(self.mmPerPix)