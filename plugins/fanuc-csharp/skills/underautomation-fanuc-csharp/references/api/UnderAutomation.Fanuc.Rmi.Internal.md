# UnderAutomation.Fanuc.Rmi.Internal

## RmiClientBase (robot.Rmi)

`abstract class RmiClientBase : IDisposable`

High-level Remote Motion Interface (RMI) client for FANUC controllers. Manages the connection lifecycle, all administrative commands, and the full set of motion instruction packets over the RMI TCP protocol.

- `RmiClientBase()`: Creates a new instance of the RMI client.
- `void Abort()`: Abort the running motion program. Note that a Reset() will be called automatically if the controller is in the HOLD state.
- `RmiControllerStatusResponse AutoSetNextSequenceId()`: Calls internally RmiClientBase.GetStatus and set RmiClientBase.LastSequenceId only if $RMI_CFG.$Chk_seqID = FALSE. It also set RmiClientBase.CheckSequenceId to $RMI_CFG.$Chk_seqID.
- `bool CheckSequenceId { get; set; }`: Indicates whether the controller checks for consecutive sequence IDs in motion instructions ($RMI_CFG.$Chk_seqID). Modified by RmiClientBase.AutoSetNextSequenceId.
- `void ClearCompletedInstructions()`: Removes all instructions with a terminal status (RmiInstructionStatus.Completed or RmiInstructionStatus.Error) from the tracked instruction list. Instructions that are still pending or in progress are not affected.
- `void ClearLocalQueuedInstructions()`: Cancels and removes all instructions that are still in the local client buffer (RmiInstructionStatus.LocalQueued). These instructions have not been sent to the controller yet. Each cancelled instruction is marked with an error so that any thread blocked on WaitForCompletion(System.Int32) is unblo...
- `bool Connected { get; }`: Indicates that the client is currently connected to the controller working port.
- `event Action ConnectionTerminated`: Fired when the controller closes the session (e.g. communication idle timeout). The client is automatically disconnected after this event fires.
- `void Continue()`: Resume a paused motion program.
- `void Disconnect()`: Disconnect from the controller by sending the disconnect command on the working port. Safe to call even when already disconnected.
- `void Dispose()`: Disconnect from the controller and release resources.
- `RmiExtendedControllerStatusResponse GetExtendedStatus()`: Get extended controller status including drive power state and speed clamp.
- `RmiControllerStatusResponse GetStatus()`: Get the current controller and RMI motion status.
- `RmiUFrameUToolNumbersResponse GetUFrameUTool(byte? group = null)`: Get the current UFRAME and UTOOL numbers.
- `void Initialize(byte? groupMask = null, bool? rtsa = null, RmiPltzMode? pltzMode = null)`: Initialize RMI and start the motion program. Must be called before sending any motion instructions. It also Resets RmiClientBase.LastSequenceId and empty the instruction buffer RmiClientBase.Instructions
- `RmiInstructionResponse[] Instructions { get; }`: All instructions submitted since the last Data.RmiPltzMode%7d) or explicit clear, in submission order. Includes instructions in all states: RmiInstructionStatus.LocalQueued, RmiInstructionStatus.ControllerQueued, RmiInstructionStatus.Executing, RmiInstructionStatus.Completed and RmiInstructionSta...
- `bool IsInHoldState { get; }`: Indicates that the controller has entered the HOLD state and will not accept new TP instructions until RmiClientBase.Reset is called. The HOLD state is entered in two situations: An invalid sequence ID was detected (error RMIT-029, error code 2556957). RMI checks that sequence IDs are consecutive...
- `int LastSequenceId { get; }`: Sequence ID used for the last instruction sent to the controller. Reset to 0 by Data.RmiPltzMode%7d).. Modified by RmiClientBase.AutoSetNextSequenceId.
- `short MajorVersion { get; }`: Controller protocol major version reported during the connection handshake.
- `short MinorVersion { get; }`: Controller protocol minor version reported during the connection handshake.
- `void Pause()`: Pause the running motion program.
- `RmiCartesianPositionResponse ReadCartesianPosition(byte? group = null)`: Read current Cartesian TCP position.
- `RmiDigitalInputValueResponse ReadDIN(short portNumber)`: Read a digital input port value.
- `RmiControllerErrorTextResponse ReadError(byte? count = null)`: Read the most recent controller error text. Up to 5 consecutive errors can be requested.
- `RmiIoPortValueResponse ReadIOPort(RmiIoPortType portType, int portNumber)`: Read a generic IO port (DI, DO, AI, AO, GO, RO, FLAG, RI, UI, UO).
- `RmiJointAnglesSampleResponse ReadJointAngles(byte? group = null)`: Read current joint angles.
- `RmiNumericRegisterValueResponse ReadNumericRegister(int number)`: Read a numeric register
- `RmiPositionRegisterDataResponse ReadPositionRegister(short number, byte? group = null)`: Read a position register
- `RmiTcpSpeedResponse ReadTcpSpeed()`: Read the current TCP speed in mm/s.
- `int ReadTimeoutMs { get; }`: RMI connection parameters used during Connect().
- `RmiIndexedFrameResponse ReadUFrame(byte number, byte? group = null)`: Read the UFRAME at the given index.
- `RmiIndexedFrameResponse ReadUTool(byte number, byte? group = null)`: Read the UTOOL at the given index.
- `RmiVariableValueResponse ReadVariable(string name)`: Read a system variable by name (name must include the leading $ character).
- `event Action<RmiRecordedCartesianPosition> RecordedCartesianPositionReceived`: Fired when the controller sends a Cartesian position via the RMI Position Record menu.
- `event Action<RmiRecordedJointPosition> RecordedJointPositionReceived`: Fired when the controller sends a joint position via the RMI Position Record menu.
- `void Reset()`: Reset controller errors and exit the HOLD state.
- `RmiInstructionResponse SendTpInstruction(RmiInstructionBase instruction)`: Sends the instruction to the controller, which queues it. Returns an Data.RmiInstructionResponse that tracks execution.
- `void SetOverride(byte value)`: Set the program speed override (1–100 %).
- `void SetPayloadCompensation(byte scheduleNumber, float massKg, float cgXm, float cgYm, float cgZm, float inertiaXkgm2, float inertiaYkgm2, float inertiaZkgm2, byte? group = null)`: Define payload compensation parameters for a payload schedule.
- `void SetPayloadCompensation(RmiSetPayloadCompensationParameters p)`: Define payload compensation parameters for a payload schedule.
- `void SetPayloadSchedule(byte scheduleNumber, byte? group = null)`: Immediately apply a payload schedule to the active group (command, not an instruction).
- `void SetPayloadValue(byte scheduleNumber, float massKg, float cgXm, float cgYm, float cgZm, float? inertiaXkgm2 = null, float? inertiaYkgm2 = null, float? inertiaZkgm2 = null, byte? group = null)`: Define payload mass, center of gravity, and optionally inertia for a payload schedule.
- `void SetPayloadValue(RmiSetPayloadParameters p)`: Define payload mass, center of gravity, and optionally inertia for a payload schedule.
- `void SetUFrameUTool(byte uframe, byte utool, byte? group = null)`: Set the current UFRAME and UTOOL numbers.
- `event Action<int> SystemFaultReceived`: Fired when the controller reports a system fault on a given sequence. The argument is the SequenceID of the faulted instruction (0 when unknown).
- `event Action<RmiResponseBase> UnknownPacketReceived`: Fired when the controller sends a response that the SDK does not know.
- `int WorkingPort { get; }`: Working port returned by the controller; all commands use this port after connection.
- `void WriteDOUT(short portNumber, RmiOnOff value)`: Write a digital output port value.
- `void WriteIOPort(RmiIoPortType portType, int portNumber, double value)`: Write a generic IO port (AO, GO, DO, RO, FLAG).
- `void WriteNumericRegisterAsDouble(int number, double value)`: Write a float value to a numeric register
- `void WriteNumericRegisterAsInteger(int number, int value)`: Write an integer value to a numeric register
- `void WritePositionRegisterCartesian(short number, CartesianPositionWithUserFrame target, byte? group = null)`: Write a Cartesian position register
- `void WriteUFrame(byte number, XYZWPRPosition position, byte? group = null)`: Write the UFRAME at the given index.
- `void WriteUTool(byte number, XYZWPRPosition position, byte? group = null)`: Write the UTOOL at the given index.
- `void WriteVariableAsDouble(string name, double value)`: Write a float value to a system variable (name must include the leading $).
- `void WriteVariableAsInteger(string name, int value)`: Write an integer value to a system variable (name must include the leading $).

## RmiClientInternal (robot.Rmi)

`class RmiClientInternal : RmiClientBase, IDisposable`

Internal RMI client used by the library infrastructure.

- Inherited from [RmiClientBase](UnderAutomation.Fanuc.Rmi.Internal.md#rmiclientbase-robotrmi): `Disconnect`, `Initialize`, `Abort`, `Pause`, `Continue`, `Reset`, `ReadError`, `GetUFrameUTool`, `SetUFrameUTool`, `GetStatus`, `AutoSetNextSequenceId`, `GetExtendedStatus`, `ReadUFrame`, `WriteUFrame`, `ReadUTool`, `WriteUTool`, `ReadDIN`, `WriteDOUT`, `ReadIOPort`, `WriteIOPort`, `ReadCartesianPosition`, `ReadJointAngles`, `SetOverride`, `ReadPositionRegister`, `WritePositionRegisterCartesian`, `ReadNumericRegister`, `WriteNumericRegisterAsInteger`, `WriteNumericRegisterAsDouble`, `ReadVariable`, `WriteVariableAsInteger`, `WriteVariableAsDouble`, `ReadTcpSpeed`, `SetPayloadSchedule`, `SetPayloadValue`, `SetPayloadCompensation`, `ClearCompletedInstructions`, `ClearLocalQueuedInstructions`, `SendTpInstruction`, `Dispose`, `Connected`, `MajorVersion`, `MinorVersion`, `WorkingPort`, `LastSequenceId`, `CheckSequenceId`, `IsInHoldState`, `ReadTimeoutMs`, `Instructions`, `ConnectionTerminated`, `SystemFaultReceived`, `RecordedCartesianPositionReceived`, `RecordedJointPositionReceived`, `UnknownPacketReceived`

## RmiConnectParametersBase

`class RmiConnectParametersBase`

Base class for RMI connection parameters.

- `RmiConnectParametersBase()`
- `const int DEFAULT_PORT = 16001`: Default RMI bootstrap port (16001).
- `const int DEFAULT_READ_TIMEOUT_MS = 2000`: Default RMI read timeout (infinite).
- `int Port { get; set; }`: RMI bootstrap port number.
- `int ReadTimeoutMs { get; set; }`: RMI read timeout in milliseconds.
