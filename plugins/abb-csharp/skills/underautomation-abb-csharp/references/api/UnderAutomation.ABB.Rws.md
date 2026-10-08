# UnderAutomation.ABB.Rws

## RwsClient

`class RwsClient : RwsClientBase`

Standalone public RWS client for ABB robot controllers. Supports both RWS v1 and v2. Use this class when you want to connect to a robot without using the ABB.AbbController class.

- `RwsClient()`: Create a new RWS client instance
- `void Connect(string ip, string username = "Default User", string password = "robotics", int port = 0, int timeout = 10000, bool useHttps = false, RwsVersion version = RwsVersion.OmniCore_V2_0)`: Connect to the robot controller RWS service
- Inherited from [RwsClientBase](UnderAutomation.ABB.Rws.Internal.md#rwsclientbase-robotrws): `Disconnect`, `Ip`, `Port`, `UseHttps`, `Timeout`, `Enabled`, `Version`, `File`, `Controller`, `Io`, `Elog`, `System`, `Panel`, `MotionSystem`, `Mastership`, `Rapid`

## RwsConnectParameters

`class RwsConnectParameters : RwsConnectParametersBase`

Connection parameters for ABB Robot Web Services (RWS). Supports both RWS v1 and v2.

- `RwsConnectParameters()`
- `const string DEFAULT_PASSWORD = "robotics"`: Default password for Digest Authentication
- `const int DEFAULT_PORT = 80`: Default RWS port (80 for HTTP, 443 for HTTPS)
- `const int DEFAULT_TIMEOUT = 10000`: Default timeout in milliseconds
- `const string DEFAULT_USERNAME = "Default User"`: Default username for Digest Authentication
- `bool Enable { get; set; }`: Enable or disable the RWS client connection
- Inherited from [RwsConnectParametersBase](UnderAutomation.ABB.Rws.Internal.md#rwsconnectparametersbase): `Port`, `Username`, `Password`, `Timeout`, `UseHttps`, `Version`

## RwsException

`class RwsException : Exception, ISerializable`

Exception thrown when an RWS API request fails. Compatible with RWS v1 and v2.

- `RwsException(string message)`: Creates a new RWS exception with a message
- `RwsException(string message, Exception innerException)`: Creates a new RWS exception with a message and inner exception
- `RwsException(string message, int statusCode, string responseBody)`: Creates a new RWS exception with a message, status code and response body
- `RwsException(string message, string responseBody)`: Creates a new RWS exception with a message and the raw response body
- `RwsException(string message, RwsException innerException)`: Creates a new RWS exception that explains the failure of another one, keeping its diagnostics
- `string ReasonPhrase { get; }`: HTTP reason phrase returned by the server (e.g. "Forbidden", "Method Not Allowed"), if available
- `string ResponseBody { get; }`: Raw response body from the server, if available
- `string RwsErrorCode { get; }`: ABB internal error code extracted from the RWS error payload (e.g. "-1073445865"), if present
- `string RwsErrorMessage { get; }`: Human readable error text extracted from the RWS error payload, if present
- `int? StatusCode { get; }`: HTTP status code returned by the server

## RwsVersion (robot.Rws.Version)

`enum RwsVersion`

Version of the ABB Robot Web Services (RWS) protocol exposed by the robot controller. The two versions differ in URL shapes, parameter placement and media types, so the client has to know which one it talks to. Pick the value that matches the controller generation.

- Irc5_V1_0: RWS 1.0, exposed by IRC5 controllers running RobotWare 6 and earlier.
- OmniCore_V2_0: RWS 2.0, exposed by OmniCore controllers running RobotWare 7 and later. This is the default when no version is specified.
