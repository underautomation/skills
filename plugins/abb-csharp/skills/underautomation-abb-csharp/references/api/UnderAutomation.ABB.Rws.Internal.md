# UnderAutomation.ABB.Rws.Internal

## RwsClientBase (robot.Rws)

`abstract class RwsClientBase`

Base class providing HTTP communication with ABB RWS REST API. Handles Digest Authentication, request building and XML response parsing. Supports both RWS v1 and v2.

- `ControllerService Controller { get; }`: Controller Service
- `void Disconnect()`: Disconnect from the robot controller
- `ElogService Elog { get; }`: Event Log Service
- `bool Enabled { get; }`: Whether the client is connected and ready
- `FileService File { get; }`: File Service
- `IoService Io { get; }`: I/O System Service
- `string Ip { get; }`: IP address or hostname of the robot controller
- `MastershipService Mastership { get; }`: Mastership Service
- `MotionSystemService MotionSystem { get; }`: Motion System Service
- `PanelService Panel { get; }`: Control Panel Service
- `int Port { get; }`: Port of the RWS service
- `RapidService Rapid { get; }`: RAPID Service
- `SystemService System { get; }`: System Service
- `int Timeout { get; }`: HTTP request timeout in milliseconds
- `bool UseHttps { get; }`: Whether the connection uses HTTPS
- `RwsVersion Version { get; }`: RWS protocol version this client talks to

## RwsClientInternal (robot.Rws)

`class RwsClientInternal : RwsClientBase`

Internal RWS client for use by ABB.AbbController. This class is used internally and should not be instantiated directly.

- Inherited from [RwsClientBase](UnderAutomation.ABB.Rws.Internal.md#rwsclientbase-robotrws): `Disconnect`, `Ip`, `Port`, `UseHttps`, `Timeout`, `Enabled`, `Version`, `File`, `Controller`, `Io`, `Elog`, `System`, `Panel`, `MotionSystem`, `Mastership`, `Rapid`

## RwsConnectParametersBase

`abstract class RwsConnectParametersBase`

Base class for connection parameters. Contains core properties needed for RWS connection.

- `string Password { get; set; }`: Password for Digest Authentication (Default is "robotics")
- `int Port { get; set; }`: RWS service port (if set to 0, the SDK will use 80 for HTTP, 443 for HTTPS)
- `int Timeout { get; set; }`: HTTP request timeout in milliseconds (default: 1000ms)
- `bool UseHttps { get; set; }`: Whether to use HTTPS instead of HTTP (default: false)
- `string Username { get; set; }`: Username for Digest Authentication (Default is "Default User")
- `RwsVersion Version { get; set; }`: RWS protocol version to use. If not specified, RwsVersion.OmniCore_V2_0 (RWS 2.0) is used. RWS 2.0 is available in RobotWare &gt;= 7, which ships the new OmniCore controller generation. For older RobotWare versions running on IRC5 controllers, use RwsVersion.Irc5_V1_0 (RWS 1.0).
