import math
import os

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
import  pyshorteners

import FileAquisitionandTransfer
from FileAquisitionandTransfer import fileSearch
import pathlib

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
        self.setPixmap(pixmap.scaled(60,60))
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        #self.setWindowFlags()


    #def changeImgae(self):
        #self.threadmanager.start(self.printing)


    def printing(self):
        if(len(os.listdir("FileToServe")) == 0):
            print("Wir haben hier eine leere vor uns")
        else:
            for f in os.listdir("FileToServe"):
                print(f)
                deleteFile = os.path.join("FileToServe/", f)
                print(deleteFile)
                os.remove(deleteFile)
        print(os.listdir("FileToServe"))
        print("Das ist das active Fenster", win32gui.GetWindowText(win32gui.GetActiveWindow()))
        print(win32gui.GetActiveWindow())
        windowHandle = win32gui.GetForegroundWindow()
        print("Wir rufen jetzt eine neue Variante auf")

        if("Google Chrome" in win32gui.GetWindowText(win32gui.GetForegroundWindow())):
            print("Google Chrome ist aktiv")
            linkforReturn = FileAquisitionandTransfer.urlSearch(windowHandle)
            print(linkforReturn)
            type_tiny = pyshorteners.Shortener()
            short_url = type_tiny.tinyurl.short(linkforReturn)
            qrcode = segno.make(short_url)
            qrcode.save("CurrentCode.png", border=4)
        else:
            fileSearch(windowHandle)
            fileItem = os.listdir("FileToServe")[0]
            fileItem = fileItem.replace("\\","/")
            fileItem = fileItem.replace(" ","%20")
            print("Das aktuelle Itel ist",fileItem)
            qrcode = segno.make(f"192.168.178.45:8000/{fileItem}")
            qrcode.save("CurrentCode.png", border=4)
        pixmap = QPixmap("CurrentCode.png")
        self.setPixmap(pixmap.scaled(60, 60))
        print("done")


    def moveit(self):
        rect = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
        distance = rect[2] - rect[0]
        aproxxomatePoint = distance * 0.7
        newPosition = rect[0] + math.floor(aproxxomatePoint)


       # print("Ausgansgparameter:", rect, "\nDistantzzwischen dem linken und rechten Punkt beträgt:", distance,
             # "\nDer ungefähre obere Punkt beträgt", aproxxomatePoint, "\nDie Koordinate ist ungefär", newPosition)

        if (rect[1] < 0):
            self.move(newPosition, rect[1] + 12)
           # print("Wir haben ein vollbild")
        else:
            #print("Wir haben hier einen Normie")
            self.move(newPosition, rect[1])




