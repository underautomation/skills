# UnderAutomation.Fanuc.Ftp.Internal

## FtpClientBase (robot.Ftp)

`abstract class FtpClientBase : FileClientBase`

Base class for FTP features

- `bool Connected { get; }`: Indicates that FTP connection is active
- `FtpDirectFileHandling DirectFileHandling { get; }`: Contains methods to manipulate files and folders on the controller (upload, download, delete, ...)
- `void Disconnect()`: Disconnects from FTP server
- `string[] EnumerateVariableFileNames()`: Get the list of all variable file names available on the controller
- `FtpListItem[] EnumerateVariableFiles()`: Get a list of all variable files on controller
- `string IP { get; }`: Connect robot IP address or host name
- `Languages Language { get; set; }`: Controller language (default is English)
- Inherited from [FileClientBase](UnderAutomation.Fanuc.Common.Files.md#fileclientbase-robotftp): `GetSummaryDiagnostic`, `GetAllErrorsList`, `GetCurrentPosition`, `GetIOState`, `GetSafetyStatus`, `GetProgramStates`, `GetVariablesFromFile`, `GetAllVariables`, `KnownVariableFiles`

## FtpClientInternal (robot.Ftp)

`class FtpClientInternal : FtpClientBase`

Internal implementation of FTP Client

- Inherited from [FtpClientBase](UnderAutomation.Fanuc.Ftp.Internal.md#ftpclientbase-robotftp): `Disconnect`, `EnumerateVariableFiles`, `EnumerateVariableFileNames`, `IP`, `Language`, `Connected`, `DirectFileHandling`
- Inherited from [FileClientBase](UnderAutomation.Fanuc.Common.Files.md#fileclientbase-robotftp): `GetSummaryDiagnostic`, `GetAllErrorsList`, `GetCurrentPosition`, `GetIOState`, `GetSafetyStatus`, `GetProgramStates`, `GetVariablesFromFile`, `GetAllVariables`, `KnownVariableFiles`

## FtpConnectParametersBase

`class FtpConnectParametersBase`

Parameters to connect to Fanuc controller FTP server

- `FtpConnectParametersBase()`
- `string FtpPassword { get; set; }`: FTP password associated to the user
- `int FtpTimeoutMs { get; set; }`: FTP connection timeout in milliseconds, default : 30000 (30 seconds)
- `string FtpUser { get; set; }`: FTP user. The rights depend on the user and on the password settings of the controller: for example, without a user the controller logs in at the OPERATOR level and can refuse the upload of a program.

## FtpDirectFileHandling (robot.Ftp.DirectFileHandling)

`class FtpDirectFileHandling`

Methods to handle files on a Fanuc controller (upload, download, delete, enumerate, ...). The controller can refuse an operation: the rights depend on the FTP user and on the password settings of the controller (for example, an upload of a program needs a user with enough rights), and a program t...

- `void CreateDirectory(string path)`: Creates a directory on the controller. If the preceding directories do not exist, then they are created.
- `void DeleteDirectory(string path)`: Deletes the specified directory and all its contents.
- `void DeleteFile(string path)`: Deletes a file on the controller
- `bool DirectoryExists(string path)`: Tests if the specified directory exists on the controller. This method works by trying to change the working directory to the path specified. If it succeeds, the directory is changed back to the old working directory and true is returned. False is returned otherwise and since the CWD failed it is...
- `bool DownloadFileFromController(out byte[] outBytes, string remotePath, OnProgressDelegate progress = null)`: Downloads the specified file and return the raw byte array. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks.
- `bool DownloadFileFromController(Stream outStream, string remotePath, OnProgressDelegate progress = null)`: Downloads the specified file into the specified stream. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks.
- `bool DownloadFileFromController(string localPath, string remotePath, OnProgressDelegate progress = null)`: Downloads the specified file onto the local file system. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks. It overwrites the file if it already exists.
- `string[] DownloadFilesFromController(string localDir, string[] remotePaths, OnProgressDelegate progress = null)`: Downloads the specified files into a local single directory. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks. A file that fails is skipped: it is not in the returned list.
- `bool FileExists(string path)`: Checks if a file exists on the controller.
- `FtpListItem[] GetListing(string path)`: Gets a file listing from the controller. Each Ftp.FtpListItem object returned contains information about the file that was able to be retrieved.
- `FtpListItem GetObjectInfo(string path)`: Returns information about a file system object. Returns null if the controller response can't be parsed or the controller returns a failure completion code. No exception is thrown on error because that would negate the usefulness of this method for checking for the existence of an object.
- `void Rename(string path, string dest)`: Renames an object on the remote file system. Throws exceptions if the file does not exist, or if the destination file already exists.
- `bool UploadFileToController(byte[] fileData, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, FtpExistsBehavior existsBehavior = FtpExistsBehavior.Overwrite)`: Uploads the specified byte array as a file onto the controller. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks. It overwrites file if it already exists.
- `bool UploadFileToController(Stream fileStream, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, FtpExistsBehavior existsBehavior = FtpExistsBehavior.Overwrite)`: Uploads the specified stream as a file onto the controller. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks. It overwrites file if it already exists.
- `bool UploadFileToController(string localPath, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, FtpExistsBehavior existsBehavior = FtpExistsBehavior.Overwrite)`: Uploads the specified file directly onto the controller. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks.
- `string[] UploadFilesToController(string[] localPaths, string remoteDir, OnProgressDelegate progress = null)`: Uploads the given file paths to a single folder on the controller. All files are placed directly into the given folder regardless of their path on the local filesystem. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks. A fi...
