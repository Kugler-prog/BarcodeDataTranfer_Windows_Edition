import math
import os
import win32gui
import win32process
from PyQt5.QtCore import Qt, QPoint
import segno
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PIL import Image
import  pyshorteners




import FileAquisitionandTransfer
import Server
import Windows_Apps_Module
from FileAquisitionandTransfer import fileSearch
child_handles = []
server_ip = Server.get_ip()

def WindowCallback(hwnd,param):
    child_handles.append(hwnd)
    return True


class QLabelMarker(QLabel):
    def __init__(self, steps=5, *args, **kwargs):
        super().__init__()
        self.initUI()



# Initialisierung des UI's
    def initUI(self):
        QLabel(self)
        pixmap = QPixmap()
        pixmap.load("CurrentCode.png")
        self.setPixmap(pixmap.scaled(60,60))
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.oldPos = self.pos()

#Methode mit welcher der Marker generiert wird, abhängig davon, ob der Fenstertitel Google-Chrome im Namen enthält wird entsprechend weiter die betreffende Datei gesucht
# Mithilfe eines shell-Dispatches wird das Ziel der ermittelten Verknüpfung ermittelt
# Wenn ein Fund erfolgt, wird es entsprechend in den FileToServe-Ordner kopiert
    def setMarker(self):
        if(len(os.listdir("FileToServe")) == 0):
            print()
        else:
            for f in os.listdir("FileToServe"):
                deleteFile = os.path.join("FileToServe/", f)
                os.remove(deleteFile)
        windowHandle = win32gui.GetForegroundWindow()

        if("Google Chrome" in win32gui.GetWindowText(win32gui.GetForegroundWindow())):
            returnedLink = FileAquisitionandTransfer.urlSearch(windowHandle)
            type_tiny = pyshorteners.Shortener()
            short_url = type_tiny.tinyurl.short(returnedLink)
            qrcode = segno.make(short_url)
            qrcode.save("CurrentCode.png", border=4)

        elif(fileSearch(windowHandle) == True):
            fileItem = os.listdir("FileToServe")[0]
            fileItem = fileItem.replace("\\","/")
            fileItem = fileItem.replace(" ","%20")
            qrcode = segno.make(f"{server_ip}:8000/{fileItem}")
            qrcode.save("CurrentCode.png", border=4)
        else:
            windowProcessor = Windows_Apps_Module.WindowsAppHandler()
            windowForeground = win32gui.GetForegroundWindow()
            process = win32process.GetWindowThreadProcessId(windowForeground)
            windowProcessor.ProcessProcessor(process[1],windowForeground)
            if(len(os.listdir("FileToServe")) != 0):
                fileItem = os.listdir("FileToServe")[0]
                fileItem = fileItem.replace("\\", "/")
                fileItem = fileItem.replace(" ", "%20")
                qrcode = segno.make(f"{server_ip}:8000/{fileItem}")
                qrcode.save("CurrentCode.png", border=4)


        pixmap = QPixmap("CurrentCode.png")
        self.setPixmap(pixmap.scaled(60, 60))



    def moveit(self):
        rect = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
        distance = rect[3] - rect[1]
        aproxxomatePoint = distance * 0.7
        newPosition = rect[1] + math.floor(aproxxomatePoint)

        if (rect[1] < 0):
            self.move(newPosition, rect[1] + 12)
        else:
            self.move(newPosition, rect[1])




