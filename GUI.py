import math
import os

import keyboard
import qrcode as qrcode
import win32api
import win32gui
import win32process
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
import validators
from keyboard import on_press, on_release
from pynput.keyboard import Key, Listener, KeyCode


import FileAquisitionandTransfer
from FileAquisitionandTransfer import fileSearch
import pathlib
import psutil
child_handles = []

def WindowCallback(hwnd,param):
    child_handles.append(hwnd)
    return True



class Worker(QObject):
    finished = pyqtSignal()

    # def run(self):
    #
    #     print("Tehheehee")
    #     self.finished.emit()


class KeyMonitor(QtCore.QObject):
    keyPressed = QtCore.pyqtSignal(KeyCode)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.listener = Listener(on_press = self.on_press)

    def on_press(self,key):
        if (key.char == "q"):
            print("Success")
        self.keyPressed.emit(key)

    def stop_monitoring(self):
        self.listener.stop()

    def start_monitoring(self):
        self.listener.start()






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

    def keyPressEvent(self, ev):
        if ev.char == "q":
            if(self.isVisible()):
                self.hide()
            else:
                self.printing()
                self.show()

            print("Wir haben hier ein event")

    def initUI(self):
        #self.threadmanager = QThreadPool()
        #self.load("CurrentCode.svg")
        #self.resize(60,60)qqqqqqq
        QLabel(self)
        pixmap = QPixmap()
        pixmap.load("CurrentCode.png")
        self.setPixmap(pixmap.scaled(60,60))
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        #self.setWindowFlags()


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
            qrcode = segno.make(linkforReturn)
            qrcode.save("CurrentCode.png", border=4)


        elif(flagOfFunction == True):
            fileItem = os.listdir("FileToServe")[0]
            fileItem = fileItem.replace("\\","/")
            fileItem = fileItem.replace(" ","%20")
            print("Das aktuelle Itel ist",fileItem)
            qrcode = segno.make(f"192.168.178.45:8000/{fileItem}")
            qrcode.save("CurrentCode.png", border=4)
        else:
            print(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
            tesxWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            handre = win32gui.GetForegroundWindow()
            process = win32process.GetWindowThreadProcessId(handre)
            print(process[1])
            win32gui.EnumChildWindows(handre,WindowCallback,None)
            print(child_handles)
            for i in child_handles:
                processList = win32process.GetWindowThreadProcessId(i)
                print(f"{i}:", win32process.GetWindowThreadProcessId(i))
                ppx = psutil.Process(processList[1]).open_files()
                print(ppx)
                for j in ppx:
                    if (tesxWindow in j[0]):
                        print("Gefunden",j)

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




        pixmap = QPixmap("CurrentCode.png")
        self.setPixmap(pixmap.scaled(60, 60))
        print("done")


    # def moveit(self):
    #     rect = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
    #     distance = rect[2] - rect[0]
    #     aproxxomatePoint = distance * 0.7
    #     newPosition = rect[0] + math.floor(aproxxomatePoint)
    #
    #
    #    # print("Ausgansgparameter:", rect, "\nDistantzzwischen dem linken und rechten Punkt beträgt:", distance,
    #          # "\nDer ungefähre obere Punkt beträgt", aproxxomatePoint, "\nDie Koordinate ist ungefär", newPosition)
    #
    #     if (rect[1] < 0):
    #         self.move(newPosition, rect[1] + 12)
    #        # print("Wir haben ein vollbild")
    #     else:
    #         #print("Wir haben hier einen Normie")
    #         self.move(newPosition, rect[1])




