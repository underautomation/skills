# underautomation.yaskawa.ftp

## FtpClient

`from underautomation.yaskawa.ftp.ftp_client import FtpClient`

Standalone FTP client for connecting directly to a Yaskawa robot controller.

- `FtpClient()`: Creates a new standalone FTP client instance.
- `connect(ip: str, user: str="anonymous", password: str=None, port: int=21, timeoutMilliseconds: int=30000) -> None`: Connects to the robot controller via FTP.
- Inherited from [FtpClientBase](underautomation.yaskawa.ftp.internal.md#ftpclientbase-robotftp): `close`, `get_file`, `get_file_list`, `get_file_list_by_pattern`, `load_file`, `delete_file`, `upload_file`, `upload_file_from_local`, `upload_files_from_local`, `download_file`, `download_file_to_local`, `download_files_to_local`, `file_exists`, `directory_exists`, `get_listing`, `address`, `connected`, `user`

## FtpConnectParameters

`from underautomation.yaskawa.ftp.ftp_connect_parameters import FtpConnectParameters`

Connection parameters for FTP communication with the Yaskawa robot controller.

- `FtpConnectParameters()`: Initializes a new instance of the FTP connection parameters with default values.
- `ftp_user: str`: Gets or sets the FTP user name used to authenticate with the robot controller. Standard accounts: rcmaster: widest rights, requires the management mode password.ftp: standard mode only, accepts any password.anonymous: standard mode only, accepts any password, download only. If the password protec...
- `ftp_password: str`: Gets or sets the FTP password associated with ftp_user. For rcmaster: must be the controller management mode password.For ftp or anonymous: any value is accepted (including null or empty).If the password protection option is enabled: use the password defined in that option. Default: null.
- `port: int`: Gets or sets the FTP port number. Default: 21.
- `timeout_milliseconds: int`: Gets or sets the timeout in milliseconds applied to FTP read, connect, and data transfer operations. Default: 30000ms.
- `static DEFAULT_PORT: int`: Default FTP port (21).
- `static DEFAULT_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for FTP operations (30000ms).

## FtpErrorReason

`from underautomation.yaskawa.ftp.ftp_error_reason import FtpErrorReason`

Reason why an FTP operation failed.

- Unknown: The controller refused the operation for another reason. See reply_message.
- LoginIncorrect: The user name or the password is not accepted by the controller.
- AccessDenied: The logged user does not have the right to do this operation on this file.
- FileNotFound: The file does not exist on the controller.
- JobAlreadyExists: The job already exists on the controller. The controller does not overwrite a job by FTP.
- DeleteRefused: The controller refused to delete the file.
- ConnectionError: The connection with the controller was lost or timed out.

## FtpException

`from UnderAutomation.Yaskawa.Ftp import FtpException`

Exception thrown when an FTP operation on the Yaskawa controller fails. The message explains the cause and, when the logged user does not have enough rights, which user to use.

The SDK raises this .NET type: catch it with `except FtpException as e` after the import above. Its members keep their .NET names. The class `FtpException` of the module `underautomation.yaskawa.ftp.ftp_exception` is not a Python exception and cannot be caught.

- `Operation: FtpOperation (read only)`: Operation that failed.
- `Reason: FtpErrorReason (read only)`: Reason of the failure.
- `RemotePath: str (read only)`: Path of the file on the controller concerned by the operation. Null for connection and listing errors.
- `User: str (read only)`: FTP user name that was logged when the error occurred.
- `ReplyCode: int (read only)`: FTP reply code returned by the controller (e.g. 550). 0 if the controller did not reply.
- `ReplyMessage: str (read only)`: Raw reply text returned by the controller. Null if the controller did not reply.
- Inherited from System.Exception: `Message`, `InnerException`

## FtpFileSystemObjectType

`from underautomation.yaskawa.ftp.ftp_file_system_object_type import FtpFileSystemObjectType`

Type of an item on the controller file system.

- File: A file.
- Directory: A folder.

## FtpListItem

`from underautomation.yaskawa.ftp.ftp_list_item import FtpListItem`

Represents a file or a folder on the robot controller.

- `full_name: str (read only)`: Full path on the controller (e.g. "/JOB/TEST.JBI").
- `name: str (read only)`: File or folder name without its path (e.g. "TEST.JBI").
- `modified: datetime (read only)`: Date and time of the last modification, as given by the controller.
- `type: FtpFileSystemObjectType (read only)`: Indicates whether this item is a file or a folder.

## FtpOperation

`from underautomation.yaskawa.ftp.ftp_operation import FtpOperation`

FTP operation that was running when an FtpException was thrown.

- Connect: Connection and login to the controller.
- List: Listing of files or folders.
- Download: File download from the controller.
- Upload: File upload to the controller.
- Delete: File deletion on the controller.

## OnProgressDelegate

`from underautomation.yaskawa.ftp.on_progress_delegate import OnProgressDelegate`

Delegate used to report file transfer progress.
