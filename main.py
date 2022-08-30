# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import ctypes
import threading
import sys
import time
import ctypes
import ctypes.wintypes
import pythoncom
import win32api
from PyQt5.QtCore import QRunnable, pyqtSignal, QThread, QThreadPool
from PyQt5.QtGui import QPixmap
from win32com.storagecon import *
import pywin
import win32gui
import winshell
from PyQt5 import QtCore,QtGui,QtWidgets

import GUI

EVENT_SYSTEM_DIALOGSTART = 0x0008
WINEVENT_OUTOFCONTEXT = 0x0000
EVENT_SYSTEM_DIALOG_FOCUS = 0x0009


user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
ole32.CoInitialize(0)

Wind = win32gui.GetWindowText(win32gui.GetForegroundWindow())
















def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    global Wind
    currentWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    #print("Das aktuelle Systemfenster ist",currentWindow)
    #print("Das globale Fenster ist",Wind)
    #print (event)
    if( currentWindow != Wind):
        print("Hier ist eine Abweichung")
        Wind = currentWindow
        print(Wind)
        print(hex(event))
        height = (win32api.GetSystemMetrics(33) + win32api.GetSystemMetrics(4) +
                  win32api.GetSystemMetrics(92))
        print("The height ist",height)
        volume.printing()






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
    print_hi('PyCharm')
    print(threading.active_count())
    app = QtWidgets.QApplication([])
    volume = GUI.QLabelMarker()
    volume.show()
    app.exec_()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
