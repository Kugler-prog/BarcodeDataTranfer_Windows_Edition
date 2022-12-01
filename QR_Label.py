import os

import keyboard
import segno
import win32gui
import win32process
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel, QWidget, QSystemTrayIcon, QMenu, QGridLayout, QLineEdit, QPushButton, \
  QListWidget, QSpinBox
from PyQt6.QtGui import QPixmap, QIcon, QAction
import configparser

import BrowserLinkAquisition
import ServerLogic
import WindowAquisition
from BrowserLinkAquisition import fileSearch
SystemDefaults = 100 #win32api.GetSystemMetrics(4)
DefaultSize = 35
config = configparser.ConfigParser()
browsernameList = ["Google Chrome"]

class FullApplication(QWidget):
    # Initialisierung des Markers und des Icons im Systemtray
    def __init__(self):
        super().__init__()
        self.Label = DisplayedMarker(SystemDefaults)
        self.TrayApplication = SystemTray()
        self.TrayApplication.pyqtSignalHotkeyAssignment.connect(self.remapHotkey)
        self.TrayApplication.pyqtSignalToHideQR.connect(self.hideCode)


    def remapHotkey(self, newkey,flag,minorflag,previouskey):
        self.Label.setnewKey(newkey,flag,minorflag,previouskey)

    def hideCode(self):
        if (self.Label.isVisible()):
            self.Label.hide()
        else:
            self.Label.show()

class DisplayedMarker(QLabel):
    # Methode zur Initialisierung des Labels
    def __init__(self, Systemdefaults):
        super().__init__()
        self.initLabel(Systemdefaults)

    # Methode mit welchem das Aussehen des Labels, sowie die entsprechenden Modifikatoren wie zum Beispiel
    # Fensterflaggen gesetzt werden. Hierbei wird zuerst ein QLabel mit einer Pixmap  und einem Default-Qr-Code
    # gesetzt, ebenso werden Funktionen genutzt, um den Marker als oberstes Fenster zu belassen und auch um die
    # Fensterdekorationen zu entfernen, um dementsprechend nur die Pixmap sichtbar zu lassen
    def initLabel(self, Systemdefaults):
        starter_pixmap = QPixmap("DefaultCode.png")
        self.setPixmap(starter_pixmap.scaled(Systemdefaults, Systemdefaults))
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.show()
        self.setHotkeys()
        config.read("ConfigFile.ini")
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        print("Current Size is", Systemdefaults,Systemdefaults)

        # Initialisierung des Kontexmenüs und der Aktionen, sowie der verknüpften Hotkeys
        self.menu = QMenu()
        hideVisibleMarker = QAction(f"Code Ausblenden({config['Hotkeys']['AusblendButton']})", self)
        doubleCodeSize = QAction(f"Doppelte Größe({config['Hotkeys']['doppelbutton']})", self)
        quintupleCodeSize = QAction(f"Fünffache Größe({config['Hotkeys']['fButton']})", self)
        decupleCodeSize = QAction(f"Zenhfache Größe({config['Hotkeys']['zbutton']})", self)
        reset = QAction(f"reset({config['Hotkeys']['resetbutton']})", self)
        standardSize = QAction(f"Standardgröße({config['Hotkeys']['standard']})", self)
        compactMode = QAction(f"Kompaktmodus({config['Hotkeys']['kompakt']})", self)


        hideVisibleMarker.triggered.connect(lambda: self.hide())
        doubleCodeSize.triggered.connect(lambda: self.increaseSize(2))
        quintupleCodeSize.triggered.connect(lambda: self.increaseSize(5))
        decupleCodeSize.triggered.connect(lambda: self.increaseSize(10))
        reset.triggered.connect(lambda: self.movetoDoubleZero())
        standardSize.triggered.connect(lambda: self.setStandardsize())
        compactMode.triggered.connect(lambda: self.resize(15, 15))


        self.menu.addAction(hideVisibleMarker)
        self.menu.addAction(doubleCodeSize)
        self.menu.addAction(quintupleCodeSize)
        self.menu.addAction(decupleCodeSize)
        self.menu.addAction(reset)
        self.menu.addAction(standardSize)
        self.menu.addAction(compactMode)


    def moveit(self, wind):
        # Ermitteln des Rechtecks des Fensters
        WindowRect = win32gui.GetWindowRect(wind)
        # Berechnung der entsprechenden Weite des Fensters, es wird eine Position ermittelt, die Ungefähr in der Mitte des Fensters liegt
        Titlebar_Width = int(WindowRect[2] * 0.6)
        self.move(Titlebar_Width, WindowRect[1])

    # Block, welche die Diversen Maus-Events handhabt, unter anderem Klicks auf das Label, sowie drag and drop events

    def mousePressEvent(self, ev):
        self.oldPos = ev.globalPosition().toPoint()
        if(ev.button() == Qt.MouseButton.RightButton):
            self.customContextMenuRequested.connect(self.on_context_menu)


    def on_context_menu(self,point):
        self.menu.exec(self.mapToGlobal(point))

    def mouseMoveEvent(self, ev):
        delta = QPoint(ev.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = ev.globalPosition().toPoint()

    def setHotkeys(self):
        config.read("ConfigFile.ini")
        keyboard.add_hotkey(config['Hotkeys']['EinblendKey'], lambda: self.show())
        keyboard.add_hotkey(config['Hotkeys']['AusblendButton'], lambda: self.hide())
        keyboard.add_hotkey(config['Hotkeys']['doppelbutton'], lambda: self.increaseSize(2))
        keyboard.add_hotkey(config['Hotkeys']['fButton'], lambda: self.increaseSize(5))
        keyboard.add_hotkey(config['Hotkeys']['zbutton'], lambda: self.increaseSize(10))
        keyboard.add_hotkey(config['Hotkeys']['resetbutton'], lambda: self.movetoDoubleZero())
        keyboard.add_hotkey(config['Hotkeys']['standard'], lambda: self.setStandardsize())
        keyboard.add_hotkey(config['Hotkeys']['kompakt'], lambda: self.resize(15, 15))
        #keyboard.add_hotkey("alt+q", lambda: self.show())

    def createCode(self):
        pixmap = QPixmap("CurrentCode.png")
        self.resize(SystemDefaults, SystemDefaults)
        self.setPixmap(pixmap.scaled(SystemDefaults, SystemDefaults))



# Methode, mit welcher eine alte Hotkeykombination durch eine neue ersetzt wird, mit einem PYQT-Signal werden die entsprechenden Signale bis zu diese Anzeigeebene weitergeleitet
    def setnewKey(self, newKey, keyFlag, minorflag, previouskey):
        config.read("ConfigFile.ini")
        if(previouskey !=""):
            keyboard.remove_hotkey(previouskey)
        if (newKey != ""):
            config.read("ConfigFile.ini")
            if(minorflag == "EinblendKey"):
                keyboard.add_hotkey(config[keyFlag][minorflag], lambda: self.show())
            if (minorflag == "AusblendButton"):
                keyboard.add_hotkey(config[keyFlag][minorflag], lambda: self.hide())
            if (minorflag == "doppelbutton"):
                keyboard.add_hotkey(config[keyFlag][minorflag], lambda: self.increaseSize(2))
            if (minorflag == "fButton"):
                keyboard.add_hotkey(config[keyFlag][minorflag], lambda: self.increaseSize(5))
            if (minorflag == "zbutton"):
                keyboard.add_hotkey(config[keyFlag][minorflag], lambda: self.increaseSize(10))
            if (minorflag == "resetbutton"):
                keyboard.add_hotkey(config[keyFlag][minorflag], lambda: self.movetoDoubleZero())
            if (minorflag == "standard"):
                keyboard.add_hotkey(config[keyFlag][minorflag], lambda: self.movetoDoubleZero())
            if (minorflag == "kompakt"):
                keyboard.add_hotkey(config[keyFlag][minorflag], lambda: self.resize(15, 15))
        print("Erfolgreich resettet")

    def compactMode(self):
        pixmap = QPixmap("CurrentCode.png")
        self.setPixmap(pixmap.scaled(15, 15))
        self.resize(15, 15)

    def setStandardsize(self):
        pixmap = QPixmap("CurrentCode.png")
        self.setPixmap(pixmap.scaled(SystemDefaults, SystemDefaults))
        self.resize(SystemDefaults,SystemDefaults)

    def movetoDoubleZero(self):
        self.move(0,0)

    def increaseSize(self,sizefactor):
        pixmap = QPixmap("CurrentCode.png")
        self.setPixmap(pixmap.scaled(self.height()*sizefactor, self.width()*sizefactor))
        self.resize(self.height() * sizefactor, self.width() * sizefactor)



# Methode zuständig für das weitere Vorgehen, je nach gefundenem Titel werden die nächsten Aktionen und Methoden aufgerufen, also wenn es eine Datei, ein Browser oder eine Windows Anwendung ist
    def printingMarker(self, handle):
        ServerIp = ServerLogic.get_ip()
        if (len(os.listdir("FileServed")) == 0):
            pass
        else:
            for f in os.listdir("FileServed"):
                deleteFile = os.path.join("FileServed/", f)
                os.remove(deleteFile)
        nameToCheck = win32gui.GetWindowText(handle)
        for name in browsernameList:
            if name in nameToCheck:
                linkforReturn = BrowserLinkAquisition.urlSearch(handle)
                qrcode = segno.make(linkforReturn)
                qrcode.save("CurrentCode.png", border=4)
                self.createCode()
                return
        flagOfFunction = fileSearch(handle)

        if (flagOfFunction == True):
            fileItem = os.listdir("FileServed")[0]
            fileItem = fileItem.replace("\\", "/")
            fileItem = fileItem.replace(" ", "%20")
            qrcode = segno.make(f"https://{ServerIp}:8000/{fileItem}")
            qrcode.save("CurrentCode.png", border=4)
            self.createCode()
            return
        else:
            WindowProcessor = WindowAquisition.WindowsAppHandler()
            WindowsWindow = win32gui.GetForegroundWindow()
            process = win32process.GetWindowThreadProcessId(WindowsWindow)
            WindowProcessor.ProcessProcessor(process[1], WindowsWindow)
            if (len(os.listdir("FileServed")) != 0):
                fileItem = os.listdir("FileServed")[0]
                fileItem = fileItem.replace("\\", "/")
                fileItem = fileItem.replace(" ", "%20")
                qrcode = segno.make(f"https://{ServerIp}:8000/{fileItem}")
                qrcode.save("CurrentCode.png", border=4)
                self.createCode()
                return





class SystemTray(QSystemTrayIcon):
    pyqtSignalHotkeyAssignment = pyqtSignal(str,str,str,str)
    pyqtSignalToHideQR = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initTray()
        self.show()

    def initTray(self):
        icon = QIcon("DefaultCode.png")
        tooltip = "Klicken sie hier um das ConfigMenu zu öffnen"
        self.setIcon(icon)
        self.setToolTip(tooltip)
        self.showMessage("Wir sind aktiv", "Die Anwendung ist aktiviert und läuft", msecs=1000)
        trayMenuActions = QMenu()
        showConfig = QAction("Konfigurationsfenster aufrufen", self)
        closeApplication = QAction("Anwendung beenden",self)
        hideMarkerFromTray = QAction("QR Einblenden/Ausblenden", self)
        showConfig.triggered.connect(self.openConfigMenu)
        closeApplication.triggered.connect(self.quitApplication)
        hideMarkerFromTray.triggered.connect(self.hide)
        trayMenuActions.addAction(showConfig)
        trayMenuActions.addAction(closeApplication)
        trayMenuActions.addAction(hideMarkerFromTray)
        self.setContextMenu(trayMenuActions)

    def openConfigMenu(self):
        self.window = ConfigWindow()
        self.window.show()
        self.window.SignalToSetHotkeys.connect(self.passHotkeys)

    def quitApplication(self):
        QtCore.QCoreApplication.quit()


    def hide(self):
        self.pyqtSignalToHideQR.emit()



    def passHotkeys(self, newkey,flag,minorflag,previouskey):
        self.pyqtSignalHotkeyAssignment.emit(newkey,flag,minorflag,previouskey)

#Snippet entnommen von hier: https://stackoverflow.com/questions/37564728/pyqt-how-to-remove-a-layout-from-a-layout
#Zuständig, um winen wechsel zwischen den Layouts zu erlauben
def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())




class ConfigWindow(QWidget):
    SignalToSetHotkeys = pyqtSignal(str,str,str,str)

    def __init__(self):
        super(ConfigWindow, self).__init__()
        self.setFixedSize(600, 300)
        self.layout = QGridLayout(self)
        self.vLayout = QGridLayout(self)
        self.listWidget = QListWidget(parent=self)
        self.listWidget.insertItem(0, "Standardgröße")
        self.listWidget.insertItem(1, "Passwort Einstellen")
        self.listWidget.insertItem(2, "Hotkeys konfigurieren")
        self.listWidget.clicked.connect(self.clicked)
        self.configDefault = QLabel()
        self.configDefault.setText("Wählen sie eine Option aus, um die Sachen zu konfigueirern")
        self.vLayout.addWidget(self.configDefault)
        self.layout.addWidget(self.listWidget, 0, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout.addLayout(self.vLayout, 0, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout)



    def clicked(self, qmodelindex):
        #Zuständig für das Menü zur Einstellung der Standardgröße
        if (self.listWidget.currentItem().text() == "Standardgröße"):
            deleteItemsOfLayout(self.vLayout)
            self.configDefault.setParent(None)
            self.widget = QWidget()
            self.textbox = QSpinBox(self)
            self.textbox.setMinimum(10)
            self.textbox.setMaximum(150)
            self.textbox.setValue(SystemDefaults)
            self.button = QPushButton()
            self.button.setText("Auf SystemDefault zurücksetzen")
            self.textlabel = QLabel()
            self.textlabel.setText(
                "In dieser Einstellung können sie die Standargröße des Markers\n verändern, welche Angezeigt wird, wenn sie den\n kleinen Marker in der Leiste anklicken")
            self.texxtlabel = QLabel()
            self.texxtlabel.setText("Vorschau")
            self.previewWindow = QLabel()
            self.previewWindow.setStyleSheet("QLabel {background-color: gray;}")
            self.previewMarker = QLabel(parent=self.previewWindow)
            self.previewMarker.move(125, 30)
            self.previewMarkerPixmap = QPixmap("DefaultCode.png")
            self.previewMarker.setPixmap(self.previewMarkerPixmap.scaled(SystemDefaults, SystemDefaults))
            self.button.clicked.connect(self.ResetButtonClicked)
            self.textbox.valueChanged.connect(self.valuechanged)

            self.vLayout.addWidget(self.textlabel,0,0)
            self.vLayout.addWidget(self.textbox,1,0)
            self.vLayout.addWidget(self.previewWindow, 2, 0)
            self.vLayout.addWidget(self.button,3,0)
        # Zuständig für das Menü zur Einstellung der Passwörter
        if (self.listWidget.currentItem().text() == "Passwort Einstellen"):
            deleteItemsOfLayout(self.vLayout)
            self.configDefault.setParent(None)
            self.NewPassword = QLineEdit()
            self.PasswordLabel = QLabel()
            self.PasswordLabel.setText("Neues Passwort eingeben")
            self.confirmLabel = QLabel()
            self.confirmLabel.setText("Bitte bestätigen sie das neue Passwort")
            self.resetLabel = QLabel()
            self.resetLabel.setText(
                "Sollten sie Bedarf haben, können sie das Passwort\n auch auf das Default-Passwort\nzurücksetzen lassen, das Default passwort finden sie Hierbei\nim beigefügten File")
            self.PasswordConfirmed = QLineEdit()
            self.setPassword = QPushButton()
            self.setPassword.setText("Neues Passwort setzen")
            self.ResetButton = QPushButton()
            self.ResetButton.setText("Passwort auf Standard zurücksetzen")
            self.vLayout.addWidget(self.PasswordLabel,0,0)
            self.vLayout.addWidget(self.NewPassword,2,0)
            self.vLayout.addWidget(self.confirmLabel,3,0)
            self.vLayout.addWidget(self.PasswordConfirmed,4,0)
            self.vLayout.addWidget(self.setPassword,5,0)
            self.vLayout.addWidget(self.resetLabel,6,0)
            self.vLayout.addWidget(self.ResetButton,7,0)
            self.setPassword.clicked.connect(lambda:self.setnewPassword(self.NewPassword.text(),self.PasswordConfirmed.text()))
            # Zuständig für das Menü zur Einstellung der Hotkeys
        if (self.listWidget.currentItem().text() == "Hotkeys konfigurieren"):
            config.read("ConfigFile.ini")
            deleteItemsOfLayout(self.vLayout)
            self.showButton = QPushButton()
            self.showButton.setText(f"{config['Hotkeys']['EinblendKey']}")
            self.hideButton = QPushButton()
            self.hideButton.setText(f"{config['Hotkeys']['AusblendButton']}")
            self.doubleButton = QPushButton()
            self.doubleButton.setText(f"{config['Hotkeys']['doppelbutton']}")
            self.quintupleButton = QPushButton()
            self.quintupleButton.setText(f"{config['Hotkeys']['fButton']}")
            self.decupleButton = QPushButton()
            self.decupleButton.setText(f"{config['Hotkeys']['zbutton']}")
            self.resetButton = QPushButton()
            self.resetButton.setText(f"{config['Hotkeys']['resetbutton']}")
            self.standardButton = QPushButton()
            self.standardButton.setText(f"{config['Hotkeys']['standard']}")
            self.compactButton = QPushButton()
            self.compactButton.setText(f"{config['Hotkeys']['kompakt']}")

            self.showButton.clicked.connect(lambda: self.ButtonPressed("EinblendKey"))
            self.hideButton.clicked.connect(lambda: self.ButtonPressed("AusblendButton"))
            self.doubleButton.clicked.connect(lambda: self.ButtonPressed("doppelbutton"))
            self.quintupleButton.clicked.connect(lambda: self.ButtonPressed("fButton"))
            self.decupleButton.clicked.connect(lambda: self.ButtonPressed("zButton"))
            self.resetButton.clicked.connect(lambda: self.ButtonPressed("resetbutton"))
            self.standardButton.clicked.connect(lambda: self.ButtonPressed("standard"))
            self.compactButton.clicked.connect(lambda: self.ButtonPressed("kompakt"))




            self.configureLabel = QLabel()
            self.configureLabel.setText("Klicken sie auf den Knopf, um einen neuen shortcut festzulegen")
            self.showText = QLabel()
            self.showText.setText("Einblenden")
            self.hideText = QLabel()
            self.hideText.setText("Ausblenden")
            self.doubleText = QLabel()
            self.doubleText.setText("Doppelte Größe")
            self.quintupleText = QLabel()
            self.quintupleText.setText("Fünffache Größe")
            self.decupleText = QLabel()
            self.decupleText.setText("Zehnfache Größe")
            self.resetText = QLabel()
            self.resetText.setText("Position resetten")
            self.standardText = QLabel()
            self.standardText.setText("Auf Standardgröße setzen")
            self.compactText = QLabel()
            self.compactText.setText("Auf Kompaktgröße einstellen")


            self.vLayout.addWidget(self.showText, 0, 0)
            self.vLayout.addWidget(self.hideText, 1, 0)
            self.vLayout.addWidget(self.doubleText, 2, 0)
            self.vLayout.addWidget(self.quintupleText, 3, 0)
            self.vLayout.addWidget(self.decupleText, 4, 0)
            self.vLayout.addWidget(self.resetText, 5, 0)
            self.vLayout.addWidget(self.standardText, 6, 0)
            self.vLayout.addWidget(self.compactText, 7, 0)
            self.vLayout.addWidget(self.configureLabel, 8, 0)



            self.vLayout.addWidget(self.showButton, 0, 1)
            self.vLayout.addWidget(self.hideButton, 1, 1)
            self.vLayout.addWidget(self.doubleButton, 2, 1)
            self.vLayout.addWidget(self.quintupleButton, 3, 1)
            self.vLayout.addWidget(self.decupleButton, 4, 1)
            self.vLayout.addWidget(self.resetButton, 5, 1)
            self.vLayout.addWidget(self.standardButton, 6, 1)
            self.vLayout.addWidget(self.compactButton, 7, 1)

    def setnewPassword(self,password,newpassword):
        if(password == newpassword):
            with open("httpd.password", "r+") as f:
                f.seek(0)
                f.truncate()
                f.write(f"user:{newpassword}")
                print(f.read())
        else:
            error_dialogue = QtWidgets.QErrorMessage()
            error_dialogue.showMessage("Ihre Passwörter stimmen nicht überein, bitte prüfen sie ob die Passwörter übereinstimmen")
            error_dialogue.exec()

    def valuechanged(self):
        global SystemDefaults
        self.previewMarker.resize(self.textbox.value(), self.textbox.value())
        self.previewMarker.setPixmap(self.previewMarkerPixmap.scaled(self.textbox.value(), self.textbox.value()))
        SystemDefaults = self.textbox.value()

    def ResetButtonClicked(self):
        self.textbox.setValue(DefaultSize)

    def ButtonPressed(self,key):
        flag = "Hotkeys"
        minorflag = key
        self.KeyListenerr = KeySequenceEdit(flag=flag, minorflag=minorflag)
        self.KeyListenerr.show()
        self.KeyListenerr.SignalToChange.connect(self.newKeyAssigned)

    def newKeyAssigned(self, newkey,flag,minorflag,previouskey):
        config.read("ConfigFile.ini")
        self.SignalToSetHotkeys.emit(newkey,flag,minorflag,previouskey)

        print("NEwKeyAssigned", newkey)


# Snippet zur Erfassung entnommen von https://stackoverflow.com/questions/54778293/how-to-record-a-pressed-key-combination-in-the-pyqt5-dialog-window


class KeySequenceEdit(QtWidgets.QKeySequenceEdit):
    SignalToChange = pyqtSignal(str,str,str,str)

    def __init__(self, flag, minorflag):
        super(KeySequenceEdit, self).__init__()
        self.flag = flag
        self.minorflag = minorflag

    def keyPressEvent(self, event):
        super(KeySequenceEdit, self).keyPressEvent(event)
        seq_string = self.keySequence().toString(QtGui.QKeySequence.SequenceFormat.NativeText)

        config.read("ConfigFile.ini")
        previousKey = config[self.flag][self.minorflag]
        config.set(self.flag, self.minorflag, seq_string)
        with open("ConfigFile.ini", "w") as configfile:
            config.write(configfile)
        newKey = config[self.flag][self.minorflag]
        self.SignalToChange.emit(newKey,self.flag,self.minorflag,previousKey)