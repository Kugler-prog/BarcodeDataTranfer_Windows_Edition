import os
import shutil
import win32com.client
import win32gui
from pywinauto import Application

def fileSearch(hwnd):
    filepath = ""
    foundflag = False

    username = os.getenv("username")
    path = os.path.join("C:\\", "Users", username, "AppData", "Roaming", "Microsoft", "Windows", "Recent")
    windowTitleName = win32gui.GetWindowText(hwnd)
    recentContentList = (item for item in os.listdir(path) if ".lnk" in item)
    for item in recentContentList:
        fileToCheck = os.path.basename(item[:-4])
        if(fileToCheck in windowTitleName):
            foundflag = True
            combinedpath = os.path.join(path,item)
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(combinedpath)
            filepath = shortcut.Targetpath
            if (os.path.isdir(filepath) == False and foundflag == True):
                shutil.copy(filepath,"FileToServe")
    return foundflag

def urlSearch(hwnd):
    link = ""
    isURL = False
    windowTitleName = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if ("Google Chrome" in windowTitleName):
        app = Application(backend="uia")
        app.connect(handle=hwnd)
        element_name = "Adress- und Suchleiste"
        dlg = app.top_window()
        wrapper = dlg.child_window(title=element_name, control_type="Edit")
        link = wrapper.get_value()
        if(os.path.exists(link) == True):
            isURL = True
            return isURL
    return link

