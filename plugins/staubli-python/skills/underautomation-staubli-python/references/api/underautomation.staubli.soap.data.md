# underautomation.staubli.soap.data

## AboveBelowConfig

`from underautomation.staubli.soap.data.above_below_config import AboveBelowConfig`

Configuration for above/below joint orientation.

- Same: Keep the same configuration as the current one.
- Above: Above configuration.
- Below: Below configuration.
- Free: Free configuration (no constraint).

## AnthroConfig

`from underautomation.staubli.soap.data.anthro_config import AnthroConfig`

Configuration for an anthropomorphic robot (shoulder, elbow, wrist).

- `AnthroConfig()`: Initializes a new instance of the AnthroConfig class.
- `shoulder: ShoulderConfig`: Shoulder configuration.
- `elbow: PositiveNegativeConfig`: Elbow configuration.
- `wrist: PositiveNegativeConfig`: Wrist configuration.

## BlendType

`from underautomation.staubli.soap.data.blend_type import BlendType`

Blend mode used during motion transitions between segments.

- BlendOff: No blending; the robot stops at each target point.
- BlendJoint: Joint-space blending between motion segments.
- BlendCartesian: Cartesian-space blending between motion segments.

## CartesianJointPosition

`from underautomation.staubli.soap.data.cartesian_joint_position import CartesianJointPosition`

Represents the joint positions and the Cartesian position of a robot end effector.

- `CartesianJointPosition()`
- `joints_position: typing.List[float]`: The joint positions in radians.
- `cartesian_position: CartesianPosition`: The Cartesian position of the robot end effector.

## CartesianPosition

`from underautomation.staubli.soap.data.cartesian_position import CartesianPosition`

Represents a Cartesian position with X, Y, Z translation and Rx, Ry, Rz rotation components.

- `CartesianPosition()`: Initializes a new instance of the CartesianPosition class.
- `x: float`: X translation component (m).
- `y: float`: Y translation component (m).
- `z: float`: Z translation component (m).
- `rx: float`: Rotation around the X axis (radians).
- `ry: float`: Rotation around the Y axis (radians).
- `rz: float`: Rotation around the Z axis (radians).

## Config

`from underautomation.staubli.soap.data.config import Config`

Robot configuration containing kinematic-specific settings.

- `Config()`: Initializes a new instance of the Config class.
- `anthro_config: AnthroConfig`: Anthropomorphic robot configuration.
- `scara_config: ScaraConfig`: SCARA robot configuration.
- `vrbx_config: VrbxConfig`: VRBX robot configuration.

## ControllerTask

`from underautomation.staubli.soap.data.controller_task import ControllerTask`

Represents a task running on the controller.

- `ControllerTask()`: Initializes a new instance of the ControllerTask class.
- `name: str`: Name of the task.
- `state: ControllerTaskState`: Current execution state of the task.
- `priority: int`: Priority level of the task.
- `created_by: str`: Name of the entity that created the task.
- `runtime_error: int`: Runtime error code (0 if no error).
- `runtime_error_description: str`: Human-readable description of the runtime error.
- `program_line: ProgramLine`: Current program line being executed by the task.

## ControllerTaskState

`from underautomation.staubli.soap.data.controller_task_state import ControllerTaskState`

Execution state of a controller task.

- Idle: Task is idle and not executing.
- Transition: Task is transitioning between states.
- Running: Task is currently running.
- Stepping: Task is executing step by step.
- Stopped: Task is stopped.

## DhParameters

`from underautomation.staubli.soap.data.dh_parameters import DhParameters`

Denavit-Hartenberg parameters for a single robot joint.

- `DhParameters()`: Initializes a new instance of the DhParameters class.
- `theta: float`: Joint angle theta (radians).
- `d: float`: Link offset d (m).
- `a: float`: Link length a (m).
- `alpha: float`: Link twist alpha (radians).
- `beta: float`: Joint twist beta (radians).

## DiameterAxis3

`from underautomation.staubli.soap.data.diameter_axis3 import DiameterAxis3`

Diameter of the third axis of the robot.

- Invalid: Invalid or unknown diameter.
- D20: 20 mm diameter.
- D25: 25 mm diameter.

## Frame

`from underautomation.staubli.soap.data.frame import Frame`

Represents a 3D transformation composed of orientation (a 3x3 rotation matrix) and position (a translation vector) in space. Used to define the pose of a robot or tool in a 3D environment. Matrix representation: [ Nx Ox Ax Px ] [ Ny Oy Ay Py ] [ Nz Oz Az Pz ] [ 0 0 0 1 ]

- `Frame()`: Default constructor.
- `nx: float`: X component of the local X-axis vector (Normal X).
- `ny: float`: Y component of the local X-axis vector (Normal Y).
- `nz: float`: Z component of the local X-axis vector (Normal Z).
- `ox: float`: X component of the local Y-axis vector (Orientation X).
- `oy: float`: Y component of the local Y-axis vector (Orientation Y).
- `oz: float`: Z component of the local Y-axis vector (Orientation Z).
- `ax: float`: X component of the local Z-axis vector (Approach X).
- `ay: float`: Y component of the local Z-axis vector (Approach Y).
- `az: float`: Z component of the local Z-axis vector (Approach Z).
- `px: float`: X coordinate of the frame's origin in global space (Pose X).
- `py: float`: Y coordinate of the frame's origin in global space (Pose Y).
- `pz: float`: Z coordinate of the frame's origin in global space (Pose Z).

## IForwardKinematics

`from underautomation.staubli.soap.data.i_forward_kinematics import IForwardKinematics`

Represents the result of a forward kinematics computation.

- `position: Frame (read only)`: Cartesian position resulting from the forward kinematics computation.
- `config: Config (read only)`: Robot configuration associated with the computed position.

## IMoveResult

`from underautomation.staubli.soap.data.i_move_result import IMoveResult`

Represents the result of a robot motion command.

- `id: int (read only)`: Identifier of the motion command.
- `return_code: MotionReturnCode (read only)`: Return code indicating the outcome of the motion command.

## IReverseKinematics

`from underautomation.staubli.soap.data.i_reverse_kinematics import IReverseKinematics`

Represents the result of a reverse (inverse) kinematics computation.

- `joint: typing.List[float] (read only)`: Joint angles resulting from the reverse kinematics computation.
- `result: ReversingResult (read only)`: Result code indicating the outcome of the reverse kinematics computation.

## JointRange

`from underautomation.staubli.soap.data.joint_range import JointRange`

Minimum and maximum range of each robot joint (radians).

- `JointRange()`: Initializes a new instance of the JointRange class.
- `min: typing.List[float]`: Minimum values for each joint (radians).
- `max: typing.List[float]`: Maximum values for each joint (radians).

## Kinematic

`from underautomation.staubli.soap.data.kinematic import Kinematic`

Robot kinematic type.

- Invalid: Invalid or unknown kinematic type.
- Anthropomorph6: 6-axis anthropomorphic robot.
- Anthrioparallel6: 6-axis anthropomorphic parallel robot.
- Anthropomorph5: 5-axis anthropomorphic robot.
- Scara: SCARA robot.
- Eisenmann: Eisenmann kinematic type.

## LengthAxis3

`from underautomation.staubli.soap.data.length_axis3 import LengthAxis3`

Length of the third axis of the robot.

- Invalid: Invalid or unknown length.
- L100: 100 mm length.
- L200: 200 mm length.
- L400: 400 mm length.
- L600: 600 mm length.

## MotionDesc

`from underautomation.staubli.soap.data.motion_desc import MotionDesc`

Describes the parameters of a robot motion, including tool, frame, velocity, acceleration, blending and configuration.

- `MotionDesc()`: Initializes a new instance of the MotionDesc class.
- `tool: Frame`: Defines the pose of the robot's tool center point (TCP) in flange, including both position and orientation.
- `frame: Frame`: Defines the frame in which the tool position is located, including both position and orientation.
- `abs_rel: MoveType`: Specifies whether the motion is defined in absolute or relative terms.
- `config: Config`: Contains additional configuration parameters specific to the robot type, such as anthropomorphic, SCARA, or VRBX configurations.
- `blend_type: BlendType`: Specifies the type of blending to be applied when transitioning between motion segments.
- `distance_blend_previous: float`: In the joint and Cartesian blending modes, the distance between the target point where blending begins and the next point, in millimeters or inches, depending on the length unit used in the application.
- `distance_blend_next: float`: In joint and Cartesian blending modes, the distance between the target point where blending ends and the next point, in millimeters or inches, depending on the length unit of the application.
- `velocity: float`: Maximum allowable joint speed, as a percentage of the robot's nominal speed.
- `acceleration: float`: Maximum allowed joint acceleration, as a percentage of the robot's nominal acceleration.
- `deceleration: float`: Maximum allowed joint deceleration, as a percentage of the robot's nominal deceleration.
- `translation_velocity: float`: Maximum allowed feed rate of the tool center, in mm/s or inches/s depending on the length unit of the application.
- `rotation_velocity: float`: Maximum permitted tool rotation speed, in degrees per second.
- `frequency: float`: Frequency of motion in Hz.

## MotionReturnCode

`from underautomation.staubli.soap.data.motion_return_code import MotionReturnCode`

Return code for robot motion commands.

- Success: Success, no error occurred.
- NotReady: The robot is not ready to execute motion.
- ParameterError: Invalid parameter provided to the motion command.
- MisuseError: Motion command misuse error.
- UnexpectedError: An unexpected error occurred during motion.

## MountType

`from underautomation.staubli.soap.data.mount_type import MountType`

Robot mounting type.

- Invalid: Invalid or unknown mount type.
- Floor: Robot is floor-mounted.
- Ceiling: Robot is ceiling-mounted.
- Wall: Robot is wall-mounted.

## MoveType

`from underautomation.staubli.soap.data.move_type import MoveType`

Specifies whether the motion is absolute or relative.

- Absolute: Absolute motion in the reference frame.
- Relative: Relative motion from the current position.

## Parameter

`from underautomation.staubli.soap.data.parameter import Parameter`

Key-value parameter from the controller.

- `Parameter()`: Initializes a new instance of the Parameter class.
- `key: str`: Parameter key identifier.
- `name: str`: Display name of the parameter.
- `value: str`: Value of the parameter.

## PhysicalAioAttribute

`from underautomation.staubli.soap.data.physical_aio_attribute import PhysicalAioAttribute`

Attributes for an analog I/O, including linear conversion coefficients.

- `PhysicalAioAttribute()`: Initializes a new instance of the PhysicalAioAttribute class.
- `coefficient_a: float`: Linear coefficient A (slope) for analog conversion.
- `coefficient_b: float`: Linear coefficient B (offset) for analog conversion.

## PhysicalDioAttribute

`from underautomation.staubli.soap.data.physical_dio_attribute import PhysicalDioAttribute`

Attributes for a digital I/O.

- `PhysicalDioAttribute()`: Initializes a new instance of the PhysicalDioAttribute class.
- `inverted: bool`: Indicates whether the digital I/O logic is inverted.

## PhysicalIo

`from underautomation.staubli.soap.data.physical_io import PhysicalIo`

Represents a physical I/O on the robot.

- `PhysicalIo()`
- `name: str`: Name of the physical I/O.
- `description: str`: Description of the physical I/O.
- `type_str: str`: Type of the physical I/O (e.g., din, dout, ain, serial, ...).
- `lockable: bool`: Indicates whether the physical I/O is lockable.

## PhysicalIoAttribute

`from underautomation.staubli.soap.data.physical_io_attribute import PhysicalIoAttribute`

Physical I/O attribute containing either analog or digital specific attributes.

- `PhysicalIoAttribute()`: Initializes a new instance of the PhysicalIoAttribute class.
- `aio_attribute: PhysicalAioAttribute`: Analog I/O specific attributes (null if digital).
- `dio_attribute: PhysicalDioAttribute`: Digital I/O specific attributes (null if analog).

## PhysicalIoEnumState

`from underautomation.staubli.soap.data.physical_io_enum_state import PhysicalIoEnumState`

Definition state of a physical I/O.

- Defined: The I/O is defined and available.
- Undefined: The I/O is not defined.
- InvalidName: The I/O name is invalid.

## PhysicalIoState

`from underautomation.staubli.soap.data.physical_io_state import PhysicalIoState`

Current state and value of a physical I/O.

- `PhysicalIoState()`: Initializes a new instance of the PhysicalIoState class.
- `state: PhysicalIoEnumState`: Definition state of the I/O.
- `locked: bool`: Indicates whether the I/O is locked.
- `simulated: bool`: Indicates whether the I/O is in simulation mode.
- `value: float`: Current numeric value of the I/O.
- `attribute: PhysicalIoAttribute`: I/O type-specific attributes (analog or digital).

## PhysicalIoWriteResponse

`from underautomation.staubli.soap.data.physical_io_write_response import PhysicalIoWriteResponse`

Result of a physical I/O write operation.

- `PhysicalIoWriteResponse()`: Initializes a new instance of the PhysicalIoWriteResponse class.
- `success: bool`: Indicates whether the write operation succeeded.
- `found: bool`: Indicates whether the specified I/O was found.

## PositiveNegativeConfig

`from underautomation.staubli.soap.data.positive_negative_config import PositiveNegativeConfig`

Positive/negative configuration for a robot joint.

- Same: Keep the same configuration as the current one.
- Positive: Positive configuration.
- Negative: Negative configuration.
- Free: Free configuration (no constraint).

## PowerReturnCode

`from underautomation.staubli.soap.data.power_return_code import PowerReturnCode`

Return code for robot power commands.

- Success: Success, no error occurred.
- RobotNotStopped: Cannot change power while the robot is not stopped.
- EnableTimeout: Timeout while enabling power.
- DisableTimeout: Timeout while disabling power.
- OnlyInRemoteMode: Power can only be changed in remote mode.

## ProgramLine

`from underautomation.staubli.soap.data.program_line import ProgramLine`

Represents a line of a VAL3 program being executed on the controller.

- `ProgramLine()`: Initializes a new instance of the ProgramLine class.
- `application_name: str`: Name of the application containing the program.
- `program_name: str`: Name of the program.
- `line_number: int`: Line number currently being executed.
- `line_content: str`: Content of the line being executed.

## ReversingResult

`from underautomation.staubli.soap.data.reversing_result import ReversingResult`

Result code for reverse kinematics computation.

- Success: Reverse kinematics succeeded.
- NoConvergence: The algorithm did not converge to a solution.
- JointOutOfRange: The computed joint position is out of range.
- OutOfWorkspace: The target is outside the robot workspace.
- InvalidConfiguration: The specified configuration is invalid.
- InvalidOrientation: The specified orientation is invalid.
- UnsupportedKinematics: The robot kinematics type is not supported.
- UnconstrainedFrame: The frame is unconstrained.
- InvalidErrorCode: Invalid error code returned.

## Robot

`from underautomation.staubli.soap.data.robot import Robot`

Represents a robot managed by the controller.

- `Robot()`: Initializes a new instance of the Robot class.
- `kinematic: Kinematic`: Kinematic type of the robot.
- `arm: str`: Arm model identifier.
- `tuning: str`: Tuning identifier.
- `mount_type: MountType`: Mounting type of the robot (floor, ceiling, wall).
- `length_axis3: LengthAxis3`: Length of the third axis.
- `diameter_axis3: DiameterAxis3`: Diameter of the third axis.

## ScaraConfig

`from underautomation.staubli.soap.data.scara_config import ScaraConfig`

Configuration for a SCARA robot.

- `ScaraConfig()`: Initializes a new instance of the ScaraConfig class.
- `shoulder: ShoulderConfig`: Shoulder configuration.

## ShoulderConfig

`from underautomation.staubli.soap.data.shoulder_config import ShoulderConfig`

Shoulder configuration for the robot arm.

- Same: Keep the same configuration as the current one.
- Lefty: Left-handed configuration.
- Righty: Right-handed configuration.
- Free: Free configuration (no constraint).

## ValApplication

`from underautomation.staubli.soap.data.val_application import ValApplication`

Represents a VAL3 application on the controller.

- `ValApplication()`
- `name: str`: Name of the application.
- `loaded: bool`: Indicates whether the application is loaded in memory.
- `is_crypted: bool`: Indicates whether the application is encrypted.
- `is_running: bool`: Indicates whether the application is currently running.

## VrbxConfig

`from underautomation.staubli.soap.data.vrbx_config import VrbxConfig`

Configuration for a VRBX-type robot.

- `VrbxConfig()`: Initializes a new instance of the VrbxConfig class.
- `joint1: AboveBelowConfig`: Joint 1 above/below configuration.
- `joint3: PositiveNegativeConfig`: Joint 3 positive/negative configuration.
- `joint5: PositiveNegativeConfig`: Joint 5 positive/negative configuration.
