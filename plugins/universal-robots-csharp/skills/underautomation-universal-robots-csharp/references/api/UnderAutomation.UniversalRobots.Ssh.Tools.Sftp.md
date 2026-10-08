# UnderAutomation.UniversalRobots.Ssh.Tools.Sftp

## SftpFile

`class SftpFile`

Represents SFTP file information

- `SftpFileAttributes Attributes { get; }`: Gets the file attributes.
- `void Delete()`: Permanently deletes a file on remote machine.
- `string FullName { get; }`: Gets the full path of the directory or file.
- `bool GroupCanExecute { get; set; }`: Gets or sets a value indicating whether the group members can execute this file.
- `bool GroupCanRead { get; set; }`: Gets or sets a value indicating whether the group members can read from this file.
- `bool GroupCanWrite { get; set; }`: Gets or sets a value indicating whether the group members can write into this file.
- `int GroupId { get; set; }`: Gets or sets file group id.
- `bool IsBlockDevice { get; }`: Gets a value indicating whether file represents a block device.
- `bool IsCharacterDevice { get; }`: Gets a value indicating whether file represents a character device.
- `bool IsDirectory { get; }`: Gets a value indicating whether file represents a directory.
- `bool IsNamedPipe { get; }`: Gets a value indicating whether file represents a named pipe.
- `bool IsRegularFile { get; }`: Gets a value indicating whether file represents a regular file.
- `bool IsSocket { get; }`: Gets a value indicating whether file represents a socket.
- `bool IsSymbolicLink { get; }`: Gets a value indicating whether file represents a symbolic link.
- `DateTime LastAccessTime { get; set; }`: Gets or sets the time the current file or directory was last accessed.
- `DateTime LastAccessTimeUtc { get; set; }`: Gets or sets the time, in coordinated universal time (UTC), the current file or directory was last accessed.
- `DateTime LastWriteTime { get; set; }`: Gets or sets the time when the current file or directory was last written to.
- `DateTime LastWriteTimeUtc { get; set; }`: Gets or sets the time, in coordinated universal time (UTC), when the current file or directory was last written to.
- `long Length { get; }`: Gets or sets the size, in bytes, of the current file.
- `void MoveTo(string destFileName)`: Moves a specified file to a new location on remote machine, providing the option to specify a new file name.
- `string Name { get; }`: For files, gets the name of the file. For directories, gets the name of the last directory in the hierarchy if a hierarchy exists. Otherwise, the Name property gets the name of the directory.
- `bool OthersCanExecute { get; set; }`: Gets or sets a value indicating whether the others can execute this file.
- `bool OthersCanRead { get; set; }`: Gets or sets a value indicating whether the others can read from this file.
- `bool OthersCanWrite { get; set; }`: Gets or sets a value indicating whether the others can write into this file.
- `bool OwnerCanExecute { get; set; }`: Gets or sets a value indicating whether the owner can execute this file.
- `bool OwnerCanRead { get; set; }`: Gets or sets a value indicating whether the owner can read from this file.
- `bool OwnerCanWrite { get; set; }`: Gets or sets a value indicating whether the owner can write into this file.
- `void SetPermissions(short mode)`: Sets file permissions.
- `void UpdateStatus()`: Updates file status on the server.
- `int UserId { get; set; }`: Gets or sets file user id.

## SftpFileAttributes

`class SftpFileAttributes`

Contains SFTP file attributes.

- `IDictionary<string, string> Extensions { get; }`: Gets or sets the extensions.
- `byte[] GetBytes()`: Returns a byte array representing the current Sftp.SftpFileAttributes.
- `bool GroupCanExecute { get; set; }`: Gets a value indicating whether the group members can execute this file.
- `bool GroupCanRead { get; set; }`: Gets a value indicating whether the group members can read from this file.
- `bool GroupCanWrite { get; set; }`: Gets a value indicating whether the group members can write into this file.
- `int GroupId { get; set; }`: Gets or sets file group id.
- `bool IsBlockDevice { get; }`: Gets a value indicating whether file represents a block device.
- `bool IsCharacterDevice { get; }`: Gets a value indicating whether file represents a character device.
- `bool IsDirectory { get; }`: Gets a value indicating whether file represents a directory.
- `bool IsNamedPipe { get; }`: Gets a value indicating whether file represents a named pipe.
- `bool IsRegularFile { get; }`: Gets a value indicating whether file represents a regular file.
- `bool IsSocket { get; }`: Gets a value indicating whether file represents a socket.
- `bool IsSymbolicLink { get; }`: Gets a value indicating whether file represents a symbolic link.
- `DateTime LastAccessTime { get; set; }`: Gets or sets the local time the current file or directory was last accessed.
- `DateTime LastAccessTimeUtc { get; set; }`: Gets or sets the UTC time the current file or directory was last accessed.
- `DateTime LastWriteTime { get; set; }`: Gets or sets the local time when the current file or directory was last written to.
- `DateTime LastWriteTimeUtc { get; set; }`: Gets or sets the UTC time when the current file or directory was last written to.
- `bool OthersCanExecute { get; set; }`: Gets a value indicating whether the others can execute this file.
- `bool OthersCanRead { get; set; }`: Gets a value indicating whether the others can read from this file.
- `bool OthersCanWrite { get; set; }`: Gets a value indicating whether the others can write into this file.
- `bool OwnerCanExecute { get; set; }`: Gets a value indicating whether the owner can execute this file.
- `bool OwnerCanRead { get; set; }`: Gets a value indicating whether the owner can read from this file.
- `bool OwnerCanWrite { get; set; }`: Gets a value indicating whether the owner can write into this file.
- `void SetPermissions(short mode)`: Sets the permissions.
- `long Size { get; set; }`: Gets or sets the size, in bytes, of the current file.
- `int UserId { get; set; }`: Gets or sets file user id.

## SftpFileStream

`class SftpFileStream : Stream, IDisposable, IAsyncDisposable`

Exposes a IO.Stream around a remote SFTP file, supporting both synchronous and asynchronous read and write operations.

- `bool CanRead { get; }`: Gets a value indicating whether the current stream supports reading.
- `bool CanSeek { get; }`: Gets a value indicating whether the current stream supports seeking.
- `bool CanTimeout { get; }`: Indicates whether timeout properties are usable for Sftp.SftpFileStream.
- `bool CanWrite { get; }`: Gets a value indicating whether the current stream supports writing.
- `void Flush()`: Clears all buffers for this stream and causes any buffered data to be written to the file.
- `byte[] Handle { get; }`: Gets the operating system file handle for the file that the current Sftp.SftpFileStream encapsulates.
- `long Length { get; }`: Gets the length in bytes of the stream.
- `string Name { get; }`: Gets the name of the path that was used to construct the current Sftp.SftpFileStream.
- `long Position { get; set; }`: Gets or sets the position within the current stream.
- `int Read(byte[] buffer, int offset, int count)`: Reads a sequence of bytes from the current stream and advances the position within the stream by the number of bytes read.
- `int ReadByte()`: Reads a byte from the stream and advances the position within the stream by one byte, or returns -1 if at the end of the stream.
- `long Seek(long offset, SeekOrigin origin)`: Sets the position within the current stream.
- `void SetLength(long value)`: Sets the length of the current stream.
- `TimeSpan Timeout { get; set; }`: Gets or sets the operation timeout.
- `void Write(byte[] buffer, int offset, int count)`: Writes a sequence of bytes to the current stream and advances the current position within this stream by the number of bytes written.
- `void WriteByte(byte value)`: Writes a byte to the current position in the stream and advances the position within the stream by one byte.

## SftpFileSytemInformation

`class SftpFileSytemInformation`

Contains File system information exposed by statvfs@openssh.com request.

- `ulong AvailableBlocks { get; }`: Gets the available blocks.
- `ulong AvailableNodes { get; }`: Gets the available nodes.
- `ulong BlockSize { get; }`: Gets the fundamental file system size of the block.
- `ulong FileSystemBlockSize { get; }`: Gets the file system block size.
- `ulong FreeBlocks { get; }`: Gets the free blocks.
- `ulong FreeNodes { get; }`: Gets the free nodes.
- `bool IsReadOnly { get; }`: Gets a value indicating whether this instance is read only.
- `ulong MaxNameLenght { get; }`: Gets the max name lenght.
- `ulong Sid { get; }`: Gets the sid.
- `bool SupportsSetUid { get; }`: Gets a value indicating whether [supports set uid].
- `ulong TotalBlocks { get; }`: Gets the total blocks.
- `ulong TotalNodes { get; }`: Gets the total nodes.
