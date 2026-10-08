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

```csharp
using UnderAutomation.Staubli;

public class ConnectQuick
{
    static void Main()
    {
        var controller = new StaubliController();

        // Default parameters: SOAP port 851, user "default", password "default"
        controller.Connect("192.168.0.254");

        bool connected = controller.Enabled;

        controller.Disconnect();
    }
}
```

`StaubliController` gives access to every function of the SDK, through its `Soap` property, and to the files of the controller through its `File` property (see [Files overview](files-overview.md)).

## Connection parameters

`ConnectionParameters` holds every option. Use it when the controller has another port, user or password.

```csharp
using UnderAutomation.Staubli;

public class Connect
{
    static void Main()
    {
        var parameters = new ConnectionParameters("192.168.0.254");

        // Ping the controller first, so an unreachable controller fails in 100 ms
        parameters.PingBeforeConnect = true;

        parameters.Soap.Enable = true;
        // 0 (default): automatic, 851 on a real controller (SoapConnectParameters.DEFAULT_PORT)
        parameters.Soap.Port = 0;
        parameters.Soap.User = "default";
        parameters.Soap.Password = "default";

        var controller = new StaubliController();
        controller.Connect(parameters);

        controller.Disconnect();
    }
}
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

```csharp
using UnderAutomation.Staubli.Common;
using UnderAutomation.Staubli.Soap;

public class ConnectStandalone
{
    static void Main()
    {
        // A SOAP client without StaubliController
        var soap = new SoapClient();
        soap.Connect("192.168.0.254", "default", "default", SoapConnectParameters.DEFAULT_PORT);

        // The services are directly on the client
        double[] joints = soap.GetCurrentJointPosition(robot: 0);

        soap.Disconnect();
    }
}
```

## Errors

```csharp
using System.Net;
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.License;
using UnderAutomation.Staubli.Soap.Errors;

public class ConnectErrors
{
    static void Main()
    {
        var controller = new StaubliController();

        try
        {
            controller.Connect("192.168.0.254");
            controller.Soap.TaskKill("myTask", "Disk://myProject/myProject.pjx");
        }
        catch (InvalidLicenseException ex)
        {
            // No valid license: the trial is over, or the key is wrong
            Console.WriteLine(ex.LicenseInfo);
        }
        catch (CustomSoapException ex) when (ex.ErrorCode == SoapErrorCode.InvalidCredentials)
        {
            Console.WriteLine("Wrong user or password");
        }
        catch (CustomSoapException ex)
        {
            // The controller refused the request
            Console.WriteLine($"{ex.ErrorCode} : {ex.Description}");
        }
        catch (WebException ex)
        {
            // No answer on the SOAP port
            Console.WriteLine(ex.Message);
        }
        catch (Exception ex)
        {
            // For example, no answer to the ping
            Console.WriteLine(ex.Message);
        }
    }
}
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

```csharp
using UnderAutomation.Staubli;

public class ConnectDisconnect
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        try
        {
            double[] joints = controller.Soap.GetCurrentJointPosition(robot: 0);
        }
        finally
        {
            // Close the session on the controller
            controller.Disconnect();
        }
    }
}
```

`Enabled` is `true` while the session is open.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**ConnectionParameters** ([reference](../api/UnderAutomation.Staubli.md#connectionparameters))

- `ConnectionParameters()`: Instanciate a new connection parameters
- `ConnectionParameters(string address)`: Instanciate a new connection parameters with a specified address
- `string Address { get; set; }`: Address of the robot: IP or host name of a real controller. For a controller emulated by Staubli Robotics Suite, path of the .controller file of the controller in the cell (for example C:\...\MyCell\Controller1\Controller1.controller): the SOAP client then connects to the local computer, and the...
- `FileConnectParameters File { get; set; }`: File client connection parameters (upload, download, listing and management of the files of the controller)
- `bool PingBeforeConnect { get; set; }`: Send a ping command before initializing any connections
- `SoapConnectParameters Soap { get; set; }`: Soap connection parameters

**SoapConnectParameters** ([reference](../api/UnderAutomation.Staubli.Common.md#soapconnectparameters))

- `SoapConnectParameters()`
- `const int DEFAULT_PORT = 851`: Default port of the SOAP server of a real controller (851), used when Port is 0
- `bool Enable { get; set; }`: Should use this service (default: true)
- Inherited from [SoapConnectParametersBase](../api/UnderAutomation.Staubli.Soap.Internal.md#soapconnectparametersbase): `User`, `Password`, `Port`

**SoapConnectParametersBase** ([reference](../api/UnderAutomation.Staubli.Soap.Internal.md#soapconnectparametersbase))

- `SoapConnectParametersBase()`
- `string Password { get; set; }`: Password for the SOAP service (default: default)
- `int Port { get; set; }`: Port of the SOAP service. Default: 0 (automatic). With 0, the SDK uses 851 for a real controller, and the SOAP port of the network configuration of a controller emulated by Staubli Robotics Suite (851 when it is not found).
- `string User { get; set; }`: Username for the SOAP service (default: default)

**CustomSoapException** ([reference](../api/UnderAutomation.Staubli.Soap.Errors.md#customsoapexception))

- `string Description { get; }`: A human-readable description of the error, providing additional context about the failure.
- `SoapErrorCode ErrorCode { get; }`: The error code as an enum value, parsed from the ErrorCodeText.
- `string ErrorCodeText { get; }`: The error code text as received from the SOAP response, formatted as a kebab-case string.
- `string Message { get; }`: Gets the error message that describes the current exception.

**SoapErrorCode** ([reference](../api/UnderAutomation.Staubli.Soap.Errors.md#soaperrorcode))

- ApplicationNotFound: The specified application was not found.
- CannotStartApplication: Cannot start the application.
- ClientAlreadyConnected: A client is already connected.
- ClientCommunicationError: Client communication error.
- InvalidCredentials: The provided credentials are invalid.
- InvalidRobotIdCode: The specified robot ID is invalid.
- InvalidSessionIdCode: The session ID is invalid or expired.
- IoWriteAccessErrorCode: I/O write access error.
- IoWriteAccessErrorValidation: I/O write access validation error.
- IoWriteAccessErrorWorkingMode: I/O write access error due to working mode.
- MismatchedCode: Mismatched code error.
- ProgramLineNotFound: The specified program line was not found.
- ProgramNotFound: The specified program was not found.
- ReadAccessErrorCode: Read access error.
- SchedulingModeError: Scheduling mode error.
- SetPosNotSimulCode: Cannot set position outside simulation mode.
- SinReturnCodeNok: SIN return code indicates failure.
- StackFrameNotFound: The specified stack frame was not found.
- TaskAlreadyLocked: The task is already locked by another client.
- TaskNotFound: The specified task was not found.
- Unknown: Unknown or unrecognized error code.
- WriteAccessErrorCode: Write access error.
