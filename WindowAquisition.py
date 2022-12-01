import shutil

import psutil
import win32gui
import win32process
from pywinauto import Application

# Module, welches für die Erfassung des Inhalts von Windows-Anwendungen zuständig ist

class WindowsAppHandler():
    def __init__(self):
        super().__init__()
        self.child_windows = []

    def WindowCallback(self,hwnd, param):
        self.child_windows.append(hwnd)
        return True

    def ProcessProcessor(self,ProcessTuple, Windowhandle):
        currentTrueProcess = ""
        currentTrueHandle = ""

# Diese Methode ist auch identisch für untere Verläufe, hierbei wird mithilfe von pywinauto das vorher ermittelte Element adressiert, welches den Dateititel enthält
# Von diesem wird dann der Inhalt ermittelt und mithilfe des zuständigen Prozesses der Filehandle gesucht, welcher mit den Dateinamen im Element übereinstimmt
# Wird ein Element gefunden, so wird dieses in den FileServed - Ordner kopiert
# Dieser Ablauf ist identisch für alle weiter unten aufgelistete Fenster - Die unterschiede liegen lediglich im Element, welches verwendet wird
        if(win32gui.GetWindowText(Windowhandle) == "Windows Media Player"):
            app = Application(backend="uia").connect(handle= Windowhandle)
            windowToConnectTo = app.window(handle = Windowhandle)
            elementWithContent = windowToConnectTo.window(title = "Status- und Befehlsleistenansicht")
            childWithContent = elementWithContent.child_window(control_type="Edit")
            valueOfChild = childWithContent.get_value()
            processId = win32process.GetWindowThreadProcessId(Windowhandle)
            processParameter = psutil.Process(processId[1]).open_files()
            parameterDictionary = dict(processParameter)
            for key, value in parameterDictionary.items():
                if (valueOfChild in key):
                    shutil.copy(key, "FileServed")
                    return key



        win32gui.EnumChildWindows(Windowhandle,self.WindowCallback,None)
        for i in self.child_windows:
            if (win32gui.GetWindowText(i) != ""):
                currentTrueProcess = win32gui.GetWindowText(i)
                currentTrueHandle = i
        self.WindowAppsOperation(currentTrueProcess,currentTrueHandle)

    def WindowAppsOperation(self,Name,handler):
        if(Name == "Filme & TV"):
            app = Application(backend="uia").connect(handle = handler)
            windowToConnectTo = app.window(handle = handler)
            elementWithContent = windowToConnectTo.window(auto_id = "MetadataPrimaryTextBlock").wrapper_object()
            childWithContent = elementWithContent.window_text()
            processId = win32process.GetWindowThreadProcessId(handler)
            processParameter = psutil.Process(processId[1]).open_files()
            parameterDictionary = dict(processParameter)
            for key, value in parameterDictionary.items():
                if(childWithContent in key):
                    shutil.copy(key, "FileServed")
                    return key

        if (Name == "Groove-Musik"):
            app = Application(backend="uia").connect(handle=handler)
            windowToConnectTo = app.window(handle=handler)
            elementWithContent = windowToConnectTo.window(auto_id="NavigateToNowPlayingPageButton").wrapper_object()
            childWithContent = elementWithContent.window_text()
            # Erforderlicher Ersatz, wegen der Art und Weise wie Groove-Musik mit den Namen umgeht
            contentReplacement = childWithContent.replace(", , Aktuelle Wiedergabe,","")
            processId = win32process.GetWindowThreadProcessId(handler)
            processParameter = psutil.Process(processId[1]).open_files()
            parameterDictionary = dict(processParameter)
            for key, value in parameterDictionary.items():
                if (contentReplacement in key):
                    shutil.copy(key, "FileServed")
                    return key

        if(Name == "Fotos"):
            app = Application(backend="uia").connect(handle=handler)
            windowToConnectTo = app.window(handle=handler)
            elementWithContent = windowToConnectTo.window(auto_id="TitleBarTitle").wrapper_object()
            childWithContent = elementWithContent.window_text()
            processId = win32process.GetWindowThreadProcessId(handler)
            processParameter = psutil.Process(processId[1]).open_files()
            parameterDictionary = dict(processParameter)
            for key, value in parameterDictionary.items():
                if (childWithContent in key):
                    shutil.copy(key, "FileServed")
                    return key
