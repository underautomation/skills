# Motion planner overview

Create smooth robot trajectories offline, with velocity, acceleration and jerk limits, using FANUC motion instructions (J, L, C, FINE, CNT, CR).

Web page: https://underautomation.com/fanuc/documentation/motion

The Motion module creates smooth robot trajectories that respect velocity, acceleration and jerk limits. It works offline, without robot connection, and its trajectories can be sent with [Stream Motion](stream-motion.md), used in a simulation, or checked before use.

Motions are described as in a TP program: joint (J), linear (L) and circular (C) motions, with a speed and a FINE, CNT or CR termination. The module also creates splines through points, geometric shapes, and trajectories from your own positions.

The planner is in the `UnderAutomation.Robotics.Motion` namespace. This namespace is the same in all UnderAutomation robot SDKs, so the same code can plan trajectories for other robot brands. The `FanucMotion` class of `UnderAutomation.Fanuc.Motion` converts FANUC positions, FINE, CNT and CR terminations and I/O to the types of the planner.

## Quick start

```python
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.geometry.joint_values import JointValues
from underautomation.robotics.motion.joint_limits import JointLimits
from underautomation.robotics.motion.cartesian_limits import CartesianLimits
from underautomation.robotics.motion.motion_planner import MotionPlanner

# Limits of the robot (example values). Read them with robot.stream_motion.read_limits().reference_limits
joint_limits = JointLimits(
    [120, 120, 180, 180, 180, 180],
    [300, 300, 450, 675, 675, 675],
    [1125, 1125, 1687, 2530, 1265, 2530])
cartesian_limits = CartesianLimits(500, 2000, 10000, 90, 360, 1800)

planner = MotionPlanner(joint_limits, cartesian_limits)

# Joint motions, as J instructions of a TP program
home = JointValues([0, 0, 0, 0, -90, 0])
pick = JointValues([30, 20, -10, 0, -70, 30])
trajectory = planner.create_joint_path(home) \
    .move_joint(pick, 50, FanucMotion.cnt(100)) \
    .move_joint(home, 50, FanucMotion.fine()) \
    .build()

print(f"Duration: {trajectory.duration:.3f} s")

# Position at any time, or one position per communication cycle
middle = trajectory.get_joints(trajectory.duration / 2)
samples = trajectory.sample_joints(0.008)

# FANUC joint position, when needed
fanuc_middle = FanucMotion.to_joints_position(middle)

# Velocity, acceleration and jerk of each axis, computed as the robot does
report = trajectory.check(joint_limits, 0.008, False)
print(report.is_valid)
```

![Joint positions of this trajectory. With CNT100, the robot passes near pick without stopping. With FINE, it stops at home.](https://underautomation.com/fanuc/documentation/diagrams/motion-quick-start.svg)

## Try it in the demo application

The [demo application](demo-app.md) (Windows) has a Stream Motion page with two buttons that build trajectories with the motion planner and send them to the robot with [Stream Motion](stream-motion.md).

- **Joint demo** uses a `JointPathBuilder`: J1 moves to +amplitude, then to -amplitude with a `Cnt` termination between the two moves, then back to the start with `Fine`.
- **Cartesian demo** uses a `CartesianPathBuilder`: a horizontal circle of the given radius, starting and ending at the current position.

Change the amplitude, the radius or the speed and send the demo again: the duration of the resulting trajectory is shown in the log, and the joint and Cartesian positions update in real time while the robot moves.

![Stream Motion page of the Showcase demo application, with the joint and Cartesian demo motions](https://underautomation.com/fanuc/documentation/demo-stream-motion-showcase-forms.gif)

The C# source of this page is in the `StreamMotionControl.cs` file of the [Fanuc.NET repository](https://github.com/underautomation/Fanuc.NET/blob/main/UnderAutomation.Fanuc.Showcase.Forms/Components/StreamMotionControl.cs).

## Main concepts

| Class | Role |
| --- | --- |
| `JointLimits` | Velocity, acceleration and jerk of each axis (9 axes). Read them from the robot with `StreamMotion.ReadLimits()` |
| `CartesianLimits` | Linear and angular velocity, acceleration and jerk, for Cartesian motions. You choose them |
| `MotionPlanner` | Creates joint and Cartesian paths with the limits, and optional tool and user frames |
| `JointPathBuilder`, `CartesianPathBuilder` | Chain motions, waits and I/O, then `Build()` the trajectory |
| `Trajectory` | Result: position at any time, samples at a fixed period, I/O events, limit checks |
| `JointValues`, `CartesianPose` | Joint and Cartesian positions of the planner. A `CartesianPose` has X, Y, Z, an `Orientation` and optional external axes |
| `FanucMotion` | Conversions with `JointsPosition` and `XYZWPRPosition`, FINE, CNT and CR terminations, I/O signals, FANUC positions of a trajectory |

All motions use jerk limited profiles: the acceleration changes progressively, which gives smooth motions and avoids the jerk alarms of the robot. 100% speed means the velocity limits, and the acceleration percentage (ACC) scales the acceleration and the jerk.

![Velocity of J1 for the same joint motion. The speed percentage limits the velocity, ACC changes the slopes.](https://underautomation.com/fanuc/documentation/diagrams/motion-speed-acceleration.svg)

## What do you want to do?

| Need | Page |
| --- | --- |
| Move to positions with J, L, C motions, FINE, CNT, CR | [Joint & Cartesian motions](motion-moves.md) |
| Pass through a list of points, draw a circle, a rectangle or a helix | [Splines & shapes](motion-splines-shapes.md) |
| Use positions computed by your application, check or slow down a trajectory | [Trajectories from points](motion-trajectory-from-points.md) |
| Convert orientations and positions between frames | [Frames & orientations](motion-frames-orientations.md) |

## Units and conventions

- Joint positions in degrees (mm for linear axes), Cartesian positions in mm, angles in degrees.
- Velocities per second, accelerations per second squared, jerks per second cubed.
- The W, P, R angles of FANUC use the fixed XYZ convention: `CartesianPose.FromEuler(x, y, z, w, p, r, EulerConvention.FixedXYZ)` gives the same pose as `FanucMotion.ToCartesianPose(new XYZWPRPosition(x, y, z, w, p, r))`.
- `FanucMotion.SampleCartesian()` gives FANUC positions whose W, P, R angles stay continuous: an angle can go beyond 180 degrees instead of jumping to -180.

## API reference

**MotionPlanner** ([reference](../api/underautomation.robotics.motion.md#motionplanner))

- `MotionPlanner(jointLimits: JointLimits, cartesianLimits: CartesianLimits)`: Creates a planner
- `create_joint_path(start: JointValues) -> JointPathBuilder`: Starts a joint path
- `create_cartesian_path(start: CartesianPose) -> CartesianPathBuilder`: Starts a Cartesian path
- `joint_limits: JointLimits`: Limits for joint motions. 100% speed uses the velocity limits of this object. The limits of axes 7 to 9 are also used for the external axes of Cartesian motions.
- `cartesian_limits: CartesianLimits`: Limits for Cartesian motions
- `tool_frame: CartesianPose`: Tool frame, relative to the flange. When it is set, the targets of Cartesian motions are poses of this tool, and the trajectory gives the flange poses. Null when the targets are flange poses.
- `user_frame: CartesianPose`: User frame, relative to the world frame. When it is set, the targets of Cartesian motions are expressed in this frame, and the trajectory gives poses in the world frame. Null when the targets are in the world frame.

**JointLimits** ([reference](../api/underautomation.robotics.motion.md#jointlimits-robotstream_motionjoint_limits))

- `JointLimits(velocity: typing.List[float], acceleration: typing.List[float], jerk: typing.List[float])`: Creates limits from arrays of values. Arrays can contain less than 9 values, missing values are set to 0.
- `scale(velocityFactor: float, accelerationFactor: float, jerkFactor: float) -> 'JointLimits'`: Returns a copy of these limits where each value is multiplied by the given factors
- `velocity: typing.List[float] (read only)`: Velocity limit of each axis (9 values)
- `acceleration: typing.List[float] (read only)`: Acceleration limit of each axis (9 values)
- `jerk: typing.List[float] (read only)`: Jerk limit of each axis (9 values)
- `static AxisCount: int`: Number of axes handled by this class

**CartesianLimits** ([reference](../api/underautomation.robotics.motion.md#cartesianlimits-robotstream_motioncartesian_limits))

- `CartesianLimits(linearVelocity: float, linearAcceleration: float, linearJerk: float, angularVelocity: float, angularAcceleration: float, angularJerk: float)`: Creates limits with the given values
- `linear_velocity: float`: Linear velocity limit in mm/s
- `linear_acceleration: float`: Linear acceleration limit in mm/s²
- `linear_jerk: float`: Linear jerk limit in mm/s³
- `angular_velocity: float`: Angular velocity limit in deg/s
- `angular_acceleration: float`: Angular acceleration limit in deg/s²
- `angular_jerk: float`: Angular jerk limit in deg/s³

**FanucMotion** ([reference](../api/underautomation.fanuc.motion.md#fanucmotion))

- `static to_cartesian_pose(position: XYZWPRPosition) -> CartesianPose`: Converts a FANUC position to a pose. The extended axes E1, E2 and E3 are copied when the position is an ExtendedCartesianPosition.
- `static to_extended_cartesian_position(pose: CartesianPose, reference: XYZWPRPosition) -> ExtendedCartesianPosition`: Converts a pose to a FANUC position with extended axes (0 when the pose has no external axes).
- `static to_joint_values(position: JointsPosition) -> JointValues`: Converts a FANUC joint position (J1 to J9) to joint values
- `static to_joints_position(values: JointValues) -> JointsPosition`: Converts joint values to a FANUC joint position. Missing axes are 0.
- `static fine() -> Termination`: FINE termination: the robot stops at the target position
- `static cnt(value: int) -> Termination`: CNT termination: the next motion starts during the deceleration of this one
- `static cr(distance: float) -> Termination`: CR termination (corner region): the corner is replaced by a smooth curve at constant speed. Only between Cartesian motions.
- `static signal(type: IOType, index: int) -> DigitalSignal`: Returns the digital signal of an I/O, to write it during a trajectory (for example DO[5])
- `static from_cartesian_samples(samples: typing.List[XYZWPRPosition], cycleTime: float) -> Trajectory`: Creates a Cartesian trajectory from FANUC positions taken at a fixed period. The W, P, R angles are kept without any change, and the extended axes are used when the positions are ExtendedCartesianPosition.
- `static sample_cartesian(trajectory: Trajectory, cycleTime: float) -> typing.List[ExtendedCartesianPosition]`: Samples a Cartesian trajectory at a fixed period and returns FANUC positions. The W, P, R angles stay continuous from one position to the next.
- `static wpr_convention: EulerConvention (read only)`: Convention of the W, P, R angles of FANUC positions: rotation W around the fixed X axis, then P around the fixed Y axis, then R around the fixed Z axis
