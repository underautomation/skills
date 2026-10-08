# underautomation.robotics.motion

## CartesianLimits (robot.stream_motion.cartesian_limits)

`from underautomation.robotics.motion.cartesian_limits import CartesianLimits`

Cartesian velocity, acceleration and jerk limits, for the position (mm) and for the orientation (degrees)

- `CartesianLimits(linearVelocity: float, linearAcceleration: float, linearJerk: float, angularVelocity: float, angularAcceleration: float, angularJerk: float)`: Creates limits with the given values
- `linear_velocity: float`: Linear velocity limit in mm/s
- `linear_acceleration: float`: Linear acceleration limit in mm/s²
- `linear_jerk: float`: Linear jerk limit in mm/s³
- `angular_velocity: float`: Angular velocity limit in deg/s
- `angular_acceleration: float`: Angular acceleration limit in deg/s²
- `angular_jerk: float`: Angular jerk limit in deg/s³

## CartesianPathBuilder

`from underautomation.robotics.motion.cartesian_path_builder import CartesianPathBuilder`

Builds a Cartesian trajectory from a sequence of linear and circular motions, splines and shapes. Create it with create_cartesian_path(). Targets are poses of the tool of the planner, in its user frame.

- `move_linear(target: CartesianPose, speed: float, termination: Termination, accelerationPercent: float=100) -> 'CartesianPathBuilder'`: Adds a linear motion: the tool moves on a straight line and its orientation turns on the shortest way.
- `move_linear_time(target: CartesianPose, duration: float, termination: Termination) -> 'CartesianPathBuilder'`: Adds a linear motion that lasts a given time. The motion takes more time when the limits do not allow this duration.
- `move_circular(via: CartesianPose, target: CartesianPose, speed: float, termination: Termination, accelerationPercent: float=100) -> 'CartesianPathBuilder'`: Adds a circular motion: the tool moves on the circle arc that passes through the via point and ends at the target. The orientation turns from the current orientation to the orientation of the target (the orientation of the via point is not used).
- `move_spline(points: typing.List[CartesianPose], speed: float, termination: Termination, accelerationPercent: float=100) -> 'CartesianPathBuilder'`: Adds a smooth motion that passes through a list of positions (cubic spline) and ends at the last one. The orientation passes through the orientation of each position. The speed is constant along the path, except where the curvature, the change of orientation or the external axes need a lower spee...
- `add_circle(plane: CartesianPose, radius: float, speed: float, termination: Termination, accelerationPercent: float=100) -> 'CartesianPathBuilder'`: Adds a full circle in the XY plane of a frame, counterclockwise around its Z axis. The circle starts and ends at the point (radius, 0, 0) of the frame. A linear motion to this point is added first when the tool is not there. The orientation of the tool does not change.
- `add_helix(plane: CartesianPose, radius: float, pitch: float, turns: float, speed: float, termination: Termination, accelerationPercent: float=100) -> 'CartesianPathBuilder'`: Adds a helix around the Z axis of a frame, counterclockwise. It starts at the point (radius, 0, 0) of the frame and rises by the pitch along Z at each turn. A linear motion to the start point is added first when the tool is not there. The orientation of the tool does not change.
- `add_spiral(plane: CartesianPose, startRadius: float, endRadius: float, turns: float, speed: float, termination: Termination, accelerationPercent: float=100) -> 'CartesianPathBuilder'`: Adds a spiral in the XY plane of a frame, counterclockwise around its Z axis. The distance to the center changes regularly from the start radius to the end radius (Archimedean spiral). It starts at the point (startRadius, 0, 0) of the frame. A linear motion to the start point is added first when...
- `add_rectangle(plane: CartesianPose, width: float, height: float, cornerRadius: float, speed: float, termination: Termination, accelerationPercent: float=100) -> 'CartesianPathBuilder'`: Adds a rectangle centered on the origin of a frame, in its XY plane: the width is along X and the height along Y. It starts and ends at the middle of the side at +X, the point (width / 2, 0, 0) of the frame, and turns counterclockwise around Z. With a corner radius, the corners are circle arcs of...
- `add_polygon(plane: CartesianPose, sideCount: int, radius: float, cornerRadius: float, speed: float, termination: Termination, accelerationPercent: float=100) -> 'CartesianPathBuilder'`: Adds a regular polygon centered on the origin of a frame, in its XY plane. One side is perpendicular to X: the polygon starts and ends at the middle of this side, and turns counterclockwise around Z. With a corner radius, the corners are circle arcs of this radius, and the curvature changes progr...
- `wait(duration: float) -> 'CartesianPathBuilder'`: Keeps the current position during a given time
- `set_io(signal: DigitalSignal, value: bool) -> 'CartesianPathBuilder'`: Writes a digital signal when the previous motion ends
- `build() -> Trajectory`: Creates the trajectory. Its poses are flange poses in the world frame when the tool and user frames of the planner are set.
- `end_position: CartesianPose (read only)`: Pose at the end of the motions added so far, as a pose of the tool in the user frame of the planner

## CartesianTrajectoryReport

`from underautomation.robotics.motion.cartesian_trajectory_report import CartesianTrajectoryReport`

Result of the check of a Cartesian trajectory against Cartesian velocity, acceleration and jerk limits

- `is_valid: bool (read only)`: True when no limit is exceeded
- `sample_count: int (read only)`: Number of samples checked
- `cycle_time: float (read only)`: Period used for the check, in seconds
- `max_linear_velocity: float (read only)`: Highest linear velocity in mm/s
- `max_linear_acceleration: float (read only)`: Highest linear acceleration in mm/s²
- `max_linear_jerk: float (read only)`: Highest linear jerk in mm/s³
- `max_angular_velocity: float (read only)`: Highest angular velocity in deg/s
- `max_angular_acceleration: float (read only)`: Highest angular acceleration in deg/s²
- `max_angular_jerk: float (read only)`: Highest angular jerk in deg/s³
- `violation_count: int (read only)`: Total number of values that exceed a limit
- `violations: typing.List[TrajectoryViolation] (read only)`: First violations (at most 100). Axis 1 is the position, axis 2 the orientation.

## DoubleSProfile

`from underautomation.robotics.motion.double_s_profile import DoubleSProfile`

One-dimensional motion profile with bounded velocity, acceleration and jerk (7 phases, "double S" profile). The acceleration is zero at the start and at the end. Start and end velocities can be different from zero.

- `DoubleSProfile(startPosition: float, endPosition: float, startVelocity: float, endVelocity: float, maxVelocity: float, maxAcceleration: float, maxJerk: float)`: Computes the fastest profile from a start position to an end position with the given limits
- `get_position(time: float) -> float`: Position at the given time (limited to [0, duration])
- `get_velocity(time: float) -> float`: Velocity at the given time (limited to [0, duration])
- `get_acceleration(time: float) -> float`: Acceleration at the given time (limited to [0, duration])
- `get_jerk(time: float) -> float`: Jerk at the given time (limited to [0, duration])
- `stretch_to(duration: float) -> 'DoubleSProfile'`: Returns the same motion slowed down to last the given duration. The velocity is divided by k, the acceleration by k² and the jerk by k³, where k is the ratio of the durations, so the limits are still respected. Only for profiles that start and end at rest.
- `start_position: float (read only)`: Start position
- `end_position: float (read only)`: End position
- `start_velocity: float (read only)`: Velocity at the start
- `end_velocity: float (read only)`: Velocity at the end
- `max_velocity: float (read only)`: Velocity limit used to compute the profile
- `max_acceleration: float (read only)`: Acceleration limit used to compute the profile
- `max_jerk: float (read only)`: Jerk limit used to compute the profile
- `duration: float (read only)`: Duration of the profile in seconds
- `acceleration_time: float (read only)`: Duration of the acceleration phase in seconds
- `constant_velocity_time: float (read only)`: Duration of the constant velocity phase in seconds
- `deceleration_time: float (read only)`: Duration of the deceleration phase in seconds
- `peak_velocity: float (read only)`: Highest velocity reached (absolute value)

## IOEvent

`from underautomation.robotics.motion.io_event import IOEvent`

Digital signal change requested at a given time of a trajectory

- `IOEvent(time: float, signal: DigitalSignal, value: bool)`: Creates an I/O event
- `time: float (read only)`: Time from the start of the trajectory, in seconds
- `signal: DigitalSignal (read only)`: Signal to write
- `value: bool (read only)`: Value to write

## JointLimits (robot.stream_motion.joint_limits)

`from underautomation.robotics.motion.joint_limits import JointLimits`

Velocity, acceleration and jerk limits of the 9 axes of a robot. Units are degrees (mm for linear axes) per second, per second squared and per second cubed. A limit of 0 means that the axis is not present or not limited.

- `JointLimits(velocity: typing.List[float], acceleration: typing.List[float], jerk: typing.List[float])`: Creates limits from arrays of values. Arrays can contain less than 9 values, missing values are set to 0.
- `scale(velocityFactor: float, accelerationFactor: float, jerkFactor: float) -> 'JointLimits'`: Returns a copy of these limits where each value is multiplied by the given factors
- `velocity: typing.List[float] (read only)`: Velocity limit of each axis (9 values)
- `acceleration: typing.List[float] (read only)`: Acceleration limit of each axis (9 values)
- `jerk: typing.List[float] (read only)`: Jerk limit of each axis (9 values)
- `static AxisCount: int`: Number of axes handled by this class

## JointPathBuilder

`from underautomation.robotics.motion.joint_path_builder import JointPathBuilder`

Builds a joint trajectory from a sequence of joint motions. Create it with create_joint_path().

- `move_joint(target: JointValues, speedPercent: float, termination: Termination, accelerationPercent: float=100) -> 'JointPathBuilder'`: Adds a joint motion: all axes move on a straight line in joint space and arrive at the same time
- `move_joint_time(target: JointValues, duration: float, termination: Termination) -> 'JointPathBuilder'`: Adds a joint motion that lasts a given time. The motion takes more time when the limits do not allow this duration.
- `move_joint_spline(points: typing.List[JointValues], speedPercent: float, termination: Termination, accelerationPercent: float=100) -> 'JointPathBuilder'`: Adds a smooth joint motion that passes through a list of positions (cubic spline) and ends at the last one. The speed changes along the path so that the velocity, acceleration and jerk of each axis stay within the limits. The points must describe a smooth path: close or noisy points give high cur...
- `wait(duration: float) -> 'JointPathBuilder'`: Keeps the current position during a given time
- `set_io(signal: DigitalSignal, value: bool) -> 'JointPathBuilder'`: Writes a digital signal when the previous motion ends
- `build() -> Trajectory`: Creates the trajectory
- `end_position: JointValues (read only)`: Position at the end of the motions added so far

## LimitType

`from underautomation.robotics.motion.limit_type import LimitType`

Type of limit of a robot axis

- Velocity: Velocity limit, in deg/s (mm/s for linear axes)
- Acceleration: Acceleration limit, in deg/s² (mm/s² for linear axes)
- Jerk: Jerk limit, in deg/s³ (mm/s³ for linear axes)

## MotionPlanner

`from underautomation.robotics.motion.motion_planner import MotionPlanner`

Creates trajectories from joint motions, linear and circular motions, splines and shapes, with velocity, acceleration and jerk limits.

- `MotionPlanner(jointLimits: JointLimits, cartesianLimits: CartesianLimits)`: Creates a planner
- `create_joint_path(start: JointValues) -> JointPathBuilder`: Starts a joint path
- `create_cartesian_path(start: CartesianPose) -> CartesianPathBuilder`: Starts a Cartesian path
- `joint_limits: JointLimits`: Limits for joint motions. 100% speed uses the velocity limits of this object. The limits of axes 7 to 9 are also used for the external axes of Cartesian motions.
- `cartesian_limits: CartesianLimits`: Limits for Cartesian motions
- `tool_frame: CartesianPose`: Tool frame, relative to the flange. When it is set, the targets of Cartesian motions are poses of this tool, and the trajectory gives the flange poses. Null when the targets are flange poses.
- `user_frame: CartesianPose`: User frame, relative to the world frame. When it is set, the targets of Cartesian motions are expressed in this frame, and the trajectory gives poses in the world frame. Null when the targets are in the world frame.

## PositionFormat (robot.stream_motion.active_format)

`from underautomation.robotics.motion.position_format import PositionFormat`

Format of the positions of a trajectory

- Joint: Joint positions (up to 9 axes), in degrees (mm for linear axes)
- Cartesian: Cartesian positions X, Y, Z in mm with an orientation, plus up to 3 external axes

## Termination

`from underautomation.robotics.motion.termination import Termination`

Termination of a motion: stop at the target, overlap with the next motion, or corner region of a given size

- `static stop() -> 'Termination'`: The robot stops at the target position
- `static overlap(percent: float) -> 'Termination'`: The next motion starts during the deceleration of this one
- `static corner(distance: float) -> 'Termination'`: Corner region: the corner is replaced by a smooth curve at constant speed. Only between Cartesian motions.
- `type: TerminationType (read only)`: Type of termination
- `value: float (read only)`: Overlap in percent (0 to 100), or corner distance in mm. 0 for a stop.

## TerminationType

`from underautomation.robotics.motion.termination_type import TerminationType`

Type of termination of a motion

- Stop: The robot stops at the target position
- Overlap: The next motion starts during the deceleration of this one. The corner is rounded, more at high speed. Between linear and circular motions, the corner is replaced by a smooth curve that starts where the robot would start to decelerate (overlap of 100%), or closer to the target.
- Corner: Corner region: the corner is replaced by a smooth curve that starts and ends at a given distance from the target position. The speed stays constant in the curve, and is reduced when its curvature needs it. Only between Cartesian motions.

## Trajectory

`from underautomation.robotics.motion.trajectory import Trajectory`

Robot trajectory in joint or Cartesian format. A trajectory can be evaluated at any time between 0 and duration, and can carry I/O events.

- `add_io_event(time: float, signal: DigitalSignal, value: bool) -> None`: Adds a digital signal change at a given time of the trajectory
- `get_joints(time: float) -> JointValues`: Returns the joint position at the given time. The trajectory must be in joint format.
- `get_cartesian(time: float) -> CartesianPose`: Returns the Cartesian pose at the given time. The trajectory must be in Cartesian format.
- `sample_joints(cycleTime: float) -> typing.List[JointValues]`: Samples the trajectory at a fixed period. The trajectory must be in joint format.
- `sample_cartesian(cycleTime: float) -> typing.List[CartesianPose]`: Samples the trajectory at a fixed period. The trajectory must be in Cartesian format.
- `static from_joint_samples(samples: typing.List[JointValues], cycleTime: float) -> 'Trajectory'`: Creates a joint trajectory from positions taken at a fixed period. When the trajectory is streamed to a robot at the same period, the positions are sent without any change.
- `static from_cartesian_samples(samples: typing.List[CartesianPose], cycleTime: float) -> 'Trajectory'`: Creates a Cartesian trajectory from poses taken at a fixed period. When the trajectory is streamed to a robot at the same period, the poses are sent without any change.
- `static from_timed_joints(points: typing.List[JointValues], times: typing.List[float]) -> 'Trajectory'`: Creates a joint trajectory that passes through positions at given times. The positions are joined by a smooth curve (cubic spline), and the robot is at rest at the first and the last position. The times are kept: use check() to verify the limits, and retime() to slow down the trajectory if needed.
- `static from_timed_cartesian(points: typing.List[CartesianPose], times: typing.List[float]) -> 'Trajectory'`: Creates a Cartesian trajectory that passes through poses at given times. The poses are joined by a smooth curve (cubic spline), and the robot is at rest at the first and the last pose. The orientation is interpolated with quaternions, so it has no singularity. The times are kept: use check_cartes...
- `check(limits: JointLimits, cycleTime: float, singlePrecision: bool) -> TrajectoryReport`: Checks the velocity, acceleration and jerk of each axis as a robot computes them from a stream of positions: positions sampled at the communication cycle, differences between consecutive positions divided by the cycle time, and positions before the first one equal to the first one. The trajectory...
- `check_cartesian(limits: CartesianLimits, cycleTime: float) -> CartesianTrajectoryReport`: Checks the linear and angular velocity, acceleration and jerk, computed from positions sampled at the communication cycle. The trajectory must be in Cartesian format. The joint limits of the robot cannot be checked from Cartesian positions.
- `retime(limits: JointLimits, cycleTime: float, singlePrecision: bool=False) -> 'Trajectory'`: Returns the same path played slower so that the joint limits are respected (see check()). The positions are the same, only the time is stretched. Returns this trajectory when it is already valid.
- `retime_cartesian(limits: CartesianLimits, cycleTime: float) -> 'Trajectory'`: Returns the same path played slower so that the Cartesian limits are respected (see check_cartesian()). The positions are the same, only the time is stretched. Returns this trajectory when it is already valid.
- `format: PositionFormat (read only)`: Format of the positions of this trajectory
- `duration: float (read only)`: Duration of the trajectory in seconds
- `cycle_time: float (read only)`: Period between two samples in seconds, when the trajectory was created from samples. 0 otherwise.
- `starts_at_rest: bool (read only)`: Indicates if the velocity and the acceleration are zero at the start of the trajectory
- `ends_at_rest: bool (read only)`: Indicates if the velocity and the acceleration are zero at the end of the trajectory
- `io_events: typing.List[IOEvent] (read only)`: I/O events of this trajectory, sorted by time
- `static MaxJointCount: int`: Maximum number of axes of a joint trajectory
- `static MaxExternalAxisCount: int`: Maximum number of external axes of a Cartesian trajectory

## TrajectoryReport

`from underautomation.robotics.motion.trajectory_report import TrajectoryReport`

Result of the check of a joint trajectory against velocity, acceleration and jerk limits

- `is_valid: bool (read only)`: True when no limit is exceeded
- `sample_count: int (read only)`: Number of samples checked
- `cycle_time: float (read only)`: Period used for the check, in seconds
- `max_velocity: typing.List[float] (read only)`: Highest velocity of each axis (9 values)
- `max_acceleration: typing.List[float] (read only)`: Highest acceleration of each axis (9 values)
- `max_jerk: typing.List[float] (read only)`: Highest jerk of each axis (9 values)
- `violation_count: int (read only)`: Total number of values that exceed a limit
- `violations: typing.List[TrajectoryViolation] (read only)`: First violations (at most 100)

## TrajectoryViolation

`from underautomation.robotics.motion.trajectory_violation import TrajectoryViolation`

Limit exceeded by a trajectory at one sample

- `index: int (read only)`: Index of the sample
- `time: float (read only)`: Time of the sample in seconds
- `axis: int (read only)`: Axis number (1 to 9). For a Cartesian check: 1 for the position, 2 for the orientation.
- `type: LimitType (read only)`: Type of limit exceeded
- `value: float (read only)`: Value reached (absolute value)
- `limit: float (read only)`: Limit
