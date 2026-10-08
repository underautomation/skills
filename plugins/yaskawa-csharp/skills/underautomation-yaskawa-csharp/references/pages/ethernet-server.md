# Ethernet Server overview

The Ethernet Server of YRC1000 controllers over TCP: what the SDK does with it, how it compares with the High Speed Ethernet Server, connection, errors and units.

Web page: https://underautomation.com/yaskawa/documentation/ethernet-server

This page gives an overview of the Ethernet Server function of Yaskawa Motoman controllers (YRC1000, YRC1000micro), and of what the SDK does with it. The Ethernet Server is a second way to read and command the controller, over TCP, next to the [High Speed Ethernet Server](high-speed-ethernet-server.md).

## What is the Ethernet Server

The Ethernet Server is a function of the controller that answers commands of a PC over TCP. Its default port is 80, the port of the web server of the controller. The SDK opens one TCP connection for each command, sends it, reads the answer and closes the connection. There is no session to keep alive: a call made after a network cut works again as soon as the network is back.

The SDK gives you .NET objects. You do not build the messages. Nothing is installed on the controller and no job has to run.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerQuickTour
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;

        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // State of the controller
        HostControlStatusData status = robot.EServer.GetStatusInformation();
        Console.WriteLine($"Play: {status.Play}, remote: {status.CommandRemote}, servo: {status.ServoOn}");

        // Position of the robot, in mm and degrees
        HostControlCartesianPositionData tcp = robot.EServer.GetRobotCartesianPosition();
        Console.WriteLine($"X={tcp.X} Y={tcp.Y} Z={tcp.Z}");

        // Executing job
        HostControlJobData job = robot.EServer.GetExecutingJobInformation();
        Console.WriteLine($"Job {job.Name}, line {job.Line}");

        // Variables D000 to D003
        int[] d = robot.EServer.ReadDoubleInteger(0, 4);

        robot.Disconnect();
    }
}
```

## Ethernet Server or High Speed Ethernet Server

Both protocols read the state of the controller and command it. Most applications use the High Speed Ethernet Server. The Ethernet Server is useful in these cases:

| Need                                                        | Ethernet Server                                                                  | High Speed Ethernet Server                                      |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Transport                                                   | TCP, port 80                                                                     | UDP, ports 10040 and 10041                                      |
| A firewall lets only TCP through                            | Yes                                                                              | No                                                              |
| Read a status (measured on a YRC1000micro)                  | About 20 ms per call                                                             | About 10 ms per call                                            |
| Alarm texts                                                 | Error and 4 alarms, with code, sub code and text                                 | Up to 4 alarms with code, sub code, text and time               |
| Position in a user frame or in the tool frame               | Yes, `HostControlCoordinateSystem`                                               | Base frame. P variables in any frame                            |
| Wait for the end of a job                                   | `WaitForJobCompletion(seconds)`, one blocking call                               | Poll `GetStatusInformation().Running`                           |
| Job list, master job, job deletion                          | Yes                                                                              | Job list and deletion with the file functions                   |
| Encoder temperatures, maximum torque                        | Yes                                                                              | No                                                              |
| Position variables (P, BP, EX), registers, system variables | No                                                                               | Yes                                                             |
| File transfers                                              | No, use [FTP](ftp.md) or [HTTP](http.md) | Yes                                                             |

The two protocols can be used together: enable both in `ConnectParameters`, then call `robot.HighSpeedEServer` or `robot.EServer`. Code that must work with both can use the common interfaces, see [Choose a protocol](protocols.md#write_code_for_both_protocols).

## Topics

| Page                                                                    | What you can do                                                             |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [Status, alarms and servo](eserver-status.md)       | Read the state, read and reset alarms, servo, hold, cycle, mode, pendant    |
| [Positions and torque](eserver-positions.md)        | Joint pulses, Cartesian position in a frame, torque, encoder temperatures   |
| [Jobs](eserver-jobs.md)                             | List, select, start and wait for a job, master job, delete a job            |
| [Motion](eserver-motion.md)                         | Joint, linear and incremental moves, moves to a target in pulses            |
| [Variables and I/O](eserver-variables-io.md)        | B, I, D, R and S variables, read the I/O, write the network inputs          |

All these functions are methods of `robot.EServer` (`robot.e_server` in Python).

## Connect

### Prerequisites

- The PC reaches the controller on TCP port 80. A firewall between them must let this port through.
- The read methods work in any mode. The commands (servo, hold, jobs, moves, writes) need the remote mode, set as for the High Speed Ethernet Server: see [Prepare the controller](connect.md#prepare_the_controller).

### Enable the Ethernet Server

The Ethernet Server is disabled by default in `ConnectParameters`. Set `EServer.Enable` to `true`. The other protocols keep their own setting.

```csharp
using UnderAutomation.Yaskawa;

public class EServerConnect
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");

        // Only the Ethernet Server
        parameters.HighSpeedEServer.Enable = false;
        parameters.EServer.Enable = true;

        // TCP port of the Ethernet Server (default: 80)
        parameters.EServer.Port = 80;

        // Time to wait for an answer, in milliseconds
        parameters.EServer.TimeoutMilliseconds = 5000;          // most commands
        parameters.EServer.PowerOnTimeoutMilliseconds = 10000; // SetServo(true)
        parameters.EServer.MotionTimeoutMilliseconds = 30000;   // moves

        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        robot.Disconnect();
    }
}
```

| Parameter                            | Default | Meaning                                         |
| ------------------------------------ | ------- | ----------------------------------------------- |
| `EServer.Enable`                     | `false` | Open the Ethernet Server client                 |
| `EServer.Port`                       | `80`    | TCP port of the Ethernet Server                 |
| `EServer.TimeoutMilliseconds`        | `5000`  | Time to wait for the answer of a command        |
| `EServer.PowerOnTimeoutMilliseconds` | `10000` | Time to wait for the answer of `SetServo(true)` |
| `EServer.MotionTimeoutMilliseconds`  | `30000` | Time to wait for the answer of a move           |

### What "connected" means

Each command opens its own TCP connection. So `Connect` checks the license and the address, but does not exchange a message with the controller. The first method call is the first exchange. To check the link at startup, call a read method, for example `GetStatusInformation()`, right after `Connect`.

### Standalone client

`EServerClient` opens an Ethernet Server client without `YaskawaRobot`. The methods are then directly on the client.

```csharp
using UnderAutomation.Yaskawa.HostControl;

public class EServerStandalone
{
    static void Main()
    {
        // An Ethernet Server client without YaskawaRobot
        var client = new EServerClient();
        client.Connect("192.168.0.1");

        HostControlStatusData status = client.GetStatusInformation();
        Console.WriteLine($"Running: {status.Running}");

        client.Close();
    }
}
```

## Errors

When the controller refuses a command, the SDK throws a `HostControlException`. `Message` gives the reason in clear text, `ErrorCode` the code returned by the controller. A call made before `Connect` throws an `InvalidOperationException`.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerErrors
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        try
        {
            robot.EServer.StartJob("PICK");
        }
        catch (HostControlException ex)
        {
            // Message gives the reason, ErrorCode the code of the controller
            Console.WriteLine($"Refused: {ex.Message} (code {ex.ErrorCode})");
        }

        robot.Disconnect();
    }
}
```

Frequent reasons, and what to check:

| Reason                                    | Check                                                                               |
| ----------------------------------------- | ----------------------------------------------------------------------------------- |
| Command remote not set                    | The remote mode, see [Prepare the controller](connect.md#prepare_the_controller) |
| Servo off                                 | Call `SetServo(true)` first                                                         |
| Alarm or error                            | Read and reset the alarm, see [Alarms](eserver-status.md#alarms) |
| Hold by the pendant, by a signal, by a command | Release the hold                                                               |
| Incorrect mode                            | Play mode to start a job, teach mode for some commands                              |
| Argument out of range                     | The number of a variable, a signal or a frame does not exist on this controller     |

## Units

| Value                                  | Unit                                       |
| -------------------------------------- | ------------------------------------------ |
| Cartesian X, Y, Z                      | mm                                         |
| Cartesian Rx, Ry, Rz                   | degrees                                    |
| Joint positions and moves in pulses    | encoder pulses                             |
| Torque                                 | percent of the rated torque                |
| Encoder temperature                    | degrees Celsius                            |
| Speed of a joint move                  | percent of the maximum speed               |
| Speed of a linear move                 | percent, or mm/s, set by `HostControlSpeedType` |

## Reference

**EServerClient** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#eserverclient))

- `EServerClient()`: Creates a new instance of EServerClient for robot communication via TCP. Call Connect() to configure communication with a robot controller.
- `void Connect(string ip)`: Configures connection to the robot controller via TCP using default parameters.
- `void Connect(string ip, EServerConnectParameters parameters)`: Configures connection to the robot controller via TCP.
- Inherited from [EServerClientInternal](../api/UnderAutomation.Yaskawa.HostControl.Internal.md#eserverclientinternal-roboteserver): `Close`, `Connected`, `Address`, `Port`
- Inherited from [HostControlClientBase](../api/UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolclientbase-roboteserver): `GetAlarm`, `GetStatusInformation`, `GetExecutingJobInformation`, `GetControlGroup`, `GetRobotJointPosition`, `GetRobotCartesianPosition`, `SetHold`, `AlarmReset`, `ErrorCancel`, `SetMode`, `SetCycle`, `SetServo`, `SetTeachPendantLockState`, `Display`, `StartJob`, `SetControlGroup`, `SetTask`, `MoveJoint`, `MoveLinear`, `MoveIncremental`, `MovePulseJoint`, `MovePulseLinear`, `ReadIO`, `WriteIO`, `ReadByte`, `WriteByte`, `ReadInteger`, `WriteInteger`, `ReadDoubleInteger`, `WriteDoubleInteger`, `ReadReal`, `WriteReal`, `Read16BytesChar`, `Write16BytesChar`, `GetJobDirectory`, `GetUserFrame`, `SetUserFrame`, `DeleteJob`, `SetMasterJob`, `SelectJob`, `WaitForJobCompletion`, `ConvertToRelativeJob`, `ConvertToStandardJob`, `GetTorque`, `GetMaxTorque`, `GetEncoderTemperature`, `GetSystemTime`, `GetAbsoluteEncoderPosition`, `SetAbsoluteEncoderPosition`, `SetFrameType`, `GetAlarmWithMessages`

**EServerConnectParametersInternal** ([reference](../api/UnderAutomation.Yaskawa.HostControl.Internal.md#eserverconnectparametersinternal))

- `EServerConnectParametersInternal()`
- `bool Enable { get; set; }`: Gets or sets a value indicating whether to enable the Ethernet Server connection (default: false).
- Inherited from [EServerConnectParameters](../api/UnderAutomation.Yaskawa.HostControl.md#eserverconnectparameters): `DEFAULT_PORT`, `Port`
- Inherited from [HostControlConnectParametersBase](../api/UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolconnectparametersbase): `DEFAULT_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_MOTION_TIMEOUT_MILLISECONDS`, `TimeoutMilliseconds`, `PowerOnTimeoutMilliseconds`, `MotionTimeoutMilliseconds`

**EServerConnectParameters** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#eserverconnectparameters))

- `EServerConnectParameters()`: Initializes a new instance of the Ethernet Server connection parameters.
- `const int DEFAULT_PORT = 80`: Default TCP port for Ethernet Server communication (80).
- `int Port { get; set; }`: Gets or sets the TCP port number for Ethernet Server communication. Must match the robot controller's Ethernet Server port configuration. Default: 80.
- Inherited from [HostControlConnectParametersBase](../api/UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolconnectparametersbase): `DEFAULT_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_MOTION_TIMEOUT_MILLISECONDS`, `TimeoutMilliseconds`, `PowerOnTimeoutMilliseconds`, `MotionTimeoutMilliseconds`

**HostControlException** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolexception))

- `HostControlException(string message)`: Creates a new HostControlException with the specified message.
- `HostControlException(string message, Exception innerException)`: Creates a new HostControlException with the specified message and inner exception.
- `HostControlException(string message, string errorCode)`: Creates a new HostControlException with the specified message and error code.
- `HostControlException(string message, string command, string errorCode)`: Creates a new HostControlException with the specified message, command, and error code.
- `string Command { get; }`: Gets the command that caused the exception.
- `string ErrorCode { get; }`: Gets the error code returned by the robot controller.

## What to read next

- [Status, alarms and servo](eserver-status.md): the first commands to try.
- [Choose a protocol](protocols.md): HSES, Ethernet Server, HTTP and FTP side by side.
