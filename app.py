#!/usr/bin/python3
import os
import sys
import requests
import subprocess
import configparser

from PyQt6 import QtWidgets, QtWebEngineWidgets, QtWebEngineCore, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplashScreen, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtGui import QDesktopServices, QPixmap, QIcon

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
    def loadConfig(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.iconPath = config.get('App', 'icon')
        self.path = config.get('App', 'path')
        self.title = config.get('App', 'title')
        self.url = config.get('App', 'url')

    def loadServer(self):
        if (isReachable(self.url)):
            self.timer.stop()
            self.browser.setUrl(QUrl(self.url)) 
            self.setCentralWidget(self.browser)
            

    def showSplashscreen(self):
        label = QLabel(self)
        label.setPixmap(self.icon)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
        self.show()

    # FIXME: Unsuccessful tentative to get (optional) spell checking working.
    def enableSpellCheck(self):
        profile = self.browser.page().profile()
        profile.setSpellCheckEnabled = True
        profile.setSpellCheckLanguages = ["en-US"]

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.loadConfig()
        self.setWindowTitle(self.title)
        self.resize(1280, 800)
        self.icon = QPixmap(self.iconPath)
        self.setWindowIcon(QIcon(self.icon))

        self.browser = QWebEngineView()
        self.browser.setPage(OpenLinksInDesktopBrowserWebEnginePage(self))

        # Attemps at making local storage work, it might be better to just save the data to a local file instead.
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)

        self.browser.page().quotaRequested.connect(lambda request: request.accept())

        self.showSplashscreen()
        
        if (not isReachable(self.url)):
            subprocess.Popen(["dotnet", "run", "--project", self.path])

        self.timer=QTimer()
        self.timer.timeout.connect(self.loadServer)
        self.timer.start(100)

if __name__ == '__main__':
    # The QtWebEngine dictionaries are required for spell checking.
    workingDirectory = os.path.dirname(os.path.realpath(__file__))
    os.environ["QTWEBENGINE_DICTIONARIES_PATH"] = os.path.join(
        workingDirectory, "qtwebengine_dictionaries"
    )

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
