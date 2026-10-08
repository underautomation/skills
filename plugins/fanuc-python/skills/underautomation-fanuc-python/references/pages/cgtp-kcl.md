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

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()

# CGTP is enabled by default: no Telnet password and no Telnet setup on the robot
robot.connect("192.168.0.1")

# Before: robot.telnet.set_variable("$RMT_MASTER", 1)
result = robot.cgtp.kcl.set_variable("$RMT_MASTER", 1)
if not result.succeed:
    print(result.error_text)

# Before: robot.telnet.get_task_information("MY_PROGRAM")
task = robot.cgtp.kcl.get_task_information("MY_PROGRAM")
print(f"{task.task_status} at line {task.current_line}")
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

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.common.task_status import TaskStatus

robot = FanucRobot()
robot.connect("192.168.0.1")

# Unsafe command: the result is always a success, even if the controller refused the command
robot.cgtp.kcl.pause("MY_PROGRAM")

# Check the effect with a command that returns a result
task = robot.cgtp.kcl.get_task_information("MY_PROGRAM")
if task.task_status != TaskStatus.Paused:
    print("The program is not paused:", task.task_status_str)

# To start a program, use run_program instead of kcl.run:
# it can start at a given line and raises an exception if the controller refuses the command
robot.cgtp.run_program("MY_PROGRAM", line_num=10)
```

## Start a program: prefer RunProgram

To start a program, prefer `robot.Cgtp.RunProgram(name, lineNum)` to `robot.Cgtp.Kcl.Run(name)`, when the firmware of the controller is **V9.30** or later:

- It can start the program at a given line. `Kcl.Run` always starts at the first executable line.
- It throws a `CgtpException` when the controller refuses the command. `Kcl.Run` reports a success in all cases.

See [Program management](cgtp-programs.md) for the other program functions of CGTP (select, abort, pause).

## API reference

**CgtpKclClient** ([reference](../api/underautomation.fanuc.cgtp.internal.md#cgtpkclclient-robotcgtpkcl))

- `send_custom_command_unsafe(command: str) -> CustomCommandResult`: Sends a custom KCL command in Unsafe mode. Success or failure cannot be determined from the result.
- `enabled: bool (read only)`: Indicates whether the KCL client is currently connected.
- Inherited from [KclClientBase](../api/underautomation.fanuc.common.kcl.md#kclclientbase-robottelnet): `abort`, `abort_all`, `clear_all`, `clear_program`, `clear_vars`, `continue_`, `hold`, `pause`, `reset`, `run`, `set_port`, `set_variable`, `get_current_pose`, `get_variable`, `simulate`, `unsimulate_all`, `unsimulate`, `send_custom_command`, `get_task_information`, `add_breakpoint`, `remove_breakpoint`, `remove_all_breakpoints`, `get_breakpoints`, `step_on`, `step_off`

**KclClientBase** ([reference](../api/underautomation.fanuc.common.kcl.md#kclclientbase-robottelnet))

- `abort(program: str=None, force: bool=True) -> ProgramCommandResult`: Aborts the specified running or paused task. If program is not specified, the default program Is used. Execution of the current program statement Is completed before the task aborts except for the current motion, DELAY, WAIT, Or READ statements, which are canceled. When used through the CGTP KCL...
- `abort_all(force: bool=True) -> ProgramCommandResult`: Aborts all running or paused tasks. Execution of the current program statement Is completed before the task aborts except for the current motion, DELAY, WAIT, Or READ statements, which are canceled. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot...
- `clear_all() -> ProgramCommandResult`: Clears all KAREL and teach pendant programs and variable data from memory. All cleared programs And variables (if they were saved with the SaveVars() command) can be reloaded into memory Using the Load() command.
- `clear_program(program: str=None) -> ProgramCommandResult`: Clears the program data from memory for the specified or default program. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot be determined from the result.
- `clear_vars(program: str=None) -> ProgramCommandResult`: Clears the variable and type data associated with the specified or default program from memory. Variables And types that are referenced by a loaded program are Not cleared. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot be determined from the re...
- `continue_(program: str=None) -> ProgramCommandResult`: Continues program execution of the specified task (or all paused tasks if program argument is null) that has been paused by a hold, pause, or test run operation. If the program Is aborted, the program execution Is started at the first executable line. When a task Is paused, the CYCLE START button...
- `hold(program: str=None) -> ProgramCommandResult`: Pauses the specified or default program that is being executed and holds motion at the current position (after a normal deceleration). Use the Continue() command Or the CYCLE START button On the Operator panel To resume program execution. When used through the CGTP KCL client (Unsafe mode, from f...
- `pause(program: str=None, force: bool=False) -> ProgramCommandResult`: Pauses the specified running task. If program is not specified, the default program is used. Execution of the current motion segment and the current program statement is completed before the task is paused. Condition handlers remain active. If the condition handler action is NOPAUSE and the condi...
- `reset() -> ProgramCommandResult`: Enables servo power after an error condition has shut off servo power, provided the cause of the error has been cleared. The command also clears the message line on the CRT/KB display. The error message remains displayed if the error condition still exists. The Reset() command has no effect on a...
- `run(program: str=None) -> RunResult`: Executes the specified program. The program must be loaded in memory If no program is specified the default program is run. If uninitialized variables are encountered, program execution is paused. Execution begins at the first executable line. RUN is a motion command; therefore, the device from w...
- `set_port(port: KCLPorts, index: int, value: int) -> SetPortResult`: Assigns the specified value to a specified input or output port. SET PORT can be used either physical Or simulated output ports, but only With simulated input ports.
- `set_variable(name: str, value: float | int | str, program: str=None) -> SetVariableResult`: Assigns the specified value to the specified variable. You can assign constant values or variable values, but the value must be of the data type that has been declared for the variable. You can assign values to system variables with KCL write access, to program variables, or to standard and user-...
- `get_current_pose() -> GetCurrentPoseResult`: Returns the position of the TCP relative to the current user frame of reference with an x, y, and z location in millimeters; w, p, and r orientation in degrees; and the current configuration string. Be sure the robot is calibrated.
- `get_variable(name: str, program: str=None) -> GetVariableResult`: Get the name, type, and value of the specified variable. You can display the values of system variables that allow KCL read access or the values of program variables. Use brackets ([]) after the variable name to specify a specific ARRAY element. If you do not specify a specific element the entire...
- `simulate(port: KCLPorts, index: int, value: int) -> SimulateResult`: Simulating I/O allows you to test a program that uses I/O. Simulating I/O does not actually send output signals or receive input signals. When simulating a port value, you can specify its initial simulated value or allow the initial value to be the same as the physical port value. If no value is...
- `unsimulate_all() -> UnsimulateAllResult`: Discontinues simulation on all input or output port. When a port is unsimulated, the physical value replaces the simulated value.
- `unsimulate(port: KCLPorts, index: int) -> UnsimulateResult`: Discontinues simulation of the specified input or output port. When a port is unsimulated, the physical value replaces the simulated value.
- `send_custom_command(command: str) -> CustomCommandResult`: Sends a custom KCL command to the robot and returns the raw result.
- `get_task_information(prog_name: str) -> TaskInformationResult`: Return the task control data for the specified task. If prog_name is not specified, the default program is used
- `add_breakpoint(taskName: str, line: int) -> AddBreakpointResult`: Add a breakpoint to a specified task
- `remove_breakpoint(taskName: str, line: int) -> RemoveBreakpointResult`: Clear a breakpoint of a task at a specified line
- `remove_all_breakpoints(taskName: str) -> RemoveBreakpointResult`: Clear all breakpoints of a specified task
- `get_breakpoints(taskName: str) -> BreakpointsResult`: Returns the breakpoints set on the specified task.
- `step_on(taskName: str) -> StepOnResult`: Enables step mode for the specified task. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot be determined from the result.
- `step_off() -> StepOffResult`: Disables step mode. When used through the CGTP KCL client (Unsafe mode, from firmware 9.30), success or failure cannot be determined from the result.
