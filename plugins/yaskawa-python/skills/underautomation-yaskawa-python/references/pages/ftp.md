# FTP: connection and file management

Connect to the FTP server of a Yaskawa controller, choose the account, list the folders and files, test and delete files, and handle the FTP errors.

Web page: https://underautomation.com/yaskawa/documentation/ftp

This page explains how to connect to the FTP server of a Yaskawa Motoman controller with the SDK, which account to use, and how to list, test and delete files. It covers the YRC1000 and YRC1000micro controllers. File transfers are on the next page, [FTP file transfers](ftp-transfer.md).

## What the FTP client does

The controller has an FTP server on TCP port 21. The SDK connects to it, logs in, and gives you methods to list, download, upload and delete the files of the controller. Every FTP method has an async version in .NET (`GetListingAsync`, `DownloadFileAsync`...).

FTP is the fastest way to transfer large files: `ALL.PRM` (1.4 MB) is downloaded in about 13 s on a YRC1000micro, against about 45 s with the High Speed Ethernet Server.

## Prerequisites

- The PC reaches the controller on TCP port 21. A firewall between them must let the FTP connections through.
- The FTP server function is enabled on the controller. Depending on the controller and its settings, it can also need the command remote: see [Prepare the controller](connect.md#prepare_the_controller). On the YRC1000micro used to test this page, FTP works in teach mode, without the command remote.

## Accounts

The account gives the rights. "Download" means from the controller to the PC, "upload" from the PC to the controller.

| User name               | Password                       | Rights                                                                                       |
| ----------------------- | ------------------------------ | -------------------------------------------------------------------------------------------- |
| `anonymous` (default)   | Any                            | Download of jobs, condition files and general data. No upload, no deletion                   |
| `ftp`                   | Any                            | Download and upload of jobs, condition files and general data. Download of system data and backups |
| `rcmaster`              | Password of the management mode | Same as `ftp`, plus the download of the parameters                                          |

The rights depend on the controller and on its software version: on the YRC1000micro used to test this page, `anonymous` also downloads the parameter files. `ftp` and `anonymous` work in the standard security mode only. When the password protection option is enabled on the controller, only the user and the password defined in this option are accepted.

## Connect

### Enable FTP

Set `Ftp.Enable` to `true` in `ConnectParameters`, and choose the account. Unlike the other protocols, `Connect` opens the FTP session and logs in at once: a wrong address or a wrong password fails in `Connect`.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.ftp.enable = True

# "anonymous" (default): download only. "ftp": download and upload.
# "rcmaster" with the password of the management mode: every right.
parameters.ftp.ftp_user = "ftp"
parameters.ftp.ftp_password = None

parameters.ftp.port = 21                      # default
parameters.ftp.timeout_milliseconds = 30000   # default

robot = YaskawaRobot()
robot.connect(parameters)  # opens the FTP session and logs in

print(f"Logged as {robot.ftp.user}")

robot.disconnect()
```

| Parameter                 | Default       | Meaning                                         |
| ------------------------- | ------------- | ----------------------------------------------- |
| `Ftp.Enable`              | `false`       | Open the FTP client                             |
| `Ftp.FtpUser`             | `"anonymous"` | User name                                       |
| `Ftp.FtpPassword`         | `null`        | Password                                        |
| `Ftp.Port`                | `21`          | TCP port of the FTP server                      |
| `Ftp.TimeoutMilliseconds` | `30000`       | Time to wait for a connection, a reply or data  |

### Standalone client

`FtpClient` opens an FTP client without `YaskawaRobot`. `Connect` takes the address, the user, the password, the port and the timeout.

```python
from underautomation.yaskawa.ftp.ftp_client import FtpClient

# An FTP client without YaskawaRobot
client = FtpClient()
client.connect("192.168.0.1", "ftp")

for item in client.get_listing("/"):
    print(item.full_name)  # /JOB, /DAT, /CND, /SYS, /PRM...

client.close()
```

## List and test the files

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.common.file_extension import FileExtension

parameters = ConnectParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = "ftp"
robot = YaskawaRobot()
robot.connect(parameters)

# Folders of the controller: /JOB, /DAT, /CND, /SYS, /PRM, /LST, /CSV, /LOG, /TXT
for item in robot.ftp.get_listing("/JOB"):
    print(f"{item.name} {item.modified} {item.type.name}")

# File names by type, or by pattern
jobs = robot.ftp.get_file_list(FileExtension.JOB)
parameter_files = robot.ftp.get_file_list_by_pattern("*.PRM")

# Test a file or a folder
exists = robot.ftp.file_exists("/JOB/TEST.JBI")
folder = robot.ftp.directory_exists("/JOB")

robot.disconnect()
```

The root of the controller has one folder per type of file: `/JOB`, `/DAT`, `/CND`, `/SYS`, `/PRM`, `/LST`, `/CSV`, `/LOG`, `/TXT`.

| Method                        | Returns                                                             |
| ----------------------------- | ------------------------------------------------------------------- |
| `GetListing(path)`            | The files and folders of a folder: `Name`, `FullName`, `Modified`, `Type` |
| `GetFileList(fileExtension)`  | The names of the files of one type                                  |
| `GetFileListByPattern("*.PRM")` | The names of the files that match a pattern                       |
| `FileExists(path)`            | `true` if the file exists                                           |
| `DirectoryExists(path)`       | `true` if the folder exists                                         |

The controller does not give the size of the files in the listing. Download a file to know its size.

## Delete a file

`DeleteFile(name)` deletes a file. The folder is found from the extension. It needs the `ftp` or `rcmaster` account. There is no undo: download the file first if you may need it.

The controller does not overwrite a job by FTP. To replace a job, delete it, then send the new one:

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = "ftp"
robot = YaskawaRobot()
robot.connect(parameters)

# A job must be deleted before it is sent again: the controller does not overwrite a job by FTP
if robot.ftp.file_exists("/JOB/NEWJOB.JBI"):
    robot.ftp.delete_file("NEWJOB.JBI")

with open("NEWJOB.JBI", newline="") as f:
    robot.ftp.load_file("NEWJOB.JBI", f.read())

robot.disconnect()
```

## Errors

Each failure throws an `FtpException`, with the operation, the file and the reason.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from UnderAutomation.Yaskawa.Ftp import FtpException

parameters = ConnectParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = "ftp"
robot = YaskawaRobot()
robot.connect(parameters)

# The exceptions come from the .NET runtime: their members keep their .NET names
try:
    with open("NEWJOB.JBI", newline="") as f:
        robot.ftp.load_file("NEWJOB.JBI", f.read())
except FtpException as ex:
    # Reason: LoginIncorrect, AccessDenied, FileNotFound, JobAlreadyExists, DeleteRefused, ConnectionError
    print(f"{ex.Operation} of {ex.RemotePath} failed: {ex.Reason}")
    print(f"Controller reply {ex.ReplyCode}: {ex.ReplyMessage}")

robot.disconnect()
```

| `Reason`           | Meaning                                                                   |
| ------------------ | ------------------------------------------------------------------------- |
| `LoginIncorrect`   | The user name or the password is refused                                  |
| `AccessDenied`     | The account has no right for this operation, for example an upload with `anonymous` |
| `FileNotFound`     | The file does not exist on the controller                                 |
| `JobAlreadyExists` | The job exists: delete it first                                           |
| `DeleteRefused`    | The controller refused to delete the file                                 |
| `ConnectionError`  | The connection was lost, or no answer before the timeout                  |
| `Unknown`          | Another refusal: `ReplyCode` and `ReplyMessage` give the answer of the controller |

## Reference

**Methods of FtpClientBase** ([reference](../api/underautomation.yaskawa.ftp.internal.md#ftpclientbase-robotftp))

- `delete_file(fileName: str) -> None`: Deletes a file from the robot controller. The "anonymous" user cannot delete files.
- `file_exists(remotePath: str) -> bool`: Checks whether a file exists on the controller.
- `directory_exists(path: str) -> bool`: Checks whether a folder exists on the controller.
- `get_listing(path: str) -> typing.List[FtpListItem]`: Returns the files and folders at the specified path on the controller. The root contains one folder per file type (JOB, DAT, CND, SYS, PRM, LST, CSV, LOG, TXT).

**FtpConnectParameters** ([reference](../api/underautomation.yaskawa.ftp.md#ftpconnectparameters))

- `FtpConnectParameters()`: Initializes a new instance of the FTP connection parameters with default values.
- `ftp_user: str`: Gets or sets the FTP user name used to authenticate with the robot controller. Standard accounts: rcmaster: widest rights, requires the management mode password.ftp: standard mode only, accepts any password.anonymous: standard mode only, accepts any password, download only. If the password protec...
- `ftp_password: str`: Gets or sets the FTP password associated with ftp_user. For rcmaster: must be the controller management mode password.For ftp or anonymous: any value is accepted (including null or empty).If the password protection option is enabled: use the password defined in that option. Default: null.
- `port: int`: Gets or sets the FTP port number. Default: 21.
- `timeout_milliseconds: int`: Gets or sets the timeout in milliseconds applied to FTP read, connect, and data transfer operations. Default: 30000ms.
- `static DEFAULT_PORT: int`: Default FTP port (21).
- `static DEFAULT_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for FTP operations (30000ms).

**FtpListItem** ([reference](../api/underautomation.yaskawa.ftp.md#ftplistitem))

- `full_name: str (read only)`: Full path on the controller (e.g. "/JOB/TEST.JBI").
- `name: str (read only)`: File or folder name without its path (e.g. "TEST.JBI").
- `modified: datetime (read only)`: Date and time of the last modification, as given by the controller.
- `type: FtpFileSystemObjectType (read only)`: Indicates whether this item is a file or a folder.

**FtpException** ([reference](../api/underautomation.yaskawa.ftp.md#ftpexception))

- `Operation: FtpOperation (read only)`: Operation that failed.
- `Reason: FtpErrorReason (read only)`: Reason of the failure.
- `RemotePath: str (read only)`: Path of the file on the controller concerned by the operation. Null for connection and listing errors.
- `User: str (read only)`: FTP user name that was logged when the error occurred.
- `ReplyCode: int (read only)`: FTP reply code returned by the controller (e.g. 550). 0 if the controller did not reply.
- `ReplyMessage: str (read only)`: Raw reply text returned by the controller. Null if the controller did not reply.
- Inherited from System.Exception: `Message`, `InnerException`

**FtpErrorReason** ([reference](../api/underautomation.yaskawa.ftp.md#ftperrorreason))

- Unknown: The controller refused the operation for another reason. See reply_message.
- LoginIncorrect: The user name or the password is not accepted by the controller.
- AccessDenied: The logged user does not have the right to do this operation on this file.
- FileNotFound: The file does not exist on the controller.
- JobAlreadyExists: The job already exists on the controller. The controller does not overwrite a job by FTP.
- DeleteRefused: The controller refused to delete the file.
- ConnectionError: The connection with the controller was lost or timed out.

## What to read next

- [FTP file transfers](ftp-transfer.md): download and upload text, bytes and local files.
- [Transfer files and backups](how-to-transfer-files.md): FTP, HTTP or High Speed Ethernet Server.
