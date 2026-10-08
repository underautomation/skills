# Files and backup

List, download, upload and delete the job and data files of a Yaskawa controller, and download its CMOS backup.

Web page: https://underautomation.com/yaskawa/documentation/hses-files

This page shows how to transfer files between a PC and a Yaskawa Motoman controller with the SDK: list, download, upload and delete jobs and data files, and download the CMOS backup. The file transfers use the UDP port 10041 of the High Speed Ethernet Server.

## List the files

`GetFileList(pattern)` lists the files whose name matches a pattern with `*`.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Job files
jobs = robot.high_speed_e_server.get_file_list("*.JBI").files

# Variable data and condition files
dat = robot.high_speed_e_server.get_file_list("*.DAT").files
cnd = robot.high_speed_e_server.get_file_list("*.CND").files

for file in jobs:
    print(file)

robot.disconnect()
```

| Pattern | Files                                 |
| ------- | ------------------------------------- |
| `*.JBI` | Jobs                                  |
| `*.DAT` | Data files, for example the variables |
| `*.CND` | Condition files                       |
| `*.PRM` | Parameter files                       |

## Download a file

`GetFile(name)` downloads a file. `Content` is the text of the file, `ContentRaw` its bytes. The optional callback gives the progress of large files.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Download a file
file = robot.high_speed_e_server.get_file("WELD01.JBI")

# Text content, and the raw bytes for a binary file
with open("WELD01.JBI", "w", newline="") as f:
    f.write(file.content)

with open("WELD01.copy.JBI", "wb") as f:
    f.write(bytes(file.content_raw))

robot.disconnect()
```

## Upload a file

`LoadFile(name, content)` sends a text file to the controller. A job sent this way appears in the job list of the controller, ready to select.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

with open("WELD01.JBI", newline="") as f:
    content = f.read()

# Send the file to the controller
robot.high_speed_e_server.load_file("WELD01.JBI", content)

robot.disconnect()
```

- To replace a file that exists on the controller, the parameters `RS029` and `RS214` must be `1`. See [Connect to your robot](connect.md#allow_the_file_overwrite).
- The controller checks the syntax of a job when it receives it. A job with an error is refused, with the reason in the message of the `InvalidDataAnswerException`.

## Delete a file

`DeleteFile(name)` deletes a file of the controller. There is no undo: download the file first if you may need it.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Delete a job file of the controller. There is no undo
robot.high_speed_e_server.delete_file("WELD01.JBI")

robot.disconnect()
```

## CMOS backup

`BatchDataBackup()` makes the controller write its CMOS backup (jobs, parameters, settings) to `/SPDRV/CMOSBK.BIN`. Then `GetFile` downloads it.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Ask the controller to write its CMOS backup to /SPDRV/CMOSBK.BIN.
# It takes several seconds
robot.high_speed_e_server.batch_data_backup()

# Download the backup as binary
backup = robot.high_speed_e_server.get_file("/SPDRV/CMOSBK.BIN")
with open("CMOSBK.BIN", "wb") as f:
    f.write(bytes(backup.content_raw))

robot.disconnect()
```

- The backup takes several seconds. While it runs, a download of the file fails with an `InvalidDataAnswerException`: wait and try again.
- The command needs the automatic backup function with the RAM disk as device. In management mode, select `SETUP` > `AUTO BACKUP SET` and set `DEVICE` to `RAMDISK`. If this menu is missing, start the controller in maintenance mode and set `AUTOBACKUP` to `USED` in `SYSTEM` > `SETUP` > `OPTION FUNCTION`.

## Timeouts

The file transfers wait `FileTimeoutMilliseconds` (4000 ms by default) for each answer of the controller. Increase it if large files fail on a slow network. See [Connect to your robot](connect.md#connection_parameters).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/underautomation.yaskawa.high_speed_e_server.internal.md#highspeedeserverclientbase-robothigh_speed_e_server))

- `delete_file(name: str) -> RobotDataHeader`: Deletes a file from the robot controller's file system. Use with caution as deleted files cannot be recovered.
- `load_file(name: str, content: str, onLoadFileProgress: typing.Callable[[LoadFileProgress], None]=None) -> typing.List[RobotDataHeader]`: Uploads (loads) a file from the PC to the robot controller. Large files are automatically split into 479-byte chunks for transmission.
- `get_file_list(pattern: str) -> RobotFileListData`: Retrieves a list of files matching a pattern from the robot controller. Supports wildcards for matching multiple files.
- `get_file(name: str, onGetFileProgress: typing.Callable[[GetFileProgress], None]=None) -> RobotFileContentData`: Downloads (saves) a file from the robot controller to the PC. Large files are received in multiple blocks and automatically reassembled. Special use case : to download CMOS.BIN, first perform a CMOS backup using BatchDataBackup, then use GetFile with the backup file path.
- `batch_data_backup(file: str="/SPDRV/CMOSBK.BIN") -> RobotDataHeader`: Performs a backup of the robot's CMOS. The CMOS.BIN file is copied locally in the robot controller to "/SPDRC/CMOSBK.BIN". The operation can take several seconds to complete. After this command, the backup file can be downloaded using GetFile("/SPDRC/CMOSBK.BIN"). To enable this command : in "MAN...

**RobotFileListData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotfilelistdata))

- `headers: typing.Any (read only)`: Gets the list of response headers from multi-block transfers. File listings may span multiple UDP packets for large directories.
- `files: typing.List[str] (read only)`: Gets the array of file names returned by the listing operation. File names include extensions (e.g., "MYJOB.JBI", "SYSTEM.SYS").

**RobotFileContentData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotfilecontentdata))

- `get_param(section: str, parameterLine: int, parameterColumn: int) -> int`: Extracts an integer parameter value from a structured file section. Useful for reading values from parameter files and job data.
- `headers: typing.Any (read only)`: Gets the list of response headers from multi-block transfers. Large files are transferred in multiple UDP packets.
- `content: str (read only)`: Gets the text content of the downloaded file.
- `content_raw: typing.List[int] (read only)`: Gets the text content of the downloaded file.
- `file_name: str (read only)`: Gets the name of the downloaded file.

**LoadFileProgress** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#loadfileprogress))

- `completed: bool (read only)`: Gets whether the file upload has completed successfully.
- `file_name: str (read only)`: Gets the name of the file being uploaded.
- `total_bytes: int (read only)`: Gets the total size of the file in bytes.
- `loaded_bytes: int (read only)`: Gets the number of bytes uploaded so far.

**GetFileProgress** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#getfileprogress))

- `completed: bool (read only)`: Gets whether the file download has completed successfully.
- `file_name: str (read only)`: Gets the name of the file being downloaded.
- `downloaded_bytes: int (read only)`: Gets the number of bytes downloaded so far.
