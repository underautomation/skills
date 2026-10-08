# underautomation.abb.rws.internal

## RwsClientBase (robot.rws)

`from underautomation.abb.rws.internal.rws_client_base import RwsClientBase`

Base class providing HTTP communication with ABB RWS REST API. Handles Digest Authentication, request building and XML response parsing. Supports both RWS v1 and v2.

- `disconnect() -> None`: Disconnect from the robot controller
- `ip: str (read only)`: IP address or hostname of the robot controller
- `port: int (read only)`: Port of the RWS service
- `use_https: bool (read only)`: Whether the connection uses HTTPS
- `timeout: int (read only)`: HTTP request timeout in milliseconds
- `enabled: bool (read only)`: Whether the client is connected and ready
- `version: RwsVersion (read only)`: RWS protocol version this client talks to
- `file: FileService (read only)`: File Service
- `controller: ControllerService (read only)`: Controller Service
- `io: IoService (read only)`: I/O System Service
- `elog: ElogService (read only)`: Event Log Service
- `system: SystemService (read only)`: System Service
- `panel: PanelService (read only)`: Control Panel Service
- `motion_system: MotionSystemService (read only)`: Motion System Service
- `mastership: MastershipService (read only)`: Mastership Service
- `rapid: RapidService (read only)`: RAPID Service

## RwsClientInternal (robot.rws)

`from underautomation.abb.rws.internal.rws_client_internal import RwsClientInternal`

Internal RWS client for use by AbbController. This class is used internally and should not be instantiated directly.

- Inherited from [RwsClientBase](underautomation.abb.rws.internal.md#rwsclientbase-robotrws): `disconnect`, `ip`, `port`, `use_https`, `timeout`, `enabled`, `version`, `file`, `controller`, `io`, `elog`, `system`, `panel`, `motion_system`, `mastership`, `rapid`

## RwsConnectParametersBase

`from underautomation.abb.rws.internal.rws_connect_parameters_base import RwsConnectParametersBase`

Base class for connection parameters. Contains core properties needed for RWS connection.

- `port: int`: RWS service port (if set to 0, the SDK will use 80 for HTTP, 443 for HTTPS)
- `username: str`: Username for Digest Authentication (Default is "Default User")
- `password: str`: Password for Digest Authentication (Default is "robotics")
- `timeout: int`: HTTP request timeout in milliseconds (default: 1000ms)
- `use_https: bool`: Whether to use HTTPS instead of HTTP (default: false)
- `version: RwsVersion`: RWS protocol version to use. If not specified, OmniCore_V2_0 (RWS 2.0) is used. RWS 2.0 is available in RobotWare >= 7, which ships the new OmniCore controller generation. For older RobotWare versions running on IRC5 controllers, use (RWS 1.0).
