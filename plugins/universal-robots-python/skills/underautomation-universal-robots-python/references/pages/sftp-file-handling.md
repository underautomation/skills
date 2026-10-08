# SFTP file handling

Download, upload, list, rename and delete the files of a UR controller with SFTP: programs, installations and any other file.

Web page: https://underautomation.com/universal-robots/documentation/sftp-file-handling

SFTP (SSH File Transfer Protocol) gives access to the files of a Universal Robots controller: download, upload, list, rename and delete programs, installations and any other file. This page shows how to connect and use the SFTP client of the SDK. The controller runs Linux: the same connection can also run commands, see [SSH](ssh-commands.md).

## Prerequisites

- Secure Shell is enabled on the robot. On PolyScope, open `Settings`, `Security`, `Secure Shell`.
- The Linux user and its password. The SDK uses `ur` and `easybot` by default.

| Target    | User   | Password  | Folder of the programs           |
| --------- | ------ | --------- | -------------------------------- |
| Robot     | `root` | `easybot` | `/programs`                      |
| URSim     | `ur`   | `easybot` | `/home/ur/ursim-current/programs` |

Change the default password of the robot: anyone on the network who knows it can change its files.

## Example

SFTP is disabled by default: set `Ssh.EnableSftp` in `ConnectParameters`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# SFTP is disabled by default
parameters.ssh.enable_sftp = True

# "ur" and "easybot" by default
parameters.ssh.username = "root"
parameters.ssh.password = "easybot"

robot.connect(parameters)

# Download a program from the robot
robot.sftp.download_file("/programs/my_program.urp", "C:\\temp\\my_program.urp")

# Send a program to the robot, with the number of bytes sent
robot.sftp.upload_file("C:\\temp\\my_program.urp", "/programs/my_program.urp",
                       lambda sent: print(f"{sent} bytes sent"))

# Rename, check, delete
robot.sftp.rename_file("/programs/my_program.urp", "/programs/old_program.urp")
exists = robot.sftp.exists("/programs/old_program.urp")
robot.sftp.delete_file("/programs/old_program.urp")

# List a folder
for item in robot.sftp.list_directory("/programs/"):
    print(item.name, item.is_directory, item.length, item.last_write_time_utc)

# Read and write text files
robot.sftp.write_all_text("/programs/note.txt", "Hello")
text = robot.sftp.read_all_text("/programs/note.txt")
```

The progress callbacks of `DownloadFile`, `UploadFile` and `ListDirectory` are optional. In Python, pass a function that takes the number of bytes or of entries.

## List the programs

`EnumeratePrograms` and `EnumerateInstallations` return the relative paths of the `.urp` and `.installation` files of the programs folder and of its subfolders. They look in `/programs`, or in the folder of URSim when `/programs` does not exist. The client also works without `UR`:

```python
from underautomation.universal_robots.ssh.sftp_client import SftpClient

# An SFTP client, without a UR instance
client = SftpClient()

client.connect("192.168.0.1", "root", "easybot")

# Relative paths of the .urp files of the programs folder, and of its subfolders
programs = client.enumerate_programs()
installations = client.enumerate_installations()

client.disconnect()
```

## Operations

| Task                      | Methods                                                         |
| ------------------------- | --------------------------------------------------------------- |
| Transfer a file           | `DownloadFile`, `UploadFile`, with a local path or a `Stream`   |
| Read and write a file     | `ReadAllText`, `ReadAllLines`, `ReadAllBytes`, `WriteAllText`, `WriteAllLines`, `WriteAllBytes`, `AppendAllText`, `OpenRead`, `OpenWrite` |
| Browse                    | `ListDirectory`, `Exists`, `Get`, `GetAttributes`, `ChangeDirectory`, `WorkingDirectory` |
| Change                    | `CreateDirectory`, `RenameFile`, `DeleteFile`, `DeleteDirectory`, `Delete`, `ChangePermissions` |
| Dates                     | `GetLastWriteTime`, `GetLastAccessTime`, and their UTC versions |

A program sent with SFTP is loaded with the Dashboard Server (`LoadProgram`) or the REST API. See [Transfer files and backups](how-to-transfer-files.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**SftpClient** ([reference](../api/underautomation.universal_robots.ssh.md#sftpclient))

- `SftpClient()`
- `connect(ip: str, username: str, password: str, port: int=22) -> None`: Connects to the robot
- Inherited from [SftpClientBase](../api/underautomation.universal_robots.ssh.internal.md#sftpclientbase-robotsftp): `disconnect`, `change_directory`, `change_permissions`, `create_directory`, `delete_directory`, `delete_file`, `rename_file`, `symbolic_link`, `list_directory`, `enumerate_programs`, `enumerate_installations`, `get`, `exists`, `download_file`, `upload_file`, `get_status`, `append_all_lines`, `append_all_text`, `create`, `delete`, `get_last_access_time`, `get_last_access_time_utc`, `get_last_write_time`, `get_last_write_time_utc`, `open_read`, `open_write`, `read_all_bytes`, `read_all_lines`, `read_all_text`, `read_lines`, `write_all_bytes`, `write_all_lines`, `write_all_text`, `get_attributes`, `set_attributes`, `connected`, `operation_timeout`, `buffer_size`, `working_directory`, `protocol_version`
- Inherited from [URServiceBase](../api/underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

**SftpClientBase** ([reference](../api/underautomation.universal_robots.ssh.internal.md#sftpclientbase-robotsftp))

- `disconnect() -> None`: Disconnects this client from the SFTP server.
- `change_directory(path: str) -> None`: Changes remote directory to path.
- `change_permissions(path: str, mode: int) -> None`: Changes permissions of file(s) to specified mode.
- `create_directory(path: str) -> None`: Creates remote directory specified by path.
- `delete_directory(path: str) -> None`: Deletes remote directory specified by path.
- `delete_file(path: str) -> None`: Deletes remote file specified by path.
- `rename_file(oldPath: str, newPath: str, isPosix: bool) -> None`: Renames remote file from old path to new path.
- `rename_file(oldPath: str, newPath: str) -> None`: Renames remote file from old path to new path.
- `symbolic_link(path: str, linkPath: str) -> None`: Creates a symbolic link from old path to new path.
- `list_directory(path: str, listCallback: typing.Callable[[int], None]=None) -> typing.List[SftpFile]`: Retrieves list of files in remote directory.
- `enumerate_programs() -> typing.List[str]`: Enumerates programs with .urp extension. It searches recursively programs in "/programs" if it exists, or "/home/ur/ursim-current/programs" for simulator
- `enumerate_installations() -> typing.List[str]`: Enumerates installations with .installation extension. It searches recursively installations in "/programs" if it exists, or "/home/ur/ursim-current/programs" for simulator
- `get(path: str) -> SftpFile`: Gets reference to remote file or directory.
- `exists(path: str) -> bool`: Checks whether file or directory exists;
- `download_file(path: str, localPath: str, downloadCallback: typing.Callable[[int], None]=None) -> None`: Downloads remote file specified by the path into the stream.
- `upload_file(localPath: str, path: str, uploadCallback: typing.Callable[[int], None]=None) -> None`: Uploads file into remote file.
- `get_status(path: str) -> SftpFileSytemInformation`: Gets status using statvfs@openssh.com request.
- `append_all_lines(path: str, contents: typing.List[str]) -> None`: Appends lines to a file, creating the file if it does not already exist.
- `append_all_text(path: str, contents: str) -> None`: Appends the specified string to the file, creating the file if it does not already exist.
- `create(path: str, bufferSize: int) -> SftpFileStream`: Creates or overwrites the specified file.
- `create(path: str) -> SftpFileStream`: Creates or overwrites a file in the specified path.
- `delete(path: str) -> None`: Deletes the specified file or directory.
- `get_last_access_time(path: str) -> datetime`: Returns the date and time the specified file or directory was last accessed.
- `get_last_access_time_utc(path: str) -> datetime`: Returns the date and time, in coordinated universal time (UTC), that the specified file or directory was last accessed.
- `get_last_write_time(path: str) -> datetime`: Returns the date and time the specified file or directory was last written to.
- `get_last_write_time_utc(path: str) -> datetime`: Returns the date and time, in coordinated universal time (UTC), that the specified file or directory was last written to.
- `open_read(path: str) -> SftpFileStream`: Opens an existing file for reading.
- `open_write(path: str) -> SftpFileStream`: Opens a file for writing.
- `read_all_bytes(path: str) -> typing.List[int]`: Opens a binary file, reads the contents of the file into a byte array, and closes the file.
- `read_all_lines(path: str) -> typing.List[str]`: Opens a text file, reads all lines of the file using UTF-8 encoding, and closes the file.
- `read_all_text(path: str) -> str`: Opens a text file, reads all lines of the file with the UTF-8 encoding, and closes the file.
- `read_lines(path: str) -> typing.List[str]`: Reads the lines of a file with the UTF-8 encoding.
- `write_all_bytes(path: str, bytes: typing.List[int]) -> None`: Writes the specified byte array to the specified file, and closes the file.
- `write_all_lines(path: str, contents: typing.List[str]) -> None`: Writes a collection of strings to the file using the UTF-8 encoding, and closes the file.
- `write_all_text(path: str, contents: str) -> None`: Writes the specified string to the file using the UTF-8 encoding, and closes the file.
- `get_attributes(path: str) -> SftpFileAttributes`: Gets the SftpFileAttributes of the file on the path.
- `set_attributes(path: str, fileAttributes: SftpFileAttributes) -> None`: Sets the specified SftpFileAttributes of the file on the specified path.
- `connected: bool (read only)`: Gets a value indicating if this client is connected to the robot
- `operation_timeout: typing.Any`: Gets or sets the operation timeout.
- `buffer_size: int`: Gets or sets the maximum size of the buffer in bytes.
- `working_directory: str (read only)`: Gets remote working directory.
- `protocol_version: int (read only)`: Gets sftp protocol version.
- Inherited from [URServiceBase](../api/underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

**SftpFile** ([reference](../api/underautomation.universal_robots.ssh.tools.sftp.md#sftpfile))

- `set_permissions(mode: int) -> None`: Sets file permissions.
- `delete() -> None`: Permanently deletes a file on remote machine.
- `move_to(destFileName: str) -> None`: Moves a specified file to a new location on remote machine, providing the option to specify a new file name.
- `update_status() -> None`: Updates file status on the server.
- `attributes: SftpFileAttributes (read only)`: Gets the file attributes.
- `full_name: str (read only)`: Gets the full path of the directory or file.
- `name: str (read only)`: For files, gets the name of the file. For directories, gets the name of the last directory in the hierarchy if a hierarchy exists. Otherwise, the Name property gets the name of the directory.
- `last_access_time: datetime`: Gets or sets the time the current file or directory was last accessed.
- `last_write_time: datetime`: Gets or sets the time when the current file or directory was last written to.
- `last_access_time_utc: datetime`: Gets or sets the time, in coordinated universal time (UTC), the current file or directory was last accessed.
- `last_write_time_utc: datetime`: Gets or sets the time, in coordinated universal time (UTC), when the current file or directory was last written to.
- `length: int (read only)`: Gets or sets the size, in bytes, of the current file.
- `user_id: int`: Gets or sets file user id.
- `group_id: int`: Gets or sets file group id.
- `is_socket: bool (read only)`: Gets a value indicating whether file represents a socket.
- `is_symbolic_link: bool (read only)`: Gets a value indicating whether file represents a symbolic link.
- `is_regular_file: bool (read only)`: Gets a value indicating whether file represents a regular file.
- `is_block_device: bool (read only)`: Gets a value indicating whether file represents a block device.
- `is_directory: bool (read only)`: Gets a value indicating whether file represents a directory.
- `is_character_device: bool (read only)`: Gets a value indicating whether file represents a character device.
- `is_named_pipe: bool (read only)`: Gets a value indicating whether file represents a named pipe.
- `owner_can_read: bool`: Gets or sets a value indicating whether the owner can read from this file.
- `owner_can_write: bool`: Gets or sets a value indicating whether the owner can write into this file.
- `owner_can_execute: bool`: Gets or sets a value indicating whether the owner can execute this file.
- `group_can_read: bool`: Gets or sets a value indicating whether the group members can read from this file.
- `group_can_write: bool`: Gets or sets a value indicating whether the group members can write into this file.
- `group_can_execute: bool`: Gets or sets a value indicating whether the group members can execute this file.
- `others_can_read: bool`: Gets or sets a value indicating whether the others can read from this file.
- `others_can_write: bool`: Gets or sets a value indicating whether the others can write into this file.
- `others_can_execute: bool`: Gets or sets a value indicating whether the others can execute this file.

**SftpFileAttributes** ([reference](../api/underautomation.universal_robots.ssh.tools.sftp.md#sftpfileattributes))

- `set_permissions(mode: int) -> None`: Sets the permissions.
- `get_bytes() -> typing.List[int]`: Returns a byte array representing the current SftpFileAttributes.
- `last_access_time: datetime`: Gets or sets the local time the current file or directory was last accessed.
- `last_write_time: datetime`: Gets or sets the local time when the current file or directory was last written to.
- `last_access_time_utc: datetime`: Gets or sets the UTC time the current file or directory was last accessed.
- `last_write_time_utc: datetime`: Gets or sets the UTC time when the current file or directory was last written to.
- `size: int`: Gets or sets the size, in bytes, of the current file.
- `user_id: int`: Gets or sets file user id.
- `group_id: int`: Gets or sets file group id.
- `is_socket: bool (read only)`: Gets a value indicating whether file represents a socket.
- `is_symbolic_link: bool (read only)`: Gets a value indicating whether file represents a symbolic link.
- `is_regular_file: bool (read only)`: Gets a value indicating whether file represents a regular file.
- `is_block_device: bool (read only)`: Gets a value indicating whether file represents a block device.
- `is_directory: bool (read only)`: Gets a value indicating whether file represents a directory.
- `is_character_device: bool (read only)`: Gets a value indicating whether file represents a character device.
- `is_named_pipe: bool (read only)`: Gets a value indicating whether file represents a named pipe.
- `owner_can_read: bool`: Gets a value indicating whether the owner can read from this file.
- `owner_can_write: bool`: Gets a value indicating whether the owner can write into this file.
- `owner_can_execute: bool`: Gets a value indicating whether the owner can execute this file.
- `group_can_read: bool`: Gets a value indicating whether the group members can read from this file.
- `group_can_write: bool`: Gets a value indicating whether the group members can write into this file.
- `group_can_execute: bool`: Gets a value indicating whether the group members can execute this file.
- `others_can_read: bool`: Gets a value indicating whether the others can read from this file.
- `others_can_write: bool`: Gets a value indicating whether the others can write into this file.
- `others_can_execute: bool`: Gets a value indicating whether the others can execute this file.
- `extensions: typing.Any (read only)`: Gets or sets the extensions.

## What to read next

- [Transfer files and backups](how-to-transfer-files.md): a backup of the programs and the upload of a program.
- [Program and installation files](archive-file.md): open and change a `.urp` file on the PC.
