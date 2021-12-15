from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDesktopWidget
import PIL.ImageGrab
from ImageProcessing import ImageProcessing
from Preprocessing import Preprocessing
from InsertionWindow import InsertionWindow


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.screen = QDesktopWidget().screenGeometry()
        self.window_width, self.window_height = self.screen.width(), self.screen.height() - 106
        self.setMinimumSize(self.window_width, self.window_height)
        self.setGeometry(0, 76, self.window_width, self.window_height)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.darkGray)
        self.setWindowOpacity(.20)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.imProc = ImageProcessing()
        self.preProc = Preprocessing()

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
        self.noAction = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.red)
        painter.drawPixmap(QPoint(), self.pix)
        if not self.begin.isNull() and not self.destination.isNull() and not self.noAction:
            rect = QRect(self.begin, self.destination)
            #rect = QRect(self.xBeg, self.yBeg, 100, 100)
            painter.drawRect(rect.normalized())
        painter.setPen(Qt.green)
        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        rect = QRect(self.screen.width()-10, 0, self.screen.width(), 10)
        painter.drawRect(rect.normalized())

    def mouseDoubleClickEvent(self, event):
        self.begin = None
        self.destination = None
        if event.x() > self.screen.width()-11 and event.y() < 11:
            print("idjfoweijfwejfowefj")


    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if event.x() < self.screen.width() - 11 and event.y() > 11:
                self.xBeg = event.globalX()
                self.yBeg = event.globalY()
                self.begin = event.pos()
                self.ydest = event.globalY()
                self.xdest = event.globalX()
                self.destination = self.begin
                self.noAction = False
                self.update()
            else:
                self.noAction = True
        elif event.buttons() & Qt.RightButton:
            exit(0)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and not self.noAction:
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
        if (event.button() & Qt.LeftButton) and abs(self.xBeg-self.xdest) > 10 and abs(self.yBeg - self.ydest) > 10 and not self.noAction:
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

            self.mmPerPix = self.preProc.readNumber(43, 96, 120, 120, self, 'x')
            # Pixels betweet chanells
            self.chanY = self.preProc.readNumber(220, 96, 262, 120, self, 'chanY')
            self.compYPix = self.preProc.readNumber(355, 96, 397, 120, self, 'compY Pixels')
            self.x_scale_val, self.x_scale_pos = self.preProc.findBeltX()
            self.markedChannel, self.pixOfMChan = self.preProc.findBeltChan()

            self.imProc.binarization('markedArea.png', 'binarizated.png', 200)
            self.imProc.measurement(self.mmPerPix, self.chanY, self.markedChannel, self.pixOfMChan, self.xBeg, self.yBeg, self.xdest, self.ydest, self.compYPix, self.x_scale_val, self.x_scale_pos)