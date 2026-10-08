# UnderAutomation.Yaskawa.HighSpeedEServer

## AlarmResetType

`enum AlarmResetType`

Specifies the type of alarm reset operation to perform.

- Cancel: Cancel the current error. Used for recoverable errors.
- Reset: Reset the current alarm. Requires the alarm condition to be resolved.

## ArmFlipInformation

`enum ArmFlipInformation`

Specifies the arm configuration (upper/lower) based on L and U axis positions.

- Lower: Lower arm configuration - elbow is below the line between shoulder and wrist.
- Upper: Upper arm configuration - elbow is above the line between shoulder and wrist.

## AxisFlipInformation

`enum AxisFlipInformation`

Specifies whether an axis angle is less than or greater than/equal to 180 degrees. Used for determining robot configuration in multi-solution situations.

- LT180: Axis angle is less than 180 degrees.
- UT180: Axis angle is greater than or equal to 180 degrees.

## ControlGroup

`enum ControlGroup`

Defines control group types for robot systems. Control groups organize different motion units within the robot system.

- BaseCartesian: Base axes in Cartesian coordinates. Valid index: 1-8.
- BasePulseValue: Base axes in pulse values. Valid index: 1-8.
- RobotCartesian: Robot axes in Cartesian coordinates. Valid index: 1-8.
- RobotPulseValue: Robot axes in pulse (encoder) values. Valid index: 1-8.
- StationPulseValue: Station axes in pulse values. Valid index: 1-24 (S1 to S24).

## FlipNoFlipInformation

`enum FlipNoFlipInformation`

Specifies the flip/no-flip wrist configuration.

- Flip: Flip configuration - wrist is in flipped orientation.
- NoFlip: No-flip configuration - wrist is in standard orientation.

## GetFileProgress

`class GetFileProgress`

Contains progress information for file download (GetFile) operations. Used with the GetFileProgressDelegate callback to track download progress.

- `bool Completed { get; }`: Gets whether the file download has completed successfully.
- `int DownloadedBytes { get; }`: Gets the number of bytes downloaded so far.
- `string FileName { get; }`: Gets the name of the file being downloaded.

## HighSpeedEServerClient

`class HighSpeedEServerClient : HighSpeedEServerClientBase, IRobotClient, IStatusReader, IPositionReader, IAlarmReader, IRobotControl, IIOAccess, IVariableAccess, ITorqueReader, IMotionControl, IFileManager, IFileReader, IFileWriter, IYaskawaClient`

Main client class for communicating with Yaskawa Motoman industrial robots using the High Speed Ethernet Server protocol. This class provides methods for reading robot status, positions, variables, and controlling robot operations via UDP.

- `HighSpeedEServerClient()`: Creates a new instance of HighSpeedEServerClient for robot communication. Call Connect() to establish communication with a robot controller.
- `void Connect(string ip, HighSpeedEServerConnectParameters parameters)`: Connects to a robot controller with custom connection parameters object.
- Inherited from [HighSpeedEServerClientBase](UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md#highspeedeserverclientbase-robothighspeedeserver): `Close`, `GetAlarm`, `GetStatusInformation`, `GetExecutingJobInformation`, `GetJobStack`, `GetConfigurationInformation`, `GetRobotCartesianPosition`, `GetRobotJointPosition`, `GetRobotPosition`, `GetPositionError`, `GetTorque`, `AlarmReset`, `Display`, `StartJob`, `SelectJob`, `GetManagementTime`, `GetSystemInformation`, `GetSystemParameter`, `ReadIO`, `WriteIO`, `WriteIoNetworkInput`, `ReadRegister`, `WriteRegister`, `ReadByte`, `WriteByte`, `ReadInteger`, `WriteInteger`, `ReadDoubleInteger`, `WriteDoubleInteger`, `ReadReal`, `WriteReal`, `Read16BytesChar`, `Write16BytesChar`, `ReadPositionVariable`, `WritePositionVariable`, `ReadBasePosition`, `WriteBasePosition`, `ReadExternalPosition`, `WriteExternalPosition`, `GetAlarmExtended`, `MoveCartesian`, `MoveJoints`, `Read32BytesChar`, `Write32BytesChar`, `DeleteFile`, `LoadFile`, `GetFileList`, `GetFile`, `BatchDataBackup`, `SetServo`, `SetHold`, `SetTeachPendantLockState`, `SetCycle`, `IP`, `Connected`

## HighSpeedEServerConnectParameters

`class HighSpeedEServerConnectParameters`

Base class defining connection parameters for the High Speed Ethernet Server communication. This class cannot be instantiated directly; use a derived class or use Connect with optional parameters. Allows customization of timeouts and ports for different network environments.

- `HighSpeedEServerConnectParameters()`: Initializes a new instance of the connection parameters class.
- `const int DEFAULT_DATA_PORT = 10040`: Default UDP port for data communication (10040).
- `const int DEFAULT_DATA_TIMEOUT_MILLISECONDS = 1500`: Default timeout in milliseconds for data commands (1500ms).
- `const int DEFAULT_FILE_PORT = 10041`: Default UDP port for file transfer operations (10041).
- `const int DEFAULT_FILE_TIMEOUT_MILLISECONDS = 4000`: Default timeout in milliseconds for file operations (4000ms).
- `const int DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS = 8000`: Default timeout in milliseconds for servo power on operations (8000ms).
- `int DataPort { get; set; }`: Gets or sets the UDP port number for data communication. Must match the robot controller's High Speed Ethernet Server data port configuration. Default: 10040.
- `int DataTimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for a response to data commands. Applies to most read/write operations like position reading, variable access, etc. Default: 1500ms.
- `int FilePort { get; set; }`: Gets or sets the UDP port number for file transfer operations. Must match the robot controller's High Speed Ethernet Server file port configuration. Default: 10041.
- `int FileTimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for file operation responses. File operations may be slower due to larger data transfers and disk I/O on the controller. Default: 4000ms.
- `int PowerOnTimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for servo power on to complete. Servo power on may take longer due to brake release and motor initialization. Default: 8000ms.

## InvalidDataAnswerException

`class InvalidDataAnswerException : Exception, ISerializable`

Exception thrown when the robot controller returns an error response to a High Speed Ethernet Server command. This exception contains detailed status codes that help identify the specific error condition.

- `int AddedStatus { get; }`: Gets the additional status code providing more detailed error information. The interpretation of this value depends on the primary Status code.
- `int Status { get; }`: Gets the primary status code returned by the robot controller. A value of 0 indicates success; any other value indicates an error condition.

## LoadFileProgress

`class LoadFileProgress`

Contains progress information for file upload (LoadFile) operations. Used with the LoadFileProgressDelegate callback to track upload progress.

- `bool Completed { get; }`: Gets whether the file upload has completed successfully.
- `string FileName { get; }`: Gets the name of the file being uploaded.
- `int LoadedBytes { get; }`: Gets the number of bytes uploaded so far.
- `int TotalBytes { get; }`: Gets the total size of the file in bytes.

## ManagementTimeType

`enum ManagementTimeType`

Specifies the type of management time data to retrieve. Different metrics track various aspects of robot operation.

- ControlPowerOnTime: Total time the controller power has been on.
- MotionTimeR1ToR8: Motion time for robots R1 through R8. Pass the robot number (1 to 8) as index of GetManagementTime.
- MotionTimeS1ToS24: Motion time for stations S1 through S24. Pass the station number (1 to 24) as index of GetManagementTime.
- MotionTimeTotal: Total motion time across all robots.
- OperationTimeApplication1To8: Operation time for applications 1 through 8. Add application number (0-7) to get specific application.
- PlayBackTimeR1ToR8: Playback time for robots R1 through R8. Pass the robot number (1 to 8) as index of GetManagementTime.
- PlayBackTimeS1ToS24: Playback time for stations S1 through S24. Pass the station number (1 to 24) as index of GetManagementTime.
- PlayBackTimeTotal: Total playback time across all robots.
- ServoPowerOnTimR1ToR8: Servo power on time for robots R1 through R8. Pass the robot number (1 to 8) as index of GetManagementTime.
- ServoPowerOnTimeS1ToS24: Servo power on time for stations S1 through S24. Pass the station number (1 to 24) as index of GetManagementTime.
- ServoPowerOnTimeTotal: Total servo power on time across all robots.

## OnOffCommandType

`enum OnOffCommandType : byte`

Specifies the type of ON/OFF command to send to the robot controller. These commands control fundamental robot states that affect safety and operation.

- HLock: Lock Teach Pendant. Value: 3.
- Hold: Hold command - pauses robot motion while maintaining servo power. Robot can resume from held position. Value: 1.
- Servo: Servo power command - enables or disables motor power to the robot. Servo must be ON for the robot to move. Value: 2.

## OrientationFlipInformation

`enum OrientationFlipInformation`

Specifies the orientation (front/back) configuration of the robot arm. Determined by the position of the B-axis rotation center relative to the S-axis.

- Back: Back configuration - B-axis rotation center is behind S-axis rotation center when viewed from the right-hand side of the robot.
- Front: Front configuration - B-axis rotation center is in front of S-axis rotation center when viewed from the right-hand side of the robot.

## PositionCommandClassification

`enum PositionCommandClassification`

Specifies the speed classification (units) for motion commands. Determines how the speed value is interpreted by the controller.

- Cartesian_DEG_S: Speed in degrees per second for rotational motion. Valid range depends on robot model.
- Cartesian_MM_S: Speed in millimeters per second for linear motion. Valid range depends on robot model.
- LinkPercent: Speed as percentage of maximum link (joint) speed. Valid range: 0.01 to 100.00 percent.

## PositionCommandOperationCoordinate

`enum PositionCommandOperationCoordinate`

Specifies the coordinate system for position command interpretation. Determines how X, Y, Z, Rx, Ry, Rz values are interpreted.

- Base: Base coordinate system (world frame at robot base). Fixed reference frame typically aligned with robot mounting.
- Robot: Robot coordinate system. Reference frame at the robot's origin point.
- Tool: Tool coordinate system. Reference frame at the tool center point (TCP).
- User: User-defined coordinate system. Custom reference frame defined for specific workpiece or fixture.

## PositionCommandType

`enum PositionCommandType`

Specifies the type of position command (motion instruction) to execute. Determines the path type and whether position is absolute or incremental.

- LinkAbsolute: Link (joint interpolated) motion to an absolute position. All joints move simultaneously to reach the target, resulting in non-linear TCP path.
- StraightAbsolute: Straight (linear interpolated) motion to an absolute position. TCP moves in a straight line to the target position.
- StraightIncrement: Straight (linear interpolated) motion by an incremental offset. TCP moves in a straight line relative to current position.

## RegardedReversePositionSpecified

`enum RegardedReversePositionSpecified`

Specifies how to handle position in reverse direction scenarios.

- Form: Use the specified form/posture as reference.
- Previous: Use the previous position as reference.

## RobotAlarmData

`class RobotAlarmData : RobotData`

Contains information about a robot alarm retrieved from the controller. Alarms indicate error conditions that may require operator intervention.

- `int Code { get; }`: Gets the alarm code identifying the specific alarm type. Alarm codes are documented in the robot's maintenance manual.
- `int Data { get; }`: Gets additional alarm data providing context about the alarm. The meaning depends on the specific alarm code.
- `string OccurringTime { get; }`: Gets the timestamp when the alarm occurred. Format: "YYYY/MM/DD HH:MM:SS" (16 characters).
- `string Text { get; }`: Gets the alarm message text describing the alarm condition. Maximum 32 characters.
- `int Type { get; }`: Gets the alarm type/category classification.

## RobotAlarmDataExtended

`class RobotAlarmDataExtended : RobotAlarmData`

Contains extended information about a robot alarm, including sub-code details. Provides more detailed diagnostic information than the basic RobotAlarmData.

- `string AdditionnalInformation { get; }`: Gets additional information about the alarm condition. Maximum 16 characters.
- `string SubData { get; }`: Gets the sub-code data providing detailed error context. Maximum 96 characters.
- `string SubDataReverse { get; }`: Gets the reversed sub-code data. Maximum 96 characters.
- Inherited from [RobotAlarmData](UnderAutomation.Yaskawa.HighSpeedEServer.md#robotalarmdata): `Code`, `Data`, `Type`, `OccurringTime`, `Text`

## RobotAxisConfigData

`class RobotAxisConfigData : RobotAxisRawData<string>`

Represents raw axis data with string values for axis configuration information. Used to retrieve axis name/type information from the robot controller.

- `string[] Axes { get; }`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `string Axis1 { get; set; }`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `string Axis2 { get; set; }`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `string Axis3 { get; set; }`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `string Axis4 { get; set; }`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `string Axis5 { get; set; }`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `string Axis6 { get; set; }`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `string Axis7 { get; set; }`: Gets or sets the value for axis 7 (optional additional axis).
- `string Axis8 { get; set; }`: Gets or sets the value for axis 8 (optional additional axis).

## RobotAxisIntData

`class RobotAxisIntData : RobotAxisRawData<int>`

Represents raw axis data with 32-bit integer values for up to 8 axes. This is a concrete implementation commonly used for pulse-based position data.

- `int[] Axes { get; }`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `int Axis1 { get; set; }`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `int Axis2 { get; set; }`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `int Axis3 { get; set; }`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `int Axis4 { get; set; }`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `int Axis5 { get; set; }`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `int Axis6 { get; set; }`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `int Axis7 { get; set; }`: Gets or sets the value for axis 7 (optional additional axis).
- `int Axis8 { get; set; }`: Gets or sets the value for axis 8 (optional additional axis).

## RobotAxisRawData<T>

`class RobotAxisRawData<T> : RobotData`

Represents raw axis data with generic value type for up to 8 axes. This is the base class for position-related data structures.

- `T[] Axes { get; }`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `T Axis1 { get; set; }`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `T Axis2 { get; set; }`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `T Axis3 { get; set; }`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `T Axis4 { get; set; }`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `T Axis5 { get; set; }`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `T Axis6 { get; set; }`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `T Axis7 { get; set; }`: Gets or sets the value for axis 7 (optional additional axis).
- `T Axis8 { get; set; }`: Gets or sets the value for axis 8 (optional additional axis).

## RobotBasePositionData

`class RobotBasePositionData : RobotAxisRawData<int>`

Represents base position data for coordinated motion with travel units or external bases. Base positions define the location of the robot's base in world coordinates or pulse values.

- `RobotBasePositionData(RobotDataHeader header)`: Creates a new instance of RobotBasePositionData with the specified header information.
- `RobotBasePositionType DataType { get; }`: Gets the data type indicating whether values are pulse or coordinate values.
- `bool IsDefined { get; }`: Gets whether the variable is taught on the controller. False for a variable read with Int32%2cSystem.Int32) that is not defined: its values are then all 0.
- `int[] Axes { get; }`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `int Axis1 { get; set; }`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `int Axis2 { get; set; }`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `int Axis3 { get; set; }`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `int Axis4 { get; set; }`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `int Axis5 { get; set; }`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `int Axis6 { get; set; }`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `int Axis7 { get; set; }`: Gets or sets the value for axis 7 (optional additional axis).
- `int Axis8 { get; set; }`: Gets or sets the value for axis 8 (optional additional axis).

## RobotBasePositionType

`enum RobotBasePositionType : byte`

Defines the type of base position data representation.

- BaseCoordinateValue: Position is represented in base coordinate system values.
- PulseValue: Position is represented as encoder pulse values.

## RobotBasePositionVariableData

`class RobotBasePositionVariableData : RobotData`

Represents data returned from reading multiple base position variables (BP variables) from the robot controller. BP variables store base position information used for coordinated motion with external axes or travel units.

- `RobotBasePositionData[] Value { get; }`: Gets the array of base position data read from the robot controller.

## RobotByteVariableData

`class RobotByteVariableData : RobotData`

Represents data returned from reading multiple byte variables (B variables) from the robot controller. B variables are 8-bit unsigned integer storage locations (0-255).

- `byte[] Value { get; }`: Gets the array of byte variable values read from the robot controller.

## RobotControlGroup

`class RobotControlGroup`

Represents a robot control group combining a group type with an index. Used to specify which robot or station to query in multi-robot systems.

- `RobotControlGroup(ControlGroup group, int index)`: Creates a new RobotControlGroup with the specified group type and index.
- `readonly byte ByteValue`: The combined byte value sent to the robot controller (Group + Index).
- `static readonly RobotControlGroup DefaultRobotCartesian`: Default control group for Cartesian position of robot 1.
- `static readonly RobotControlGroup DefaultRobotPulse`: Default control group for pulse position of robot 1.
- `readonly ControlGroup Group`: The control group type (robot, base, station).
- `readonly int Index`: The index within the control group (e.g., robot number 1-8).

## RobotData

`class RobotData`

Base class for all robot data response objects returned by High Speed Ethernet Server commands. Contains common header information about the communication response.

- `RobotData()`: Creates a blank instance of RobotData, for use as input to robot commands (e.g. kinematics conversions).

## RobotDataHeader

`class RobotDataHeader`

Information about a response of the robot controller: the controller that answered, the size of the data, and the state of a transfer in several parts.

- `RobotDataHeader()`
- `int BlockNo { get; }`: Gets the raw block number of a transfer in several parts, such as a file transfer. Use RobotDataHeader.IsLastBlock to know if this response is the last part.
- `int DataSize { get; }`: Gets the size, in bytes, of the data returned by the controller in this response.
- `IPEndPoint IP { get; }`: Gets the IP endpoint (address and port) of the robot controller that sent the response. Useful for identifying the source in multi-robot configurations.
- `bool IsLastBlock { get; }`: Gets a value indicating whether this response is the last part of a transfer in several parts.

## RobotDoubleIntegerVariableData

`class RobotDoubleIntegerVariableData : RobotData`

Represents data returned from reading multiple double-precision integer variables (D variables) from the robot controller.

- `int[] Value { get; }`: Gets the array of double integer values read from the robot controller.

## RobotExternalAxisData

`class RobotExternalAxisData : RobotAxisRawData<int>`

Represents external axis position data for positioners, travel units, or additional servo axes. External axes are coordinated with the robot motion for applications like welding positioners.

- `RobotExternalAxisData(RobotAxisRawData<int> source)`: Creates a new instance of RobotExternalAxisData from a generic RobotAxisRawData. Used for conversion from generic types to specific types.
- `RobotExternalAxisData(RobotDataHeader header)`: Creates a new instance of RobotExternalAxisData with the specified header information.
- `bool IsDefined { get; }`: Gets whether the variable is taught on the controller. False for a variable read with Int32%2cSystem.Int32) that is not defined: its values are then all 0.
- `int[] Axes { get; }`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `int Axis1 { get; set; }`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `int Axis2 { get; set; }`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `int Axis3 { get; set; }`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `int Axis4 { get; set; }`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `int Axis5 { get; set; }`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `int Axis6 { get; set; }`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `int Axis7 { get; set; }`: Gets or sets the value for axis 7 (optional additional axis).
- `int Axis8 { get; set; }`: Gets or sets the value for axis 8 (optional additional axis).

## RobotExternalAxisVariableData

`class RobotExternalAxisVariableData : RobotData`

Represents data returned from reading multiple external axis variables (EX variables) from the robot controller. EX variables store position data for external axes such as positioners, travel units, or additional servo axes.

- `RobotExternalAxisData[] Value { get; }`: Gets the array of external axis data read from the robot controller.

## RobotFileContentData

`class RobotFileContentData : RobotData`

Contains the content of a file downloaded from the robot controller. Provides methods for parsing structured file content such as job files and parameter files.

- `string Content { get; }`: Gets the text content of the downloaded file.
- `byte[] ContentRaw { get; }`: Gets the text content of the downloaded file.
- `string FileName { get; }`: Gets the name of the downloaded file.
- `int GetParam(string section, int parameterLine, int parameterColumn)`: Extracts an integer parameter value from a structured file section. Useful for reading values from parameter files and job data.
- `List<RobotDataHeader> Headers { get; }`: Gets the list of response headers from multi-block transfers. Large files are transferred in multiple UDP packets.

## RobotFileListData

`class RobotFileListData : RobotData`

Contains the result of a file listing operation on the robot controller. Returns an array of file names matching the specified pattern.

- `string[] Files { get; }`: Gets the array of file names returned by the listing operation. File names include extensions (e.g., "MYJOB.JBI", "SYSTEM.SYS").
- `List<RobotDataHeader> Headers { get; }`: Gets the list of response headers from multi-block transfers. File listings may span multiple UDP packets for large directories.

## RobotIOData

`class RobotIOData : RobotData`

Represents data returned from reading multiple I/O (Input/Output) points from the robot controller. I/O addresses are organized in groups based on their function and accessibility.

- `byte[] Value { get; }`: Gets the array of I/O byte values read from the robot controller. Each byte represents 8 consecutive I/O points where each bit corresponds to one I/O state.

## RobotIntegerVariableData

`class RobotIntegerVariableData : RobotData`

Represents data returned from reading multiple integer variables (I variables) from the robot controller. I variables are 16-bit signed integer storage locations.

- `short[] Value { get; }`: Gets the array of integer variable values read from the robot controller.

## RobotJobData

`class RobotJobData : RobotData, IJobData`

Contains information about the currently executing job (program) on the robot controller. Retrieved using the executing job information reading command.

- `int Line { get; }`: Gets the current line number being executed within the job. Line numbers are 1-based and correspond to the job listing.
- `string Name { get; }`: Gets the name of the currently selected/executing job. Job names can be up to 32 characters. Returns empty string if no job is selected.
- `double SpeedOverride { get; }`: Gets the current speed override percentage (0-100). This is the global speed multiplier applied to all motions.
- `int Step { get; }`: Gets the current step number within the job. Step numbers track the execution progress through motion instructions.

## RobotJobStackData

`class RobotJobStackData : RobotData`

Contains the job call stack for a specific task on the robot controller. Represents the current nesting of CALL instructions, from the outermost job to the currently executing one. Only supported on DX200 (AY/BY/YN) controllers.

- `string[] Jobs { get; }`: Gets the job names in the call stack, outermost first. The first entry is the root job, the last entry is the currently executing job. Empty if no nested calls are active.

## RobotKinematicsCartesianData

`class RobotKinematicsCartesianData : RobotKinematicsPositionData`

Cartesian position result from a kinematics conversion. Provides named X/Y/Z and orientation properties in engineering units in addition to the raw axis values.

- `double Rx { get; }`: Gets the Rx orientation in degrees (derived from the raw 0.0001° axis value).
- `double Ry { get; }`: Gets the Ry orientation in degrees.
- `double Rz { get; }`: Gets the Rz orientation in degrees.
- `double X { get; }`: Gets the X position in millimetres (derived from the raw µm axis value).
- `double Y { get; }`: Gets the Y position in millimetres.
- `double Z { get; }`: Gets the Z position in millimetres.
- Inherited from [RobotKinematicsPositionData](UnderAutomation.Yaskawa.HighSpeedEServer.md#robotkinematicspositiondata): `DataType`, `Form`, `ToolNumber`, `UserCoordinateNumber`, `Axes`

## RobotKinematicsJointData

`class RobotKinematicsJointData : RobotKinematicsPositionData`

Joint-space position result from a kinematics conversion. Provides the 8 joint axis values in both raw 0.0001° units and as a ready-to-use degrees array.

- `double[] AxisDegrees { get; }`: Gets the 8 joint axis values converted to degrees. Each element equals the corresponding RobotKinematicsPositionData.Axes value divided by 10 000.
- Inherited from [RobotKinematicsPositionData](UnderAutomation.Yaskawa.HighSpeedEServer.md#robotkinematicspositiondata): `DataType`, `Form`, `ToolNumber`, `UserCoordinateNumber`, `Axes`

## RobotKinematicsPositionData

`class RobotKinematicsPositionData : RobotData`

Base class for kinematic position data exchanged with the robot controller. Contains coordinate type, posture flags, tool/user numbers, and the 8 raw axis values.

- `RobotKinematicsPositionData()`: Creates a blank instance for use as input to kinematics conversion methods.
- `int[] Axes { get; set; }`: Gets or sets the 8 raw axis values. For joint positions: values in 0.0001° units (divide by 10 000 for degrees). For Cartesian positions: XYZ axes (0–2) in µm; orientation axes (3–5) in 0.0001°.
- `RobotPositionDataType DataType { get; set; }`: Gets or sets the coordinate type of this position.
- `RobotPosture Form { get; set; }`: Gets or sets the posture/form flags for this position.
- `int ToolNumber { get; set; }`: Gets or sets the tool number used for this position.
- `int UserCoordinateNumber { get; set; }`: Gets or sets the user coordinate number used for this position.

## RobotManagementTimeData

`class RobotManagementTimeData : RobotData`

Contains management time information for tracking robot operation statistics. Provides uptime and usage metrics for maintenance planning and reporting.

- `string EllapseTime { get; }`: Gets the elapsed time for the tracked metric. Format: "HHHH:MM:SS.ss" or similar time duration format (12 characters).
- `string StartTime { get; }`: Gets the start time of the tracked period. Format: "YYYY/MM/DD HH:MM" (16 characters).

## RobotPluralData<T>

`class RobotPluralData<T> : RobotData`

Represents a collection of data values returned from plural (batch) read operations. Used for reading multiple variables, registers, or I/O points in a single request.

- `T[] Value { get; }`: Gets the array of values read from the robot controller. The array length corresponds to the number of values successfully read.

## RobotPositionCartesianData

`class RobotPositionCartesianData : RobotData, ICartesianPosition`

Represents Cartesian position data with coordinates in millimeters and degrees. This class provides human-readable position data converted from the raw protocol values.

- `RobotPositionDataType DataType { get; }`: Gets the position data type indicating the coordinate system used.
- `RobotPosture Form { get; }`: Gets the robot posture (form) data defining the kinematic configuration.
- `double Rx { get; }`: Gets the rotation around X axis (Rx) in degrees.
- `double Ry { get; }`: Gets the rotation around Y axis (Ry) in degrees.
- `double Rz { get; }`: Gets the rotation around Z axis (Rz) in degrees.
- `int ToolNumber { get; }`: Gets the tool number (TCP) used for this position.
- `int UserCoordinateNumber { get; }`: Gets the user coordinate system number used for this position.
- `double X { get; }`: Gets the X coordinate in millimeters.
- `double Y { get; }`: Gets the Y coordinate in millimeters.
- `double Z { get; }`: Gets the Z coordinate in millimeters.

## RobotPositionData<T>

`class RobotPositionData<T> : RobotAxisRawData<T>`

Represents generic robot position data with axis values of the specified type. This class provides a flexible structure for storing position information that can be represented in different data formats (pulse values, Cartesian coordinates, etc.).

- `RobotPositionData(RobotDataHeader header)`: Creates a new instance of RobotPositionData with the specified header information.
- `RobotPositionDataType DataType { get; set; }`: Gets or sets the position data type indicating the coordinate system used. Determines how axis values should be interpreted (pulse, base, robot, user, or tool coordinates).
- `RobotPosture Form { get; set; }`: Gets or sets the robot posture (form) data defining the robot's kinematic configuration. This includes flip/no-flip state, arm configuration (upper/lower), and axis angle ranges.
- `bool IsDefined { get; }`: Gets whether the variable is taught on the controller. False for a variable read with Int32%2cSystem.Int32) that is not defined: its values are then all 0.
- `int ToolNumber { get; set; }`: Gets or sets the tool number (TCP - Tool Center Point) used for this position. Tool numbers typically range from 0-63, where 0 is often the robot flange center.
- `int UserCoordinateNumber { get; set; }`: Gets or sets the user coordinate system number used for this position. User coordinates define custom reference frames for specific workpiece locations.
- `T[] Axes { get; }`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `T Axis1 { get; set; }`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `T Axis2 { get; set; }`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `T Axis3 { get; set; }`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `T Axis4 { get; set; }`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `T Axis5 { get; set; }`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `T Axis6 { get; set; }`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `T Axis7 { get; set; }`: Gets or sets the value for axis 7 (optional additional axis).
- `T Axis8 { get; set; }`: Gets or sets the value for axis 8 (optional additional axis).

## RobotPositionDataType

`enum RobotPositionDataType`

Defines the coordinate system type for position data.

- BaseCoordinateValue: Position in base coordinate system (world frame, value 16).
- PulseValue: Position in encoder pulse values (joint space).
- RobotCoordinateValue: Position in robot coordinate system (robot base frame, value 17).
- ToolCoordinateValue: Position in tool coordinate system (value 18).
- UserCoordinateValue: Position in user-defined coordinate system (value 19).

## RobotPositionIntData

`class RobotPositionIntData : RobotPositionData<int>, IJointPulses`

Represents robot position data with 32-bit integer axis values. This is the primary type used for pulse-based position data from the High Speed Ethernet Server. Axis values are in pulse units (encoder counts) or scaled coordinate values.

- `RobotPositionIntData()`: Creates a blank instance of RobotPositionIntData
- `RobotPositionIntData(RobotDataHeader header)`: Creates a new instance of RobotPositionIntData with the specified header information.
- `RobotPositionCartesianData ToCartesian()`: Converts a Cartesian position to millimeters and degrees.
- `RobotPosture Form { get; set; }`: Gets or sets the robot posture (form) data defining the robot's kinematic configuration. This includes flip/no-flip state, arm configuration (upper/lower), and axis angle ranges.
- `RobotPositionDataType DataType { get; set; }`: Gets or sets the position data type indicating the coordinate system used. Determines how axis values should be interpreted (pulse, base, robot, user, or tool coordinates).
- `int ToolNumber { get; set; }`: Gets or sets the tool number (TCP - Tool Center Point) used for this position. Tool numbers typically range from 0-63, where 0 is often the robot flange center.
- `int UserCoordinateNumber { get; set; }`: Gets or sets the user coordinate system number used for this position. User coordinates define custom reference frames for specific workpiece locations.
- `bool IsDefined { get; }`: Gets whether the variable is taught on the controller. False for a variable read with Int32%2cSystem.Int32) that is not defined: its values are then all 0.
- `int[] Axes { get; }`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `int Axis1 { get; set; }`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `int Axis2 { get; set; }`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `int Axis3 { get; set; }`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `int Axis4 { get; set; }`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `int Axis5 { get; set; }`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `int Axis6 { get; set; }`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `int Axis7 { get; set; }`: Gets or sets the value for axis 7 (optional additional axis).
- `int Axis8 { get; set; }`: Gets or sets the value for axis 8 (optional additional axis).

## RobotPositionVariableData

`class RobotPositionVariableData : RobotData`

Represents data returned from reading multiple position variables (P variables) from the robot controller. P variables store complete robot position data including coordinates, posture, tool and user coordinate references.

- `RobotPositionIntData[] Value { get; }`: Gets the array of position variable data read from the robot controller. Each element contains full position information including axis values, posture, and coordinate references.

## RobotPosture

`class RobotPosture`

Represents the complete robot posture (form) configuration. Encodes the kinematic configuration choices that determine which of multiple inverse kinematics solutions is used to reach a Cartesian position.

- `RobotPosture()`: Creates a new RobotPosture with default values.
- `RobotPosture(int form, int extendedForm)`: Creates a new RobotPosture with specified form values.
- `RobotPosture(OrientationFlipInformation orientation = OrientationFlipInformation.Front, ArmFlipInformation arm = ArmFlipInformation.Upper, FlipNoFlipInformation flip = FlipNoFlipInformation.Flip, AxisFlipInformation rAxis = AxisFlipInformation.LT180, AxisFlipInformation tAxis = AxisFlipInformation.LT180, AxisFlipInformation sAxis = AxisFlipInformation.LT180, OrientationFlipInformation redundant = OrientationFlipInformation.Front, RegardedReversePositionSpecified regardedReversePositionSpecified = RegardedReversePositionSpecified.Previous, AxisFlipInformation lAxis = AxisFlipInformation.LT180, AxisFlipInformation uAxis = AxisFlipInformation.LT180, AxisFlipInformation bAxis = AxisFlipInformation.LT180, AxisFlipInformation eAxis = AxisFlipInformation.LT180, AxisFlipInformation wAxis = AxisFlipInformation.LT180)`: Creates a new RobotPosture with specified configuration values.
- `ArmFlipInformation Arm { get; set; }`: Gets or sets the upper/lower arm configuration based on L and U axis positions.
- `AxisFlipInformation BAxis { get; set; }`: Gets or sets the B-axis (wrist bend) angle range configuration from extended form.
- `static readonly RobotPosture Default`: Default posture with Form=0 and ExtendedForm=0.
- `AxisFlipInformation EAxis { get; set; }`: Gets or sets the E-axis (external/elbow) angle range configuration from extended form.
- `int ExtendedForm { get; set; }`: Gets or sets the extended form byte for additional axis configurations. Bit-encoded: L-axis, U-axis, B-axis, E-axis, W-axis range flags.
- `FlipNoFlipInformation Flip { get; set; }`: Gets or sets the flip/no-flip wrist configuration.
- `int Form { get; set; }`: Gets or sets the primary form byte encoding basic posture flags. Bit-encoded: orientation, arm, flip, R-axis, T-axis, S-axis, redundant, reverse position.
- `static RobotPosture FromInteger(int value)`: Creates a RobotPosture from a combined 16-bit integer value.
- `AxisFlipInformation LAxis { get; set; }`: Gets or sets the L-axis (lower arm) angle range configuration from extended form.
- `OrientationFlipInformation Orientation { get; set; }`: Gets or sets the front/back orientation configuration. Specifies where the B-axis rotation center locates relative to the S-axis when viewing the L and U axes from the right-hand side.
- `AxisFlipInformation RAxis { get; set; }`: Gets or sets the R-axis (wrist rotation) angle range configuration.
- `OrientationFlipInformation Redundant { get; set; }`: Gets or sets the redundant axis orientation configuration (for 7+ axis robots).
- `RegardedReversePositionSpecified RegardedReversePositionSpecified { get; set; }`: Gets or sets the reverse position specification mode.
- `AxisFlipInformation SAxis { get; set; }`: Gets or sets the S-axis (base rotation) angle range configuration.
- `AxisFlipInformation TAxis { get; set; }`: Gets or sets the T-axis (tool rotation) angle range configuration.
- `int ToInteger()`: Converts the posture to a single 16-bit integer value. Form is stored in the low byte, ExtendedForm in the high byte.
- `AxisFlipInformation UAxis { get; set; }`: Gets or sets the U-axis (upper arm) angle range configuration from extended form.
- `AxisFlipInformation WAxis { get; set; }`: Gets or sets the W-axis angle range configuration from extended form.

## RobotRealVariableData

`class RobotRealVariableData : RobotData`

Represents data returned from reading multiple real variables (R variables) from the robot controller. R variables are 32-bit single-precision floating point storage locations.

- `float[] Value { get; }`: Gets the array of single-precision floating point values read from the robot controller.

## RobotRecentAlarm

`enum RobotRecentAlarm`

Specifies which recent alarm to retrieve from the robot controller. The controller maintains a history of the most recent alarms.

- FourthLatest: The fourth most recent alarm.
- Latest: The most recent (current) alarm.
- SecondLatest: The second most recent alarm.
- ThirdLatest: The third most recent alarm.

## RobotRegisterData

`class RobotRegisterData : RobotData`

Represents data returned from reading multiple register values from the robot controller. Registers are 16-bit signed integer storage locations used for general-purpose data.

- `short[] Value { get; }`: Gets the array of register values read from the robot controller. Each value is a 16-bit signed integer (-32768 to 32767).

## RobotStatusData

`class RobotStatusData : RobotData, IStatusData`

Contains the current operational status of the robot controller. Provides information about the robot's mode, running state, and safety conditions. Retrieved using the status information reading command.

- `bool Alarming { get; }`: Gets whether an alarm is currently active. Check GetAlarm() for detailed alarm information.
- `bool Automatic { get; }`: Gets whether the robot is in automatic operation mode. When true, the robot can operate automatically without pendant interaction.
- `bool CommandRemote { get; }`: Gets whether remote command mode is enabled. When true, the robot accepts commands from external sources (including this API).
- `bool Cycle { get; }`: Gets whether the robot is in cycle execution mode. When true, the robot executes one complete cycle then stops.
- `bool ErrorOccurring { get; }`: Gets whether an error condition is occurring. Errors may prevent normal operation until resolved.
- `bool InGuardSafeOperation { get; }`: Gets whether the robot is in guard safe operation mode. Indicates collaborative/safety-rated operation mode is active.
- `bool InHoldStatusByCommand { get; }`: Gets whether the robot is held by a command (software hold). A hold command was issued via the API or job instruction.
- `bool InHoldStatusExternally { get; }`: Gets whether the robot is held by an external hold signal. External safety circuit has triggered a hold condition.
- `bool InHoldStatusPendant { get; }`: Gets whether the robot is held by the programming pendant. Operator has pressed hold on the pendant.
- `bool Play { get; }`: Gets whether the robot is in play mode. In play mode, the robot can execute programmed jobs.
- `bool Running { get; }`: Gets whether the robot is currently running (executing a job).
- `bool ServoOn { get; }`: Gets whether servo power is enabled. Servo must be ON for the robot to move.
- `bool Step { get; }`: Gets whether the robot is in step (single-step) execution mode. When true, the robot executes one instruction at a time.
- `bool Teach { get; }`: Gets whether the robot is in teach mode. In teach mode, the robot can be manually positioned and jobs can be edited.

## RobotStringVariableData

`class RobotStringVariableData : RobotData`

Represents data returned from reading multiple string variables (S variables) from the robot controller. S variables can be either 16-byte or 32-byte character strings depending on the command used.

- `string[] Value { get; }`: Gets the array of string values read from the robot controller. Strings are null-terminated and trimmed of trailing null characters.

## RobotSystemInformation

`class RobotSystemInformation : RobotData`

Contains system information about the robot controller including software version and configuration. Retrieved using the system information acquiring command.

- `string Name { get; }`: Gets the system/robot name or model identifier. Maximum 16 characters.
- `string Parameter { get; }`: Gets parameter file or configuration information. Maximum 8 characters.
- `string SoftwareVersion { get; }`: Gets the controller software version string. Format typically includes model and version number. Maximum 24 characters.

## RobotSystemParamData

`class RobotSystemParamData : RobotData`

Contains a system parameter value read from the robot controller.

- `uint Value { get; }`: Gets the raw system parameter value returned by the controller.

## RobotSystemType

`enum RobotSystemType : byte`

Defines the types of system components that can be queried for information.

- Application: Application system (APP1-APP8). Valid index: 1-8.
- Robot: Robot manipulator system (R1-R8). Valid index: 1-8.
- Station: Station/positioner system (S1-S24). Valid index: 1-24.

## RobotSystemTypeData

`class RobotSystemTypeData`

Represents a system type and index combination for querying specific robot system components. Used to specify which robot, station, or application to query in multi-robot configurations.

- `readonly byte Byte`: Gets the combined byte value sent to the controller (Type + Index).
- `static readonly RobotSystemTypeData Default`: Default system type data for querying the primary robot (Robot 1).
- `readonly int Index`: Gets the index within the system type (1-based).
- `readonly RobotSystemType Type`: Gets the system type (Robot, Station, or Application).

## SwitchingCommands

`enum SwitchingCommands`

Specifies the execution mode switching command to send to the robot controller. These modes control how the robot executes programmed jobs.

- Continue: Continuous mode - robot executes the program continuously until stopped. Normal production operation mode.
- Cycle: Cycle mode - robot executes one complete cycle of the program then stops. Useful for testing or single-part operations.
- Step: Step mode - robot executes one instruction at a time, stopping after each. Useful for debugging and detailed program verification.

## SystemParameterTypes

`enum SystemParameterTypes`

Specifies the category of a system parameter to read from the controller. Types S1CG, AP, and SE require a group number when reading.

- AP: AxP. Requires a group number.
- RS: RS
- S1CG: S1CxG. requires group number.
- S2C: S2C
- S3C: S3C
- S4C: S4C
- SE: SxE. Requires a group number.
