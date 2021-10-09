from PIL import Image
import cv2
from openpyxl import Workbook, load_workbook
import os
import WarningWindow

class ImageProcessing:
    # def __init__(self):

    @staticmethod
    def binarization(openFile: str, savingFile: str, threshold: int):
        img = cv2.imread(openFile)
        th, im_th = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        cv2.imwrite(savingFile, im_th)

    @staticmethod
    def measurement(mmPerPix: int):
        if os.path.isfile('pomiaryUszkodzen.xlsx') and os.access('pomiaryUszkodzen.xlsx', os.W_OK):
            wb = load_workbook('pomiaryUszkodzen.xlsx')
        else:
            wb = Workbook()
        ws = wb.active
        ws.title = "dane"
        binarizated = Image.open('binarizated.png')
        width, height = binarizated.size
        yellow = True
        countingOn = False
        greenCounting = 0
        baseThreshold = 15
        damageLen = 0
        showedWarning = False
        showedWarning2 = False
        sheetRow = []
        for y in range(height):
            # Jeżeli poprzedni wiersz kończył się w pasku, a nie w "szarej strefie"
            if countingOn:
                if yellow == True:
                    print('| z ' + str((damageLen + greenCounting) * mmPerPix) + 'mm |')
                    #ws.append()
                else:
                    print('| n ' + str((damageLen + greenCounting) * mmPerPix) + 'mm |')
                damageLen = 0
                countingOn = False
                greenCounting = 0
                redCounting = 0
                if showedWarning == False:
                    WarningWindow('Możliwe ucięcie paska! Możliwie źle zapisane dane!')
                    showedWarning = True
            if list != []:
                ws.append(sheetRow)
            sheetRow.clear()
            print(str(y) + '  ')
            for x in range(width):
                p = binarizated.getpixel((x, y))
                if p[1] == 255:
                    # Jeśli kolor żółty
                    if p[0] == 255 and p[2] == 0:
                        if x == 0 and showedWarning == False:
                            WarningWindow('Możliwe ucięcie paska! Możliwie źle zapisane dane!')
                            showedWarning = True
                        # Przed żółtym jest czerwony
                        if redCounting > 0:
                            if yellow:
                                damageLen += redCounting + 1
                            else:
                                yellow = True
                            redCounting = 0
                        # Przed żółtym jest też piksel żółty
                        elif countingOn == True and yellow == True and greenCounting == 0:
                            damageLen += 1
                        # Przed żółtym jest niebieski
                        elif countingOn == True and yellow == False and greenCounting == 0:
                            print('| n ' + str(damageLen * mmPerPix) + 'mm |')
                            sheetRow.append('n ' + str(damageLen * mmPerPix) + 'mm')
                            damageLen = 1
                            yellow = True
                        # Przed żółtym jest szary
                        elif countingOn == False:
                            countingOn = True
                            damageLen = 1
                            yellow = True
                        # Przed żółtym jest zielony
                        else:
                            print('| n ' + str(damageLen * mmPerPix) + 'mm |')
                            sheetRow.append('n ' + str(damageLen * mmPerPix) + 'mm')
                            damageLen = greenCounting + 1
                            greenCounting = 0
                            yellow = True
                    # Jeśli kolor niebieski
                    elif p[0] == 0 and p[2] == 255:
                        if x == 0 and showedWarning == False:
                            WarningWindow('Możliwe ucięcie paska! Możliwie źle zapisane dane!')
                            showedWarning = True
                        if redCounting > 0:
                            if yellow == False:
                                damageLen += redCounting + 1
                            else:
                                yellow = False
                            redCounting = 0
                        # Przed niebieskim jest też piksel niebieski
                        elif countingOn == True and yellow == False and greenCounting == 0:
                            damageLen += 1
                        # Przed niebieskim jest żółty
                        elif countingOn == True and yellow == True and greenCounting == 0:
                            print('| z ' + str(damageLen * mmPerPix) + 'mm |')
                            sheetRow.append('z ' + str(damageLen * mmPerPix) + 'mm ')
                            damageLen = 1
                            yellow = False
                        # Przed niebieskim jest szary
                        elif countingOn == False:
                            countingOn = True
                            damageLen = 1
                            yellow = False
                        # Przed niebieskim jest zielony
                        else:
                            yellow = False
                            print('| z ' + str(damageLen * mmPerPix) + 'mm |')
                            sheetRow.append('z ' + str(damageLen * mmPerPix) + 'mm ')
                            damageLen = greenCounting + 1
                            greenCounting = 0
                    # kolor zielony
                    elif countingOn:
                        greenCounting += 1

                # kolor szary (lub jakiś błąd koloru czerwonego/niebieskiego)
                else:
                    # kolor czerwony
                    if p[0] == 255:
                        # dodane po pokazie u promo, bo czerwony przerywał paski z czarną ramką
                        #WarningWindow(
                        #    'Usun czerwony wskaznik z zaznaczonego pola! Możliwe błędne zapisanie danych!')
                        #showedWarning2 = True
                        #dodane po pokazie u promo, bo czerwony przerywał paski z czarną ramką
                        if showedWarning2 == False:
                            WarningWindow(
                                'Usun czerwony wskaznik z zaznaczonego pola! Możliwe błędne zapisanie danych!')
                            showedWarning2 = True
                        if countingOn:
                            redCounting += 1
                    else:
                        redCounting = 0
                    # zakończenie paska...
                    if countingOn:
                        countingOn = False
                        # ...żółtego
                        if yellow == True:
                            print('| z ' + str((damageLen + greenCounting) * mmPerPix) + 'mm |')
                            sheetRow.append('z ' + str((damageLen + greenCounting) * mmPerPix) + 'mm')
                            damageLen = 0
                            greenCounting = 0
                        # ...niebieskiego
                        else:
                            print('| n ' + str((damageLen + greenCounting) * mmPerPix) + 'mm |')
                            sheetRow.append('n ' + str((damageLen + greenCounting) * mmPerPix) + 'mm')
                            damageLen = 0
                            greenCounting = 0
        wb.save('pomiaryUszkodzen.xlsx')

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
    # def canalCounting(self):
