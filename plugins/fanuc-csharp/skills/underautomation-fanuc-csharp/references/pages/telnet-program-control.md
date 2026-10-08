# Program control via Telnet

Run, pause, hold, continue, and abort TP and Karel programs remotely using Telnet KCL commands.

Web page: https://underautomation.com/fanuc/documentation/telnet-program-control

> **Telnet KCL is a legacy protocol.** It is not secured: the password and the commands are sent in clear text. It is hard to maintain: the answers of the controller change with the firmware version, and ROBOGUIDE behaves differently from a real controller. The KCL commands of `robot.Telnet` are also available with `robot.Cgtp.Kcl`, through the web server of the controller (firmware V8.30 and later), without Telnet setup. Prefer it for new developments: see [KCL commands over CGTP](cgtp-kcl.md).

Run, pause, hold, continue, and abort TP and Karel programs remotely using Telnet KCL commands.

## Run, pause, hold, continue

```csharp
using UnderAutomation.Fanuc;

public class TelnetProgramControlRun
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Telnet.Enable = true;
        parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
        robot.Connect(parameters);

        // Run the default program
        robot.Telnet.Run();

        // Run a specific program
        robot.Telnet.Run("MyProgram");

        // Pause a running program (stops at the next fine point)
        robot.Telnet.Pause("MyProgram");

        // Force pause immediately
        robot.Telnet.Pause("MyProgram", force: true);

        // Hold a program (stops at the current position)
        robot.Telnet.Hold("MyProgram");

        // Resume a paused or held program
        robot.Telnet.Continue("MyProgram");
    }
}
```

**Pause** stops at the next motion fine point. **Hold** decelerates the robot to stop at the current position.

## Abort, clear, and reset

```csharp
using UnderAutomation.Fanuc;

public class TelnetProgramControlAbort
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Telnet.Enable = true;
        parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
        robot.Connect(parameters);

        // Abort a specific program
        robot.Telnet.Abort("MyProgram", force: true);

        // Abort all running programs
        robot.Telnet.AbortAll(force: true);

        // Clear all programs from memory
        robot.Telnet.ClearAll();

        // Clear a specific program
        robot.Telnet.ClearProgram("MyProgram");

        // Clear variables of a specific program
        robot.Telnet.ClearVars("MyProgram");

        // Reset alarms and re-enable servo power
        robot.Telnet.Reset();
    }
}
```

The `Reset()` command has the same effect as the FAULT RESET button on the operator panel. The error message remains displayed if the error condition still exists.

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class TelnetProgramControl
{
  static void Main()
  {
    FanucRobot robot = new FanucRobot();
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Telnet.Enable = true;
    parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
    robot.Connect(parameters);

    // Run a program
    robot.Telnet.Run("MyProgram");

    // Pause (stops at next fine point)
    robot.Telnet.Pause("MyProgram");

    // Hold (decelerates and stops at current position)
    robot.Telnet.Hold("MyProgram");

    // Resume a paused or held program
    robot.Telnet.Continue("MyProgram");

    // Abort a program
    robot.Telnet.Abort("MyProgram", force: true);

    // Abort all running programs
    robot.Telnet.AbortAll(force: true);

    // Reset alarms (same as FAULT RESET button)
    robot.Telnet.Reset();

    // Clear program variables
    robot.Telnet.ClearVars("MyProgram");
  }
}
```

## API reference

**RunResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#runresult))

- `RunResult()`
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

**ProgramCommandResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#programcommandresult))

- `ProgramCommandResult()`
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`
