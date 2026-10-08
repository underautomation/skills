# KCL commands

Send KCL commands through the web server instead of Telnet. Unsafe commands without result, and when to use RunProgram.

Web page: https://underautomation.com/fanuc/documentation/cgtp-kcl

`robot.Cgtp.Kcl` sends KCL commands (Karel Command Language) through the web server of the controller. It has the same methods and the same result types as the Telnet KCL client `robot.Telnet`, without the Telnet protocol.

Use it instead of Telnet KCL for new developments. Telnet KCL is a legacy protocol: it is not secured, and its behavior changes with the firmware version and on ROBOGUIDE.

## Why CGTP instead of Telnet

| | Telnet KCL (`robot.Telnet`) | KCL over CGTP (`robot.Cgtp.Kcl`) |
|---|---|---|
| Setup on the robot | Telnet password, J541 security level, special port on ROBOGUIDE | None, CGTP is enabled by default in the SDK |
| Security | Password and commands sent in clear text | Web server of the controller, optional HTTP authentication |
| Firmware | Answers change with the version and on ROBOGUIDE | V8.30 and later, V9.30 and later for the Unsafe commands |
| Result of the commands | Text answer of the controller for every command | No result for the Unsafe commands (see below) |

## Move from Telnet to CGTP

Replace `robot.Telnet` by `robot.Cgtp.Kcl`. The method names, the parameters and the result types do not change. You can remove the Telnet parameters of the connection.

```csharp
using UnderAutomation.Fanuc;

public class CgtpKclMigration
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();

        // CGTP is enabled by default: no Telnet password and no Telnet setup on the robot
        robot.Connect("192.168.0.1");

        // Before: robot.Telnet.SetVariable("$RMT_MASTER", 1);
        SetVariableResult result = robot.Cgtp.Kcl.SetVariable("$RMT_MASTER", 1);
        if (!result.Succeed)
        {
            Console.WriteLine(result.ErrorText);
        }

        // Before: robot.Telnet.GetTaskInformation("MY_PROGRAM");
        TaskInformationResult task = robot.Cgtp.Kcl.GetTaskInformation("MY_PROGRAM");
        Console.WriteLine($"{task.TaskStatus} at line {task.CurrentLine}");
    }
}
```

## Unsafe commands

Some KCL commands are sent in **Unsafe** mode through CGTP. The controller executes them but returns no status and no error. The result object always reports a success (`Succeed` is `true`, `ErrorText` is empty), even if the controller refused the command, for example because the program does not exist or because the device has no motion control.

These commands need firmware **V9.30** or later:

| Method | Action |
|---|---|
| `Run` | Start a program |
| `Pause` | Pause a program |
| `Hold` | Hold a program |
| `Continue` | Resume a paused or held program |
| `Abort`, `AbortAll` | Abort one or all tasks |
| `ClearProgram`, `ClearVars` | Clear a program or its variables from memory |
| `StepOn`, `StepOff` | Enable or disable the step mode |
| `SendCustomCommandUnsafe` | Send any KCL command without reading the answer |

The other commands (`GetVariable`, `SetVariable`, `SetPort`, `Simulate`, `Reset`, `GetTaskInformation`, breakpoints, `SendCustomCommand`...) return the answer of the controller, like with Telnet. The controller refuses some commands when they come from the web server: `Succeed` is then `false` and `ErrorText` gives the message of the controller.

After an Unsafe command, check the state of the controller yourself if your application depends on it: read the task status with `GetTaskInformation()`, or read a variable or an I/O.

```csharp
using UnderAutomation.Fanuc;

public class CgtpKclUnsafe
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Unsafe command: the result is always a success, even if the controller refused the command
        robot.Cgtp.Kcl.Pause("MY_PROGRAM");

        // Check the effect with a command that returns a result
        TaskInformationResult task = robot.Cgtp.Kcl.GetTaskInformation("MY_PROGRAM");
        if (task.TaskStatus != TaskStatus.Paused)
        {
            Console.WriteLine("The program is not paused: " + task.TaskStatusStr);
        }

        // To start a program, use RunProgram instead of Kcl.Run:
        // it can start at a given line and throws a CgtpException if the controller refuses the command
        robot.Cgtp.RunProgram("MY_PROGRAM", lineNum: 10);
    }
}
```

## Start a program: prefer RunProgram

To start a program, prefer `robot.Cgtp.RunProgram(name, lineNum)` to `robot.Cgtp.Kcl.Run(name)`, when the firmware of the controller is **V9.30** or later:

- It can start the program at a given line. `Kcl.Run` always starts at the first executable line.
- It throws a `CgtpException` when the controller refuses the command. `Kcl.Run` reports a success in all cases.

See [Program management](cgtp-programs.md) for the other program functions of CGTP (select, abort, pause).

## API reference

**CgtpKclClient** ([reference](../api/UnderAutomation.Fanuc.Cgtp.Internal.md#cgtpkclclient-robotcgtpkcl))

- `bool Enabled { get; }`: Indicates whether the KCL client is currently connected.
- `CustomCommandResult SendCustomCommandUnsafe(string command)`: Sends a custom KCL command in Unsafe mode. Success or failure cannot be determined from the result.
- Inherited from [KclClientBase](../api/UnderAutomation.Fanuc.Common.Kcl.md#kclclientbase-robottelnet): `Abort`, `AbortAll`, `ClearAll`, `ClearProgram`, `ClearVars`, `Continue`, `Hold`, `Pause`, `Reset`, `Run`, `SetPort`, `SetVariable`, `GetCurrentPose`, `GetVariable`, `Simulate`, `UnsimulateAll`, `Unsimulate`, `SendCustomCommand`, `SendCustomCommand``1`, `GetTaskInformation`, `AddBreakpoint`, `RemoveBreakpoint`, `RemoveAllBreakpoints`, `GetBreakpoints`, `StepOn`, `StepOff`

**KclClientBase** ([reference](../api/UnderAutomation.Fanuc.Common.Kcl.md#kclclientbase-robottelnet))

- `ProgramCommandResult Abort(string program = null, bool force = true)`: Aborts the specified running or paused task. If program is not specified, the default program Is used. Execution of the current program statement Is completed before the task aborts except for the current motion, DELAY, WAIT, Or READ statements, which are canceled. When used through the CGTP KCL...
- `ProgramCommandResult AbortAll(bool force = true)`: Aborts all running or paused tasks. Execution of the current program statement Is completed before the task aborts except for the current motion, DELAY, WAIT, Or READ statements, which are canceled. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot...
- `AddBreakpointResult AddBreakpoint(string taskName, int line)`: Add a breakpoint to a specified task
- `ProgramCommandResult ClearAll()`: Clears all KAREL and teach pendant programs and variable data from memory. All cleared programs And variables (if they were saved with the SaveVars() command) can be reloaded into memory Using the Load() command.
- `ProgramCommandResult ClearProgram(string program = null)`: Clears the program data from memory for the specified or default program. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot be determined from the result.
- `ProgramCommandResult ClearVars(string program = null)`: Clears the variable and type data associated with the specified or default program from memory. Variables And types that are referenced by a loaded program are Not cleared. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot be determined from the re...
- `ProgramCommandResult Continue(string program = null)`: Continues program execution of the specified task (or all paused tasks if program argument is null) that has been paused by a hold, pause, or test run operation. If the program Is aborted, the program execution Is started at the first executable line. When a task Is paused, the CYCLE START button...
- `BreakpointsResult GetBreakpoints(string taskName)`: Returns the breakpoints set on the specified task.
- `GetCurrentPoseResult GetCurrentPose()`: Returns the position of the TCP relative to the current user frame of reference with an x, y, and z location in millimeters; w, p, and r orientation in degrees; and the current configuration string. Be sure the robot is calibrated.
- `TaskInformationResult GetTaskInformation(string prog_name)`: Return the task control data for the specified task. If prog_name is not specified, the default program is used
- `GetVariableResult GetVariable(string name, string program = null)`: Get the name, type, and value of the specified variable. You can display the values of system variables that allow KCL read access or the values of program variables. Use brackets ([]) after the variable name to specify a specific ARRAY element. If you do not specify a specific element the entire...
- `ProgramCommandResult Hold(string program = null)`: Pauses the specified or default program that is being executed and holds motion at the current position (after a normal deceleration). Use the Continue() command Or the CYCLE START button On the Operator panel To resume program execution. When used through the CGTP KCL client (Unsafe mode, from f...
- `ProgramCommandResult Pause(string program = null, bool force = false)`: Pauses the specified running task. If program is not specified, the default program is used. Execution of the current motion segment and the current program statement is completed before the task is paused. Condition handlers remain active. If the condition handler action is NOPAUSE and the condi...
- `RemoveBreakpointResult RemoveAllBreakpoints(string taskName)`: Clear all breakpoints of a specified task
- `RemoveBreakpointResult RemoveBreakpoint(string taskName, int line)`: Clear a breakpoint of a task at a specified line
- `ProgramCommandResult Reset()`: Enables servo power after an error condition has shut off servo power, provided the cause of the error has been cleared. The command also clears the message line on the CRT/KB display. The error message remains displayed if the error condition still exists. The Reset() command has no effect on a...
- `RunResult Run(string program = null)`: Executes the specified program. The program must be loaded in memory If no program is specified the default program is run. If uninitialized variables are encountered, program execution is paused. Execution begins at the first executable line. RUN is a motion command; therefore, the device from w...
- `CustomCommandResult SendCustomCommand(string command)`: Sends a custom KCL command to the robot and returns the raw result.
- `T SendCustomCommand<T>(string command) where T : BaseResult, new()`: Sends a custom KCL command to the robot and returns the result as the specified type.
- `SetPortResult SetPort(KCLPorts port, int index, int value)`: Assigns the specified value to a specified input or output port. SET PORT can be used either physical Or simulated output ports, but only With simulated input ports.
- `SetVariableResult SetVariable(string name, double value, string program = null)`: Assigns the specified value to the specified variable. You can assign constant values or variable values, but the value must be of the data type that has been declared for the variable. You can assign values to system variables with KCL write access, to program variables, or to standard and user-...
- `SetVariableResult SetVariable(string name, int value, string program = null)`: Assigns the specified value to the specified variable. You can assign constant values or variable values, but the value must be of the data type that has been declared for the variable. You can assign values to system variables with KCL write access, to program variables, or to standard and user-...
- `SetVariableResult SetVariable(string name, string value, string program = null)`: Assigns the specified value to the specified variable. You can assign constant values or variable values, but the value must be of the data type that has been declared for the variable. You can assign values to system variables with KCL write access, to program variables, or to standard and user-...
- `SimulateResult Simulate(KCLPorts port, int index, int value)`: Simulating I/O allows you to test a program that uses I/O. Simulating I/O does not actually send output signals or receive input signals. When simulating a port value, you can specify its initial simulated value or allow the initial value to be the same as the physical port value. If no value is...
- `StepOffResult StepOff()`: Disables step mode. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot be determined from the result.
- `StepOnResult StepOn(string taskName)`: Enables step mode for the specified task. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot be determined from the result.
- `UnsimulateResult Unsimulate(KCLPorts port, int index)`: Discontinues simulation of the specified input or output port. When a port is unsimulated, the physical value replaces the simulated value.
- `UnsimulateAllResult UnsimulateAll()`: Discontinues simulation on all input or output port. When a port is unsimulated, the physical value replaces the simulated value.
