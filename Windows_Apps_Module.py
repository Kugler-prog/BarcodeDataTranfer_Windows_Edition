import shutil

import psutil
import win32gui
import win32process
from pywinauto import Application


class WindowsAppHandler():
    def __init__(self):
        super().__init__()
        self.child_windows = []

    def WindowCallback(self,hwnd, param):
        self.child_windows.append(hwnd)
        return True

    def ProcessProcessor(self,ProcessTuple, Windowhandle):
        print("Aktiviert")
        currentTrueProcess = ""
        currentTrueHandle = ""


        if(win32gui.GetWindowText(Windowhandle) == "Windows Media Player"):
            print("Hab dich gefunden, playa")
            app = Application(backend="uia").connect(handle= Windowhandle)
            dlg = app.window(handle = Windowhandle)
            #print(dlg.print_control_identifiers())
            #print(app.Properties.child_window(title = "Status- und Befehlsleistenansicht"))
            res = dlg.window(title = "Status- und Befehlsleistenansicht")
            print(res.window_text())
            rest = res.child_window(control_type="Edit")
            löst = rest.get_value()
            prozess = win32process.GetWindowThreadProcessId(Windowhandle)
            proc = psutil.Process(prozess[1]).open_files()
            print(proc)
            press = dict(proc)
            for key, value in press.items():
                print(key)
                if (löst in key):
                    print("Begone Thost", key)
                    shutil.copy(key, "FileToServe")
                    return key



        win32gui.EnumChildWindows(Windowhandle,self.WindowCallback,None)
        for i in self.child_windows:
            if (win32gui.GetWindowText(i) != ""):
                print("Endlich ein Name", win32gui.GetWindowText(i))
                prozess = win32process.GetWindowThreadProcessId(i)
                proc = psutil.Process(prozess[1]).open_files()
                print(proc)
                currentTrueProcess = win32gui.GetWindowText(i)
                currentTrueHandle = i
        self.WindowAppsOperation(currentTrueProcess,currentTrueHandle)

    def WindowAppsOperation(self,Name,handler):
        print(handler)
        if(Name == "Filme & TV"):
            app = Application(backend="uia").connect(handle = handler)
            dlg = app.window(handle = handler)
            #print(dlg.print_control_identifiers())
            print(app.Properties.child_window(auto_id="MetadataPrimaryTextBlock"))
            res = dlg.window(auto_id = "MetadataPrimaryTextBlock").wrapper_object()
            tres = res.window_text()
            print(tres)
            prozesss = win32process.GetWindowThreadProcessId(handler)
            procs = psutil.Process(prozesss[1]).open_files()
            print(procs)
            pross = dict(procs)
            print(pross)
            for key, value in pross.items():
                print(key)
                if(tres in key):
                    print(key)
                    shutil.copy(key, "FileToServe")
                    return key

        if (Name == "Groove-Musik"):
            app = Application(backend="uia").connect(handle=handler)
            dlg = app.window(handle=handler)
            print(dlg.print_control_identifiers())
            print(app.Properties.child_window(auto_id="NavigateToNowPlayingPageButton"))
            res = dlg.window(auto_id="NavigateToNowPlayingPageButton").wrapper_object()
            tres = res.window_text()
            cres = tres.replace(", , Aktuelle Wiedergabe,","")
            print(cres)
            prozesss = win32process.GetWindowThreadProcessId(handler)
            procs = psutil.Process(prozesss[1]).open_files()
            print(procs)
            pross = dict(procs)
            print(pross)
            for key, value in pross.items():
                print(key)
                if (cres in key):
                    print("Begone Thost",key)
                    shutil.copy(key, "FileToServe")
                    return key

        if(Name == "Fotos"):
            app = Application(backend="uia").connect(handle=handler)
            dlg = app.window(handle=handler)
            #print(dlg.print_control_identifiers())
            print(app.Properties.child_window(auto_id="TitleBarTitle"))
            res = dlg.window(auto_id="TitleBarTitle").wrapper_object()
            tres = res.window_text()
            print(tres)
            prozesss = win32process.GetWindowThreadProcessId(handler)
            procs = psutil.Process(prozesss[1]).open_files()
            print(procs)
            pross = dict(procs)
            print(pross)
            for key, value in pross.items():
                #print(key)
                if (tres in key):
                    print("Begone Thost", key)
                    shutil.copy(key, "FileToServe")
                    return key
