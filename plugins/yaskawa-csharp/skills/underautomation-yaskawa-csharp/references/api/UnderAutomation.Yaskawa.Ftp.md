# UnderAutomation.Yaskawa.Ftp

## FtpClient

`class FtpClient : FtpClientBase, IFileManager, IFileReader, IFileWriter, IYaskawaClient`

Standalone FTP client for connecting directly to a Yaskawa robot controller.

- `FtpClient()`: Creates a new standalone FTP client instance.
- `void Connect(string ip, string user = "anonymous", string password = null, int port = 21, int timeoutMilliseconds = 30000)`: Connects to the robot controller via FTP.
  - async: `Task ConnectAsync(string ip, string user = "anonymous", string password = null, int port = 21, int timeoutMilliseconds = 30000, CancellationToken cancellationToken = default)`
- Inherited from [FtpClientBase](UnderAutomation.Yaskawa.Ftp.Internal.md#ftpclientbase-robotftp): `Close`, `GetFile`, `GetFileList`, `GetFileListByPattern`, `GetFileAsync`, `GetFileListAsync`, `GetFileListByPatternAsync`, `LoadFile`, `DeleteFile`, `LoadFileAsync`, `DeleteFileAsync`, `UploadFile`, `UploadFileFromStream`, `UploadFileFromLocal`, `UploadFilesFromLocal`, `UploadFileAsync`, `UploadFileFromStreamAsync`, `UploadFileFromLocalAsync`, `UploadFilesFromLocalAsync`, `DownloadFile`, `DownloadFileToStream`, `DownloadFileToLocal`, `DownloadFilesToLocal`, `DownloadFileAsync`, `DownloadFileToStreamAsync`, `DownloadFileToLocalAsync`, `DownloadFilesToLocalAsync`, `FileExists`, `DirectoryExists`, `FileExistsAsync`, `DirectoryExistsAsync`, `GetListing`, `GetListingAsync`, `Address`, `Connected`, `User`

## FtpConnectParameters

`class FtpConnectParameters`

Connection parameters for FTP communication with the Yaskawa robot controller.

- `FtpConnectParameters()`: Initializes a new instance of the FTP connection parameters with default values.
- `const int DEFAULT_PORT = 21`: Default FTP port (21).
- `const int DEFAULT_TIMEOUT_MILLISECONDS = 30000`: Default timeout in milliseconds for FTP operations (30000ms).
- `string FtpPassword { get; set; }`: Gets or sets the FTP password associated with FtpConnectParameters.FtpUser. For rcmaster: must be the controller management mode password.For ftp or anonymous: any value is accepted (including null or empty).If the password protection option is enabled: use the password defined in that option. De...
- `string FtpUser { get; set; }`: Gets or sets the FTP user name used to authenticate with the robot controller. Standard accounts: rcmaster: widest rights, requires the management mode password.ftp: standard mode only, accepts any password.anonymous: standard mode only, accepts any password, download only. If the password protec...
- `int Port { get; set; }`: Gets or sets the FTP port number. Default: 21.
- `int TimeoutMilliseconds { get; set; }`: Gets or sets the timeout in milliseconds applied to FTP read, connect, and data transfer operations. Default: 30000ms.

## FtpErrorReason

`enum FtpErrorReason`

Reason why an FTP operation failed.

- AccessDenied: The logged user does not have the right to do this operation on this file.
- ConnectionError: The connection with the controller was lost or timed out.
- DeleteRefused: The controller refused to delete the file.
- FileNotFound: The file does not exist on the controller.
- JobAlreadyExists: The job already exists on the controller. The controller does not overwrite a job by FTP.
- LoginIncorrect: The user name or the password is not accepted by the controller.
- Unknown: The controller refused the operation for another reason. See FtpException.ReplyMessage.

## FtpException

`class FtpException : Exception, ISerializable`

Exception thrown when an FTP operation on the Yaskawa controller fails. The message explains the cause and, when the logged user does not have enough rights, which user to use.

- `FtpOperation Operation { get; }`: Operation that failed.
- `FtpErrorReason Reason { get; }`: Reason of the failure.
- `string RemotePath { get; }`: Path of the file on the controller concerned by the operation. Null for connection and listing errors.
- `int ReplyCode { get; }`: FTP reply code returned by the controller (e.g. 550). 0 if the controller did not reply.
- `string ReplyMessage { get; }`: Raw reply text returned by the controller. Null if the controller did not reply.
- `string User { get; }`: FTP user name that was logged when the error occurred.

## FtpFileSystemObjectType

`enum FtpFileSystemObjectType`

Type of an item on the controller file system.

- Directory: A folder.
- File: A file.

## FtpListItem

`class FtpListItem`

Represents a file or a folder on the robot controller.

- `string FullName { get; }`: Full path on the controller (e.g. "/JOB/TEST.JBI").
- `DateTime Modified { get; }`: Date and time of the last modification, as given by the controller.
- `string Name { get; }`: File or folder name without its path (e.g. "TEST.JBI").
- `FtpFileSystemObjectType Type { get; }`: Indicates whether this item is a file or a folder.

## FtpOperation

`enum FtpOperation`

FTP operation that was running when an Ftp.FtpException was thrown.

- Connect: Connection and login to the controller.
- Delete: File deletion on the controller.
- Download: File download from the controller.
- List: Listing of files or folders.
- Upload: File upload to the controller.

## OnProgressDelegate

`delegate void OnProgressDelegate(double progress)`

Delegate used to report file transfer progress.

- `OnProgressDelegate(object @object, nint method)`
- `IAsyncResult BeginInvoke(double progress, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(double progress)`
