# underautomation.yaskawa.host_control

## EServerClient

`from underautomation.yaskawa.host_control.e_server_client import EServerClient`

Standalone client class for communicating with Yaskawa Motoman industrial robots using the Host Control protocol via Ethernet Server (TCP). This class provides methods for reading robot status, positions, variables, and controlling robot operations.

- `EServerClient()`: Creates a new instance of EServerClient for robot communication via TCP. Call Connect() to configure communication with a robot controller.
- `connect(ip: str, parameters: EServerConnectParameters) -> None`: Configures connection to the robot controller via TCP.
- `connect(ip: str) -> None`: Configures connection to the robot controller via TCP using default parameters.
- Inherited from [EServerClientInternal](underautomation.yaskawa.host_control.internal.md#eserverclientinternal-robote_server): `close`, `connected`, `address`, `port`
- Inherited from [HostControlClientBase](underautomation.yaskawa.host_control.internal.md#hostcontrolclientbase-robote_server): `get_alarm`, `get_status_information`, `get_executing_job_information`, `get_control_group`, `get_robot_joint_position`, `get_robot_cartesian_position`, `set_hold`, `alarm_reset`, `error_cancel`, `set_mode`, `set_cycle`, `set_servo`, `set_teach_pendant_lock_state`, `display`, `start_job`, `set_control_group`, `set_task`, `move_joint`, `move_linear`, `move_incremental`, `move_pulse_joint`, `move_pulse_linear`, `read_io`, `write_io`, `read_byte`, `write_byte`, `read_integer`, `write_integer`, `read_double_integer`, `write_double_integer`, `read_real`, `write_real`, `read16_bytes_char`, `write16_bytes_char`, `get_job_directory`, `get_user_frame`, `set_user_frame`, `delete_job`, `set_master_job`, `select_job`, `wait_for_job_completion`, `convert_to_relative_job`, `convert_to_standard_job`, `get_torque`, `get_max_torque`, `get_encoder_temperature`, `get_system_time`, `get_absolute_encoder_position`, `set_absolute_encoder_position`, `set_frame_type`, `get_alarm_with_messages`

## EServerConnectParameters

`from underautomation.yaskawa.host_control.e_server_connect_parameters import EServerConnectParameters`

Base class defining Ethernet Server (TCP) connection parameters for the Host Control communication. This class provides configuration for TCP-based communication with YRC1000 controllers.

- `EServerConnectParameters()`: Initializes a new instance of the Ethernet Server connection parameters.
- `port: int`: Gets or sets the TCP port number for Ethernet Server communication. Must match the robot controller's Ethernet Server port configuration. Default: 80.
- `static DEFAULT_PORT: int`: Default TCP port for Ethernet Server communication (80).
- Inherited from [HostControlConnectParametersBase](underautomation.yaskawa.host_control.internal.md#hostcontrolconnectparametersbase): `DEFAULT_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_MOTION_TIMEOUT_MILLISECONDS`, `timeout_milliseconds`, `power_on_timeout_milliseconds`, `motion_timeout_milliseconds`

## HostControlAlarmData

`from underautomation.yaskawa.host_control.host_control_alarm_data import HostControlAlarmData`

Contains alarm information retrieved from the robot controller.

- `codes: typing.List[int] (read only)`: Gets the codes (5 entries). Index 0 is the code of the active error, indexes 1 to 4 are the codes of the active alarms. A code of 0 means no error or no alarm.
- `data: typing.List[int] (read only)`: Gets the sub-codes (5 entries), at the same index as codes. Index 0 is the sub-code of the error, indexes 1 to 4 are the data of the alarms.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlAlarmEntry

`from underautomation.yaskawa.host_control.host_control_alarm_entry import HostControlAlarmEntry`

Represents a single alarm entry with code, sub-code and text description.

- `code: int (read only)`: Gets the alarm code number.
- `sub_code: int (read only)`: Gets the alarm sub-code (data).
- `message: str (read only)`: Gets the alarm text message.

## HostControlAlarmStringData

`from underautomation.yaskawa.host_control.host_control_alarm_string_data import HostControlAlarmStringData`

Contains alarm information with text messages retrieved from the robot controller.

- `alarm_count: int (read only)`: Gets the number of active alarms (entries of alarms with a code other than 0).
- `error: HostControlAlarmEntry (read only)`: Gets the active error. Its code is 0 when no error is active.
- `alarms: typing.List[HostControlAlarmEntry] (read only)`: Gets the alarm entries with codes and text messages (always 4 entries, the code of an unused entry is 0).
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlCartesianPositionData

`from underautomation.yaskawa.host_control.host_control_cartesian_position_data import HostControlCartesianPositionData`

Contains Cartesian position data (TCP position and orientation).

- `x: float (read only)`: Gets or sets the X position in millimeters.
- `y: float (read only)`: Gets or sets the Y position in millimeters.
- `z: float (read only)`: Gets or sets the Z position in millimeters.
- `rx: float (read only)`: Gets or sets the Rx (rotation around X axis) in degrees.
- `ry: float (read only)`: Gets or sets the Ry (rotation around Y axis) in degrees.
- `rz: float (read only)`: Gets or sets the Rz (rotation around Z axis) in degrees.
- `re: float (read only)`: Gets the elbow angle Re of a 7-axis robot, in degrees. On a 6-axis robot, value of the 7th axis (degrees or millimeters) when the external axes are read, 0 otherwise.
- `tool_number: int (read only)`: Gets the tool number (0 to 63) of the position.
- `axis8: float (read only)`: Gets or sets the 8th external axis value.
- `axis9: float (read only)`: Gets or sets the 9th external axis value.
- `axis10: float (read only)`: Gets or sets the 10th external axis value.
- `axis11: float (read only)`: Gets or sets the 11th external axis value.
- `axis12: float (read only)`: Gets or sets the 12th external axis value.
- `type: int (read only)`: Gets or sets the robot posture/configuration type. Defines arm configuration (flip, upper/lower arm, front/back, etc.). Use is_flip, is_upper_arm, is_front... to read it.
- `coordinate_system: int (read only)`: Gets or sets the coordinate system index. 0: Base, 1-65: User coordinates.
- `is_flip: bool (read only)`: Gets whether the robot is in flip configuration.
- `is_upper_arm: bool (read only)`: Gets whether the robot is in upper arm configuration.
- `is_front: bool (read only)`: Gets whether the robot is in front configuration.
- `is_r_less_than180: bool (read only)`: Gets whether R axis is less than 180 degrees.
- `is_t_less_than180: bool (read only)`: Gets whether T axis is less than 180 degrees.
- `is_s_less_than180: bool (read only)`: Gets whether S axis is less than 180 degrees.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlCoordinateSystem

`from underautomation.yaskawa.host_control.host_control_coordinate_system import HostControlCoordinateSystem`

Specifies the coordinate system for position commands.

- Base: Base coordinate system (robot base frame).
- Robot: Robot coordinate system.
- User1: User coordinate system 1.
- User2: User coordinate system 2.
- User3: User coordinate system 3.
- User4: User coordinate system 4.
- User5: User coordinate system 5.
- User6: User coordinate system 6.
- User7: User coordinate system 7.
- User8: User coordinate system 8.
- Tool: Tool coordinate system.

## HostControlCycleType

`from underautomation.yaskawa.host_control.host_control_cycle_type import HostControlCycleType`

Specifies the execution cycle type.

- Step: Step mode - execute one instruction at a time.
- OneCycle: One cycle mode - execute one complete cycle then stop.
- Automatic: Automatic mode - continuous operation.

## HostControlEncoderTemperatureData

`from underautomation.yaskawa.host_control.host_control_encoder_temperature_data import HostControlEncoderTemperatureData`

Contains encoder temperature values for each robot axis. Retrieved using the RENCTMP command.

- `values: typing.List[float] (read only)`: Gets the temperature values for each axis encoder (up to 12 axes). Values are in degrees Celsius.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlException

`from UnderAutomation.Yaskawa.HostControl import HostControlException`

Exception thrown when a Host Control command fails.

The SDK raises this .NET type: catch it with `except HostControlException as e` after the import above. Its members keep their .NET names. The class `HostControlException` of the module `underautomation.yaskawa.host_control.host_control_exception` is not a Python exception and cannot be caught.

- `ErrorCode: str (read only)`: Gets the error code returned by the robot controller.
- `Command: str (read only)`: Gets the command that caused the exception.
- Inherited from System.Exception: `Message`, `InnerException`

## HostControlGroupData

`from underautomation.yaskawa.host_control.host_control_group_data import HostControlGroupData`

Contains control group information. Retrieved using the RGROUP command.

- `robot_group: int (read only)`: Gets or sets the robot group bits. Each bit represents a robot control group (R1, R2, etc.).
- `station_group: int (read only)`: Gets or sets the station group bits. Each bit represents a station control group (S1, S2, etc.).
- `task: int (read only)`: Gets or sets the current task number. 0: Master task, 1-15: Sub tasks.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlIOData

`from underautomation.yaskawa.host_control.host_control_io_data import HostControlIOData`

Contains I/O signal data.

- `get_bit(bitOffset: int) -> bool`: Gets the bit value at the specified offset from the start address.
- `start_address: int (read only)`: Gets or sets the starting I/O contact number.
- `count: int (read only)`: Gets or sets the number of I/O bytes read.
- `data: typing.List[int] (read only)`: Gets or sets the I/O data bytes.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlJobData

`from underautomation.yaskawa.host_control.host_control_job_data import HostControlJobData`

Contains information about the currently executing job (program). Retrieved using the RJSEQ command.

- `name: str (read only)`: Gets or sets the name of the currently executing job.
- `line: int (read only)`: Gets or sets the current line number within the job (0-9999).
- `step: int (read only)`: Gets or sets the current step number within the job (1-9998).
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlJobDirectoryData

`from underautomation.yaskawa.host_control.host_control_job_directory_data import HostControlJobDirectoryData`

Contains job directory listing data. Retrieved using the RJDIR command.

- `job_names: typing.Any (read only)`: Gets or sets the list of job names in the directory.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlJointPositionData

`from underautomation.yaskawa.host_control.host_control_joint_position_data import HostControlJointPositionData`

Contains joint position data in pulse (encoder) values.

- `s: int (read only)`: Gets or sets the S axis position in pulses.
- `l: int (read only)`: Gets or sets the L axis position in pulses.
- `u: int (read only)`: Gets or sets the U axis position in pulses.
- `r: int (read only)`: Gets or sets the R axis position in pulses.
- `b: int (read only)`: Gets or sets the B axis position in pulses.
- `t: int (read only)`: Gets or sets the T axis position in pulses.
- `e: int (read only)`: Gets or sets the E axis (7th axis) position in pulses.
- `axis8: int (read only)`: Gets or sets the 8th axis position in pulses.
- `axis9: int (read only)`: Gets or sets the 9th axis position in pulses.
- `axis10: int (read only)`: Gets or sets the 10th axis position in pulses.
- `axis11: int (read only)`: Gets or sets the 11th axis position in pulses.
- `axis12: int (read only)`: Gets or sets the 12th axis position in pulses.
- `axes: typing.List[int] (read only)`: Gets all axis values as an array of encoder pulse values. Array contains 12 elements: S, L, U, R, B, T, E, Axis8 through Axis12.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlResponse

`from underautomation.yaskawa.host_control.host_control_response import HostControlResponse`

Base class for all robot data response objects returned by Host Control commands. Contains common response information about the communication.

- `response_code: str (read only)`: Gets or sets the raw response code from the robot controller. "0000" indicates normal completion.
- `command: str (read only)`: Gets or sets the command that was executed.
- `success: bool (read only)`: Gets a value indicating whether the command completed successfully.
- `error_message: str (read only)`: Gets or sets the error message if the command failed.

## HostControlResponseCode

`from underautomation.yaskawa.host_control.host_control_response_code import HostControlResponseCode`

Specifies the interpreter error/response codes.

- Success: Normal completion.
- ManipulatorMoving: Manipulator is moving.
- HoldByCommand: In hold state (command).
- HoldByExternal: In hold state (external).
- HoldByPendant: In hold state (pendant).
- HoldByOperationPanel: In hold state (operation panel).
- AlarmOrError: Alarm or error occurring.
- ServoOff: Servo OFF.
- IncorrectMode: Incorrect mode.
- NoCommandRemote: No command remote setting.

## HostControlRobotMode

`from underautomation.yaskawa.host_control.host_control_robot_mode import HostControlRobotMode`

Specifies the robot mode.

- Teach: Teach mode - robot can be manually positioned and jobs can be edited.
- Play: Play mode - robot can execute programmed jobs.

## HostControlSpeedType

`from underautomation.yaskawa.host_control.host_control_speed_type import HostControlSpeedType`

Specifies the speed type for motion commands.

- Percentage: Speed is specified as a percentage of maximum speed (V).
- MillimetersPerSecond: Speed is specified in mm/s (VE).

## HostControlStatusData

`from underautomation.yaskawa.host_control.host_control_status_data import HostControlStatusData`

Contains the current operational status of the robot controller. Provides information about the robot's mode, running state, and safety conditions.

- `step: bool (read only)`: Gets whether the robot is in step (single-step) execution mode. When true, the robot executes one instruction at a time.
- `cycle: bool (read only)`: Gets whether the robot is in cycle execution mode. When true, the robot executes one complete cycle then stops.
- `automatic: bool (read only)`: Gets whether the robot is in automatic operation mode. When true, the robot can operate automatically without pendant interaction.
- `running: bool (read only)`: Gets whether the robot is currently running (executing a job).
- `speed_limit: bool (read only)`: Gets whether speed limit is active.
- `teach: bool (read only)`: Gets whether the robot is in teach mode. In teach mode, the robot can be manually positioned and jobs can be edited.
- `play: bool (read only)`: Gets whether the robot is in play mode. In play mode, the robot can execute programmed jobs.
- `command_remote: bool (read only)`: Gets whether remote command mode is enabled. When true, the robot accepts commands from external sources (including this API).
- `servo_on: bool (read only)`: Gets whether servo power is enabled. Servo must be ON for the robot to move.
- `error_occurring: bool (read only)`: Gets whether an error condition is occurring. Errors may prevent normal operation until resolved.
- `alarming: bool (read only)`: Gets whether an alarm is currently active. Check GetAlarm() for detailed alarm information.
- `in_hold_status_by_command: bool (read only)`: Gets whether the robot is held by a command (software hold). A hold command was issued via the API or job instruction.
- `in_hold_status_externally: bool (read only)`: Gets whether the robot is held by an external hold signal. External safety circuit has triggered a hold condition.
- `in_hold_status_pendant: bool (read only)`: Gets whether the robot is held by the programming pendant. Operator has pressed hold on the pendant.
- `raw_data1: int (read only)`: Gets the first raw status word from the controller response.
- `raw_data2: int (read only)`: Gets the second raw status word from the controller response.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlSystemTimeData

`from underautomation.yaskawa.host_control.host_control_system_time_data import HostControlSystemTimeData`

Contains system time information from the robot controller. Retrieved using the RSYSTM command.

- `year: str (read only)`: Gets the year.
- `month_day: str (read only)`: Gets the month and day (MM/DD format).
- `hour_minute: str (read only)`: Gets the hour and minute (HH:MM format).
- `second: str (read only)`: Gets the second.
- `day_of_week: str (read only)`: Gets the day of the week.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlTorqueData

`from underautomation.yaskawa.host_control.host_control_torque_data import HostControlTorqueData`

Contains torque values for each robot axis. Retrieved using the RTRQ (current torque) or RMAXTRQ (maximum torque) commands.

- `values: typing.List[float] (read only)`: Gets the torque values for each axis (up to 12 axes). Values are in percentage of maximum rated torque.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlUserFrameData

`from underautomation.yaskawa.host_control.host_control_user_frame_data import HostControlUserFrameData`

Contains user coordinate frame data defined by three reference points (ORG, XX, XY). Retrieved using the RUFRAME command, written using the WUFRAME command.

- `user_coordinate_number: int (read only)`: Gets or sets the user coordinate number (2-64).
- `org_x: float (read only)`: ORG X coordinate value in mm.
- `org_y: float (read only)`: ORG Y coordinate value in mm.
- `org_z: float (read only)`: ORG Z coordinate value in mm.
- `org_tx: float (read only)`: ORG wrist angle TX in degrees.
- `org_ty: float (read only)`: ORG wrist angle TY in degrees.
- `org_tz: float (read only)`: ORG wrist angle TZ in degrees.
- `org_type: int (read only)`: ORG posture type.
- `xx_x: float (read only)`: XX X coordinate value in mm.
- `xx_y: float (read only)`: XX Y coordinate value in mm.
- `xx_z: float (read only)`: XX Z coordinate value in mm.
- `xx_tx: float (read only)`: XX wrist angle TX in degrees.
- `xx_ty: float (read only)`: XX wrist angle TY in degrees.
- `xx_tz: float (read only)`: XX wrist angle TZ in degrees.
- `xx_type: int (read only)`: XX posture type.
- `xy_x: float (read only)`: XY X coordinate value in mm.
- `xy_y: float (read only)`: XY Y coordinate value in mm.
- `xy_z: float (read only)`: XY Z coordinate value in mm.
- `xy_tx: float (read only)`: XY wrist angle TX in degrees.
- `xy_ty: float (read only)`: XY wrist angle TY in degrees.
- `xy_tz: float (read only)`: XY wrist angle TZ in degrees.
- `xy_type: int (read only)`: XY posture type.
- `tool_number: int (read only)`: Tool number (0-63).
- `axis7: int (read only)`: 7th axis pulses (for travel axis, mm).
- `axis8: int (read only)`: 8th axis pulses (for travel axis, mm).
- `axis9: int (read only)`: 9th axis pulses (for travel axis, mm).
- `axis10: int (read only)`: 10th axis pulses.
- `axis11: int (read only)`: 11th axis pulses.
- `axis12: int (read only)`: 12th axis pulses.
- Inherited from [HostControlResponse](underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## HostControlVariableType

`from underautomation.yaskawa.host_control.host_control_variable_type import HostControlVariableType`

Specifies the type of variable to read or write.

- Byte: Byte variable (B).
- Integer: Integer variable (I).
- DoubleInteger: Double integer variable (D).
- Real: Real (floating point) variable (R).
- Position: Robot axis position variable (P).
- BasePosition: Base axis position variable (BP).
- ExternalPosition: Station axis position variable (EX), pulse type only.
- String: String variable (S).
