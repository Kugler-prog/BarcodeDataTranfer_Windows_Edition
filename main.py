# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import base64
import ctypes
import http.server
import os
import threading
import sys
import time
import ctypes
import ctypes.wintypes
import pythoncom
import win32api
from PyQt5.QtCore import QRunnable, pyqtSignal, QThread, QThreadPool
from PyQt5.QtGui import QPixmap
from keyboard import on_press, on_release
import keyboard
from win32com.storagecon import *
import pywin
import win32gui
import winshell
from PyQt5 import QtCore,QtGui,QtWidgets

import GUI
import Server


from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler


EVENT_SYSTEM_DIALOGSTART = 0x0008
WINEVENT_OUTOFCONTEXT = 0x0000
EVENT_SYSTEM_DIALOG_FOCUS = 0x0017
key = "john"

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
ole32.CoInitialize(0)

Wind = win32gui.GetWindowText(win32gui.GetForegroundWindow())


class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, directory="FileToServe", **kwargs)
        print("activated")


class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Main class to present webpages and authentication."""

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
        """Present frontpage with user authentication."""
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
    #print("Das aktuelle Systemfenster ist",currentWindow)
    #print("Das globale Fenster ist",Wind)
    #print (event)
    if( currentWindow != Wind and event == 9 and currentWindow != "python"):
        volume.hide()
        print(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
    #   print("Neues Fenster erwählt")
    #     volume.show()
    #     print("Hier ist eine Abweichung")
       # Wind = currentWindow
    #     print(Wind)
    #     print(hex(event))
    #     height = (win32api.GetSystemMetrics(33) + win32api.GetSystemMetrics(4) +
    #               win32api.GetSystemMetrics(92))
    #     print("The height ist",height)
    #     volume.printing()

    if(event == 11):
        volume.show()
        volume.moveit()

    if(event == 22):
        print("Minimze")
        volume.hide()


    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        print('{0} released'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False



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
    print('SetWinEventHook failed')
    sys.exit(1)

msg = ctypes.wintypes.MSG()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(os.listdir("FileToServe"))
    for f in os.listdir("FileToServe"):
        print(f)
        deleteFile = os.path.join("FileToServe/",f)
        print(deleteFile)
        os.remove(deleteFile)

    print_hi('PyCharm')
    app = QtWidgets.QApplication([])
    volume = GUI.QLabelMarker()
    #volume.show()
    print(threading.active_count())

    FileServerThreaded = threading.Thread(name="daemon_backround_server",target=FileServer.serve_forever)
    FileServerThreaded.daemon = "True"
    FileServerThreaded.start()
    print(threading.active_count())
    #monitor = GUI.KeyMonitor()
    #monitor.keyPressed.connect(volume.keyPressEvent)
    #monitor.start_monitoring()
    keyboard.add_hotkey("ctrl+alt+1", lambda:volume.oneEvent())
    keyboard.add_hotkey("ctrl+alt+2", lambda: volume.secondEvent())
    keyboard.add_hotkey("ctrl+alt+3", lambda: volume.thirdEvent())
    keyboard.add_hotkey("ctrl+alt+esc", lambda: volume.disappearevent())
    keyboard.add_hotkey("ctrl+alt+r", lambda: volume.resetPosition())
    print("activated")
    volume.show()
    app.exec_()
    print(threading.active_count())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
