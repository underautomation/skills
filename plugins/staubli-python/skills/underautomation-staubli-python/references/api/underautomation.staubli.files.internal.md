# underautomation.staubli.files.internal

## FileClientBase (controller.file)

`from underautomation.staubli.files.internal.file_client_base import FileClientBase`

Upload, download, listing and management of the files of the controller. With a real controller, the files are accessed through the FTP server of the controller. With a controller emulated by Staubli Robotics Suite, there is no FTP server: give the path of its .controller file as address. The fil...

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

## FileClientInternal (controller.file)

`from underautomation.staubli.files.internal.file_client_internal import FileClientInternal`

File client of StaubliController, connected by connect()

- Inherited from [FileClientBase](underautomation.staubli.files.internal.md#fileclientbase-controllerfile): `USER_APP_FOLDER`, `disconnect`, `get_listing`, `get_file_info`, `file_exists`, `directory_exists`, `create_directory`, `delete_file`, `delete_directory`, `rename`, `upload_file_to_controller`, `upload_bytes_to_controller`, `upload_application_to_controller`, `download_file_from_controller`, `download_bytes_from_controller`, `ip`, `port`, `controller_file`, `controller_folder`, `is_simulated`, `enabled`

## FileConnectParametersBase

`from underautomation.staubli.files.internal.file_connect_parameters_base import FileConnectParametersBase`

Base class for the connection parameters of the file client

- `FileConnectParametersBase()`
- `user: str`: User of the FTP server of the controller (default: default). Not used with a controller emulated by Staubli Robotics Suite.
- `password: str`: Password of the user (default: default). Not used with a controller emulated by Staubli Robotics Suite.
- `port: int`: Port of the FTP server of the controller (default: 21)
- `timeout_ms: int`: Timeout of the FTP connection and of the transfers, in milliseconds (default: 30000)
