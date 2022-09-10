import math
import os

import keyboard
import qrcode as qrcode
import win32api
import win32gui
import win32process
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QRunnable, QThreadPool, QMimeData, QPoint
import segno
from PyQt5.QtGui import QPixmap, QDrag, QPainter
from PyQt5.QtSvg import QSvgRenderer, QSvgWidget
from PyQt5.QtWidgets import QLabel, QApplication
from PIL import Image
import short_url
import qrcode
import  pyshorteners
import validators
import keyboard



import FileAquisitionandTransfer
import Server
import Windows_Apps_Module
from FileAquisitionandTransfer import fileSearch
import pathlib
import psutil
child_handles = []

server_ip = Server.get_ip()
def WindowCallback(hwnd,param):
    child_handles.append(hwnd)
    return True


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

    def getImageSize(self):
        im = Image.open("CurrentCode.png")
        h,w = im.size
        return im.size


    def oneEvent(self):
        size = self.getImageSize()
        if (not self.isVisible()):
            self.show()
        else:
            self.show()
            self.resize(size[0],size[1])
            self.printing()
            pixmap = QPixmap("CurrentCode.png")
            self.setPixmap(pixmap.scaled(size[0], size[1]))

    def secondEvent(self):
        size = self.getImageSize()
        if (not self.isVisible()):
            self.show()
        else:
            self.resize(size[0]*2, size[1]*2)
            self.printing()
            pixmap = QPixmap("CurrentCode.png")
            self.setPixmap(pixmap.scaled(size[0]*2, size[1]*2))

    def thirdEvent(self):
        size = self.getImageSize()
        if (not self.isVisible()):
            self.show()
        else:
            self.show()
            self.resize(size[0]*4, size[1]*4)
            self.printing()
            pixmap = QPixmap("CurrentCode.png")
            self.setPixmap(pixmap.scaled(size[0]*4, size[1]*4))

    def disappearevent(self):
        if(self.isVisible()):
            self.hide()

    def resetPosition(self):
        self.move(0,0)


    def mousePressEvent(self, ev):
        self.oldPos = ev.globalPos()

    def mouseMoveEvent(self, ev):
        delta = QPoint(ev.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = ev.globalPos()


    def initUI(self):
        #self.threadmanager = QThreadPool()
        #self.load("CurrentCode.svg")
        #self.resize(60,60)qqqqqqq
        QLabel(self)
        pixmap = QPixmap()
        pixmap.load("CurrentCode.png")
        self.setPixmap(pixmap.scaled(60,60))
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.oldPos = self.pos()


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
        print("Das ist das active Fenster", win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        print(win32gui.GetActiveWindow())
        windowHandle = win32gui.GetForegroundWindow()
        print("Wir rufen jetzt eine neue Variante auf")
        flagOfFunction = fileSearch(windowHandle)

        if("Google Chrome" in win32gui.GetWindowText(win32gui.GetForegroundWindow())):
            print("Google Chrome ist aktiv")
            linkforReturn = FileAquisitionandTransfer.urlSearch(windowHandle)
            print(linkforReturn)
            type_tiny = pyshorteners.Shortener()
            short_url = type_tiny.tinyurl.short(linkforReturn)
            qrcode = segno.make(short_url)
            qrcode.save("CurrentCode.png", border=4)


        elif(flagOfFunction == True):
            fileItem = os.listdir("FileToServe")[0]
            fileItem = fileItem.replace("\\","/")
            fileItem = fileItem.replace(" ","%20")
            print("Das aktuelle Itel ist",fileItem)
            qrcode = segno.make(f"{server_ip}:8000/{fileItem}")
            qrcode.save("CurrentCode.png", border=4)
        else:
            WindowProcessor = Windows_Apps_Module.WindowsAppHandler()
            WindowsWindow = win32gui.GetForegroundWindow()
            process = win32process.GetWindowThreadProcessId(WindowsWindow)
            print("Leider konnten wir hier nix finden",process[1])
            WindowProcessor.ProcessProcessor(process[1],WindowsWindow)
            if(len(os.listdir("FileToServe")) != 0):
                fileItem = os.listdir("FileToServe")[0]
                fileItem = fileItem.replace("\\", "/")
                fileItem = fileItem.replace(" ", "%20")
                qrcode = segno.make(f"{server_ip}:8000/{fileItem}")
                qrcode.save("CurrentCode.png", border=4)


        pixmap = QPixmap("CurrentCode.png")
        self.setPixmap(pixmap.scaled(60, 60))
        print("done")

            # print(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
            # tesxWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            # handre = win32gui.GetForegroundWindow()
            # process = win32process.GetWindowThreadProcessId(handre)
            # print(process[1])
            # win32gui.EnumChildWindows(handre,WindowCallback,None)
            # print(child_handles)
            # for i in child_handles:
            #     processList = win32process.GetWindowThreadProcessId(i)
            #     print(f"{i}:", win32process.GetWindowThreadProcessId(i))
            #     ppx = psutil.Process(processList[1]).open_files()
            #     print(ppx)
            #     for j in ppx:
            #         if (tesxWindow in j[0]):
            #             print("Gefunden",j)

            #     processs = win32process.GetWindowThreadProcessId(i)
            #     print(processs[1])
            #     pp = psutil.Process(process[1]).name()
            #     ppx = psutil.Process(process[1]).open_files()
            #     print(pp)
            #     print(ppx)
            #     if(pp == "ApplicationFrameHost.exe"):
            #         pass
            #     else:
            #       print(pp)
            #       print(processs[1])
            #       print(win32gui.GetWindowText(i))


            #pruc = psutil.Process(12152).cmdline()
            #print(pruc)
            # print(win32gui.GetWindowText(264892))
            # proc = win32process.GetWindowThreadProcessId(264892)
            # print(proc)
            # prec = psutil.Process(proc[1]).open_files()
            # print(prec)
          # hw = win32gui.GetForegroundWindow()
          # print("Sie haben aktuell das Fenster offen", hw)
          # print(win32gui.GetWindowText(hw))
          # print(process[1])
          # p = psutil.Process(process[1]).open_files()
          # print(p)

          # #print(win32api.GetModuleFileName(process[1]))
          # print(child_handles)




    def moveit(self):
        rect = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
        distance = rect[3] - rect[1]
        aproxxomatePoint = distance * 0.7
        newPosition = rect[1] + math.floor(aproxxomatePoint)


       # print("Ausgansgparameter:", rect, "\nDistantzzwischen dem linken und rechten Punkt beträgt:", distance,
             # "\nDer ungefähre obere Punkt beträgt", aproxxomatePoint, "\nDie Koordinate ist ungefär", newPosition)

        if (rect[1] < 0):
            self.move(newPosition, rect[1] + 12)
           # print("Wir haben ein vollbild")
        else:
            #print("Wir haben hier einen Normie")
            self.move(newPosition, rect[1])




