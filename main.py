import http.server
import os
import threading
import sys
import ctypes.wintypes
import keyboard
import win32gui
from PyQt5 import QtWidgets
import GUI
from http.server import HTTPServer, SimpleHTTPRequestHandler


EVENT_SYSTEM_DIALOGSTART = 0x0008
WINEVENT_OUTOFCONTEXT = 0x0000
EVENT_SYSTEM_DIALOG_FOCUS = 0x0017


user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
ole32.CoInitialize(0)

Wind = win32gui.GetWindowText(win32gui.GetForegroundWindow())


class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, directory="FileToServe", **kwargs)
        print("activated")




class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Test"')
        self.send_header("Content-type", "text/html")
        self.end_headers()


    def do_GET(self):
        global key
        if self.headers.get("Authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write(b"no auth header received")
        elif self.headers.get("Authorization") == "Basic " + key:
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.get("Authorization").encode())
            self.wfile.write(b"not authenticated")


FileServer = HTTPServer(("",8000),ServerHandler)

def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    global Wind
    currentWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    if(currentWindow != Wind and event == 9 and currentWindow != "python"):
        displayedMarker.hide()
        print(win32gui.GetWindowText(win32gui.GetForegroundWindow()))

    if(event == 11):
        displayedMarker.show()
        displayedMarker.moveit()

    if(event == 22):
        print("Minimze")
        displayedMarker.hide()

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

WinEventProc = WinEventProcType(callback)

user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
hook = user32.SetWinEventHook(
    EVENT_SYSTEM_DIALOGSTART,
    EVENT_SYSTEM_DIALOG_FOCUS,
    0,
    WinEventProc,
    0,
    0,
    WINEVENT_OUTOFCONTEXT
)
if hook == 0:
    sys.exit(1)

msg = ctypes.wintypes.MSG()



if __name__ == '__main__':
    print(os.listdir("FileToServe"))
    for f in os.listdir("FileToServe"):
        deleteFile = os.path.join("FileToServe/",f)
        os.remove(deleteFile)


    app = QtWidgets.QApplication([])
    displayedMarker = GUI.QLabelMarker()
    FileServerThreaded = threading.Thread(name="daemon_backround_server",target=FileServer.serve_forever)
    FileServerThreaded.daemon = "True"
    FileServerThreaded.start()

    keyboard.add_hotkey("ctrl+alt+1", lambda:displayedMarker.standardSize())
    keyboard.add_hotkey("ctrl+alt+2", lambda: displayedMarker.doubleSize())
    keyboard.add_hotkey("ctrl+alt+3", lambda: displayedMarker.quadrupleSize())
    keyboard.add_hotkey("ctrl+alt+esc", lambda: displayedMarker.disappearevent())
    keyboard.add_hotkey("ctrl+alt+r", lambda: displayedMarker.resetPosition())

    displayedMarker.show()
    app.exec_()
