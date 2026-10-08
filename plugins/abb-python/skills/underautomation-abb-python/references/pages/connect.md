# Connect to your robot

Configure the connection to an IRC5 or OmniCore controller, choose the Robot Web Services version, and use the synchronous or asynchronous API.

Web page: https://underautomation.com/abb/documentation/connect

The SDK talks to the robot controller over Robot Web Services (RWS), the HTTP interface that ABB controllers expose on the network. Nothing has to be installed on the robot.

Two classes can open a connection:

- `AbbController` : the main entry point. It holds the connection parameters and gives access to every protocol.
- `RwsClient` : a standalone RWS client, when you only need RWS and prefer a smaller object.

## Quick connection

Pass an IP address and you are connected. The default parameters match an OmniCore controller with its factory user account.

```python
from underautomation.abb.abb_controller import AbbController

# Connect to an OmniCore controller with the default RWS parameters
robot = AbbController()
robot.connect("192.168.0.1")

# Every RWS service is reachable from robot.rws
print(robot.rws.controller.get_identity().name)

robot.disconnect()
```

Do not know the address yet? [Discover the controllers of the network](discover-controllers.md) instead of typing one.

## Full connection parameters

`ConnectionParameters` gives access to every option. Use it when the controller is not on its default port, uses HTTPS, or runs RobotWare 6.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.connection_parameters import ConnectionParameters
from underautomation.abb.rws.rws_version import RwsVersion

parameters = ConnectionParameters("192.168.0.1")

# Ping the controller first, so an unreachable robot fails immediately
parameters.ping_before_connect = True

parameters.rws.enable = True
parameters.rws.username = "Default User"
parameters.rws.password = "robotics"
parameters.rws.use_https = False
parameters.rws.port = 0  # 0 means 80 for HTTP and 443 for HTTPS
parameters.rws.timeout = 10000
parameters.rws.version = RwsVersion.OmniCore_V2_0

robot = AbbController()
robot.connect(parameters)

robot.disconnect()
```

When `PingBeforeConnect` is `true` (default), the SDK sends an ICMP ping before the first HTTP request. An unreachable robot then fails in a few milliseconds instead of waiting for the HTTP timeout. Set it to `false` when ICMP is blocked on your network.

The default user account of an ABB controller is `Default User` with the password `robotics`. Change it if your controller uses a dedicated account. The account must have the User Authorization System (UAS) grants for what you want to do: reading is always allowed, writing needs the matching grant.

## IRC5 or OmniCore

One API covers the two generations of controllers. Only the `Version` property changes.

| Controller | RobotWare     | RWS version | `RwsVersion` value |
| ---------- | ------------- | ----------- | ------------------ |
| IRC5       | 6 and earlier | RWS 1.0     | `Irc5_V1_0`        |
| OmniCore   | 7 and later   | RWS 2.0     | `OmniCore_V2_0`    |

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.connection_parameters import ConnectionParameters
from underautomation.abb.rws.rws_version import RwsVersion

# IRC5 controller, RobotWare 6 : RWS 1.0
irc5 = ConnectionParameters("192.168.0.1")
irc5.rws.version = RwsVersion.Irc5_V1_0

# OmniCore controller, RobotWare 7 : RWS 2.0
omni_core = ConnectionParameters("192.168.0.2")
omni_core.rws.version = RwsVersion.OmniCore_V2_0

# use_https is independent of the version. Set it to match how this
# particular controller is configured on the network, not its generation.
omni_core.rws.use_https = True

robot = AbbController()
robot.connect(omni_core)

# The same code then works on both controllers
print(robot.rws.system.get_info().version)
```

`OmniCore_V2_0` is the default. If you connect to an IRC5 without setting the version, the first request fails with a 404 status code.

`UseHttps` is a separate setting from `Version`. Both generations can be configured for HTTP or for HTTPS, this depends on how the controller itself is set up, not on which RWS version it speaks. Check your controller's own network configuration and set `UseHttps` to match. When the controller answers on HTTPS with a self-signed certificate, the SDK accepts it, you do not have to install anything in the certificate store.

The details of both versions are described in [IRC5 or OmniCore: which RWS version](irc5-vs-omnicore.md).

## Standalone RWS client

`RwsClient` connects without `AbbController`. The services are then directly on the client, `client.Controller` instead of `robot.Rws.Controller`.

```python
from underautomation.abb.rws.rws_client import RwsClient
from underautomation.abb.rws.rws_version import RwsVersion

# RwsClient talks to the controller without going through AbbController
client = RwsClient()
client.connect("192.168.0.1", "Default User", "robotics", 0, 10000, False, RwsVersion.OmniCore_V2_0)

print(client.controller.get_identity().name)

client.disconnect()
```

## Synchronous and asynchronous

Every service method exists twice: a synchronous version, and an asynchronous one with the same name followed by `Async` and an optional `CancellationToken`.



The asynchronous methods are not available on .NET Framework 3.5 and 4.0, which have no `async` / `await`. Everything else in the SDK works on those versions.

## Errors

Every RWS failure is reported as an `RwsException`. It carries the HTTP status code and, when the controller sends one, the ABB error code and message.

```python
from underautomation.abb.abb_controller import AbbController
from UnderAutomation.ABB.Rws import RwsException

robot = AbbController()
robot.connect("192.168.0.1")

try:
    robot.rws.panel.set_speed_ratio(50)
except RwsException as ex:
    # The exception comes from the .NET runtime, so its members keep their original names
    # StatusCode is the HTTP status returned by the controller
    # 403 usually means that another client holds the mastership
    print(f"RWS error {ex.StatusCode} : {ex.RwsErrorMessage}")
    print(f"ABB error code : {ex.RwsErrorCode}")
    print(f"Raw response : {ex.ResponseBody}")
```

Common status codes:

| Status | Meaning                                                                                                           |
| ------ | ----------------------------------------------------------------------------------------------------------------- |
| 400    | The controller refused the value, for example a speed ratio out of range                                          |
| 403    | Another client holds the [mastership](rws-mastership.md), or the user account lacks the UAS grant |
| 404    | The resource does not exist on this controller, often a wrong `RwsVersion`                                        |
| 500    | The controller could not run the operation in its current state                                                   |

## Disconnect

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Always disconnect : the controller keeps a limited number of sessions open
robot.disconnect()

print(robot.enabled)  # False
```

A controller accepts a limited number of simultaneous sessions, around 70 on OmniCore. An application that connects in a loop without disconnecting exhausts them, and every following request answers 503.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**ConnectionParameters** ([reference](../api/underautomation.abb.md#connectionparameters))

- `ConnectionParameters(address: str)`: Instantiate new connection parameters with a specified address
- `address: str`: Address of the robot controller (IP or host name), default value is 127.0.0.1
- `ping_before_connect: bool`: Send a ping command before initializing any connections
- `rws: RwsConnectParameters`: RWS2 (Robot Web Services 2) connection parameters

**RwsConnectParameters** ([reference](../api/underautomation.abb.rws.md#rwsconnectparameters))

- `RwsConnectParameters()`
- `enable: bool`: Enable or disable the RWS client connection
- `static DEFAULT_PORT: int`: Default RWS port (80 for HTTP, 443 for HTTPS)
- `static DEFAULT_USERNAME: str`: Default username for Digest Authentication
- `static DEFAULT_PASSWORD: str`: Default password for Digest Authentication
- `static DEFAULT_TIMEOUT: int`: Default timeout in milliseconds
- Inherited from [RwsConnectParametersBase](../api/underautomation.abb.rws.internal.md#rwsconnectparametersbase): `port`, `username`, `password`, `timeout`, `use_https`, `version`

**RwsConnectParametersBase** ([reference](../api/underautomation.abb.rws.internal.md#rwsconnectparametersbase))

- `port: int`: RWS service port (if set to 0, the SDK will use 80 for HTTP, 443 for HTTPS)
- `username: str`: Username for Digest Authentication (Default is "Default User")
- `password: str`: Password for Digest Authentication (Default is "robotics")
- `timeout: int`: HTTP request timeout in milliseconds (default: 1000ms)
- `use_https: bool`: Whether to use HTTPS instead of HTTP (default: false)
- `version: RwsVersion`: RWS protocol version to use. If not specified, OmniCore_V2_0 (RWS 2.0) is used. RWS 2.0 is available in RobotWare >= 7, which ships the new OmniCore controller generation. For older RobotWare versions running on IRC5 controllers, use (RWS 1.0).

**RwsVersion** ([reference](../api/underautomation.abb.rws.md#rwsversion-robotrwsversion))

- Irc5_V1_0: RWS 1.0, exposed by IRC5 controllers running RobotWare 6 and earlier.
- OmniCore_V2_0: RWS 2.0, exposed by OmniCore controllers running RobotWare 7 and later. This is the default when no version is specified.

**RwsException** ([reference](../api/underautomation.abb.rws.md#rwsexception))

- `ResponseBody: str (read only)`: Raw response body from the server, if available
- `StatusCode: int | None (read only)`: HTTP status code returned by the server
- `ReasonPhrase: str (read only)`: HTTP reason phrase returned by the server (e.g. "Forbidden", "Method Not Allowed"), if available
- `RwsErrorCode: str (read only)`: ABB internal error code extracted from the RWS error payload (e.g. "-1073445865"), if present
- `RwsErrorMessage: str (read only)`: Human readable error text extracted from the RWS error payload, if present
- Inherited from System.Exception: `Message`, `InnerException`
