# API index: UnderAutomation Fanuc SDK, Python

SDK version 7.1.0. One line per public type, grouped by namespace: name, then summary. Open the namespace file to read the members of a type.

## underautomation.fanuc

File: [underautomation.fanuc.md](underautomation.fanuc.md)

- ConnectionParameters: Connection parameters
- FanucRobot: Main class of the SDK that represents a connection to a Fanuc robot

## underautomation.fanuc.cgtp

File: [underautomation.fanuc.cgtp.md](underautomation.fanuc.cgtp.md)

- CgtpAsciiFileItem: Represents a file entry that has both a binary and an ASCII format.
- CgtpClient: Standalone CGTP Web Server client for direct use without Fanuc.FanucRobot.
- CgtpCommentIoType: Type of I/O pair whose comments can be read via CGTP.
- CgtpCommentType: Type of element whose comment can be read or written via CGTP.
- CgtpException: Represents an error returned by the FANUC controller via CGTP.
- CgtpFileItem: Represents a file entry returned by the controller's index pages.
- CgtpIoPortType: Type of I/O port on the controller.
- CgtpProgramSubType: Sub-type of a TP program on the controller.
- CgtpProgramType: Type of a TP program on the controller.
- CgtpVariableType: Data types that can be returned when reading a controller variable.
- CgtpVariableValue: Represents the value of a controller variable with its data type.

## underautomation.fanuc.cgtp.batch_variables

File: [underautomation.fanuc.cgtp.batch_variables.md](underautomation.fanuc.cgtp.batch_variables.md)

- CgtpBatchReadResult: Result of a batch read operation.
- CgtpBatchVariables: Collection of batch variables to read from or write to the controller in a single operation. Provides convenience methods to add typed variables.
- CgtpBatchWriteResult: Result of a batch write operation.
- CgtpNumericRegister: Represents a numeric register (R[]) for batch read/write operations. A numeric register always has a comment and a numeric value (integer or real).
- CgtpPositionRegister: Represents a position register (PR[]) for batch read/write operations.
- CgtpStringRegister: Represents a string register (SR[]) for batch read/write operations. A string register always has a comment and a string value.
- CgtpStructureField: Represents a FIELD or ARRAY node inside a structured variable response.
- CgtpVariable: Represents a generic controller variable for batch read/write operations. Supports scalar values (integer, real, boolean, string, position, vector, configuration) and structured values (FIELD/ARRAY hierarchies).
- ICgtpBatchVariable: Common interface for all batch variable types used with batch read/write operations.

## underautomation.fanuc.cgtp.internal

File: [underautomation.fanuc.cgtp.internal.md](underautomation.fanuc.cgtp.internal.md)

- CgtpClientBase: Base implementation for the CGTP Web Server client.
- CgtpClientInternal: Internal CGTP Web Server client used by the library infrastructure.
- CgtpConnectParametersBase: Base class for CGTP Web Server connection parameters.
- CgtpHttpClient: Provides methods to download and list files from the controller via HTTP.
- CgtpKclClient: KCL client that uses the web server of the controller (CGTP) instead of Telnet. It has the same commands as the Telnet KCL client and does not need a Telnet password. Some commands (Abort, AbortAll, ClearProgram, ClearVars, Continue, Hold, Pause, Run, StepOn, StepOff, SendCustomCommandUnsafe) are...

## underautomation.fanuc.common

File: [underautomation.fanuc.common.md](underautomation.fanuc.common.md)

- ArmFrontBack: Arm configuration
- ArmLeftRight: Arm left right
- ArmUpDown: Arm configuration
- CartesianPosition: Fanuc cartesian position and rotations
- CartesianPositionVariable: Represents a Cartesian position variable parsed from a Fanuc variable file
- CartesianPositionWithTool: A cartesian position with a tool ID
- CartesianPositionWithUserFrame: A cartesian tool position with a user frame ID
- CgtpConnectParameters: CGTP Web Server connection parameters
- Configuration: Fanuc arm configuration
- ConnectException: Exception thrown when connection to the robot fails
- DigitalPorts: Fanuc digital port types
- ExtendedCartesianPosition: Cartesian position with extended axes (E1, E2, E3)
- FtpConnectParameters: Memory access parameters
- IOComments: Contains input and output comment arrays for an I/O type.
- IOStatus: A digital port status
- JointPositionVariable: Represents a joint position variable parsed from a Fanuc variable file
- JointsPosition: Joints position in degrees
- Languages: Languages supported by the Fanuc robots
- NumericRegister: Represents a numeric register value that can be either integer or real.
- NumericRegisterWithComment: Represents a numeric register with an associated comment.
- Position: Robot position with joints and cartesian representations
- PositionRegister: Represents a position register that can hold either a Cartesian or joint position
- PositionRegisterWithComment: Represents a position register with an associated comment.
- ProgramType: Represents the type of a program.
- Quaternion: Quaternion that represents an orientation (Qw + Qx.i + Qy.j + Qz.k). Use XYZWPRPosition.GetQuaternion and Common.Quaternion) to convert from and to W, P, R angles.
- RmiConnectParameters: RMI parameters
- SnpxConnectParameters: SNPX parameters
- StreamMotionConnectParameters: Stream Motion connection parameters (J519 option)
- StringRegisterWithComment: Represents a string register with an associated comment.
- StringUtils: Contains string related utility methods
- TaskStatus: Represents the status of a task.
- TelnetConnectParameters: Connection parameters of the Telnet KCL client (remote commands). Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on the web server of the co...
- UserAlarmDefinition: Represents a user alarm definition with a comment and severity level.
- VectorVariable: Represents a 3D vector variable with X, Y, Z components
- WristFlip: Wrist configuration
- XYZPosition: Cartesian position X, Y, Z
- XYZWPRPosition: Cartesian position X, Y, Z with W, P, R rotations

## underautomation.fanuc.common.files

File: [underautomation.fanuc.common.files.md](underautomation.fanuc.common.files.md)

- FanucFileReaders: Contains static functions to decode Fanuc files (variables, diagnosis, listing, ...)
- FileClientBase: Base class for Fanuc file client. It provides methods to read and parse known files such as summary diagnostic, error list, current position, ...
- FileReader1: File reader for specific files
- FileReader: Read and decode fanuc files
- IFanucContent: Interface of a file that comes from a Fanuc controller
- IFileReader1: Interface for Fanuc file readers
- IFileReader: Interface for Fanuc file readers
- KnownVariableFiles: Wrapper class of methods to download and decode variable files
- OnProgressDelegate: Delegate to track File transfer progress. The value provided is in the range 0 to 100
- SectionParser1: Abstract generic section parser that creates and populates a section of type T.
- SectionParser: Abstract base class for parsing sections of diagnostic files.

## underautomation.fanuc.common.files.diagnosis

File: [underautomation.fanuc.common.files.diagnosis.md](underautomation.fanuc.common.files.diagnosis.md)

- CurrentPosition: Contains the position for each robots
- CurrentPositionReader: Parser for reading and interpreting current robot position data from diagnostic files.
- DiagnosisReader2: Generic diagnosis file reader that parses a specific section from a diagnostic stream.
- Feature: Represents a single software feature installed on the controller.
- Features: Represents the collection of features available on the controller.
- FeaturesParser: Parser for reading and interpreting controller feature data from diagnostic files.
- GroupPosition: Complete position information of a group
- HeaderSection: Header information of a diagnostic file
- IOState: Status of all controller inputs and outputs
- IOStateParser: Parser for reading and interpreting IO state data from diagnostic files.
- ProgramStates: Implements IFanucContent to hold a collection of task states.
- ProgramStatesParser: Parser for the "TASK STATES" section, renamed from ProgramStatesReader to ProgramStatesParser. Uses compiled Regex for efficiency.
- SafetyStatus: Safety status informations
- SafetyStatusParser: Parser for reading and interpreting safety status signals from diagnostic files.
- SummaryDiagnosis: All diagnosis information
- SummaryDiagnosisReader: Read and parse the file summary.dg
- TaskHistoryData: Represents one frame in the task's call stack.
- TaskState: Represents a single task's state.

## underautomation.fanuc.common.files.list

File: [underautomation.fanuc.common.files.list.md](underautomation.fanuc.common.files.list.md)

- ErrallSectionItem: Represents a single error item from the ERRALL error log
- ErrorList: Represents the parsed content of the ERRALL.LS error log file
- ErrorListReader: Reader for the ERRALL.LS error log file

## underautomation.fanuc.common.files.variables

File: [underautomation.fanuc.common.files.variables.md](underautomation.fanuc.common.files.variables.md)

- AavmmainFile: Describes the Fanuc variable file aavmmain.va
- ArrayElement: Describes all elements inside an array. Basically, a wrapping of GenericField where some properties are inherited from it
- BicsetupFile: Describes the Fanuc variable file bicsetup.va
- CbparamFile: Describes the Fanuc variable file cbparam.va
- CellioFile: Describes the Fanuc variable file cellio.va
- ComsetFile: Describes the Fanuc variable file comset.va
- DiocfgsvFile: Describes the Fanuc variable file diocfgsv.va
- GemdataFile: Describes the Fanuc variable file gemdata.va
- GenericField: Represents a named field within a variable structure
- GenericValue: Represents a generic variable value with optional child fields
- GenericVariable: Represents a top-level variable declaration with scope and storage information
- GenericVariableFile: Represents a parsed Fanuc variable file containing one or more variables
- GenericVariableTypeHelpers: Extension methods for IGenericVariableType
- HtcolrecFile: Describes the Fanuc variable file htcolrec.va
- HttpkclFile: Describes the Fanuc variable file httpkcl.va
- IrcCounterFile: Describes the Fanuc variable file irc_counter.va
- IrcMsgFile: Describes the Fanuc variable file irc_msg.va
- IrcStatusFile: Describes the Fanuc variable file irc_status.va
- IrcStlabelFile: Describes the Fanuc variable file irc_stlabel.va
- KlactionFile: Describes the Fanuc variable file klaction.va
- MixlogicFile: Describes the Fanuc variable file mixlogic.va
- MtparamFile: Describes the Fanuc variable file mtparam.va
- NumregFile: Describes the Fanuc variable file numreg.va
- PalregFile: Describes the Fanuc variable file palreg.va
- PosregFile: Describes the Fanuc variable file posreg.va
- StrregFile: Describes the Fanuc variable file strreg.va
- SwiupdtFile: Describes the Fanuc variable file swiupdt.va
- SycldintFile: Describes the Fanuc variable file sycldint.va
- SymotnFile: Describes the Fanuc variable file symotn.va
- SynosaveFile: Describes the Fanuc variable file synosave.va
- SysframeFile: Describes the Fanuc variable file sysframe.va
- SysfsacFile: Describes the Fanuc variable file sysfsac.va
- SyshostFile: Describes the Fanuc variable file syshost.va
- SysmacroFile: Describes the Fanuc variable file sysmacro.va
- SysmastFile: Describes the Fanuc variable file sysmast.va
- SyspassFile: Describes the Fanuc variable file syspass.va
- SysservoFile: Describes the Fanuc variable file sysservo.va
- SystemFile: Describes the Fanuc variable file system.va
- SysuifFile: Describes the Fanuc variable file sysuif.va
- TpsnapFile: Describes the Fanuc variable file tpsnap.va
- ValueKind: Describes the kind of a variable value
- VariableFile: Abstract base class for typed variable file readers
- VariableFileList: Collection of variable files that aggregates all variables from the controller
- VariableReader1: Typed variable file reader for specific variable file types
- VariableReader: Reader for Fanuc variable files (*.va)
- VcmrinitFile: Describes the Fanuc variable file vcmrinit.va

## underautomation.fanuc.common.kcl

File: [underautomation.fanuc.common.kcl.md](underautomation.fanuc.common.kcl.md)

- AbortResult: Result of an abort command.
- AddBreakpointResult: Result of adding a breakpoint.
- BaseResult: Base class for simple results that store error text from the response.
- Breakpoint: Represents a breakpoint set on a task line.
- BreakpointsResult: Result containing the breakpoints of a task.
- ContinueResult: Result of a continue command.
- CustomCommandResult: Result of a custom KCL command.
- GetCurrentPoseResult: Result of a get current pose command.
- GetVariableResult: Result of a get variable command containing the raw value.
- KCLPorts: Enum representing the different KCL ports.
- KclClientBase: Abstract base class for KCL (Keyboard Command Line) clients. Provides all KCL commands shared between Telnet and CGTP implementations.
- PauseResult: Result of a pause command.
- ProgramCommandResult: Result of a program command (abort, continue, hold, pause, run, etc.).
- RemoveBreakpointResult: Result of removing a breakpoint.
- ResetResult: Result of a reset command.
- Result: Abstract base class for all KCL command results.
- RunResult: Result of a run command.
- SetPortResult: Result of a set port command.
- SetValueResult: Base class for results that contain a former and new value.
- SetVariableResult: Result of a set variable command.
- SimulateResult: Result of a simulate port command.
- StepOffResult: Result of the step off command.
- StepOnResult: Result of the step on command.
- TaskInformationResult: Result of the show task command containing task properties.
- UnsimulateAllResult: Result of an unsimulate all command.
- UnsimulateResult: Result of an unsimulate port command.
- VariableResult: Result of a show variable command.
- VariablesResult: Result of a show variables command.

## underautomation.fanuc.ftp

File: [underautomation.fanuc.ftp.md](underautomation.fanuc.ftp.md)

- FtpClient: FTP Client connection to a robot
- FtpExistsBehavior: Defines the behavior for handling files that already exist
- FtpFileSystemObjectType: Type of file system of object
- FtpListItem: Represents a file system object on the controller

## underautomation.fanuc.ftp.internal

File: [underautomation.fanuc.ftp.internal.md](underautomation.fanuc.ftp.internal.md)

- FtpClientBase: Base class for FTP features
- FtpClientInternal: Internal implementation of FTP Client
- FtpConnectParametersBase: Parameters to connect to Fanuc controller FTP server
- FtpDirectFileHandling: Methods to handle files on a Fanuc controller (upload, download, delete, enumerate, ...). The controller can refuse an operation: the rights depend on the FTP user and on the password settings of the controller (for example, an upload of a program needs a user with enough rights), and a program t...

## underautomation.fanuc.kinematics

File: [underautomation.fanuc.kinematics.md](underautomation.fanuc.kinematics.md)

- ArmKinematicModels: Fanuc Robot Known Arm Models
- DhParameters: Denavit-Hartenberg parameters for a 6-axis robot arm.
- IDhParameters: Interface defining the Denavit-Hartenberg parameters for a 6-axis robot arm.
- KinematicsCategory: Category of kinematics model for a robot arm.
- KinematicsUtils: Kinematics utilities

## underautomation.fanuc.kinematics.crx

File: [underautomation.fanuc.kinematics.crx.md](underautomation.fanuc.kinematics.crx.md)

- CrxKinematicsUtils: Utility methods implementing CRX collaborative robot inverse kinematics using a geometric approach.

## underautomation.fanuc.kinematics.opw

File: [underautomation.fanuc.kinematics.opw.md](underautomation.fanuc.kinematics.opw.md)

- OpwKinematicsUtils: Utility methods implementing OPW kinematics for a 6R industrial robot with ortho-parallel base and spherical wrist (so called 3-2-1 structure). This class is a C# implementation of the analytical solution described in: M. Brandstötter et al., "An Analytical Solution of the Inverse Kinematics Prob...

## underautomation.fanuc.license

File: [underautomation.fanuc.license.md](underautomation.fanuc.license.md)

- InvalidLicenseException: Exception thrown while using the product if the license is not valid.
- LicenseInfo: Information about a license key
- LicenseState: States that can take a license

## underautomation.fanuc.motion

File: [underautomation.fanuc.motion.md](underautomation.fanuc.motion.md)

- FanucMotion: Conversions between the FANUC types (positions, FINE/CNT/CR terminations, I/O types) and the types of the motion planner of namespace UnderAutomation.Robotics.Motion.

## underautomation.fanuc.rmi

File: [underautomation.fanuc.rmi.md](underautomation.fanuc.rmi.md)

- RmiClient: RMI client for connecting to and controlling FANUC robots via the Remote Motion Interface protocol.
- RmiException: Represents an error reported by the FANUC RMI controller or thrown by the client runtime.

## underautomation.fanuc.rmi.data

File: [underautomation.fanuc.rmi.data.md](underautomation.fanuc.rmi.data.md)

- RmiCartesianPositionResponse: Result of reading the current Cartesian position.
- RmiControllerErrorTextResponse: Result of reading the most recent controller error text.
- RmiControllerStatusResponse: Status snapshot returned by FRC_GetStatus.
- RmiDigitalInputValueResponse: Result of reading a digital input.
- RmiExtendedControllerStatusResponse: Extended controller status returned by FRC_GetExtStatus.
- RmiIndexedFrameResponse: Cartesian frame data paired with an index (UFRAME or UTOOL number).
- RmiInitializeResponse: Response to the Initialize command, which starts the RMI motion program on the controller.
- RmiInstructionResponse: Response returned immediately when a motion instruction is queued. The RmiInstructionResponse.Status property and RmiResponseBase.ErrorId are updated in the background as the controller processes the instruction. Use WaitForCompletion(System.Int32) to block until the instruction reaches a termina...
- RmiInstructionStatus: Execution state of an RMI instruction in the pipeline.
- RmiIoPortType: IO port type for generic read/write operations.
- RmiIoPortValueResponse: Result of reading a generic IO port.
- RmiJointAnglesSampleResponse: Result of reading the current joint angles.
- RmiJointSpeedType: Speed type for joint motion commands.
- RmiLinearSpeedType: Speed type for linear and circular motion commands.
- RmiNumericRegisterValueResponse: Result of reading a numeric register.
- RmiOnOff: Generic ON/OFF string values used by RMI.
- RmiPltzMode: Palletizing motion mode passed to Data.RmiPltzMode%7d). Requires MajorVersion &gt;= 7.
- RmiPortType: Digital port type used with Local Condition Block (LCB).
- RmiPositionRegisterDataResponse: Position register data paired with its register number.
- RmiRecordedCartesianPosition: Cartesian position received from the controller via the RMI Position Record menu (TouchUp).
- RmiRecordedJointPosition: Joint position received from the controller via the RMI Position Record menu (TouchUp).
- RmiResponseBase: Base class for RMI responses that return an error id from the controller.
- RmiSetPayloadCompensationParameters: Parameters for defining payload compensation for a payload schedule. Used by Data.RmiSetPayloadCompensationParameters). All positional values are in meters; mass in kg; inertia in kg·m².
- RmiSetPayloadParameters: Parameters for defining payload mass, center of gravity, and optionally inertia for a payload schedule. Used by Data.RmiSetPayloadParameters). All positional values are in meters; mass in kg; inertia in kg·m².
- RmiTcpSpeedResponse: Result of reading TCP speed.
- RmiTerminationType: Termination type for motion.
- RmiTimedResponse: Base class for responses with a controller RmiTimedResponse.TimeTag value.
- RmiUFrameUToolNumbersResponse: Current UFRAME and UTOOL numbers, optionally scoped to a motion group.
- RmiVariableValueResponse: Result of reading a system variable.

## underautomation.fanuc.rmi.internal

File: [underautomation.fanuc.rmi.internal.md](underautomation.fanuc.rmi.internal.md)

- RmiClientBase: High-level Remote Motion Interface (RMI) client for FANUC controllers. Manages the connection lifecycle, all administrative commands, and the full set of motion instruction packets over the RMI TCP protocol.
- RmiClientInternal: Internal RMI client used by the library infrastructure.
- RmiConnectParametersBase: Base class for RMI connection parameters.

## underautomation.fanuc.rmi.tp_instructions

File: [underautomation.fanuc.rmi.tp_instructions.md](underautomation.fanuc.rmi.tp_instructions.md)

- CallProgramTpInstruction: Instruction for a CALL program instruction. Pass to TpInstructions.RmiInstructionBase). Requires MajorVersion &gt;= 4.
- CartesianMotionTpInstructionBase: Extends TpInstructions.FullMotionTpInstructionBase with a Cartesian target position. Base class for all Cartesian motion instruction types.
- CircularMotionTpInstruction: Instruction for a circular motion (C in TP), Cartesian target representation. Pass to TpInstructions.RmiInstructionBase).
- CircularRelativeTpInstruction: Instruction for an incremental circular motion (C in TP), Cartesian delta representation. Pass to TpInstructions.RmiInstructionBase).
- FullMotionTpInstructionBase: Extends TpInstructions.MotionTpInstructionBase with the full set of optional motion modifiers shared by all non-simplified instruction types.
- JRepMotionTpInstructionBase: Extends TpInstructions.FullMotionTpInstructionBase with a joint-angle target. Base class for all joint-representation motion instruction types.
- JointMotionJRepTpInstruction: Instruction for a joint motion (J in TP), joint-angle representation, full options. Pass to TpInstructions.RmiInstructionBase).
- JointMotionTpInstruction: Instruction for a joint motion (J in TP), Cartesian target representation. Pass to TpInstructions.RmiInstructionBase).
- JointRelativeJRepTpInstruction: Instruction for an incremental joint motion (J in TP), joint-angle representation, full options. Pass to TpInstructions.RmiInstructionBase).
- JointRelativeTpInstruction: Instruction for an incremental joint motion (J in TP), Cartesian delta representation. Pass to TpInstructions.RmiInstructionBase).
- LinearMotionJRepTpInstruction: Instruction for a linear motion (L in TP), joint-angle representation. Pass to TpInstructions.RmiInstructionBase).
- LinearMotionTpInstruction: Instruction for a linear motion (L in TP), Cartesian target representation. Pass to TpInstructions.RmiInstructionBase).
- LinearRelativeJRepTpInstruction: Instruction for an incremental linear motion (L in TP), joint-angle representation. Pass to TpInstructions.RmiInstructionBase).
- LinearRelativeTpInstruction: Instruction for an incremental linear motion (L in TP), Cartesian delta representation. Pass to TpInstructions.RmiInstructionBase).
- MotionTpInstructionBase: Base class for all RMI motion instructions. Carries the three parameters that are mandatory on every motion instruction.
- RmiInstructionBase: Base class for all RMI TP instructions. Pass an instance to TpInstructions.RmiInstructionBase) to queue the instruction on the controller.
- SetPayloadTpInstruction: Instruction for a PAYLOAD[n] schedule selection. Pass to TpInstructions.RmiInstructionBase).
- SetUFrameTpInstruction: Instruction for a UFRAME_NUM = n assignment. Pass to TpInstructions.RmiInstructionBase).
- SetUToolTpInstruction: Instruction for a UTOOL_NUM = n assignment. Pass to TpInstructions.RmiInstructionBase).
- SplineMotionJRepTpInstruction: Instruction for a spline motion with joint-angle representation. Pass to TpInstructions.RmiInstructionBase). Requires MajorVersion &gt;= 7.
- SplineMotionTpInstruction: Instruction for a spline motion with a Cartesian target. Pass to TpInstructions.RmiInstructionBase). Requires MajorVersion &gt;= 7.
- WaitDinTpInstruction: Instruction for a WAIT DI[n] = value condition. Pass to TpInstructions.RmiInstructionBase).
- WaitTimeTpInstruction: Instruction for a WAIT t (sec) time delay. Pass to TpInstructions.RmiInstructionBase).

## underautomation.fanuc.snpx

File: [underautomation.fanuc.snpx.md](underautomation.fanuc.snpx.md)

- SnpxClient: SNPX protocol client for communicating with Fanuc robots.

## underautomation.fanuc.snpx.assignment

File: [underautomation.fanuc.snpx.assignment.md](underautomation.fanuc.snpx.assignment.md)

- CommentBatchAssignment: Batch assignment for reading multiple comments at once.
- FlagBatchAssignment: Batch assignment for reading multiple flag values at once.
- IntegerSystemVariablesBatchAssignment: Batch assignment for reading multiple integer system variables at once.
- NumericRegistersBatchAssignment: Batch assignment for reading multiple numeric registers at once as float
- NumericRegistersInt16BatchAssignment: Batch assignment for reading multiple numeric registers at once as 16-bit integers.
- NumericRegistersInt32BatchAssignment: Batch assignment for reading multiple numeric registers at once as 32-bit integers.
- PositionRegistersBatchAssignment: Batch assignment for reading multiple position registers at once.
- PositionSystemVariablesBatchAssignment: Batch assignment for reading multiple position system variables at once.
- RealSystemVariablesBatchAssignment: Batch assignment for reading multiple real (float) system variables at once.
- SimulationStatusBatchAssignment: Batch assignment for reading multiple I/O simulation statuses at once.
- StringRegistersBatchAssignment: Batch assignment for reading multiple string registers at once.
- StringSystemVariablesBatchAssignment: Batch assignment for reading multiple string system variables at once.

## underautomation.fanuc.snpx.internal

File: [underautomation.fanuc.snpx.internal.md](underautomation.fanuc.snpx.internal.md)

- AlarmAccess: Provides access to robot alarms (active or historical) via SNPX.
- AlarmId
- AlarmSeverity: Represents the severity level of a robot alarm.
- AlarmType: Defines whether an alarm is active or historical.
- Assignment1: Represents a typed SNPX memory assignment with an index.
- Assignment: Represents an SNPX assignment: an element of the robot that the SNPX client can read in one request.
- BatchAssignment2: Abstract base class for batch assignment operations that read multiple values at once.
- CommentData: Specifies the data type, index, and string length for reading or writing a comment via SNPX.
- CommentType: Identifies the type of data for which a comment can be read or written.
- Comments: Provides read/write access to comments of registers, I/O signals and other data via SNPX.
- CurrentPosition: Provides access to the current robot position via SNPX.
- CurrentPositionRequest: Specifies the motion group and user frame for reading the current robot position.
- CurrentTaskStatus: Provides access to the current task (program) status on the robot via SNPX. Index starts from 1.
- DigitalSignals: Provides read/write access to digital I/O signals on the robot.
- Flags: Provides access to flag registers (F[]) on the robot via SNPX.
- IntegerSystemVariables: Provides access to integer system variables on the robot via SNPX.
- NumericIO: Provides read/write access to numeric (group/analog) I/O on the robot.
- NumericRegisters: Provides access to numeric registers as float (R[]) on the robot via SNPX.
- NumericRegistersBase2: Provides access to numeric registers (R[]) on the robot via SNPX.
- NumericRegistersInt16: Provides access to numeric registers as 16 bits integer (R[]) on the robot via SNPX.
- NumericRegistersInt32: Provides access to numeric registers as 32 bits integer (R[]) on the robot via SNPX.
- PositionRegisters: Provides access to position registers (PR[]) on the robot via SNPX.
- PositionSystemVariables: Provides access to position system variables on the robot via SNPX.
- RealSystemVariables: Provides access to real (float) system variables on the robot via SNPX.
- RobotAlarm: Represents a robot alarm with its category, severity, time, and message.
- RobotTaskState: Represents the execution state of a robot task.
- RobotTaskStatus: Represents the status of a running task on the robot controller.
- SegmentName: Identifies a family of I/O signals.
- SimulationData: Specifies the I/O type and index for reading or writing simulation status via SNPX.
- SimulationStatus: Provides read/write access to I/O simulation status via SNPX.
- SimulationType: Identifies the type of I/O for which simulation status can be read or written.
- SnpxAssignableElements2: Abstract base class for SNPX elements that support memory assignment for efficient access.
- SnpxClientBase: Base class for Snpx internal and public client
- SnpxClientInternal: Internal SNPX client used by the framework for establishing connections.
- SnpxConnectParametersBase: Base class for SNPX connection parameters.
- SnpxElements2: Abstract base class for accessing SNPX elements by index.
- SnpxWritableAssignableElements3: Abstract base class for writable assignable SNPX elements.
- SnpxWritableAssignableIndexableElements2: Abstract base class for writable assignable elements accessed by integer index.
- StringRegisters: Provides access to string registers (SR[]) on the robot via SNPX.
- StringSystemVariables: Provides access to string system variables on the robot via SNPX.

## underautomation.fanuc.stream_motion

File: [underautomation.fanuc.stream_motion.md](underautomation.fanuc.stream_motion.md)

- StreamMotionClient: Stream Motion client for standalone use (J519 option): real-time control of the robot by sending a position every communication cycle.
- StreamMotionError: Kind of Stream Motion error
- StreamMotionException: Error raised by the Stream Motion client

## underautomation.fanuc.stream_motion.data

File: [underautomation.fanuc.stream_motion.data.md](underautomation.fanuc.stream_motion.data.md)

- IOType: I/O types supported by Stream Motion protocol
- IOValue: State of 16 consecutive I/O read by Stream Motion
- LimitTable: Table of allowable limits of one axis for one type of limit. The limit depends on the speed of the flange center: the table gives 20 values, for speeds up to 1/20, 2/20, ... 20/20 of LimitTable.MaxSpeed, with no payload and with the maximum payload.
- MotionEventArgs: Arguments of the motion events
- SessionEndReason: Reason of the end of a Stream Motion session
- SessionEndedEventArgs: Arguments of the SessionEnded event
- SessionEventArgs: Arguments of the session events
- SetpointRequestEventArgs: Arguments of the SetpointRequested event. Call Common.JointsPosition), Common.XYZWPRPosition) or SetpointRequestEventArgs.Hold to give the next position to send. The object is only valid during the call of the event handler.
- StatusReceivedEventArgs: Arguments of the StatusReceived event
- StreamMotionErrorEventArgs: Arguments of the ErrorOccurred event
- StreamMotionLimits: Allowable velocity, acceleration and jerk limits of the robot axes, read from the robot. The robot stops with an alarm when a position sent to it exceeds these limits.
- StreamMotionState: State of a Stream Motion client
- StreamMotionStatistics: Communication statistics of a Stream Motion client, since the status output was started
- StreamMotionStatus: Status sent by the robot every communication cycle

## underautomation.fanuc.stream_motion.internal

File: [underautomation.fanuc.stream_motion.internal.md](underautomation.fanuc.stream_motion.internal.md)

- StreamMotionClientBase: Stream Motion client (J519 option): real-time control of the robot by sending a position every communication cycle.
- StreamMotionClientInternal: Stream Motion client used by Fanuc.FanucRobot
- StreamMotionConnectParametersBase: Connection parameters for Stream Motion (J519 option)

## underautomation.fanuc.telnet

File: [underautomation.fanuc.telnet.md](underautomation.fanuc.telnet.md)

- CommandSentEventArgs: Event arguments for command sent events.
- KclClientErrorEventArgs: Event arguments for KCL client error events.
- KclCommandReceived: Event arguments for KCL command received events.
- MessageReceivedEventArgs: Event arguments for message received events.
- RawDataReceivedEventArgs: Event arguments for raw data received events.
- TelnetClient: Standalone Telnet KCL client for direct use without Fanuc.FanucRobot. Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on the web server of th...
- TpCoordinates: Enumeration of TP (Teach Pendant) coordinate systems.
- TpCoordinatesReceivedEventArgs: Event arguments for TP coordinates received events.

## underautomation.fanuc.telnet.internal

File: [underautomation.fanuc.telnet.internal.md](underautomation.fanuc.telnet.internal.md)

- TelnetClientBase: Base class for Telnet KCL client. Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on the web server of the controller with robot.Cgtp.Kcl (fi...
- TelnetClientInternal: Telnet KCL client created and managed by Fanuc.FanucRobot. Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on the web server of the controlle...
- TelnetConnectParametersBase: Base class for Telnet connection parameters.

## underautomation.robotics.geometry

File: [underautomation.robotics.geometry.md](underautomation.robotics.geometry.md)

- CartesianPose: Cartesian pose: position X, Y, Z in mm, orientation, and optional values of external axes (mm or degrees). It can describe a position of the robot or a frame.
- EulerConvention: Convention of three Euler angles (a, b, c) that describe an orientation. Angles are in degrees.
- JointValues: Position of the axes of a robot: one value per axis, in degrees for rotary axes and in mm for linear axes
- Orientation: Orientation in space, stored as a unit quaternion (Qw + Qx.i + Qy.j + Qz.k). It can be created from and converted to Euler angles, a rotation vector, an axis and an angle, or a rotation matrix.

## underautomation.robotics.io

File: [underautomation.robotics.io.md](underautomation.robotics.io.md)

- DigitalSignal: Digital signal of a robot controller, identified by a group and an index. The names of the groups and the valid indexes depend on the robot.

## underautomation.robotics.motion

File: [underautomation.robotics.motion.md](underautomation.robotics.motion.md)

- CartesianLimits: Cartesian velocity, acceleration and jerk limits, for the position (mm) and for the orientation (degrees)
- CartesianPathBuilder: Builds a Cartesian trajectory from a sequence of linear and circular motions, splines and shapes. Create it with Geometry.CartesianPose). Targets are poses of the tool of the planner, in its user frame.
- CartesianTrajectoryReport: Result of the check of a Cartesian trajectory against Cartesian velocity, acceleration and jerk limits
- DoubleSProfile: One-dimensional motion profile with bounded velocity, acceleration and jerk (7 phases, "double S" profile). The acceleration is zero at the start and at the end. Start and end velocities can be different from zero.
- IOEvent: Digital signal change requested at a given time of a trajectory
- JointLimits: Velocity, acceleration and jerk limits of the 9 axes of a robot. Units are degrees (mm for linear axes) per second, per second squared and per second cubed. A limit of 0 means that the axis is not present or not limited.
- JointPathBuilder: Builds a joint trajectory from a sequence of joint motions. Create it with Geometry.JointValues).
- LimitType: Type of limit of a robot axis
- MotionPlanner: Creates trajectories from joint motions, linear and circular motions, splines and shapes, with velocity, acceleration and jerk limits.
- PositionFormat: Format of the positions of a trajectory
- Termination: Termination of a motion: stop at the target, overlap with the next motion, or corner region of a given size
- TerminationType: Type of termination of a motion
- Trajectory: Robot trajectory in joint or Cartesian format. A trajectory can be evaluated at any time between 0 and Trajectory.Duration, and can carry I/O events.
- TrajectoryReport: Result of the check of a joint trajectory against velocity, acceleration and jerk limits
- TrajectoryViolation: Limit exceeded by a trajectory at one sample

## Types not detailed in this folder

- 427 types `UnderAutomation.Fanuc.Common.Files.Variables.*VariableType`, named `<Name>VariableType` (for example AavmGrpVariableType, AavmWrkVariableType, AbsposGrpVariableType, AdjRtrqVariableType). One generated type per structure of system variable of the controller. They are the values of the variable files (the <Name>File types of the same namespace), read with FTP or CGTP through KnownVariableFiles. Their members are in the installed package (`pip show -f UnderAutomation.Fanuc`).
