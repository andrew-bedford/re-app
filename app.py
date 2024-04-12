from PyQt6 import QtWidgets, QtWebEngineWidgets, QtWebEngineCore, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices

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

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # l = QVBoxLayout() 
        # l.addWidget(view)
        # self.setLayout(l)

        self.browser = QWebEngineView()
        self.setWindowTitle("re/window")
        self.browser.setPage(OpenLinksInDesktopBrowserWebEnginePage(self))

        if (not isReachable("http://localhost:7000/")):
            os.system("dotnet run --project /re/log")
        sleep(1000)
        self.browser.setUrl(QUrl("http://localhost:7000/")) 
        self.setCentralWidget(self.browser)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
