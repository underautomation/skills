# UnderAutomation.Fanuc.Ftp

## FtpClient

`class FtpClient : FtpClientBase`

FTP Client connection to a robot

- `FtpClient()`: Instanciate a new FTP client connection
- `void Connect(string ip, string user, string password, int port = 21, int timeoutMs = 30000)`: Connect to a robot
- Inherited from [FtpClientBase](UnderAutomation.Fanuc.Ftp.Internal.md#ftpclientbase-robotftp): `Disconnect`, `EnumerateVariableFiles`, `EnumerateVariableFileNames`, `IP`, `Language`, `Connected`, `DirectFileHandling`
- Inherited from [FileClientBase](UnderAutomation.Fanuc.Common.Files.md#fileclientbase-robotftp): `GetSummaryDiagnostic`, `GetAllErrorsList`, `GetCurrentPosition`, `GetIOState`, `GetSafetyStatus`, `GetProgramStates`, `GetVariablesFromFile`, `GetAllVariables`, `KnownVariableFiles`

## FtpException

`class FtpException : Exception, ISerializable, _Exception`

Exception thrown when the controller refuses an FTP operation, or when the FTP communication fails. The message gives the reply of the controller and, when it is known, what to do.

- `bool ProgramInUse { get; }`: True when the controller refused the operation because the program is in use: it is selected on the teach pendant or it runs. Select another program before you upload or delete it.
- `string RemotePath { get; }`: Path of the file or folder on the controller concerned by the operation. Null when the operation has no path.
- `int ReplyCode { get; }`: FTP reply code returned by the controller (for example 550). 0 when the controller did not reply.
- `string ReplyMessage { get; }`: Reply text returned by the controller (for example "Specified program is in use"). Null when the controller did not reply.

## FtpExistsBehavior

`enum FtpExistsBehavior`

Defines the behavior for handling files that already exist

- Append: Append to the file if it exists, by checking the length and adding the missing data.
- AppendNoCheck: Append to the file, but don't check if it exists and add missing data. This might be required if you don't have permissions on the server to list files in the folder. Only use this if you are SURE that the file does not exist on the server otherwise it can cause the UploadFile method to hang due...
- NoCheck: Do not check if the file exists. A bit faster than the other options. Only use this if you are SURE that the file does not exist on the server. Otherwise it can cause the UploadFile method to hang due to filesize mismatch.
- Overwrite: Overwrite the file if it exists.
- Skip: Skip the file if it exists, without any more checks.

## FtpFileSystemObjectType

`enum FtpFileSystemObjectType`

Type of file system of object

- Directory: A directory
- File: A file
- Link: A symbolic link

## FtpListItem

`class FtpListItem`

Represents a file system object on the controller

- `int Chmod { get; }`: Gets the file permissions in the CHMOD format.
- `DateTime Created { get; }`: Gets the created date of the object.
- `string FullName { get; }`: Gets the full path name to the object.
- `DateTime Modified { get; }`: Gets the last write time of the object.
- `string Name { get; }`: Gets name to the object.
- `long Size { get; }`: Gets the size of the object. Only a few files (like *.tp or *.df) have a size that can be retrieved, for most files this is 0 even if they are not empty. For directories this is always 0.
- `FtpFileSystemObjectType Type { get; }`: Gets the type of file system object.
