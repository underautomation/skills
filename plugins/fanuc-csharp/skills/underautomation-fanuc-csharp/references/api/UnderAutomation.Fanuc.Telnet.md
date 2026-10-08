# UnderAutomation.Fanuc.Telnet

## CommandSentEventArgs

`class CommandSentEventArgs : EventArgs`

Event arguments for command sent events.

- `CommandSentEventArgs()`
- `string Command`: Gets the command that was sent.

## KclClientErrorEventArgs

`class KclClientErrorEventArgs : EventArgs`

Event arguments for KCL client error events.

- `KclClientErrorEventArgs()`
- `Exception Exception`: Gets the exception that occurred.

## KclCommandReceived

`class KclCommandReceived : EventArgs`

Event arguments for KCL command received events.

- `KclCommandReceived()`
- `Result Result`: Gets the result of the received command.

## MessageReceivedEventArgs

`class MessageReceivedEventArgs : EventArgs`

Event arguments for message received events.

- `MessageReceivedEventArgs()`
- `bool IsReset { get; }`: Gets a value indicating whether the message is a reset (empty message).
- `string Message`: Gets the message received from the controller.

## RawDataReceivedEventArgs

`class RawDataReceivedEventArgs : EventArgs`

Event arguments for raw data received events.

- `RawDataReceivedEventArgs()`
- `string Data`: Gets the raw data received.

## TelnetClient

`class TelnetClient : TelnetClientBase`

Standalone Telnet KCL client for direct use without Fanuc.FanucRobot. Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on the web server of th...

- `TelnetClient()`: Create a new instance of a robot communication
- `void Connect(string ip, string telnetKclPassword)`: Connect to a robot
- Inherited from [TelnetClientBase](UnderAutomation.Fanuc.Telnet.Internal.md#telnetclientbase-robottelnet): `PollAndGetUpdatedConnectedState`, `Disconnect`, `IP`, `Language`, `TpCoordinates`, `Connected`, `RawDataReceived`, `StringDataReceived`, `TpCoordinatesReceived`, `MessageReceived`, `ErrorOccured`, `CommandSent`, `CommandReceived`
- Inherited from [KclClientBase](UnderAutomation.Fanuc.Common.Kcl.md#kclclientbase-robottelnet): `Abort`, `AbortAll`, `ClearAll`, `ClearProgram`, `ClearVars`, `Continue`, `Hold`, `Pause`, `Reset`, `Run`, `SetPort`, `SetVariable`, `GetCurrentPose`, `GetVariable`, `Simulate`, `UnsimulateAll`, `Unsimulate`, `SendCustomCommand`, `SendCustomCommand``1`, `GetTaskInformation`, `AddBreakpoint`, `RemoveBreakpoint`, `RemoveAllBreakpoints`, `GetBreakpoints`, `StepOn`, `StepOff`

## TpCoordinates (robot.Telnet.TpCoordinates)

`enum TpCoordinates`

Enumeration of TP (Teach Pendant) coordinate systems.

- JogFrame: Jog frame coordinate system.
- Joint: Joint coordinate system.
- Tool: Tool coordinate system.
- Unknown: Unknown coordinate system.
- User: User coordinate system.
- World: World coordinate system.

## TpCoordinatesReceivedEventArgs

`class TpCoordinatesReceivedEventArgs : EventArgs`

Event arguments for TP coordinates received events.

- `TpCoordinatesReceivedEventArgs()`
- `TpCoordinates Coord`: Gets the TP coordinate system received.
