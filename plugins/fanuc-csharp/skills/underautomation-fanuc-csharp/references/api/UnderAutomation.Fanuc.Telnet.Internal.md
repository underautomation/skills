# UnderAutomation.Fanuc.Telnet.Internal

## TelnetClientBase (robot.Telnet)

`abstract class TelnetClientBase : KclClientBase`

Base class for Telnet KCL client. Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on the web server of the controller with robot.Cgtp.Kcl (fi...

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
- Inherited from [KclClientBase](UnderAutomation.Fanuc.Common.Kcl.md#kclclientbase-robottelnet): `Abort`, `AbortAll`, `ClearAll`, `ClearProgram`, `ClearVars`, `Continue`, `Hold`, `Pause`, `Reset`, `Run`, `SetPort`, `SetVariable`, `GetCurrentPose`, `GetVariable`, `Simulate`, `UnsimulateAll`, `Unsimulate`, `SendCustomCommand`, `SendCustomCommand``1`, `GetTaskInformation`, `AddBreakpoint`, `RemoveBreakpoint`, `RemoveAllBreakpoints`, `GetBreakpoints`, `StepOn`, `StepOff`

## TelnetClientInternal (robot.Telnet)

`class TelnetClientInternal : TelnetClientBase`

Telnet KCL client created and managed by Fanuc.FanucRobot. Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on the web server of the controlle...

- Inherited from [TelnetClientBase](UnderAutomation.Fanuc.Telnet.Internal.md#telnetclientbase-robottelnet): `PollAndGetUpdatedConnectedState`, `Disconnect`, `IP`, `Language`, `TpCoordinates`, `Connected`, `RawDataReceived`, `StringDataReceived`, `TpCoordinatesReceived`, `MessageReceived`, `ErrorOccured`, `CommandSent`, `CommandReceived`
- Inherited from [KclClientBase](UnderAutomation.Fanuc.Common.Kcl.md#kclclientbase-robottelnet): `Abort`, `AbortAll`, `ClearAll`, `ClearProgram`, `ClearVars`, `Continue`, `Hold`, `Pause`, `Reset`, `Run`, `SetPort`, `SetVariable`, `GetCurrentPose`, `GetVariable`, `Simulate`, `UnsimulateAll`, `Unsimulate`, `SendCustomCommand`, `SendCustomCommand``1`, `GetTaskInformation`, `AddBreakpoint`, `RemoveBreakpoint`, `RemoveAllBreakpoints`, `GetBreakpoints`, `StepOn`, `StepOff`

## TelnetConnectParametersBase

`class TelnetConnectParametersBase`

Base class for Telnet connection parameters.

- `TelnetConnectParametersBase()`
- `string TelnetKclPassword { get; set; }`: Gets or sets the Telnet KCL password used for authentication.
