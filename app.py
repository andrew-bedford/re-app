import subprocess
import time
from PyQt6 import QtWidgets, QtWebEngineWidgets, QtWebEngineCore, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplashScreen, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtGui import QDesktopServices, QPixmap, QIcon

import os
import sys
import requests

def isReachable(url):
    try:
        request = requests.get(url)
        if request.status_code == 200:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        return False

class OpenLinksInDesktopBrowserWebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, navType, isMainFrame):
        if (navType == QWebEnginePage.NavigationType.NavigationTypeLinkClicked):
            # Use the system's default URL handler.
            QDesktopServices.openUrl(url)
            return False
        return super().acceptNavigationRequest(url, navType, isMainFrame)

class MainWindow(QtWidgets.QMainWindow):

    def loadServer(self):
        if (isReachable("http://localhost:7000/")):
            self.timer.stop()
            self.browser.setUrl(QUrl("http://localhost:7000/")) 
            self.setCentralWidget(self.browser)
            

    def showSplashscreen(self):
        label = QLabel(self)
        label.setPixmap(self.icon)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
        self.show()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("re/window")
        self.resize(1280, 800)
        self.icon = QPixmap('icon.png')
        self.setWindowIcon(QIcon(self.icon))

        self.browser = QWebEngineView()
        self.browser.setPage(OpenLinksInDesktopBrowserWebEnginePage(self))

        self.showSplashscreen()
        
        if (not isReachable("http://localhost:7000/")):
            subprocess.Popen(["dotnet", "run", "--project", "/re/log"])

        self.timer=QTimer()
        self.timer.timeout.connect(self.loadServer)
        self.timer.start(100)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
