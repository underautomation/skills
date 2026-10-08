# UnderAutomation.Yaskawa.Common

## AlarmEntry

`class AlarmEntry : IAlarmEntry`

Default implementation of Common.IAlarmEntry.

- `AlarmEntry()`
- `int Code { get; }`: Alarm code identifying the alarm type.
- `string Message { get; }`: Human-readable alarm message text.
- `string OccurringTime { get; }`: Timestamp of alarm occurrence (format depends on protocol).
- `int SubCode { get; }`: Alarm sub-code providing additional context.

## CartesianPosition

`class CartesianPosition : ICartesianPosition`

Cartesian position of the robot flange in the robot frame.

- `CartesianPosition()`: Initializes a new instance of Common.CartesianPosition at the origin, with zero angles.
- `CartesianPosition(double x, double y, double z, double rx, double ry, double rz)`: Initializes a new instance of Common.CartesianPosition with the specified values.
- `CartesianPosition(ICartesianPosition position)`: Initializes a new instance of Common.CartesianPosition by copying any Cartesian position, for example a position read from the robot.
- `static CartesianPosition FromHomogeneousMatrix(double[,] matrix)`: Creates a Cartesian position from a homogeneous matrix (3x4 or 4x4, translation in mm). When Ry is +90 or -90 degrees, Rx and Rz are not unique: Rz is set to 0.
- `double Rx { get; set; }`: Rotation around the X axis in degrees.
- `double Ry { get; set; }`: Rotation around the Y axis in degrees.
- `double Rz { get; set; }`: Rotation around the Z axis in degrees.
- `double[,] ToHomogeneousMatrix()`: Returns the 4x4 homogeneous matrix of this position (rotation and translation in mm).
- `double X { get; set; }`: X position in millimeters.
- `double Y { get; set; }`: Y position in millimeters.
- `double Z { get; set; }`: Z position in millimeters.

## ConnectException

`class ConnectException : Exception, ISerializable`

Exception thrown when connection to a Yaskawa robot fails

- `string Address { get; }`: Address of the robot (IP:port)
- `string Service { get; }`: Name of the protocol that failed to connect

## DhParameters

`class DhParameters : IDhParameters`

Denavit-Hartenberg parameters of a 6-axis Yaskawa arm (axes S, L, U, R, B, T).

- `DhParameters()`: Initializes a new instance of Common.DhParameters with zero lengths and standard home angles (DhParameters.Theta2 = -90, DhParameters.Theta3 = 0, DhParameters.Theta5 = 0).
- `DhParameters(double a1, double a2, double a3, double d4, double d5, double d6, double theta2, double theta3, double theta5)`: Initializes a new instance of Common.DhParameters with the specified values.
- `DhParameters(IDhParameters parameters)`: Initializes a new instance of Common.DhParameters by copying an existing Common.IDhParameters.
- `double A1 { get; set; }`: Offset between the S axis and the L axis, along the arm (mm).
- `double A2 { get; set; }`: Lower arm length, between the L axis and the U axis (mm).
- `double A3 { get; set; }`: Elbow offset, between the U axis and the forearm axis (mm).
- `double D4 { get; set; }`: Forearm length, between the U axis and the wrist (mm).
- `double D5 { get; set; }`: Wrist offset along the B axis (mm). Zero for a spherical wrist.
- `double D6 { get; set; }`: Distance between the wrist and the flange, along the T axis (mm).
- `static DhParameters FromArmKinematicModel(ArmKinematicModels model)`: Returns the DH parameters of a known robot model.
- `static DhParameters FromArmKinematicModelName(string modelName)`: Returns the DH parameters of a known robot model, from its name (for example "GP7" or "HC10DTP"). The comparison ignores case.
- `static DhParameters FromPrmContent(string content)`: Reads the DH parameters of robot group 1 from the text content of an ALL.PRM parameter file. DX100, DX200, FS100, YRC1000 and YRC1000micro files are supported.
- `static DhParameters FromPrmFile(string path)`: Reads the DH parameters of robot group 1 from an ALL.PRM parameter file saved from a controller. DX100, DX200, FS100, YRC1000 and YRC1000micro files are supported.
- `KinematicsCategory KinematicsCategory { get; }`: Kinematic structure of the arm: KinematicsCategory.Opw when DhParameters.D5 is 0, KinematicsCategory.J5OffsetWrist otherwise.
- `double Theta2 { get; set; }`: DH angle of the L axis when the L axis is at zero pulse (degrees).
- `double Theta3 { get; set; }`: DH angle of the U axis when the U axis is at zero pulse (degrees).
- `double Theta5 { get; set; }`: DH angle of the B axis when the B axis is at zero pulse (degrees).

## FileExtension

`enum FileExtension`

Represents the file types available on a Yaskawa robot controller.

- CND: Condition files (.CND)
- CSV: CSV files (.CSV)
- DAT: Data files (.DAT)
- JOB: Job files (.JBI)
- LOG: Log files (.LOG)
- LST: List files (.LST)
- PRM: Parameter files (.PRM)
- SYS: System files (.SYS)
- TXT: Text files (.TXT)

## IAlarmEntry

`interface IAlarmEntry`

Represents an active alarm on a Yaskawa robot controller.

- `int Code { get; }`: Alarm code identifying the alarm type.
- `string Message { get; }`: Human-readable alarm message text.
- `string OccurringTime { get; }`: Timestamp of alarm occurrence (format depends on protocol).
- `int SubCode { get; }`: Alarm sub-code providing additional context.

## IAlarmReader

`interface IAlarmReader : IYaskawaClient`

Provides access to active alarm information from the robot controller.

- `IAlarmEntry[] GetActiveAlarms()`: Reads the currently active alarms from the robot controller. Returns an array of active alarm entries. Empty array if no alarms are active.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## ICartesianPosition

`interface ICartesianPosition`

Represents a robot Cartesian position (TCP position and orientation).

- `double Rx { get; }`: Rotation around X axis in degrees.
- `double Ry { get; }`: Rotation around Y axis in degrees.
- `double Rz { get; }`: Rotation around Z axis in degrees.
- `double X { get; }`: X position in millimeters.
- `double Y { get; }`: Y position in millimeters.
- `double Z { get; }`: Z position in millimeters.

## IDhParameters

`interface IDhParameters`

Denavit-Hartenberg parameters of a 6-axis Yaskawa arm (axes S, L, U, R, B, T).

- `double A1 { get; }`: Offset between the S axis and the L axis, along the arm (mm).
- `double A2 { get; }`: Lower arm length, between the L axis and the U axis (mm).
- `double A3 { get; }`: Elbow offset, between the U axis and the forearm axis (mm).
- `double D4 { get; }`: Forearm length, between the U axis and the wrist (mm).
- `double D5 { get; }`: Wrist offset along the B axis (mm). Zero for a spherical wrist.
- `double D6 { get; }`: Distance between the wrist and the flange, along the T axis (mm).
- `double Theta2 { get; }`: DH angle of the L axis when the L axis is at zero pulse (degrees).
- `double Theta3 { get; }`: DH angle of the U axis when the U axis is at zero pulse (degrees).
- `double Theta5 { get; }`: DH angle of the B axis when the B axis is at zero pulse (degrees).

## IFileManager

`interface IFileManager : IFileReader, IFileWriter, IYaskawaClient`

Provides complete file management: read, write, list, and delete operations.

- Inherited from [IFileReader](UnderAutomation.Yaskawa.Common.md#ifilereader): `GetFile`, `GetFileList`
- Inherited from [IFileWriter](UnderAutomation.Yaskawa.Common.md#ifilewriter): `LoadFile`, `DeleteFile`
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IFileReader

`interface IFileReader : IYaskawaClient`

Provides file read operations: download files and list directory contents.

- `string GetFile(string fileName)`: Downloads a file from the robot controller and returns its content as a string.
- `string[] GetFileList(string pattern)`: Lists files matching a name pattern.
- `string[] GetFileList(FileExtension fileExtension)`: Lists files matching the specified file extension.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IFileWriter

`interface IFileWriter : IYaskawaClient`

Provides file write and delete operations on the robot controller.

- `void DeleteFile(string fileName)`: Deletes a file from the robot controller.
- `void LoadFile(string fileName, string content)`: Uploads a file to the robot controller.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IIOAccess

`interface IIOAccess : IYaskawaClient`

Provides read/write access to robot I/O signals.

- `byte[] ReadIO(int startAddress, int count)`: Reads I/O signal bytes from the robot controller. Each byte holds a group of 8 signals.
- `void WriteIO(int startAddress, byte[] data)`: Writes I/O signal bytes to the robot controller. Each byte holds a group of 8 signals.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IJobData

`interface IJobData`

Represents information about the currently executing job on a Yaskawa robot controller.

- `int Line { get; }`: Current line number being executed.
- `string Name { get; }`: Name of the current job.
- `int Step { get; }`: Current step number being executed.

## IJointAngles

`interface IJointAngles`

Represents a joint position of a 6-axis arm in degrees, with the same signs as the pendant.

- `double[] Values { get; }`: Angles of axes S, L, U, R, B, T in degrees.

## IJointPulses

`interface IJointPulses`

Represents a robot joint position in pulse (encoder) values.

- `int[] Axes { get; }`: Axis values in encoder pulses. Typically 8 to 12 elements depending on the robot configuration.

## IMotionControl

`interface IMotionControl : IYaskawaClient`

Provides motion commands to move the robot.

- `void MoveCartesian(double x, double y, double z, double rx, double ry, double rz, double speed, int tool = 0)`: Moves the robot to a Cartesian position.
- `void MoveJoints(int[] axesPulse, double speed, int tool = 0)`: Moves the robot to a joint (pulse) position.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IOType

`enum IOType`

Yaskawa Motoman I/O signal type categories.

- AuxiliaryRelay: Auxiliary relay signals (#70010–)
- ExternalInput: External input signals (#20010–)
- ExternalOutput: External output signals (#30010–)
- GeneralInput: Robot user input signals (#00010–)
- GeneralOutput: Robot user output signals (#10010–)
- InterfacePanelInput: Interface panel input signals (#60010–)
- NetworkInput: Network input signals (#27010–)
- NetworkOutput: Network output signals (#37010–)
- PseudoInput: Pseudo input signals (#82010–)
- RobotControlStatus: Robot control status signals (#80010–)
- SpecificInput: Robot system input signals (#40010–)
- SpecificOutput: Robot system output signals (#50010–)

## IPositionReader

`interface IPositionReader : IYaskawaClient`

Provides access to current robot position readings.

- `ICartesianPosition GetRobotCartesianPosition()`: Reads the current robot Cartesian position (TCP position and orientation).
- `IJointPulses GetRobotJointPosition()`: Reads the current robot joint position in pulse (encoder) values.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IRobotClient

`interface IRobotClient : IStatusReader, IPositionReader, IAlarmReader, IRobotControl, IIOAccess, IVariableAccess, ITorqueReader, IMotionControl, IYaskawaClient`

Super-interface that combines all robot control capabilities. Implemented by High Speed Ethernet Server and Host Control clients.

- Inherited from [IStatusReader](UnderAutomation.Yaskawa.Common.md#istatusreader): `GetStatusInformation`, `GetExecutingJobInformation`
- Inherited from [IPositionReader](UnderAutomation.Yaskawa.Common.md#ipositionreader): `GetRobotJointPosition`, `GetRobotCartesianPosition`
- Inherited from [IAlarmReader](UnderAutomation.Yaskawa.Common.md#ialarmreader): `GetActiveAlarms`
- Inherited from [IRobotControl](UnderAutomation.Yaskawa.Common.md#irobotcontrol): `AlarmReset`, `SetServo`, `SetHold`, `SetTeachPendantLockState`, `SetCycle`, `StartJob`, `SelectJob`, `Display`
- Inherited from [IIOAccess](UnderAutomation.Yaskawa.Common.md#iioaccess): `ReadIO`, `WriteIO`
- Inherited from [IVariableAccess](UnderAutomation.Yaskawa.Common.md#ivariableaccess): `ReadByte`, `WriteByte`, `ReadInteger`, `WriteInteger`, `ReadDoubleInteger`, `WriteDoubleInteger`, `ReadReal`, `WriteReal`, `Read16BytesChar`, `Write16BytesChar`
- Inherited from [ITorqueReader](UnderAutomation.Yaskawa.Common.md#itorquereader): `GetTorque`
- Inherited from [IMotionControl](UnderAutomation.Yaskawa.Common.md#imotioncontrol): `MoveCartesian`, `MoveJoints`
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IRobotControl

`interface IRobotControl : IYaskawaClient`

Provides robot control commands: alarm reset, servo, hold, cycle, job and display.

- `void AlarmReset()`: Resets the current alarm condition.
- `void Display(string message)`: Displays a popup message on the robot programming pendant.
- `void SelectJob(string jobName, int line)`: Selects a job for execution and positions to a specific line.
- `void SetCycle(RobotCycleType cycle)`: Sets the execution cycle type (Step, One Cycle, or Automatic).
- `void SetHold(bool enable)`: Sets the hold state of the robot. When hold is ON, robot motion is paused.
- `void SetServo(bool enable)`: Enables or disables servo power. Servo must be ON for the robot to move.
- `void SetTeachPendantLockState(bool locked)`: Locks or unlocks the teach pendant.
- `void StartJob()`: Starts execution of the currently selected job.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IStatusData

`interface IStatusData`

Represents the operational status of a Yaskawa robot controller. Common status flags shared across all communication protocols.

- `bool Alarming { get; }`: An alarm is active.
- `bool Automatic { get; }`: Automatic operation mode active.
- `bool CommandRemote { get; }`: Remote command mode enabled.
- `bool Cycle { get; }`: Cycle execution mode active.
- `bool ErrorOccurring { get; }`: An error condition is occurring.
- `bool InHoldStatusByCommand { get; }`: Hold state triggered by software command.
- `bool InHoldStatusExternally { get; }`: Hold state triggered by external signal.
- `bool InHoldStatusPendant { get; }`: Hold state triggered by teach pendant.
- `bool Play { get; }`: Program playback mode active.
- `bool Running { get; }`: Currently executing a job.
- `bool ServoOn { get; }`: Servo power is on.
- `bool Step { get; }`: Step execution mode active.
- `bool Teach { get; }`: Manual teach mode active.

## IStatusReader

`interface IStatusReader : IYaskawaClient`

Provides access to robot status and executing job information.

- `IJobData GetExecutingJobInformation()`: Reads the currently executing job information.
- `IStatusData GetStatusInformation()`: Reads the current operational status of the robot controller.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## ITorqueReader

`interface ITorqueReader : IYaskawaClient`

Provides access to robot axis torque readings.

- `double[] GetTorque()`: Reads the current torque values of all robot axes as a percentage of the maximum rated torque.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IVariableAccess

`interface IVariableAccess : IYaskawaClient`

Provides typed read/write access to robot controller variables.

- `string[] Read16BytesChar(int firstIndex, int count)`: Reads 16-byte string (S) variables starting at the specified index.
- `byte[] ReadByte(int firstIndex, int count)`: Reads byte (B) variables starting at the specified index.
- `int[] ReadDoubleInteger(int firstIndex, int count)`: Reads double integer (D) variables starting at the specified index.
- `short[] ReadInteger(int firstIndex, int count)`: Reads integer (I) variables starting at the specified index.
- `float[] ReadReal(int firstIndex, int count)`: Reads real (R) variables starting at the specified index.
- `void Write16BytesChar(int firstIndex, string[] data)`: Writes 16-byte string (S) variables starting at the specified index.
- `void WriteByte(int firstIndex, byte[] data)`: Writes byte (B) variables starting at the specified index.
- `void WriteDoubleInteger(int firstIndex, int[] data)`: Writes double integer (D) variables starting at the specified index.
- `void WriteInteger(int firstIndex, short[] data)`: Writes integer (I) variables starting at the specified index.
- `void WriteReal(int firstIndex, float[] data)`: Writes real (R) variables starting at the specified index.
- Inherited from [IYaskawaClient](UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## IYaskawaClient

`interface IYaskawaClient`

Base interface for all Yaskawa robot communication clients. Provides connection management shared across all communication protocols.

- `string Address { get; }`: Gets the address of the robot controller: an IP address or a host name.
- `void Close()`: Closes the connection to the robot controller and releases resources.
- `bool Connected { get; }`: Gets a value indicating whether the client is connected to a robot controller.

## IoHelpers

`static class IoHelpers`

Helper methods for handling Yaskawa I/O group conversions and related utilities.

- `static uint ConvertIOGroupToBitAddress(IOType type, ushort group, byte bitIndex)`: Converts an I/O group address (type + group + bit) to a flat Yaskawa 5-digit contact number.

## JointsAngles

`class JointsAngles : IJointAngles`

Joint angles of a 6-axis arm, in degrees, with the same signs as the pendant (axes S, L, U, R, B, T).

- `JointsAngles()`: Initializes a new instance of Common.JointsAngles with all angles at 0.
- `JointsAngles(double s, double l, double u, double r, double b, double t)`: Initializes a new instance of Common.JointsAngles with the specified angles (degrees).
- `JointsAngles(double[] values)`: Initializes a new instance of Common.JointsAngles from an array of at least 6 angles (degrees). The array is copied.
- `double B { get; set; }`: B axis angle (degrees).
- `double L { get; set; }`: L axis angle (degrees).
- `double R { get; set; }`: R axis angle (degrees).
- `double S { get; set; }`: S axis angle (degrees).
- `double T { get; set; }`: T axis angle (degrees).
- `double U { get; set; }`: U axis angle (degrees).
- `double[] Values { get; }`: Angles of axes S, L, U, R, B, T in degrees.

## KinematicsCategory

`enum KinematicsCategory`

Kinematic structure of a 6-axis arm. It decides which inverse kinematics solver is used.

- J5OffsetWrist: Ortho-parallel base with a wrist offset along the B axis (D5 is not 0): the R and T axes do not meet. Collaborative robots such as HC10, HC10DT, HC20SDT. Up to 16 inverse kinematics solutions.
- Opw: Ortho-parallel base with a spherical wrist: the R, B and T axes meet at one point (D5 = 0). Most industrial arms (GP, MH, ES, HC20DT, HC30PL...). Up to 8 inverse kinematics solutions.

## RobotCycleType

`enum RobotCycleType`

Specifies the execution cycle type.

- Automatic: Automatic mode : continuous operation.
- OneCycle: One cycle mode : execute one complete cycle then stop.
- Step: Step mode : execute one instruction at a time.

## RobotMode

`enum RobotMode`

Specifies the robot operation mode.

- Play: Play mode : robot can execute programmed jobs.
- Teach: Teach mode : robot can be manually positioned and jobs can be edited.
