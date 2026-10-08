# UnderAutomation.Robotics.Motion

## CartesianLimits (robot.StreamMotion.CartesianLimits)

`class CartesianLimits`

Cartesian velocity, acceleration and jerk limits, for the position (mm) and for the orientation (degrees)

- `CartesianLimits()`: Creates limits with all values set to 0
- `CartesianLimits(double linearVelocity, double linearAcceleration, double linearJerk, double angularVelocity, double angularAcceleration, double angularJerk)`: Creates limits with the given values
- `double AngularAcceleration { get; set; }`: Angular acceleration limit in deg/s²
- `double AngularJerk { get; set; }`: Angular jerk limit in deg/s³
- `double AngularVelocity { get; set; }`: Angular velocity limit in deg/s
- `double LinearAcceleration { get; set; }`: Linear acceleration limit in mm/s²
- `double LinearJerk { get; set; }`: Linear jerk limit in mm/s³
- `double LinearVelocity { get; set; }`: Linear velocity limit in mm/s

## CartesianPathBuilder

`class CartesianPathBuilder`

Builds a Cartesian trajectory from a sequence of linear and circular motions, splines and shapes. Create it with Geometry.CartesianPose). Targets are poses of the tool of the planner, in its user frame.

- `CartesianPathBuilder AddCircle(CartesianPose plane, double radius, double speed, Termination termination, double accelerationPercent = 100)`: Adds a full circle in the XY plane of a frame, counterclockwise around its Z axis. The circle starts and ends at the point (radius, 0, 0) of the frame. A linear motion to this point is added first when the tool is not there. The orientation of the tool does not change.
- `CartesianPathBuilder AddHelix(CartesianPose plane, double radius, double pitch, double turns, double speed, Termination termination, double accelerationPercent = 100)`: Adds a helix around the Z axis of a frame, counterclockwise. It starts at the point (radius, 0, 0) of the frame and rises by the pitch along Z at each turn. A linear motion to the start point is added first when the tool is not there. The orientation of the tool does not change.
- `CartesianPathBuilder AddPolygon(CartesianPose plane, int sideCount, double radius, double cornerRadius, double speed, Termination termination, double accelerationPercent = 100)`: Adds a regular polygon centered on the origin of a frame, in its XY plane. One side is perpendicular to X: the polygon starts and ends at the middle of this side, and turns counterclockwise around Z. With a corner radius, the corners are circle arcs of this radius, and the curvature changes progr...
- `CartesianPathBuilder AddRectangle(CartesianPose plane, double width, double height, double cornerRadius, double speed, Termination termination, double accelerationPercent = 100)`: Adds a rectangle centered on the origin of a frame, in its XY plane: the width is along X and the height along Y. It starts and ends at the middle of the side at +X, the point (width / 2, 0, 0) of the frame, and turns counterclockwise around Z. With a corner radius, the corners are circle arcs of...
- `CartesianPathBuilder AddSpiral(CartesianPose plane, double startRadius, double endRadius, double turns, double speed, Termination termination, double accelerationPercent = 100)`: Adds a spiral in the XY plane of a frame, counterclockwise around its Z axis. The distance to the center changes regularly from the start radius to the end radius (Archimedean spiral). It starts at the point (startRadius, 0, 0) of the frame. A linear motion to the start point is added first when...
- `Trajectory Build()`: Creates the trajectory. Its poses are flange poses in the world frame when the tool and user frames of the planner are set.
- `CartesianPose EndPosition { get; }`: Pose at the end of the motions added so far, as a pose of the tool in the user frame of the planner
- `CartesianPathBuilder MoveCircular(CartesianPose via, CartesianPose target, double speed, Termination termination, double accelerationPercent = 100)`: Adds a circular motion: the tool moves on the circle arc that passes through the via point and ends at the target. The orientation turns from the current orientation to the orientation of the target (the orientation of the via point is not used).
- `CartesianPathBuilder MoveLinear(CartesianPose target, double speed, Termination termination, double accelerationPercent = 100)`: Adds a linear motion: the tool moves on a straight line and its orientation turns on the shortest way.
- `CartesianPathBuilder MoveLinearTime(CartesianPose target, double duration, Termination termination)`: Adds a linear motion that lasts a given time. The motion takes more time when the limits do not allow this duration.
- `CartesianPathBuilder MoveSpline(CartesianPose[] points, double speed, Termination termination, double accelerationPercent = 100)`: Adds a smooth motion that passes through a list of positions (cubic spline) and ends at the last one. The orientation passes through the orientation of each position. The speed is constant along the path, except where the curvature, the change of orientation or the external axes need a lower spee...
- `CartesianPathBuilder SetIO(DigitalSignal signal, bool value)`: Writes a digital signal when the previous motion ends
- `CartesianPathBuilder Wait(double duration)`: Keeps the current position during a given time

## CartesianTrajectoryReport

`class CartesianTrajectoryReport`

Result of the check of a Cartesian trajectory against Cartesian velocity, acceleration and jerk limits

- `double CycleTime { get; }`: Period used for the check, in seconds
- `bool IsValid { get; }`: True when no limit is exceeded
- `double MaxAngularAcceleration { get; }`: Highest angular acceleration in deg/s²
- `double MaxAngularJerk { get; }`: Highest angular jerk in deg/s³
- `double MaxAngularVelocity { get; }`: Highest angular velocity in deg/s
- `double MaxLinearAcceleration { get; }`: Highest linear acceleration in mm/s²
- `double MaxLinearJerk { get; }`: Highest linear jerk in mm/s³
- `double MaxLinearVelocity { get; }`: Highest linear velocity in mm/s
- `int SampleCount { get; }`: Number of samples checked
- `int ViolationCount { get; }`: Total number of values that exceed a limit
- `TrajectoryViolation[] Violations { get; }`: First violations (at most 100). Axis 1 is the position, axis 2 the orientation.

## DoubleSProfile

`class DoubleSProfile`

One-dimensional motion profile with bounded velocity, acceleration and jerk (7 phases, "double S" profile). The acceleration is zero at the start and at the end. Start and end velocities can be different from zero.

- `DoubleSProfile(double startPosition, double endPosition, double startVelocity, double endVelocity, double maxVelocity, double maxAcceleration, double maxJerk)`: Computes the fastest profile from a start position to an end position with the given limits
- `double AccelerationTime { get; }`: Duration of the acceleration phase in seconds
- `double ConstantVelocityTime { get; }`: Duration of the constant velocity phase in seconds
- `double DecelerationTime { get; }`: Duration of the deceleration phase in seconds
- `double Duration { get; }`: Duration of the profile in seconds
- `double EndPosition { get; }`: End position
- `double EndVelocity { get; }`: Velocity at the end
- `double GetAcceleration(double time)`: Acceleration at the given time (limited to [0, DoubleSProfile.Duration])
- `double GetJerk(double time)`: Jerk at the given time (limited to [0, DoubleSProfile.Duration])
- `double GetPosition(double time)`: Position at the given time (limited to [0, DoubleSProfile.Duration])
- `double GetVelocity(double time)`: Velocity at the given time (limited to [0, DoubleSProfile.Duration])
- `double MaxAcceleration { get; }`: Acceleration limit used to compute the profile
- `double MaxJerk { get; }`: Jerk limit used to compute the profile
- `double MaxVelocity { get; }`: Velocity limit used to compute the profile
- `double PeakVelocity { get; }`: Highest velocity reached (absolute value)
- `double StartPosition { get; }`: Start position
- `double StartVelocity { get; }`: Velocity at the start
- `DoubleSProfile StretchTo(double duration)`: Returns the same motion slowed down to last the given duration. The velocity is divided by k, the acceleration by k² and the jerk by k³, where k is the ratio of the durations, so the limits are still respected. Only for profiles that start and end at rest.

## IOEvent

`class IOEvent`

Digital signal change requested at a given time of a trajectory

- `IOEvent(double time, DigitalSignal signal, bool value)`: Creates an I/O event
- `DigitalSignal Signal { get; }`: Signal to write
- `double Time { get; }`: Time from the start of the trajectory, in seconds
- `bool Value { get; }`: Value to write

## JointLimits (robot.StreamMotion.JointLimits)

`class JointLimits`

Velocity, acceleration and jerk limits of the 9 axes of a robot. Units are degrees (mm for linear axes) per second, per second squared and per second cubed. A limit of 0 means that the axis is not present or not limited.

- `JointLimits()`: Creates limits with all values set to 0
- `JointLimits(double[] velocity, double[] acceleration, double[] jerk)`: Creates limits from arrays of values. Arrays can contain less than 9 values, missing values are set to 0.
- `double[] Acceleration { get; }`: Acceleration limit of each axis (9 values)
- `const int AxisCount = 9`: Number of axes handled by this class
- `double[] Jerk { get; }`: Jerk limit of each axis (9 values)
- `JointLimits Scale(double velocityFactor, double accelerationFactor, double jerkFactor)`: Returns a copy of these limits where each value is multiplied by the given factors
- `double[] Velocity { get; }`: Velocity limit of each axis (9 values)

## JointPathBuilder

`class JointPathBuilder`

Builds a joint trajectory from a sequence of joint motions. Create it with Geometry.JointValues).

- `Trajectory Build()`: Creates the trajectory
- `JointValues EndPosition { get; }`: Position at the end of the motions added so far
- `JointPathBuilder MoveJoint(JointValues target, double speedPercent, Termination termination, double accelerationPercent = 100)`: Adds a joint motion: all axes move on a straight line in joint space and arrive at the same time
- `JointPathBuilder MoveJointSpline(JointValues[] points, double speedPercent, Termination termination, double accelerationPercent = 100)`: Adds a smooth joint motion that passes through a list of positions (cubic spline) and ends at the last one. The speed changes along the path so that the velocity, acceleration and jerk of each axis stay within the limits. The points must describe a smooth path: close or noisy points give high cur...
- `JointPathBuilder MoveJointTime(JointValues target, double duration, Termination termination)`: Adds a joint motion that lasts a given time. The motion takes more time when the limits do not allow this duration.
- `JointPathBuilder SetIO(DigitalSignal signal, bool value)`: Writes a digital signal when the previous motion ends
- `JointPathBuilder Wait(double duration)`: Keeps the current position during a given time

## LimitType

`enum LimitType`

Type of limit of a robot axis

- Acceleration: Acceleration limit, in deg/s² (mm/s² for linear axes)
- Jerk: Jerk limit, in deg/s³ (mm/s³ for linear axes)
- Velocity: Velocity limit, in deg/s (mm/s for linear axes)

## MotionPlanner

`class MotionPlanner`

Creates trajectories from joint motions, linear and circular motions, splines and shapes, with velocity, acceleration and jerk limits.

- `MotionPlanner(JointLimits jointLimits, CartesianLimits cartesianLimits)`: Creates a planner
- `CartesianLimits CartesianLimits { get; set; }`: Limits for Cartesian motions
- `CartesianPathBuilder CreateCartesianPath(CartesianPose start)`: Starts a Cartesian path
- `JointPathBuilder CreateJointPath(JointValues start)`: Starts a joint path
- `JointLimits JointLimits { get; set; }`: Limits for joint motions. 100% speed uses the velocity limits of this object. The limits of axes 7 to 9 are also used for the external axes of Cartesian motions.
- `CartesianPose ToolFrame { get; set; }`: Tool frame, relative to the flange. When it is set, the targets of Cartesian motions are poses of this tool, and the trajectory gives the flange poses. Null when the targets are flange poses.
- `CartesianPose UserFrame { get; set; }`: User frame, relative to the world frame. When it is set, the targets of Cartesian motions are expressed in this frame, and the trajectory gives poses in the world frame. Null when the targets are in the world frame.

## PositionFormat (robot.StreamMotion.ActiveFormat)

`enum PositionFormat`

Format of the positions of a trajectory

- Cartesian: Cartesian positions X, Y, Z in mm with an orientation, plus up to 3 external axes
- Joint: Joint positions (up to 9 axes), in degrees (mm for linear axes)

## Termination

`class Termination`

Termination of a motion: stop at the target, overlap with the next motion, or corner region of a given size

- `static Termination Corner(double distance)`: Corner region: the corner is replaced by a smooth curve at constant speed. Only between Cartesian motions.
- `static Termination Overlap(double percent)`: The next motion starts during the deceleration of this one
- `static Termination Stop()`: The robot stops at the target position
- `TerminationType Type { get; }`: Type of termination
- `double Value { get; }`: Overlap in percent (0 to 100), or corner distance in mm. 0 for a stop.

## TerminationType

`enum TerminationType`

Type of termination of a motion

- Corner: Corner region: the corner is replaced by a smooth curve that starts and ends at a given distance from the target position. The speed stays constant in the curve, and is reduced when its curvature needs it. Only between Cartesian motions.
- Overlap: The next motion starts during the deceleration of this one. The corner is rounded, more at high speed. Between linear and circular motions, the corner is replaced by a smooth curve that starts where the robot would start to decelerate (overlap of 100%), or closer to the target.
- Stop: The robot stops at the target position

## Trajectory

`class Trajectory`

Robot trajectory in joint or Cartesian format. A trajectory can be evaluated at any time between 0 and Trajectory.Duration, and can carry I/O events.

- `void AddIOEvent(double time, DigitalSignal signal, bool value)`: Adds a digital signal change at a given time of the trajectory
- `TrajectoryReport Check(JointLimits limits, double cycleTime, bool singlePrecision)`: Checks the velocity, acceleration and jerk of each axis as a robot computes them from a stream of positions: positions sampled at the communication cycle, differences between consecutive positions divided by the cycle time, and positions before the first one equal to the first one. The trajectory...
- `CartesianTrajectoryReport CheckCartesian(CartesianLimits limits, double cycleTime)`: Checks the linear and angular velocity, acceleration and jerk, computed from positions sampled at the communication cycle. The trajectory must be in Cartesian format. The joint limits of the robot cannot be checked from Cartesian positions.
- `double CycleTime { get; }`: Period between two samples in seconds, when the trajectory was created from samples. 0 otherwise.
- `double Duration { get; }`: Duration of the trajectory in seconds
- `bool EndsAtRest { get; }`: Indicates if the velocity and the acceleration are zero at the end of the trajectory
- `PositionFormat Format { get; }`: Format of the positions of this trajectory
- `static Trajectory FromCartesianSamples(CartesianPose[] samples, double cycleTime)`: Creates a Cartesian trajectory from poses taken at a fixed period. When the trajectory is streamed to a robot at the same period, the poses are sent without any change.
- `static Trajectory FromJointSamples(JointValues[] samples, double cycleTime)`: Creates a joint trajectory from positions taken at a fixed period. When the trajectory is streamed to a robot at the same period, the positions are sent without any change.
- `static Trajectory FromTimedCartesian(CartesianPose[] points, double[] times)`: Creates a Cartesian trajectory that passes through poses at given times. The poses are joined by a smooth curve (cubic spline), and the robot is at rest at the first and the last pose. The orientation is interpolated with quaternions, so it has no singularity. The times are kept: use CartesianLim...
- `static Trajectory FromTimedJoints(JointValues[] points, double[] times)`: Creates a joint trajectory that passes through positions at given times. The positions are joined by a smooth curve (cubic spline), and the robot is at rest at the first and the last position. The times are kept: use Double%2cSystem.Boolean) to verify the limits, and Double%2cSystem.Boolean) to s...
- `CartesianPose GetCartesian(double time)`: Returns the Cartesian pose at the given time. The trajectory must be in Cartesian format.
- `JointValues GetJoints(double time)`: Returns the joint position at the given time. The trajectory must be in joint format.
- `IOEvent[] IOEvents { get; }`: I/O events of this trajectory, sorted by time
- `const int MaxExternalAxisCount = 3`: Maximum number of external axes of a Cartesian trajectory
- `const int MaxJointCount = 9`: Maximum number of axes of a joint trajectory
- `Trajectory Retime(JointLimits limits, double cycleTime, bool singlePrecision = false)`: Returns the same path played slower so that the joint limits are respected (see Double%2cSystem.Boolean)). The positions are the same, only the time is stretched. Returns this trajectory when it is already valid.
- `Trajectory RetimeCartesian(CartesianLimits limits, double cycleTime)`: Returns the same path played slower so that the Cartesian limits are respected (see CartesianLimits%2cSystem.Double)). The positions are the same, only the time is stretched. Returns this trajectory when it is already valid.
- `CartesianPose[] SampleCartesian(double cycleTime)`: Samples the trajectory at a fixed period. The trajectory must be in Cartesian format.
- `JointValues[] SampleJoints(double cycleTime)`: Samples the trajectory at a fixed period. The trajectory must be in joint format.
- `bool StartsAtRest { get; }`: Indicates if the velocity and the acceleration are zero at the start of the trajectory

## TrajectoryReport

`class TrajectoryReport`

Result of the check of a joint trajectory against velocity, acceleration and jerk limits

- `double CycleTime { get; }`: Period used for the check, in seconds
- `bool IsValid { get; }`: True when no limit is exceeded
- `double[] MaxAcceleration { get; }`: Highest acceleration of each axis (9 values)
- `double[] MaxJerk { get; }`: Highest jerk of each axis (9 values)
- `double[] MaxVelocity { get; }`: Highest velocity of each axis (9 values)
- `int SampleCount { get; }`: Number of samples checked
- `int ViolationCount { get; }`: Total number of values that exceed a limit
- `TrajectoryViolation[] Violations { get; }`: First violations (at most 100)

## TrajectoryViolation

`class TrajectoryViolation`

Limit exceeded by a trajectory at one sample

- `int Axis { get; }`: Axis number (1 to 9). For a Cartesian check: 1 for the position, 2 for the orientation.
- `int Index { get; }`: Index of the sample
- `double Limit { get; }`: Limit
- `double Time { get; }`: Time of the sample in seconds
- `LimitType Type { get; }`: Type of limit exceeded
- `double Value { get; }`: Value reached (absolute value)
