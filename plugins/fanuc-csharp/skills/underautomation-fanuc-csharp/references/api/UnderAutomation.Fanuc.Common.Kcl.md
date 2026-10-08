# UnderAutomation.Fanuc.Common.Kcl

## AbortResult

`class AbortResult : Result`

Result of an abort command.

- `AbortResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## AddBreakpointResult

`class AddBreakpointResult : Result`

Result of adding a breakpoint.

- `AddBreakpointResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## BaseResult

`abstract class BaseResult : Result`

Base class for simple results that store error text from the response.

- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## Breakpoint

`class Breakpoint`

Represents a breakpoint set on a task line.

- `Breakpoint()`
- `int Line { get; }`: Gets the line number where the breakpoint is set.

## BreakpointsResult

`class BreakpointsResult : Result`

Result containing the breakpoints of a task.

- `BreakpointsResult()`
- `Breakpoint[] Breakpoints { get; }`: Gets the breakpoints set on the task.
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## ContinueResult

`class ContinueResult : Result`

Result of a continue command.

- `ContinueResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## CustomCommandResult

`class CustomCommandResult : Result`

Result of a custom KCL command.

- `CustomCommandResult()`
- `string Data { get; }`: Gets the raw data returned by the custom command.
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## GetCurrentPoseResult

`class GetCurrentPoseResult : Result`

Result of a get current pose command.

- `GetCurrentPoseResult()`
- `int Group { get; }`: Group number of the current pose.
- `CartesianPosition Position { get; }`: Cartesian position value of the current pose.
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## GetVariableResult

`class GetVariableResult : Result`

Result of a get variable command containing the raw value.

- `GetVariableResult()`
- `GenericVariable ParseResult()`: Returns a structured object which represents the variable (not supported with Telnet)
- `string RawValue { get; }`: Gets the raw value of the variable as a string.
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## KCLPorts

`enum KCLPorts`

Enum representing the different KCL ports.

- AIN: Analog Input port.
- AOUT: Analog Output port.
- DIN: Digital Input port.
- DOUT: Digital Output port.
- GIN: General Input port.
- GOUT: General Output port.
- OPOUT: Operator Panel Output port.
- RDO: Robot Digital Output port.
- TPOUT: Teach Pendant Output port.
- WDI: Weld Digital Input port.
- WDO: Weld Digital Output port.

## KclClientBase (robot.Telnet)

`abstract class KclClientBase`

Abstract base class for KCL (Keyboard Command Line) clients. Provides all KCL commands shared between Telnet and CGTP implementations.

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

## PauseResult

`class PauseResult : Result`

Result of a pause command.

- `PauseResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## ProgramCommandResult

`class ProgramCommandResult : Result`

Result of a program command (abort, continue, hold, pause, run, etc.).

- `ProgramCommandResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## RemoveBreakpointResult

`class RemoveBreakpointResult : Result`

Result of removing a breakpoint.

- `RemoveBreakpointResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## ResetResult

`class ResetResult : Result`

Result of a reset command.

- `ResetResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## Result

`abstract class Result`

Abstract base class for all KCL command results.

- `string ErrorText { get; }`: Error text if any error occured during command execution
- `string KclCommand { get; }`: The KCL command that was sent to the controller
- `bool Succeed { get; }`: Command succeeded if no error text is present

## RunResult

`class RunResult : ProgramCommandResult`

Result of a run command.

- `RunResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## SetPortResult

`class SetPortResult : SetValueResult`

Result of a set port command.

- `SetPortResult()`
- Inherited from [SetValueResult](UnderAutomation.Fanuc.Common.Kcl.md#setvalueresult): `FormerValue`, `NewValue`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## SetValueResult

`abstract class SetValueResult : Result`

Base class for results that contain a former and new value.

- `string FormerValue { get; protected set; }`: Former value before the command
- `string NewValue { get; protected set; }`: New value after the command execution
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## SetVariableResult

`class SetVariableResult : SetValueResult`

Result of a set variable command.

- `SetVariableResult()`
- Inherited from [SetValueResult](UnderAutomation.Fanuc.Common.Kcl.md#setvalueresult): `FormerValue`, `NewValue`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## SimulateResult

`class SimulateResult : BaseResult`

Result of a simulate port command.

- `SimulateResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## StepOffResult

`class StepOffResult : Result`

Result of the step off command.

- `StepOffResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## StepOnResult

`class StepOnResult : Result`

Result of the step on command.

- `StepOnResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## TaskInformationResult

`class TaskInformationResult : Result`

Result of the show task command containing task properties.

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
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## UnsimulateAllResult

`class UnsimulateAllResult : BaseResult`

Result of an unsimulate all command.

- `UnsimulateAllResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## UnsimulateResult

`class UnsimulateResult : BaseResult`

Result of an unsimulate port command.

- `UnsimulateResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## VariableResult

`class VariableResult : Result`

Result of a show variable command.

- `VariableResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`

## VariablesResult

`class VariablesResult : Result`

Result of a show variables command.

- `VariablesResult()`
- Inherited from [Result](UnderAutomation.Fanuc.Common.Kcl.md#result): `ErrorText`, `Succeed`, `KclCommand`
