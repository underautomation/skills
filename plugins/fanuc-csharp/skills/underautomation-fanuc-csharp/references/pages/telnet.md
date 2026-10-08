# Telnet overview

Telnet KCL (Keyboard Command Line) sends commands to a Fanuc robot: run programs, reset alarms, read and write variables, control I/O ports.

Web page: https://underautomation.com/fanuc/documentation/telnet

> **Telnet KCL is a legacy protocol.** It is not secured: the password and the commands are sent in clear text. It is hard to maintain: the answers of the controller change with the firmware version, and ROBOGUIDE behaves differently from a real controller. The KCL commands of `robot.Telnet` are also available with `robot.Cgtp.Kcl`, through the web server of the controller (firmware V8.30 and later), without Telnet setup. Prefer it for new developments: see [KCL commands over CGTP](cgtp-kcl.md).

Telnet KCL is a text-based protocol that lets you send commands to a Fanuc robot controller. It requires no paid option and is available on all controllers and ROBOGUIDE.

## Key features

- **Program control**: Run, pause, hold, continue, abort programs
- **Variable access**: Read and write system variables
- **I/O control**: Set output ports, simulate and unsimulate inputs
- **Alarm management**: Reset alarms and errors
- **Debugging**: Add breakpoints, step through code line by line
- **Custom commands**: Send any raw KCL command

## Prerequisites

Telnet must be enabled on your robot controller. See [Enable Telnet on your robot](telnet-enable-on-robot.md) for setup instructions.

## Quick example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

  public class Telnet
  {
    static void Main()
    {
      // Create a new Fanuc robot instance
      FanucRobot robot = new FanucRobot();

      // Set connection parameters
      ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
      parameters.Telnet.Enable = true;
      parameters.Telnet.TelnetKclPassword = "TELNET_PASS";

      // Connect to the robot
      robot.Connect(parameters);

      // Reset alarms
      robot.Telnet.Reset();

      // Run a program
      robot.Telnet.Run("MyProgram");
      robot.Telnet.Pause("MyProgram");
      robot.Telnet.Hold("MyProgram");
      robot.Telnet.Continue("MyProgram");
      robot.Telnet.Abort("MyProgram", force: true);

      // Set a variable
      robot.Telnet.SetVariable("$RMT_MASTER", 1);

      // Set an output port (example: DOUT port 2 = 0)
      robot.Telnet.SetPort(KCLPorts.DOUT, 2, 0);

      // Simulate an input port (example: DIN port 3 = 1)
      robot.Telnet.Simulate(KCLPorts.DIN, 3, 1);
      robot.Telnet.Unsimulate(KCLPorts.DIN, 3);
    }

  }
```

## Connection

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class TelnetConnection
{
    static void Main()
    {
        // Via FanucRobot
        var robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Telnet.Enable = true;
        parameters.Telnet.TelnetKclPassword = "your_password";
        robot.Connect(parameters);

        // Or standalone
        var telnet = new TelnetClient();
        telnet.Connect("192.168.0.1", "your_password");
    }
}
```

For ROBOGUIDE, pass the workcell folder path instead of an IP address. The SDK reads `services.txt` to find the correct Telnet port.

## Events

The Telnet client raises events for real-time monitoring:

- `MessageReceived` : Fired when a message is received from the controller
- `RawDataReceived` : Raw byte data from the TCP socket
- `ErrorOccured` : Connection or communication errors
- `CommandSent` / `CommandReceived` : Track sent and received KCL commands
- `TpCoordinatesReceived` : Teach pendant coordinate system changes

## Check if Telnet is available

Via FTP, you can check if Telnet is available on the controller:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common.Files.Diagnosis;

public class TelnetFeatures
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        Features features = robot.Ftp.GetSummaryDiagnostic().Features;
        bool isTelnetAvailable = features.HasTelnet;
    }
}
```

## Limitations

- **Text-based protocol**: Slower than binary protocols like SNPX for bulk data operations
- **Sequential commands**: Commands are sent one at a time over a single TCP connection
- **No bulk register read**: Variable reading is done by name, not by index. Use SNPX, FTP or CGTP for reading registers in bulk

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Next steps

- [Program control](telnet-program-control.md) : Run, pause, abort programs
- [Variables & I/O](telnet-variables-io.md) : Read/write variables and control ports
- [Debugging & breakpoints](telnet-debugging.md) : Step-by-step debugging

## API reference

**TelnetClient** ([reference](../api/UnderAutomation.Fanuc.Telnet.md#telnetclient))

- `TelnetClient()`: Create a new instance of a robot communication
- `void Connect(string ip, string telnetKclPassword)`: Connect to a robot
- Inherited from [TelnetClientBase](../api/UnderAutomation.Fanuc.Telnet.Internal.md#telnetclientbase-robottelnet): `PollAndGetUpdatedConnectedState`, `Disconnect`, `IP`, `Language`, `TpCoordinates`, `Connected`, `RawDataReceived`, `StringDataReceived`, `TpCoordinatesReceived`, `MessageReceived`, `ErrorOccured`, `CommandSent`, `CommandReceived`
- Inherited from [KclClientBase](../api/UnderAutomation.Fanuc.Common.Kcl.md#kclclientbase-robottelnet): `Abort`, `AbortAll`, `ClearAll`, `ClearProgram`, `ClearVars`, `Continue`, `Hold`, `Pause`, `Reset`, `Run`, `SetPort`, `SetVariable`, `GetCurrentPose`, `GetVariable`, `Simulate`, `UnsimulateAll`, `Unsimulate`, `SendCustomCommand`, `SendCustomCommand``1`, `GetTaskInformation`, `AddBreakpoint`, `RemoveBreakpoint`, `RemoveAllBreakpoints`, `GetBreakpoints`, `StepOn`, `StepOff`

**TelnetClientBase** ([reference](../api/UnderAutomation.Fanuc.Telnet.Internal.md#telnetclientbase-robottelnet))

- `event EventHandler<KclCommandReceived> CommandReceived`: Occurs when a KCL command is received.
- `event EventHandler<CommandSentEventArgs> CommandSent`: Occurs when a command is sent.
- `bool Connected { get; }`: Is Telnet client connected
- `void Disconnect()`: Disconnect Telnet client from robot
- `event EventHandler<KclClientErrorEventArgs> ErrorOccured`: Occurs when an error occurs in the KCL client.
- `string IP { get; }`: Connect robot IP address or host name
- `Languages Language { get; set; }`: Controller language (default is English)
- `event EventHandler<MessageReceivedEventArgs> MessageReceived`: Occurs when a message is received.
- `bool PollAndGetUpdatedConnectedState()`: Checks the actual connection status via an active socket polling
- `event EventHandler<RawDataReceivedEventArgs> RawDataReceived`: Occurs when raw data is received.
- `event EventHandler<RawDataReceivedEventArgs> StringDataReceived`: Occurs when data is received and its content can successfully be parsed as a string message.
- `TpCoordinates TpCoordinates { get; }`: Gets the current Teach Pendant coordinate system.
- `event EventHandler<TpCoordinatesReceivedEventArgs> TpCoordinatesReceived`: Occurs when TP coordinates are received.
- Inherited from [KclClientBase](../api/UnderAutomation.Fanuc.Common.Kcl.md#kclclientbase-robottelnet): `Abort`, `AbortAll`, `ClearAll`, `ClearProgram`, `ClearVars`, `Continue`, `Hold`, `Pause`, `Reset`, `Run`, `SetPort`, `SetVariable`, `GetCurrentPose`, `GetVariable`, `Simulate`, `UnsimulateAll`, `Unsimulate`, `SendCustomCommand`, `SendCustomCommand``1`, `GetTaskInformation`, `AddBreakpoint`, `RemoveBreakpoint`, `RemoveAllBreakpoints`, `GetBreakpoints`, `StepOn`, `StepOff`
