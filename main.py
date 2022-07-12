# Diese Anwendung erstellt ein Overlayfenster, welches über das aktuell aktive Fenster im Vordergrund gelegt wird und einen Barcode mit der ID des Fensters als Hex-Zahl einblendet

#Import der benötigten Module, hierbei werden die folgenden Bibliotheken genutzt

#https://pypi.org/project/pywin32/
#https://pypi.org/project/python-barcode/
#https://docs.python.org/3/library/ctypes.html
#https://pypi.org/project/PyQt5/

import barcode.base
import win32gui
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from barcode import Code128
from barcode.writer import ImageWriter
import sys
import ctypes.wintypes
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

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

ole32.CoInitialize(0)

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
        barcodeGenerator(hex(activeWindow))
        modifiedCoordinates = calculateWindowDimensions(activeWindow)
        moveAndSizeOperation(modifiedCoordinates)
        overlayWindow.show()
    if (event == 23):
        overlayWindow.hide()

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


# Funktion mit welchen der Barcode generiert wird, hierbei wird der Funktion die Id des Fensters übergeben und als Input für die Code128()-Funktion genutzt. Aufgrund der Beschaffenheit akzeptiert die Code128()-Funktion nur Strings als Input, weswegen ein effektiverer Input in dieser Version (bislang) noch nicht möglich ist
def barcodeGenerator(windowId):
    with open(f'ExampleBarcode.png', "wb") as f:
        Code128(f'{windowId}', writer=ImageWriter()).write(f)


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
    displayedBarcode.move(windowDimensions[1] * 0.60, 0)
    currentPixmap = QPixmap("ExampleBarcode.png")
    displayedBarcode.setPixmap(currentPixmap.scaled(200, windowDimensions[0] * 4))
    overlayWindow.update()


# Hauptfunktion, hier wird das Overlay erstmalig initialisiert und entsprechend von den Attributen und Windowflags modifiziert, ebenso wird die QT-Hauptloop gestartet
if __name__ == '__main__':
    # In diesem Block wird das anfänglich aktivste, vorderste Fenster ermittelt, welches im Fokus liegt, dessen ID wird dann der barcode-Funktion übergeben, um einen korrespondierenden Barcode dynamisch zu generieren
    handleId = win32gui.GetForegroundWindow()
    win32gui.SetForegroundWindow(handleId)

    barcodeGenerator(hex(handleId))

    # Block der die Erschaffung des Fensters übernimmt und die Elemente festlegt, das Fenster besteht aus einem unsichtbaren Hauptfenster und einem Label, wo alles angezeigt wird
    app = QApplication(sys.argv)
    overlayWindow = QWidget()
    displayedBarcode = QLabel()
    pixMap = QPixmap("ExampleBarcode.png")
    displayedBarcode.setParent(overlayWindow)

    #Festlegen der Attribute und Flaggen
    overlayWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
    overlayWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
    overlayWindow.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
    displayedBarcode.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

    #Finaler Block, der für den Start die ersten Operationen durchführt
    windowDimensions = calculateWindowDimensions(handleId)
    moveAndSizeOperation(windowDimensions)
    overlayWindow.show()
    sys.exit(app.exec_())
