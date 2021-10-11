import PIL
import cv2
import pytesseract as tess

tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from ImageProcessing import ImageProcessing
from PyQt5.QtWidgets import (QWidget, QInputDialog)


class Preprocessing:
    @staticmethod
    def readNumber(x1: int, y1: int, x2: int, y2: int, mainWin: QWidget, elementToRead: str):
        im = PIL.ImageGrab.grab()
        mmPerPixIm = im.crop((x1, y1, x2, y2))
        mmPerPixIm.save("number.png")
        img = cv2.imread("number.png")
        #img = cv2.resize(img, (0, 0), fx=3, fy=3)
        try:
            number = int(tess.image_to_string(img, config='--psm 7'))
            print(number)
        except ValueError:
            number, ok = QInputDialog.getInt(mainWin, 'Błąd zczytywania wartości',
                                            'Nie udało się zczytać wartości parametru "' +
                                            elementToRead + '".\n Proszę wprowadzić wartość ręcznie:')
            if ok:
                return number
        return number

    @staticmethod
    def findBeltX():
        im = PIL.ImageGrab.grab()
        width, height = im.size
        xpos = im.crop((45, 140, width-50, height-55))
        xpos = xpos.convert('L')
        xpos.save("beltX.png")
        imProc = ImageProcessing()
        imProc.binarization('beltX.png', 'beltXbin.png', 80)

        img = cv2.imread('beltXbin.png')
        cong = r'--oem 3 --psm 6 outputbase digits'
        boxes = tess.image_to_data(img, config=cong)
        for x,b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                print(b)
                if len(b) == 12:
                    x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                    cv2.rectangle(img, (x, y), (w+x, h+y), 100, 1)
                    cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,110, 2)
        cv2.imshow('res', img)

