# underautomation.universal_robots.ssh.tools.sftp

## SftpFile

`from underautomation.universal_robots.ssh.tools.sftp.sftp_file import SftpFile`

Represents SFTP file information

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

## SftpFileAttributes

`from underautomation.universal_robots.ssh.tools.sftp.sftp_file_attributes import SftpFileAttributes`

Contains SFTP file attributes.

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

## SftpFileStream

`from underautomation.universal_robots.ssh.tools.sftp.sftp_file_stream import SftpFileStream`

Exposes a Stream around a remote SFTP file, supporting both synchronous and asynchronous read and write operations.

- `flush() -> None`: Clears all buffers for this stream and causes any buffered data to be written to the file.
- `read(buffer: typing.List[int], offset: int, count: int) -> int`: Reads a sequence of bytes from the current stream and advances the position within the stream by the number of bytes read.
- `read_byte() -> int`: Reads a byte from the stream and advances the position within the stream by one byte, or returns -1 if at the end of the stream.
- `set_length(value: int) -> None`: Sets the length of the current stream.
- `write(buffer: typing.List[int], offset: int, count: int) -> None`: Writes a sequence of bytes to the current stream and advances the current position within this stream by the number of bytes written.
- `write_byte(value: int) -> None`: Writes a byte to the current position in the stream and advances the position within the stream by one byte.
- `can_read: bool (read only)`: Gets a value indicating whether the current stream supports reading.
- `can_seek: bool (read only)`: Gets a value indicating whether the current stream supports seeking.
- `can_write: bool (read only)`: Gets a value indicating whether the current stream supports writing.
- `can_timeout: bool (read only)`: Indicates whether timeout properties are usable for SftpFileStream.
- `length: int (read only)`: Gets the length in bytes of the stream.
- `position: int`: Gets or sets the position within the current stream.
- `name: str (read only)`: Gets the name of the path that was used to construct the current SftpFileStream.
- `handle: typing.List[int] (read only)`: Gets the operating system file handle for the file that the current SftpFileStream encapsulates.
- `timeout: typing.Any`: Gets or sets the operation timeout.

## SftpFileSytemInformation

`from underautomation.universal_robots.ssh.tools.sftp.sftp_file_sytem_information import SftpFileSytemInformation`

Contains File system information exposed by statvfs@openssh.com request.

- `file_system_block_size: int (read only)`: Gets the file system block size.
- `block_size: int (read only)`: Gets the fundamental file system size of the block.
- `total_blocks: int (read only)`: Gets the total blocks.
- `free_blocks: int (read only)`: Gets the free blocks.
- `available_blocks: int (read only)`: Gets the available blocks.
- `total_nodes: int (read only)`: Gets the total nodes.
- `free_nodes: int (read only)`: Gets the free nodes.
- `available_nodes: int (read only)`: Gets the available nodes.
- `sid: int (read only)`: Gets the sid.
- `is_read_only: bool (read only)`: Gets a value indicating whether this instance is read only.
- `supports_set_uid: bool (read only)`: Gets a value indicating whether [supports set uid].
- `max_name_lenght: int (read only)`: Gets the max name lenght.
