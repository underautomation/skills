# UnderAutomation.UniversalRobots.Ssh.Internal

## SftpClientBase (robot.Sftp)

`abstract class SftpClientBase : URServiceBase`

Implementation of the SSH File Transfer Protocol (SFTP) over SSH for transfering files to the robot controller

- `void AppendAllLines(string path, string[] contents)`: Appends lines to a file, creating the file if it does not already exist.
- `void AppendAllLines(string path, string[] contents, Encoding encoding)`: Appends lines to a file by using a specified encoding, creating the file if it does not already exist.
- `void AppendAllText(string path, string contents)`: Appends the specified string to the file, creating the file if it does not already exist.
- `void AppendAllText(string path, string contents, Encoding encoding)`: Appends the specified string to the file, creating the file if it does not already exist.
- `StreamWriter AppendText(string path)`: Creates a IO.StreamWriter that appends UTF-8 encoded text to the specified file, creating the file if it does not already exist.
- `StreamWriter AppendText(string path, Encoding encoding)`: Creates a IO.StreamWriter that appends text to a file using the specified encoding, creating the file if it does not already exist.
- `IAsyncResult BeginDownloadFile(string path, Stream output)`: Begins an asynchronous file downloading into the stream.
- `IAsyncResult BeginDownloadFile(string path, Stream output, AsyncCallback asyncCallback)`: Begins an asynchronous file downloading into the stream.
- `IAsyncResult BeginDownloadFile(string path, Stream output, AsyncCallback asyncCallback, object state, Action<ulong> downloadCallback = null)`: Begins an asynchronous file downloading into the stream.
- `IAsyncResult BeginListDirectory(string path, AsyncCallback asyncCallback, object state, Action<int> listCallback = null)`: Begins an asynchronous operation of retrieving list of files in remote directory.
- `IAsyncResult BeginSynchronizeDirectories(string sourcePath, string destinationPath, string searchPattern, AsyncCallback asyncCallback, object state)`: Begins the synchronize directories.
- `IAsyncResult BeginUploadFile(Stream input, string path)`: Begins an asynchronous uploading the stream into remote file.
- `IAsyncResult BeginUploadFile(Stream input, string path, AsyncCallback asyncCallback)`: Begins an asynchronous uploading the stream into remote file.
- `IAsyncResult BeginUploadFile(Stream input, string path, AsyncCallback asyncCallback, object state, Action<ulong> uploadCallback = null)`: Begins an asynchronous uploading the stream into remote file.
- `IAsyncResult BeginUploadFile(Stream input, string path, bool canOverride, AsyncCallback asyncCallback, object state, Action<ulong> uploadCallback = null)`: Begins an asynchronous uploading the stream into remote file.
- `uint BufferSize { get; set; }`: Gets or sets the maximum size of the buffer in bytes.
- `void ChangeDirectory(string path)`: Changes remote directory to path.
- `void ChangePermissions(string path, short mode)`: Changes permissions of file(s) to specified mode.
- `bool Connected { get; }`: Gets a value indicating if this client is connected to the robot
- `SftpFileStream Create(string path)`: Creates or overwrites a file in the specified path.
- `SftpFileStream Create(string path, int bufferSize)`: Creates or overwrites the specified file.
- `void CreateDirectory(string path)`: Creates remote directory specified by path.
- `StreamWriter CreateText(string path)`: Creates or opens a file for writing UTF-8 encoded text.
- `StreamWriter CreateText(string path, Encoding encoding)`: Creates or opens a file for writing text using the specified encoding.
- `void Delete(string path)`: Deletes the specified file or directory.
- `void DeleteDirectory(string path)`: Deletes remote directory specified by path.
- `void DeleteFile(string path)`: Deletes remote file specified by path.
- `void Disconnect()`: Disconnects this client from the SFTP server.
- `void DownloadFile(string path, Stream output, Action<ulong> downloadCallback = null)`: Downloads remote file specified by the path into the stream.
- `void DownloadFile(string path, string localPath, Action<ulong> downloadCallback = null)`: Downloads remote file specified by the path into the stream.
- `void EndDownloadFile(IAsyncResult asyncResult)`: Ends an asynchronous file downloading into the stream.
- `SftpFile[] EndListDirectory(IAsyncResult asyncResult)`: Ends an asynchronous operation of retrieving list of files in remote directory.
- `FileInfo[] EndSynchronizeDirectories(IAsyncResult asyncResult)`: Ends the synchronize directories.
- `void EndUploadFile(IAsyncResult asyncResult)`: Ends an asynchronous uploading the stream into remote file.
- `string[] EnumerateInstallations()`: Enumerates installations with .installation extension. It searches recursively installations in "/programs" if it exists, or "/home/ur/ursim-current/programs" for simulator
- `string[] EnumeratePrograms()`: Enumerates programs with .urp extension. It searches recursively programs in "/programs" if it exists, or "/home/ur/ursim-current/programs" for simulator
- `bool Exists(string path)`: Checks whether file or directory exists;
- `SftpFile Get(string path)`: Gets reference to remote file or directory.
- `SftpFileAttributes GetAttributes(string path)`: Gets the Sftp.SftpFileAttributes of the file on the path.
- `DateTime GetLastAccessTime(string path)`: Returns the date and time the specified file or directory was last accessed.
- `DateTime GetLastAccessTimeUtc(string path)`: Returns the date and time, in coordinated universal time (UTC), that the specified file or directory was last accessed.
- `DateTime GetLastWriteTime(string path)`: Returns the date and time the specified file or directory was last written to.
- `DateTime GetLastWriteTimeUtc(string path)`: Returns the date and time, in coordinated universal time (UTC), that the specified file or directory was last written to.
- `SftpFileSytemInformation GetStatus(string path)`: Gets status using statvfs@openssh.com request.
- `SftpFile[] ListDirectory(string path, Action<int> listCallback = null)`: Retrieves list of files in remote directory.
- `SftpFileStream Open(string path, FileMode mode)`: Opens a Sftp.SftpFileStream on the specified path with read/write access.
- `SftpFileStream Open(string path, FileMode mode, FileAccess access)`: Opens a Sftp.SftpFileStream on the specified path, with the specified mode and access.
- `SftpFileStream OpenRead(string path)`: Opens an existing file for reading.
- `StreamReader OpenText(string path)`: Opens an existing UTF-8 encoded text file for reading.
- `SftpFileStream OpenWrite(string path)`: Opens a file for writing.
- `TimeSpan OperationTimeout { get; set; }`: Gets or sets the operation timeout.
- `int ProtocolVersion { get; }`: Gets sftp protocol version.
- `byte[] ReadAllBytes(string path)`: Opens a binary file, reads the contents of the file into a byte array, and closes the file.
- `string[] ReadAllLines(string path)`: Opens a text file, reads all lines of the file using UTF-8 encoding, and closes the file.
- `string[] ReadAllLines(string path, Encoding encoding)`: Opens a file, reads all lines of the file with the specified encoding, and closes the file.
- `string ReadAllText(string path)`: Opens a text file, reads all lines of the file with the UTF-8 encoding, and closes the file.
- `string ReadAllText(string path, Encoding encoding)`: Opens a file, reads all lines of the file with the specified encoding, and closes the file.
- `string[] ReadLines(string path)`: Reads the lines of a file with the UTF-8 encoding.
- `string[] ReadLines(string path, Encoding encoding)`: Read the lines of a file that has a specified encoding.
- `void RenameFile(string oldPath, string newPath)`: Renames remote file from old path to new path.
- `void RenameFile(string oldPath, string newPath, bool isPosix)`: Renames remote file from old path to new path.
- `void SetAttributes(string path, SftpFileAttributes fileAttributes)`: Sets the specified Sftp.SftpFileAttributes of the file on the specified path.
- `void SymbolicLink(string path, string linkPath)`: Creates a symbolic link from old path to new path.
- `FileInfo[] SynchronizeDirectories(string sourcePath, string destinationPath, string searchPattern)`: Synchronizes the directories.
- `void UploadFile(Stream input, string path, Action<ulong> uploadCallback = null)`: Uploads stream into remote file.
- `void UploadFile(Stream input, string path, bool canOverride, Action<ulong> uploadCallback = null)`: Uploads stream into remote file.
- `void UploadFile(string localPath, string path, Action<ulong> uploadCallback = null)`: Uploads file into remote file.
- `string WorkingDirectory { get; }`: Gets remote working directory.
- `void WriteAllBytes(string path, byte[] bytes)`: Writes the specified byte array to the specified file, and closes the file.
- `void WriteAllLines(string path, string[] contents)`: Writes a collection of strings to the file using the UTF-8 encoding, and closes the file.
- `void WriteAllText(string path, string contents)`: Writes the specified string to the file using the UTF-8 encoding, and closes the file.
- `void WriteAllText(string path, string contents, Encoding encoding)`: Writes the specified string to the file using the specified encoding, and closes the file.
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## SshClientBase (robot.Ssh)

`abstract class SshClientBase : URServiceBase`

Provides a client connection to SSH server

- `bool Connected { get; }`: Gets a value indicating if this client is connected to the robot
- `SshCommand CreateCommand(string commandText)`: Creates the command to be executed.
- `SshCommand CreateCommand(string commandText, Encoding encoding)`: Creates the command to be executed with specified encoding.
- `Shell CreateShell(Stream input, Stream output, Stream extendedOutput)`: Creates the shell.
- `Shell CreateShell(Stream input, Stream output, Stream extendedOutput, string terminalName, uint columns, uint rows, uint width, uint height, IDictionary<TerminalModes, uint> terminalModes)`: Creates the shell.
- `Shell CreateShell(Stream input, Stream output, Stream extendedOutput, string terminalName, uint columns, uint rows, uint width, uint height, IDictionary<TerminalModes, uint> terminalModes, int bufferSize)`: Creates the shell.
- `Shell CreateShell(Encoding encoding, string input, Stream output, Stream extendedOutput)`: Creates the shell.
- `Shell CreateShell(Encoding encoding, string input, Stream output, Stream extendedOutput, string terminalName, uint columns, uint rows, uint width, uint height, IDictionary<TerminalModes, uint> terminalModes)`: Creates the shell.
- `Shell CreateShell(Encoding encoding, string input, Stream output, Stream extendedOutput, string terminalName, uint columns, uint rows, uint width, uint height, IDictionary<TerminalModes, uint> terminalModes, int bufferSize)`: Creates the shell.
- `ShellStream CreateShellStream(string terminalName, uint columns, uint rows, uint width, uint height, int bufferSize)`: Creates the shell stream.
- `ShellStream CreateShellStream(string terminalName, uint columns, uint rows, uint width, uint height, int bufferSize, IDictionary<TerminalModes, uint> terminalModeValues)`: Creates the shell stream.
- `void Disconnect()`: Disconnects this client from the SSH server
- `SshCommand RunCommand(string commandText)`: Creates and executes the command.
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## SshParametersBase

`abstract class SshParametersBase`

Base class for SSH and SFTP connection parameters, including credentials and port configuration.

- `const int DEFAULT_PORT = 22`: Default SSH server TCP port
- `string Password { get; set; }`: Setup Linux Password for SSH connection Default value is "easybot"
- `int Port { get; set; }`: SSH and SFTP TCP port. Default : 22
- `string Username { get; set; }`: Setup Linux Username for SSH connection Default value is "ur" for simulator and "root" for real robot
