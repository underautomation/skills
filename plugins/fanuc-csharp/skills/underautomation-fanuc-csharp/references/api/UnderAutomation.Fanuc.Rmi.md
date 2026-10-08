# UnderAutomation.Fanuc.Rmi

## RmiClient

`class RmiClient : RmiClientBase, IDisposable`

RMI client for connecting to and controlling FANUC robots via the Remote Motion Interface protocol.

- `RmiClient()`: Creates a new instance of the RMI client.
- `void Connect(string ip, int port = 16001, int readTimeoutMs = 2000)`: Connect to the FANUC controller using the RMI protocol.
- Inherited from [RmiClientBase](UnderAutomation.Fanuc.Rmi.Internal.md#rmiclientbase-robotrmi): `Disconnect`, `Initialize`, `Abort`, `Pause`, `Continue`, `Reset`, `ReadError`, `GetUFrameUTool`, `SetUFrameUTool`, `GetStatus`, `AutoSetNextSequenceId`, `GetExtendedStatus`, `ReadUFrame`, `WriteUFrame`, `ReadUTool`, `WriteUTool`, `ReadDIN`, `WriteDOUT`, `ReadIOPort`, `WriteIOPort`, `ReadCartesianPosition`, `ReadJointAngles`, `SetOverride`, `ReadPositionRegister`, `WritePositionRegisterCartesian`, `ReadNumericRegister`, `WriteNumericRegisterAsInteger`, `WriteNumericRegisterAsDouble`, `ReadVariable`, `WriteVariableAsInteger`, `WriteVariableAsDouble`, `ReadTcpSpeed`, `SetPayloadSchedule`, `SetPayloadValue`, `SetPayloadCompensation`, `ClearCompletedInstructions`, `ClearLocalQueuedInstructions`, `SendTpInstruction`, `Dispose`, `Connected`, `MajorVersion`, `MinorVersion`, `WorkingPort`, `LastSequenceId`, `CheckSequenceId`, `IsInHoldState`, `ReadTimeoutMs`, `Instructions`, `ConnectionTerminated`, `SystemFaultReceived`, `RecordedCartesianPositionReceived`, `RecordedJointPositionReceived`, `UnknownPacketReceived`

## RmiException

`class RmiException : Exception, ISerializable, _Exception`

Represents an error reported by the FANUC RMI controller or thrown by the client runtime.

- `RmiException(int errorId, string message)`: Constructs a new Rmi.RmiException with an error id coming from the controller.
- `RmiException(string message)`: Constructs a new Rmi.RmiException with a message.
- `RmiException(string message, Exception inner)`: Constructs a new Rmi.RmiException with a message and an inner exception.
- `int ErrorId { get; }`: Gets the controller error id when available (0 means no error id was attached).
