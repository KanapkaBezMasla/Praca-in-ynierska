import math
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
            #print(number)
        except ValueError:
            number = 0
            while number < 1:
                number, ok = QInputDialog.getInt(mainWin, 'Błąd zczytywania wartości',
                                            'Nie udało się zczytać wartości parametru "' +
                                            elementToRead + '".\n Proszę wprowadzić wartość ręcznie:')
                if ok and number > 0:
                    return number
                elif not ok:
                    quit()
        return number

    @staticmethod
    def findBeltX():
        im = PIL.ImageGrab.grab()
        width, height = im.size
        xpos = im.crop((46, 140, width-50, height-53))
        xpos = xpos.convert('L')
        xpos.save("beltX.png")
        imProc = ImageProcessing()
        imProc.binarization('beltX.png', 'beltXbin.png', 80)

        img = cv2.imread('beltXbin.png')
        cong = r'--oem 3 --psm 6 outputbase digits'
        boxes = tess.image_to_data(img, config=cong)
        x_val, global_x = 0, 0
        for x,b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                #print(b)
                if len(b) == 12:
                    print(b[11])
                    if(b[11]!= "1" and b[11]!= "." and b[11] != ","):
                        x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                        global_x = x + math.floor(w / 2) + 46
                        x_val = float(b[11])
                        #cv2.rectangle(img, (x, y), (w+x, h+y), 100, 1)
                        #img = cv2.line(img, (x + math.floor(w / 2), 500), (x + math.floor(w / 2), 1000), 100, 1)
                        #cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,110, 2)
                        break
        #cv2.imshow('res', img)
        return x_val, global_x

    @staticmethod
    def findBeltChan():
        im = PIL.ImageGrab.grab()
        width, height = im.size
        xpos = im.crop((4, 140, 50, height-90))
        xpos = xpos.convert('L')
        xpos.save("beltY.png")
        imProc = ImageProcessing()
        imProc.binarization('beltY.png', 'beltYbin.png', 80)

        img = cv2.imread('beltYbin.png')
        cong = r'--oem 3 --psm 6 outputbase digits'
        boxes = tess.image_to_data(img, config=cong)
        markedChannel = -1
        pixOfChan = -1
        for x,b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                if len(b) == 12:
                    x, y, w, h, text = int(b[6]), int(b[7]), int(b[8]), int(b[9]), b[11]
                    if text[len(text)-1] == '-':
                        text = text[0:len(text)-1]
                        markedChannel = int(text)
                        pixOfChan = y + math.ceil(h/2) + 140
                        #print(markedChannel)
                        #print(pixOfChan)
                        break
                    elif len(text) == 3:
                        markedChannel = int(text)
                        pixOfChan = y + math.ceil(h / 2) + 140
                        break
                    #print(str(y) + '<-y;w-> ' + str(math.ceil(h / 2)))
                    #img = cv2.line(img, (0, y + math.ceil(h / 2)), (40, y + math.ceil(h / 2)), 100, 1)
                    #cv2.rectangle(img, (x, y), (w+x, h+y), 100, 1)
                    #cv2.putText(img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,110, 2)
        #cv2.imshow('res', img)
        return markedChannel, pixOfChan
