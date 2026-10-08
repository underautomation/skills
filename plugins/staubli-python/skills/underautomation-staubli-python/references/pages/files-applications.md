# Send a VAL 3 application

Send the folder of a VAL 3 application to /usr/usrapp on the controller in one call, then load and start it with the SOAP methods.

Web page: https://underautomation.com/staubli/documentation/files-applications

This page shows how to send a complete VAL 3 application from a PC to a Staubli CS8 or CS9 controller, real or emulated by Staubli Robotics Suite, then load and start it. One call copies the folder of the application with all its files and sub-folders.

## Where the applications are

The VAL 3 applications are in the folder `/usr/usrapp` of the controller (`FileClientBase.USER_APP_FOLDER`). Each application has its own sub-folder, named as the application, with its project file inside:

| On the PC                   | On the controller             | For the SOAP methods     |
| --------------------------- | ----------------------------- | ------------------------ |
| `C:\MyApps\myApp\myApp.pjx` | `/usr/usrapp/myApp/myApp.pjx` | `Disk://myApp/myApp.pjx` |
| `C:\MyApps\myApp\start.pgx` | `/usr/usrapp/myApp/start.pgx` |                          |

## Send, load and start

`UploadApplicationToController(localAppFolder)` takes the local folder of the application. The name of the folder is the name of the application.

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.connection_parameters import ConnectionParameters

parameters = ConnectionParameters("192.168.0.254")
parameters.file.enable = True
controller = StaubliController()
controller.connect(parameters)

# The application must not be in memory while its files are replaced
controller.soap.stop_and_unload_all()

# Copies C:\MyApps\myApp and its sub-folders to /usr/usrapp/myApp on the controller
remote_folder = controller.file.upload_application_to_controller(r"C:\MyApps\myApp",
                                                                 lambda progress: print(f"{progress:.0f}%"))

# /usr/usrapp/myApp/myApp.pjx is Disk://myApp/myApp.pjx for the SOAP methods
controller.soap.load_project("Disk://myApp/myApp.pjx")
controller.soap.start_application("Disk://myApp/myApp.pjx")

controller.disconnect()
```

### What the method does

1. When `/usr/usrapp/myApp` exists on the controller, it deletes it with all its content. The files that are not in the local folder do not stay on the controller.
2. It creates the folder of the application and all its sub-folders, also the empty ones.
3. It uploads every file. `progress` receives the percentage of all the files, from 0 to 100.
4. It returns the folder of the application on the controller, for example `/usr/usrapp/myApp`.

`UploadApplicationToControllerAsync` does the same, with a `CancellationToken`.

### Before and after

- An application in memory can be refused by the controller while its files are replaced. Call `StopAndUnloadAll()` first.
- After the upload, load the project with `LoadProject("Disk://myApp/myApp.pjx")`, then start it with `StartApplication`. See [VAL 3 applications](soap-applications.md).
- A running application can move the arm: check the state of the cell before you start it from a PC.

## Errors

- **`DirectoryNotFoundException`:** the local folder does not exist.
- **`FileException`:** the controller refused a file or a folder, for example because the application is still loaded, or the user has no right to write. The message gives the path and the reply of the controller.

See [Files overview](files-overview.md) for the connection and the other errors.
