# HTTP: read files from the web server

List the files of a Yaskawa controller with their description and read their text through its web server, without account and in any mode.

Web page: https://underautomation.com/yaskawa/documentation/http

This page shows how to list the files of a Yaskawa Motoman controller and read their content through its web server, with the HTTP client of the SDK. It covers the YRC1000 and YRC1000micro controllers, and gives read only access: jobs, data files, parameters, logs.

## What the HTTP client does

The controller has a web server on TCP port 80. The SDK reads the file lists and the files of this server, and gives you the names, the descriptions and the text of the files. It is the simplest way to read a file: no account, no remote mode, any mode of the controller.

| Need                                    | HTTP | Other protocol                                              |
| --------------------------------------- | ---- | ----------------------------------------------------------- |
| List the files of one type              | Yes  | FTP, High Speed Ethernet Server                             |
| Name and description of the data files  | Yes  | No                                                          |
| Read a text file (job, data, parameter) | Yes  | FTP, High Speed Ethernet Server                             |
| Upload or delete a file                 | No   | [FTP](ftp-transfer.md), [High Speed Ethernet Server](hses-files.md) |
| Binary files, CMOS backup               | No   | FTP, High Speed Ethernet Server                             |

## Connect

### Prerequisites

- The PC reaches the controller on TCP port 80.
- Nothing else: HTTP works in teach and in play mode, without the remote mode.

### Enable HTTP

Set `Http.Enable` to `true` in `ConnectParameters`. `Connect` checks the address but does not send a request: the first method call is the first exchange.

| Parameter                  | Default | Meaning                               |
| -------------------------- | ------- | ------------------------------------- |
| `Http.Enable`              | `false` | Open the HTTP client                  |
| `Http.Port`                | `80`    | TCP port of the web server            |
| `Http.TimeoutMilliseconds` | `5000`  | Time to wait for the answer of a request |

## List the files

`GetFileList(fileExtension)` lists the files of one type. Each `FileDescription` has the `Name` of the file and, for the data and parameter files, the `Description` given by the controller.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.common.file_extension import FileExtension

parameters = ConnectParameters("192.168.0.1")
parameters.http.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Jobs: the name only
jobs = robot.http.get_file_list(FileExtension.JOB)

# Data files: the name and the description given by the controller
for file in robot.http.get_file_list(FileExtension.DAT):
    print(f"{file.name}: {file.description}")  # VAR.DAT: VARIABLE DATA

robot.disconnect()
```

| `FileExtension` | Files                                                       |
| --------------- | ----------------------------------------------------------- |
| `JOB`           | Jobs (`.JBI`)                                               |
| `DAT`           | Data files: variables, alarm history, I/O names... (`.DAT`) |
| `CND`           | Condition files (`.CND`)                                    |
| `PRM`           | Parameter files (`.PRM`), for example `ALL.PRM`             |
| `SYS`           | System files (`.SYS`)                                       |
| `LST`           | List files (`.LST`)                                         |
| `CSV`, `LOG`, `TXT` | Other text files                                        |

On a YRC1000micro, `GetFileList(FileExtension.DAT)` returns `VAR.DAT - VARIABLE DATA`, `ALMHIST.DAT - ALARM HISTORY DATA`, `IONAME.DAT - IO NAME DATA` and more.

## Read a file

`GetFile(name)` returns the text of a file. The SDK finds the folder of the file from its extension: `TEST.JBI` is a job, `VAR.DAT` a data file.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.http.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Text of a job: the folder is deduced from the extension
job = robot.http.get_file("TEST.JBI")

# Variables, alarm history, parameters...
variables = robot.http.get_file("VAR.DAT")
alarm_history = robot.http.get_file("ALMHIST.DAT")

with open("TEST.JBI", "w", newline="") as f:
    f.write(job)

robot.disconnect()
```

The text is the same as the file downloaded with FTP or with the High Speed Ethernet Server. A large file takes time: `ALL.PRM` (1.4 MB) takes about 13 s on a YRC1000micro, the same as with FTP. Increase `TimeoutMilliseconds` for large files.

## Standalone client

`HttpClient` of the namespace `UnderAutomation.Yaskawa.Http` opens an HTTP client without `YaskawaRobot`. In a .NET project with implicit usings, `System.Net.Http.HttpClient` has the same name: write the full name, or add a `using` alias.

```python
from underautomation.yaskawa.common.file_extension import FileExtension
from underautomation.yaskawa.http.http_client import HttpClient
from underautomation.yaskawa.http.http_connect_parameters import HttpConnectParameters

# An HTTP client without YaskawaRobot
parameters = HttpConnectParameters()
parameters.port = 80                    # default
parameters.timeout_milliseconds = 5000  # default

client = HttpClient()
client.connect("192.168.0.1", parameters)

for file in client.get_file_list(FileExtension.PRM):
    print(file)

client.close()
```

## Reference

**Methods of HttpClientBase** ([reference](../api/underautomation.yaskawa.http.internal.md#httpclientbase-robothttp))

- `close() -> None`: Marks the client as disconnected.
- `get_file_list(fileExtension: FileExtension) -> typing.List[FileDescription]`: Gets the list of files of the specified type available on the robot controller.
- `get_file(fileName: str) -> str`: Gets the content of a file from the robot controller. The file type is deduced from the file name extension (e.g. "PICK_JOB.JBI" queries /FGET_REQUEST/ROBOT/JOB/PICK_JOB.JBI).

**FileDescription** ([reference](../api/underautomation.yaskawa.http.md#filedescription))

- `FileDescription()`
- `name: str (read only)`: File name including extension.
- `description: str (read only)`: Description of the file, if available.

**FileExtension** ([reference](../api/underautomation.yaskawa.common.md#fileextension))

- JOB: Job files (.JBI)
- DAT: Data files (.DAT)
- CND: Condition files (.CND)
- SYS: System files (.SYS)
- PRM: Parameter files (.PRM)
- LST: List files (.LST)
- CSV: CSV files (.CSV)
- LOG: Log files (.LOG)
- TXT: Text files (.TXT)

**HttpConnectParameters** ([reference](../api/underautomation.yaskawa.http.md#httpconnectparameters))

- `HttpConnectParameters()`: Initializes a new instance of the HTTP connection parameters.
- `port: int`: Gets or sets the HTTP port number. Default: 80.
- `timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for a response. Default: 5000ms.
- `static DEFAULT_PORT: int`: Default HTTP port (80).
- `static DEFAULT_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for HTTP requests (5000ms).

## What to read next

- [FTP](ftp.md): upload, download and delete files.
- [Transfer files and backups](how-to-transfer-files.md): which protocol to choose for each file task.
