import os
import shutil
import win32com.client
import win32gui
from pywinauto import Application


# Methoden, welche zuständig ist, die betreffenden Dateien bzw URL's zu ermitteln

#Diese Methode ermittelt anhand einer suche im "Recen" Ordner von Windows und mithilfe eines Dispatches, ob die Geöffnete Datei in Recent auffindbar ist, wenn dies
# Zutrifft, wird der Pfad der übereinstimmenden Datei ermittelt und diese wrd in den Webordner ("FileServed") kopiert.
def fileSearch(hwnd):
    filepath = ""
    fileFound = False
    Username = os.getenv("username")
    path = os.path.join("C:\\", "Users", Username, "AppData", "Roaming", "Microsoft", "Windows", "Recent")
    windowName = win32gui.GetWindowText(hwnd)
    recentContent = (item for item in os.listdir(path) if ".lnk" in item)
    for item in recentContent:
        itemToCheck = os.path.basename(item[:-4])
        if(itemToCheck in windowName):
            fileFound = True
            combinedPath = os.path.join(path,item)
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(combinedPath)
            filepath = shortcut.Targetpath
            if (os.path.isdir(filepath) == False and fileFound == True):
                shutil.copy(filepath,"FileServed")
    return fileFound



# Mithilfe von PywinAuto wird hier bei einem Chrome Browserfenster der Inhalt der Adressleiste (die URL) ermittelt, hierfür wird die Anwendung pywinauto verwendet
# Snippet entnommen von
def urlSearch(hwnd):
    link = ""
    WindowName = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if ("Google Chrome" in WindowName):
        app = Application(backend="uia")
        app.connect(handle=hwnd)
        element_name = "Adress- und Suchleiste"
        adressBar = app.top_window()
        wrapper = adressBar.child_window(title=element_name, control_type="Edit")
        link = wrapper.get_value()
    return link

