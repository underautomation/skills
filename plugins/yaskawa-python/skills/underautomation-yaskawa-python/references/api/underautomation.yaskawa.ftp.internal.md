# underautomation.yaskawa.ftp.internal

## FtpClientBase (robot.ftp)

`from underautomation.yaskawa.ftp.internal.ftp_client_base import FtpClientBase`

Abstract base class that implements FTP communication with a Yaskawa robot controller. Provides file management (upload, download, list, delete) via the controller's FTP server.

- `close() -> None`
- `get_file(fileName: str) -> str`: Downloads a text file from the robot controller and returns its content.
- `get_file_list(fileExtension: FileExtension) -> typing.List[str]`: Lists the files of the specified type on the controller.
- `get_file_list_by_pattern(pattern: str) -> typing.List[str]`: Lists the files whose names match the specified pattern. When the pattern has a known extension (e.g. "*.JBI"), only the matching folder is listed. Otherwise, all folders of the controller are listed.
- `load_file(fileName: str, content: str) -> None`: Uploads text content to the robot controller as a file. The file type is given by the extension of fileName (e.g. ".JBI" for a job).
- `delete_file(fileName: str) -> None`: Deletes a file from the robot controller. The "anonymous" user cannot delete files.
- `upload_file(remotePath: str, data: typing.List[int], progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Uploads a byte array as a file onto the controller. Only jobs (.JBI, .JBR), condition files (.CND) and general data (.DAT) can be uploaded, with the "ftp" or "rcmaster" user. An existing job is not overwritten: delete it first with delete_file().
- `upload_file_from_local(localPath: str, remotePath: str=None, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Uploads a local file onto the controller. Only jobs (.JBI, .JBR), condition files (.CND) and general data (.DAT) can be uploaded, with the "ftp" or "rcmaster" user. An existing job is not overwritten: delete it first with delete_file().
- `upload_files_from_local(localPaths: typing.List[str], progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[str]`: Uploads several local files onto the controller. Each file is uploaded with its local file name. The controller stores each file in the folder of its type (e.g. a ".JBI" file goes to the JOB folder). The upload stops at the first error.
- `download_file(remotePath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[int]`: Downloads a file from the controller and returns its content.
- `download_file_to_local(remotePath: str, localPath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> None`: Downloads a file from the controller and saves it on the local file system. Overwrites the local file if it already exists. The local file is not created if the download fails.
- `download_files_to_local(remotePaths: typing.List[str], localFolder: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[str]`: Downloads several files from the controller into a local folder. Each file is saved with its name, and existing local files are overwritten.
- `file_exists(remotePath: str) -> bool`: Checks whether a file exists on the controller.
- `directory_exists(path: str) -> bool`: Checks whether a folder exists on the controller.
- `get_listing(path: str) -> typing.List[FtpListItem]`: Returns the files and folders at the specified path on the controller. The root contains one folder per file type (JOB, DAT, CND, SYS, PRM, LST, CSV, LOG, TXT).
- `address: str (read only)`
- `connected: bool (read only)`
- `user: str (read only)`: FTP user name used for the current connection.

## FtpClientInternal (robot.ftp)

`from underautomation.yaskawa.ftp.internal.ftp_client_internal import FtpClientInternal`

Internal implementation of the FTP client. This class is not intended for direct use by application code. Use YaskawaRobot instead.

- Inherited from [FtpClientBase](underautomation.yaskawa.ftp.internal.md#ftpclientbase-robotftp): `close`, `get_file`, `get_file_list`, `get_file_list_by_pattern`, `load_file`, `delete_file`, `upload_file`, `upload_file_from_local`, `upload_files_from_local`, `download_file`, `download_file_to_local`, `download_files_to_local`, `file_exists`, `directory_exists`, `get_listing`, `address`, `connected`, `user`

## FtpConnectParametersInternal

`from underautomation.yaskawa.ftp.internal.ftp_connect_parameters_internal import FtpConnectParametersInternal`

FTP connection parameters with an enable flag, used by ConnectParameters.

- `FtpConnectParametersInternal()`
- `enable: bool`: Gets or sets a value indicating whether to establish an FTP connection when calling connect(). Default: false.
- Inherited from [FtpConnectParameters](underautomation.yaskawa.ftp.md#ftpconnectparameters): `DEFAULT_PORT`, `DEFAULT_TIMEOUT_MILLISECONDS`, `ftp_user`, `ftp_password`, `port`, `timeout_milliseconds`
