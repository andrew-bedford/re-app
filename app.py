#!/usr/bin/python3
import os
import sys
import time
import requests
import subprocess
import configparser

from PyQt6 import QtWidgets, QtWebEngineWidgets, QtWebEngineCore, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplashScreen, QLabel, QSizePolicy, QStyle
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings, QWebEngineProfile
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QDesktopServices, QPixmap, QIcon, QGuiApplication

def isReachable(url):
    try:
        request = requests.get(url)
        if request.status_code == 200:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        return False

def take_screenshot():
    screen_geometry = QGuiApplication.primaryScreen().geometry()
    # TODO: Check if this will work with multiple screens, probably not.
    screenshot = QGuiApplication.primaryScreen().grabWindow(0, screen_geometry.left(), screen_geometry.top(), screen_geometry.width(), screen_geometry.height())
    screenshot.save("screenshot.png")

class OpenLinksInDesktopBrowserWebEnginePage(QWebEnginePage):
    def __init__(self, webengine_view):
        # Enable persistent local storage
        # TODO: Use a slug of the application's name instead of "persistent" to avoid conflicts
        #       with other applications. To get the location where the data is being saved:
        #       `self.browser.page().profile().persistentStoragePath()`
        persistent_profile = QWebEngineProfile("persistent", webengine_view)
        super().__init__(persistent_profile, webengine_view)

    def acceptNavigationRequest(self, url, navType, isMainFrame):
        if (navType == QWebEnginePage.NavigationType.NavigationTypeLinkClicked):
            # Use the system's default URL handler.
            QDesktopServices.openUrl(url)
            return False
        return super().acceptNavigationRequest(url, navType, isMainFrame)

class MainWindow(QtWidgets.QMainWindow):
    def loadConfig(self):
        config = configparser.ConfigParser()
        config.read('_internal/config.ini')
        self.iconPath = config.get('App', 'icon')
        self.path = config.get('App', 'path')
        self.title = config.get('App', 'title')
        self.url = config.get('App', 'url')
        self.close_confirmation = config.get('App', 'close_confirmation', fallback=None)

    def loadServer(self):
        if (isReachable(self.url)):
            self.timer.stop()
            self.browser.setUrl(QUrl(self.url))
            self.browser.loadFinished.connect(self.delayedShowBrowser)

    # We introduce a small delay to give the pages a bit more time to render
    # after loading.
    def delayedShowBrowser(self):
        self.timer=QTimer()
        self.timer.timeout.connect(self.showBrowser)
        self.timer.start(100)

    def showBrowser(self):
        self.timer.stop()
        self.splash.hide()
        self.browser.show()

    def showSplashscreen(self):
        self.splash = QLabel(self.main_widget)
        self.splash.setGeometry(self.rect())
        self.splash.setPixmap(self.icon)
        self.splash.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.show()

    # FIXME: Unsuccessful tentative to get (optional) spell checking working.
    def enableSpellCheck(self):
        profile = self.browser.page().profile()
        profile.setSpellCheckEnabled = True
        profile.setSpellCheckLanguages = ["en-US"]

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint) # For a frameless window

        self.main_widget = QWidget(self)
        self.setGeometry(0, 0, 1280, 720)
        self.setCentralWidget(self.main_widget)

        self.background_widget = QWidget(self.main_widget)
        self.background_widget.setGeometry(0, 0, self.width(), self.height())
        self.background = QLabel(self.background_widget)
        self.screenshot = QPixmap("screenshot.png")
        self.background.setPixmap(self.screenshot)
        self.background.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a blur effect to the screenshot used as background for the window
        blur = QtWidgets.QGraphicsBlurEffect()
        blur.setBlurRadius(15.0)
        self.background.setGraphicsEffect(blur)

        # Add a black semi-transparent layer over the background to darken it
        self.color_layer = QWidget(self.main_widget)
        self.color_layer.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
        self.color_layer.setGeometry(self.rect())

        self.previousWindowState = self.windowState()

        # self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed) # Prevents the window from resizing when changing the central widget
        self.loadConfig()
        self.setWindowTitle(self.title)
        self.resize(self.screen().geometry().width(), self.screen().geometry().height()) # Use screen dimensions as default window size
        self.icon = QPixmap(self.iconPath)
        self.setWindowIcon(QIcon(self.icon))

        self.browser = QWebEngineView(self.main_widget)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        self.browser.setGeometry(self.rect())
        self.browser.setPage(OpenLinksInDesktopBrowserWebEnginePage(self.browser))
        self.browser.page().setBackgroundColor(QtCore.Qt.GlobalColor.transparent)
        self.browser.page().quotaRequested.connect(lambda request: request.accept())

        self.showSplashscreen()

        if (not isReachable(self.url)):
            subprocess.Popen(["dotnet", "run", "--project", self.path])

        self.timer=QTimer()
        self.timer.timeout.connect(self.loadServer)
        self.timer.start(100)

    def resizeEvent(self, event):
        # Quick attempt to get the titlebar's height so that we can correctly offset the image. We do not actually
        # use it at the moment because my window manager hides title bars.
        titlebar_height = app.style().pixelMetric(QStyle.PixelMetric.PM_TitleBarHeight)

        self.background_widget.setGeometry(-self.x(), -self.y(), self.width()+self.x(), self.height()+self.y())
        self.color_layer.setGeometry(self.rect())
        self.browser.setGeometry(self.rect())
        super().resizeEvent(event)

    def moveEvent(self, event):
        titlebar_height = app.style().pixelMetric(QStyle.PixelMetric.PM_TitleBarHeight)
        self.background_widget.setGeometry(-self.x(), -self.y(), self.width()+self.x(), self.height()+self.y())
        super().moveEvent(event)

    def update_background(self):
        take_screenshot()
        self.screenshot = QPixmap("screenshot.png")
        self.background.setPixmap(self.screenshot)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            # HACK: Update background when un-minimizing
            if ((self.previousWindowState & QtCore.Qt.WindowState.WindowMinimized) and
                (not self.windowState() or (self.windowState() & QtCore.Qt.WindowState.WindowMaximized))):
                self.update_background()
                super().changeEvent(event)

            self.previousWindowState = self.windowState()

    def closeEvent(self, event):
        if self.close_confirmation:
            reply = QtWidgets.QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?',
                                                   QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                                                   QtWidgets.QMessageBox.StandardButton.No)
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == '__main__':
    # QtWebEngine dictionaries are required for spell checking.
    workingDirectory = os.path.dirname(os.path.realpath(__file__))
    os.environ["QTWEBENGINE_DICTIONARIES_PATH"] = os.path.join(
        workingDirectory, "_internal", "qtwebengine_dictionaries"
    )

    app = QtWidgets.QApplication(sys.argv)
    take_screenshot() # Take initial screenshot before showing the main window
    window = MainWindow()
    window.showMaximized()
    app.exec()
