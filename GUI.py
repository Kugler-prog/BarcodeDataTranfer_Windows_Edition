import win32gui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QRunnable, QThreadPool
import segno
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PIL import Image

class Worker(QObject):
    finished = pyqtSignal()

    # def run(self):
    #
    #     print("Tehheehee")
    #     self.finished.emit()


class QLabelMarker(QtWidgets.QLabel):
    """
    Custom Qt Widget to show a power bar and dial.
    Demonstrating compound and custom-drawn widget.
    """

    def __init__(self, steps=5, *args, **kwargs):
        super().__init__()
        self.initUI()

    # def runLongTask(self):
    #     self.thread = QThread()
    #     self.worker = Worker()
    #     self.worker.moveToThread(self.thread)
    #     self.thread.started.connect(self.worker.run)
    #     self.worker.finished.connect(self.thread.quit)
    #     self.worker.finished.connect(self.worker.deleteLater)
    #     self.thread.finished.connect(self.thread.deleteLater)
    #     self.thread.start()



    def initUI(self):
        #self.threadmanager = QThreadPool()
        QLabel(self)
        pixmap = QPixmap()
        pixmap.load("CurrentCode.png")
        self.setPixmap(pixmap.scaled(31,31))
        #self.setWindowFlags(Qt.FramelessWindowHint)


    #def changeImgae(self):
        #self.threadmanager.start(self.printing)


    def printing(self):
        print("Das ist das active Fenster", win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        print(win32gui.GetForegroundWindow())
        qrcode = segno.make(win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        qrcode.save("CurrentCode.png")
        pixmap = QPixmap("CurrentCode.png")
        self.setPixmap(pixmap.scaled(31,31))
        handle = win32gui.GetForegroundWindow()
        rect = win32gui.GetWindowRect(handle)
        print("die höhenposition ist", rect[1])
        print("Breite ist", )
        self.resize(rect[1])
        print("done")




