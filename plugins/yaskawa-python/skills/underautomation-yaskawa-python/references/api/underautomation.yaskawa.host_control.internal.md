# underautomation.yaskawa.host_control.internal

## EServerClientInternal (robot.e_server)

`from underautomation.yaskawa.host_control.internal.e_server_client_internal import EServerClientInternal`

Internal implementation of the Host Control client for Ethernet Server (TCP) communication. Supports YRC1000 and compatible controllers.

- `close() -> None`: Marks the client as disconnected and releases any stored state.
- `connected: bool (read only)`: Gets a value indicating whether the client is ready to communicate with the robot. Since each command opens its own TCP connection, this reflects whether Connect has been called.
- `address: str (read only)`
- `port: int (read only)`: Gets the TCP port number.
- Inherited from [HostControlClientBase](underautomation.yaskawa.host_control.internal.md#hostcontrolclientbase-robote_server): `get_alarm`, `get_status_information`, `get_executing_job_information`, `get_control_group`, `get_robot_joint_position`, `get_robot_cartesian_position`, `set_hold`, `alarm_reset`, `error_cancel`, `set_mode`, `set_cycle`, `set_servo`, `set_teach_pendant_lock_state`, `display`, `start_job`, `set_control_group`, `set_task`, `move_joint`, `move_linear`, `move_incremental`, `move_pulse_joint`, `move_pulse_linear`, `read_io`, `write_io`, `read_byte`, `write_byte`, `read_integer`, `write_integer`, `read_double_integer`, `write_double_integer`, `read_real`, `write_real`, `read16_bytes_char`, `write16_bytes_char`, `get_job_directory`, `get_user_frame`, `set_user_frame`, `delete_job`, `set_master_job`, `select_job`, `wait_for_job_completion`, `convert_to_relative_job`, `convert_to_standard_job`, `get_torque`, `get_max_torque`, `get_encoder_temperature`, `get_system_time`, `get_absolute_encoder_position`, `set_absolute_encoder_position`, `set_frame_type`, `get_alarm_with_messages`

## EServerConnectParametersInternal

`from underautomation.yaskawa.host_control.internal.e_server_connect_parameters_internal import EServerConnectParametersInternal`

Connection parameters for Host Control Ethernet Server (TCP) communication. Use this class to configure network settings for TCP connection to YRC1000 and compatible controllers.

- `EServerConnectParametersInternal()`
- `enable: bool`: Gets or sets a value indicating whether to enable the Ethernet Server connection (default: false).
- Inherited from [EServerConnectParameters](underautomation.yaskawa.host_control.md#eserverconnectparameters): `DEFAULT_PORT`, `port`
- Inherited from [HostControlConnectParametersBase](underautomation.yaskawa.host_control.internal.md#hostcontrolconnectparametersbase): `DEFAULT_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_MOTION_TIMEOUT_MILLISECONDS`, `timeout_milliseconds`, `power_on_timeout_milliseconds`, `motion_timeout_milliseconds`

## HostControlClientBase (robot.e_server)

`from underautomation.yaskawa.host_control.internal.host_control_client_base import HostControlClientBase`

Base class implementing the Host Control protocol for Yaskawa robot communication. Provides methods for reading robot status, positions, variables, and executing commands.

- `close() -> None`: Closes the connection to the robot controller and releases resources.
- `get_alarm() -> HostControlAlarmData`: Reads the codes of the active error and alarms from the robot controller. Index 0 of the arrays is the error, indexes 1 to 4 are the alarms.
- `get_status_information() -> HostControlStatusData`: Reads the current operational status of the robot controller. Returns information about mode (teach/play), running state, hold status, alarms, and servo power.
- `get_executing_job_information() -> HostControlJobData`: Reads information about the currently selected and executing job (program). Returns job name, current line, and step.
- `get_control_group() -> HostControlGroupData`: Reads the current control group configuration. Returns robot group bits, station group bits, and current task number.
- `get_robot_joint_position() -> HostControlJointPositionData`: Reads the current robot joint position in pulse (encoder) values. Returns raw pulse values for all robot axes (S, L, U, R, B, T, and external axes).
- `get_robot_cartesian_position(coordinateSystem: HostControlCoordinateSystem=HostControlCoordinateSystem.Base, includeExternalAxes: bool=False) -> HostControlCartesianPositionData`: Reads the current robot Cartesian position (TCP position and orientation). Coordinates are returned in millimeters for X, Y, Z and degrees for Rx, Ry, Rz.
- `set_hold(enable: bool) -> HostControlResponse`: Sets the hold state of the robot. When hold is ON, robot motion is paused. When OFF, motion can resume.
- `alarm_reset() -> HostControlResponse`: Resets the current alarm condition. The cause of the alarm must be resolved before reset will succeed. Command remote must be enabled on the controller.
- `error_cancel() -> HostControlResponse`: Cancels the current error condition. Used for recoverable errors that don't require full alarm reset.
- `set_mode(mode: RobotMode) -> HostControlResponse`: Sets the robot operation mode (Teach or Play).
- `set_cycle(cycle: RobotCycleType) -> HostControlResponse`: Sets the execution cycle type (Step, One Cycle, or Automatic).
- `set_servo(enable: bool) -> HostControlResponse`: Enables or disables servo power. Servo must be ON for the robot to move. Uses extended timeout for power-on.
- `set_teach_pendant_lock_state(locked: bool) -> HostControlResponse`: Locks or unlocks the operations from the teach pendant and from the I/O operation signals. The emergency stop of the teach pendant stays active. Command remote must be enabled on the controller.
- `display(message: str) -> HostControlResponse`: Displays a message on the remote display of the teach pendant. Command remote must be enabled on the controller.
- `start_job(jobName: str=None) -> HostControlResponse`: Starts job execution. Starts the currently selected job, or starts a specific job if specified.
- `set_control_group(robotGroup: int, stationGroup: int) -> HostControlResponse`: Changes the control group selection.
- `set_task(task: int) -> HostControlResponse`: Changes the current task selection.
- `move_joint(speedPercent: int, coordinateSystem: HostControlCoordinateSystem, x: float, y: float, z: float, rx: float, ry: float, rz: float, type: int=0, toolNumber: int=0) -> HostControlResponse`: Moves the robot to a Cartesian position using joint interpolation. Joint motion is faster but the path is not linear.
- `move_linear(speedType: HostControlSpeedType, speed: float, coordinateSystem: HostControlCoordinateSystem, x: float, y: float, z: float, rx: float, ry: float, rz: float, type: int=0, toolNumber: int=0) -> HostControlResponse`: Moves the robot to a Cartesian position using linear interpolation. Linear motion follows a straight line path.
- `move_incremental(speedType: HostControlSpeedType, speed: float, coordinateSystem: HostControlCoordinateSystem, dx: float, dy: float, dz: float, drx: float, dry: float, drz: float, toolNumber: int=0) -> HostControlResponse`: Moves the robot incrementally using linear interpolation. Movement is relative to the current position.
- `move_pulse_joint(speedPercent: int, s: int, l: int, u: int, r: int, b: int, t: int, toolNumber: int=0) -> HostControlResponse`: Moves the robot to a pulse position using joint interpolation.
- `move_pulse_linear(speedType: HostControlSpeedType, speed: float, s: int, l: int, u: int, r: int, b: int, t: int, toolNumber: int=0) -> HostControlResponse`: Moves the robot to a pulse position using linear interpolation.
- `read_io(startAddress: int, count: int) -> HostControlIOData`: Reads I/O signals from the robot controller. Each byte holds 8 signals.
- `write_io(startAddress: int, data: typing.List[int]) -> HostControlResponse`: Writes I/O signals to the robot controller. Each byte holds 8 signals. By default, the controller accepts only the network input signals (#27010 to #29567).
- `read_byte(firstIndex: int, count: int) -> typing.List[int]`: Reads byte (B) variables starting at the specified index.
- `write_byte(firstIndex: int, data: typing.List[int]) -> None`: Writes byte (B) variables starting at the specified index.
- `read_integer(firstIndex: int, count: int) -> typing.List[int]`: Reads integer (I) variables starting at the specified index.
- `write_integer(firstIndex: int, data: typing.List[int]) -> None`: Writes integer (I) variables starting at the specified index.
- `read_double_integer(firstIndex: int, count: int) -> typing.List[int]`: Reads double integer (D) variables starting at the specified index.
- `write_double_integer(firstIndex: int, data: typing.List[int]) -> None`: Writes double integer (D) variables starting at the specified index.
- `read_real(firstIndex: int, count: int) -> typing.List[float]`: Reads real (R) variables starting at the specified index.
- `write_real(firstIndex: int, data: typing.List[float]) -> None`: Writes real (R) variables starting at the specified index.
- `read16_bytes_char(firstIndex: int, count: int) -> typing.List[str]`: Reads 16-byte string (S) variables starting at the specified index.
- `write16_bytes_char(firstIndex: int, data: typing.List[str]) -> None`: Writes 16-byte string (S) variables starting at the specified index.
- `get_job_directory(jobNameFilter: str="*") -> HostControlJobDirectoryData`: Reads the job directory listing from the robot controller.
- `get_user_frame(userCoordinateNumber: int) -> HostControlUserFrameData`: Reads user coordinate frame data from the robot controller. Returns the three reference points (ORG, XX, XY) defining the user coordinate system.
- `set_user_frame(userCoordinateNumber: int, frame: HostControlUserFrameData) -> HostControlResponse`: Writes user coordinate frame data to the robot controller. Defines a user coordinate system using three reference points (ORG, XX, XY).
- `delete_job(jobName: str) -> HostControlResponse`: Deletes a specified job from the robot controller.
- `set_master_job(jobName: str) -> HostControlResponse`: Sets a specified job as the master job and execution job.
- `select_job(jobName: str, line: int) -> HostControlResponse`: Sets the job name and line number for execution.
- `wait_for_job_completion(timeoutSeconds: int=-1) -> bool`: Waits for the current job to complete or the specified timeout to elapse. No response is sent until the job completes or the timeout expires.
- `convert_to_relative_job(jobName: str, coordinateSystem: HostControlCoordinateSystem) -> HostControlResponse`: Converts a specified job to a relative job of a specified coordinate system. Requires the relative job function on the robot controller.
- `convert_to_standard_job(jobName: str, convertingMethod: int, referencePositionVariable: int) -> HostControlResponse`: Converts a specified job to a standard job (pulse job). Requires the relative job function on the robot controller.
- `get_torque() -> HostControlTorqueData`: Reads the current torque values of all robot axes. Returns values as a percentage of the maximum rated torque.
- `get_max_torque() -> HostControlTorqueData`: Reads the maximum torque values of all robot axes. Returns values as a percentage of the maximum rated torque.
- `get_encoder_temperature() -> HostControlEncoderTemperatureData`: Reads the encoder temperature values of all robot axes.
- `get_system_time() -> HostControlSystemTimeData`: Reads the system time from the robot controller.
- `get_absolute_encoder_position(axisNumber: int) -> int`: Reads the absolute encoder position of a specific axis.
- `set_absolute_encoder_position(axisNumber: int, value: int) -> HostControlResponse`: Writes the absolute encoder data for a specific axis.
- `set_frame_type(frameType: int) -> HostControlResponse`: Sets the coordinate frame type used for position display on the pendant.
- `get_alarm_with_messages() -> HostControlAlarmStringData`: Reads the active error and alarms with their text messages from the robot controller. Returns the error and up to 4 alarms, each with its code, sub-code and message.
- `address: str (read only)`: Gets the address of the connected robot controller (IP address).
- `connected: bool (read only)`: Gets a value indicating whether the client is connected to a robot controller.

## HostControlConnectParametersBase

`from underautomation.yaskawa.host_control.internal.host_control_connect_parameters_base import HostControlConnectParametersBase`

Base class defining connection parameters for the Host Control communication. This class cannot be instantiated directly; use EServerConnectParameters instead.

- `timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for a response to commands. Default: 5000ms.
- `power_on_timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for servo power on to complete. Servo power on may take longer due to brake release and motor initialization. Default: 10000ms.
- `motion_timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for motion commands to complete. Motion commands may take longer depending on the distance to travel. Default: 30000ms.
- `static DEFAULT_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for commands (5000ms).
- `static DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for servo power on operations (10000ms).
- `static DEFAULT_MOTION_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for motion commands (30000ms).
