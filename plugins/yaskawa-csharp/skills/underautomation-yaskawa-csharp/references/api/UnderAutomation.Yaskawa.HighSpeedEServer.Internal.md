# UnderAutomation.Yaskawa.HighSpeedEServer.Internal

## HighSpeedEServerClientBase.GetFileProgressDelegate

`delegate void HighSpeedEServerClientBase.GetFileProgressDelegate(GetFileProgress progress)`

Delegate for receiving file download progress notifications.

- `GetFileProgressDelegate(object @object, nint method)`
- `IAsyncResult BeginInvoke(GetFileProgress progress, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(GetFileProgress progress)`

## HighSpeedEServerClientBase.LoadFileProgressDelegate

`delegate void HighSpeedEServerClientBase.LoadFileProgressDelegate(LoadFileProgress progress)`

Delegate for receiving file upload progress notifications.

- `LoadFileProgressDelegate(object @object, nint method)`
- `IAsyncResult BeginInvoke(LoadFileProgress progress, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(LoadFileProgress progress)`

## HighSpeedEServerClientBase (robot.HighSpeedEServer)

`abstract class HighSpeedEServerClientBase : IRobotClient, IStatusReader, IPositionReader, IAlarmReader, IRobotControl, IIOAccess, IVariableAccess, ITorqueReader, IMotionControl, IFileManager, IFileReader, IFileWriter, IYaskawaClient`

Base class of the High Speed Ethernet Server client of a Yaskawa robot controller. Provides methods for reading robot status, positions, variables, and executing commands via UDP.

- `RobotDataHeader AlarmReset(AlarmResetType type)`: Resets alarms or cancels errors on the robot controller. Use Reset to clear alarm conditions after resolving the cause. Use Cancel for recoverable errors that don't require alarm reset.
- `RobotDataHeader BatchDataBackup(string file = "/SPDRV/CMOSBK.BIN")`: Performs a backup of the robot's CMOS. The CMOS.BIN file is copied locally in the robot controller to "/SPDRC/CMOSBK.BIN". The operation can take several seconds to complete. After this command, the backup file can be downloaded using GetFile("/SPDRC/CMOSBK.BIN"). To enable this command : in "MAN...
- `void Close()`: Closes the connection to the robot controller and releases network resources.
- `bool Connected { get; }`: Gets a value indicating whether the client is connected to a robot controller. Note: Since UDP is connectionless, this only indicates if the socket is configured.
- `RobotDataHeader DeleteFile(string name)`: Deletes a file from the robot controller's file system. Use with caution as deleted files cannot be recovered.
- `RobotDataHeader Display(string message)`: Displays a popup message on the robot programming pendant. Message will appear as a notification to the operator.
- `RobotAlarmData GetAlarm(RobotRecentAlarm alarm)`: Reads alarm information from the robot controller. Retrieves alarm code, type, occurrence time, and descriptive text.
- `RobotAlarmDataExtended GetAlarmExtended(RobotRecentAlarm alarm)`: Retrieves extended alarm information including sub-code character strings. Provides more detailed information than GetAlarm for troubleshooting.
- `RobotAxisConfigData GetConfigurationInformation()`: Reads axis configuration information for the default robot control group. Returns axis type names for each of the 8 possible axes.
- `RobotAxisConfigData GetConfigurationInformation(RobotControlGroup type)`: Reads axis configuration information for a specified control group. Returns axis type names (e.g., "S", "L", "U", "R", "B", "T") for each axis.
- `RobotJobData GetExecutingJobInformation()`: Reads information about the currently selected and executing job (program). Returns job name, current line, step, and speed override percentage.
- `RobotFileContentData GetFile(string name, HighSpeedEServerClientBase.GetFileProgressDelegate onGetFileProgress = null)`: Downloads (saves) a file from the robot controller to the PC. Large files are received in multiple blocks and automatically reassembled. Special use case : to download CMOS.BIN, first perform a CMOS backup using BatchDataBackup, then use GetFile with the backup file path.
- `RobotFileListData GetFileList(string pattern)`: Retrieves a list of files matching a pattern from the robot controller. Supports wildcards for matching multiple files.
- `RobotJobStackData GetJobStack(int taskNumber = 0)`: Reads the job call stack for a specific task on the robot controller. Returns the current nesting of CALL instructions, from the outermost job to the currently executing one.
- `RobotManagementTimeData GetManagementTime(ManagementTimeType type, int index = 0)`: Retrieves management time statistics from the robot controller. Can query various timing metrics like control power ON time, servo ON time, etc.
- `RobotAxisIntData GetPositionError()`: Reads the position error (difference between commanded and actual position) for the default robot. Values indicate servo tracking error in pulse units.
- `RobotAxisIntData GetPositionError(RobotControlGroup type)`: Reads the position error for a specified control group. Position error indicates the difference between commanded and actual position.
- `RobotPositionCartesianData GetRobotCartesianPosition()`: Reads the current robot Cartesian position (TCP position and orientation). Coordinates are returned in millimeters for X, Y, Z and degrees for Rx, Ry, Rz.
- `RobotPositionIntData GetRobotJointPosition()`: Reads the current robot joint position in pulse (encoder) values. Returns raw pulse values for all robot axes.
- `RobotPositionIntData GetRobotPosition(RobotControlGroup type)`: Reads position data for a specified control group. Can read robot, base, or station position data depending on the control group specified.
- `RobotStatusData GetStatusInformation()`: Reads the current operational status of the robot controller. Returns information about mode (teach/play), running state, hold status, alarms, and servo power.
- `RobotSystemInformation GetSystemInformation()`: Retrieves system information about the default robot system (R1). Returns software version, robot name, and parameter file information.
- `RobotSystemInformation GetSystemInformation(RobotSystemTypeData type)`: Retrieves system information for a specific robot system or control group. Use for multi-robot controllers or to query specific axes groups.
- `RobotSystemParamData GetSystemParameter(SystemParameterTypes type, int number, int group = 1)`: Reads a system parameter from the robot controller.
- `RobotAxisIntData GetTorque()`: Reads the current torque values for the default robot's servo motors. Torque values indicate motor load as a percentage of rated torque.
- `RobotAxisIntData GetTorque(RobotControlGroup type)`: Reads the current torque values for a specified control group's servo motors. Torque values indicate motor load as a percentage of rated torque.
- `string IP { get; }`: Gets the IP address or hostname of the connected robot controller.
- `RobotDataHeader[] LoadFile(string name, string content, HighSpeedEServerClientBase.LoadFileProgressDelegate onLoadFileProgress = null)`: Uploads (loads) a file from the PC to the robot controller. Large files are automatically split into 479-byte chunks for transmission.
- `RobotDataHeader MoveCartesian(double x, double y, double z, double rx, double ry, double rz, PositionCommandClassification classification, double speed, PositionCommandOperationCoordinate coordinate, RobotPosture posture = null, PositionCommandType commandtype = PositionCommandType.StraightIncrement, int RobotControlGroup = 1, int StationControlGroup = 0, int tool = 0, int userCoordinate = 0)`: Commands the robot to move to a Cartesian position (X, Y, Z, Rx, Ry, Rz). Movement is relative to the specified coordinate system.
- `RobotDataHeader MoveJoints(int[] axesPulse, PositionCommandClassification classification, double speed, PositionCommandType commandtype = PositionCommandType.StraightIncrement, int RobotControlGroup = 1, int StationControlGroup = 1, int tool = 0)`: Commands the robot to move using joint (pulse) positions. This specifies the position of each axis directly in encoder pulses.
- `RobotStringVariableData Read16BytesChar(int firstIndex, int count)`: Reads multiple 16-byte string variables (S variables) from the robot controller. String variables are fixed-length, null-terminated ASCII strings.
- `RobotStringVariableData Read32BytesChar(int firstIndex, int count)`: Reads multiple 32-byte string variables (S variables) from the robot controller (DX200 only). Extended string variables for longer text storage than 16-byte variants.
- `RobotBasePositionVariableData ReadBasePosition(int firstIndex, int count)`: Reads multiple base position variables (BP variables) from the robot controller. Base position variables store the position of the base axes (travel axis) of a robot.
- `RobotByteVariableData ReadByte(int firstIndex, int count)`: Reads multiple byte variables (B variables) from the robot controller. Byte variables are 8-bit unsigned values used for compact data storage.
- `RobotDoubleIntegerVariableData ReadDoubleInteger(int firstIndex, int count)`: Reads multiple double-precision variables (D variables) from the robot controller. Note: The protocol actually transmits float values which are then cast to double.
- `RobotExternalAxisVariableData ReadExternalPosition(int firstIndex, int count)`: Reads multiple external axis variables (EX variables) from the robot controller. External axis variables store the position of the station axes (positioner...), in encoder pulses.
- `RobotIOData ReadIO(int firstIndex, int count)`: Reads multiple I/O bytes from the robot controller starting at a specified index.
- `RobotIOData ReadIO(IOType type, ushort group, int count)`: Reads multiple I/O bytes from the robot controller using I/O group addressing. The starting byte index is computed from the I/O type and group number.
- `RobotIntegerVariableData ReadInteger(int firstIndex, int count)`: Reads multiple integer variables (I variables) from the robot controller. Integer variables are 16-bit signed values (-32768 to 32767).
- `RobotPositionVariableData ReadPositionVariable(int firstIndex, int count)`: Reads multiple position variables (P variables) from the robot controller. Each variable is a pulse position or a Cartesian position (base, robot, tool or user frame), with its posture, tool number and user frame number.
- `RobotRealVariableData ReadReal(int firstIndex, int count)`: Reads multiple real (single-precision float) variables (R variables) from the robot controller. Real variables are 32-bit IEEE 754 floating-point values.
- `RobotRegisterData ReadRegister(int firstIndex, int count)`: Reads multiple 16-bit register values (M variables) from the robot controller. Registers are used for general-purpose integer storage in robot programs.
- `RobotDataHeader SelectJob(string job, int line)`: Selects a job for execution and optionally positions to a specific line. Call StartJob after selecting to begin execution.
- `RobotDataHeader SetCycle(RobotCycleType cycle)`: Sets the execution cycle type.
- `RobotDataHeader SetHold(bool enable)`: Sets the hold state of the robot.
- `RobotDataHeader SetServo(bool enable)`: Enables or disables servo power.
- `RobotDataHeader SetTeachPendantLockState(bool locked)`: Locks or unlocks the teach pendant.
- `RobotDataHeader StartJob()`: Starts execution of the currently selected job. The job must be selected first using SelectJob before calling this method. Servo must be ON and the robot must not be in alarm state.
- `RobotDataHeader Write16BytesChar(int firstIndex, string[] data)`: Writes 16-byte string variables (S variables) to the robot controller. Strings longer than 16 characters will be truncated.
- `RobotDataHeader Write32BytesChar(int firstIndex, string[] data)`: Writes 32-byte string variables (S variables) to the robot controller. Strings longer than 32 characters will be truncated.
- `RobotDataHeader WriteBasePosition(int firstIndex, RobotBasePositionData[] data)`: Writes base position variables (BP variables) to the robot controller.
- `RobotDataHeader WriteByte(int firstIndex, byte[] data)`: Writes byte variables (B variables) to the robot controller.
- `RobotDataHeader WriteDoubleInteger(int firstIndex, int[] data)`: Writes double-precision variables (D variables) to the robot controller.
- `RobotDataHeader WriteExternalPosition(int firstIndex, RobotAxisRawData<int>[] data)`: Writes external axis variables (EX variables) to the robot controller using generic type. Provided for backward compatibility with existing code.
- `RobotDataHeader WriteExternalPosition(int firstIndex, RobotExternalAxisData[] data)`: Writes external axis variables (EX variables) to the robot controller.
- `RobotDataHeader WriteIO(int firstIndex, byte[] data)`: Writes I/O bytes to the robot controller starting at a specified index.
- `RobotDataHeader WriteIO(IOType type, ushort group, byte[] data)`: Writes I/O bytes to the robot controller using I/O group addressing. By default, only Network Input can be written The starting byte index is computed from the I/O type and group number.
- `RobotDataHeader WriteInteger(int firstIndex, short[] data)`: Writes integer variables (I variables) to the robot controller.
- `RobotDataHeader WriteIoNetworkInput(ushort group, byte[] data)`: Writes network input bytes to the robot controller
- `RobotDataHeader WritePositionVariable(int firstIndex, RobotPositionIntData[] data)`: Writes position variables (P variables) to the robot controller.
- `RobotDataHeader WriteReal(int firstIndex, float[] data)`: Writes real (single-precision float) variables (R variables) to the robot controller.
- `RobotDataHeader WriteRegister(int firstIndex, short[] data)`: Writes multiple 16-bit register values (M variables) to the robot controller.

## HighSpeedEServerClientInternal (robot.HighSpeedEServer)

`class HighSpeedEServerClientInternal : HighSpeedEServerClientBase, IRobotClient, IStatusReader, IPositionReader, IAlarmReader, IRobotControl, IIOAccess, IVariableAccess, ITorqueReader, IMotionControl, IFileManager, IFileReader, IFileWriter, IYaskawaClient`

Internal implementation of the High Speed Ethernet Server client. This class provides the concrete implementation used internally by the SDK.

- Inherited from [HighSpeedEServerClientBase](UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md#highspeedeserverclientbase-robothighspeedeserver): `Close`, `GetAlarm`, `GetStatusInformation`, `GetExecutingJobInformation`, `GetJobStack`, `GetConfigurationInformation`, `GetRobotCartesianPosition`, `GetRobotJointPosition`, `GetRobotPosition`, `GetPositionError`, `GetTorque`, `AlarmReset`, `Display`, `StartJob`, `SelectJob`, `GetManagementTime`, `GetSystemInformation`, `GetSystemParameter`, `ReadIO`, `WriteIO`, `WriteIoNetworkInput`, `ReadRegister`, `WriteRegister`, `ReadByte`, `WriteByte`, `ReadInteger`, `WriteInteger`, `ReadDoubleInteger`, `WriteDoubleInteger`, `ReadReal`, `WriteReal`, `Read16BytesChar`, `Write16BytesChar`, `ReadPositionVariable`, `WritePositionVariable`, `ReadBasePosition`, `WriteBasePosition`, `ReadExternalPosition`, `WriteExternalPosition`, `GetAlarmExtended`, `MoveCartesian`, `MoveJoints`, `Read32BytesChar`, `Write32BytesChar`, `DeleteFile`, `LoadFile`, `GetFileList`, `GetFile`, `BatchDataBackup`, `SetServo`, `SetHold`, `SetTeachPendantLockState`, `SetCycle`, `IP`, `Connected`

## HighSpeedEServerConnectParametersInternal

`class HighSpeedEServerConnectParametersInternal : HighSpeedEServerConnectParameters`

Represents a set of High Speed Ethernet Server connection parameters

- `HighSpeedEServerConnectParametersInternal()`
- `bool Enable { get; set; }`: Gets or sets a value indicating whether to enable the High Speed Ethernet Server connection (default: true).
- Inherited from [HighSpeedEServerConnectParameters](UnderAutomation.Yaskawa.HighSpeedEServer.md#highspeedeserverconnectparameters): `DEFAULT_DATA_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_FILE_TIMEOUT_MILLISECONDS`, `DEFAULT_DATA_PORT`, `DEFAULT_FILE_PORT`, `DataTimeoutMilliseconds`, `PowerOnTimeoutMilliseconds`, `FileTimeoutMilliseconds`, `DataPort`, `FilePort`
