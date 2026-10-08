# underautomation.fanuc.snpx.internal

## AlarmAccess (robot.snpx.active_alarm)

`from underautomation.fanuc.snpx.internal.alarm_access import AlarmAccess`

Provides access to robot alarms (active or historical) via SNPX.

- `read(index: int) -> RobotAlarm`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## AlarmId

`from underautomation.fanuc.snpx.internal.alarm_id import AlarmId`

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

`from underautomation.fanuc.snpx.internal.alarm_severity import AlarmSeverity`

Represents the severity level of a robot alarm.

- NONE_: No severity.
- WARN: Warning level alarm.
- PAUSE_L: Local pause level alarm.
- PAUSE_G: Global pause level alarm.
- STOP_L: Local stop level alarm.
- STOP_G: Global stop level alarm.
- SERVO: Servo error alarm.
- ABORT_L: Local abort level alarm.
- ABORT_G: Global abort level alarm.
- SERVO2: Servo error level 2 alarm.
- SYSTEM: System level alarm.

## AlarmType

`from underautomation.fanuc.snpx.internal.alarm_type import AlarmType`

Defines whether an alarm is active or historical.

- Active: Currently active alarm.
- History: Historical alarm from the alarm log.

## Assignment1

`from underautomation.fanuc.snpx.internal.assignment_1 import Assignment1`

Represents a typed SNPX memory assignment with an index.

- `index: TIndex (read only)`: Gets the index of this assignment.
- Inherited from [Assignment](underautomation.fanuc.snpx.internal.md#assignment): `offset`, `is_assignment_cleared`, `name`

## Assignment

`from underautomation.fanuc.snpx.internal.assignment import Assignment`

Represents an SNPX memory assignment mapping a named element to a memory offset.

- `offset: int (read only)`: Gets the memory offset for this assignment. Negative if cleared.
- `is_assignment_cleared: bool (read only)`: Gets a value indicating whether this assignment has been cleared.
- `name: str (read only)`: Gets the display name of this assignment.

## BatchAssignment2

`from underautomation.fanuc.snpx.internal.batch_assignment_2 import BatchAssignment2`

Abstract base class for batch assignment operations that read multiple values at once.

- `read() -> typing.List[TValue]`: Reads all values from the batch assignment.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## CommentData

`from underautomation.fanuc.snpx.internal.comment_data import CommentData`

Specifies the data type, index, and string length for reading or writing a comment via SNPX.

- `CommentData(type: CommentType, index: int, stringLength: int)`: Creates a new instance with the specified type, index, and optional string length.
- `type: CommentType`: The type of data to read the comment for.
- `index: int`: The 1-based index of the element. Must be >= 1.
- `string_length: int`: Number of characters to read/write. Must be even, >= 2. Default is 16.

## CommentType

`from underautomation.fanuc.snpx.internal.comment_type import CommentType`

Identifies the type of data for which a comment can be read or written.

- Register: Numeric register R[].
- PositionRegister: Position register PR[].
- StringRegister: String register SR[].
- DI: Digital Input.
- DO: Digital Output.
- RI: Remote Input.
- RO: Remote Output.
- UI: User Input.
- UO: User Output.
- SI: System Input.
- SO: System Output.
- WI: Weld Input.
- WO: Weld Output.
- WSI: Wire Stick Input.
- WSO: Wire Stick Output.
- GI: Group Input.
- GO: Group Output.
- AI: Analog Input.
- AO: Analog Output.
- Flag: Flag

## Comments (robot.snpx.comments)

`from underautomation.fanuc.snpx.internal.comments import Comments`

Provides read/write access to comments of registers, I/O signals and other data via SNPX.

- `read(type: CommentType, index: int, stringLength: int=16) -> str`: Reads the comment for the specified data type and index.
- `write(type: CommentType, index: int, value: str, stringLength: int=16) -> None`: Writes a comment for the specified data type and index.
- `create_batch_assignment(indexes: typing.List[CommentData]) -> CommentBatchAssignment`: Creates a batch assignment for the specified indices.
- `get_or_create_assignment(index: CommentData) -> Assignment1[CommentData]`: Gets or creates an assignment for the specified index.

## CurrentPosition (robot.snpx.current_position)

`from underautomation.fanuc.snpx.internal.current_position import CurrentPosition`

Provides access to the current robot position via SNPX.

- `read_world_position(group: int) -> Position`: Reads the current world position of the specified motion group.
- `read_world_position() -> Position`: Reads the current world position of the robot.
- `read_user_frame_position(userFrame: int, group: int) -> Position`: Reads the current position in the specified user frame and motion group.
- `read_user_frame_position(userFrame: int) -> Position`: Reads the current position in the specified user frame.
- `read(index: CurrentPositionRequest) -> Position`: Reads the value at the specified index.
- `get_or_create_assignment(index: CurrentPositionRequest) -> Assignment1[CurrentPositionRequest]`: Gets or creates an assignment for the specified index.

## CurrentPositionRequest

`from underautomation.fanuc.snpx.internal.current_position_request import CurrentPositionRequest`

Specifies the motion group and user frame for reading the current robot position.

- `CurrentPositionRequest()`
- `group: int`: Gets or sets the motion group number. Starts from 1.
- `user_frame: int`: Gets or sets the user frame number. Use 0 for World Frame

## CurrentTaskStatus (robot.snpx.current_task_status)

`from underautomation.fanuc.snpx.internal.current_task_status import CurrentTaskStatus`

Provides access to the current task (program) status on the robot via SNPX. Index starts from 1.

- `read(index: int) -> RobotTaskStatus`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## DigitalSignals (robot.snpx.sdi)

`from underautomation.fanuc.snpx.internal.digital_signals import DigitalSignals`

Provides read/write access to digital I/O signals on the robot.

- `read(firstIndex: int, count: int) -> typing.List[bool]`: Reads a range of digital signals.
- `read(index: int) -> bool`: Reads the digital signal at the specified index.
- `write(firstIndex_or_index: int, value_or_values: bool | typing.List[bool]) -> None`: Writes a value to the digital signal at the specified index. Writes values to consecutive digital signals.
- `segment_name: SegmentName (read only)`: Gets the segment name identifying this signal group.

## Flags (robot.snpx.flags)

`from underautomation.fanuc.snpx.internal.flags import Flags`

Provides access to flag registers (F[]) on the robot via SNPX.

- `create_batch_assignment(startIndex: int, count: int) -> FlagBatchAssignment`: Creates a batch assignment for reading multiple flags.
- `write(index: int, value: bool) -> None`: Write value at a certain index.
- `read(index: int) -> bool`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## IntegerSystemVariables (robot.snpx.integer_system_variables)

`from underautomation.fanuc.snpx.internal.integer_system_variables import IntegerSystemVariables`

Provides access to integer system variables on the robot via SNPX.

- `write(index: str, value: int) -> None`: Write value at a certain index.
- `create_batch_assignment(indexes: typing.List[str]) -> IntegerSystemVariablesBatchAssignment`: Creates a batch assignment for the specified indices.
- `read(index: str) -> int`: Reads the value at the specified index.
- `get_or_create_assignment(index: str) -> Assignment1[str]`: Gets or creates an assignment for the specified index.

## NumericIO (robot.snpx.gi)

`from underautomation.fanuc.snpx.internal.numeric_io import NumericIO`

Provides read/write access to numeric (group/analog) I/O on the robot.

- `read(firstIndex: int, count: int) -> typing.List[int]`: Reads a range of numeric I/O values.
- `read(index: int) -> int`: Reads the numeric I/O value at the specified index.
- `write(firstIndex_or_index: int, value_or_values: int | typing.List[int]) -> None`: Writes a value to the numeric I/O at the specified index. Writes values to consecutive numeric I/O.
- `segment_name: SegmentName (read only)`: Gets the segment name identifying this I/O group.

## NumericRegisters (robot.snpx.numeric_registers)

`from underautomation.fanuc.snpx.internal.numeric_registers import NumericRegisters`

Provides access to numeric registers as float (R[]) on the robot via SNPX.

- `create_batch_assignment(startIndex: int, count: int) -> NumericRegistersBatchAssignment`: Creates a batch assignment for reading multiple numeric registers.
- `write(index: int, value: float) -> None`: Write value at a certain index.
- `read(index: int) -> float`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## NumericRegistersBase2

`from underautomation.fanuc.snpx.internal.numeric_registers_base_2 import NumericRegistersBase2`

Provides access to numeric registers (R[]) on the robot via SNPX.

- `create_batch_assignment(startIndex: int, count: int) -> TAssignment`: Creates a batch assignment for a range of consecutive indices.
- `write(index: int, value: TValue) -> None`: Write value at a certain index.
- `create_batch_assignment(indexes: typing.List[int]) -> TAssignment`: Creates a batch assignment for the specified indices.
- `read(index: int) -> TValue`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## NumericRegistersInt16 (robot.snpx.numeric_registers_int16)

`from underautomation.fanuc.snpx.internal.numeric_registers_int16 import NumericRegistersInt16`

Provides access to numeric registers as 16 bits integer (R[]) on the robot via SNPX.

- `create_batch_assignment(startIndex: int, count: int) -> NumericRegistersInt16BatchAssignment`: Creates a batch assignment for reading multiple numeric registers.
- `write(index: int, value: int) -> None`: Write value at a certain index.
- `read(index: int) -> int`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## NumericRegistersInt32 (robot.snpx.numeric_registers_int32)

`from underautomation.fanuc.snpx.internal.numeric_registers_int32 import NumericRegistersInt32`

Provides access to numeric registers as 32 bits integer (R[]) on the robot via SNPX.

- `create_batch_assignment(startIndex: int, count: int) -> NumericRegistersInt32BatchAssignment`: Creates a batch assignment for reading multiple numeric registers.
- `write(index: int, value: int) -> None`: Write value at a certain index.
- `read(index: int) -> int`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## PositionRegisters (robot.snpx.position_registers)

`from underautomation.fanuc.snpx.internal.position_registers import PositionRegisters`

Provides access to position registers (PR[]) on the robot via SNPX.

- `create_batch_assignment(startIndex: int, count: int) -> PositionRegistersBatchAssignment`: Creates a batch assignment for reading multiple position registers.
- `write(index: int, cartesianPosition_or_extendedCartesianPosition_or_jointsPosition: CartesianPosition | ExtendedCartesianPosition | JointsPosition) -> None`: Writes a Cartesian position to the specified position register. Writes an extended Cartesian position to the specified position register. Writes a joints position to the specified position register.
- `read(index: int) -> Position`: Reads the position at the specified register index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## PositionSystemVariables (robot.snpx.position_system_variables)

`from underautomation.fanuc.snpx.internal.position_system_variables import PositionSystemVariables`

Provides access to position system variables on the robot via SNPX.

- `write(variable: str, cartesianPosition_or_extendedCartesianPosition_or_jointsPosition: CartesianPosition | ExtendedCartesianPosition | JointsPosition) -> None`: Writes a Cartesian position to the specified system variable. Writes an extended Cartesian position to the specified system variable. Writes a joints position to the specified system variable.
- `read(index: str) -> Position`: Reads the position at the specified system variable.
- `create_batch_assignment(indexes: typing.List[str]) -> PositionSystemVariablesBatchAssignment`: Creates a batch assignment for the specified indices.
- `get_or_create_assignment(index: str) -> Assignment1[str]`: Gets or creates an assignment for the specified index.

## RealSystemVariables (robot.snpx.real_system_variables)

`from underautomation.fanuc.snpx.internal.real_system_variables import RealSystemVariables`

Provides access to real (float) system variables on the robot via SNPX.

- `write(index: str, value: float) -> None`: Write value at a certain index.
- `create_batch_assignment(indexes: typing.List[str]) -> RealSystemVariablesBatchAssignment`: Creates a batch assignment for the specified indices.
- `read(index: str) -> float`: Reads the value at the specified index.
- `get_or_create_assignment(index: str) -> Assignment1[str]`: Gets or creates an assignment for the specified index.

## RobotAlarm

`from underautomation.fanuc.snpx.internal.robot_alarm import RobotAlarm`

Represents a robot alarm with its category, severity, time, and message.

- `RobotAlarm()`
- `static from_bytes(bytes: typing.List[int], language: Languages, start: int=0) -> 'RobotAlarm'`: Creates a RobotAlarm from a byte array.
- `id: AlarmId`: Alarm Category
- `number: int`: Alarm Number
- `cause_id: AlarmId`: Cause Category
- `cause_number: int`: Cause Number
- `severity: AlarmSeverity`: Alarm Severity
- `time: datetime`: Occurrence Time
- `message: str`: Error Message
- `cause_message: str`: Cause message
- `severity_message: str`: Severity message

## RobotTaskState

`from underautomation.fanuc.snpx.internal.robot_task_state import RobotTaskState`

Represents the execution state of a robot task.

- Stopped: Task is stopped.
- Paused: Task is paused.
- Running: Task is running.

## RobotTaskStatus

`from underautomation.fanuc.snpx.internal.robot_task_status import RobotTaskStatus`

Represents the status of a running task on the robot controller.

- `RobotTaskStatus()`
- `static from_bytes(bytes: typing.List[int], language: Languages, start: int=0) -> 'RobotTaskStatus'`: Creates a RobotTaskStatus from a byte array.
- `program_name: str`: Gets or sets the name of the program being executed.
- `line_number: int`: Gets or sets the current line number in the program.
- `state: RobotTaskState`: Gets or sets the current execution state of the task.
- `caller: str`: Gets or sets the name of the calling program.

## SegmentName (robot.snpx.sdi.segment_name)

`from underautomation.fanuc.snpx.internal.segment_name import SegmentName`

Identifies the type of I/O segment.

- SDI: Safety Digital Input.
- SDO: Safety Digital Output.
- RDI: Remote Digital Input.
- RDO: Remote Digital Output.
- UI: User Input.
- UO: User Output.
- SI: System Input.
- SO: System Output.
- WI: Weld Input.
- WO: Weld Output.
- WSI: Wire Stick Input.
- PMC_K: PMC Keep Relay.
- PMC_R: PMC Internal Relay.
- AI: Analog Input.
- AO: Analog Output.
- GI: Group Input.
- GO: Group Output.
- PMC_D: PMC Data Table.

## SimulationData

`from underautomation.fanuc.snpx.internal.simulation_data import SimulationData`

Specifies the I/O type and index for reading or writing simulation status via SNPX.

- `SimulationData(type: SimulationType, index: int)`: Creates a new instance with the specified type and index.
- `type: SimulationType`: The type of I/O.
- `index: int`: The 1-based index of the I/O. Must be >= 1.

## SimulationStatus (robot.snpx.simulation_status)

`from underautomation.fanuc.snpx.internal.simulation_status import SimulationStatus`

Provides read/write access to I/O simulation status via SNPX.

- `read(type: SimulationType, index: int) -> bool`: Reads the simulation status for the specified I/O type and index.
- `write(type: SimulationType, index: int, value: bool) -> None`: Sets the simulation status for the specified I/O type and index.
- `create_batch_assignment(indexes: typing.List[SimulationData]) -> SimulationStatusBatchAssignment`: Creates a batch assignment for the specified indices.
- `get_or_create_assignment(index: SimulationData) -> Assignment1[SimulationData]`: Gets or creates an assignment for the specified index.

## SimulationType

`from underautomation.fanuc.snpx.internal.simulation_type import SimulationType`

Identifies the type of I/O for which simulation status can be read or written.

- DI: Digital Input.
- DO: Digital Output.
- RI: Remote Input.
- RO: Remote Output.
- WI: Weld Input.
- WO: Weld Output.
- WSI: Wire Stick Input.
- WSO: Wire Stick Output.
- GI: Group Input.
- GO: Group Output.
- AI: Analog Input.
- AO: Analog Output.

## SnpxAssignableElements2

`from underautomation.fanuc.snpx.internal.snpx_assignable_elements_2 import SnpxAssignableElements2`

Abstract base class for SNPX elements that support memory assignment for efficient access.

- `read(index: TIndex) -> TValue`
- `get_or_create_assignment(index: TIndex) -> Assignment1[TIndex]`: Gets or creates an assignment for the specified index.

## SnpxClientBase (robot.snpx)

`from underautomation.fanuc.snpx.internal.snpx_client_base import SnpxClientBase`

Base class for Snpx internal and public client

- `poll_and_get_updated_connected_state() -> bool`: Checks the actual connection status via an active socket polling
- `disconnect() -> None`: Disconnect from the robot
- `clear_alarms() -> None`: Clear all active alarms
- `set_variable(name: str, value: bool | float | int | str) -> None`: Set boolean variable without assignments. Set double variable without assignments. Set integer variable without assignments. Set string variable without assignments.
- `clear_assignments() -> None`: Clear all assignments
- `get_assignments() -> typing.List[Assignment]`: Gets all current assignments.
- `ip: str (read only)`: IP address of the connected robot.
- `numeric_registers: NumericRegisters (read only)`: Number registers R[] as floating point values
- `numeric_registers_int32: NumericRegistersInt32 (read only)`: Number registers R[] as 32-bit integer values
- `numeric_registers_int16: NumericRegistersInt16 (read only)`: Number registers R[] as 16-bit integer values
- `position_registers: PositionRegisters (read only)`: Position registers
- `string_registers: StringRegisters (read only)`: String registers
- `integer_system_variables: IntegerSystemVariables (read only)`: Integer variables
- `real_system_variables: RealSystemVariables (read only)`: Real variables
- `position_system_variables: PositionSystemVariables (read only)`: Position variables
- `string_system_variables: StringSystemVariables (read only)`: String variables
- `digital_signals: typing.List[DigitalSignals] (read only)`: List of all digital signal accessors (SDI, SDO, RDI, RDO, ...)
- `sdi: DigitalSignals (read only)`: Safety Digital Inputs
- `sdo: DigitalSignals (read only)`: Safety Digital Outputs
- `rdi: DigitalSignals (read only)`: Remote Digital Inputs
- `rdo: DigitalSignals (read only)`: Remote Digital Outputs
- `ui: DigitalSignals (read only)`: User Inputs
- `uo: DigitalSignals (read only)`: User Outputs
- `si: DigitalSignals (read only)`: System Inputs
- `so: DigitalSignals (read only)`: System Outputs
- `wi: DigitalSignals (read only)`: Weld Inputs
- `wo: DigitalSignals (read only)`: Weld Outputs
- `wsi: DigitalSignals (read only)`: Weld System Inputs
- `pmc_k: DigitalSignals (read only)`: Programmable Machine Controller Constants
- `pmc_r: DigitalSignals (read only)`: Programmable Machine Controller Relays
- `numeric_i_os: typing.List[NumericIO] (read only)`: List of all Numeric IOs accessors (GI, GO, AI, AO, ...)
- `gi: NumericIO (read only)`: Group Inputs
- `go: NumericIO (read only)`: Group Outputs
- `ai: NumericIO (read only)`: Analog Inputs
- `ao: NumericIO (read only)`: Analog Outputs
- `pmc_d: NumericIO (read only)`: Programmable Machine Controller Data
- `flags: Flags (read only)`: Flags
- `current_position: CurrentPosition (read only)`: Current position in world or user frame
- `current_task_status: CurrentTaskStatus (read only)`: Current program tasks status. Index starts from 1.
- `active_alarm: AlarmAccess (read only)`: Current active alarms
- `alarm_history: AlarmAccess (read only)`: Alarm history
- `comments: Comments (read only)`: Comments of registers, I/O signals and other data
- `simulation_status: SimulationStatus (read only)`: I/O simulation status
- `language: Languages`: Controller language (default is English)
- `connected: bool (read only)`: Indicates if the SNPX underlying TCP client is connected to the robot

## SnpxClientInternal (robot.snpx)

`from underautomation.fanuc.snpx.internal.snpx_client_internal import SnpxClientInternal`

Internal SNPX client used by the framework for establishing connections.

- Inherited from [SnpxClientBase](underautomation.fanuc.snpx.internal.md#snpxclientbase-robotsnpx): `poll_and_get_updated_connected_state`, `disconnect`, `clear_alarms`, `set_variable`, `clear_assignments`, `get_assignments`, `ip`, `numeric_registers`, `numeric_registers_int32`, `numeric_registers_int16`, `position_registers`, `string_registers`, `integer_system_variables`, `real_system_variables`, `position_system_variables`, `string_system_variables`, `digital_signals`, `sdi`, `sdo`, `rdi`, `rdo`, `ui`, `uo`, `si`, `so`, `wi`, `wo`, `wsi`, `pmc_k`, `pmc_r`, `numeric_i_os`, `gi`, `go`, `ai`, `ao`, `pmc_d`, `flags`, `current_position`, `current_task_status`, `active_alarm`, `alarm_history`, `comments`, `simulation_status`, `language`, `connected`

## SnpxConnectParametersBase

`from underautomation.fanuc.snpx.internal.snpx_connect_parameters_base import SnpxConnectParametersBase`

Base class for SNPX connection parameters.

- `SnpxConnectParametersBase()`
- `port: int`: Gets or sets the port number for the SNPX connection.
- `static DEFAULT_PORT: int`: The default SNPX port number.

## SnpxElements2

`from underautomation.fanuc.snpx.internal.snpx_elements_2 import SnpxElements2`

Abstract base class for accessing SNPX elements by index.

- `read(index: TIndex) -> TValue`: Reads the value at the specified index.

## SnpxWritableAssignableElements3

`from underautomation.fanuc.snpx.internal.snpx_writable_assignable_elements_3 import SnpxWritableAssignableElements3`

Abstract base class for writable assignable SNPX elements.

- `write(index: TIndex, value: TValue) -> None`: Write value at a certain index.
- `create_batch_assignment(indexes: typing.List[TIndex]) -> TAssignment`: Creates a batch assignment for the specified indices.
- `read(index: TIndex) -> TValue`: Reads the value at the specified index.
- `get_or_create_assignment(index: TIndex) -> Assignment1[TIndex]`: Gets or creates an assignment for the specified index.

## SnpxWritableAssignableIndexableElements2

`from underautomation.fanuc.snpx.internal.snpx_writable_assignable_indexable_elements_2 import SnpxWritableAssignableIndexableElements2`

Abstract base class for writable assignable elements accessed by integer index.

- `create_batch_assignment(startIndex: int, count: int) -> TAssignment`: Creates a batch assignment for a range of consecutive indices.
- `write(index: int, value: TValue) -> None`: Write value at a certain index.
- `read(index: int) -> TValue`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## StringRegisters (robot.snpx.string_registers)

`from underautomation.fanuc.snpx.internal.string_registers import StringRegisters`

Provides access to string registers (SR[]) on the robot via SNPX.

- `create_batch_assignment(startIndex: int, count: int) -> StringRegistersBatchAssignment`: Creates a batch assignment for reading multiple string registers.
- `static string_length: int`: Number of characters for string register reads/writes. Must be even, greater than 2, and less than ushort.MaxValue. Warning: this static value must be set before any string register read/write and must not be changed while the SDK is running. Default: 80.
- `write(index: int, value: str) -> None`: Write value at a certain index.
- `read(index: int) -> str`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

## StringSystemVariables (robot.snpx.string_system_variables)

`from underautomation.fanuc.snpx.internal.string_system_variables import StringSystemVariables`

Provides access to string system variables on the robot via SNPX.

- `write(index: str, value: str) -> None`: Write value at a certain index.
- `create_batch_assignment(indexes: typing.List[str]) -> StringSystemVariablesBatchAssignment`: Creates a batch assignment for the specified indices.
- `read(index: str) -> str`: Reads the value at the specified index.
- `get_or_create_assignment(index: str) -> Assignment1[str]`: Gets or creates an assignment for the specified index.
