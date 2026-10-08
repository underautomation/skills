# Transfer files and backups

Back up every job of a Yaskawa controller, send a job written on the PC and download the CMOS backup, from C# or Python.

Web page: https://underautomation.com/yaskawa/documentation/how-to-transfer-files

This article shows how to transfer files between a PC and a Yaskawa Motoman controller, in C# or Python. It gives a complete program that saves every job of the controller, sends a new job and downloads the CMOS backup.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md). With the High Speed Ethernet Server, the file transfers use the UDP port 10041.
- To replace a file, `RS029` and `RS214` are `1`. For the CMOS backup, the automatic backup uses the RAM disk. See [Files and backup](hses-files.md).

## Which protocol to choose

The SDK transfers files with three protocols of the controller:

| Need                                | High Speed Ethernet Server       | FTP                                 | HTTP                     |
| ----------------------------------- | -------------------------------- | ----------------------------------- | ------------------------ |
| List the files                      | `GetFileList("*.JBI")`           | `GetFileList`, `GetListing`         | `GetFileList`, with descriptions |
| Download a text file                | `GetFile(name)`                  | `GetFile(name)`                     | `GetFile(name)`          |
| Download to a file of the PC        | No                               | `DownloadFileToLocal`, `DownloadFilesToLocal` | No             |
| Upload a job                        | `LoadFile`, overwrite with `RS029` and `RS214` | `LoadFile`, `UploadFileFromLocal`, delete the job first | No |
| Delete a file                       | `DeleteFile`                     | `DeleteFile`                        | No                       |
| CMOS backup                         | `BatchDataBackup()`              | No                                  | No                       |
| `ALL.PRM` (1.4 MB), YRC1000micro    | About 45 s                       | About 13 s                          | About 13 s               |
| Port                                | UDP 10041                        | TCP 21                              | TCP 80                   |

Use FTP for large files and for backups of many files, the High Speed Ethernet Server for the CMOS backup, and HTTP to read a file without an account. The program below uses the High Speed Ethernet Server.

## Which method to choose

| Need                                | Method                                                   |
| ----------------------------------- | -------------------------------------------------------- |
| The list of the jobs or data files  | `GetFileList("*.JBI")`                                   |
| A copy of one file                  | `GetFile(name)`                                          |
| A job written or changed on the PC  | `LoadFile(name, content)`                                |
| A complete backup of the controller | `BatchDataBackup()`, then `GetFile("/SPDRV/CMOSBK.BIN")` |
| Remove a file                       | `DeleteFile(name)`                                       |

## Example

```python
import os
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))
hses = robot.high_speed_e_server

folder = "JobsBackup"
os.makedirs(folder, exist_ok=True)

# 1. Download every job of the controller
for name in hses.get_file_list("*.JBI").files:
    file = hses.get_file(name)
    with open(os.path.join(folder, name), "w", newline="") as f:
        f.write(file.content)
    print(f"Saved {name}")

# 2. Send a job written on the PC. RS029 and RS214 must allow the overwrite
with open("NEWJOB.JBI", newline="") as f:
    hses.load_file("NEWJOB.JBI", f.read())

# 3. Save the CMOS backup of the controller
hses.batch_data_backup()
with open(os.path.join(folder, "CMOSBK.BIN"), "wb") as f:
    f.write(bytes(hses.get_file("/SPDRV/CMOSBK.BIN").content_raw))

robot.disconnect()
```

The program:

1. downloads each job to the folder `JobsBackup` of the PC;
2. sends the job `NEWJOB.JBI` of the PC to the controller;
3. makes the CMOS backup on the controller and downloads it.

## Version the jobs

The jobs are text files. Save them in a version control system (Git...) after each download: you see what changed on the controller between two backups, and you can send an older version back.

## With FTP

The same backup with [FTP](ftp-transfer.md) is shorter: `DownloadFilesToLocal` saves several files in a folder of the PC in one call. To send a job that exists on the controller, delete it first: the controller does not overwrite a job by FTP.

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

## Troubleshooting

- **`Cannot over write the target file`:** set `RS029` and `RS214` to `1`.
- **The upload of a job is refused with a syntax error:** the controller checks the job when it receives it. Open the job in MotoSim or on the pendant to find the line.
- **The CMOS download fails just after `BatchDataBackup()`:** the backup is still running. Wait a few seconds and download again.
- **A large file fails on a slow network:** increase `FileTimeoutMilliseconds`.

## What to read next

- [Files and backup](hses-files.md): the reference of the file methods.
- [FTP](ftp.md) and [HTTP](http.md): the accounts, the folders and the errors.
- [Run a job](how-to-run-program.md).
