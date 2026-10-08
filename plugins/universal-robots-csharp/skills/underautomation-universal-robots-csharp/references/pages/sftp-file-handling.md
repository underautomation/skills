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

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Ssh.Tools.Sftp;

class Sftp
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // SFTP is disabled by default
    parameters.Ssh.EnableSftp = true;

    // "ur" and "easybot" by default
    parameters.Ssh.Username = "root";
    parameters.Ssh.Password = "easybot";

    robot.Connect(parameters);

    // Download a program from the robot
    robot.Sftp.DownloadFile("/programs/my_program.urp", @"C:\temp\my_program.urp");

    // Send a program to the robot
    robot.Sftp.UploadFile(@"C:\temp\my_program.urp", "/programs/my_program.urp");

    // Rename, check, delete
    robot.Sftp.RenameFile("/programs/my_program.urp", "/programs/old_program.urp");
    bool exists = robot.Sftp.Exists("/programs/old_program.urp");
    robot.Sftp.DeleteFile("/programs/old_program.urp");

    // List a folder
    foreach (SftpFile item in robot.Sftp.ListDirectory("/programs/"))
      Console.WriteLine(item.Name + " " + item.IsDirectory + " " + item.Length + " " + item.LastWriteTimeUtc);

    // Read and write text files
    robot.Sftp.WriteAllText("/programs/note.txt", "Hello");
    string text = robot.Sftp.ReadAllText("/programs/note.txt");
  }
}
```

The progress callbacks of `DownloadFile`, `UploadFile` and `ListDirectory` are optional. In Python, pass a function that takes the number of bytes or of entries.

## List the programs

`EnumeratePrograms` and `EnumerateInstallations` return the relative paths of the `.urp` and `.installation` files of the programs folder and of its subfolders. They look in `/programs`, or in the folder of URSim when `/programs` does not exist. The client also works without `UR`:

```csharp
using UnderAutomation.UniversalRobots.Ssh;

class SftpDirect
{
  static void Main(string[] args)
  {
    // An SFTP client, without a UR instance
    var client = new SftpClient();

    client.Connect("192.168.0.1", "root", "easybot");

    // Relative paths of the .urp files of the programs folder, and of its subfolders
    string[] programs = client.EnumeratePrograms();
    string[] installations = client.EnumerateInstallations();

    client.Disconnect();
  }
}
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

**SftpClient** ([reference](../api/UnderAutomation.UniversalRobots.Ssh.md#sftpclient))

- `SftpClient()`
- `void Connect(string ip, string username, string password, int port = 22)`: Connects to the robot
- Inherited from [SftpClientBase](../api/UnderAutomation.UniversalRobots.Ssh.Internal.md#sftpclientbase-robotsftp): `Disconnect`, `ChangeDirectory`, `ChangePermissions`, `CreateDirectory`, `DeleteDirectory`, `DeleteFile`, `RenameFile`, `SymbolicLink`, `ListDirectory`, `EnumeratePrograms`, `EnumerateInstallations`, `BeginListDirectory`, `EndListDirectory`, `Get`, `Exists`, `DownloadFile`, `BeginDownloadFile`, `EndDownloadFile`, `UploadFile`, `BeginUploadFile`, `EndUploadFile`, `GetStatus`, `AppendAllLines`, `AppendAllText`, `AppendText`, `Create`, `CreateText`, `Delete`, `GetLastAccessTime`, `GetLastAccessTimeUtc`, `GetLastWriteTime`, `GetLastWriteTimeUtc`, `Open`, `OpenRead`, `OpenText`, `OpenWrite`, `ReadAllBytes`, `ReadAllLines`, `ReadAllText`, `ReadLines`, `WriteAllBytes`, `WriteAllLines`, `WriteAllText`, `GetAttributes`, `SetAttributes`, `SynchronizeDirectories`, `BeginSynchronizeDirectories`, `EndSynchronizeDirectories`, `Connected`, `OperationTimeout`, `BufferSize`, `WorkingDirectory`, `ProtocolVersion`
- Inherited from [URServiceBase](../api/UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

**SftpClientBase** ([reference](../api/UnderAutomation.UniversalRobots.Ssh.Internal.md#sftpclientbase-robotsftp))

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
- Inherited from [URServiceBase](../api/UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

**SftpFile** ([reference](../api/UnderAutomation.UniversalRobots.Ssh.Tools.Sftp.md#sftpfile))

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

**SftpFileAttributes** ([reference](../api/UnderAutomation.UniversalRobots.Ssh.Tools.Sftp.md#sftpfileattributes))

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

## What to read next

- [Transfer files and backups](how-to-transfer-files.md): a backup of the programs and the upload of a program.
- [Program and installation files](archive-file.md): open and change a `.urp` file on the PC.
