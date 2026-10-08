# underautomation.yaskawa.common

## AlarmEntry

`from underautomation.yaskawa.common.alarm_entry import AlarmEntry`

Default implementation of IAlarmEntry.

- `AlarmEntry()`
- `code: int (read only)`
- `sub_code: int (read only)`
- `message: str (read only)`
- `occurring_time: str (read only)`

## CartesianPosition

`from underautomation.yaskawa.common.cartesian_position import CartesianPosition`

Cartesian position of the robot flange in the robot frame.

- `CartesianPosition(x: float, y: float, z: float, rx: float, ry: float, rz: float)`: Initializes a new instance of CartesianPosition with the specified values.
- `to_homogeneous_matrix() -> typing.List[float]`: Returns the 4x4 homogeneous matrix of this position (rotation and translation in mm).
- `static from_homogeneous_matrix(matrix: typing.List[float]) -> 'CartesianPosition'`: Creates a Cartesian position from a homogeneous matrix (3x4 or 4x4, translation in mm). When Ry is +90 or -90 degrees, Rx and Rz are not unique: Rz is set to 0.
- `x: float`: X position in millimeters.
- `y: float`: Y position in millimeters.
- `z: float`: Z position in millimeters.
- `rx: float`: Rotation around the X axis in degrees.
- `ry: float`: Rotation around the Y axis in degrees.
- `rz: float`: Rotation around the Z axis in degrees.

## ConnectException

`from UnderAutomation.Yaskawa.Common import ConnectException`

Exception thrown when connection to a Yaskawa robot fails

The SDK raises this .NET type: catch it with `except ConnectException as e` after the import above. Its members keep their .NET names. The class `ConnectException` of the module `underautomation.yaskawa.common.connect_exception` is not a Python exception and cannot be caught.

- `Service: str (read only)`: Name of the protocol that failed to connect
- `Address: str (read only)`: Address of the robot (IP:port)
- Inherited from System.Exception: `Message`, `InnerException`

## DhParameters

`from underautomation.yaskawa.common.dh_parameters import DhParameters`

Denavit-Hartenberg parameters of a 6-axis Yaskawa arm (axes S, L, U, R, B, T).

- `DhParameters(a1: float, a2: float, a3: float, d4: float, d5: float, d6: float, theta2: float, theta3: float, theta5: float)`: Initializes a new instance of DhParameters with the specified values.
- `static from_arm_kinematic_model_name(modelName: str) -> 'DhParameters'`: Returns the DH parameters of a known robot model, from its name (for example "GP7" or "HC10DTP"). The comparison ignores case.
- `static from_arm_kinematic_model(model: ArmKinematicModels) -> 'DhParameters'`: Returns the DH parameters of a known robot model.
- `static from_prm_file(path: str) -> 'DhParameters'`: Reads the DH parameters of robot group 1 from an ALL.PRM parameter file saved from a controller. DX100, DX200, FS100, YRC1000 and YRC1000micro files are supported.
- `static from_prm_content(content: str) -> 'DhParameters'`: Reads the DH parameters of robot group 1 from the text content of an ALL.PRM parameter file. DX100, DX200, FS100, YRC1000 and YRC1000micro files are supported.
- `a1: float`
- `a2: float`
- `a3: float`
- `d4: float`
- `d5: float`
- `d6: float`
- `theta2: float`
- `theta3: float`
- `theta5: float`
- `kinematics_category: KinematicsCategory (read only)`: Kinematic structure of the arm: Opw when d5 is 0, J5OffsetWrist otherwise.

## FileExtension

`from underautomation.yaskawa.common.file_extension import FileExtension`

Represents the file types available on a Yaskawa robot controller.

- JOB: Job files (.JBI)
- DAT: Data files (.DAT)
- CND: Condition files (.CND)
- SYS: System files (.SYS)
- PRM: Parameter files (.PRM)
- LST: List files (.LST)
- CSV: CSV files (.CSV)
- LOG: Log files (.LOG)
- TXT: Text files (.TXT)

## IAlarmEntry

`from underautomation.yaskawa.common.i_alarm_entry import IAlarmEntry`

Represents an active alarm on a Yaskawa robot controller.

- `code: int (read only)`: Alarm code identifying the alarm type.
- `sub_code: int (read only)`: Alarm sub-code providing additional context.
- `message: str (read only)`: Human-readable alarm message text.
- `occurring_time: str (read only)`: Timestamp of alarm occurrence (format depends on protocol).

## IAlarmReader

`from underautomation.yaskawa.common.i_alarm_reader import IAlarmReader`

Provides access to active alarm information from the robot controller.

- `get_active_alarms() -> typing.List[IAlarmEntry]`: Reads the currently active alarms from the robot controller. Returns an array of active alarm entries. Empty array if no alarms are active.
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## ICartesianPosition

`from underautomation.yaskawa.common.i_cartesian_position import ICartesianPosition`

Represents a robot Cartesian position (TCP position and orientation).

- `x: float (read only)`: X position in millimeters.
- `y: float (read only)`: Y position in millimeters.
- `z: float (read only)`: Z position in millimeters.
- `rx: float (read only)`: Rotation around X axis in degrees.
- `ry: float (read only)`: Rotation around Y axis in degrees.
- `rz: float (read only)`: Rotation around Z axis in degrees.

## IDhParameters

`from underautomation.yaskawa.common.i_dh_parameters import IDhParameters`

Denavit-Hartenberg parameters of a 6-axis Yaskawa arm (axes S, L, U, R, B, T).

- `a1: float (read only)`: Offset between the S axis and the L axis, along the arm (mm).
- `a2: float (read only)`: Lower arm length, between the L axis and the U axis (mm).
- `a3: float (read only)`: Elbow offset, between the U axis and the forearm axis (mm).
- `d4: float (read only)`: Forearm length, between the U axis and the wrist (mm).
- `d5: float (read only)`: Wrist offset along the B axis (mm). Zero for a spherical wrist.
- `d6: float (read only)`: Distance between the wrist and the flange, along the T axis (mm).
- `theta2: float (read only)`: DH angle of the L axis when the L axis is at zero pulse (degrees).
- `theta3: float (read only)`: DH angle of the U axis when the U axis is at zero pulse (degrees).
- `theta5: float (read only)`: DH angle of the B axis when the B axis is at zero pulse (degrees).

## IFileManager

`from underautomation.yaskawa.common.i_file_manager import IFileManager`

Provides complete file management: read, write, list, and delete operations.

- Inherited from [IFileReader](underautomation.yaskawa.common.md#ifilereader): `get_file`, `get_file_list`
- Inherited from [IFileWriter](underautomation.yaskawa.common.md#ifilewriter): `load_file`, `delete_file`
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IFileReader

`from underautomation.yaskawa.common.i_file_reader import IFileReader`

Provides file read operations: download files and list directory contents.

- `get_file(fileName: str) -> str`: Downloads a file from the robot controller and returns its content as a string.
- `get_file_list(fileExtension_or_pattern: str | FileExtension) -> typing.List[str]`: Lists files matching a name pattern. Lists files matching the specified file extension.
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IFileWriter

`from underautomation.yaskawa.common.i_file_writer import IFileWriter`

Provides file write and delete operations on the robot controller.

- `load_file(fileName: str, content: str) -> None`: Uploads a file to the robot controller.
- `delete_file(fileName: str) -> None`: Deletes a file from the robot controller.
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IIOAccess

`from underautomation.yaskawa.common.iio_access import IIOAccess`

Provides read/write access to robot I/O signals.

- `read_io(startAddress: int, count: int) -> typing.List[int]`: Reads I/O signal bytes from the robot controller. Each byte holds a group of 8 signals.
- `write_io(startAddress: int, data: typing.List[int]) -> None`: Writes I/O signal bytes to the robot controller. Each byte holds a group of 8 signals.
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IJobData

`from underautomation.yaskawa.common.i_job_data import IJobData`

Represents information about the currently executing job on a Yaskawa robot controller.

- `name: str (read only)`: Name of the current job.
- `line: int (read only)`: Current line number being executed.
- `step: int (read only)`: Current step number being executed.

## IJointAngles

`from underautomation.yaskawa.common.i_joint_angles import IJointAngles`

Represents a joint position of a 6-axis arm in degrees, with the same signs as the pendant.

- `values: typing.List[float] (read only)`: Angles of axes S, L, U, R, B, T in degrees.

## IJointPulses

`from underautomation.yaskawa.common.i_joint_pulses import IJointPulses`

Represents a robot joint position in pulse (encoder) values.

- `axes: typing.List[int] (read only)`: Axis values in encoder pulses. Typically 8 to 12 elements depending on the robot configuration.

## IMotionControl

`from underautomation.yaskawa.common.i_motion_control import IMotionControl`

Provides motion commands to move the robot.

- `move_cartesian(x: float, y: float, z: float, rx: float, ry: float, rz: float, speed: float, tool: int=0) -> None`: Moves the robot to a Cartesian position.
- `move_joints(axesPulse: typing.List[int], speed: float, tool: int=0) -> None`: Moves the robot to a joint (pulse) position.
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IOType

`from underautomation.yaskawa.common.io_type import IOType`

Yaskawa Motoman I/O signal type categories.

- GeneralInput: Robot user input signals (#00010–)
- GeneralOutput: Robot user output signals (#10010–)
- ExternalInput: External input signals (#20010–)
- NetworkInput: Network input signals (#27010–)
- ExternalOutput: External output signals (#30010–)
- NetworkOutput: Network output signals (#37010–)
- SpecificInput: Robot system input signals (#40010–)
- SpecificOutput: Robot system output signals (#50010–)
- InterfacePanelInput: Interface panel input signals (#60010–)
- AuxiliaryRelay: Auxiliary relay signals (#70010–)
- RobotControlStatus: Robot control status signals (#80010–)
- PseudoInput: Pseudo input signals (#82010–)

## IPositionReader

`from underautomation.yaskawa.common.i_position_reader import IPositionReader`

Provides access to current robot position readings.

- `get_robot_joint_position() -> IJointPulses`: Reads the current robot joint position in pulse (encoder) values.
- `get_robot_cartesian_position() -> ICartesianPosition`: Reads the current robot Cartesian position (TCP position and orientation).
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IRobotClient

`from underautomation.yaskawa.common.i_robot_client import IRobotClient`

Super-interface that combines all robot control capabilities. Implemented by High Speed Ethernet Server and Host Control clients.

- Inherited from [IStatusReader](underautomation.yaskawa.common.md#istatusreader): `get_status_information`, `get_executing_job_information`
- Inherited from [IPositionReader](underautomation.yaskawa.common.md#ipositionreader): `get_robot_joint_position`, `get_robot_cartesian_position`
- Inherited from [IAlarmReader](underautomation.yaskawa.common.md#ialarmreader): `get_active_alarms`
- Inherited from [IRobotControl](underautomation.yaskawa.common.md#irobotcontrol): `alarm_reset`, `set_servo`, `set_hold`, `set_teach_pendant_lock_state`, `set_cycle`, `start_job`, `select_job`, `display`
- Inherited from [IIOAccess](underautomation.yaskawa.common.md#iioaccess): `read_io`, `write_io`
- Inherited from [IVariableAccess](underautomation.yaskawa.common.md#ivariableaccess): `read_byte`, `write_byte`, `read_integer`, `write_integer`, `read_double_integer`, `write_double_integer`, `read_real`, `write_real`, `read16_bytes_char`, `write16_bytes_char`
- Inherited from [ITorqueReader](underautomation.yaskawa.common.md#itorquereader): `get_torque`
- Inherited from [IMotionControl](underautomation.yaskawa.common.md#imotioncontrol): `move_cartesian`, `move_joints`
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IRobotControl

`from underautomation.yaskawa.common.i_robot_control import IRobotControl`

Provides robot control commands: alarm reset, servo, hold, cycle, job and display.

- `alarm_reset() -> None`: Resets the current alarm condition.
- `set_servo(enable: bool) -> None`: Enables or disables servo power. Servo must be ON for the robot to move.
- `set_hold(enable: bool) -> None`: Sets the hold state of the robot. When hold is ON, robot motion is paused.
- `set_teach_pendant_lock_state(locked: bool) -> None`: Locks or unlocks the teach pendant.
- `set_cycle(cycle: RobotCycleType) -> None`: Sets the execution cycle type (Step, One Cycle, or Automatic).
- `start_job() -> None`: Starts execution of the currently selected job.
- `select_job(jobName: str, line: int) -> None`: Selects a job for execution and positions to a specific line.
- `display(message: str) -> None`: Displays a popup message on the robot programming pendant.
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IStatusData

`from underautomation.yaskawa.common.i_status_data import IStatusData`

Represents the operational status of a Yaskawa robot controller. Common status flags shared across all communication protocols.

- `step: bool (read only)`: Step execution mode active.
- `cycle: bool (read only)`: Cycle execution mode active.
- `automatic: bool (read only)`: Automatic operation mode active.
- `running: bool (read only)`: Currently executing a job.
- `teach: bool (read only)`: Manual teach mode active.
- `play: bool (read only)`: Program playback mode active.
- `command_remote: bool (read only)`: Remote command mode enabled.
- `servo_on: bool (read only)`: Servo power is on.
- `error_occurring: bool (read only)`: An error condition is occurring.
- `alarming: bool (read only)`: An alarm is active.
- `in_hold_status_by_command: bool (read only)`: Hold state triggered by software command.
- `in_hold_status_externally: bool (read only)`: Hold state triggered by external signal.
- `in_hold_status_pendant: bool (read only)`: Hold state triggered by teach pendant.

## IStatusReader

`from underautomation.yaskawa.common.i_status_reader import IStatusReader`

Provides access to robot status and executing job information.

- `get_status_information() -> IStatusData`: Reads the current operational status of the robot controller.
- `get_executing_job_information() -> IJobData`: Reads the currently executing job information.
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## ITorqueReader

`from underautomation.yaskawa.common.i_torque_reader import ITorqueReader`

Provides access to robot axis torque readings.

- `get_torque() -> typing.List[float]`: Reads the current torque values of all robot axes as a percentage of the maximum rated torque.
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IVariableAccess

`from underautomation.yaskawa.common.i_variable_access import IVariableAccess`

Provides typed read/write access to robot controller variables.

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
- Inherited from [IYaskawaClient](underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## IYaskawaClient

`from underautomation.yaskawa.common.i_yaskawa_client import IYaskawaClient`

Base interface for all Yaskawa robot communication clients. Provides connection management shared across all communication protocols.

- `close() -> None`: Closes the connection to the robot controller and releases resources.
- `address: str (read only)`: Gets the address of the robot controller: an IP address or a host name.
- `connected: bool (read only)`: Gets a value indicating whether the client is connected to a robot controller.

## IoHelpers

`from underautomation.yaskawa.common.io_helpers import IoHelpers`

Helper methods for handling Yaskawa I/O group conversions and related utilities.

- `static convert_io_group_to_bit_address(type: IOType, group: int, bitIndex: int) -> int`: Converts an I/O group address (type + group + bit) to a flat Yaskawa 5-digit contact number.

## JointsAngles

`from underautomation.yaskawa.common.joints_angles import JointsAngles`

Joint angles of a 6-axis arm, in degrees, with the same signs as the pendant (axes S, L, U, R, B, T).

- `JointsAngles(s: float, l: float, u: float, r: float, b: float, t: float)`: Initializes a new instance of JointsAngles with the specified angles (degrees).
- `values: typing.List[float] (read only)`: Angles of axes S, L, U, R, B, T in degrees.
- `s: float`: S axis angle (degrees).
- `l: float`: L axis angle (degrees).
- `u: float`: U axis angle (degrees).
- `r: float`: R axis angle (degrees).
- `b: float`: B axis angle (degrees).
- `t: float`: T axis angle (degrees).

## KinematicsCategory

`from underautomation.yaskawa.common.kinematics_category import KinematicsCategory`

Kinematic structure of a 6-axis arm. It decides which inverse kinematics solver is used.

- Opw: Ortho-parallel base with a spherical wrist: the R, B and T axes meet at one point (D5 = 0). Most industrial arms (GP, MH, ES, HC20DT, HC30PL...). Up to 8 inverse kinematics solutions.
- J5OffsetWrist: Ortho-parallel base with a wrist offset along the B axis (D5 is not 0): the R and T axes do not meet. Collaborative robots such as HC10, HC10DT, HC20SDT. Up to 16 inverse kinematics solutions.

## RobotCycleType

`from underautomation.yaskawa.common.robot_cycle_type import RobotCycleType`

Specifies the execution cycle type.

- Step: Step mode : execute one instruction at a time.
- OneCycle: One cycle mode : execute one complete cycle then stop.
- Automatic: Automatic mode : continuous operation.

## RobotMode

`from underautomation.yaskawa.common.robot_mode import RobotMode`

Specifies the robot operation mode.

- Teach: Teach mode : robot can be manually positioned and jobs can be edited.
- Play: Play mode : robot can execute programmed jobs.
