# Connect to your robot

Connect to a CS8 or CS9 controller over its SOAP server: network, port, user and password, connection parameters, errors and disconnection.

Web page: https://underautomation.com/staubli/documentation/connect

This page explains how to connect the SDK to a Staubli CS8 or CS9 controller: the settings of the controller, the connection parameters, the errors and the disconnection. The SDK uses the SOAP server of the controller over TCP/IP. Nothing is installed on the controller.

## Prerequisites

- The PC reaches the controller on the network. Its address is shown in the network settings of the controller, on the pendant.
- The SOAP server of the controller answers on its port, 851 by default. Staubli Robotics Suite uses the same server: if Staubli Robotics Suite connects to the controller, the SDK can connect too.
- A user of the controller, with its password. The rights of this user limit what the SDK can do, as for a person on the pendant.
- To power the arm and move it, the controller must be in remote mode.

## Quick connection

Pass the address of the controller. The other parameters keep their default values.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()

# Default parameters: SOAP port 851, user "default", password "default"
controller.connect("192.168.0.254")

connected = controller.enabled

controller.disconnect()
```

`StaubliController` gives access to every function of the SDK, through its `Soap` property, and to the files of the controller through its `File` property (see [Files overview](files-overview.md)).

## Connection parameters

`ConnectionParameters` holds every option. Use it when the controller has another port, user or password.

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.connection_parameters import ConnectionParameters

parameters = ConnectionParameters("192.168.0.254")

# Ping the controller first, so an unreachable controller fails in 100 ms
parameters.ping_before_connect = True

parameters.soap.enable = True
# 0 (default): automatic, 851 on a real controller (SoapConnectParameters.DEFAULT_PORT)
parameters.soap.port = 0
parameters.soap.user = "default"
parameters.soap.password = "default"

controller = StaubliController()
controller.connect(parameters)

controller.disconnect()
```

| Parameter           | Default     | Meaning                                                                 |
| ------------------- | ----------- | ----------------------------------------------------------------------- |
| `Address`           | none        | IP address or host name of the controller. For the emulator of Staubli Robotics Suite, the path of the `.controller` file of the emulated controller (see [the emulator](simulator.md)) |
| `PingBeforeConnect` | `true`      | Send a ping first. The connection fails if there is no answer in 100 ms |
| `Soap.Enable`       | `true`      | Open the SOAP session                                                   |
| `Soap.Port`         | `0`         | TCP port of the SOAP server. `0`: automatic, 851 on a real controller (`SoapConnectParameters.DEFAULT_PORT`), port of the configuration of an emulated controller |
| `Soap.User`         | `"default"` | User of the controller                                                  |
| `Soap.Password`     | `"default"` | Password of this user                                                   |
| `File.Enable`       | `false`     | Connect the file client. The other `File` parameters are on [Files overview](files-overview.md) |

Set `PingBeforeConnect` to `false` when a firewall blocks ICMP between the PC and the controller.

The address `localhost` is replaced by `127.0.0.1`, to avoid a slow name resolution.

## One controller, several robots

A controller can drive more than one arm. The methods that concern an arm take a `robot` argument: `0` is the first robot of `GetRobots()`. With one arm, always pass `0`. See [Controller and robots](soap-controller.md).

## Standalone SOAP client

`SoapClient` opens a SOAP session without `StaubliController`. The methods are then directly on the client: `soap.GetRobots()` instead of `controller.Soap.GetRobots()`.

```python
from underautomation.staubli.soap.soap_client import SoapClient
from underautomation.staubli.common.soap_connect_parameters import SoapConnectParameters

# A SOAP client without StaubliController
soap = SoapClient()
soap.connect("192.168.0.254", "default", "default", SoapConnectParameters.DEFAULT_PORT)

# The services are directly on the client
joints = soap.get_current_joint_position(0)

soap.disconnect()
```

## Errors

```python
from underautomation.staubli.staubli_controller import StaubliController
from UnderAutomation.Staubli.License import InvalidLicenseException
from UnderAutomation.Staubli.Soap.Errors import CustomSoapException, SoapErrorCode
from System.Net import WebException

controller = StaubliController()

# The exceptions come from the .NET runtime, so their members keep their original names
try:
    controller.connect("192.168.0.254")
    controller.soap.task_kill("myTask", "Disk://myProject/myProject.pjx")
except InvalidLicenseException as ex:
    # No valid license: the trial is over, or the key is wrong
    print(ex.LicenseInfo)
except CustomSoapException as ex:
    if ex.ErrorCode == SoapErrorCode.InvalidCredentials:
        print("Wrong user or password")
    else:
        # The controller refused the request
        print(f"{ex.ErrorCode} : {ex.Description}")
except WebException as ex:
    # No answer on the SOAP port
    print(ex.Message)
except Exception as ex:
    # For example, no answer to the ping
    print(ex)
```

| Exception                   | When                                                                                                       |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `InvalidLicenseException`   | `Connect` is called without a valid license. See [Licensing](license.md)               |
| `CustomSoapException`       | The controller refused the request. `ErrorCode` gives the reason, `Description` the text of the controller |
| `WebException`              | No answer on the SOAP port, or a network error                                                             |
| `ArgumentException`         | The address is a path but not a `.controller` file                                                         |
| `FileNotFoundException`     | The address is a `.controller` file that does not exist                                                    |
| `InvalidOperationException` | A method is called before `Connect`, or after `Disconnect`                                                 |
| `Exception`                 | No answer to the ping                                                                                      |

Frequent values of `CustomSoapException.ErrorCode`:

| `SoapErrorCode`        | Meaning                                                      |
| ---------------------- | ------------------------------------------------------------ |
| `InvalidCredentials`   | Wrong user or password                                       |
| `InvalidSessionIdCode` | The session has expired: connect again                       |
| `InvalidRobotIdCode`   | The `robot` argument does not match a robot of `GetRobots()` |
| `WriteAccessErrorCode` | The user has no right to change this                         |
| `ApplicationNotFound`  | No VAL 3 application with this name                          |
| `TaskNotFound`         | No task with this name and this creator                      |

## Disconnect

`Disconnect` closes the session on the controller. Call it when your application ends, or when it no longer needs the controller.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

try:
    joints = controller.soap.get_current_joint_position(0)
finally:
    # Close the session on the controller
    controller.disconnect()
```

`Enabled` is `true` while the session is open.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**ConnectionParameters** ([reference](../api/underautomation.staubli.md#connectionparameters))

- `ConnectionParameters(address: str)`: Instanciate a new connection parameters with a specified address
- `address: str`: Address of the robot: IP or host name of a real controller. For a controller emulated by Staubli Robotics Suite, path of the .controller file of the controller in the cell (for example C:\...\MyCell\Controller1\Controller1.controller): the SOAP client then connects to the local computer, and the...
- `ping_before_connect: bool`: Send a ping command before initializing any connections
- `soap: SoapConnectParameters`: Soap connection parameters
- `file: FileConnectParameters`: File client connection parameters (upload, download, listing and management of the files of the controller)

**SoapConnectParameters** ([reference](../api/underautomation.staubli.common.md#soapconnectparameters))

- `SoapConnectParameters()`
- `enable: bool`: Should use this service (default: true)
- `static DEFAULT_PORT: int`: Default port of the SOAP server of a real controller (851), used when Port is 0
- Inherited from [SoapConnectParametersBase](../api/underautomation.staubli.soap.internal.md#soapconnectparametersbase): `user`, `password`, `port`

**SoapConnectParametersBase** ([reference](../api/underautomation.staubli.soap.internal.md#soapconnectparametersbase))

- `SoapConnectParametersBase()`
- `user: str`: Username for the SOAP service (default: default)
- `password: str`: Password for the SOAP service (default: default)
- `port: int`: Port of the SOAP service. Default: 0 (automatic). With 0, the SDK uses 851 for a real controller, and the SOAP port of the network configuration of a controller emulated by Staubli Robotics Suite (851 when it is not found).

**CustomSoapException** ([reference](../api/underautomation.staubli.soap.errors.md#customsoapexception))

- `ErrorCodeText: str (read only)`: The error code text as received from the SOAP response, formatted as a kebab-case string.
- `ErrorCode: SoapErrorCode (read only)`: The error code as an enum value, parsed from the ErrorCodeText.
- `Description: str (read only)`: A human-readable description of the error, providing additional context about the failure.
- `Message: str (read only)`: Gets the error message that describes the current exception.
- Inherited from System.Exception: `InnerException`

**SoapErrorCode** ([reference](../api/underautomation.staubli.soap.errors.md#soaperrorcode))

- Unknown: Unknown or unrecognized error code.
- InvalidCredentials: The provided credentials are invalid.
- TaskNotFound: The specified task was not found.
- MismatchedCode: Mismatched code error.
- ProgramNotFound: The specified program was not found.
- TaskAlreadyLocked: The task is already locked by another client.
- SinReturnCodeNok: SIN return code indicates failure.
- SchedulingModeError: Scheduling mode error.
- ApplicationNotFound: The specified application was not found.
- StackFrameNotFound: The specified stack frame was not found.
- ProgramLineNotFound: The specified program line was not found.
- ReadAccessErrorCode: Read access error.
- SetPosNotSimulCode: Cannot set position outside simulation mode.
- InvalidSessionIdCode: The session ID is invalid or expired.
- WriteAccessErrorCode: Write access error.
- CannotStartApplication: Cannot start the application.
- ClientAlreadyConnected: A client is already connected.
- IoWriteAccessErrorCode: I/O write access error.
- ClientCommunicationError: Client communication error.
- IoWriteAccessErrorValidation: I/O write access validation error.
- IoWriteAccessErrorWorkingMode: I/O write access error due to working mode.
- InvalidRobotIdCode: The specified robot ID is invalid.
