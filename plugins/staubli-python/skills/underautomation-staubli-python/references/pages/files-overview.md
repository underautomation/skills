# Files overview

Access the files of a CS8 or CS9 controller: FTP server of a real controller, or .controller file of a controller emulated by Staubli Robotics Suite. Connection, paths, /usr/usrapp and errors.

Web page: https://underautomation.com/staubli/documentation/files-overview

This page explains how the Staubli SDK accesses the files of a CS8 or CS9 controller, real or emulated by Staubli Robotics Suite: the connection, the paths and the errors. The file client `controller.File` uploads, downloads, lists and manages the files, and sends complete VAL 3 applications.

## Real or emulated controller

The same methods work on both, with the same paths. Only the address changes.

### Real controller

The file client uses the FTP server of the controller. Give its IP address, and the user and the password of the FTP server.

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.connection_parameters import ConnectionParameters

parameters = ConnectionParameters("192.168.0.254")

# The file client is disabled by default
parameters.file.enable = True

# User and password of the FTP server of the controller
parameters.file.user = "default"
parameters.file.password = "default"

controller = StaubliController()
controller.connect(parameters)

# False with a real controller: the files go through FTP
print(controller.file.is_simulated)

controller.disconnect()
```

### Emulated controller

The emulator of Staubli Robotics Suite (SRS) has no FTP server. It keeps the files of the emulated controller in the folder of its `.controller` file, with the same tree as a real controller (`usr`, `log`). Give the path of the `.controller` file as address:

- **Local path** (`C:\...\MyCell\Controller1\Controller1.controller`): the emulator runs on this PC. The SOAP client connects to `127.0.0.1`.
- **UNC path** (`\\SRS-PC\share\...\Controller1\Controller1.controller`): the emulator runs on another PC. The SOAP client connects to this PC, and the files go through the Windows share.

A path that is not a `.controller` file is refused. The SOAP port of the emulated controller is read from its configuration: see [Test with the Staubli Robotics Suite emulator](simulator.md).

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.connection_parameters import ConnectionParameters

# Controller emulated by Staubli Robotics Suite on this PC: give its .controller file.
# The SOAP client connects to 127.0.0.1, the file client uses the folder of the .controller file.
parameters = ConnectionParameters(r"C:\SRS\MyCell\Controller1\Controller1.controller")

# Emulator on another PC: give a UNC path. The SOAP client connects to this PC.
# parameters = ConnectionParameters(r"\\SRS-PC\SRS\MyCell\Controller1\Controller1.controller")

parameters.file.enable = True

controller = StaubliController()
controller.connect(parameters)

# True: the files are read and written in the folder of the .controller file
print(controller.file.is_simulated)
print(controller.file.controller_folder)

controller.disconnect()
```

`IsSimulated` tells which mode is used. With an emulated controller, `ControllerFile` gives the full path of the `.controller` file and `ControllerFolder` the folder of the files, and the user and the password are not used.

## Connection parameters

| Parameter        | Default     | Meaning                                                       |
| ---------------- | ----------- | ------------------------------------------------------------- |
| `File.Enable`    | `false`     | Connect the file client                                       |
| `File.User`      | `"default"` | User of the FTP server of the controller                      |
| `File.Password`  | `"default"` | Password of this user                                         |
| `File.Port`      | `21`        | Port of the FTP server (`FileConnectParameters.DEFAULT_PORT`) |
| `File.TimeoutMs` | `30000`     | Timeout of the FTP connection and of the transfers, in ms     |

Set `Soap.Enable` to `false` to use the file client alone. The SOAP parameters are on the page [Connect to your robot](connect.md).

## Paths on the controller

The paths are the paths of the controller, with `/` as separator: `/usr/usrapp/myApp/myApp.pjx`. A path that does not start with `/` is relative to the root of the controller. With an emulated controller, the root is the folder of the `.controller` file: a path cannot go outside of it.

| Folder              | Content                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------- |
| `/usr/usrapp`       | The VAL 3 applications, one sub-folder per application (`FileClientBase.USER_APP_FOLDER`) |
| `/usr/usrapp/myApp` | The files of the application `myApp`: `myApp.pjx`, its programs and its data              |

The project path `Disk://myApp/myApp.pjx` of the SOAP methods (`LoadProject`, `StartApplication`) is the file `/usr/usrapp/myApp/myApp.pjx`.

## Standalone file client

`FileClient` connects without `StaubliController`. Its address is an IP or the path of a `.controller` file, as above.

```python
from underautomation.staubli.files.file_client import FileClient

files = FileClient()

# Real controller: IP, FTP user and password (port 21 by default)
files.connect("192.168.0.254", "default", "default")

# Or the .controller file of a controller emulated by Staubli Robotics Suite (the user and the password are not used)
# files.connect(r"C:\SRS\MyCell\Controller1\Controller1.controller", None, None)

for item in files.get_listing("/usr/usrapp"):
    print(item.name)

files.disconnect()
```

## Errors

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.connection_parameters import ConnectionParameters
from UnderAutomation.Staubli.Files import FileException
from System.IO import DirectoryNotFoundException

parameters = ConnectionParameters("192.168.0.254")
parameters.file.enable = True
controller = StaubliController()

# The exceptions come from the .NET runtime, so their members keep their original names
try:
    controller.connect(parameters)
    content = controller.file.download_bytes_from_controller("/usr/usrapp/myApp/myApp.pjx")
except FileException as ex:
    # Connection refused, file not found, or operation refused by the controller
    print(ex.Message)

    # FTP reply of the controller, 0 and None when there is none
    print(ex.RemotePath, ex.ReplyCode, ex.ReplyMessage)
except DirectoryNotFoundException as ex:
    # The address is a folder that does not exist
    print(ex.Message)

controller.disconnect()
```

| Exception                    | When                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------- |
| `FileException`              | The FTP connection failed, the file does not exist, or the controller refused the operation |
| `ArgumentException`          | The address is a path but not a `.controller` file, or a path goes outside of its folder    |
| `FileNotFoundException`      | The `.controller` file does not exist                                                       |
| `InvalidOperationException`  | A method is called before the connection, or after `Disconnect`                             |

When the FTP connection fails, the message of `FileException` also reminds that an emulated controller needs the path of its `.controller` file. `ReplyCode` and `ReplyMessage` give the reply of the FTP server of the controller, when there is one. The errors of the local files of your PC (for example a local file that does not exist) are not converted.

## Reference

**Methods of FileClientBase** ([reference](../api/underautomation.staubli.files.internal.md#fileclientbase-controllerfile))

- `disconnect() -> None`: Disconnects the client
- `get_listing(path: str) -> typing.List[FileItem]`: Lists the files and folders of a folder of the controller
- `get_file_info(path: str) -> FileItem`: Gets information about a file or a folder of the controller
- `file_exists(path: str) -> bool`: Checks if a file exists on the controller
- `directory_exists(path: str) -> bool`: Checks if a folder exists on the controller
- `create_directory(path: str) -> None`: Creates a folder on the controller, with its parent folders when they do not exist. Nothing is done when the folder exists.
- `delete_file(path: str) -> None`: Deletes a file of the controller
- `delete_directory(path: str) -> None`: Deletes a folder of the controller and all its content
- `rename(path: str, newPath: str) -> None`: Renames or moves a file or a folder of the controller
- `upload_file_to_controller(localPath: str, remotePath: str, createRemoteDir: bool=False, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Uploads a local file to the controller. The file of the controller is replaced when it exists.
- `upload_bytes_to_controller(data: typing.List[int], remotePath: str, createRemoteDir: bool=False, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Uploads data as a file to the controller. The file of the controller is replaced when it exists.
- `upload_application_to_controller(localAppFolder: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> str`: Uploads a complete VAL 3 application to the controller. The local folder of the application, named as the application and with its project file inside (for example C:\MyApps\myApp\myApp.pjx), is copied with its sub-folders to "/usr/usrapp/myApp" (USER_APP_FOLDER). When the application already exi...
- `download_file_from_controller(localPath: str, remotePath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Downloads a file of the controller to a local file. The local file is replaced when it exists, and its folder is created when it does not exist.
- `download_bytes_from_controller(remotePath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[int]`: Downloads a file of the controller and returns its content

**FileClientBase** ([reference](../api/underautomation.staubli.files.internal.md#fileclientbase-controllerfile))

- `disconnect() -> None`: Disconnects the client
- `get_listing(path: str) -> typing.List[FileItem]`: Lists the files and folders of a folder of the controller
- `get_file_info(path: str) -> FileItem`: Gets information about a file or a folder of the controller
- `file_exists(path: str) -> bool`: Checks if a file exists on the controller
- `directory_exists(path: str) -> bool`: Checks if a folder exists on the controller
- `create_directory(path: str) -> None`: Creates a folder on the controller, with its parent folders when they do not exist. Nothing is done when the folder exists.
- `delete_file(path: str) -> None`: Deletes a file of the controller
- `delete_directory(path: str) -> None`: Deletes a folder of the controller and all its content
- `rename(path: str, newPath: str) -> None`: Renames or moves a file or a folder of the controller
- `upload_file_to_controller(localPath: str, remotePath: str, createRemoteDir: bool=False, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Uploads a local file to the controller. The file of the controller is replaced when it exists.
- `upload_bytes_to_controller(data: typing.List[int], remotePath: str, createRemoteDir: bool=False, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Uploads data as a file to the controller. The file of the controller is replaced when it exists.
- `upload_application_to_controller(localAppFolder: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> str`: Uploads a complete VAL 3 application to the controller. The local folder of the application, named as the application and with its project file inside (for example C:\MyApps\myApp\myApp.pjx), is copied with its sub-folders to "/usr/usrapp/myApp" (USER_APP_FOLDER). When the application already exi...
- `download_file_from_controller(localPath: str, remotePath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Downloads a file of the controller to a local file. The local file is replaced when it exists, and its folder is created when it does not exist.
- `download_bytes_from_controller(remotePath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[int]`: Downloads a file of the controller and returns its content
- `ip: str (read only)`: IP or host name of the controller. Null with an emulated controller.
- `port: int (read only)`: Port of the FTP server of the controller. 0 with an emulated controller.
- `controller_file: str (read only)`: Full path of the .controller file of the controller emulated by Staubli Robotics Suite. Null with a real controller.
- `controller_folder: str (read only)`: Full path of the folder of the .controller file: root of the files of the emulated controller. Null with a real controller.
- `is_simulated: bool (read only)`: True when the files are accessed in the folder of the .controller file of a controller emulated by Staubli Robotics Suite, false when they are accessed through FTP
- `enabled: bool (read only)`: True when the client is connected
- `static USER_APP_FOLDER: str`: Folder of the VAL 3 applications on the controller. Each application is in a sub-folder named as the application (for example "/usr/usrapp/myApp/myApp.pjx"). The project path "Disk://myApp/myApp.pjx" of robot.Soap.LoadProject(...) is this file.

**FileConnectParameters** ([reference](../api/underautomation.staubli.common.md#fileconnectparameters))

- `FileConnectParameters()`
- `enable: bool`: Should use this service (default: false)
- `static DEFAULT_PORT: int`: Default port of the FTP server
- `static DEFAULT_TIMEOUT_MS: int`: Default timeout of the FTP connection and of the transfers, in milliseconds
- Inherited from [FileConnectParametersBase](../api/underautomation.staubli.files.internal.md#fileconnectparametersbase): `user`, `password`, `port`, `timeout_ms`

**FileConnectParametersBase** ([reference](../api/underautomation.staubli.files.internal.md#fileconnectparametersbase))

- `FileConnectParametersBase()`
- `user: str`: User of the FTP server of the controller (default: default). Not used with a controller emulated by Staubli Robotics Suite.
- `password: str`: Password of the user (default: default). Not used with a controller emulated by Staubli Robotics Suite.
- `port: int`: Port of the FTP server of the controller (default: 21)
- `timeout_ms: int`: Timeout of the FTP connection and of the transfers, in milliseconds (default: 30000)

**FileException** ([reference](../api/underautomation.staubli.files.md#fileexception))

- `RemotePath: str (read only)`: Path of the file or folder on the controller concerned by the operation. Null when the operation has no path.
- `ReplyCode: int (read only)`: FTP reply code returned by the controller (for example 550). 0 when the controller did not reply, and with an emulated controller.
- `ReplyMessage: str (read only)`: Reply text returned by the controller. Null when the controller did not reply, and with an emulated controller.
- Inherited from System.Exception: `Message`, `InnerException`
