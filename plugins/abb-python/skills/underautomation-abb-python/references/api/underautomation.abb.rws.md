# underautomation.abb.rws

## RwsClient

`from underautomation.abb.rws.rws_client import RwsClient`

Standalone public RWS client for ABB robot controllers. Supports both RWS v1 and v2. Use this class when you want to connect to a robot without using the AbbController class.

- `RwsClient()`: Create a new RWS client instance
- `connect(ip: str, username: str="Default User", password: str="robotics", port: int=0, timeout: int=10000, useHttps: bool=False, version: RwsVersion=RwsVersion.OmniCore_V2_0) -> None`: Connect to the robot controller RWS service
- Inherited from [RwsClientBase](underautomation.abb.rws.internal.md#rwsclientbase-robotrws): `disconnect`, `ip`, `port`, `use_https`, `timeout`, `enabled`, `version`, `file`, `controller`, `io`, `elog`, `system`, `panel`, `motion_system`, `mastership`, `rapid`

## RwsConnectParameters

`from underautomation.abb.rws.rws_connect_parameters import RwsConnectParameters`

Connection parameters for ABB Robot Web Services (RWS). Supports both RWS v1 and v2.

- `RwsConnectParameters()`
- `enable: bool`: Enable or disable the RWS client connection
- `static DEFAULT_PORT: int`: Default RWS port (80 for HTTP, 443 for HTTPS)
- `static DEFAULT_USERNAME: str`: Default username for Digest Authentication
- `static DEFAULT_PASSWORD: str`: Default password for Digest Authentication
- `static DEFAULT_TIMEOUT: int`: Default timeout in milliseconds
- Inherited from [RwsConnectParametersBase](underautomation.abb.rws.internal.md#rwsconnectparametersbase): `port`, `username`, `password`, `timeout`, `use_https`, `version`

## RwsException

`from UnderAutomation.ABB.Rws import RwsException`

Exception thrown when an RWS API request fails. Compatible with RWS v1 and v2.

The SDK raises this .NET type: catch it with `except RwsException as e` after the import above. Its members keep their .NET names. The class `RwsException` of the module `underautomation.abb.rws.rws_exception` is not a Python exception and cannot be caught.

- `ResponseBody: str (read only)`: Raw response body from the server, if available
- `StatusCode: int | None (read only)`: HTTP status code returned by the server
- `ReasonPhrase: str (read only)`: HTTP reason phrase returned by the server (e.g. "Forbidden", "Method Not Allowed"), if available
- `RwsErrorCode: str (read only)`: ABB internal error code extracted from the RWS error payload (e.g. "-1073445865"), if present
- `RwsErrorMessage: str (read only)`: Human readable error text extracted from the RWS error payload, if present
- Inherited from System.Exception: `Message`, `InnerException`

## RwsVersion (robot.rws.version)

`from underautomation.abb.rws.rws_version import RwsVersion`

Version of the ABB Robot Web Services (RWS) protocol exposed by the robot controller. The two versions differ in URL shapes, parameter placement and media types, so the client has to know which one it talks to. Pick the value that matches the controller generation.

- Irc5_V1_0: RWS 1.0, exposed by IRC5 controllers running RobotWare 6 and earlier.
- OmniCore_V2_0: RWS 2.0, exposed by OmniCore controllers running RobotWare 7 and later. This is the default when no version is specified.
