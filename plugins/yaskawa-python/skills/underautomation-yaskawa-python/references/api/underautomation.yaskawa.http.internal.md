# underautomation.yaskawa.http.internal

## HttpClientBase (robot.http)

`from underautomation.yaskawa.http.internal.http_client_base import HttpClientBase`

Base class implementing HTTP communication with Yaskawa robot controllers. Provides file listing and file content retrieval via the controller's built-in HTTP server.

- `close() -> None`: Marks the client as disconnected.
- `get_file_list(fileExtension: FileExtension) -> typing.List[FileDescription]`: Gets the list of files of the specified type available on the robot controller.
- `get_file(fileName: str) -> str`: Gets the content of a file from the robot controller. The file type is deduced from the file name extension (e.g. "PICK_JOB.JBI" queries /FGET_REQUEST/ROBOT/JOB/PICK_JOB.JBI).
- `connected: bool (read only)`: Indicates whether the client is configured and ready to communicate.
- `address: str (read only)`
- `port: int (read only)`: Gets the HTTP port number.

## HttpClientInternal (robot.http)

`from underautomation.yaskawa.http.internal.http_client_internal import HttpClientInternal`

Internal implementation of the HTTP client. This class is not intended for direct use by application code. Use YaskawaRobot instead.

- Inherited from [HttpClientBase](underautomation.yaskawa.http.internal.md#httpclientbase-robothttp): `close`, `get_file_list`, `get_file`, `connected`, `address`, `port`

## HttpConnectParametersInternal

`from underautomation.yaskawa.http.internal.http_connect_parameters_internal import HttpConnectParametersInternal`

Connection parameters for HTTP communication with the robot controller, with enable flag.

- `HttpConnectParametersInternal()`
- `enable: bool`: Gets or sets a value indicating whether to enable the HTTP connection (default: false).
- Inherited from [HttpConnectParameters](underautomation.yaskawa.http.md#httpconnectparameters): `DEFAULT_PORT`, `DEFAULT_TIMEOUT_MILLISECONDS`, `port`, `timeout_milliseconds`
