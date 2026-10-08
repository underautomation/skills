# UnderAutomation.Yaskawa.Http.Internal

## HttpClientBase (robot.Http)

`abstract class HttpClientBase : IFileReader, IYaskawaClient`

Base class implementing HTTP communication with Yaskawa robot controllers. Provides file listing and file content retrieval via the controller's built-in HTTP server.

- `string Address { get; }`: Gets the address of the robot controller: an IP address or a host name.
- `void Close()`: Marks the client as disconnected.
- `bool Connected { get; }`: Indicates whether the client is configured and ready to communicate.
- `string GetFile(string fileName)`: Gets the content of a file from the robot controller. The file type is deduced from the file name extension (e.g. "PICK_JOB.JBI" queries /FGET_REQUEST/ROBOT/JOB/PICK_JOB.JBI).
- `FileDescription[] GetFileList(FileExtension fileExtension)`: Gets the list of files of the specified type available on the robot controller.
- `int Port { get; }`: Gets the HTTP port number.

## HttpClientInternal (robot.Http)

`class HttpClientInternal : HttpClientBase, IFileReader, IYaskawaClient`

Internal implementation of the HTTP client. This class is not intended for direct use by application code. Use Yaskawa.YaskawaRobot instead.

- Inherited from [HttpClientBase](UnderAutomation.Yaskawa.Http.Internal.md#httpclientbase-robothttp): `Close`, `GetFileList`, `GetFile`, `Connected`, `Address`, `Port`

## HttpConnectParametersInternal

`class HttpConnectParametersInternal : HttpConnectParameters`

Connection parameters for HTTP communication with the robot controller, with enable flag.

- `HttpConnectParametersInternal()`
- `bool Enable { get; set; }`: Gets or sets a value indicating whether to enable the HTTP connection (default: false).
- Inherited from [HttpConnectParameters](UnderAutomation.Yaskawa.Http.md#httpconnectparameters): `DEFAULT_PORT`, `DEFAULT_TIMEOUT_MILLISECONDS`, `Port`, `TimeoutMilliseconds`
