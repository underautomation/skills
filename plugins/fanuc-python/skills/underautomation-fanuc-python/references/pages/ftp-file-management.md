# File management

Upload, download, delete, rename files and directories on the Fanuc robot controller via FTP.

Web page: https://underautomation.com/fanuc/documentation/ftp-file-management

Upload, download, delete, and rename files and directories on the Fanuc robot controller via FTP.

## Upload files

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.ftp.ftp_exists_behavior import FtpExistsBehavior

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Upload a TP program to the controller (overwrites if it already exists)
robot.ftp.direct_file_handling.upload_file_to_controller(r"C:\Programs\MyPrg.tp", "md:/MyPrg.tp")

# Skip upload if the file already exists on the controller
robot.ftp.direct_file_handling.upload_file_to_controller(
    r"C:\Programs\MyPrg.tp", "md:/MyPrg.tp",
    exists_behavior=FtpExistsBehavior.Skip)

# Resume a partial upload (appends missing bytes)
robot.ftp.direct_file_handling.upload_file_to_controller(
    r"C:\LargeFile.tp", "md:/LargeFile.tp",
    exists_behavior=FtpExistsBehavior.Append)

# Upload from bytes
with open(r"C:\Programs\MyPrg.tp", "rb") as f:
    file_bytes = f.read()
robot.ftp.direct_file_handling.upload_file_to_controller(
    file_bytes, "md:/MyPrg.tp",
    exists_behavior=FtpExistsBehavior.Overwrite)

# Upload multiple files to a directory
robot.ftp.direct_file_handling.upload_files_to_controller(
    [r"C:\file1.tp", r"C:\file2.tp"],
    "md:/programs/")
```

## Download files

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Download to a local file
robot.ftp.direct_file_handling.download_file_from_controller(r"C:\Backup\Backup.va", "md:/Backup.va")

# Download multiple files
robot.ftp.direct_file_handling.download_files_from_controller(
    r"C:\Backup\\",
    ["md:/file1.tp", "md:/file2.va"])
```

## Delete, list, and manage directories

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Delete a file
robot.ftp.direct_file_handling.delete_file("md:/OldProgram.tp")

# Delete a directory and its contents
robot.ftp.direct_file_handling.delete_directory("md:/OldFolder")

# Check if a directory exists
exists = robot.ftp.direct_file_handling.directory_exists("md:/programs")

# Create a directory
robot.ftp.direct_file_handling.create_directory("md:/NewFolder")

# List files and directories
items = robot.ftp.direct_file_handling.get_listing("md:/")
for item in items:
    print(f"{item.name} ({item.type}) - {item.size} bytes")

# Rename or move a file
robot.ftp.direct_file_handling.rename("md:/old.tp", "md:/new.tp")
```

## Asynchronous transfers

Each method has an asynchronous version (`UploadFileToControllerAsync`, `DownloadFileFromControllerAsync`, `DownloadBytesFromControllerAsync`, `GetListingAsync`, `FileExistsAsync`, `DeleteFileAsync`...) with an optional `CancellationToken`. They are not available on .NET Framework 3.5 and 4.0.



## Errors

When the controller refuses an operation, the SDK throws an `FtpException` with the reply of the controller (`ReplyCode`, `ReplyMessage`) and, when it is known, what to do. A download that does not complete returns `false` (or `null` for `DownloadBytesFromControllerAsync`).

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from UnderAutomation.Fanuc.Ftp import FtpException

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

try:
    robot.ftp.direct_file_handling.upload_file_to_controller(r"C:\Programs\MyPrg.ls", "md:/MyPrg.ls")
except FtpException as ex:
    # The exception comes from the .NET runtime, so its members keep their original names
    if ex.ProgramInUse:
        # The program is selected on the teach pendant or it runs:
        # select another program (teach pendant, or robot.cgtp.select_program from V9.10), then upload again
        print(ex.Message)
    else:
        # Other refusal of the controller, for example "Operation password protected":
        # the FTP user does not have enough rights
        print(f"{ex.ReplyCode} {ex.ReplyMessage}")

robot.disconnect()
```

### Rights of the user

The password settings of the controller can restrict the rights of the FTP user. Without a user, the controller logs in at the OPERATOR level and can refuse the upload of a program with "Operation password protected". Connect with a user that has the needed level, for example INSTALL.

### Program in use

A program that is selected on the teach pendant, or that runs, cannot be replaced: the controller replies "Specified program is in use" and `FtpException.ProgramInUse` is true. Select another program, then upload again:

- on the teach pendant, with the SELECT key;
- remotely, with `robot.Cgtp.SelectProgram("OTHER")` (web server of the controller, firmware V9.10 and later). See [Programs](cgtp-programs.md).

The controller writes the modification date into the program when it is uploaded: a program downloaded after an upload can differ from the uploaded file on the date lines only.

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Upload a TP program to the controller
robot.ftp.direct_file_handling.upload_file_to_controller("C:/Programs/MyPrg.tp", "md:/MyPrg.tp")

# Download a file from the robot
robot.ftp.direct_file_handling.download_file_from_controller("C:/Backup/Backup.va", "md:/Backup.va")

# Delete a file
robot.ftp.direct_file_handling.delete_file("md:/OldProgram.tp")

# List files in a directory
items = robot.ftp.direct_file_handling.get_listing("md:/")
for item in items:
    print(f"{item.name} ({item.type})")

# Create a directory
robot.ftp.direct_file_handling.create_directory("md:/NewFolder")

# Rename a file
robot.ftp.direct_file_handling.rename("md:/old.tp", "md:/new.tp")

# Check file existence
exists = robot.ftp.direct_file_handling.file_exists("md:/MyPrg.tp")
```

## API reference

**FtpDirectFileHandling** ([reference](../api/underautomation.fanuc.ftp.internal.md#ftpdirectfilehandling-robotftpdirect_file_handling))

- `upload_file_to_controller(fileData_or_localPath: typing.List[int] | str, remotePath: str, createRemoteDir: bool=False, progress: typing.Callable[[float], None] | OnProgressDelegate=None, existsBehavior: FtpExistsBehavior=FtpExistsBehavior.Overwrite) -> bool`: Uploads the specified byte array as a file onto the controller. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks. It overwrites file if it already exists. Uploads the specified file directly onto the controller. High-level...
- `upload_files_to_controller(localPaths: typing.List[str], remoteDir: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[str]`: Uploads the given file paths to a single folder on the controller. All files are placed directly into the given folder regardless of their path on the local filesystem. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks.
- `download_file_from_controller(localPath_or_outBytes: typing.List[int] | str, remotePath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> bool`: Downloads the specified file and return the raw byte array. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks. Downloads the specified file onto the local file system. High-level API that takes care of various edge cases i...
- `download_files_from_controller(localDir: str, remotePaths: typing.List[str], progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[str]`: Downloads the specified files into a local single directory. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks.
- `file_exists(path: str) -> bool`: Checks if a file exists on the controller.
- `directory_exists(path: str) -> bool`: Tests if the specified directory exists on the controller. This method works by trying to change the working directory to the path specified. If it succeeds, the directory is changed back to the old working directory and true is returned. False is returned otherwise and since the CWD failed it is...
- `create_directory(path: str) -> None`: Creates a directory on the controller. If the preceding directories do not exist, then they are created.
- `delete_directory(path: str) -> None`: Deletes the specified directory and all its contents.
- `delete_file(path: str) -> None`: Deletes a file on the controller
- `get_listing(path: str) -> typing.List[FtpListItem]`: Gets a file listing from the controller. Each FtpListItem object returned contains information about the file that was able to be retrieved.
- `get_object_info(path: str) -> FtpListItem`: Returns information about a file system object. Returns null if the controller response can't be parsed or the controller returns a failure completion code. The error for a failure is logged with FtpTrace. No exception is thrown on error because that would negate the usefulness of this method for...
- `rename(path: str, dest: str) -> None`: Renames an object on the remote file system. Throws exceptions if the file does not exist, or if the destination file already exists.

**FtpListItem** ([reference](../api/underautomation.fanuc.ftp.md#ftplistitem))

- `size: int (read only)`: Gets the size of the object. Only a few files (like *.tp or *.df) have a size that can be retrieved, for most files this is 0 even if they are not empty. For directories this is always 0.
- `chmod: int (read only)`: Gets the file permissions in the CHMOD format.
- `created: datetime (read only)`: Gets the created date of the object.
- `full_name: str (read only)`: Gets the full path name to the object.
- `name: str (read only)`: Gets name to the object.
- `modified: datetime (read only)`: Gets the last write time of the object.
- `type: FtpFileSystemObjectType (read only)`: Gets the type of file system object.
