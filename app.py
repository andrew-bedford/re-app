import subprocess
import time
from PyQt6 import QtWidgets, QtWebEngineWidgets, QtWebEngineCore, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplashScreen, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices, QPixmap

import os
import sys
import requests

def isReachable(url):
    try:
        request = requests.get(url)
        if request.status_code == 200:
            print(f"{url}: is reachable")
            return True
        else:
            print(f"{url}: is Not reachable, status_code: {get.status_code}")
            return False

    #Exception
    except requests.exceptions.RequestException as e:
        print(f"{url}: is not reachable")
        return False

class OpenLinksInDesktopBrowserWebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, navType, isMainFrame):
        if (navType == QWebEnginePage.NavigationType.NavigationTypeLinkClicked):
            # Use the system's default URL handler.
            QDesktopServices.openUrl(url)
            return False

        return super().acceptNavigationRequest(url, navType, isMainFrame)

class StartServerWorker(QRunnable):
    @pyqtSlot()
    def run(self):
        print("Thread start")
        time.sleep(5)
        print("Thread complete")

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("re/window")
        self.resize(1280, 800)

        self.browser = QWebEngineView()
        self.browser.setPage(OpenLinksInDesktopBrowserWebEnginePage(self))

        label = QLabel(self)
        icon = QPixmap('icon.png')
        label.setPixmap(icon)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
        self.show()
        
        if (not isReachable("http://localhost:7000/")):
            subprocess.Popen(["dotnet", "run", "--project", "/re/log"])
        while not isReachable("http://localhost:7000/"):
            QApplication.processEvents()
            time.sleep(1)

        self.browser.setUrl(QUrl("http://localhost:7000/")) 
        self.setCentralWidget(self.browser)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # pixmap = QPixmap("/re/window/icon.png")
    # splash = QSplashScreen(pixmap)
    # splash.show()
    # app.processEvents()

    # splash.close()
    w = MainWindow()
    w.show()
    app.exec()
