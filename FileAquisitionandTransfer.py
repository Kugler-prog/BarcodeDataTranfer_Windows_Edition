import os
import shutil

import win32com.client
import win32gui
from pywinauto import Application

def fileSearch(hwnd):
    filepath = ""
    print(hwnd)
    Username = os.getenv("username")
    path = os.path.join("C:\\", "Users", Username, "AppData", "Roaming", "Microsoft", "Windows", "Recent")
    text = win32gui.GetWindowText(hwnd)
    print(os.listdir(path))
    print("Folgendes Item wird gesucht",text)
    ite = (item for item in os.listdir(path) if ".lnk" in item)
    for item in ite:
        test = os.path.basename(item[:-4])
        if(test in text):
            print("Ich habe das Item gefunden", test)
            combinedpath = os.path.join(path,item)
            print(combinedpath)

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(combinedpath)
            filepath = shortcut.Targetpath
            print(os.path.isdir(filepath))
            print("Der Betreffende PFad ist",filepath)
            if (os.path.isdir(filepath) == False):
                shutil.copy(filepath,"FileToServe")
    return filepath

def urlSearch(hwnd):
    link = ""
    text = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if ("Google Chrome" in text):
        print("hier ist ein browser")
        app = Application(backend="uia")
        app.connect(handle=hwnd)
        element_name = "Adress- und Suchleiste"
        dlg = app.top_window()
        wrapper = dlg.child_window(title=element_name, control_type="Edit")
        print(wrapper.get_value())
        link = wrapper.get_value()
    return link

