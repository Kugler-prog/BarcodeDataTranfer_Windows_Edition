import math

import qrcode as qrcode
import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QRunnable, QThreadPool
import segno
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QSvgRenderer, QSvgWidget
from PyQt5.QtWidgets import QLabel
from PIL import Image
import short_url
import qrcode

class Worker(QObject):
    finished = pyqtSignal()

    # def run(self):
    #
    #     print("Tehheehee")
    #     self.finished.emit()


class QLabelMarker(QLabel):
    """
    Custom Qt Widget to show a power bar and dial.
    Demonstrating compound and custom-drawn widget.
    """

    def __init__(self, steps=5, *args, **kwargs):
        super().__init__()
        self.initUI()

    # def runLongTask(self):
    #     self.thread = QThread()
    #     self.worker = Worker()
    #     self.worker.moveToThread(self.thread)
    #     self.thread.started.connect(self.worker.run)
    #     self.worker.finished.connect(self.thread.quit)
    #     self.worker.finished.connect(self.worker.deleteLater)
    #     self.thread.finished.connect(self.thread.deleteLater)
    #     self.thread.start()



    def initUI(self):
        #self.threadmanager = QThreadPool()
        #self.load("CurrentCode.svg")
        #self.resize(60,60)
        QLabel(self)
        pixmap = QPixmap()
        pixmap.load("CurrentCode.png")
        self.setPixmap(pixmap.scaled(56,56))
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        #self.setWindowFlags()


    #def changeImgae(self):
        #self.threadmanager.start(self.printing)


    def printing(self):
        print("Das ist das active Fenster", win32gui.GetWindowText(win32gui.GetActiveWindow()))
        print(win32gui.GetActiveWindow())

        qrcode = segno.make(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        qrcode.save("CurrentCode.png", border = 4)
        #self.load("CurrentCode.svg")

        # qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=1,border=1)
        # qr.add_data(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        # qr.make()
        # img = qr.make_image(fill_color="black", back_color ="white")
        # img.save("CurrentCode.png")
        # ig = Image.open("CurrentCode.png")
        # new_img = ig.resize((32,32))
        # new_img.save("CurrentCode.png","png",optimize = True)
        # print(img.width)
        # print(img.height)
        # self.clear()
        # #qrcode = segno.make(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        # #qrcode.save("CurrentCode.png")
        pixmap = QPixmap("CurrentCode.png")
        #
        self.setPixmap(pixmap.scaled(56,56))
        print("done")


    def moveit(self):
        rect = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
        distance = rect[2] - rect[0]
        aproxxomatePoint = distance * 0.7
        newPosition = rect[0] + math.floor(aproxxomatePoint)


        print("Ausgansgparameter:", rect, "\nDistantzzwischen dem linken und rechten Punkt beträgt:", distance,
              "\nDer ungefähre obere Punkt beträgt", aproxxomatePoint, "\nDie Koordinate ist ungefär", newPosition)

        if (rect[1] < 0):
            self.move(newPosition, rect[1] + 12)
            print("Wir haben ein vollbild")
        else:
            print("Wir haben hier einen Normie")
            self.move(newPosition, rect[1])




