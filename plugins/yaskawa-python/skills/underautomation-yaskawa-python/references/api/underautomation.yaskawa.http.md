# underautomation.yaskawa.http

## FileDescription

`from underautomation.yaskawa.http.file_description import FileDescription`

Describes a file available on the robot controller.

- `FileDescription()`
- `name: str (read only)`: File name including extension.
- `description: str (read only)`: Description of the file, if available.

## HttpClient

`from underautomation.yaskawa.http.http_client import HttpClient`

Standalone client class for communicating with Yaskawa Motoman industrial robots via HTTP. Provides file listing and file content retrieval from the robot controller's built-in web server.

- `HttpClient()`: Creates a new instance of HttpClient for robot communication. Call Connect() to establish communication with a robot controller.
- `connect(ip: str, parameters: HttpConnectParameters) -> None`: Connects to the robot controller with custom connection parameters.
- `connect(ip: str) -> None`: Connects to the robot controller using default parameters.
- Inherited from [HttpClientBase](underautomation.yaskawa.http.internal.md#httpclientbase-robothttp): `close`, `get_file_list`, `get_file`, `connected`, `address`, `port`

## HttpConnectParameters

`from underautomation.yaskawa.http.http_connect_parameters import HttpConnectParameters`

Connection parameters for HTTP communication with the robot controller.

- `HttpConnectParameters()`: Initializes a new instance of the HTTP connection parameters.
- `port: int`: Gets or sets the HTTP port number. Default: 80.
- `timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for a response. Default: 5000ms.
- `static DEFAULT_PORT: int`: Default HTTP port (80).
- `static DEFAULT_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for HTTP requests (5000ms).
