import PIL
import cv2
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image


class Preprocessing:
    @staticmethod
    def readmmPerPix():
        im = PIL.ImageGrab.grab()
        mmPerPixIm = im.crop((43, 96, 120, 120))
        mmPerPixIm.save("mmPerPix.png")
        img = cv2.imread("mmPerPix.png")
        #img = cv2.resize(img, (0, 0), fx=3, fy=3)
        number = int(tess.image_to_string(img, lang='eng', config='--psm 7'))
        print(number)
        return number

    @staticmethod
    def readNumber(x1: int, y1: int, x2: int, y2: int):
        im = PIL.ImageGrab.grab()
        mmPerPixIm = im.crop((x1, y1, x2, y2))
        mmPerPixIm.save("number.png")
        img = cv2.imread("number.png")
        #img = cv2.resize(img, (0, 0), fx=3, fy=3)
        number = int(tess.image_to_string(img, lang='eng', config='--psm 7'))
        print(number)
        return number

    @staticmethod
    def findBeltX():
        im = PIL.ImageGrab.grab()
        width, height = im.size
        mmPerPixIm = im.crop((0, height-300, width, height-200))
        mmPerPixIm.save("beltX.png")
