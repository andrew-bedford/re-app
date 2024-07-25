# re/appify
A simple python script that creates a desktop window using Qt, automatically starts your web app's server locally, displays a splashscreen with your application's logo while it's starting and then load the page in a webview once the server is reachable.

**Note**: Work in progress. It's more of a proof of concept at the moment.

## Development
### Running
```
pip3 install PyQt6 PyQt6-WebEngine
python app.py
```

### Configuration
To configure your re/app, edit the `config.ini` file that is located in the root. It allows you to specify:
 - `icon`: Path to the image that is to be used as the taskbar's icon and as the splashscreen.
 - `title`: The window title to display. At the moment, this window title is static, so it cannot be changed at runtime once the application starts.
 - `path`: The path to your project on which `dotnet run` will be executed. We may want to update this later to support more than just .NET applications.
 - `url`: The url of your web application (e.g., https://localhost:12345). Once the server has started, it will load and display the screen. While the local server is starting, the splashscreen will be displayed.

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

