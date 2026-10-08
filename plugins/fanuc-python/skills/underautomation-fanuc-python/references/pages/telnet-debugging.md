# Debugging & breakpoints

Add, remove, and manage breakpoints on TP and Karel programs. Step through code line by line using Telnet KCL.

Web page: https://underautomation.com/fanuc/documentation/telnet-debugging

> **Telnet KCL is a legacy protocol.** It is not secured: the password and the commands are sent in clear text. It is hard to maintain: the answers of the controller change with the firmware version, and ROBOGUIDE behaves differently from a real controller. The KCL commands of `robot.Telnet` are also available with `robot.Cgtp.Kcl`, through the web server of the controller (firmware V8.30 and later), without Telnet setup. Prefer it for new developments: see [KCL commands over CGTP](cgtp-kcl.md).

The Fanuc SDK lets you add, remove, and manage breakpoints on TP and Karel programs. It can also run a program line by line, for remote debugging or for a custom TP editor.

## Breakpoints

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Add a breakpoint at line 10
robot.telnet.add_breakpoint("MyProgram", 10)

# List breakpoints
result = robot.telnet.get_breakpoints("MyProgram")
for bp in result.breakpoints:
    print(f"Breakpoint at line {bp.line}")

# Remove a single breakpoint
robot.telnet.remove_breakpoint("MyProgram", 10)

# Remove all breakpoints of a program
robot.telnet.remove_all_breakpoints("MyProgram")
```

## Step-by-step execution and task info

When step mode is enabled, the program pauses after each line execution, allowing you to inspect state between instructions.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Enable step mode for a task
robot.telnet.step_on("MyProgram")

# Disable step mode
robot.telnet.step_off()

# Get task information (current line, status, etc.)
info = robot.telnet.get_task_information("MyProgram")
```

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Add a breakpoint at line 10 of MyProgram
robot.telnet.add_breakpoint("MyProgram", 10)

# List all breakpoints
result = robot.telnet.get_breakpoints("MyProgram")
for bp in result.breakpoints:
    print(f"Breakpoint at line {bp.line}")

# Remove a single breakpoint
robot.telnet.remove_breakpoint("MyProgram", 10)

# Remove all breakpoints
robot.telnet.remove_all_breakpoints("MyProgram")

# Enable step-by-step execution
robot.telnet.step_on("MyProgram")

# Disable step mode
robot.telnet.step_off()
```

## See also

- [TP editor with breakpoints](tp-editor-with-breakpoints.md) : Build a custom TP editor with syntax highlighting and breakpoints

## API reference

**BreakpointsResult** ([reference](../api/underautomation.fanuc.common.kcl.md#breakpointsresult))

- `BreakpointsResult()`
- `breakpoints: typing.List[Breakpoint] (read only)`: Gets the breakpoints set on the task.
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**Breakpoint** ([reference](../api/underautomation.fanuc.common.kcl.md#breakpoint))

- `Breakpoint()`
- `line: int (read only)`: Gets the line number where the breakpoint is set.

**AddBreakpointResult** ([reference](../api/underautomation.fanuc.common.kcl.md#addbreakpointresult))

- `AddBreakpointResult()`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**RemoveBreakpointResult** ([reference](../api/underautomation.fanuc.common.kcl.md#removebreakpointresult))

- `RemoveBreakpointResult()`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**StepOnResult** ([reference](../api/underautomation.fanuc.common.kcl.md#steponresult))

- `StepOnResult()`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**TaskInformationResult** ([reference](../api/underautomation.fanuc.common.kcl.md#taskinformationresult))

- `TaskInformationResult()`
- `task_name: str (read only)`: Gets the name of the task.
- `task_number: int (read only)`: Gets the task number.
- `task_status_str: str (read only)`: Gets the task status as a string.
- `task_status: TaskStatus (read only)`: Gets the task status.
- `routine_name: str (read only)`: Gets the name of the routine.
- `current_line: int (read only)`: Gets the current line number.
- `program_type: ProgramType (read only)`: Gets the type of the program.
- `hold_conditions: str (read only)`: Gets the hold conditions.
- `invisible_task: bool (read only)`: Gets a value indicating whether the task is invisible.
- `system_task: bool (read only)`: Gets a value indicating whether the task is a system task.
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`
