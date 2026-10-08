# underautomation.fanuc.ftp.internal

## FtpClientBase (robot.ftp)

`from underautomation.fanuc.ftp.internal.ftp_client_base import FtpClientBase`

Base class for FTP features

- `disconnect() -> None`: Disconnects from FTP server
- `enumerate_variable_files() -> typing.List[FtpListItem]`: Get a list of all variable files on controller
- `enumerate_variable_file_names() -> typing.List[str]`
- `ip: str (read only)`: Connect robot IP address or host name
- `language: Languages`: Controller language (default is English)
- `connected: bool (read only)`: Indicates that FTP connection is active
- `direct_file_handling: FtpDirectFileHandling (read only)`: Contains methods to manipulate files and folders on the controller (upload, download, delete, ...)
- Inherited from [FileClientBase](underautomation.fanuc.common.files.md#fileclientbase-robotftp): `get_summary_diagnostic`, `get_all_errors_list`, `get_current_position`, `get_io_state`, `get_safety_status`, `get_program_states`, `get_variables_from_file`, `get_all_variables`, `known_variable_files`

## FtpClientInternal (robot.ftp)

`from underautomation.fanuc.ftp.internal.ftp_client_internal import FtpClientInternal`

Internal implementation of FTP Client

- Inherited from [FtpClientBase](underautomation.fanuc.ftp.internal.md#ftpclientbase-robotftp): `disconnect`, `enumerate_variable_files`, `enumerate_variable_file_names`, `ip`, `language`, `connected`, `direct_file_handling`
- Inherited from [FileClientBase](underautomation.fanuc.common.files.md#fileclientbase-robotftp): `get_summary_diagnostic`, `get_all_errors_list`, `get_current_position`, `get_io_state`, `get_safety_status`, `get_program_states`, `get_variables_from_file`, `get_all_variables`, `known_variable_files`

## FtpConnectParametersBase

`from underautomation.fanuc.ftp.internal.ftp_connect_parameters_base import FtpConnectParametersBase`

Parameters to connect to Fanuc controller FTP server

- `FtpConnectParametersBase()`
- `ftp_user: str`: FTP user
- `ftp_password: str`: FTP password associated to the user
- `ftp_timeout_ms: int`: FTP connection timeout in milliseconds, default : 30000 (30 seconds)

## FtpDirectFileHandling (robot.ftp.direct_file_handling)

`from underautomation.fanuc.ftp.internal.ftp_direct_file_handling import FtpDirectFileHandling`

Methods to handle files on a Fanuc controller (upload, download, delete, enumerate, ...)

- `upload_file_to_controller(fileData_or_localPath: typing.List[int] | str, remotePath: str, createRemoteDir: bool=False, progress: typing.Callable[[float], None] | OnProgressDelegate=None, existsBehavior: FtpExistsBehavior=FtpExistsBehavior.Overwrite) -> bool`: Uploads the specified byte array as a file onto the controller. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks. It overwrites file if it already exists. Uploads the specified file directly onto the controller. High-level...
- `upload_files_to_controller(localPaths: typing.List[str], remoteDir: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[str]`: Uploads the given file paths to a single folder on the controller. All files are placed directly into the given folder regardless of their path on the local filesystem. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks.
- `download_file_from_controller(localPath_or_outBytes: typing.List[int] | str, remotePath: str, progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> bool`: Downloads the specified file and return the raw byte array. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks. Downloads the specified file onto the local file system. High-level API that takes care of various edge cases i...
- `download_files_from_controller(localDir: str, remotePaths: typing.List[str], progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> typing.List[str]`: Downloads the specified files into a local single directory. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks.
- `file_exists(path: str) -> bool`: Checks if a file exists on the controller.
- `directory_exists(path: str) -> bool`: Tests if the specified directory exists on the controller. This method works by trying to change the working directory to the path specified. If it succeeds, the directory is changed back to the old working directory and true is returned. False is returned otherwise and since the CWD failed it is...
- `create_directory(path: str) -> None`: Creates a directory on the controller. If the preceding directories do not exist, then they are created.
- `delete_directory(path: str) -> None`: Deletes the specified directory and all its contents.
- `delete_file(path: str) -> None`: Deletes a file on the controller
- `get_listing(path: str) -> typing.List[FtpListItem]`: Gets a file listing from the controller. Each FtpListItem object returned contains information about the file that was able to be retrieved.
- `get_object_info(path: str) -> FtpListItem`: Returns information about a file system object. Returns null if the controller response can't be parsed or the controller returns a failure completion code. The error for a failure is logged with FtpTrace. No exception is thrown on error because that would negate the usefulness of this method for...
- `rename(path: str, dest: str) -> None`: Renames an object on the remote file system. Throws exceptions if the file does not exist, or if the destination file already exists.
