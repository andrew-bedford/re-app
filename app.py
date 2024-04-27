import os
import sys
import requests
import subprocess

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
        self.icon = QPixmap(os.path.join(workingDirectory, 'icon.png'))
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
        
        if (not isReachable("http://localhost:7000/")):
            subprocess.Popen(["dotnet", "run", "--project", "/re/log"])

        self.timer=QTimer()
        self.timer.timeout.connect(self.loadServer)
        self.timer.start(100)

if __name__ == '__main__':
    workingDirectory = os.path.abspath(os.path.dirname(__file__))
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
