import ctypes.wintypes
import sys
import threading
from twisted.web import guard
from twisted.web._auth.digest import DigestCredentialFactory
from twisted.web.server import Site
from twisted.internet import reactor, ssl, endpoints
from twisted.web.static import File
from twisted.cred.checkers import FilePasswordDB
from zope.interface import implementer
from twisted.web.resource import IResource
from twisted.cred.portal import IRealm, Portal
import win32gui
from PyQt6.QtWidgets import QApplication


import QR_Label
import configparser

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
ole32.CoInitialize(0)

EVENT_SYSTEM_DIALOGSTART = 0x0008
WINEVENT_OUTOFCONTEXT = 0x0000
EVENT_SYSTEM_DIALOG_FOCUS = 0x0017
previousWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())

def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    global previousWindow
    currentWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    wind = win32gui.GetForegroundWindow()
    if event == 9 and (previousWindow != currentWindow and not currentWindow == "python"):
        displayedMarker.Label.moveit(wind)
        previousWindow = currentWindow
        displayedMarker.Label.printingMarker(wind)
    if(event == 11):
        displayedMarker.Label.moveit(wind)


## Block, welcher mithilfe eines Ctypes eine Eventhook einrichtet, die Windows Events erfasst, der Input wird mithilfe eines Callbacks verarbeitet

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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.



# Block, welcher zuständig für die Einrichtung der Authentifikation beim Twisted webserver zuständig ist, basierend auf
@implementer(IRealm)
class PublicHTMLRealm(object):

    def __init__(self, root):
        self.root = root

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IResource in interfaces:
            return (IResource,self.root, lambda: None)
        raise NotImplementedError()

def build_sharing_resource():
    root = build_shared_folder_resource()
    portal = Portal(PublicHTMLRealm(root), [FilePasswordDB('httpd.password')])

    credentialFactory = DigestCredentialFactory(b"md5", b"Einloggen zum Downloaden")
    return guard.HTTPAuthSessionWrapper(portal, [guard.BasicCredentialFactory(b"auth")])



def build_shared_folder_resource():
    root = File("./FileServed")
    return root













# Starten der Anwendung, mit einem vorgegebenen Port, sowie der Start des Twisted-Webserver mithilfe eines ewactors, sowie das Einbinden der Zertifikate
if __name__ == '__main__':
    print_hi('PyCharm')

    ssl_context = ssl.DefaultOpenSSLContextFactory(privateKeyFileName="certs/localhost+1-key.pem",
                                                   certificateFileName="certs/localhost+1.pem")
    port = 8000
    root = build_sharing_resource()
    factory = Site(root)
    reactor.listenSSL(port, factory, ssl_context)
    print('server is running on %i' % (port,))




    # Ermittlung der Default-Caption-size um das Icon in die Leiste zu integrieren sowie Start der Anwendung und des Server-Thread
    app = QApplication(sys.argv)
    config = configparser.ConfigParser()
    serverThread = threading.Thread(
        target=reactor.run,
        kwargs={"installSignalHandlers": False},
        daemon=True,
    )
    serverThread.start()


    displayedMarker = QR_Label.FullApplication()
    app.exec()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
