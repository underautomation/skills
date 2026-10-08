# UnderAutomation.Yaskawa.HostControl

## EServerClient

`class EServerClient : EServerClientInternal, IRobotClient, IStatusReader, IPositionReader, IAlarmReader, IRobotControl, IIOAccess, IVariableAccess, ITorqueReader, IMotionControl, IYaskawaClient`

Standalone client class for communicating with Yaskawa Motoman industrial robots using the Host Control protocol via Ethernet Server (TCP). This class provides methods for reading robot status, positions, variables, and controlling robot operations.

- `EServerClient()`: Creates a new instance of EServerClient for robot communication via TCP. Call Connect() to configure communication with a robot controller.
- `void Connect(string ip)`: Configures connection to the robot controller via TCP using default parameters.
- `void Connect(string ip, EServerConnectParameters parameters)`: Configures connection to the robot controller via TCP.
- Inherited from [EServerClientInternal](UnderAutomation.Yaskawa.HostControl.Internal.md#eserverclientinternal-roboteserver): `Close`, `Connected`, `Address`, `Port`
- Inherited from [HostControlClientBase](UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolclientbase-roboteserver): `GetAlarm`, `GetStatusInformation`, `GetExecutingJobInformation`, `GetControlGroup`, `GetRobotJointPosition`, `GetRobotCartesianPosition`, `SetHold`, `AlarmReset`, `ErrorCancel`, `SetMode`, `SetCycle`, `SetServo`, `SetTeachPendantLockState`, `Display`, `StartJob`, `SetControlGroup`, `SetTask`, `MoveJoint`, `MoveLinear`, `MoveIncremental`, `MovePulseJoint`, `MovePulseLinear`, `ReadIO`, `WriteIO`, `ReadByte`, `WriteByte`, `ReadInteger`, `WriteInteger`, `ReadDoubleInteger`, `WriteDoubleInteger`, `ReadReal`, `WriteReal`, `Read16BytesChar`, `Write16BytesChar`, `GetJobDirectory`, `GetUserFrame`, `SetUserFrame`, `DeleteJob`, `SetMasterJob`, `SelectJob`, `WaitForJobCompletion`, `ConvertToRelativeJob`, `ConvertToStandardJob`, `GetTorque`, `GetMaxTorque`, `GetEncoderTemperature`, `GetSystemTime`, `GetAbsoluteEncoderPosition`, `SetAbsoluteEncoderPosition`, `SetFrameType`, `GetAlarmWithMessages`

## EServerConnectParameters

`class EServerConnectParameters : HostControlConnectParametersBase`

Base class defining Ethernet Server (TCP) connection parameters for the Host Control communication. This class provides configuration for TCP-based communication with YRC1000 controllers.

- `EServerConnectParameters()`: Initializes a new instance of the Ethernet Server connection parameters.
- `const int DEFAULT_PORT = 80`: Default TCP port for Ethernet Server communication (80).
- `int Port { get; set; }`: Gets or sets the TCP port number for Ethernet Server communication. Must match the robot controller's Ethernet Server port configuration. Default: 80.
- Inherited from [HostControlConnectParametersBase](UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolconnectparametersbase): `DEFAULT_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_MOTION_TIMEOUT_MILLISECONDS`, `TimeoutMilliseconds`, `PowerOnTimeoutMilliseconds`, `MotionTimeoutMilliseconds`

## HostControlAlarmData

`class HostControlAlarmData : HostControlResponse`

Contains alarm information retrieved from the robot controller.

- `int[] Codes { get; }`: Gets the codes (5 entries). Index 0 is the code of the active error, indexes 1 to 4 are the codes of the active alarms. A code of 0 means no error or no alarm.
- `int[] Data { get; }`: Gets the sub-codes (5 entries), at the same index as HostControlAlarmData.Codes. Index 0 is the sub-code of the error, indexes 1 to 4 are the data of the alarms.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlAlarmEntry

`class HostControlAlarmEntry`

Represents a single alarm entry with code, sub-code and text description.

- `int Code { get; }`: Gets the alarm code number.
- `string Message { get; }`: Gets the alarm text message.
- `int SubCode { get; }`: Gets the alarm sub-code (data).

## HostControlAlarmStringData

`class HostControlAlarmStringData : HostControlResponse`

Contains alarm information with text messages retrieved from the robot controller.

- `int AlarmCount { get; }`: Gets the number of active alarms (entries of HostControlAlarmStringData.Alarms with a code other than 0).
- `HostControlAlarmEntry[] Alarms { get; }`: Gets the alarm entries with codes and text messages (always 4 entries, the code of an unused entry is 0).
- `HostControlAlarmEntry Error { get; }`: Gets the active error. Its code is 0 when no error is active.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlCartesianPositionData

`class HostControlCartesianPositionData : HostControlResponse, ICartesianPosition`

Contains Cartesian position data (TCP position and orientation).

- `double Axis10 { get; }`: Gets or sets the 10th external axis value.
- `double Axis11 { get; }`: Gets or sets the 11th external axis value.
- `double Axis12 { get; }`: Gets or sets the 12th external axis value.
- `double Axis8 { get; }`: Gets or sets the 8th external axis value.
- `double Axis9 { get; }`: Gets or sets the 9th external axis value.
- `int CoordinateSystem { get; }`: Gets or sets the coordinate system index. 0: Base, 1-65: User coordinates.
- `bool IsFlip { get; }`: Gets whether the robot is in flip configuration.
- `bool IsFront { get; }`: Gets whether the robot is in front configuration.
- `bool IsRLessThan180 { get; }`: Gets whether R axis is less than 180 degrees.
- `bool IsSLessThan180 { get; }`: Gets whether S axis is less than 180 degrees.
- `bool IsTLessThan180 { get; }`: Gets whether T axis is less than 180 degrees.
- `bool IsUpperArm { get; }`: Gets whether the robot is in upper arm configuration.
- `double Re { get; }`: Gets or sets the Re (7th axis rotation) in degrees or millimeters.
- `double Rx { get; }`: Gets or sets the Rx (rotation around X axis) in degrees.
- `double Ry { get; }`: Gets or sets the Ry (rotation around Y axis) in degrees.
- `double Rz { get; }`: Gets or sets the Rz (rotation around Z axis) in degrees.
- `int Type { get; }`: Gets or sets the robot posture/configuration type. Defines arm configuration (flip, upper/lower arm, front/back, etc.).
- `double X { get; }`: Gets or sets the X position in millimeters.
- `double Y { get; }`: Gets or sets the Y position in millimeters.
- `double Z { get; }`: Gets or sets the Z position in millimeters.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlCoordinateSystem

`enum HostControlCoordinateSystem`

Specifies the coordinate system for position commands.

- Base: Base coordinate system (robot base frame).
- Robot: Robot coordinate system.
- Tool: Tool coordinate system.
- User1: User coordinate system 1.
- User2: User coordinate system 2.
- User3: User coordinate system 3.
- User4: User coordinate system 4.
- User5: User coordinate system 5.
- User6: User coordinate system 6.
- User7: User coordinate system 7.
- User8: User coordinate system 8.

## HostControlCycleType

`enum HostControlCycleType`

Specifies the execution cycle type.

- Automatic: Automatic mode - continuous operation.
- OneCycle: One cycle mode - execute one complete cycle then stop.
- Step: Step mode - execute one instruction at a time.

## HostControlEncoderTemperatureData

`class HostControlEncoderTemperatureData : HostControlResponse`

Contains encoder temperature values for each robot axis. Retrieved using the RENCTMP command.

- `double[] Values { get; }`: Gets the temperature values for each axis encoder (up to 12 axes). Values are in degrees Celsius.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlException

`class HostControlException : Exception, ISerializable`

Exception thrown when a Host Control command fails.

- `HostControlException(string message)`: Creates a new HostControlException with the specified message.
- `HostControlException(string message, Exception innerException)`: Creates a new HostControlException with the specified message and inner exception.
- `HostControlException(string message, string errorCode)`: Creates a new HostControlException with the specified message and error code.
- `HostControlException(string message, string command, string errorCode)`: Creates a new HostControlException with the specified message, command, and error code.
- `string Command { get; }`: Gets the command that caused the exception.
- `string ErrorCode { get; }`: Gets the error code returned by the robot controller.

## HostControlGroupData

`class HostControlGroupData : HostControlResponse`

Contains control group information. Retrieved using the RGROUP command.

- `int RobotGroup { get; }`: Gets or sets the robot group bits. Each bit represents a robot control group (R1, R2, etc.).
- `int StationGroup { get; }`: Gets or sets the station group bits. Each bit represents a station control group (S1, S2, etc.).
- `int Task { get; }`: Gets or sets the current task number. 0: Master task, 1-15: Sub tasks.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlIOData

`class HostControlIOData : HostControlResponse`

Contains I/O signal data.

- `int Count { get; }`: Gets or sets the number of I/O bytes read.
- `byte[] Data { get; }`: Gets or sets the I/O data bytes.
- `bool GetBit(int bitOffset)`: Gets the bit value at the specified offset from the start address.
- `int StartAddress { get; }`: Gets or sets the starting I/O contact number.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlJobData

`class HostControlJobData : HostControlResponse, IJobData`

Contains information about the currently executing job (program). Retrieved using the RJSEQ command.

- `int Line { get; }`: Gets or sets the current line number within the job (0-9999).
- `string Name { get; }`: Gets or sets the name of the currently executing job.
- `int Step { get; }`: Gets or sets the current step number within the job (1-9998).
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlJobDirectoryData

`class HostControlJobDirectoryData : HostControlResponse`

Contains job directory listing data. Retrieved using the RJDIR command.

- `List<string> JobNames { get; }`: Gets or sets the list of job names in the directory.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlJointPositionData

`class HostControlJointPositionData : HostControlResponse, IJointPulses`

Contains joint position data in pulse (encoder) values.

- `int[] Axes { get; }`: Gets all axis values as an array of encoder pulse values. Array contains 12 elements: S, L, U, R, B, T, E, Axis8 through Axis12.
- `int Axis10 { get; }`: Gets or sets the 10th axis position in pulses.
- `int Axis11 { get; }`: Gets or sets the 11th axis position in pulses.
- `int Axis12 { get; }`: Gets or sets the 12th axis position in pulses.
- `int Axis8 { get; }`: Gets or sets the 8th axis position in pulses.
- `int Axis9 { get; }`: Gets or sets the 9th axis position in pulses.
- `int B { get; }`: Gets or sets the B axis position in pulses.
- `int E { get; }`: Gets or sets the E axis (7th axis) position in pulses.
- `int L { get; }`: Gets or sets the L axis position in pulses.
- `int R { get; }`: Gets or sets the R axis position in pulses.
- `int S { get; }`: Gets or sets the S axis position in pulses.
- `int T { get; }`: Gets or sets the T axis position in pulses.
- `int U { get; }`: Gets or sets the U axis position in pulses.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlResponse

`class HostControlResponse`

Base class for all robot data response objects returned by Host Control commands. Contains common response information about the communication.

- `string Command { get; }`: Gets or sets the command that was executed.
- `string ErrorMessage { get; }`: Gets or sets the error message if the command failed.
- `string ResponseCode { get; }`: Gets or sets the raw response code from the robot controller. "0000" indicates normal completion.
- `bool Success { get; }`: Gets a value indicating whether the command completed successfully.

## HostControlResponseCode

`enum HostControlResponseCode`

Specifies the interpreter error/response codes.

- AlarmOrError: Alarm or error occurring.
- HoldByCommand: In hold state (command).
- HoldByExternal: In hold state (external).
- HoldByOperationPanel: In hold state (operation panel).
- HoldByPendant: In hold state (pendant).
- IncorrectMode: Incorrect mode.
- ManipulatorMoving: Manipulator is moving.
- NoCommandRemote: No command remote setting.
- ServoOff: Servo OFF.
- Success: Normal completion.

## HostControlRobotMode

`enum HostControlRobotMode`

Specifies the robot mode.

- Play: Play mode - robot can execute programmed jobs.
- Teach: Teach mode - robot can be manually positioned and jobs can be edited.

## HostControlSpeedType

`enum HostControlSpeedType`

Specifies the speed type for motion commands.

- MillimetersPerSecond: Speed is specified in mm/s (VE).
- Percentage: Speed is specified as a percentage of maximum speed (V).

## HostControlStatusData

`class HostControlStatusData : HostControlResponse, IStatusData`

Contains the current operational status of the robot controller. Provides information about the robot's mode, running state, and safety conditions.

- `bool Alarming { get; }`: Gets whether an alarm is currently active. Check GetAlarm() for detailed alarm information.
- `bool Automatic { get; }`: Gets whether the robot is in automatic operation mode. When true, the robot can operate automatically without pendant interaction.
- `bool CommandRemote { get; }`: Gets whether remote command mode is enabled. When true, the robot accepts commands from external sources (including this API).
- `bool Cycle { get; }`: Gets whether the robot is in cycle execution mode. When true, the robot executes one complete cycle then stops.
- `bool ErrorOccurring { get; }`: Gets whether an error condition is occurring. Errors may prevent normal operation until resolved.
- `bool InHoldStatusByCommand { get; }`: Gets whether the robot is held by a command (software hold). A hold command was issued via the API or job instruction.
- `bool InHoldStatusExternally { get; }`: Gets whether the robot is held by an external hold signal. External safety circuit has triggered a hold condition.
- `bool InHoldStatusPendant { get; }`: Gets whether the robot is held by the programming pendant. Operator has pressed hold on the pendant.
- `bool Play { get; }`: Gets whether the robot is in play mode. In play mode, the robot can execute programmed jobs.
- `int RawData1 { get; }`: Gets the first raw status word from the controller response.
- `int RawData2 { get; }`: Gets the second raw status word from the controller response.
- `bool Running { get; }`: Gets whether the robot is currently running (executing a job).
- `bool ServoOn { get; }`: Gets whether servo power is enabled. Servo must be ON for the robot to move.
- `bool SpeedLimit { get; }`: Gets whether speed limit is active.
- `bool Step { get; }`: Gets whether the robot is in step (single-step) execution mode. When true, the robot executes one instruction at a time.
- `bool Teach { get; }`: Gets whether the robot is in teach mode. In teach mode, the robot can be manually positioned and jobs can be edited.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlSystemTimeData

`class HostControlSystemTimeData : HostControlResponse`

Contains system time information from the robot controller. Retrieved using the RSYSTM command.

- `string DayOfWeek { get; }`: Gets the day of the week.
- `string HourMinute { get; }`: Gets the hour and minute (HH:MM format).
- `string MonthDay { get; }`: Gets the month and day (MM/DD format).
- `string Second { get; }`: Gets the second.
- `string Year { get; }`: Gets the year.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlTorqueData

`class HostControlTorqueData : HostControlResponse`

Contains torque values for each robot axis. Retrieved using the RTRQ (current torque) or RMAXTRQ (maximum torque) commands.

- `double[] Values { get; }`: Gets the torque values for each axis (up to 12 axes). Values are in percentage of maximum rated torque.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlUserFrameData

`class HostControlUserFrameData : HostControlResponse`

Contains user coordinate frame data defined by three reference points (ORG, XX, XY). Retrieved using the RUFRAME command, written using the WUFRAME command.

- `int Axis10 { get; }`: 10th axis pulses.
- `int Axis11 { get; }`: 11th axis pulses.
- `int Axis12 { get; }`: 12th axis pulses.
- `int Axis7 { get; }`: 7th axis pulses (for travel axis, mm).
- `int Axis8 { get; }`: 8th axis pulses (for travel axis, mm).
- `int Axis9 { get; }`: 9th axis pulses (for travel axis, mm).
- `double OrgTx { get; }`: ORG wrist angle TX in degrees.
- `double OrgTy { get; }`: ORG wrist angle TY in degrees.
- `int OrgType { get; }`: ORG posture type.
- `double OrgTz { get; }`: ORG wrist angle TZ in degrees.
- `double OrgX { get; }`: ORG X coordinate value in mm.
- `double OrgY { get; }`: ORG Y coordinate value in mm.
- `double OrgZ { get; }`: ORG Z coordinate value in mm.
- `int ToolNumber { get; }`: Tool number (0-63).
- `int UserCoordinateNumber { get; }`: Gets or sets the user coordinate number (2-64).
- `double XxTx { get; }`: XX wrist angle TX in degrees.
- `double XxTy { get; }`: XX wrist angle TY in degrees.
- `int XxType { get; }`: XX posture type.
- `double XxTz { get; }`: XX wrist angle TZ in degrees.
- `double XxX { get; }`: XX X coordinate value in mm.
- `double XxY { get; }`: XX Y coordinate value in mm.
- `double XxZ { get; }`: XX Z coordinate value in mm.
- `double XyTx { get; }`: XY wrist angle TX in degrees.
- `double XyTy { get; }`: XY wrist angle TY in degrees.
- `int XyType { get; }`: XY posture type.
- `double XyTz { get; }`: XY wrist angle TZ in degrees.
- `double XyX { get; }`: XY X coordinate value in mm.
- `double XyY { get; }`: XY Y coordinate value in mm.
- `double XyZ { get; }`: XY Z coordinate value in mm.
- Inherited from [HostControlResponse](UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## HostControlVariableType

`enum HostControlVariableType`

Specifies the type of variable to read or write.

- BasePosition: Base axis position variable (BP).
- Byte: Byte variable (B).
- DoubleInteger: Double integer variable (D).
- ExternalPosition: Station axis position variable (EX), pulse type only.
- Integer: Integer variable (I).
- Position: Robot axis position variable (P).
- Real: Real (floating point) variable (R).
- String: String variable (S).
