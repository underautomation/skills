# UnderAutomation.Yaskawa.HostControl.Internal

## EServerClientInternal (robot.EServer)

`class EServerClientInternal : HostControlClientBase, IRobotClient, IStatusReader, IPositionReader, IAlarmReader, IRobotControl, IIOAccess, IVariableAccess, ITorqueReader, IMotionControl, IYaskawaClient`

Internal implementation of the Host Control client for Ethernet Server (TCP) communication. Supports YRC1000 and compatible controllers.

- `string Address { get; }`: Gets the address of the connected robot controller (IP address).
- `void Close()`: Marks the client as disconnected and releases any stored state.
- `bool Connected { get; }`: Gets a value indicating whether the client is ready to communicate with the robot. Since each command opens its own TCP connection, this reflects whether Connect has been called.
- `int Port { get; }`: Gets the TCP port number.
- Inherited from [HostControlClientBase](UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolclientbase-roboteserver): `GetAlarm`, `GetStatusInformation`, `GetExecutingJobInformation`, `GetControlGroup`, `GetRobotJointPosition`, `GetRobotCartesianPosition`, `SetHold`, `AlarmReset`, `ErrorCancel`, `SetMode`, `SetCycle`, `SetServo`, `SetTeachPendantLockState`, `Display`, `StartJob`, `SetControlGroup`, `SetTask`, `MoveJoint`, `MoveLinear`, `MoveIncremental`, `MovePulseJoint`, `MovePulseLinear`, `ReadIO`, `WriteIO`, `ReadByte`, `WriteByte`, `ReadInteger`, `WriteInteger`, `ReadDoubleInteger`, `WriteDoubleInteger`, `ReadReal`, `WriteReal`, `Read16BytesChar`, `Write16BytesChar`, `GetJobDirectory`, `GetUserFrame`, `SetUserFrame`, `DeleteJob`, `SetMasterJob`, `SelectJob`, `WaitForJobCompletion`, `ConvertToRelativeJob`, `ConvertToStandardJob`, `GetTorque`, `GetMaxTorque`, `GetEncoderTemperature`, `GetSystemTime`, `GetAbsoluteEncoderPosition`, `SetAbsoluteEncoderPosition`, `SetFrameType`, `GetAlarmWithMessages`

## EServerConnectParametersInternal

`class EServerConnectParametersInternal : EServerConnectParameters`

Connection parameters for Host Control Ethernet Server (TCP) communication. Use this class to configure network settings for TCP connection to YRC1000 and compatible controllers.

- `EServerConnectParametersInternal()`
- `bool Enable { get; set; }`: Gets or sets a value indicating whether to enable the Ethernet Server connection (default: false).
- Inherited from [EServerConnectParameters](UnderAutomation.Yaskawa.HostControl.md#eserverconnectparameters): `DEFAULT_PORT`, `Port`
- Inherited from [HostControlConnectParametersBase](UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolconnectparametersbase): `DEFAULT_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_MOTION_TIMEOUT_MILLISECONDS`, `TimeoutMilliseconds`, `PowerOnTimeoutMilliseconds`, `MotionTimeoutMilliseconds`

## HostControlClientBase (robot.EServer)

`abstract class HostControlClientBase : IRobotClient, IStatusReader, IPositionReader, IAlarmReader, IRobotControl, IIOAccess, IVariableAccess, ITorqueReader, IMotionControl, IYaskawaClient`

Base class implementing the Host Control protocol for Yaskawa robot communication. Provides methods for reading robot status, positions, variables, and executing commands.

- `abstract string Address { get; }`: Gets the address of the connected robot controller (IP address).
- `HostControlResponse AlarmReset()`: Resets the current alarm condition. The cause of the alarm must be resolved before reset will succeed. Command remote must be enabled on the controller.
- `abstract void Close()`: Closes the connection to the robot controller and releases resources.
- `abstract bool Connected { get; }`: Gets a value indicating whether the client is connected to a robot controller.
- `HostControlResponse ConvertToRelativeJob(string jobName, HostControlCoordinateSystem coordinateSystem)`: Converts a specified job to a relative job of a specified coordinate system. Requires the relative job function on the robot controller.
- `HostControlResponse ConvertToStandardJob(string jobName, int convertingMethod, int referencePositionVariable)`: Converts a specified job to a standard job (pulse job). Requires the relative job function on the robot controller.
- `HostControlResponse DeleteJob(string jobName)`: Deletes a specified job from the robot controller.
- `HostControlResponse Display(string message)`: Displays a message on the remote display of the teach pendant. Command remote must be enabled on the controller.
- `HostControlResponse ErrorCancel()`: Cancels the current error condition. Used for recoverable errors that don't require full alarm reset.
- `long GetAbsoluteEncoderPosition(int axisNumber)`: Reads the absolute encoder position of a specific axis.
- `HostControlAlarmData GetAlarm()`: Reads the codes of the active error and alarms from the robot controller. Index 0 of the arrays is the error, indexes 1 to 4 are the alarms.
- `HostControlAlarmStringData GetAlarmWithMessages()`: Reads the active error and alarms with their text messages from the robot controller. Returns the error and up to 4 alarms, each with its code, sub-code and message.
- `HostControlGroupData GetControlGroup()`: Reads the current control group configuration. Returns robot group bits, station group bits, and current task number.
- `HostControlEncoderTemperatureData GetEncoderTemperature()`: Reads the encoder temperature values of all robot axes.
- `HostControlJobData GetExecutingJobInformation()`: Reads information about the currently selected and executing job (program). Returns job name, current line, and step.
- `HostControlJobDirectoryData GetJobDirectory(string jobNameFilter = "*")`: Reads the job directory listing from the robot controller.
- `HostControlTorqueData GetMaxTorque()`: Reads the maximum torque values of all robot axes. Returns values as a percentage of the maximum rated torque.
- `HostControlCartesianPositionData GetRobotCartesianPosition(HostControlCoordinateSystem coordinateSystem = HostControlCoordinateSystem.Base, bool includeExternalAxes = false)`: Reads the current robot Cartesian position (TCP position and orientation). Coordinates are returned in millimeters for X, Y, Z and degrees for Rx, Ry, Rz.
- `HostControlJointPositionData GetRobotJointPosition()`: Reads the current robot joint position in pulse (encoder) values. Returns raw pulse values for all robot axes (S, L, U, R, B, T, and external axes).
- `HostControlStatusData GetStatusInformation()`: Reads the current operational status of the robot controller. Returns information about mode (teach/play), running state, hold status, alarms, and servo power.
- `HostControlSystemTimeData GetSystemTime()`: Reads the system time from the robot controller.
- `HostControlTorqueData GetTorque()`: Reads the current torque values of all robot axes. Returns values as a percentage of the maximum rated torque.
- `HostControlUserFrameData GetUserFrame(int userCoordinateNumber)`: Reads user coordinate frame data from the robot controller. Returns the three reference points (ORG, XX, XY) defining the user coordinate system.
- `HostControlResponse MoveIncremental(HostControlSpeedType speedType, double speed, HostControlCoordinateSystem coordinateSystem, double dx, double dy, double dz, double drx, double dry, double drz, int toolNumber = 0)`: Moves the robot incrementally using linear interpolation. Movement is relative to the current position.
- `HostControlResponse MoveJoint(int speedPercent, HostControlCoordinateSystem coordinateSystem, double x, double y, double z, double rx, double ry, double rz, int type = 0, int toolNumber = 0)`: Moves the robot to a Cartesian position using joint interpolation. Joint motion is faster but the path is not linear.
- `HostControlResponse MoveLinear(HostControlSpeedType speedType, double speed, HostControlCoordinateSystem coordinateSystem, double x, double y, double z, double rx, double ry, double rz, int type = 0, int toolNumber = 0)`: Moves the robot to a Cartesian position using linear interpolation. Linear motion follows a straight line path.
- `HostControlResponse MovePulseJoint(int speedPercent, int s, int l, int u, int r, int b, int t, int toolNumber = 0)`: Moves the robot to a pulse position using joint interpolation.
- `HostControlResponse MovePulseLinear(HostControlSpeedType speedType, double speed, int s, int l, int u, int r, int b, int t, int toolNumber = 0)`: Moves the robot to a pulse position using linear interpolation.
- `string[] Read16BytesChar(int firstIndex, int count)`: Reads 16-byte string (S) variables starting at the specified index.
- `byte[] ReadByte(int firstIndex, int count)`: Reads byte (B) variables starting at the specified index.
- `int[] ReadDoubleInteger(int firstIndex, int count)`: Reads double integer (D) variables starting at the specified index.
- `HostControlIOData ReadIO(int startAddress, int count)`: Reads I/O signals from the robot controller. Each byte holds 8 signals.
- `short[] ReadInteger(int firstIndex, int count)`: Reads integer (I) variables starting at the specified index.
- `float[] ReadReal(int firstIndex, int count)`: Reads real (R) variables starting at the specified index.
- `HostControlResponse SelectJob(string jobName, int line)`: Sets the job name and line number for execution.
- `HostControlResponse SetAbsoluteEncoderPosition(int axisNumber, long value)`: Writes the absolute encoder data for a specific axis.
- `HostControlResponse SetControlGroup(int robotGroup, int stationGroup)`: Changes the control group selection.
- `HostControlResponse SetCycle(RobotCycleType cycle)`: Sets the execution cycle type (Step, One Cycle, or Automatic).
- `HostControlResponse SetFrameType(int frameType)`: Sets the coordinate frame type used for position display on the pendant.
- `HostControlResponse SetHold(bool enable)`: Sets the hold state of the robot. When hold is ON, robot motion is paused. When OFF, motion can resume.
- `HostControlResponse SetMasterJob(string jobName)`: Sets a specified job as the master job and execution job.
- `HostControlResponse SetMode(RobotMode mode)`: Sets the robot operation mode (Teach or Play).
- `HostControlResponse SetServo(bool enable)`: Enables or disables servo power. Servo must be ON for the robot to move. Uses extended timeout for power-on.
- `HostControlResponse SetTask(int task)`: Changes the current task selection.
- `HostControlResponse SetTeachPendantLockState(bool locked)`: Locks or unlocks the operations from the teach pendant and from the I/O operation signals. The emergency stop of the teach pendant stays active. Command remote must be enabled on the controller.
- `HostControlResponse SetUserFrame(int userCoordinateNumber, HostControlUserFrameData frame)`: Writes user coordinate frame data to the robot controller. Defines a user coordinate system using three reference points (ORG, XX, XY).
- `HostControlResponse StartJob(string jobName = null)`: Starts job execution. Starts the currently selected job, or starts a specific job if specified.
- `bool WaitForJobCompletion(int timeoutSeconds = -1)`: Waits for the current job to complete or the specified timeout to elapse. No response is sent until the job completes or the timeout expires.
- `void Write16BytesChar(int firstIndex, string[] data)`: Writes 16-byte string (S) variables starting at the specified index.
- `void WriteByte(int firstIndex, byte[] data)`: Writes byte (B) variables starting at the specified index.
- `void WriteDoubleInteger(int firstIndex, int[] data)`: Writes double integer (D) variables starting at the specified index.
- `HostControlResponse WriteIO(int startAddress, byte[] data)`: Writes I/O signals to the robot controller. Each byte holds 8 signals. By default, the controller accepts only the network input signals (#27010 to #29567).
- `void WriteInteger(int firstIndex, short[] data)`: Writes integer (I) variables starting at the specified index.
- `void WriteReal(int firstIndex, float[] data)`: Writes real (R) variables starting at the specified index.

## HostControlConnectParametersBase

`abstract class HostControlConnectParametersBase`

Base class defining connection parameters for the Host Control communication. This class cannot be instantiated directly; use HostControl.EServerConnectParameters instead.

- `const int DEFAULT_MOTION_TIMEOUT_MILLISECONDS = 30000`: Default timeout in milliseconds for motion commands (30000ms).
- `const int DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS = 10000`: Default timeout in milliseconds for servo power on operations (10000ms).
- `const int DEFAULT_TIMEOUT_MILLISECONDS = 5000`: Default timeout in milliseconds for commands (5000ms).
- `int MotionTimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for motion commands to complete. Motion commands may take longer depending on the distance to travel. Default: 30000ms.
- `int PowerOnTimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for servo power on to complete. Servo power on may take longer due to brake release and motor initialization. Default: 10000ms.
- `int TimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for a response to commands. Default: 5000ms.
