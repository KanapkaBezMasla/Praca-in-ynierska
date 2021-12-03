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
        self.window_width, self.window_height = screen.width(), screen.height() - 106
        self.setMinimumSize(self.window_width, self.window_height)
        self.setGeometry(0, 76, self.window_width, self.window_height)
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
        self.markedChannel = -1
        self.pixOfMChan = -1
        self.x_scale_pos = -1
        self.x_scale_val = -1

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
            #print(str(self.xBeg) + "; " + str(self.yBeg))
        elif event.buttons() & Qt.RightButton:
            exit(0)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if 76 < event.globalY() < self.window_height + 70:
                self.destination = event.pos()
                self.update()
                self.ydest = event.globalY()
                self.xdest = event.globalX()
            else:
                if 76 > event.globalY():
                    self.destination.setY(1)
                else:
                    self.destination.setY(self.window_height-13)
                self.destination.setX(event.globalX())
                self.update()
                self.xdest = event.globalX()
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
            imProc.measurement(self.mmPerPix, self.chanY, self.markedChannel, self.pixOfMChan, self.xBeg, self.yBeg, self.xdest, self.ydest, self.compYPix, self.x_scale_val, self.x_scale_pos)