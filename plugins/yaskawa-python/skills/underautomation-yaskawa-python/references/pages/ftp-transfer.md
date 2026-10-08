# FTP file transfers

Download and upload the jobs and data files of a Yaskawa controller over FTP: text, bytes, local files, several files at once, progress and async methods.

Web page: https://underautomation.com/yaskawa/documentation/ftp-transfer

This page shows how to download and upload the files of a Yaskawa Motoman controller over FTP with the SDK: text, bytes, local files and several files at once, with the progress of each transfer. It covers the YRC1000 and YRC1000micro controllers. The connection and the accounts are explained in [FTP](ftp.md).

## File names and paths

Each method takes a file name or a full path on the controller:

- A name, for example `TEST.JBI`: the SDK finds the folder from the extension. `.JBI` and `.JBR` go to `/JOB`, `.DAT` to `/DAT`, `.PRM` to `/PRM`, and so on for `.CND`, `.SYS`, `.LST`, `.CSV`, `.LOG` and `.TXT`.
- A full path, for example `/JOB/TEST.JBI`.

## Download

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = "ftp"
robot = YaskawaRobot()
robot.connect(parameters)

# Text of a file: the folder is deduced from the extension
job = robot.ftp.get_file("TEST.JBI")

# Bytes of a file, with its full path
variables = bytes(robot.ftp.download_file("/DAT/VAR.DAT"))

# To a file of the PC
robot.ftp.download_file_to_local("/PRM/ALL.PRM", r"C:\Backup\ALL.PRM")

# Several files into a folder of the PC: returns the local paths
saved = robot.ftp.download_files_to_local(["/JOB/TEST.JBI", "/DAT/VAR.DAT"], r"C:\Backup")

robot.disconnect()
```

| Method                                    | Result                                                                  |
| ----------------------------------------- | ----------------------------------------------------------------------- |
| `GetFile(name)`                           | Text of the file                                                        |
| `DownloadFile(path)`                      | Bytes of the file                                                       |
| `DownloadFileToLocal(path, localPath)`    | File saved on the PC. An existing local file is replaced. Nothing is written if the download fails |
| `DownloadFilesToLocal(paths, localFolder)` | Files saved in a folder of the PC, created if needed. Returns the local paths |
| `DownloadFileToStream(path, stream)`      | Bytes written to a .NET stream (.NET only)                              |

## Upload

### Rules of the controller

- Only jobs (`.JBI`, `.JBR`), condition files (`.CND`) and general data (`.DAT`) can be uploaded.
- The account must be `ftp` or `rcmaster`. `anonymous` cannot upload.
- The controller does not overwrite a job: delete it first, see [Delete a file](ftp.md#delete_a_file). Otherwise the upload fails with the reason `JobAlreadyExists`.
- An empty file is refused: the SDK throws an `ArgumentException` before the transfer.
- The controller checks the syntax of a job when it receives it.

### Methods

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = "ftp"
robot = YaskawaRobot()
robot.connect(parameters)

# A job written on the PC: the folder is deduced from the extension
with open("NEWJOB.JBI", newline="") as f:
    job = f.read()
robot.ftp.load_file("NEWJOB.JBI", job)

# Bytes, with the full path on the controller
robot.ftp.upload_file("/JOB/OTHER.JBI", list(job.encode("ascii")))

# A file of the PC: the remote path is deduced from its name and extension
robot.ftp.upload_file_from_local(r"C:\Jobs\PICK.JBI")

# Several files of the PC: returns the remote paths
sent = robot.ftp.upload_files_from_local([r"C:\Jobs\A.JBI", r"C:\Jobs\B.JBI"])

robot.disconnect()
```

| Method                                   | Source                                                                  |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| `LoadFile(name, text)`                   | Text                                                                    |
| `UploadFile(path, bytes)`                | Bytes                                                                   |
| `UploadFileFromLocal(localPath, path)`   | File of the PC. Without `path`, the name of the local file is used      |
| `UploadFilesFromLocal(localPaths)`       | Several files of the PC, each with its own name. Stops at the first error. Returns the remote names |
| `UploadFileFromStream(path, stream)`     | A .NET stream, read from its current position (.NET only)               |

## Progress

The transfer methods take an optional callback. It receives the progress in percent, from 0 to 100, or -1 when the size is not known. For several files, the progress is the global progress.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = "ftp"
robot = YaskawaRobot()
robot.connect(parameters)

# Percentage from 0 to 100, -1 when the size is not known
backup = robot.ftp.download_file("/PRM/ALL.PRM",
    lambda progress: print(f"{progress:.0f} %"))

robot.disconnect()
```

In Python, pass a function or a lambda.

## Async methods

In .NET, every FTP method has an async version that takes a `CancellationToken`: `ConnectAsync`, `GetFileAsync`, `DownloadFilesToLocalAsync`, `UploadFileFromLocalAsync`... Use them in a user interface, so that a long transfer does not block it. They are not available on .NET Framework 3.5 and 4.0, and not in Python.



## Reference

**Methods of FtpClientBase** ([reference](../api/underautomation.yaskawa.ftp.internal.md#ftpclientbase-robotftp))

- `upload_file(remotePath: str, data: typing.List[int], progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Uploads a byte array as a file onto the controller. Only jobs (.JBI, .JBR), condition files (.CND) and general data (.DAT) can be uploaded, with the "ftp" or "rcmaster" user. An existing job is not overwritten: delete it first with delete_file().
- `upload_file_from_local(localPath: str, remotePath: str=None, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Uploads a local file onto the controller. Only jobs (.JBI, .JBR), condition files (.CND) and general data (.DAT) can be uploaded, with the "ftp" or "rcmaster" user. An existing job is not overwritten: delete it first with delete_file().
- `upload_files_from_local(localPaths: typing.List[str], progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[str]`: Uploads several local files onto the controller. Each file is uploaded with its local file name. The controller stores each file in the folder of its type (e.g. a ".JBI" file goes to the JOB folder). The upload stops at the first error.
- `download_file(remotePath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[int]`: Downloads a file from the controller and returns its content.
- `download_file_to_local(remotePath: str, localPath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Downloads a file from the controller and saves it on the local file system. Overwrites the local file if it already exists. The local file is not created if the download fails.
- `download_files_to_local(remotePaths: typing.List[str], localFolder: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[str]`: Downloads several files from the controller into a local folder. Each file is saved with its name, and existing local files are overwritten.

**OnProgressDelegate** ([reference](../api/underautomation.yaskawa.ftp.md#onprogressdelegate))


## What to read next

- [Transfer files and backups](how-to-transfer-files.md): a complete backup program, and which protocol to choose.
- [Kinematics models](kinematics-models.md): read the geometry of the robot from its `ALL.PRM` file.
