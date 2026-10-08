# List and transfer files

List the files of a Staubli controller, upload and download files, create, rename and delete files and folders, with synchronous and asynchronous methods.

Web page: https://underautomation.com/staubli/documentation/files-transfer

This page shows how to list, upload, download, rename and delete the files of a Staubli CS8 or CS9 controller from a PC, with `controller.File`. The same code works on a real controller (FTP) and on the emulator of Staubli Robotics Suite (folder of its `.controller` file): see [Files overview](files-overview.md) for the connection.

## List the files

`GetListing(path)` returns the files and folders of a folder. `GetFileInfo(path)` returns one item, or `null` when it does not exist.

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.connection_parameters import ConnectionParameters

parameters = ConnectionParameters("192.168.0.254")
parameters.file.enable = True
controller = StaubliController()
controller.connect(parameters)

# Content of a folder of the controller
for item in controller.file.get_listing("/usr/usrapp"):
    print(item.full_name, item.type, item.size, "bytes", item.modified)

# One file or folder, None when it does not exist
project = controller.file.get_file_info("/usr/usrapp/myApp/myApp.pjx")

file_exists = controller.file.file_exists("/usr/usrapp/myApp/myApp.pjx")
folder_exists = controller.file.directory_exists("/usr/usrapp/myApp")

controller.disconnect()
```

| Property   | Meaning                                                                |
| ---------- | ---------------------------------------------------------------------- |
| `Name`     | Name, without the path                                                 |
| `FullName` | Full path on the controller, for example `/usr/usrapp/myApp/myApp.pjx` |
| `Type`     | `FileItemType.File` or `FileItemType.Directory`                        |
| `Size`     | Size in bytes, `0` for a folder                                        |
| `Modified` | Date of the last change. With the emulator, local time of the PC       |

## Upload and download

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.connection_parameters import ConnectionParameters

parameters = ConnectionParameters("192.168.0.254")
parameters.file.enable = True
controller = StaubliController()
controller.connect(parameters)

# Upload a local file. The third argument True creates the folder on the controller when it does not exist.
controller.file.upload_file_to_controller(r"C:\Data\points.dat", "/usr/usrapp/myApp/points.dat", True,
                                          lambda progress: print(f"{progress:.0f}%"))

# Upload bytes
controller.file.upload_bytes_to_controller(b"1;2;3", "/usr/usrapp/myApp/data.txt")

# Download to a local file (replaced when it exists)
controller.file.download_file_from_controller(r"C:\Backup\myApp.pjx", "/usr/usrapp/myApp/myApp.pjx")

# Download the content
content = controller.file.download_bytes_from_controller("/usr/usrapp/myApp/data.txt")
print(bytes(content).decode("ascii"))

controller.disconnect()
```

### Upload

- `UploadFileToController(localPath, remotePath)` sends a local file.
- `UploadBytesToController(data, remotePath)` and `UploadStreamToController(stream, remotePath)` send data from memory or a stream.
- The file of the controller is replaced when it exists. With `createRemoteDir` set to `true`, its folder is created when it does not exist.

### Download

- `DownloadFileFromController(localPath, remotePath)` writes a local file. The local file is replaced, and its folder is created.
- `DownloadBytesFromController(remotePath)` returns the content, `DownloadStreamFromController(stream, remotePath)` writes it to a stream.
- A file that does not exist on the controller throws a `FileException`. No local file is created.

The optional `progress` argument receives the percentage of the transfer, from 0 to 100.

## Folders, rename and delete

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.connection_parameters import ConnectionParameters

parameters = ConnectionParameters("192.168.0.254")
parameters.file.enable = True
controller = StaubliController()
controller.connect(parameters)

# Create a folder, with its parent folders
controller.file.create_directory("/usr/usrapp/myApp/backup")

# Rename or move a file or a folder
controller.file.rename("/usr/usrapp/myApp/data.txt", "/usr/usrapp/myApp/backup/data.txt")

# Delete a file
controller.file.delete_file("/usr/usrapp/myApp/backup/data.txt")

# Delete a folder and all its content
controller.file.delete_directory("/usr/usrapp/myApp/backup")

controller.disconnect()
```

- `CreateDirectory` creates the parent folders too. Nothing is done when the folder exists.
- `Rename` renames or moves a file or a folder.
- `DeleteFile` and `DeleteDirectory` throw a `FileException` when the item does not exist. `DeleteDirectory` deletes all the content.

To send a complete VAL 3 application, see [Send a VAL 3 application](files-applications.md).

## Asynchronous methods

Each method has an asynchronous version, with an optional `CancellationToken`: `GetListingAsync`, `UploadFileToControllerAsync`, `DownloadBytesFromControllerAsync`... They are not available on .NET Framework 3.5 and 4.0.



## Reference

**FileItem** ([reference](../api/underautomation.staubli.files.md#fileitem))

- `name: str (read only)`: Name of the file or folder, without its path (for example "myApp.pjx")
- `full_name: str (read only)`: Full path of the file or folder on the controller (for example "/usr/usrapp/myApp/myApp.pjx")
- `type: FileItemType (read only)`: File or folder
- `size: int (read only)`: Size of the file in bytes. 0 for a folder, and 0 when the controller does not give the size.
- `modified: datetime (read only)`: Date and time of the last modification, as given by the controller. With a controller emulated by Staubli Robotics Suite, local time of the computer.

**FileItemType** ([reference](../api/underautomation.staubli.files.md#fileitemtype))

- File: A file
- Directory: A folder
