# UnderAutomation.Fanuc.Cgtp

## CgtpAsciiFileItem

`class CgtpAsciiFileItem : CgtpFileItem`

Represents a file entry that has both a binary and an ASCII format.

- `CgtpAsciiFileItem()`
- `string AsciiFile { get; }`: ASCII format file name, or null if not available.
- Inherited from [CgtpFileItem](UnderAutomation.Fanuc.Cgtp.md#cgtpfileitem): `File`, `Comment`

## CgtpClient

`class CgtpClient : CgtpClientBase`

Standalone CGTP Web Server client for direct use without Fanuc.FanucRobot.

- `CgtpClient()`: Creates a new instance of the CGTP Web Server client.
- `void Connect(string ip, int port = 3080, int requestTimeoutMs = 3000, string login = null, string password = null)`: Connect to the CGTP Web Server on the controller.
- Inherited from [CgtpClientBase](UnderAutomation.Fanuc.Cgtp.Internal.md#cgtpclientbase-robotcgtp): `Disconnect`, `AbortTask`, `SelectProgram`, `DeleteProgram`, `GetProgramComment`, `SetProgramComment`, `GetProgramOwner`, `SetProgramOwner`, `GetProgramStackSize`, `SetProgramStackSize`, `GetProgramIgnorePause`, `SetProgramIgnorePause`, `GetProgramWriteProtect`, `SetProgramWriteProtect`, `GetProgramSubType`, `SetProgramSubType`, `CreateProgram`, `RenameProgram`, `ListPrograms`, `ListTpPrograms`, `DeleteSourceLines`, `InsertSourceLine`, `ReplaceSourceLine`, `SetProgramPositionToCurrentCartesianPosition`, `SetProgramPosition`, `RunProgram`, `ChangeActiveProgram`, `PauseAllPrograms`, `ReadVariableAsString`, `ReadVariable`, `WriteVariable`, `SetComment`, `WriteNumericRegisterAsDouble`, `WriteNumericRegisterAsInteger`, `WriteStringRegister`, `SetUserAlarmSeverity`, `ReadNumericRegistersWithComment`, `ReadStringRegistersWithComment`, `ReadUserAlarms`, `GetIoComments`, `GetComments`, `ReadNumericRegisterWithComment`, `ReadPositionRegisterWithComment`, `ReadBatchVariables`, `WritePositionRegisterAsCartesian`, `WritePositionRegisterAsJoint`, `WriteBatchVariables`, `ReadIo`, `WriteIo`, `GetIoSimulationStatus`, `SimulateIo`, `UnsimulateIo`, `ReadCartesianPosition`, `ReadJointPosition`, `InvertKinematics`, `ForwardKinematics`, `ListFiles`, `GetFileAsString`, `Kcl`, `Http`, `Language`, `Enabled`

## CgtpCommentIoType

`enum CgtpCommentIoType`

Type of I/O pair whose comments can be read via CGTP.

- AnalogIO: Analog I/O (AI/AO).
- DigitalIO: Digital I/O (DI/DO).
- GroupIO: Group I/O (GI/GO).
- RobotIO: Robot I/O (RI/RO).

## CgtpCommentType

`enum CgtpCommentType`

Type of element whose comment can be read or written via CGTP.

- AI: Analog input.
- AO: Analog output.
- DI: Digital input.
- DO: Digital output.
- Flag: Flag (F[]).
- GI: Group input.
- GO: Group output.
- NumericRegister: Numeric register (R[]).
- PositionRegister: Position register (PR[]).
- RI: Robot input.
- RO: Robot output.
- StringRegister: String register (SR[]).
- UserAlarm: User alarm.

## CgtpException

`class CgtpException : Exception, ISerializable, _Exception`

Represents an error returned by the FANUC controller via CGTP.

- `int Status { get; }`: The status code returned by the controller when available.

## CgtpFileItem

`class CgtpFileItem`

Represents a file entry returned by the controller's index pages.

- `CgtpFileItem()`
- `string Comment { get; }`: Comment associated with the file, if any.
- `string File { get; }`: File name on the controller.

## CgtpIoPortType

`enum CgtpIoPortType`

Type of I/O port on the controller.

- AI: Analog input.
- AO: Analog output.
- DI: Digital input.
- DO: Digital output.
- Flag: Flag.
- GI: Group input.
- GO: Group output.
- RI: Robot input.
- RO: Robot output.

## CgtpProgramSubType

`enum CgtpProgramSubType`

Sub-type of a TP program on the controller.

- Condition: Condition handler program.
- Job: Job program.
- Macro: Macro program.
- None: No specific sub-type.
- Process: Process program.

## CgtpProgramType

`enum CgtpProgramType`

Type of a TP program on the controller.

- Karel: Karel program
- Tp: TP program

## CgtpVariableType

`enum CgtpVariableType`

Data types that can be returned when reading a controller variable.

- Boolean: Boolean value (TRUE or FALSE).
- Byte: 8-bit byte value.
- CartesianPosition: Cartesian position (X, Y, Z, W, P, R with configuration).
- Config: Robot configuration string.
- Integer: 32-bit integer value.
- JointPose9: Joint position with up to 9 axes.
- JointPosition: Joint position (J1..J9).
- Numeric: Numeric value that can be either integer or real.
- POSITION: Full position type.
- Real: Double-precision floating-point value.
- Short: 16-bit short integer value.
- String: String value. The actual type code encodes the maximum string length.
- Vector: 3D vector (X, Y, Z).
- XYZWPR: XYZWPR position type.
- XYZWPRExt: Extended XYZWPR position with additional axes.

## CgtpVariableValue

`class CgtpVariableValue`

Represents the value of a controller variable with its data type.

- `bool BooleanValue { get; }`: Value interpreted as a boolean (TRUE/FALSE).
- `CartesianPositionVariable CartesianPositionValue { get; }`: Value interpreted as a Cartesian position.
- `Configuration ConfigurationValue { get; }`: Value interpreted as a robot configuration.
- `int IntegerValue { get; }`: Value interpreted as an integer.
- `JointPositionVariable JointPositionValue { get; }`: Value interpreted as a joint position.
- `double RealValue { get; }`: Value interpreted as a double-precision floating-point number.
- `int StringLength { get; }`: Maximum string length if the variable type is String
- `string StringValue { get; }`: Raw string value of the variable
- `CgtpVariableType Type { get; }`: Data type of the variable
- `VectorVariable VectorValue { get; }`: Value interpreted as a 3D vector.
