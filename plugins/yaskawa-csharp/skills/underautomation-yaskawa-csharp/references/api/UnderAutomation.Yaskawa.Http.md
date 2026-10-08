# UnderAutomation.Yaskawa.Http

## FileDescription

`class FileDescription`

Describes a file available on the robot controller.

- `FileDescription()`
- `string Description { get; }`: Description of the file, if available.
- `string Name { get; }`: File name including extension.

## HttpClient

`class HttpClient : HttpClientBase, IFileReader, IYaskawaClient`

Standalone client class for communicating with Yaskawa Motoman industrial robots via HTTP. Provides file listing and file content retrieval from the robot controller's built-in web server.

- `HttpClient()`: Creates a new instance of HttpClient for robot communication. Call Connect() to establish communication with a robot controller.
- `void Connect(string ip)`: Connects to the robot controller using default parameters.
- `void Connect(string ip, HttpConnectParameters parameters)`: Connects to the robot controller with custom connection parameters.
- Inherited from [HttpClientBase](UnderAutomation.Yaskawa.Http.Internal.md#httpclientbase-robothttp): `Close`, `GetFileList`, `GetFile`, `Connected`, `Address`, `Port`

## HttpConnectParameters

`class HttpConnectParameters`

Connection parameters for HTTP communication with the robot controller.

- `HttpConnectParameters()`: Initializes a new instance of the HTTP connection parameters.
- `const int DEFAULT_PORT = 80`: Default HTTP port (80).
- `const int DEFAULT_TIMEOUT_MILLISECONDS = 5000`: Default timeout in milliseconds for HTTP requests (5000ms).
- `int Port { get; set; }`: Gets or sets the HTTP port number. Default: 80.
- `int TimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for a response. Default: 5000ms.
