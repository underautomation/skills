# underautomation.fanuc.common.kcl

## AbortResult

`from underautomation.fanuc.common.kcl.abort_result import AbortResult`

Result of an abort command.

- `AbortResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## AddBreakpointResult

`from underautomation.fanuc.common.kcl.add_breakpoint_result import AddBreakpointResult`

Result of adding a breakpoint.

- `AddBreakpointResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## BaseResult

`from underautomation.fanuc.common.kcl.base_result import BaseResult`

Base class for simple results that store error text from the response.

- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## Breakpoint

`from underautomation.fanuc.common.kcl.breakpoint import Breakpoint`

Represents a breakpoint set on a task line.

- `Breakpoint()`
- `line: int (read only)`: Gets the line number where the breakpoint is set.

## BreakpointsResult

`from underautomation.fanuc.common.kcl.breakpoints_result import BreakpointsResult`

Result containing the breakpoints of a task.

- `BreakpointsResult()`
- `breakpoints: typing.List[Breakpoint] (read only)`: Gets the breakpoints set on the task.
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## ContinueResult

`from underautomation.fanuc.common.kcl.continue_result import ContinueResult`

Result of a continue command.

- `ContinueResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## CustomCommandResult

`from underautomation.fanuc.common.kcl.custom_command_result import CustomCommandResult`

Result of a custom KCL command.

- `CustomCommandResult()`
- `data: str (read only)`: Gets the raw data returned by the custom command.
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## GetCurrentPoseResult

`from underautomation.fanuc.common.kcl.get_current_pose_result import GetCurrentPoseResult`

Result of a get current pose command.

- `GetCurrentPoseResult()`
- `group: int (read only)`: Group number of the current pose.
- `position: CartesianPosition (read only)`: Cartesian position value of the current pose.
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## GetVariableResult

`from underautomation.fanuc.common.kcl.get_variable_result import GetVariableResult`

Result of a get variable command containing the raw value.

- `GetVariableResult()`
- `parse_result() -> GenericVariable`: Returns a structured object which represents the variable (not supported with Telnet)
- `raw_value: str (read only)`: Gets the raw value of the variable as a string.
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## KCLPorts

`from underautomation.fanuc.common.kcl.kcl_ports import KCLPorts`

Enum representing the different KCL ports.

- DIN: Digital Input port.
- DOUT: Digital Output port.
- RDO: Robot Digital Output port.
- OPOUT: Operator Panel Output port.
- TPOUT: Teach Pendant Output port.
- WDI: Weld Digital Input port.
- WDO: Weld Digital Output port.
- AIN: Analog Input port.
- AOUT: Analog Output port.
- GIN: General Input port.
- GOUT: General Output port.

## KclClientBase (robot.telnet)

`from underautomation.fanuc.common.kcl.kcl_client_base import KclClientBase`

Abstract base class for KCL (Keyboard Command Line) clients. Provides all KCL commands shared between Telnet and CGTP implementations.

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

## PauseResult

`from underautomation.fanuc.common.kcl.pause_result import PauseResult`

Result of a pause command.

- `PauseResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## ProgramCommandResult

`from underautomation.fanuc.common.kcl.program_command_result import ProgramCommandResult`

Result of a program command (abort, continue, hold, pause, run, etc.).

- `ProgramCommandResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## RemoveBreakpointResult

`from underautomation.fanuc.common.kcl.remove_breakpoint_result import RemoveBreakpointResult`

Result of removing a breakpoint.

- `RemoveBreakpointResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## ResetResult

`from underautomation.fanuc.common.kcl.reset_result import ResetResult`

Result of a reset command.

- `ResetResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## Result

`from underautomation.fanuc.common.kcl.result import Result`

Abstract base class for all KCL command results.

- `error_text: str (read only)`: Error text if any error occured during command execution
- `succeed: bool (read only)`: Command succeeded if no error text is present
- `kcl_command: str (read only)`: The KCL command that was sent to the controller

## RunResult

`from underautomation.fanuc.common.kcl.run_result import RunResult`

Result of a run command.

- `RunResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## SetPortResult

`from underautomation.fanuc.common.kcl.set_port_result import SetPortResult`

Result of a set port command.

- `SetPortResult()`
- Inherited from [SetValueResult](underautomation.fanuc.common.kcl.md#setvalueresult): `former_value`, `new_value`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## SetValueResult

`from underautomation.fanuc.common.kcl.set_value_result import SetValueResult`

Base class for results that contain a former and new value.

- `former_value: str (read only)`: Former value before the command
- `new_value: str (read only)`: New value after the command execution
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## SetVariableResult

`from underautomation.fanuc.common.kcl.set_variable_result import SetVariableResult`

Result of a set variable command.

- `SetVariableResult()`
- Inherited from [SetValueResult](underautomation.fanuc.common.kcl.md#setvalueresult): `former_value`, `new_value`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## SimulateResult

`from underautomation.fanuc.common.kcl.simulate_result import SimulateResult`

Result of a simulate port command.

- `SimulateResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## StepOffResult

`from underautomation.fanuc.common.kcl.step_off_result import StepOffResult`

Result of the step off command.

- `StepOffResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## StepOnResult

`from underautomation.fanuc.common.kcl.step_on_result import StepOnResult`

Result of the step on command.

- `StepOnResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## TaskInformationResult

`from underautomation.fanuc.common.kcl.task_information_result import TaskInformationResult`

Result of the show task command containing task properties.

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
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## UnsimulateAllResult

`from underautomation.fanuc.common.kcl.unsimulate_all_result import UnsimulateAllResult`

Result of an unsimulate all command.

- `UnsimulateAllResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## UnsimulateResult

`from underautomation.fanuc.common.kcl.unsimulate_result import UnsimulateResult`

Result of an unsimulate port command.

- `UnsimulateResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## VariableResult

`from underautomation.fanuc.common.kcl.variable_result import VariableResult`

Result of a show variable command.

- `VariableResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

## VariablesResult

`from underautomation.fanuc.common.kcl.variables_result import VariablesResult`

Result of a show variables command.

- `VariablesResult()`
- Inherited from [Result](underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`
