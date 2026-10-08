# underautomation.fanuc.common

## ArmFrontBack (robot.stream_motion.queue_end_cartesian_position.configuration.arm_front_back)

`from underautomation.fanuc.common.arm_front_back import ArmFrontBack`

Arm configuration

- Unknown: Unknown
- Front: Front : T
- Back: Back : B

## ArmLeftRight (robot.stream_motion.queue_end_cartesian_position.configuration.arm_left_right)

`from underautomation.fanuc.common.arm_left_right import ArmLeftRight`

Arm left right

- Unknown: Unknown
- Left: Left : L
- Right: Right : R

## ArmUpDown (robot.stream_motion.queue_end_cartesian_position.configuration.arm_up_down)

`from underautomation.fanuc.common.arm_up_down import ArmUpDown`

Arm configuration

- Unknown: Unknown
- Up: Up : U
- Down: Down : D

## CartesianPosition (robot.stream_motion.queue_end_cartesian_position)

`from underautomation.fanuc.common.cartesian_position import CartesianPosition`

Fanuc cartesian position and rotations

- `CartesianPosition(x: float, y: float, z: float, w: float, p: float, r: float, configuration: Configuration)`: Constructor with position, rotations and configuration
- `static from_homogeneous_matrix(R: typing.List[float]) -> 'CartesianPosition'`: Create a CartesianPosition with unknow configuration from a homogeneous rotation and translation 4x4 matrix
- `static normalize_angle(angle: float) -> float`: Normalize an angle to the range ]-180, 180]
- `static normalize_angles(pose: 'CartesianPosition') -> None`: Normalize the W, P, R angles to the range ]-180, 180]
- `static is_near(a: 'CartesianPosition', b: 'CartesianPosition', mmTolerance: float, degreesTolerance: float) -> bool`: Check if two Cartesian positions are near each other within specified tolerances
- `configuration: Configuration`: Position configuration
- Inherited from [XYZWPRPosition](underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position): `to_homogeneous_matrix`, `get_quaternion`, `set_quaternion`, `multiply`, `inverse`, `flange_to_tcp`, `tcp_to_flange`, `user_frame_to_world`, `world_to_user_frame`, `w`, `p`, `r`
- Inherited from [XYZPosition](underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`

## CartesianPositionVariable

`from underautomation.fanuc.common.cartesian_position_variable import CartesianPositionVariable`

Represents a Cartesian position variable parsed from a Fanuc variable file

- `CartesianPositionVariable(group: int, position: CartesianPosition)`: Creates a Cartesian position variable from Cartesian position values and a motion group number.
- `static parse(value: str) -> 'CartesianPositionVariable'`: Parses a Cartesian position from its string representation
- `group: int`: Motion group number
- Inherited from [CartesianPosition](underautomation.fanuc.common.md#cartesianposition-robotstream_motionqueue_end_cartesian_position): `from_homogeneous_matrix`, `normalize_angle`, `normalize_angles`, `is_near`, `configuration`
- Inherited from [XYZWPRPosition](underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position): `to_homogeneous_matrix`, `get_quaternion`, `set_quaternion`, `multiply`, `inverse`, `flange_to_tcp`, `tcp_to_flange`, `user_frame_to_world`, `world_to_user_frame`, `w`, `p`, `r`
- Inherited from [XYZPosition](underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`

## CartesianPositionWithTool

`from underautomation.fanuc.common.cartesian_position_with_tool import CartesianPositionWithTool`

A cartesian position with a tool ID

- `CartesianPositionWithTool(x: float, y: float, z: float, w: float, p: float, r: float, e1: float, e2: float, e3: float, tool: int)`: Constructor with position, rotations and tool ID
- `tool: int`: Tool ID
- Inherited from [ExtendedCartesianPosition](underautomation.fanuc.common.md#extendedcartesianposition-robotstream_motionqueue_end_cartesian_position): `e1`, `e2`, `e3`
- Inherited from [CartesianPosition](underautomation.fanuc.common.md#cartesianposition-robotstream_motionqueue_end_cartesian_position): `from_homogeneous_matrix`, `normalize_angle`, `normalize_angles`, `is_near`, `configuration`
- Inherited from [XYZWPRPosition](underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position): `to_homogeneous_matrix`, `get_quaternion`, `set_quaternion`, `multiply`, `inverse`, `flange_to_tcp`, `tcp_to_flange`, `user_frame_to_world`, `world_to_user_frame`, `w`, `p`, `r`
- Inherited from [XYZPosition](underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`

## CartesianPositionWithUserFrame

`from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame`

A cartesian tool position with a user frame ID

- `CartesianPositionWithUserFrame(x: float, y: float, z: float, w: float, p: float, r: float, tool: int, frame: int)`: Constructor with position, rotations, tool and frame IDs
- `frame: int`: Frame ID in the controller
- Inherited from [CartesianPositionWithTool](underautomation.fanuc.common.md#cartesianpositionwithtool): `tool`
- Inherited from [ExtendedCartesianPosition](underautomation.fanuc.common.md#extendedcartesianposition-robotstream_motionqueue_end_cartesian_position): `e1`, `e2`, `e3`
- Inherited from [CartesianPosition](underautomation.fanuc.common.md#cartesianposition-robotstream_motionqueue_end_cartesian_position): `from_homogeneous_matrix`, `normalize_angle`, `normalize_angles`, `is_near`, `configuration`
- Inherited from [XYZWPRPosition](underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position): `to_homogeneous_matrix`, `get_quaternion`, `set_quaternion`, `multiply`, `inverse`, `flange_to_tcp`, `tcp_to_flange`, `user_frame_to_world`, `world_to_user_frame`, `w`, `p`, `r`
- Inherited from [XYZPosition](underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`

## CgtpConnectParameters

`from underautomation.fanuc.common.cgtp_connect_parameters import CgtpConnectParameters`

CGTP Web Server connection parameters

- `CgtpConnectParameters()`
- `enable: bool`: Should enable CGTP Web Server for this connection (default: true)
- Inherited from [CgtpConnectParametersBase](underautomation.fanuc.cgtp.internal.md#cgtpconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_REQUEST_TIMEOUT_MS`, `port`, `request_timeout_ms`, `login`, `password`

## Configuration (robot.stream_motion.queue_end_cartesian_position.configuration)

`from underautomation.fanuc.common.configuration import Configuration`

Fanuc arm configuration

- `Configuration(wristFlip: WristFlip, armUpDown: ArmUpDown, armLeftRight: ArmLeftRight, armFrontBack: ArmFrontBack, turnAxis1: int, turnAxis2: int, turnAxis3: int)`: Constructor with all configuration parameters
- `static parse(value: str) -> 'Configuration'`: Parse a Fanuc configuration from its string representation, like : "N U T, 0, 0, 0" or "R, 0, 0, 0"
- `from_string(value: str) -> None`: Parse a Fanuc configuration string representation, like : "N U T, 0, 0, 0" or "R, 0, 0, 0"
- `is_unknown: bool (read only)`: Indicates if the configuration is unknown
- `wrist_flip: WristFlip`: Wrist configuration
- `arm_up_down: ArmUpDown`: Arm up/down configuration
- `arm_left_right: ArmLeftRight`: Arm left/right configuration
- `arm_front_back: ArmFrontBack`: Arm back/front configuration
- `turn_axis4: int`: Turn number of axis J4 (1:180° to 539°, 0:-179° to 179°, -1:-539° to -180°)
- `turn_axis5: int`: Turn number of axis J5 (1:180° to 539°, 0:-179° to 179°, -1:-539° to -180°)
- `turn_axis6: int`: Turn number of axis J6 (1:180° to 539°, 0:-179° to 179°, -1:-539° to -180°)

## ConnectException

`from UnderAutomation.Fanuc.Common import ConnectException`

Exception thrown when connection to the robot fails

The SDK raises this .NET type: catch it with `except ConnectException as e` after the import above. Its members keep their .NET names. The class `ConnectException` of the module `underautomation.fanuc.common.connect_exception` is not a Python exception and cannot be caught.

- `Service: str (read only)`: Name of the service that failed to connect
- `RobotIp: str (read only)`: IP address of the robot
- Inherited from System.Exception: `Message`, `InnerException`

## DigitalPorts

`from underautomation.fanuc.common.digital_ports import DigitalPorts`

Fanuc digital port types

- DIN: Digital input
- DOUT: Digital outputs
- UI: User inputs
- UO: User outputs
- SI: SI
- SO: SO
- RI: Robot inputs
- RO: Robot outputs
- FLG: Flags

## ExtendedCartesianPosition (robot.stream_motion.queue_end_cartesian_position)

`from underautomation.fanuc.common.extended_cartesian_position import ExtendedCartesianPosition`

Cartesian position with extended axes (E1, E2, E3)

- `ExtendedCartesianPosition(x: float, y: float, z: float, w: float, p: float, r: float, e1: float, e2: float, e3: float)`: Constructor with position, rotations, and extended axes
- `e1: float`: Extended axis 1 value
- `e2: float`: Extended axis 2 value
- `e3: float`: Extended axis 3 value
- Inherited from [CartesianPosition](underautomation.fanuc.common.md#cartesianposition-robotstream_motionqueue_end_cartesian_position): `from_homogeneous_matrix`, `normalize_angle`, `normalize_angles`, `is_near`, `configuration`
- Inherited from [XYZWPRPosition](underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position): `to_homogeneous_matrix`, `get_quaternion`, `set_quaternion`, `multiply`, `inverse`, `flange_to_tcp`, `tcp_to_flange`, `user_frame_to_world`, `world_to_user_frame`, `w`, `p`, `r`
- Inherited from [XYZPosition](underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`

## FtpConnectParameters

`from underautomation.fanuc.common.ftp_connect_parameters import FtpConnectParameters`

Memory access parameters

- `FtpConnectParameters()`
- `enable: bool`: Should enable memory access for this connection (default: true)
- Inherited from [FtpConnectParametersBase](underautomation.fanuc.ftp.internal.md#ftpconnectparametersbase): `ftp_user`, `ftp_password`, `ftp_timeout_ms`

## IOComments

`from underautomation.fanuc.common.io_comments import IOComments`

Contains input and output comment arrays for an I/O type.

- `IOComments()`
- `inputs: typing.List[str]`: Array of input comments. Index 0 corresponds to Fanuc port 1.
- `outputs: typing.List[str]`: Array of output comments. Index 0 corresponds to Fanuc port 1.

## IOStatus

`from underautomation.fanuc.common.io_status import IOStatus`

A digital port status

- `IOStatus()`
- `port: DigitalPorts (read only)`: Digital port type
- `id: int (read only)`: Digital port ID
- `value: bool (read only)`: Digital port value
- `name: str (read only)`: IO Name

## JointPositionVariable

`from underautomation.fanuc.common.joint_position_variable import JointPositionVariable`

Represents a joint position variable parsed from a Fanuc variable file

- `JointPositionVariable(group: int, position: JointsPosition)`: Creates a joint position variable from a group number and joint position values.
- `static parse(value: str) -> 'JointPositionVariable'`: Parses a joint position from its string representation
- `group: int`: Motion group number
- Inherited from [JointsPosition](underautomation.fanuc.common.md#jointsposition-robotstream_motionqueue_end_joint_position): `is_near`, `values`, `j1`, `j2`, `j3`, `j4`, `j5`, `j6`, `j7`, `j8`, `j9`

## JointsPosition (robot.stream_motion.queue_end_joint_position)

`from underautomation.fanuc.common.joints_position import JointsPosition`

Joints position in degrees

- `JointsPosition(j1Deg: float, j2Deg: float, j3Deg: float, j4Deg: float, j5Deg: float, j6Deg: float, j7Deg: float, j8Deg: float, j9Deg: float)`: Constructor with 9 joint values in degrees
- `static is_near(j1: 'JointsPosition', j2: 'JointsPosition', degreesTolerance: float) -> bool`: Check if joints position is near to expected joints position with a tolerance value
- `values: typing.List[float] (read only)`: Numeric values for each joints
- `j1: float`: Joint 1 in degrees
- `j2: float`: Joint 2 in degrees
- `j3: float`: Joint 3 in degrees
- `j4: float`: Joint 4 in degrees
- `j5: float`: Joint 5 in degrees
- `j6: float`: Joint 6 in degrees
- `j7: float`: Joint 7 in degrees
- `j8: float`: Joint 8 in degrees
- `j9: float`: Joint 9 in degrees

## Languages (robot.cgtp.language)

`from underautomation.fanuc.common.languages import Languages`

Languages supported by the Fanuc robots

- English: For robots set to English language
- Japanese: For robots set to Japanese language
- Chinese: For robots set to Chinese language

## NumericRegister

`from underautomation.fanuc.common.numeric_register import NumericRegister`

Represents a numeric register value that can be either integer or real.

- `NumericRegister(value: int)`: Creates a numeric register with an integer value.
- `is_integer: bool`: Indicates whether the register holds an integer value (true) or a real value (false)
- `integer_value: int`: Gets or sets the value as an integer. Internally stored as a double.
- `real_value: float`: Gets or sets the value as a double-precision floating-point number.

## NumericRegisterWithComment

`from underautomation.fanuc.common.numeric_register_with_comment import NumericRegisterWithComment`

Represents a numeric register with an associated comment.

- `NumericRegisterWithComment(value: int, comment: str)`: Creates a numeric register with an integer value and comment.
- `comment: str`: Comment associated with this register.
- Inherited from [NumericRegister](underautomation.fanuc.common.md#numericregister): `is_integer`, `integer_value`, `real_value`

## Position

`from underautomation.fanuc.common.position import Position`

Robot position with joints and cartesian representations

- `Position(userFrame: int, userTool: int, jointsPosition: JointsPosition, cartesianPosition: ExtendedCartesianPosition)`: Constructor with user frame, tool, joints and cartesian position
- `user_frame: int`: User frame index
- `user_tool: int`: User tool index
- `joints_position: JointsPosition`: Joint values in degrees
- `cartesian_position: ExtendedCartesianPosition`: Cartesian position with extended axes

## PositionRegister

`from underautomation.fanuc.common.position_register import PositionRegister`

Represents a position register that can hold either a Cartesian or joint position

- `PositionRegister(jointsPosition: JointPositionVariable, cartesianPosition: CartesianPositionVariable)`: Creates a position register from joint and Cartesian position values
- `static parse(value: str) -> 'PositionRegister'`: Parses a position register from its string representation
- `joints_position: JointPositionVariable`: Joint position value, if available
- `cartesian_position: CartesianPositionVariable`: Cartesian position value, if available

## PositionRegisterWithComment

`from underautomation.fanuc.common.position_register_with_comment import PositionRegisterWithComment`

Represents a position register with an associated comment.

- `PositionRegisterWithComment()`: Default constructor.
- `static parse(value: str) -> 'PositionRegisterWithComment'`: Parses a position register with comment from its string representation.
- `comment: str`: Comment associated with this position register.
- Inherited from [PositionRegister](underautomation.fanuc.common.md#positionregister): `joints_position`, `cartesian_position`

## ProgramType

`from underautomation.fanuc.common.program_type import ProgramType`

Represents the type of a program.

- Unknown: The program type is unknown.
- Karel: The program is a Karel program, also known as PC (Programmable Control).
- TP: The program is a TP (Teach Pendant) program.

## Quaternion

`from underautomation.fanuc.common.quaternion import Quaternion`

Quaternion that represents an orientation (Qw + Qx.i + Qy.j + Qz.k). Use get_quaternion() and set_quaternion() to convert from and to W, P, R angles.

- `Quaternion(qw: float, qx: float, qy: float, qz: float)`: Creates a quaternion from its components
- `normalize() -> 'Quaternion'`: Returns this quaternion with a norm of 1
- `conjugate() -> 'Quaternion'`: Returns the conjugate of this quaternion. For a rotation, it is the inverse rotation.
- `multiply(other: 'Quaternion') -> 'Quaternion'`: Returns the product this x other: the rotation other applied after the rotation this, in the frame of this.
- `dot(other: 'Quaternion') -> float`: Dot product of the two quaternions
- `angle_to(other: 'Quaternion') -> float`: Angle of the rotation between the two orientations, in degrees (0 to 180)
- `static slerp(start: 'Quaternion', end: 'Quaternion', t: float) -> 'Quaternion'`: Spherical linear interpolation between two orientations, on the shortest way
- `static from_axis_angle(x: float, y: float, z: float, angle: float) -> 'Quaternion'`: Creates a rotation around an axis
- `to_axis_angle() -> typing.List[float]`: Returns the rotation axis and angle: [x, y, z, angle in degrees]. The axis is a unit vector and the angle is between 0 and 180.
- `static from_rotation_matrix(matrix: typing.List[float]) -> 'Quaternion'`: Creates a quaternion from a rotation matrix (3x3, or 4x4 homogeneous matrix)
- `to_rotation_matrix() -> typing.List[float]`: Returns the 3x3 rotation matrix of this orientation
- `qw: float`: Scalar part
- `qx: float`: X component of the vector part
- `qy: float`: Y component of the vector part
- `qz: float`: Z component of the vector part
- `norm: float (read only)`: Norm of the quaternion (1 for a rotation)

## RmiConnectParameters

`from underautomation.fanuc.common.rmi_connect_parameters import RmiConnectParameters`

RMI parameters

- `RmiConnectParameters()`
- `enable: bool`: Should enable RMI for this connection (default: false)
- Inherited from [RmiConnectParametersBase](underautomation.fanuc.rmi.internal.md#rmiconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_READ_TIMEOUT_MS`, `port`, `read_timeout_ms`

## SnpxConnectParameters

`from underautomation.fanuc.common.snpx_connect_parameters import SnpxConnectParameters`

SNPX parameters

- `SnpxConnectParameters()`
- `enable: bool`: Should enable SNPX for this connection (default: false)
- Inherited from [SnpxConnectParametersBase](underautomation.fanuc.snpx.internal.md#snpxconnectparametersbase): `DEFAULT_PORT`, `port`

## StreamMotionConnectParameters

`from underautomation.fanuc.common.stream_motion_connect_parameters import StreamMotionConnectParameters`

Stream Motion connection parameters (J519 option)

- `StreamMotionConnectParameters()`
- `enable: bool`: Should enable Stream Motion for this connection (default: false)
- `ip: str`: IP address of the robot for standalone Stream Motion connections
- Inherited from [StreamMotionConnectParametersBase](underautomation.fanuc.stream_motion.internal.md#streammotionconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_PROTOCOL_VERSION`, `DEFAULT_BUFFER_LEAD_TIME`, `DEFAULT_PACKET_STACK_SIZE`, `DEFAULT_STATUS_TIMEOUT_MS`, `port`, `protocol_version`, `buffer_lead_time`, `packet_stack_size`, `status_timeout_ms`, `high_priority`

## StringRegisterWithComment

`from underautomation.fanuc.common.string_register_with_comment import StringRegisterWithComment`

Represents a string register with an associated comment.

- `StringRegisterWithComment()`
- `comment: str`: Comment associated with this register.
- `value: str`: String value of the register.

## StringUtils

`from underautomation.fanuc.common.string_utils import StringUtils`

Contains string related utility methods

## TaskStatus

`from underautomation.fanuc.common.task_status import TaskStatus`

Represents the status of a task.

- Unknown: The task status is unknown.
- Running: The task is running.
- Paused: The task is paused.
- Aborted: The task is aborted.

## TelnetConnectParameters

`from underautomation.fanuc.common.telnet_connect_parameters import TelnetConnectParameters`

Connect parameters for remote command

- `TelnetConnectParameters()`
- `enable: bool`: Should use this service (default: false)
- Inherited from [TelnetConnectParametersBase](underautomation.fanuc.telnet.internal.md#telnetconnectparametersbase): `telnet_kcl_password`

## UserAlarmDefinition

`from underautomation.fanuc.common.user_alarm_definition import UserAlarmDefinition`

Represents a user alarm definition with a comment and severity level.

- `UserAlarmDefinition()`
- `comment: str`: Comment associated with this alarm.
- `severity: int`: Severity level of the alarm.

## VectorVariable

`from underautomation.fanuc.common.vector_variable import VectorVariable`

Represents a 3D vector variable with X, Y, Z components

- `VectorVariable()`
- `static parse(value: str) -> 'VectorVariable'`: Parses a vector variable from its string representation
- `x: float`: X component of the vector
- `y: float`: Y component of the vector
- `z: float`: Z component of the vector

## WristFlip (robot.stream_motion.queue_end_cartesian_position.configuration.wrist_flip)

`from underautomation.fanuc.common.wrist_flip import WristFlip`

Wrist configuration

- Unknown: Unknown
- Flip: Flip : F
- NoFlip: No flip : N

## XYZPosition (robot.stream_motion.queue_end_cartesian_position)

`from underautomation.fanuc.common.xyz_position import XYZPosition`

Cartesian position X, Y, Z

- `XYZPosition(x: float, y: float, z: float)`: Constructor with X, Y, Z coordinates in millimeters
- `x: float`: X coordinate in millimeters
- `y: float`: Y coordinate in millimeters
- `z: float`: Z coordinate in millimeters

## XYZWPRPosition (robot.stream_motion.queue_end_cartesian_position)

`from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition`

Cartesian position X, Y, Z with W, P, R rotations

- `XYZWPRPosition(x: float, y: float, z: float, w: float, p: float, r: float)`: Constructor with position and rotations
- `to_homogeneous_matrix() -> typing.List[float]`: Convert position to a homogeneous rotation and translation 4x4 matrix
- `get_quaternion() -> Quaternion`: Returns the orientation W, P, R as a quaternion
- `set_quaternion(quaternion: Quaternion) -> None`: Sets the orientation W, P, R from a quaternion. Angles are between -180 and 180 degrees.
- `multiply(other: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Returns the composition of this frame with another one: the pose other, expressed in this frame, converted to the frame where this position is expressed.
- `inverse() -> 'XYZWPRPosition'`: Returns the inverse of this frame
- `flange_to_tcp(tool: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Converts a flange position to the position of the tool center point (TCP)
- `tcp_to_flange(tool: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Converts a position of the tool center point (TCP) to the flange position
- `user_frame_to_world(userFrame: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Converts this position, expressed in a user frame, to the world frame
- `world_to_user_frame(userFrame: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Converts this position, expressed in the world frame, to a user frame
- `w: float`: W rotation in degrees (Rx)
- `p: float`: P rotation in degrees (Ry)
- `r: float`: R rotation in degrees (Rz)
- Inherited from [XYZPosition](underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`
