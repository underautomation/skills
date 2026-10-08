# underautomation.yaskawa.high_speed_e_server.internal

## HighSpeedEServerClientBase (robot.high_speed_e_server)

`from underautomation.yaskawa.high_speed_e_server.internal.high_speed_e_server_client_base import HighSpeedEServerClientBase`

Base class of the High Speed Ethernet Server client of a Yaskawa robot controller. Provides methods for reading robot status, positions, variables, and executing commands via UDP.

- `close() -> None`: Closes the connection to the robot controller and releases network resources.
- `get_alarm(alarm: RobotRecentAlarm) -> RobotAlarmData`: Reads alarm information from the robot controller. Retrieves alarm code, type, occurrence time, and descriptive text.
- `get_status_information() -> RobotStatusData`: Reads the current operational status of the robot controller. Returns information about mode (teach/play), running state, hold status, alarms, and servo power.
- `get_executing_job_information() -> RobotJobData`: Reads information about the currently selected and executing job (program). Returns job name, current line, step, and speed override percentage.
- `get_job_stack(taskNumber: int=0) -> RobotJobStackData`: Reads the job call stack for a specific task on the robot controller. Returns the current nesting of CALL instructions, from the outermost job to the currently executing one.
- `get_configuration_information(type: RobotControlGroup) -> RobotAxisConfigData`: Reads axis configuration information for a specified control group. Returns axis type names (e.g., "S", "L", "U", "R", "B", "T") for each axis.
- `get_configuration_information() -> RobotAxisConfigData`: Reads axis configuration information for the default robot control group. Returns axis type names for each of the 8 possible axes.
- `get_robot_cartesian_position() -> RobotPositionCartesianData`: Reads the current robot Cartesian position (TCP position and orientation). Coordinates are returned in millimeters for X, Y, Z and degrees for Rx, Ry, Rz.
- `get_robot_joint_position() -> RobotPositionIntData`: Reads the current robot joint position in pulse (encoder) values. Returns raw pulse values for all robot axes.
- `get_robot_position(type: RobotControlGroup) -> RobotPositionIntData`: Reads position data for a specified control group. Can read robot, base, or station position data depending on the control group specified.
- `get_position_error(type: RobotControlGroup) -> RobotAxisIntData`: Reads the position error for a specified control group. Position error indicates the difference between commanded and actual position.
- `get_position_error() -> RobotAxisIntData`: Reads the position error (difference between commanded and actual position) for the default robot. Values indicate servo tracking error in pulse units.
- `get_torque(type: RobotControlGroup) -> RobotAxisIntData`: Reads the current torque values for a specified control group's servo motors. Torque values indicate motor load as a percentage of rated torque.
- `get_torque() -> RobotAxisIntData`: Reads the current torque values for the default robot's servo motors. Torque values indicate motor load as a percentage of rated torque.
- `alarm_reset(type: AlarmResetType) -> RobotDataHeader`: Resets alarms or cancels errors on the robot controller. Use Reset to clear alarm conditions after resolving the cause. Use Cancel for recoverable errors that don't require alarm reset.
- `display(message: str) -> RobotDataHeader`: Displays a popup message on the robot programming pendant. Message will appear as a notification to the operator.
- `start_job() -> RobotDataHeader`: Starts execution of the currently selected job. The job must be selected first using SelectJob before calling this method. Servo must be ON and the robot must not be in alarm state.
- `select_job(job: str, line: int) -> RobotDataHeader`: Selects a job for execution and optionally positions to a specific line. Call StartJob after selecting to begin execution.
- `get_management_time(type: ManagementTimeType, index: int=0) -> RobotManagementTimeData`: Retrieves management time statistics from the robot controller. Can query various timing metrics like control power ON time, servo ON time, etc.
- `get_system_information(type: RobotSystemTypeData) -> RobotSystemInformation`: Retrieves system information for a specific robot system or control group. Use for multi-robot controllers or to query specific axes groups.
- `get_system_information() -> RobotSystemInformation`: Retrieves system information about the default robot system (R1). Returns software version, robot name, and parameter file information.
- `get_system_parameter(type: SystemParameterTypes, number: int, group: int=1) -> RobotSystemParamData`: Reads a system parameter from the robot controller.
- `read_io(type: IOType, group: int, count: int) -> RobotIOData`: Reads multiple I/O bytes from the robot controller using I/O group addressing. The starting byte index is computed from the I/O type and group number.
- `read_io(firstIndex: int, count: int) -> RobotIOData`: Reads multiple I/O bytes from the robot controller starting at a specified index.
- `write_io(type: IOType, group: int, data: typing.List[int]) -> RobotDataHeader`: Writes I/O bytes to the robot controller using I/O group addressing. By default, only Network Input can be written The starting byte index is computed from the I/O type and group number.
- `write_io(firstIndex: int, data: typing.List[int]) -> RobotDataHeader`: Writes I/O bytes to the robot controller starting at a specified index.
- `write_io_network_input(group: int, data: typing.List[int]) -> RobotDataHeader`: Writes network input bytes to the robot controller
- `read_register(firstIndex: int, count: int) -> RobotRegisterData`: Reads multiple 16-bit register values (M variables) from the robot controller. Registers are used for general-purpose integer storage in robot programs.
- `write_register(firstIndex: int, data: typing.List[int]) -> RobotDataHeader`: Writes multiple 16-bit register values (M variables) to the robot controller.
- `read_byte(firstIndex: int, count: int) -> RobotByteVariableData`: Reads multiple byte variables (B variables) from the robot controller. Byte variables are 8-bit unsigned values used for compact data storage.
- `write_byte(firstIndex: int, data: typing.List[int]) -> RobotDataHeader`: Writes byte variables (B variables) to the robot controller.
- `read_integer(firstIndex: int, count: int) -> RobotIntegerVariableData`: Reads multiple integer variables (I variables) from the robot controller. Integer variables are 16-bit signed values (-32768 to 32767).
- `write_integer(firstIndex: int, data: typing.List[int]) -> RobotDataHeader`: Writes integer variables (I variables) to the robot controller.
- `read_double_integer(firstIndex: int, count: int) -> RobotDoubleIntegerVariableData`: Reads multiple double-precision variables (D variables) from the robot controller. Note: The protocol actually transmits float values which are then cast to double.
- `write_double_integer(firstIndex: int, data: typing.List[int]) -> RobotDataHeader`: Writes double-precision variables (D variables) to the robot controller.
- `read_real(firstIndex: int, count: int) -> RobotRealVariableData`: Reads multiple real (single-precision float) variables (R variables) from the robot controller. Real variables are 32-bit IEEE 754 floating-point values.
- `write_real(firstIndex: int, data: typing.List[float]) -> RobotDataHeader`: Writes real (single-precision float) variables (R variables) to the robot controller.
- `read16_bytes_char(firstIndex: int, count: int) -> RobotStringVariableData`: Reads multiple 16-byte string variables (S variables) from the robot controller. String variables are fixed-length, null-terminated ASCII strings.
- `write16_bytes_char(firstIndex: int, data: typing.List[str]) -> RobotDataHeader`: Writes 16-byte string variables (S variables) to the robot controller. Strings longer than 16 characters will be truncated.
- `read_position_variable(firstIndex: int, count: int) -> RobotPositionVariableData`: Reads multiple position variables (P variables) from the robot controller. Each variable is a pulse position or a Cartesian position (base, robot, tool or user frame), with its posture, tool number and user frame number.
- `write_position_variable(firstIndex: int, data: typing.List[RobotPositionIntData]) -> RobotDataHeader`: Writes position variables (P variables) to the robot controller.
- `read_base_position(firstIndex: int, count: int) -> RobotBasePositionVariableData`: Reads multiple base position variables (BP variables) from the robot controller. Base position variables store the position of the base axes (travel axis) of a robot.
- `write_base_position(firstIndex: int, data: typing.List[RobotBasePositionData]) -> RobotDataHeader`: Writes base position variables (BP variables) to the robot controller.
- `read_external_position(firstIndex: int, count: int) -> RobotExternalAxisVariableData`: Reads multiple external axis variables (EX variables) from the robot controller. External axis variables store the position of the station axes (positioner...), in encoder pulses.
- `write_external_position(firstIndex: int, data: typing.List[RobotAxisRawData1] | typing.List[RobotExternalAxisData]) -> RobotDataHeader`: Writes external axis variables (EX variables) to the robot controller using generic type. Provided for backward compatibility with existing code. Writes external axis variables (EX variables) to the robot controller.
- `get_alarm_extended(alarm: RobotRecentAlarm) -> RobotAlarmDataExtended`: Retrieves extended alarm information including sub-code character strings. Provides more detailed information than GetAlarm for troubleshooting.
- `move_cartesian(x: float, y: float, z: float, rx: float, ry: float, rz: float, classification: PositionCommandClassification, speed: float, coordinate: PositionCommandOperationCoordinate, posture: RobotPosture=None, commandtype: PositionCommandType=PositionCommandType.StraightIncrement,...`: Commands the robot to move to a Cartesian position (X, Y, Z, Rx, Ry, Rz). Movement is relative to the specified coordinate system.
- `move_joints(axesPulse: typing.List[int], classification: PositionCommandClassification, speed: float, commandtype: PositionCommandType=PositionCommandType.StraightIncrement, RobotControlGroup: int=1, StationControlGroup: int=1, tool: int=0) -> RobotDataHeader`: Commands the robot to move using joint (pulse) positions. This specifies the position of each axis directly in encoder pulses.
- `read32_bytes_char(firstIndex: int, count: int) -> RobotStringVariableData`: Reads multiple 32-byte string variables (S variables) from the robot controller. Available on the controllers that store their S variables in 32 bytes (DX200, YRC1000...). Extended string variables for longer text storage than 16-byte variants.
- `write32_bytes_char(firstIndex: int, data: typing.List[str]) -> RobotDataHeader`: Writes 32-byte string variables (S variables) to the robot controller. Strings longer than 32 characters will be truncated.
- `delete_file(name: str) -> RobotDataHeader`: Deletes a file from the robot controller's file system. Use with caution as deleted files cannot be recovered.
- `load_file(name: str, content: str, onLoadFileProgress: typing.Callable[[LoadFileProgress], None]=None) -> typing.List[RobotDataHeader]`: Uploads (loads) a file from the PC to the robot controller. Large files are automatically split into 479-byte chunks for transmission.
- `get_file_list(pattern: str) -> RobotFileListData`: Retrieves a list of files matching a pattern from the robot controller. Supports wildcards for matching multiple files.
- `get_file(name: str, onGetFileProgress: typing.Callable[[GetFileProgress], None]=None) -> RobotFileContentData`: Downloads (saves) a file from the robot controller to the PC. Large files are received in multiple blocks and automatically reassembled. Special use case : to download CMOS.BIN, first perform a CMOS backup using BatchDataBackup, then use GetFile with the backup file path.
- `batch_data_backup(file: str="/SPDRV/CMOSBK.BIN") -> RobotDataHeader`: Performs a backup of the robot's CMOS. The CMOS.BIN file is copied locally in the robot controller to "/SPDRC/CMOSBK.BIN". The operation can take several seconds to complete. After this command, the backup file can be downloaded using GetFile("/SPDRC/CMOSBK.BIN"). To enable this command : in "MAN...
- `set_servo(enable: bool) -> RobotDataHeader`: Enables or disables servo power.
- `set_hold(enable: bool) -> RobotDataHeader`: Sets the hold state of the robot.
- `set_teach_pendant_lock_state(locked: bool) -> RobotDataHeader`: Locks or unlocks the teach pendant.
- `set_cycle(cycle: RobotCycleType) -> RobotDataHeader`: Sets the execution cycle type.
- `ip: str (read only)`: Gets the IP address or hostname of the connected robot controller.
- `connected: bool (read only)`: Gets a value indicating whether the client is connected to a robot controller. Note: Since UDP is connectionless, this only indicates if the socket is configured.

## HighSpeedEServerClientInternal (robot.high_speed_e_server)

`from underautomation.yaskawa.high_speed_e_server.internal.high_speed_e_server_client_internal import HighSpeedEServerClientInternal`

Internal implementation of the High Speed Ethernet Server client. This class provides the concrete implementation used internally by the SDK.

- Inherited from [HighSpeedEServerClientBase](underautomation.yaskawa.high_speed_e_server.internal.md#highspeedeserverclientbase-robothigh_speed_e_server): `close`, `get_alarm`, `get_status_information`, `get_executing_job_information`, `get_job_stack`, `get_configuration_information`, `get_robot_cartesian_position`, `get_robot_joint_position`, `get_robot_position`, `get_position_error`, `get_torque`, `alarm_reset`, `display`, `start_job`, `select_job`, `get_management_time`, `get_system_information`, `get_system_parameter`, `read_io`, `write_io`, `write_io_network_input`, `read_register`, `write_register`, `read_byte`, `write_byte`, `read_integer`, `write_integer`, `read_double_integer`, `write_double_integer`, `read_real`, `write_real`, `read16_bytes_char`, `write16_bytes_char`, `read_position_variable`, `write_position_variable`, `read_base_position`, `write_base_position`, `read_external_position`, `write_external_position`, `get_alarm_extended`, `move_cartesian`, `move_joints`, `read32_bytes_char`, `write32_bytes_char`, `delete_file`, `load_file`, `get_file_list`, `get_file`, `batch_data_backup`, `set_servo`, `set_hold`, `set_teach_pendant_lock_state`, `set_cycle`, `ip`, `connected`

## HighSpeedEServerConnectParametersInternal

`from underautomation.yaskawa.high_speed_e_server.internal.high_speed_e_server_connect_parameters_internal import HighSpeedEServerConnectParametersInternal`

Represents a set of High Speed Ethernet Server connection parameters

- `HighSpeedEServerConnectParametersInternal()`
- `enable: bool`: Gets or sets a value indicating whether to enable the High Speed Ethernet Server connection (default: true).
- Inherited from [HighSpeedEServerConnectParameters](underautomation.yaskawa.high_speed_e_server.md#highspeedeserverconnectparameters): `DEFAULT_DATA_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_FILE_TIMEOUT_MILLISECONDS`, `DEFAULT_DATA_PORT`, `DEFAULT_FILE_PORT`, `data_timeout_milliseconds`, `power_on_timeout_milliseconds`, `file_timeout_milliseconds`, `data_port`, `file_port`
