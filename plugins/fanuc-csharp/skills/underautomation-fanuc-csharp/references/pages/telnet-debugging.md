# Debugging & breakpoints

Add, remove, and manage breakpoints on TP and Karel programs. Step through code line by line using Telnet KCL.

Web page: https://underautomation.com/fanuc/documentation/telnet-debugging

> **Telnet KCL is a legacy protocol.** It is not secured: the password and the commands are sent in clear text. It is hard to maintain: the answers of the controller change with the firmware version, and ROBOGUIDE behaves differently from a real controller. The KCL commands of `robot.Telnet` are also available with `robot.Cgtp.Kcl`, through the web server of the controller (firmware V8.30 and later), without Telnet setup. Prefer it for new developments: see [KCL commands over CGTP](cgtp-kcl.md).

The Fanuc SDK lets you add, remove, and manage breakpoints on TP and Karel programs. It can also run a program line by line, for remote debugging or for a custom TP editor.

## Breakpoints

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class TelnetDebuggingBreakpoints
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Telnet.Enable = true;
        parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
        robot.Connect(parameters);

        // Add a breakpoint at line 10
        robot.Telnet.AddBreakpoint("MyProgram", 10);

        // List breakpoints
        BreakpointsResult result = robot.Telnet.GetBreakpoints("MyProgram");
        foreach (Breakpoint bp in result.Breakpoints)
        {
            Console.WriteLine($"Breakpoint at line {bp.Line}");
        }

        // Remove a single breakpoint
        robot.Telnet.RemoveBreakpoint("MyProgram", 10);

        // Remove all breakpoints of a program
        robot.Telnet.RemoveAllBreakpoints("MyProgram");
    }
}
```

## Step-by-step execution and task info

When step mode is enabled, the program pauses after each line execution, allowing you to inspect state between instructions.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class TelnetDebuggingStep
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Telnet.Enable = true;
        parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
        robot.Connect(parameters);

        // Enable step mode for a task
        robot.Telnet.StepOn("MyProgram");

        // Disable step mode
        robot.Telnet.StepOff();

        // Get task information (current line, status, etc.)
        TaskInformationResult info = robot.Telnet.GetTaskInformation("MyProgram");
    }
}
```

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class TelnetDebugging
{
  static void Main()
  {
    FanucRobot robot = new FanucRobot();
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Telnet.Enable = true;
    parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
    robot.Connect(parameters);

    // Add a breakpoint at line 10 of MyProgram
    robot.Telnet.AddBreakpoint("MyProgram", 10);

    // List all breakpoints
    BreakpointsResult result = robot.Telnet.GetBreakpoints("MyProgram");
    foreach (Breakpoint bp in result.Breakpoints)
    {
      Console.WriteLine($"Breakpoint at line {bp.Line}");
    }

    // Remove a single breakpoint
    robot.Telnet.RemoveBreakpoint("MyProgram", 10);

    // Remove all breakpoints
    robot.Telnet.RemoveAllBreakpoints("MyProgram");

    // Enable step-by-step execution
    robot.Telnet.StepOn("MyProgram");

    // Disable step mode
    robot.Telnet.StepOff();
  }
}
```

## See also

- [TP editor with breakpoints](tp-editor-with-breakpoints.md) : Build a custom TP editor with syntax highlighting and breakpoints

## API reference

**BreakpointsResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#breakpointsresult))

- `BreakpointsResult()`
- `Breakpoint[] Breakpoints { get; }`: Gets the breakpoints set on the task.
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

**Breakpoint** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#breakpoint))

- `Breakpoint()`
- `int Line { get; }`: Gets the line number where the breakpoint is set.

**AddBreakpointResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#addbreakpointresult))

- `AddBreakpointResult()`
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

**RemoveBreakpointResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#removebreakpointresult))

- `RemoveBreakpointResult()`
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

**StepOnResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#steponresult))

- `StepOnResult()`
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

**TaskInformationResult** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#taskinformationresult))

- `TaskInformationResult()`
- `int CurrentLine { get; }`: Gets the current line number.
- `string HoldConditions { get; }`: Gets the hold conditions.
- `bool InvisibleTask { get; }`: Gets a value indicating whether the task is invisible.
- `ProgramType ProgramType { get; }`: Gets the type of the program.
- `string RoutineName { get; }`: Gets the name of the routine.
- `bool SystemTask { get; }`: Gets a value indicating whether the task is a system task.
- `string TaskName { get; }`: Gets the name of the task.
- `int TaskNumber { get; }`: Gets the task number.
- `TaskStatus TaskStatus { get; }`: Gets the task status.
- `string TaskStatusStr { get; }`: Gets the task status as a string.
- Inherited from [Result](../api/UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`
