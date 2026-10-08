# underautomation.universal_robots.ssh.internal

## SftpClientBase (robot.sftp)

`from underautomation.universal_robots.ssh.internal.sftp_client_base import SftpClientBase`

Implementation of the SSH File Transfer Protocol (SFTP) over SSH for transfering files to the robot controller

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
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## SshClientBase (robot.ssh)

`from underautomation.universal_robots.ssh.internal.ssh_client_base import SshClientBase`

Provides a client connection to SSH server

- `disconnect() -> None`: Disconnects this client from the SSH server
- `create_command(commandText: str) -> SshCommand`: Creates the command to be executed.
- `run_command(commandText: str) -> SshCommand`: Creates and executes the command.
- `create_shell_stream(terminalName: str, columns: int, rows: int, width: int, height: int, bufferSize: int) -> ShellStream`: Creates the shell stream.
- `connected: bool (read only)`: Gets a value indicating if this client is connected to the robot
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## SshParametersBase

`from underautomation.universal_robots.ssh.internal.ssh_parameters_base import SshParametersBase`

Base class for SSH and SFTP connection parameters, including credentials and port configuration.

- `username: str`: Setup Linux Username for SSH connection Default value is "ur" for simulator and "root" for real robot
- `password: str`: Setup Linux Password for SSH connection Default value is "easybot"
- `port: int`: SSH and SFTP TCP port. Default : 22
- `static DEFAULT_PORT: int`: Default SSH server TCP port
