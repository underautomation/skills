# underautomation.staubli.files

## FileClient

`from underautomation.staubli.files.file_client import FileClient`

Standalone client for the files of a Staubli controller: upload, download, listing and management. With a real controller, the files are accessed through the FTP server of the controller. With a controller emulated by Staubli Robotics Suite, they are accessed in the folder of its .controller file.

- `FileClient()`: Create a new instance of FileClient
- `connect(address: str, user: str, password: str, port: int=21, timeoutMs: int=30000) -> None`: Connect to a controller
- Inherited from [FileClientBase](underautomation.staubli.files.internal.md#fileclientbase-controllerfile): `USER_APP_FOLDER`, `disconnect`, `get_listing`, `get_file_info`, `file_exists`, `directory_exists`, `create_directory`, `delete_file`, `delete_directory`, `rename`, `upload_file_to_controller`, `upload_bytes_to_controller`, `upload_application_to_controller`, `download_file_from_controller`, `download_bytes_from_controller`, `ip`, `port`, `controller_file`, `controller_folder`, `is_simulated`, `enabled`

## FileException

`from UnderAutomation.Staubli.Files import FileException`

Exception thrown when an operation on the files of the controller fails: the controller refused it, the file does not exist, or the communication failed. The message gives the reason and, when it is known, what to do.

The SDK raises this .NET type: catch it with `except FileException as e` after the import above. Its members keep their .NET names. The class `FileException` of the module `underautomation.staubli.files.file_exception` is not a Python exception and cannot be caught.

- `RemotePath: str (read only)`: Path of the file or folder on the controller concerned by the operation. Null when the operation has no path.
- `ReplyCode: int (read only)`: FTP reply code returned by the controller (for example 550). 0 when the controller did not reply, and with an emulated controller.
- `ReplyMessage: str (read only)`: Reply text returned by the controller. Null when the controller did not reply, and with an emulated controller.
- Inherited from System.Exception: `Message`, `InnerException`

## FileItem

`from underautomation.staubli.files.file_item import FileItem`

A file or a folder of the controller

- `name: str (read only)`: Name of the file or folder, without its path (for example "myApp.pjx")
- `full_name: str (read only)`: Full path of the file or folder on the controller (for example "/usr/usrapp/myApp/myApp.pjx")
- `type: FileItemType (read only)`: File or folder
- `size: int (read only)`: Size of the file in bytes. 0 for a folder, and 0 when the controller does not give the size.
- `modified: datetime (read only)`: Date and time of the last modification, as given by the controller. With a controller emulated by Staubli Robotics Suite, local time of the computer.

## FileItemType

`from underautomation.staubli.files.file_item_type import FileItemType`

Type of an item of the controller file system

- File: A file
- Directory: A folder

## OnProgressDelegate

`from underautomation.staubli.files.on_progress_delegate import OnProgressDelegate`

Reports the progress of a file transfer
