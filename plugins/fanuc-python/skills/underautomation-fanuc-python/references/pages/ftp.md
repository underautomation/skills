# FTP overview

FTP provides access to internal controller files including variables, programs, diagnostics, safety status, and current position.

Web page: https://underautomation.com/fanuc/documentation/ftp

FTP (File Transfer Protocol) provides direct access to the Fanuc controller's internal file system. The SDK uses FTP to transfer files (programs, backups) and to read and decode diagnostic data, variables, registers, and safety status.

## Key features

- **File management**: Upload, download, delete, rename files and directories
- **Variable reading**: Read all system variables in bulk from .va files
- **Registers**: Read numeric, position, and string registers
- **Diagnostics**: Safety status, I/O state, current position, error history
- **Installed features**: Detect available options on the controller
- **Asynchronous methods**: every blocking method has an `...Async` version with a `CancellationToken`

## Quick example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Read I/O state
io_state = robot.ftp.get_io_state()

# Read all variables from all files
all_variables = robot.ftp.get_all_variables()
for file in all_variables:
    for variable in file.variables:
        print(f"{variable.name} = {variable.value}")

# Access well-known system variables
rmt_master = robot.ftp.known_variable_files.get_system_file().rmt_master

# Read safety status
safety_status = robot.ftp.get_safety_status()
print(f"Emergency Stop: {safety_status.external_e_stop}")
print(f"Teach Pendant Enabled: {safety_status.tp_enable}")

# Read current position (joints, world, user frames)
current_position = robot.ftp.get_current_position()

# Upload a TP program to the controller
robot.ftp.direct_file_handling.upload_file_to_controller("C:/Programs/MyPrg.tp", "md:/MyPrg.tp")

# Download a file from the robot
robot.ftp.direct_file_handling.download_file_from_controller("C:/Backup/Backup.va", "md:/Backup.va")

# Delete a file
robot.ftp.direct_file_handling.delete_file("md:/OldProgram.tp")
```

## Connection

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.ftp.ftp_client import FtpClient

# Via FanucRobot
robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""          # usually empty
parameters.ftp.ftp_password = ""      # usually empty
parameters.ftp.ftp_timeout_ms = 30000  # optional, default is 30 seconds
robot.connect(parameters)

# Or standalone
ftp = FtpClient()
ftp.connect("192.168.0.1", "", "")
```

The `FtpTimeoutMs` property controls the connection, read, and data transfer timeouts. The default is 30,000 ms (30 seconds). Lower it for faster failure detection on unreachable controllers, or raise it for slow networks.

### User and rights

The rights of the FTP session depend on the user and on the password settings of the controller. Without a user (`FtpUser = ""`), the controller logs in at the OPERATOR level: it can refuse some operations, for example the upload of a program, with the reply "Operation password protected". Connect with a user of a higher level (for example INSTALL), defined in the password settings of the controller. The refusal is an `FtpException`, see [File management](ftp-file-management.md).

### Standalone client

`FtpClient` connects to the FTP server only, without `FanucRobot`: `Connect(ip, user, password, port, timeoutMs)` or `ConnectAsync(...)`.

## Synchronous and asynchronous

Every blocking FTP method exists twice: a synchronous version, and an asynchronous one with the same name followed by `Async` and an optional `CancellationToken`. The file reading methods (`GetSummaryDiagnosticAsync`, `KnownVariableFiles.GetNumregFileAsync`...) are also available on the web server client, `robot.Cgtp.Http`.



The asynchronous methods are not available on .NET Framework 3.5 and 4.0, which have no `async` / `await`. The synchronous and asynchronous methods of one client can be called from several threads: they run one at a time on the FTP connection.

## Limitations

- **Read-only for most data**: Variables and diagnostics are read-only via FTP. Use Telnet, SNPX, or CGTP to write values
- **Slower than SNPX**: FTP transfers entire files rather than individual values
- **No real-time data**: Data represents a snapshot at the time of the FTP request

## Next steps

- [File management](ftp-file-management.md) : Upload, download, delete files
- [Diagnostics & variables](ftp-diagnostics.md) : Safety status, registers, variables

## API reference

**FtpClient** ([reference](../api/underautomation.fanuc.ftp.md#ftpclient))

- `FtpClient()`: Instanciate a new FTP client connection
- `connect(ip: str, user: str, password: str, port: int=21, timeoutMs: int=30000) -> None`: Connect to a robot
- Inherited from [FtpClientBase](../api/underautomation.fanuc.ftp.internal.md#ftpclientbase-robotftp): `disconnect`, `enumerate_variable_files`, `enumerate_variable_file_names`, `ip`, `language`, `connected`, `direct_file_handling`
- Inherited from [FileClientBase](../api/underautomation.fanuc.common.files.md#fileclientbase-robotftp): `get_summary_diagnostic`, `get_all_errors_list`, `get_current_position`, `get_io_state`, `get_safety_status`, `get_program_states`, `get_variables_from_file`, `get_all_variables`, `known_variable_files`

**FtpClientBase** ([reference](../api/underautomation.fanuc.ftp.internal.md#ftpclientbase-robotftp))

- `disconnect() -> None`: Disconnects from FTP server
- `enumerate_variable_files() -> typing.List[FtpListItem]`: Get a list of all variable files on controller
- `enumerate_variable_file_names() -> typing.List[str]`
- `ip: str (read only)`: Connect robot IP address or host name
- `language: Languages`: Controller language (default is English)
- `connected: bool (read only)`: Indicates that FTP connection is active
- `direct_file_handling: FtpDirectFileHandling (read only)`: Contains methods to manipulate files and folders on the controller (upload, download, delete, ...)
- Inherited from [FileClientBase](../api/underautomation.fanuc.common.files.md#fileclientbase-robotftp): `get_summary_diagnostic`, `get_all_errors_list`, `get_current_position`, `get_io_state`, `get_safety_status`, `get_program_states`, `get_variables_from_file`, `get_all_variables`, `known_variable_files`
