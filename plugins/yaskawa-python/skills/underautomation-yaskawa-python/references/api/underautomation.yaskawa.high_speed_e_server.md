# underautomation.yaskawa.high_speed_e_server

## AlarmResetType

`from underautomation.yaskawa.high_speed_e_server.alarm_reset_type import AlarmResetType`

Specifies the type of alarm reset operation to perform.

- Reset: Reset the current alarm. Requires the alarm condition to be resolved.
- Cancel: Cancel the current error. Used for recoverable errors.

## ArmFlipInformation

`from underautomation.yaskawa.high_speed_e_server.arm_flip_information import ArmFlipInformation`

Specifies the arm configuration (upper/lower) based on L and U axis positions.

- Upper: Upper arm configuration - elbow is above the line between shoulder and wrist.
- Lower: Lower arm configuration - elbow is below the line between shoulder and wrist.

## AxisFlipInformation

`from underautomation.yaskawa.high_speed_e_server.axis_flip_information import AxisFlipInformation`

Specifies whether an axis angle is less than or greater than/equal to 180 degrees. Used for determining robot configuration in multi-solution situations.

- LT180: Axis angle is less than 180 degrees.
- UT180: Axis angle is greater than or equal to 180 degrees.

## ControlGroup

`from underautomation.yaskawa.high_speed_e_server.control_group import ControlGroup`

Defines control group types for robot systems. Control groups organize different motion units within the robot system.

- RobotPulseValue: Robot axes in pulse (encoder) values. Valid index: 1-8.
- BasePulseValue: Base axes in pulse values. Valid index: 1-8.
- StationPulseValue: Station axes in pulse values. Valid index: 1-24 (S1 to S24).
- RobotCartesian: Robot axes in Cartesian coordinates. Valid index: 1-8.
- BaseCartesian: Base axes in Cartesian coordinates. Valid index: 1-8.

## FlipNoFlipInformation

`from underautomation.yaskawa.high_speed_e_server.flip_no_flip_information import FlipNoFlipInformation`

Specifies the flip/no-flip wrist configuration.

- Flip: Flip configuration - wrist is in flipped orientation.
- NoFlip: No-flip configuration - wrist is in standard orientation.

## GetFileProgress

`from underautomation.yaskawa.high_speed_e_server.get_file_progress import GetFileProgress`

Contains progress information for file download (GetFile) operations. Used with the GetFileProgressDelegate callback to track download progress.

- `completed: bool (read only)`: Gets whether the file download has completed successfully.
- `file_name: str (read only)`: Gets the name of the file being downloaded.
- `downloaded_bytes: int (read only)`: Gets the number of bytes downloaded so far.

## HighSpeedEServerClient

`from underautomation.yaskawa.high_speed_e_server.high_speed_e_server_client import HighSpeedEServerClient`

Main client class for communicating with Yaskawa Motoman industrial robots using the High Speed Ethernet Server protocol. This class provides methods for reading robot status, positions, variables, and controlling robot operations via UDP.

- `HighSpeedEServerClient()`: Creates a new instance of HighSpeedEServerClient for robot communication. Call Connect() to establish communication with a robot controller.
- `connect(ip: str, parameters: HighSpeedEServerConnectParameters) -> None`: Connects to a robot controller with custom connection parameters object.
- Inherited from [HighSpeedEServerClientBase](underautomation.yaskawa.high_speed_e_server.internal.md#highspeedeserverclientbase-robothigh_speed_e_server): `close`, `get_alarm`, `get_status_information`, `get_executing_job_information`, `get_job_stack`, `get_configuration_information`, `get_robot_cartesian_position`, `get_robot_joint_position`, `get_robot_position`, `get_position_error`, `get_torque`, `alarm_reset`, `display`, `start_job`, `select_job`, `get_management_time`, `get_system_information`, `get_system_parameter`, `read_io`, `write_io`, `write_io_network_input`, `read_register`, `write_register`, `read_byte`, `write_byte`, `read_integer`, `write_integer`, `read_double_integer`, `write_double_integer`, `read_real`, `write_real`, `read16_bytes_char`, `write16_bytes_char`, `read_position_variable`, `write_position_variable`, `read_base_position`, `write_base_position`, `read_external_position`, `write_external_position`, `get_alarm_extended`, `move_cartesian`, `move_joints`, `read32_bytes_char`, `write32_bytes_char`, `delete_file`, `load_file`, `get_file_list`, `get_file`, `batch_data_backup`, `set_servo`, `set_hold`, `set_teach_pendant_lock_state`, `set_cycle`, `ip`, `connected`

## HighSpeedEServerConnectParameters

`from underautomation.yaskawa.high_speed_e_server.high_speed_e_server_connect_parameters import HighSpeedEServerConnectParameters`

Base class defining connection parameters for the High Speed Ethernet Server communication. This class cannot be instantiated directly; use a derived class or use Connect with optional parameters. Allows customization of timeouts and ports for different network environments.

- `HighSpeedEServerConnectParameters()`: Initializes a new instance of the connection parameters class.
- `data_timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for a response to data commands. Applies to most read/write operations like position reading, variable access, etc. Default: 1500ms.
- `power_on_timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for servo power on to complete. Servo power on may take longer due to brake release and motor initialization. Default: 8000ms.
- `file_timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for file operation responses. File operations may be slower due to larger data transfers and disk I/O on the controller. Default: 4000ms.
- `data_port: int`: Gets or sets the UDP port number for data communication. Must match the robot controller's High Speed Ethernet Server data port configuration. Default: 10040.
- `file_port: int`: Gets or sets the UDP port number for file transfer operations. Must match the robot controller's High Speed Ethernet Server file port configuration. Default: 10041.
- `static DEFAULT_DATA_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for data commands (1500ms).
- `static DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for servo power on operations (8000ms).
- `static DEFAULT_FILE_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for file operations (4000ms).
- `static DEFAULT_DATA_PORT: int`: Default UDP port for data communication (10040).
- `static DEFAULT_FILE_PORT: int`: Default UDP port for file transfer operations (10041).

## InvalidDataAnswerException

`from UnderAutomation.Yaskawa.HighSpeedEServer import InvalidDataAnswerException`

Exception thrown when the robot controller returns an error response to a High Speed Ethernet Server command. This exception contains detailed status codes that help identify the specific error condition.

The SDK raises this .NET type: catch it with `except InvalidDataAnswerException as e` after the import above. Its members keep their .NET names. The class `InvalidDataAnswerException` of the module `underautomation.yaskawa.high_speed_e_server.invalid_data_answer_exception` is not a Python exception and cannot be caught.

- `Status: int (read only)`: Gets the primary status code returned by the robot controller. A value of 0 indicates success; any other value indicates an error condition.
- `AddedStatus: int (read only)`: Gets the additional status code providing more detailed error information. The interpretation of this value depends on the primary Status code.
- Inherited from System.Exception: `Message`, `InnerException`

## LoadFileProgress

`from underautomation.yaskawa.high_speed_e_server.load_file_progress import LoadFileProgress`

Contains progress information for file upload (LoadFile) operations. Used with the LoadFileProgressDelegate callback to track upload progress.

- `completed: bool (read only)`: Gets whether the file upload has completed successfully.
- `file_name: str (read only)`: Gets the name of the file being uploaded.
- `total_bytes: int (read only)`: Gets the total size of the file in bytes.
- `loaded_bytes: int (read only)`: Gets the number of bytes uploaded so far.

## ManagementTimeType

`from underautomation.yaskawa.high_speed_e_server.management_time_type import ManagementTimeType`

Specifies the type of management time data to retrieve. Different metrics track various aspects of robot operation.

- ControlPowerOnTime: Total time the controller power has been on.
- ServoPowerOnTimeTotal: Total servo power on time across all robots.
- ServoPowerOnTimR1ToR8: Servo power on time for robots R1 through R8. Pass the robot number (1 to 8) as index of GetManagementTime.
- ServoPowerOnTimeS1ToS24: Servo power on time for stations S1 through S24. Pass the station number (1 to 24) as index of GetManagementTime.
- PlayBackTimeTotal: Total playback time across all robots.
- PlayBackTimeR1ToR8: Playback time for robots R1 through R8. Pass the robot number (1 to 8) as index of GetManagementTime.
- PlayBackTimeS1ToS24: Playback time for stations S1 through S24. Pass the station number (1 to 24) as index of GetManagementTime.
- MotionTimeTotal: Total motion time across all robots.
- MotionTimeR1ToR8: Motion time for robots R1 through R8. Pass the robot number (1 to 8) as index of GetManagementTime.
- MotionTimeS1ToS24: Motion time for stations S1 through S24. Pass the station number (1 to 24) as index of GetManagementTime.
- OperationTimeApplication1To8: Operation time for applications 1 through 8. Add application number (0-7) to get specific application.

## OnOffCommandType

`from underautomation.yaskawa.high_speed_e_server.on_off_command_type import OnOffCommandType`

Specifies the type of ON/OFF command to send to the robot controller. These commands control fundamental robot states that affect safety and operation.

- Hold: Hold command - pauses robot motion while maintaining servo power. Robot can resume from held position. Value: 1.
- Servo: Servo power command - enables or disables motor power to the robot. Servo must be ON for the robot to move. Value: 2.
- HLock: Lock Teach Pendant. Value: 3.

## OrientationFlipInformation

`from underautomation.yaskawa.high_speed_e_server.orientation_flip_information import OrientationFlipInformation`

Specifies the orientation (front/back) configuration of the robot arm. Determined by the position of the B-axis rotation center relative to the S-axis.

- Front: Front configuration - B-axis rotation center is in front of S-axis rotation center when viewed from the right-hand side of the robot.
- Back: Back configuration - B-axis rotation center is behind S-axis rotation center when viewed from the right-hand side of the robot.

## PositionCommandClassification

`from underautomation.yaskawa.high_speed_e_server.position_command_classification import PositionCommandClassification`

Specifies the speed classification (units) for motion commands. Determines how the speed value is interpreted by the controller.

- LinkPercent: Speed as percentage of maximum link (joint) speed. Valid range: 0.01 to 100.00 percent.
- Cartesian_MM_S: Speed in millimeters per second for linear motion. Valid range depends on robot model.
- Cartesian_DEG_S: Speed in degrees per second for rotational motion. Valid range depends on robot model.

## PositionCommandOperationCoordinate

`from underautomation.yaskawa.high_speed_e_server.position_command_operation_coordinate import PositionCommandOperationCoordinate`

Specifies the coordinate system for position command interpretation. Determines how X, Y, Z, Rx, Ry, Rz values are interpreted.

- Base: Base coordinate system (world frame at robot base). Fixed reference frame typically aligned with robot mounting.
- Robot: Robot coordinate system. Reference frame at the robot's origin point.
- Tool: Tool coordinate system. Reference frame at the tool center point (TCP).
- User: User-defined coordinate system. Custom reference frame defined for specific workpiece or fixture.

## PositionCommandType

`from underautomation.yaskawa.high_speed_e_server.position_command_type import PositionCommandType`

Specifies the type of position command (motion instruction) to execute. Determines the path type and whether position is absolute or incremental.

- LinkAbsolute: Link (joint interpolated) motion to an absolute position. All joints move simultaneously to reach the target, resulting in non-linear TCP path.
- StraightAbsolute: Straight (linear interpolated) motion to an absolute position. TCP moves in a straight line to the target position.
- StraightIncrement: Straight (linear interpolated) motion by an incremental offset. TCP moves in a straight line relative to current position.

## RegardedReversePositionSpecified

`from underautomation.yaskawa.high_speed_e_server.regarded_reverse_position_specified import RegardedReversePositionSpecified`

Specifies how to handle position in reverse direction scenarios.

- Previous: Use the previous position as reference.
- Form: Use the specified form/posture as reference.

## RobotAlarmData

`from underautomation.yaskawa.high_speed_e_server.robot_alarm_data import RobotAlarmData`

Contains information about a robot alarm retrieved from the controller. Alarms indicate error conditions that may require operator intervention.

- `code: int (read only)`: Gets the alarm code identifying the specific alarm type. Alarm codes are documented in the robot's maintenance manual.
- `data: int (read only)`: Gets additional alarm data providing context about the alarm. The meaning depends on the specific alarm code.
- `type: int (read only)`: Gets the alarm type/category classification.
- `occurring_time: str (read only)`: Gets the timestamp when the alarm occurred. Format: "YYYY/MM/DD HH:MM:SS" (16 characters).
- `text: str (read only)`: Gets the alarm message text describing the alarm condition. Maximum 32 characters.

## RobotAlarmDataExtended

`from underautomation.yaskawa.high_speed_e_server.robot_alarm_data_extended import RobotAlarmDataExtended`

Contains extended information about a robot alarm, including sub-code details. Provides more detailed diagnostic information than the basic RobotAlarmData.

- `additionnal_information: str (read only)`: Gets additional information about the alarm condition. Maximum 16 characters.
- `sub_data: str (read only)`: Gets the sub-code data providing detailed error context. Maximum 96 characters.
- `sub_data_reverse: str (read only)`: Gets the reversed sub-code data. Maximum 96 characters.
- Inherited from [RobotAlarmData](underautomation.yaskawa.high_speed_e_server.md#robotalarmdata): `code`, `data`, `type`, `occurring_time`, `text`

## RobotAxisConfigData

`from underautomation.yaskawa.high_speed_e_server.robot_axis_config_data import RobotAxisConfigData`

Represents raw axis data with string values for axis configuration information. Used to retrieve axis name/type information from the robot controller.

- `axes: typing.List[str] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: str`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: str`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: str`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: str`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: str`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: str`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: str`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: str`: Gets or sets the value for axis 8 (optional additional axis).

## RobotAxisIntData

`from underautomation.yaskawa.high_speed_e_server.robot_axis_int_data import RobotAxisIntData`

Represents raw axis data with 32-bit integer values for up to 8 axes. This is a concrete implementation commonly used for pulse-based position data.

- `axes: typing.List[int] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: int`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: int`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: int`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: int`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: int`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: int`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: int`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: int`: Gets or sets the value for axis 8 (optional additional axis).

## RobotAxisRawData1

`from underautomation.yaskawa.high_speed_e_server.robot_axis_raw_data_1 import RobotAxisRawData1`

Represents raw axis data with generic value type for up to 8 axes. This is the base class for position-related data structures.

- `axes: typing.List[T] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: T`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: T`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: T`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: T`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: T`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: T`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: T`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: T`: Gets or sets the value for axis 8 (optional additional axis).

## RobotBasePositionData

`from underautomation.yaskawa.high_speed_e_server.robot_base_position_data import RobotBasePositionData`

Represents base position data for coordinated motion with travel units or external bases. Base positions define the location of the robot's base in world coordinates or pulse values.

- `RobotBasePositionData(header: RobotDataHeader)`: Creates a new instance of RobotBasePositionData with the specified header information.
- `data_type: RobotBasePositionType (read only)`: Gets the data type indicating whether values are pulse or coordinate values.
- `is_defined: bool (read only)`: Gets whether the variable is taught on the controller. False for a variable read with read_base_position() that is not defined: its values are then all 0.
- `axes: typing.List[int] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: int`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: int`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: int`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: int`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: int`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: int`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: int`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: int`: Gets or sets the value for axis 8 (optional additional axis).

## RobotBasePositionType

`from underautomation.yaskawa.high_speed_e_server.robot_base_position_type import RobotBasePositionType`

Defines the type of base position data representation.

- PulseValue: Position is represented as encoder pulse values.
- BaseCoordinateValue: Position is represented in base coordinate system values.

## RobotBasePositionVariableData

`from underautomation.yaskawa.high_speed_e_server.robot_base_position_variable_data import RobotBasePositionVariableData`

Represents data returned from reading multiple base position variables (BP variables) from the robot controller. BP variables store base position information used for coordinated motion with external axes or travel units.

- `value: typing.List[RobotBasePositionData] (read only)`: Gets the array of base position data read from the robot controller.

## RobotByteVariableData

`from underautomation.yaskawa.high_speed_e_server.robot_byte_variable_data import RobotByteVariableData`

Represents data returned from reading multiple byte variables (B variables) from the robot controller. B variables are 8-bit unsigned integer storage locations (0-255).

- `value: typing.List[int] (read only)`: Gets the array of byte variable values read from the robot controller.

## RobotControlGroup

`from underautomation.yaskawa.high_speed_e_server.robot_control_group import RobotControlGroup`

Represents a robot control group combining a group type with an index. Used to specify which robot or station to query in multi-robot systems.

- `RobotControlGroup(group: ControlGroup, index: int)`: Creates a new RobotControlGroup with the specified group type and index.
- `group: ControlGroup`: The control group type (robot, base, station).
- `index: int`: The index within the control group (e.g., robot number 1-8).
- `byte_value: int`: The combined byte value sent to the robot controller (Group + Index).
- `static DefaultRobotCartesian: 'RobotControlGroup'`: Default control group for Cartesian position of robot 1.
- `static DefaultRobotPulse: 'RobotControlGroup'`: Default control group for pulse position of robot 1.

## RobotData

`from underautomation.yaskawa.high_speed_e_server.robot_data import RobotData`

Base class for all robot data response objects returned by High Speed Ethernet Server commands. Contains common header information about the communication response.

- `RobotData()`: Creates a blank instance of RobotData, for use as input to robot commands (e.g. kinematics conversions).

## RobotDataHeader

`from underautomation.yaskawa.high_speed_e_server.robot_data_header import RobotDataHeader`

Information about a response of the robot controller: the controller that answered, the size of the data, and the state of a transfer in several parts.

- `RobotDataHeader()`
- `ip: typing.Any (read only)`: Gets the IP endpoint (address and port) of the robot controller that sent the response. Useful for identifying the source in multi-robot configurations.
- `data_size: int (read only)`: Gets the size, in bytes, of the data returned by the controller in this response.
- `block_no: int (read only)`: Gets the raw block number of a transfer in several parts, such as a file transfer. Use is_last_block to know if this response is the last part.
- `is_last_block: bool (read only)`: Gets a value indicating whether this response is the last part of a transfer in several parts.

## RobotDoubleIntegerVariableData

`from underautomation.yaskawa.high_speed_e_server.robot_double_integer_variable_data import RobotDoubleIntegerVariableData`

Represents data returned from reading multiple double-precision integer variables (D variables) from the robot controller.

- `value: typing.List[int] (read only)`: Gets the array of double integer values read from the robot controller.

## RobotExternalAxisData

`from underautomation.yaskawa.high_speed_e_server.robot_external_axis_data import RobotExternalAxisData`

Represents external axis position data for positioners, travel units, or additional servo axes. External axes are coordinated with the robot motion for applications like welding positioners.

- `RobotExternalAxisData(header: RobotDataHeader)`: Creates a new instance of RobotExternalAxisData with the specified header information.
- `is_defined: bool (read only)`: Gets whether the variable is taught on the controller. False for a variable read with read_external_position() that is not defined: its values are then all 0.
- `axes: typing.List[int] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: int`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: int`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: int`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: int`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: int`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: int`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: int`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: int`: Gets or sets the value for axis 8 (optional additional axis).

## RobotExternalAxisVariableData

`from underautomation.yaskawa.high_speed_e_server.robot_external_axis_variable_data import RobotExternalAxisVariableData`

Represents data returned from reading multiple external axis variables (EX variables) from the robot controller. EX variables store position data for external axes such as positioners, travel units, or additional servo axes.

- `value: typing.List[RobotExternalAxisData] (read only)`: Gets the array of external axis data read from the robot controller.

## RobotFileContentData

`from underautomation.yaskawa.high_speed_e_server.robot_file_content_data import RobotFileContentData`

Contains the content of a file downloaded from the robot controller. Provides methods for parsing structured file content such as job files and parameter files.

- `get_param(section: str, parameterLine: int, parameterColumn: int) -> int`: Extracts an integer parameter value from a structured file section. Useful for reading values from parameter files and job data.
- `headers: typing.Any (read only)`: Gets the list of response headers from multi-block transfers. Large files are transferred in multiple UDP packets.
- `content: str (read only)`: Gets the text content of the downloaded file.
- `content_raw: typing.List[int] (read only)`: Gets the text content of the downloaded file.
- `file_name: str (read only)`: Gets the name of the downloaded file.

## RobotFileListData

`from underautomation.yaskawa.high_speed_e_server.robot_file_list_data import RobotFileListData`

Contains the result of a file listing operation on the robot controller. Returns an array of file names matching the specified pattern.

- `headers: typing.Any (read only)`: Gets the list of response headers from multi-block transfers. File listings may span multiple UDP packets for large directories.
- `files: typing.List[str] (read only)`: Gets the array of file names returned by the listing operation. File names include extensions (e.g., "MYJOB.JBI", "SYSTEM.SYS").

## RobotIOData

`from underautomation.yaskawa.high_speed_e_server.robot_io_data import RobotIOData`

Represents data returned from reading multiple I/O (Input/Output) points from the robot controller. I/O addresses are organized in groups based on their function and accessibility.

- `value: typing.List[int] (read only)`: Gets the array of I/O byte values read from the robot controller. Each byte represents 8 consecutive I/O points where each bit corresponds to one I/O state.

## RobotIntegerVariableData

`from underautomation.yaskawa.high_speed_e_server.robot_integer_variable_data import RobotIntegerVariableData`

Represents data returned from reading multiple integer variables (I variables) from the robot controller. I variables are 16-bit signed integer storage locations.

- `value: typing.List[int] (read only)`: Gets the array of integer variable values read from the robot controller.

## RobotJobData

`from underautomation.yaskawa.high_speed_e_server.robot_job_data import RobotJobData`

Contains information about the currently executing job (program) on the robot controller. Retrieved using the executing job information reading command.

- `name: str (read only)`: Gets the name of the currently selected/executing job. Job names can be up to 32 characters. Returns empty string if no job is selected.
- `line: int (read only)`: Gets the current line number being executed within the job. Line numbers are 1-based and correspond to the job listing.
- `step: int (read only)`: Gets the current step number within the job. Step numbers track the execution progress through motion instructions.
- `speed_override: float (read only)`: Gets the current speed override percentage (0-100). This is the global speed multiplier applied to all motions.

## RobotJobStackData

`from underautomation.yaskawa.high_speed_e_server.robot_job_stack_data import RobotJobStackData`

Contains the job call stack for a specific task on the robot controller. Represents the current nesting of CALL instructions, from the outermost job to the currently executing one. Only supported on DX200 (AY/BY/YN) controllers.

- `jobs: typing.List[str] (read only)`: Gets the job names in the call stack, outermost first. The first entry is the root job, the last entry is the currently executing job. Empty if no nested calls are active.

## RobotKinematicsCartesianData

`from underautomation.yaskawa.high_speed_e_server.robot_kinematics_cartesian_data import RobotKinematicsCartesianData`

Cartesian position result from a kinematics conversion. Provides named X/Y/Z and orientation properties in engineering units in addition to the raw axis values.

- `x: float (read only)`: Gets the X position in millimetres (derived from the raw µm axis value).
- `y: float (read only)`: Gets the Y position in millimetres.
- `z: float (read only)`: Gets the Z position in millimetres.
- `rx: float (read only)`: Gets the Rx orientation in degrees (derived from the raw 0.0001° axis value).
- `ry: float (read only)`: Gets the Ry orientation in degrees.
- `rz: float (read only)`: Gets the Rz orientation in degrees.
- Inherited from [RobotKinematicsPositionData](underautomation.yaskawa.high_speed_e_server.md#robotkinematicspositiondata): `data_type`, `form`, `tool_number`, `user_coordinate_number`, `axes`

## RobotKinematicsJointData

`from underautomation.yaskawa.high_speed_e_server.robot_kinematics_joint_data import RobotKinematicsJointData`

Joint-space position result from a kinematics conversion. Provides the 8 joint axis values in both raw 0.0001° units and as a ready-to-use degrees array.

- `axis_degrees: typing.List[float] (read only)`: Gets the 8 joint axis values converted to degrees. Each element equals the corresponding axes value divided by 10 000.
- Inherited from [RobotKinematicsPositionData](underautomation.yaskawa.high_speed_e_server.md#robotkinematicspositiondata): `data_type`, `form`, `tool_number`, `user_coordinate_number`, `axes`

## RobotKinematicsPositionData

`from underautomation.yaskawa.high_speed_e_server.robot_kinematics_position_data import RobotKinematicsPositionData`

Base class for kinematic position data exchanged with the robot controller. Contains coordinate type, posture flags, tool/user numbers, and the 8 raw axis values.

- `RobotKinematicsPositionData()`: Creates a blank instance for use as input to kinematics conversion methods.
- `data_type: RobotPositionDataType`: Gets or sets the coordinate type of this position.
- `form: RobotPosture`: Gets or sets the posture/form flags for this position.
- `tool_number: int`: Gets or sets the tool number used for this position.
- `user_coordinate_number: int`: Gets or sets the user coordinate number used for this position.
- `axes: typing.List[int]`: Gets or sets the 8 raw axis values. For joint positions: values in 0.0001° units (divide by 10 000 for degrees). For Cartesian positions: XYZ axes (0–2) in µm; orientation axes (3–5) in 0.0001°.

## RobotManagementTimeData

`from underautomation.yaskawa.high_speed_e_server.robot_management_time_data import RobotManagementTimeData`

Contains management time information for tracking robot operation statistics. Provides uptime and usage metrics for maintenance planning and reporting.

- `start_time: str (read only)`: Gets the start time of the tracked period. Format: "YYYY/MM/DD HH:MM" (16 characters).
- `ellapse_time: str (read only)`: Gets the elapsed time for the tracked metric. Format: "HHHH:MM:SS.ss" or similar time duration format (12 characters).

## RobotPluralData1

`from underautomation.yaskawa.high_speed_e_server.robot_plural_data_1 import RobotPluralData1`

Represents a collection of data values returned from plural (batch) read operations. Used for reading multiple variables, registers, or I/O points in a single request.

- `value: typing.List[T] (read only)`: Gets the array of values read from the robot controller. The array length corresponds to the number of values successfully read.

## RobotPositionCartesianData

`from underautomation.yaskawa.high_speed_e_server.robot_position_cartesian_data import RobotPositionCartesianData`

Represents Cartesian position data with coordinates in millimeters and degrees. This class provides human-readable position data converted from the raw protocol values.

- `form: RobotPosture (read only)`: Gets the robot posture (form) data defining the kinematic configuration.
- `data_type: RobotPositionDataType (read only)`: Gets the position data type indicating the coordinate system used.
- `tool_number: int (read only)`: Gets the tool number (TCP) used for this position.
- `user_coordinate_number: int (read only)`: Gets the user coordinate system number used for this position.
- `x: float (read only)`: Gets the X coordinate in millimeters.
- `y: float (read only)`: Gets the Y coordinate in millimeters.
- `z: float (read only)`: Gets the Z coordinate in millimeters.
- `rx: float (read only)`: Gets the rotation around X axis (Rx) in degrees.
- `ry: float (read only)`: Gets the rotation around Y axis (Ry) in degrees.
- `rz: float (read only)`: Gets the rotation around Z axis (Rz) in degrees.

## RobotPositionData1

`from underautomation.yaskawa.high_speed_e_server.robot_position_data_1 import RobotPositionData1`

Represents generic robot position data with axis values of the specified type. This class provides a flexible structure for storing position information that can be represented in different data formats (pulse values, Cartesian coordinates, etc.).

- `RobotPositionData1(header: RobotDataHeader)`: Creates a new instance of RobotPositionData with the specified header information.
- `form: RobotPosture`: Gets or sets the robot posture (form) data defining the robot's kinematic configuration. This includes flip/no-flip state, arm configuration (upper/lower), and axis angle ranges.
- `data_type: RobotPositionDataType`: Gets or sets the position data type indicating the coordinate system used. Determines how axis values should be interpreted (pulse, base, robot, user, or tool coordinates).
- `tool_number: int`: Gets or sets the tool number (TCP - Tool Center Point) used for this position. Tool numbers typically range from 0-63, where 0 is often the robot flange center.
- `user_coordinate_number: int`: Gets or sets the user coordinate system number used for this position. User coordinates define custom reference frames for specific workpiece locations.
- `is_defined: bool (read only)`: Gets whether the variable is taught on the controller. False for a variable read with read_position_variable() that is not defined: its values are then all 0.
- `axes: typing.List[T] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: T`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: T`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: T`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: T`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: T`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: T`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: T`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: T`: Gets or sets the value for axis 8 (optional additional axis).

## RobotPositionDataType

`from underautomation.yaskawa.high_speed_e_server.robot_position_data_type import RobotPositionDataType`

Defines the coordinate system type for position data.

- PulseValue: Position in encoder pulse values (joint space).
- BaseCoordinateValue: Position in base coordinate system (world frame, value 16).
- RobotCoordinateValue: Position in robot coordinate system (robot base frame, value 17).
- ToolCoordinateValue: Position in tool coordinate system (value 18).
- UserCoordinateValue: Position in user-defined coordinate system (value 19).

## RobotPositionIntData

`from underautomation.yaskawa.high_speed_e_server.robot_position_int_data import RobotPositionIntData`

Represents robot position data with 32-bit integer axis values. This is the primary type used for pulse-based position data from the High Speed Ethernet Server. Axis values are in pulse units (encoder counts) or scaled coordinate values.

- `RobotPositionIntData(header: RobotDataHeader)`: Creates a new instance of RobotPositionIntData with the specified header information.
- `to_cartesian() -> RobotPositionCartesianData`: Converts a Cartesian position to millimeters and degrees.
- `form: RobotPosture`: Gets or sets the robot posture (form) data defining the robot's kinematic configuration. This includes flip/no-flip state, arm configuration (upper/lower), and axis angle ranges.
- `data_type: RobotPositionDataType`: Gets or sets the position data type indicating the coordinate system used. Determines how axis values should be interpreted (pulse, base, robot, user, or tool coordinates).
- `tool_number: int`: Gets or sets the tool number (TCP - Tool Center Point) used for this position. Tool numbers typically range from 0-63, where 0 is often the robot flange center.
- `user_coordinate_number: int`: Gets or sets the user coordinate system number used for this position. User coordinates define custom reference frames for specific workpiece locations.
- `is_defined: bool (read only)`: Gets whether the variable is taught on the controller. False for a variable read with Int32%2cSystem.Int32) that is not defined: its values are then all 0.
- `axes: typing.List[int] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: int`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: int`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: int`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: int`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: int`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: int`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: int`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: int`: Gets or sets the value for axis 8 (optional additional axis).

## RobotPositionVariableData

`from underautomation.yaskawa.high_speed_e_server.robot_position_variable_data import RobotPositionVariableData`

Represents data returned from reading multiple position variables (P variables) from the robot controller. P variables store complete robot position data including coordinates, posture, tool and user coordinate references.

- `value: typing.List[RobotPositionIntData] (read only)`: Gets the array of position variable data read from the robot controller. Each element contains full position information including axis values, posture, and coordinate references.

## RobotPosture

`from underautomation.yaskawa.high_speed_e_server.robot_posture import RobotPosture`

Represents the complete robot posture (form) configuration. Encodes the kinematic configuration choices that determine which of multiple inverse kinematics solutions is used to reach a Cartesian position.

- `RobotPosture(orientation: OrientationFlipInformation, arm: ArmFlipInformation, flip: FlipNoFlipInformation, rAxis: AxisFlipInformation, tAxis: AxisFlipInformation, sAxis: AxisFlipInformation, redundant: OrientationFlipInformation, regardedReversePositionSpecified: RegardedReversePositionSpe...`: Creates a new RobotPosture with specified configuration values.
- `to_integer() -> int`: Converts the posture to a single 16-bit integer value. Form is stored in the low byte, ExtendedForm in the high byte.
- `static from_integer(value: int) -> 'RobotPosture'`: Creates a RobotPosture from a combined 16-bit integer value.
- `form: int`: Gets or sets the primary form byte encoding basic posture flags. Bit-encoded: orientation, arm, flip, R-axis, T-axis, S-axis, redundant, reverse position.
- `extended_form: int`: Gets or sets the extended form byte for additional axis configurations. Bit-encoded: L-axis, U-axis, B-axis, E-axis, W-axis range flags.
- `orientation: OrientationFlipInformation`: Gets or sets the front/back orientation configuration. Specifies where the B-axis rotation center locates relative to the S-axis when viewing the L and U axes from the right-hand side.
- `arm: ArmFlipInformation`: Gets or sets the upper/lower arm configuration based on L and U axis positions.
- `flip: FlipNoFlipInformation`: Gets or sets the flip/no-flip wrist configuration.
- `r_axis: AxisFlipInformation`: Gets or sets the R-axis (wrist rotation) angle range configuration.
- `t_axis: AxisFlipInformation`: Gets or sets the T-axis (tool rotation) angle range configuration.
- `s_axis: AxisFlipInformation`: Gets or sets the S-axis (base rotation) angle range configuration.
- `redundant: OrientationFlipInformation`: Gets or sets the redundant axis orientation configuration (for 7+ axis robots).
- `regarded_reverse_position_specified: RegardedReversePositionSpecified`: Gets or sets the reverse position specification mode.
- `l_axis: AxisFlipInformation`: Gets or sets the L-axis (lower arm) angle range configuration from extended form.
- `u_axis: AxisFlipInformation`: Gets or sets the U-axis (upper arm) angle range configuration from extended form.
- `b_axis: AxisFlipInformation`: Gets or sets the B-axis (wrist bend) angle range configuration from extended form.
- `e_axis: AxisFlipInformation`: Gets or sets the E-axis (external/elbow) angle range configuration from extended form.
- `w_axis: AxisFlipInformation`: Gets or sets the W-axis angle range configuration from extended form.
- `static Default: 'RobotPosture'`: Default posture with Form=0 and ExtendedForm=0.

## RobotRealVariableData

`from underautomation.yaskawa.high_speed_e_server.robot_real_variable_data import RobotRealVariableData`

Represents data returned from reading multiple real variables (R variables) from the robot controller. R variables are 32-bit single-precision floating point storage locations.

- `value: typing.List[float] (read only)`: Gets the array of single-precision floating point values read from the robot controller.

## RobotRecentAlarm

`from underautomation.yaskawa.high_speed_e_server.robot_recent_alarm import RobotRecentAlarm`

Specifies which recent alarm to retrieve from the robot controller. The controller maintains a history of the most recent alarms.

- Latest: The most recent (current) alarm.
- SecondLatest: The second most recent alarm.
- ThirdLatest: The third most recent alarm.
- FourthLatest: The fourth most recent alarm.

## RobotRegisterData

`from underautomation.yaskawa.high_speed_e_server.robot_register_data import RobotRegisterData`

Represents data returned from reading multiple register values from the robot controller. Registers are 16-bit signed integer storage locations used for general-purpose data.

- `value: typing.List[int] (read only)`: Gets the array of register values read from the robot controller. Each value is a 16-bit signed integer (-32768 to 32767).

## RobotStatusData

`from underautomation.yaskawa.high_speed_e_server.robot_status_data import RobotStatusData`

Contains the current operational status of the robot controller. Provides information about the robot's mode, running state, and safety conditions. Retrieved using the status information reading command.

- `step: bool (read only)`: Gets whether the robot is in step (single-step) execution mode. When true, the robot executes one instruction at a time.
- `cycle: bool (read only)`: Gets whether the robot is in cycle execution mode. When true, the robot executes one complete cycle then stops.
- `automatic: bool (read only)`: Gets whether the robot is in automatic operation mode. When true, the robot can operate automatically without pendant interaction.
- `running: bool (read only)`: Gets whether the robot is currently running (executing a job).
- `in_guard_safe_operation: bool (read only)`: Gets whether the robot is in guard safe operation mode. Indicates collaborative/safety-rated operation mode is active.
- `teach: bool (read only)`: Gets whether the robot is in teach mode. In teach mode, the robot can be manually positioned and jobs can be edited.
- `play: bool (read only)`: Gets whether the robot is in play mode. In play mode, the robot can execute programmed jobs.
- `command_remote: bool (read only)`: Gets whether remote command mode is enabled. When true, the robot accepts commands from external sources (including this API).
- `in_hold_status_pendant: bool (read only)`: Gets whether the robot is held by the programming pendant. Operator has pressed hold on the pendant.
- `in_hold_status_externally: bool (read only)`: Gets whether the robot is held by an external hold signal. External safety circuit has triggered a hold condition.
- `in_hold_status_by_command: bool (read only)`: Gets whether the robot is held by a command (software hold). A hold command was issued via the API or job instruction.
- `alarming: bool (read only)`: Gets whether an alarm is currently active. Check GetAlarm() for detailed alarm information.
- `error_occurring: bool (read only)`: Gets whether an error condition is occurring. Errors may prevent normal operation until resolved.
- `servo_on: bool (read only)`: Gets whether servo power is enabled. Servo must be ON for the robot to move.

## RobotStringVariableData

`from underautomation.yaskawa.high_speed_e_server.robot_string_variable_data import RobotStringVariableData`

Represents data returned from reading multiple string variables (S variables) from the robot controller. S variables can be either 16-byte or 32-byte character strings depending on the command used.

- `value: typing.List[str] (read only)`: Gets the array of string values read from the robot controller. Strings are null-terminated and trimmed of trailing null characters.

## RobotSystemInformation

`from underautomation.yaskawa.high_speed_e_server.robot_system_information import RobotSystemInformation`

Contains system information about the robot controller including software version and configuration. Retrieved using the system information acquiring command.

- `software_version: str (read only)`: Gets the controller software version string. Format typically includes model and version number. Maximum 24 characters.
- `name: str (read only)`: Gets the system/robot name or model identifier. Maximum 16 characters.
- `parameter: str (read only)`: Gets parameter file or configuration information. Maximum 8 characters.

## RobotSystemParamData

`from underautomation.yaskawa.high_speed_e_server.robot_system_param_data import RobotSystemParamData`

Contains a system parameter value read from the robot controller.

- `value: int (read only)`: Gets the raw system parameter value returned by the controller.

## RobotSystemType

`from underautomation.yaskawa.high_speed_e_server.robot_system_type import RobotSystemType`

Defines the types of system components that can be queried for information.

- Robot: Robot manipulator system (R1-R8). Valid index: 1-8.
- Station: Station/positioner system (S1-S24). Valid index: 1-24.
- Application: Application system (APP1-APP8). Valid index: 1-8.

## RobotSystemTypeData

`from underautomation.yaskawa.high_speed_e_server.robot_system_type_data import RobotSystemTypeData`

Represents a system type and index combination for querying specific robot system components. Used to specify which robot, station, or application to query in multi-robot configurations.

- `index: int`: Gets the index within the system type (1-based).
- `type: RobotSystemType`: Gets the system type (Robot, Station, or Application).
- `byte: int`: Gets the combined byte value sent to the controller (Type + Index).
- `static Default: 'RobotSystemTypeData'`: Default system type data for querying the primary robot (Robot 1).

## SwitchingCommands

`from underautomation.yaskawa.high_speed_e_server.switching_commands import SwitchingCommands`

Specifies the execution mode switching command to send to the robot controller. These modes control how the robot executes programmed jobs.

- Cycle: Cycle mode - robot executes one complete cycle of the program then stops. Useful for testing or single-part operations.
- Step: Step mode - robot executes one instruction at a time, stopping after each. Useful for debugging and detailed program verification.
- Continue_: Continuous mode - robot executes the program continuously until stopped. Normal production operation mode.

## SystemParameterTypes

`from underautomation.yaskawa.high_speed_e_server.system_parameter_types import SystemParameterTypes`

Specifies the category of a system parameter to read from the controller. Types S1CG, AP, and SE require a group number when reading.

- S1CG: S1CxG. requires group number.
- S2C: S2C
- S3C: S3C
- S4C: S4C
- RS: RS
- AP: AxP. Requires a group number.
- SE: SxE. Requires a group number.
