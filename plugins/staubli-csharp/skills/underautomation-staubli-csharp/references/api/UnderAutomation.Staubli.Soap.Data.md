# UnderAutomation.Staubli.Soap.Data

## AboveBelowConfig

`enum AboveBelowConfig`

Configuration for above/below joint orientation.

- Above: Above configuration.
- Below: Below configuration.
- Free: Free configuration (no constraint).
- Same: Keep the same configuration as the current one.

## AnthroConfig

`class AnthroConfig`

Configuration for an anthropomorphic robot (shoulder, elbow, wrist).

- `AnthroConfig()`: Initializes a new instance of the Data.AnthroConfig class.
- `PositiveNegativeConfig Elbow { get; set; }`: Elbow configuration.
- `ShoulderConfig Shoulder { get; set; }`: Shoulder configuration.
- `PositiveNegativeConfig Wrist { get; set; }`: Wrist configuration.

## BlendType

`enum BlendType`

Blend mode used during motion transitions between segments.

- BlendCartesian: Cartesian-space blending between motion segments.
- BlendJoint: Joint-space blending between motion segments.
- BlendOff: No blending; the robot stops at each target point.

## CartesianJointPosition

`class CartesianJointPosition`

Represents the joint positions and the Cartesian position of a robot end effector.

- `CartesianJointPosition()`
- `CartesianPosition CartesianPosition { get; set; }`: The Cartesian position of the robot end effector.
- `double[] JointsPosition { get; set; }`: The joint positions in radians.

## CartesianPosition

`class CartesianPosition`

Represents a Cartesian position with X, Y, Z translation and Rx, Ry, Rz rotation components.

- `CartesianPosition()`: Initializes a new instance of the Data.CartesianPosition class.
- `double Rx { get; set; }`: Rotation around the X axis (radians).
- `double Ry { get; set; }`: Rotation around the Y axis (radians).
- `double Rz { get; set; }`: Rotation around the Z axis (radians).
- `double X { get; set; }`: X translation component (m).
- `double Y { get; set; }`: Y translation component (m).
- `double Z { get; set; }`: Z translation component (m).

## Config

`class Config`

Robot configuration containing kinematic-specific settings.

- `Config()`: Initializes a new instance of the Data.Config class.
- `AnthroConfig AnthroConfig { get; set; }`: Anthropomorphic robot configuration.
- `ScaraConfig ScaraConfig { get; set; }`: SCARA robot configuration.
- `VrbxConfig VrbxConfig { get; set; }`: VRBX robot configuration.

## ControllerTask

`class ControllerTask`

Represents a task running on the controller.

- `ControllerTask()`: Initializes a new instance of the Data.ControllerTask class.
- `string CreatedBy { get; set; }`: Name of the entity that created the task.
- `string Name { get; set; }`: Name of the task.
- `int Priority { get; set; }`: Priority level of the task.
- `ProgramLine ProgramLine { get; set; }`: Current program line being executed by the task.
- `int RuntimeError { get; set; }`: Runtime error code (0 if no error).
- `string RuntimeErrorDescription { get; set; }`: Human-readable description of the runtime error.
- `ControllerTaskState State { get; set; }`: Current execution state of the task.

## ControllerTaskState

`enum ControllerTaskState`

Execution state of a controller task.

- Idle: Task is idle and not executing.
- Running: Task is currently running.
- Stepping: Task is executing step by step.
- Stopped: Task is stopped.
- Transition: Task is transitioning between states.

## DhParameters

`class DhParameters`

Denavit-Hartenberg parameters for a single robot joint.

- `DhParameters()`: Initializes a new instance of the Data.DhParameters class.
- `double A { get; set; }`: Link length a (m).
- `double Alpha { get; set; }`: Link twist alpha (radians).
- `double Beta { get; set; }`: Joint twist beta (radians).
- `double D { get; set; }`: Link offset d (m).
- `double Theta { get; set; }`: Joint angle theta (radians).

## DiameterAxis3

`enum DiameterAxis3`

Diameter of the third axis of the robot.

- D20: 20 mm diameter.
- D25: 25 mm diameter.
- Invalid: Invalid or unknown diameter.

## Frame

`class Frame`

Represents a 3D transformation composed of orientation (a 3x3 rotation matrix) and position (a translation vector) in space. Used to define the pose of a robot or tool in a 3D environment. Matrix representation: [ Nx Ox Ax Px ] [ Ny Oy Ay Py ] [ Nz Oz Az Pz ] [ 0 0 0 1 ]

- `Frame()`: Default constructor.
- `double Ax { get; set; }`: X component of the local Z-axis vector (Approach X).
- `double Ay { get; set; }`: Y component of the local Z-axis vector (Approach Y).
- `double Az { get; set; }`: Z component of the local Z-axis vector (Approach Z).
- `double Nx { get; set; }`: X component of the local X-axis vector (Normal X).
- `double Ny { get; set; }`: Y component of the local X-axis vector (Normal Y).
- `double Nz { get; set; }`: Z component of the local X-axis vector (Normal Z).
- `double Ox { get; set; }`: X component of the local Y-axis vector (Orientation X).
- `double Oy { get; set; }`: Y component of the local Y-axis vector (Orientation Y).
- `double Oz { get; set; }`: Z component of the local Y-axis vector (Orientation Z).
- `double Px { get; set; }`: X coordinate of the frame's origin in global space (Pose X).
- `double Py { get; set; }`: Y coordinate of the frame's origin in global space (Pose Y).
- `double Pz { get; set; }`: Z coordinate of the frame's origin in global space (Pose Z).

## IForwardKinematics

`interface IForwardKinematics`

Represents the result of a forward kinematics computation.

- `Config Config { get; }`: Robot configuration associated with the computed position.
- `Frame Position { get; }`: Cartesian position resulting from the forward kinematics computation.

## IMoveResult

`interface IMoveResult`

Represents the result of a robot motion command.

- `int Id { get; }`: Identifier of the motion command.
- `MotionReturnCode ReturnCode { get; }`: Return code indicating the outcome of the motion command.

## IReverseKinematics

`interface IReverseKinematics`

Represents the result of a reverse (inverse) kinematics computation.

- `double[] Joint { get; }`: Joint angles resulting from the reverse kinematics computation.
- `ReversingResult Result { get; }`: Result code indicating the outcome of the reverse kinematics computation.

## JointRange

`class JointRange`

Minimum and maximum range of each robot joint (radians).

- `JointRange()`: Initializes a new instance of the Data.JointRange class.
- `double[] Max { get; set; }`: Maximum values for each joint (radians).
- `double[] Min { get; set; }`: Minimum values for each joint (radians).

## Kinematic

`enum Kinematic`

Robot kinematic type.

- Anthrioparallel6: 6-axis anthropomorphic parallel robot.
- Anthropomorph5: 5-axis anthropomorphic robot.
- Anthropomorph6: 6-axis anthropomorphic robot.
- Eisenmann: Eisenmann kinematic type.
- Invalid: Invalid or unknown kinematic type.
- Scara: SCARA robot.

## LengthAxis3

`enum LengthAxis3`

Length of the third axis of the robot.

- Invalid: Invalid or unknown length.
- L100: 100 mm length.
- L200: 200 mm length.
- L400: 400 mm length.
- L600: 600 mm length.

## MotionDesc

`class MotionDesc`

Describes the parameters of a robot motion, including tool, frame, velocity, acceleration, blending and configuration.

- `MotionDesc()`: Initializes a new instance of the Data.MotionDesc class.
- `MoveType AbsRel { get; set; }`: Specifies whether the motion is defined in absolute or relative terms.
- `double Acceleration { get; set; }`: Maximum allowed joint acceleration, as a percentage of the robot's nominal acceleration.
- `BlendType BlendType { get; set; }`: Specifies the type of blending to be applied when transitioning between motion segments.
- `Config Config { get; set; }`: Contains additional configuration parameters specific to the robot type, such as anthropomorphic, SCARA, or VRBX configurations.
- `double Deceleration { get; set; }`: Maximum allowed joint deceleration, as a percentage of the robot's nominal deceleration.
- `double DistanceBlendNext { get; set; }`: In joint and Cartesian blending modes, the distance between the target point where blending ends and the next point, in millimeters or inches, depending on the length unit of the application.
- `double DistanceBlendPrevious { get; set; }`: In the joint and Cartesian blending modes, the distance between the target point where blending begins and the next point, in millimeters or inches, depending on the length unit used in the application.
- `Frame Frame { get; set; }`: Defines the frame in which the tool position is located, including both position and orientation.
- `double Frequency { get; set; }`: Frequency of motion in Hz.
- `double RotationVelocity { get; set; }`: Maximum permitted tool rotation speed, in degrees per second.
- `Frame Tool { get; set; }`: Defines the pose of the robot's tool center point (TCP) in flange, including both position and orientation.
- `double TranslationVelocity { get; set; }`: Maximum allowed feed rate of the tool center, in mm/s or inches/s depending on the length unit of the application.
- `double Velocity { get; set; }`: Maximum allowable joint speed, as a percentage of the robot's nominal speed.

## MotionReturnCode

`enum MotionReturnCode`

Return code for robot motion commands.

- MisuseError: Motion command misuse error.
- NotReady: The robot is not ready to execute motion.
- ParameterError: Invalid parameter provided to the motion command.
- Success: Success, no error occurred.
- UnexpectedError: An unexpected error occurred during motion.

## MountType

`enum MountType`

Robot mounting type.

- Ceiling: Robot is ceiling-mounted.
- Floor: Robot is floor-mounted.
- Invalid: Invalid or unknown mount type.
- Wall: Robot is wall-mounted.

## MoveType

`enum MoveType`

Specifies whether the motion is absolute or relative.

- Absolute: Absolute motion in the reference frame.
- Relative: Relative motion from the current position.

## Parameter

`class Parameter`

Key-value parameter from the controller.

- `Parameter()`: Initializes a new instance of the Data.Parameter class.
- `string Key { get; set; }`: Parameter key identifier.
- `string Name { get; set; }`: Display name of the parameter.
- `string Value { get; set; }`: Value of the parameter.

## PhysicalAioAttribute

`class PhysicalAioAttribute`

Attributes for an analog I/O, including linear conversion coefficients.

- `PhysicalAioAttribute()`: Initializes a new instance of the Data.PhysicalAioAttribute class.
- `double CoefficientA { get; set; }`: Linear coefficient A (slope) for analog conversion.
- `double CoefficientB { get; set; }`: Linear coefficient B (offset) for analog conversion.

## PhysicalDioAttribute

`class PhysicalDioAttribute`

Attributes for a digital I/O.

- `PhysicalDioAttribute()`: Initializes a new instance of the Data.PhysicalDioAttribute class.
- `bool Inverted { get; set; }`: Indicates whether the digital I/O logic is inverted.

## PhysicalIo

`class PhysicalIo`

Represents a physical I/O on the robot.

- `PhysicalIo()`
- `string Description { get; set; }`: Description of the physical I/O.
- `bool Lockable { get; set; }`: Indicates whether the physical I/O is lockable.
- `string Name { get; set; }`: Name of the physical I/O.
- `string TypeStr { get; set; }`: Type of the physical I/O (e.g., din, dout, ain, serial, ...).

## PhysicalIoAttribute

`class PhysicalIoAttribute`

Physical I/O attribute containing either analog or digital specific attributes.

- `PhysicalIoAttribute()`: Initializes a new instance of the Data.PhysicalIoAttribute class.
- `PhysicalAioAttribute AioAttribute { get; set; }`: Analog I/O specific attributes (null if digital).
- `PhysicalDioAttribute DioAttribute { get; set; }`: Digital I/O specific attributes (null if analog).

## PhysicalIoEnumState

`enum PhysicalIoEnumState`

Definition state of a physical I/O.

- Defined: The I/O is defined and available.
- InvalidName: The I/O name is invalid.
- Undefined: The I/O is not defined.

## PhysicalIoState

`class PhysicalIoState`

Current state and value of a physical I/O.

- `PhysicalIoState()`: Initializes a new instance of the Data.PhysicalIoState class.
- `PhysicalIoAttribute Attribute { get; set; }`: I/O type-specific attributes (analog or digital).
- `bool Locked { get; set; }`: Indicates whether the I/O is locked.
- `bool Simulated { get; set; }`: Indicates whether the I/O is in simulation mode.
- `PhysicalIoEnumState State { get; set; }`: Definition state of the I/O.
- `double Value { get; set; }`: Current numeric value of the I/O.

## PhysicalIoWriteResponse

`class PhysicalIoWriteResponse`

Result of a physical I/O write operation.

- `PhysicalIoWriteResponse()`: Initializes a new instance of the Data.PhysicalIoWriteResponse class.
- `bool Found { get; set; }`: Indicates whether the specified I/O was found.
- `bool Success { get; set; }`: Indicates whether the write operation succeeded.

## PositiveNegativeConfig

`enum PositiveNegativeConfig`

Positive/negative configuration for a robot joint.

- Free: Free configuration (no constraint).
- Negative: Negative configuration.
- Positive: Positive configuration.
- Same: Keep the same configuration as the current one.

## PowerReturnCode

`enum PowerReturnCode`

Return code for robot power commands.

- DisableTimeout: Timeout while disabling power.
- EnableTimeout: Timeout while enabling power.
- OnlyInRemoteMode: Power can only be changed in remote mode.
- RobotNotStopped: Cannot change power while the robot is not stopped.
- Success: Success, no error occurred.

## ProgramLine

`class ProgramLine`

Represents a line of a VAL3 program being executed on the controller.

- `ProgramLine()`: Initializes a new instance of the Data.ProgramLine class.
- `string ApplicationName { get; set; }`: Name of the application containing the program.
- `string LineContent { get; set; }`: Content of the line being executed.
- `int LineNumber { get; set; }`: Line number currently being executed.
- `string ProgramName { get; set; }`: Name of the program.

## ReversingResult

`enum ReversingResult`

Result code for reverse kinematics computation.

- InvalidConfiguration: The specified configuration is invalid.
- InvalidErrorCode: Invalid error code returned.
- InvalidOrientation: The specified orientation is invalid.
- JointOutOfRange: The computed joint position is out of range.
- NoConvergence: The algorithm did not converge to a solution.
- OutOfWorkspace: The target is outside the robot workspace.
- Success: Reverse kinematics succeeded.
- UnconstrainedFrame: The frame is unconstrained.
- UnsupportedKinematics: The robot kinematics type is not supported.

## Robot

`class Robot`

Represents a robot managed by the controller.

- `Robot()`: Initializes a new instance of the Data.Robot class.
- `string Arm { get; set; }`: Arm model identifier.
- `DiameterAxis3 DiameterAxis3 { get; set; }`: Diameter of the third axis.
- `Kinematic Kinematic { get; set; }`: Kinematic type of the robot.
- `LengthAxis3 LengthAxis3 { get; set; }`: Length of the third axis.
- `MountType MountType { get; set; }`: Mounting type of the robot (floor, ceiling, wall).
- `string Tuning { get; set; }`: Tuning identifier.

## ScaraConfig

`class ScaraConfig`

Configuration for a SCARA robot.

- `ScaraConfig()`: Initializes a new instance of the Data.ScaraConfig class.
- `ShoulderConfig Shoulder { get; set; }`: Shoulder configuration.

## ShoulderConfig

`enum ShoulderConfig`

Shoulder configuration for the robot arm.

- Free: Free configuration (no constraint).
- Lefty: Left-handed configuration.
- Righty: Right-handed configuration.
- Same: Keep the same configuration as the current one.

## ValApplication

`class ValApplication`

Represents a VAL3 application on the controller.

- `ValApplication()`
- `bool IsCrypted { get; set; }`: Indicates whether the application is encrypted.
- `bool IsRunning { get; set; }`: Indicates whether the application is currently running.
- `bool Loaded { get; set; }`: Indicates whether the application is loaded in memory.
- `string Name { get; set; }`: Name of the application.

## VrbxConfig

`class VrbxConfig`

Configuration for a VRBX-type robot.

- `VrbxConfig()`: Initializes a new instance of the Data.VrbxConfig class.
- `AboveBelowConfig Joint1 { get; set; }`: Joint 1 above/below configuration.
- `PositiveNegativeConfig Joint3 { get; set; }`: Joint 3 positive/negative configuration.
- `PositiveNegativeConfig Joint5 { get; set; }`: Joint 5 positive/negative configuration.
