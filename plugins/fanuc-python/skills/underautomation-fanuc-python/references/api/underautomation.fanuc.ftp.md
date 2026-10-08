# underautomation.fanuc.ftp

## FtpClient

`from underautomation.fanuc.ftp.ftp_client import FtpClient`

FTP Client connection to a robot

- `FtpClient()`: Instanciate a new FTP client connection
- `connect(ip: str, user: str, password: str, port: int=21, timeoutMs: int=30000) -> None`: Connect to a robot
- Inherited from [FtpClientBase](underautomation.fanuc.ftp.internal.md#ftpclientbase-robotftp): `disconnect`, `enumerate_variable_files`, `enumerate_variable_file_names`, `ip`, `language`, `connected`, `direct_file_handling`
- Inherited from [FileClientBase](underautomation.fanuc.common.files.md#fileclientbase-robotftp): `get_summary_diagnostic`, `get_all_errors_list`, `get_current_position`, `get_io_state`, `get_safety_status`, `get_program_states`, `get_variables_from_file`, `get_all_variables`, `known_variable_files`

## FtpExistsBehavior

`from underautomation.fanuc.ftp.ftp_exists_behavior import FtpExistsBehavior`

Defines the behavior for handling files that already exist

- NoCheck: Do not check if the file exists. A bit faster than the other options. Only use this if you are SURE that the file does not exist on the server. Otherwise it can cause the UploadFile method to hang due to filesize mismatch.
- Skip: Skip the file if it exists, without any more checks.
- Overwrite: Overwrite the file if it exists.
- Append: Append to the file if it exists, by checking the length and adding the missing data.
- AppendNoCheck: Append to the file, but don't check if it exists and add missing data. This might be required if you don't have permissions on the server to list files in the folder. Only use this if you are SURE that the file does not exist on the server otherwise it can cause the UploadFile method to hang due...

## FtpFileSystemObjectType

`from underautomation.fanuc.ftp.ftp_file_system_object_type import FtpFileSystemObjectType`

Type of file system of object

- File: A file
- Directory: A directory
- Link: A symbolic link

## FtpListItem

`from underautomation.fanuc.ftp.ftp_list_item import FtpListItem`

Represents a file system object on the controller

- `size: int (read only)`: Gets the size of the object. Only a few files (like *.tp or *.df) have a size that can be retrieved, for most files this is 0 even if they are not empty. For directories this is always 0.
- `chmod: int (read only)`: Gets the file permissions in the CHMOD format.
- `created: datetime (read only)`: Gets the created date of the object.
- `full_name: str (read only)`: Gets the full path name to the object.
- `name: str (read only)`: Gets name to the object.
- `modified: datetime (read only)`: Gets the last write time of the object.
- `type: FtpFileSystemObjectType (read only)`: Gets the type of file system object.
