# re/appify
A simple python script that creates a desktop window using Qt, automatically starts your web app's server locally, displays a splashscreen with your application's logo while it's starting and then load the page in a webview once the server is reachable.

**Note**: Work in progress. It's more of a proof of concept at the moment. It is not configurable without editing the script itself.

## Development
### Running
```
pip3 install PyQt6 PyQt6-WebEngine
python app.py
```

### Publishing
To generate an installer for your application, you can use PyInstaller:
```
pip3 install PyInstaller
pyinstaller app.py
```
Note that it has to be run on the platform that you are targeting (e.g., on Windows for a Windows installer).

## FAQ
### Why?
I was developing .NET web applications that I wanted to run in desktop windows. Existing options didn't quite meet my needs:
 - [MAUI](https://github.com/dotnet/maui) is not available on Linux, my main operating system.
 - [Electron.NET](https://github.com/ElectronNET/) and [SpiderEye](https://github.com/JBildstein/SpiderEye) were a few .NET versions behind, which prevented me from using either.
 - [Photino](https://github.com/tryphotino/photino.NET) seemed promising, but I encountered issues on Windows (application would not load) and on Linux (WebKit quirks).

All I wanted was a cross-platform way to automatically start the application's server and display the page in a window. How hard could it be? This lead me to create re/appify.

