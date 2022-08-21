# Diese Anwendung erstellt ein Overlayfenster, welches über das aktuell aktive Fenster im Vordergrund gelegt wird und einen Barcode mit der ID des Fensters als Hex-Zahl einblendet

#Import der benötigten Module, hierbei werden die folgenden Bibliotheken genutzt

#https://pypi.org/project/pywin32/
#https://pypi.org/project/python-barcode/
#https://docs.python.org/3/library/ctypes.html
#https://pypi.org/project/PyQt5/
import http.server
import os
import threading
from http.server import  HTTPServer
import psutil
import validators
import win32process
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import Server
import barcode.base
import win32gui
from PyQt5 import QtCore, QtSvg
from PyQt5.QtGui import QPixmap
import sys
import ctypes.wintypes
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import pyshorteners
import aztec_code_generator
from selenium import webdriver
from pdf417 import encode,render_image,render_svg
from pyqt_svg_label import SvgLabel
import qrcode.image.svg
import segno
import win32com.client
from pywinauto import Application
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
# Der Code für die Eventhook wurde mit leichten Veränderungen vollständig von dem folgenden Beitrag übernommen https://stackoverflow.com/questions/15849564/how-to-use-winapi-setwineventhook-in-python , entsprechende Abschnitte werden mit dem Präfix "Eventhook" bezeichnet
# Hier Werden die Eventkonstanten und die Kontext-Flagge gesetzt, welche darüber bestimmen, welche Events konkret gefiltert werden sollen und welche ignoriert werden sollen
# Zu einer genaueren Dokumentation der Kontextflaggen sei hierbei auf die Dokumentation hier verwiesen #https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook
# Eventkonstanten finden sich hier: https://docs.microsoft.com/en-gb/windows/win32/winauto/event-constants, Die Konstanten werden von den Methoden und als Output hierbei als int behandelt, es ist folglich die ein oder andere Umrechnung nötig
EVENT_SYSTEM_FOREGROUND = 0x0003
EVENT_OBJECT_LOCATIONCHANGE = 0x0016
EVENT_OBJECT_SIZECHANGE = 0x000A
WINEVENT_OUTOFCONTEXT = 0x0000
# Eventhook - Zugriff auf die beiden nötigen .dll Dateien und ihren Funktionen mithilfe von ctypes, da die Hookfunktionen von .dll-Dateien gehandhabt werden
user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
ipOfDevice = Server.get_ip()
ole32.CoInitialize(0)


#Einrichten der Directories, Standardports und Handlers für die beiden Webserver, über welche dann die Daten übertragen werden (C und D als Defaults in diesem Fall
C_DIRECTORY = "C:\\"
D_DIRECTORY = "D:\\"

C_PORT = 8000
D_PORT = 8080

class C_Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=C_DIRECTORY, **kwargs)
        print("activated")


class D_Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=D_DIRECTORY, **kwargs)


cDirectionServer = HTTPServer(("", C_PORT), C_Handler)
dDirectionServer = HTTPServer(("", D_PORT), D_Handler)

# Recherchen bisweilen noch nicht fortgeschritten genug, aktuelle Hypothese ist, dass es sich um eine Wrapper Funktion handelt, aufgrund der Nutzung von "ctypes"
WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)

# Callback Methode in welche die verschiedenen Events gehandhabt werden, die Events werden anhand eines int-Wertes beschrieben: Die Liste der Aktuell erfassten Events lautet:
# 11 - Fenster wurde resiszed oder bewegt
#  3 - Es wurde ein neues Hauptfenster ausgewählt mithilfe eines Klicks
# 23 - Das Fenster wurde minimiert

# Hierbei ist zu beachten, dass Windows verschiedene Werte für ähnliche Events hat, so wird unterschieden ob gerade angesetzt wird oder ob der Vorgang abgeschlossen wird,
# in diesem Fall wird anhand abgeschlossener Events gefiltert
def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    activeWindow = win32gui.GetForegroundWindow()
    if (event == 11):
        modifiedCoordinates = calculateWindowDimensions(activeWindow)
        moveAndSizeOperation(modifiedCoordinates)
    if (event == 3):
        print("Das aktive Fenster ist", win32gui.GetWindowText(activeWindow))
        modifiedCoordinates = calculateWindowDimensions(activeWindow)
        moveAndSizeOperation(modifiedCoordinates)
        name = win32gui.GetWindowText(activeWindow)
        restul = aquireInfo(activeWindow)
        print("Das restul ist",restul)
        print("wir haben hier nen leeren")
        link = getBrowserThingy(activeWindow)
        print(link)
        barcodeGenerator(ipOfDevice, restul)







# Eventhook - Code und Dokumentation müssen hierbei noch eingehender studiert werden, aber aus der Dokumentation zu der Windows WinEventHook lässt sich schließen, dass hierbei die hook initialisiert wird, welche die Events filtert
user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
WinEventProc = WinEventProcType(callback)
hook = user32.SetWinEventHook(
    EVENT_SYSTEM_FOREGROUND,
    EVENT_OBJECT_LOCATIONCHANGE,
    0,
    WinEventProc,
    0,
    0,
    WINEVENT_OUTOFCONTEXT
)

# Zeile mit welchem dem ImageWriter vom Barcode-Creator der Befehl gegeben wird, bei der Erstellung keinen Text mitanzugeben, der Inhalt wird damit nicht verändert, aber es wird im Bild Platz eingespart
# Zur Dokumentation vom Barcode-Package siehe hierzu  https://python-barcode.readthedocs.io/en/stable/
barcode.base.Barcode.default_writer_options["write_text"] = False


# In dieser Funktion wird jetzt ein PDF417-Barcode generiert,in welchen eine eigens erstellte URL encoded wird, welche aus dem Pfad für den Dateinamen besteht, mit welcher dann die Datei vom server "heruntergeladen" werden kann
def barcodeGenerator(windowId, filePathName):
    print("Der Pfad ist", filePathName)
    flag = ""
    convertedPath = ""
    convertedPath = filePathName.replace("\\", "/")
    pathDrivePrefix = filePathName[:2]
    if(pathDrivePrefix == "C:"):
        print("Ein C-Verzeichnis")
        flag = C_PORT
    elif(pathDrivePrefix =="D:"):
        print("Ein D-Verzeichnis ")
        flag = D_PORT
    currentPort = flag
    url = f"{windowId}:{currentPort}/{convertedPath[3:]}"
    print("Der Pfad ist",url)
    image = segno.make(url)
    image.save("ExampleBarcode.png")
    currentPixmap = QPixmap("ExampleBarcode.png")
    displayedBarcode.setPixmap(currentPixmap)


def aquireInfo(hwndName):
    print(hwndName, win32gui.GetWindowText(hwndName))
    pathResult = ""
    text = win32gui.GetWindowText(hwndName)
    print(type(win32gui.GetWindowText(hwndName)))
    Username = os.getenv("username")
    path = os.path.join("C:\\","Users",Username,"AppData","Roaming","Microsoft","Windows","Recent")
    print(os.listdir(path))
    for item in os.listdir(path):
        test = item[:-4]
        #print(item)
        if( test in text):
            print("habe das entsprechende Item gefunden")
            fileThingy = os.path.join(path,item)
            print(fileThingy)
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(fileThingy)
            pathResult = shortcut.Targetpath
            print(pathResult)
    return pathResult

def getBrowserThingy(hwnd):
    linkforReturn = ""
    text = win32gui.GetWindowText(hwnd)
    if("Chrome" in text):
        print("hier ist ein browser")
        app = Application(backend="uia")
        app.connect(handle=hwnd)
        element_name = "Adress- und Suchleiste"
        dlg = app.top_window()
        wrapper = dlg.child_window(title=element_name, control_type="Edit")
        print(wrapper.get_value())
        linkforReturn = wrapper.get_value()
    return linkforReturn





#Funktion mit welchen die Dimensionen des aktiven Fensters kalkuliert wird. Hierbei deren die GetWindowRect() und GetClientRect() - Funktionen genutzt, um die größe und die Ränder zu ermitteln,
#da bisher noch kein Windows-Äquivalent für die Xlib Frame Extents gefunden wurde
#Die Methode exportiert hierbei die Höhe,Weite, Frame Extents und die ersten beiden Rect-Koordinaten mit, welche die lage der linken oberen Ecke festlegen
def calculateWindowDimensions(windowId):
    windowFrameRectangle = win32gui.GetWindowRect(windowId)
    clientRectangle = win32gui.GetClientRect(windowId)
    windowWidth = windowFrameRectangle[2] - windowFrameRectangle[0]
    windowHeight = windowFrameRectangle[3] - windowFrameRectangle[1]
    windowOffset = windowHeight - clientRectangle[3]

    return windowOffset, windowWidth, windowHeight, windowFrameRectangle[0], windowFrameRectangle[1]

# Diese Funktion übernimmt die Operationen zur Veränderung der Größe und Lage des Fensters, wenn das aktive Fenster bewegt oder in der Größe verändert wird. Hierbei wird auch die Pixmap,
# welche den Barcode anzeigt aktualisiert, wenn sich das aktive Fenster zwischendurch ändern sollte, wodurch sich auch der Inhalt des Barcodes ändern würde
def moveAndSizeOperation(windowDimensions):

    overlayWindow.resize(windowDimensions[1], windowDimensions[2])
    overlayWindow.move(windowDimensions[3], windowDimensions[4])
    displayedBarcode.move(int(windowDimensions[1] * 0.40), 0)
    currentPixmap = QPixmap("ExampleBarcode.png")
    displayedBarcode.setPixmap(currentPixmap)
    overlayWindow.update()

# Hauptfunktion, hier wird das Overlay erstmalig initialisiert und entsprechend von den Attributen und Windowflags modifiziert, ebenso wird die QT-Hauptloop gestartet
if __name__ == '__main__':
    # In diesem Block wird das anfänglich aktivste, vorderste Fenster ermittelt, welches im Fokus liegt, dessen ID wird dann der barcode-Funktion übergeben, um einen korrespondierenden Barcode dynamisch zu generieren
    handleId = win32gui.GetForegroundWindow()
    win32gui.SetForegroundWindow(handleId)







    # Block der die Erschaffung des Fensters übernimmt und die Elemente festlegt, das Fenster besteht aus einem unsichtbaren Hauptfenster und einem Label, wo alles angezeigt wird
    app = QApplication(sys.argv)
    overlayWindow = QWidget()
    displayedBarcode = SvgLabel()
    pixMap = QPixmap("ExampleBarcode.png")
    displayedBarcode.setParent(overlayWindow)

    #Festlegen der Attribute und Flaggen
    overlayWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
    overlayWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
    overlayWindow.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
    displayedBarcode.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)


    #Finaler Block, der für den Start die ersten Operationen durchführt
    windowDimensions = calculateWindowDimensions(handleId)
    #print(f"Hier ist die Id {handleId}")
    name = win32gui.GetWindowText(handleId)
    #print(f"Der Fenstername ist {name}",type(name))
    #print("Windowinfo is",win32process.GetWindowThreadProcessId(handleId))
    win32gui.UpdateWindow(handleId)
    moveAndSizeOperation(windowDimensions)
    overlayWindow.show()


    #Aktivieren der Threads für die beiden Verzeichnisserver
    cThreadedServer = threading.Thread(name="daemon_server", target=cDirectionServer.serve_forever)
    cThreadedServer.daemon = True
    cThreadedServer.start()

    dThreadedServer = threading.Thread(name="second_server", target=dDirectionServer.serve_forever)
    dThreadedServer.daemon = True
    dThreadedServer.start()




    sys.exit(app.exec_())
