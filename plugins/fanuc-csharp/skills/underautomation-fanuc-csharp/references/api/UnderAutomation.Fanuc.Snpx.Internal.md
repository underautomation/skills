# UnderAutomation.Fanuc.Snpx.Internal

## AlarmAccess (robot.Snpx.ActiveAlarm)

`class AlarmAccess : SnpxAssignableElements<RobotAlarm, int>`

Provides access to robot alarms (active or historical) via SNPX.

- `RobotAlarm Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

## AlarmId

`enum AlarmId : short`

- ACAL: AccuCal II Error Code
- APPL: Application Shell Error
- APSH: Application Shell Error
- ARC: Arc Welding Application
- ASBN: Mnemonic Editor
- ATZN: AutoZone Error
- BBOX: Position Bumpbox Error
- BRCH: Brake Check Error
- CALM: CalMate Error
- CD: Coordinated Motion Softpart
- CMND: Command Processor Error
- CNTR: Continuous Turn Softpart
- COMP: Compensator Error
- COND: Condition Handler Error
- COPT: Common Options Error
- CPMO: Constant Path Error Code
- CUST: Customer-Specific Errors
- CVIS: Integrated Vision (Controller Vision)
- DIAG: IRDiagnostics
- DICT: Dictionary Processor
- DMDR: Dual Motion Drive Error
- DMER: Data Monitor Error
- DNET: DeviceNet Error
- DTBR: Data Transfer Between Robots
- DX: Delta Tool/Frame Softpart
- ELOG: Error Logger
- FILE: File System Error
- FLPY: Serial Floppy Disk System Error
- FORC: Impedance Control (Force Control)
- FRSY: Flash File System Error
- FXTL: C-Flex Tool Error
- HOST: Host Communications General Error
- HRTL: Host Communications Runtime Library Error
- IBS: InterBus-S Error
- ICRZ: IC Railzone Error
- IFPN: Interface Panel Error
- INTP: Interpreter Internal Error
- IRPK: IRPickTool Error
- ISD: Integral Servo Dispenser Error
- ISDT: Integral Servo Driven Tool Error
- JOG: Manual Jog Task Error
- KALM: KAREL Alarm Error
- LANG: Language Utility Error
- LECO: Arc Errors from Lincoln Electric
- LNTK: Line Tracking Error
- LSTP: Local Stop Error Codes
- MACR: Macro Option Error
- MARL: Material Removal Error
- MASI: Multi-Arm Sync Instructions Error
- MCTL: Motion Control Manager Error
- MEMO: Memory Manager Error
- MOTN: Motion Subsystem Error
- MUPS: Multi-Pass Motion Error
- OPTN: Option Installation Error
- OS: Operating System Error
- PALL: PalletTool Error
- PALT: Palletizing Application Error
- PICK: PickTool Error
- PMON: PC Monitor Error
- PNT1: Paint Application Errors (Post V6.31)
- PNT2: PaintTool Application Errors #2
- PRIO: Digital I/O Subsystem Error
- PROF: Profibus DP Error
- PROG: Program Interpreter Error
- PWD: Password Logging Error
- QMGR: KAREL Queue Manager Error
- RIPE: ROS IP Errors
- ROUT: SoftPart Built-in Routine for Interpreter Error
- RPC: RPC Error
- RPM: Root Pass Memorization Error
- RTCP: Remote TCP Error
- SCIO: Syntax Checking for Teach Pendant Programs Error
- SDTL: System Design Tool Error
- SEAL: Sealing Application Error
- SENS: Sensor Interface Error
- SHAP: Shape Generation Error
- SPOT: Spot Welding Application Error
- SPRM: Ramp Motion SoftPart Error
- SRIO: Serial Driver Error
- SRVO: Servo in Motion Sub-System Error
- SSPC: Special Space Checking Function Error
- SVGN: Servo Weld Gun Application Error
- SYST: System Error
- TAST: Through-Arc Seam Tracking Error
- TCPP: TCP Speed Prediction Error
- TG: Triggering Accuracy Error
- THSR: Touch Sensing SoftPart Error
- TJOG: Tracking Jog Error
- TMAT: Torch Mate Error
- TOOL: Servo Tool Change Error
- TPIF: Teach Pendant User Interface Error
- TRAK: Tracking SoftPart Error
- VARS: Variable Manager Subsystem Error
- WEAV: Weaving Error
- WNDW: Window I/O Manager Sub-System Error
- XMLF: XML Errors

## AlarmSeverity

`enum AlarmSeverity : short`

Represents the severity level of a robot alarm.

- ABORT_G: Global abort level alarm.
- ABORT_L: Local abort level alarm.
- NONE: No severity.
- PAUSE_G: Global pause level alarm.
- PAUSE_L: Local pause level alarm.
- SERVO: Servo error alarm.
- SERVO2: Servo error level 2 alarm.
- STOP_G: Global stop level alarm.
- STOP_L: Local stop level alarm.
- SYSTEM: System level alarm.
- WARN: Warning level alarm.

## AlarmType

`enum AlarmType`

Defines whether an alarm is active or historical.

- Active: Currently active alarm.
- History: Historical alarm from the alarm log.

## Assignment<TIndex>

`class Assignment<TIndex> : Assignment`

Represents a typed SNPX memory assignment with an index.

- `TIndex Index { get; }`: Gets the index of this assignment.
- Inherited from [Assignment](UnderAutomation.Fanuc.Snpx.Internal.md#assignment): `Offset`, `IsAssignmentCleared`, `Name`

## Assignment

`class Assignment`

Represents an SNPX assignment: an element of the robot that the SNPX client can read in one request.

- `bool IsAssignmentCleared { get; }`: Gets a value indicating whether this assignment has been cleared.
- `string Name { get; }`: Gets the display name of this assignment.
- `int Offset { get; }`: Gets the position of this assignment in the data of the SNPX client. Negative if cleared.

## BatchAssignment<TValue, TIndex>

`abstract class BatchAssignment<TValue, TIndex>`

Abstract base class for batch assignment operations that read multiple values at once.

- `Assignment<TIndex>[] Assignments`: The assignments included in this batch.
- `abstract TValue[] Read()`: Reads all values from the batch assignment.

## CommentData

`class CommentData`

Specifies the data type, index, and string length for reading or writing a comment via SNPX.

- `CommentData()`: Creates a new instance with default values.
- `CommentData(CommentType type, int index, int stringLength = 16)`: Creates a new instance with the specified type, index, and optional string length.
- `int Index { get; set; }`: The 1-based index of the element. Must be &gt;= 1.
- `int StringLength { get; set; }`: Number of characters to read/write. Must be even, &gt;= 2. Default is 16.
- `CommentType Type { get; set; }`: The type of data to read the comment for.

## CommentType

`enum CommentType`

Identifies the type of data for which a comment can be read or written.

- AI: Analog Input.
- AO: Analog Output.
- DI: Digital Input.
- DO: Digital Output.
- Flag: Flag
- GI: Group Input.
- GO: Group Output.
- PositionRegister: Position register PR[].
- RI: Remote Input.
- RO: Remote Output.
- Register: Numeric register R[].
- SI: System Input.
- SO: System Output.
- StringRegister: String register SR[].
- UI: User Input.
- UO: User Output.
- WI: Weld Input.
- WO: Weld Output.
- WSI: Wire Stick Input.
- WSO: Wire Stick Output.

## Comments (robot.Snpx.Comments)

`class Comments : SnpxWritableAssignableElements<string, CommentData, CommentBatchAssignment>`

Provides read/write access to comments of registers, I/O signals and other data via SNPX.

- `string Read(CommentType type, int index, int stringLength = 16)`: Reads the comment for the specified data type and index.
- `void Write(CommentType type, int index, string value, int stringLength = 16)`: Writes a comment for the specified data type and index.
- `CommentBatchAssignment CreateBatchAssignment(CommentData[] indexes)`: Creates a batch assignment for the specified indices.
- `Assignment<CommentData> GetOrCreateAssignment(CommentData index)`: Gets or creates an assignment for the specified index.

## CurrentPosition (robot.Snpx.CurrentPosition)

`class CurrentPosition : SnpxAssignableElements<Position, CurrentPositionRequest>`

Provides access to the current robot position via SNPX.

- `Position ReadUserFramePosition(int userFrame)`: Reads the current position in the specified user frame.
- `Position ReadUserFramePosition(int userFrame, int group)`: Reads the current position in the specified user frame and motion group.
- `Position ReadWorldPosition()`: Reads the current world position of the robot.
- `Position ReadWorldPosition(int group)`: Reads the current world position of the specified motion group.
- `Position Read(CurrentPositionRequest index)`: Reads the value at the specified index.
- `Assignment<CurrentPositionRequest> GetOrCreateAssignment(CurrentPositionRequest index)`: Gets or creates an assignment for the specified index.

## CurrentPositionRequest

`class CurrentPositionRequest`

Specifies the motion group and user frame for reading the current robot position.

- `CurrentPositionRequest()`
- `int Group { get; set; }`: Gets or sets the motion group number. Starts from 1.
- `int UserFrame { get; set; }`: Gets or sets the user frame number. Use 0 for World Frame

## CurrentTaskStatus (robot.Snpx.CurrentTaskStatus)

`class CurrentTaskStatus : SnpxAssignableElements<RobotTaskStatus, int>`

Provides access to the current task (program) status on the robot via SNPX. Index starts from 1.

- `RobotTaskStatus Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

## DigitalSignals (robot.Snpx.SDI)

`class DigitalSignals : SnpxElements<bool, int>`

Provides read/write access to digital I/O signals on the robot.

- `bool Read(int index)`: Reads the digital signal at the specified index.
- `bool[] Read(int firstIndex, ushort count)`: Reads a range of digital signals.
- `SegmentName SegmentName { get; }`: Gets the name of the family of signals of this signal group.
- `void Write(int index, bool value)`: Writes a value to the digital signal at the specified index.
- `void Write(int firstIndex, bool[] values)`: Writes values to consecutive digital signals.

## Flags (robot.Snpx.Flags)

`class Flags : SnpxWritableAssignableIndexableElements<bool, FlagBatchAssignment>`

Provides access to flag registers (F[]) on the robot via SNPX.

- `FlagBatchAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for reading multiple flags.
- `void Write(int index, bool value)`: Write value at a certain index.
- `bool Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

## IntegerSystemVariables (robot.Snpx.IntegerSystemVariables)

`class IntegerSystemVariables : SnpxWritableAssignableElements<int, string, IntegerSystemVariablesBatchAssignment>`

Provides access to integer system variables on the robot via SNPX.

- `void Write(string index, int value)`: Write value at a certain index.
- `IntegerSystemVariablesBatchAssignment CreateBatchAssignment(string[] indexes)`: Creates a batch assignment for the specified indices.
- `int Read(string index)`: Reads the value at the specified index.
- `Assignment<string> GetOrCreateAssignment(string index)`: Gets or creates an assignment for the specified index.

## NumericIO (robot.Snpx.GI)

`class NumericIO : SnpxElements<ushort, int>`

Provides read/write access to numeric (group/analog) I/O on the robot.

- `ushort Read(int index)`: Reads the numeric I/O value at the specified index.
- `ushort[] Read(int firstIndex, ushort count)`: Reads a range of numeric I/O values.
- `SegmentName SegmentName { get; }`: Gets the name of the family of signals of this I/O group.
- `void Write(int index, ushort value)`: Writes a value to the numeric I/O at the specified index.
- `void Write(int firstIndex, ushort[] values)`: Writes values to consecutive numeric I/O.

## NumericRegisters (robot.Snpx.NumericRegisters)

`class NumericRegisters : NumericRegistersBase<float, NumericRegistersBatchAssignment>`

Provides access to numeric registers as float (R[]) on the robot via SNPX.

- `NumericRegistersBatchAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for reading multiple numeric registers.
- `void Write(int index, float value)`: Write value at a certain index.
- `float Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

## NumericRegistersBase<TValue, TAssignment>

`abstract class NumericRegistersBase<TValue, TAssignment> : SnpxWritableAssignableIndexableElements<TValue, TAssignment> where TAssignment : BatchAssignment<TValue, int>, new()`

Provides access to numeric registers (R[]) on the robot via SNPX.

- `TAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for a range of consecutive indices.
- `void Write(int index, TValue value)`: Write value at a certain index.
- `TAssignment CreateBatchAssignment(int[] indexes)`: Creates a batch assignment for the specified indices.
- `TValue Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.
- `abstract TValue Read(int index)`: Reads the value at the specified index.

## NumericRegistersInt16 (robot.Snpx.NumericRegistersInt16)

`class NumericRegistersInt16 : NumericRegistersBase<short, NumericRegistersInt16BatchAssignment>`

Provides access to numeric registers as 16 bits integer (R[]) on the robot via SNPX.

- `NumericRegistersInt16BatchAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for reading multiple numeric registers.
- `void Write(int index, short value)`: Write value at a certain index.
- `short Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

## NumericRegistersInt32 (robot.Snpx.NumericRegistersInt32)

`class NumericRegistersInt32 : NumericRegistersBase<int, NumericRegistersInt32BatchAssignment>`

Provides access to numeric registers as 32 bits integer (R[]) on the robot via SNPX.

- `NumericRegistersInt32BatchAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for reading multiple numeric registers.
- `void Write(int index, int value)`: Write value at a certain index.
- `int Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

## PositionRegisters (robot.Snpx.PositionRegisters)

`class PositionRegisters : SnpxWritableAssignableIndexableElements<Position, PositionRegistersBatchAssignment>`

Provides access to position registers (PR[]) on the robot via SNPX.

- `PositionRegistersBatchAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for reading multiple position registers.
- `Position Read(int index)`: Reads the position at the specified register index.
- `void Write(int index, CartesianPosition cartesianPosition)`: Writes a Cartesian position to the specified position register.
- `void Write(int index, ExtendedCartesianPosition extendedCartesianPosition)`: Writes an extended Cartesian position to the specified position register.
- `void Write(int index, JointsPosition jointsPosition)`: Writes a joints position to the specified position register.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

## PositionSystemVariables (robot.Snpx.PositionSystemVariables)

`class PositionSystemVariables : SnpxWritableAssignableElements<Position, string, PositionSystemVariablesBatchAssignment>`

Provides access to position system variables on the robot via SNPX.

- `Position Read(string index)`: Reads the position at the specified system variable.
- `void Write(string variable, CartesianPosition cartesianPosition)`: Writes a Cartesian position to the specified system variable.
- `void Write(string variable, ExtendedCartesianPosition extendedCartesianPosition)`: Writes an extended Cartesian position to the specified system variable.
- `void Write(string variable, JointsPosition jointsPosition)`: Writes a joints position to the specified system variable.
- `PositionSystemVariablesBatchAssignment CreateBatchAssignment(string[] indexes)`: Creates a batch assignment for the specified indices.
- `Assignment<string> GetOrCreateAssignment(string index)`: Gets or creates an assignment for the specified index.

## RealSystemVariables (robot.Snpx.RealSystemVariables)

`class RealSystemVariables : SnpxWritableAssignableElements<float, string, RealSystemVariablesBatchAssignment>`

Provides access to real (float) system variables on the robot via SNPX.

- `void Write(string index, float value)`: Write value at a certain index.
- `RealSystemVariablesBatchAssignment CreateBatchAssignment(string[] indexes)`: Creates a batch assignment for the specified indices.
- `float Read(string index)`: Reads the value at the specified index.
- `Assignment<string> GetOrCreateAssignment(string index)`: Gets or creates an assignment for the specified index.

## RobotAlarm

`class RobotAlarm : IEquatable<RobotAlarm>`

Represents a robot alarm with its category, severity, time, and message.

- `RobotAlarm()`
- `AlarmId CauseId { get; set; }`: Cause Category
- `string CauseMessage { get; set; }`: Cause message
- `short CauseNumber { get; set; }`: Cause Number
- `static RobotAlarm FromBytes(byte[] bytes, Languages language, int start = 0)`: Creates a Internal.RobotAlarm from a byte array.
- `AlarmId Id { get; set; }`: Alarm Category
- `string Message { get; set; }`: Error Message
- `short Number { get; set; }`: Alarm Number
- `AlarmSeverity Severity { get; set; }`: Alarm Severity
- `string SeverityMessage { get; set; }`: Severity message
- `DateTime Time { get; set; }`: Occurrence Time

## RobotTaskState

`enum RobotTaskState`

Represents the execution state of a robot task.

- Paused: Task is paused.
- Running: Task is running.
- Stopped: Task is stopped.

## RobotTaskStatus

`class RobotTaskStatus : IEquatable<RobotTaskStatus>`

Represents the status of a running task on the robot controller.

- `RobotTaskStatus()`
- `string Caller { get; set; }`: Gets or sets the name of the calling program.
- `static RobotTaskStatus FromBytes(byte[] bytes, Languages language, int start = 0)`: Creates a Internal.RobotTaskStatus from a byte array.
- `short LineNumber { get; set; }`: Gets or sets the current line number in the program.
- `string ProgramName { get; set; }`: Gets or sets the name of the program being executed.
- `RobotTaskState State { get; set; }`: Gets or sets the current execution state of the task.

## SegmentName (robot.Snpx.SDI.SegmentName)

`enum SegmentName`

Identifies a family of I/O signals.

- AI: Analog Input.
- AO: Analog Output.
- GI: Group Input.
- GO: Group Output.
- PMC_D: PMC Data Table.
- PMC_K: PMC Keep Relay.
- PMC_R: PMC Internal Relay.
- RDI: Remote Digital Input.
- RDO: Remote Digital Output.
- SDI: Safety Digital Input.
- SDO: Safety Digital Output.
- SI: System Input.
- SO: System Output.
- UI: User Input.
- UO: User Output.
- WI: Weld Input.
- WO: Weld Output.
- WSI: Wire Stick Input.

## SimulationData

`class SimulationData`

Specifies the I/O type and index for reading or writing simulation status via SNPX.

- `SimulationData()`: Creates a new instance with default values.
- `SimulationData(SimulationType type, int index)`: Creates a new instance with the specified type and index.
- `int Index { get; set; }`: The 1-based index of the I/O. Must be &gt;= 1.
- `SimulationType Type { get; set; }`: The type of I/O.

## SimulationStatus (robot.Snpx.SimulationStatus)

`class SimulationStatus : SnpxWritableAssignableElements<bool, SimulationData, SimulationStatusBatchAssignment>`

Provides read/write access to I/O simulation status via SNPX.

- `bool Read(SimulationType type, int index)`: Reads the simulation status for the specified I/O type and index.
- `void Write(SimulationType type, int index, bool value)`: Sets the simulation status for the specified I/O type and index.
- `SimulationStatusBatchAssignment CreateBatchAssignment(SimulationData[] indexes)`: Creates a batch assignment for the specified indices.
- `Assignment<SimulationData> GetOrCreateAssignment(SimulationData index)`: Gets or creates an assignment for the specified index.

## SimulationType

`enum SimulationType`

Identifies the type of I/O for which simulation status can be read or written.

- AI: Analog Input.
- AO: Analog Output.
- DI: Digital Input.
- DO: Digital Output.
- GI: Group Input.
- GO: Group Output.
- RI: Remote Input.
- RO: Remote Output.
- WI: Weld Input.
- WO: Weld Output.
- WSI: Wire Stick Input.
- WSO: Wire Stick Output.

## SnpxAssignableElements<TValue, TIndex>

`abstract class SnpxAssignableElements<TValue, TIndex> : SnpxElements<TValue, TIndex>`

Abstract base class for SNPX elements that support memory assignment for efficient access.

- `Assignment<TIndex> GetOrCreateAssignment(TIndex index)`: Gets or creates an assignment for the specified index.
- `TValue Read(TIndex index)`: Reads the value at the specified index.

## SnpxClientBase (robot.Snpx)

`class SnpxClientBase`

Base class for Snpx internal and public client

- `NumericIO AI { get; }`: Analog Inputs
- `NumericIO AO { get; }`: Analog Outputs
- `AlarmAccess ActiveAlarm { get; }`: Current active alarms
- `AlarmAccess AlarmHistory { get; }`: Alarm history
- `void ClearAlarms()`: Clear all active alarms
- `void ClearAssignments()`: Clear all assignments
- `Comments Comments { get; }`: Comments of registers, I/O signals and other data
- `bool Connected { get; }`: Indicates if the SNPX underlying TCP client is connected to the robot
- `CurrentPosition CurrentPosition { get; }`: Current position in world or user frame
- `CurrentTaskStatus CurrentTaskStatus { get; }`: Current program tasks status. Index starts from 1.
- `DigitalSignals[] DigitalSignals { get; }`: List of all digital signal accessors (SDI, SDO, RDI, RDO, ...)
- `void Disconnect()`: Disconnect from the robot
- `Flags Flags { get; }`: Flags
- `NumericIO GI { get; }`: Group Inputs
- `NumericIO GO { get; }`: Group Outputs
- `Assignment[] GetAssignments()`: Gets all current assignments.
- `IntegerSystemVariables IntegerSystemVariables { get; }`: Integer variables
- `string Ip { get; }`: IP address of the connected robot.
- `Languages Language { get; set; }`: Controller language (default is English)
- `NumericIO[] NumericIOs { get; }`: List of all Numeric IOs accessors (GI, GO, AI, AO, ...)
- `NumericRegisters NumericRegisters { get; }`: Number registers R[] as floating point values
- `NumericRegistersInt16 NumericRegistersInt16 { get; }`: Number registers R[] as 16-bit integer values
- `NumericRegistersInt32 NumericRegistersInt32 { get; }`: Number registers R[] as 32-bit integer values
- `NumericIO PMC_D { get; }`: Programmable Machine Controller Data
- `DigitalSignals PMC_K { get; }`: Programmable Machine Controller Constants
- `DigitalSignals PMC_R { get; }`: Programmable Machine Controller Relays
- `bool PollAndGetUpdatedConnectedState()`: Checks the actual connection status via an active socket polling
- `PositionRegisters PositionRegisters { get; }`: Position registers
- `PositionSystemVariables PositionSystemVariables { get; }`: Position variables
- `DigitalSignals RDI { get; }`: Remote Digital Inputs
- `DigitalSignals RDO { get; }`: Remote Digital Outputs
- `RealSystemVariables RealSystemVariables { get; }`: Real variables
- `DigitalSignals SDI { get; }`: Safety Digital Inputs
- `DigitalSignals SDO { get; }`: Safety Digital Outputs
- `DigitalSignals SI { get; }`: System Inputs
- `DigitalSignals SO { get; }`: System Outputs
- `void SetVariable(string name, bool value)`: Set boolean variable without assignments.
- `void SetVariable(string name, double value)`: Set double variable without assignments.
- `void SetVariable(string name, int value)`: Set integer variable without assignments.
- `void SetVariable(string name, string value)`: Set string variable without assignments.
- `SimulationStatus SimulationStatus { get; }`: I/O simulation status
- `StringRegisters StringRegisters { get; }`: String registers
- `StringSystemVariables StringSystemVariables { get; }`: String variables
- `DigitalSignals UI { get; }`: User Inputs
- `DigitalSignals UO { get; }`: User Outputs
- `DigitalSignals WI { get; }`: Weld Inputs
- `DigitalSignals WO { get; }`: Weld Outputs
- `DigitalSignals WSI { get; }`: Weld System Inputs

## SnpxClientInternal (robot.Snpx)

`class SnpxClientInternal : SnpxClientBase`

Internal SNPX client used by the framework for establishing connections.

- Inherited from [SnpxClientBase](UnderAutomation.Fanuc.Snpx.Internal.md#snpxclientbase-robotsnpx): `PollAndGetUpdatedConnectedState`, `Disconnect`, `ClearAlarms`, `SetVariable`, `ClearAssignments`, `GetAssignments`, `Ip`, `NumericRegisters`, `NumericRegistersInt32`, `NumericRegistersInt16`, `PositionRegisters`, `StringRegisters`, `IntegerSystemVariables`, `RealSystemVariables`, `PositionSystemVariables`, `StringSystemVariables`, `DigitalSignals`, `SDI`, `SDO`, `RDI`, `RDO`, `UI`, `UO`, `SI`, `SO`, `WI`, `WO`, `WSI`, `PMC_K`, `PMC_R`, `NumericIOs`, `GI`, `GO`, `AI`, `AO`, `PMC_D`, `Flags`, `CurrentPosition`, `CurrentTaskStatus`, `ActiveAlarm`, `AlarmHistory`, `Comments`, `SimulationStatus`, `Language`, `Connected`

## SnpxConnectParametersBase

`class SnpxConnectParametersBase`

Base class for SNPX connection parameters.

- `SnpxConnectParametersBase()`
- `const int DEFAULT_PORT = 60008`: The default SNPX port number.
- `int Port { get; set; }`: Gets or sets the port number for the SNPX connection.

## SnpxElements<TValue, TIndex>

`abstract class SnpxElements<TValue, TIndex>`

Abstract base class for accessing SNPX elements by index.

- `abstract TValue Read(TIndex index)`: Reads the value at the specified index.

## SnpxWritableAssignableElements<TValue, TIndex, TAssignment>

`abstract class SnpxWritableAssignableElements<TValue, TIndex, TAssignment> : SnpxAssignableElements<TValue, TIndex> where TAssignment : BatchAssignment<TValue, TIndex>, new()`

Abstract base class for writable assignable SNPX elements.

- `TAssignment CreateBatchAssignment(TIndex[] indexes)`: Creates a batch assignment for the specified indices.
- `void Write(TIndex index, TValue value)`: Write value at a certain index.
- `TValue Read(TIndex index)`: Reads the value at the specified index.
- `Assignment<TIndex> GetOrCreateAssignment(TIndex index)`: Gets or creates an assignment for the specified index.
- `abstract TValue Read(TIndex index)`: Reads the value at the specified index.

## SnpxWritableAssignableIndexableElements<TValue, TAssignment>

`abstract class SnpxWritableAssignableIndexableElements<TValue, TAssignment> : SnpxWritableAssignableElements<TValue, int, TAssignment> where TAssignment : BatchAssignment<TValue, int>, new()`

Abstract base class for writable assignable elements accessed by integer index.

- `TAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for a range of consecutive indices.
- `void Write(int index, TValue value)`: Write value at a certain index.
- `TValue Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.
- `abstract TValue Read(int index)`: Reads the value at the specified index.

## StringRegisters (robot.Snpx.StringRegisters)

`class StringRegisters : SnpxWritableAssignableIndexableElements<string, StringRegistersBatchAssignment>`

Provides access to string registers (SR[]) on the robot via SNPX.

- `StringRegistersBatchAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for reading multiple string registers.
- `static int StringLength { get; set; }`: Number of characters for string register reads/writes. Must be even, greater than 2, and less than ushort.MaxValue. Warning: this static value must be set before any string register read/write and must not be changed while the SDK is running. Default: 80.
- `void Write(int index, string value)`: Write value at a certain index.
- `string Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

## StringSystemVariables (robot.Snpx.StringSystemVariables)

`class StringSystemVariables : SnpxWritableAssignableElements<string, string, StringSystemVariablesBatchAssignment>`

Provides access to string system variables on the robot via SNPX.

- `void Write(string index, string value)`: Write value at a certain index.
- `StringSystemVariablesBatchAssignment CreateBatchAssignment(string[] indexes)`: Creates a batch assignment for the specified indices.
- `string Read(string index)`: Reads the value at the specified index.
- `Assignment<string> GetOrCreateAssignment(string index)`: Gets or creates an assignment for the specified index.
