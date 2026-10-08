# Trajectories from points

Create trajectories from your own positions, sampled or timed, check them against the limits of the robot, and slow them down if needed.

Web page: https://underautomation.com/fanuc/documentation/motion-trajectory-from-points

When your application computes the positions itself, create a `Trajectory` from them. The SDK never changes your positions silently: it gives you the tools to check them against the limits of the robot, and to slow them down if needed.

## One position per cycle

If you have one position per communication cycle of the robot, create the trajectory from these samples. With Stream Motion, they are sent exactly as they are, one per cycle.

```python
import math
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.geometry.joint_values import JointValues
from underautomation.robotics.motion.trajectory import Trajectory

# One position every 8 ms (communication cycle of the robot), computed by your application
cycle = 0.008
samples = []
for i in range(501):
    s = (1 - math.cos(math.pi * i / 500)) / 2   # smooth from 0 to 1 in 4 s
    samples.append(JointValues([20 * s, 0, 0, 0, -90, 0]))

# These positions are sent without any change, one per cycle
trajectory = Trajectory.from_joint_samples(samples, cycle)

# FANUC Cartesian positions work the same way: W, P, R are sent without any change
cartesian = FanucMotion.from_cartesian_samples([
    XYZWPRPosition(500, 0, 300, 180, 0, 0),
    XYZWPRPosition(500, 0, 300, 180, 0, 0),
], cycle)
```

![J1 of this trajectory. The zoom shows the positions: one every 8 ms.](https://underautomation.com/fanuc/documentation/diagrams/motion-samples.svg)

The period must be the communication cycle of the robot, given by `StreamMotion.CycleTime` (for example 0.008 or 0.002 s).

## Positions at given times

If you have a few positions with their time, the SDK joins them with a smooth curve (cubic spline). The trajectory passes through each position at its time, and the robot is at rest at the first and the last position.

```python
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.geometry.joint_values import JointValues
from underautomation.robotics.motion.trajectory import Trajectory

# A few positions with their time: the trajectory passes through each one at this time
points = [
    JointValues([0, 0, 0, 0, -90, 0]),
    JointValues([10, 5, 0, 0, -90, 0]),
    JointValues([20, 0, 5, 0, -80, 0]),
    JointValues([25, -5, 5, 0, -80, 10]),
]
times = [0.0, 1.0, 2.5, 4.0]
trajectory = Trajectory.from_timed_joints(points, times)

# Same with Cartesian positions: the orientation is interpolated with quaternions
poses = [
    XYZWPRPosition(500, 0, 300, 170, 0, 0),
    XYZWPRPosition(520, 20, 300, -175, 5, 10),
    XYZWPRPosition(540, 0, 310, -170, 0, 20),
]
cartesian = Trajectory.from_timed_cartesian([FanucMotion.to_cartesian_pose(p) for p in poses], [0.0, 1.5, 3.0])
```

![Joint positions of the joint trajectory. The curve passes through each position at its time.](https://underautomation.com/fanuc/documentation/diagrams/motion-timed-points.svg)

- The times are in seconds and must increase. The trajectory starts at the first time.
- For Cartesian positions, the orientation is interpolated with quaternions: there is no singularity, and the W, P, R angles of the trajectory stay continuous.
- The times are kept as they are. If they are too short for the robot, `Check()` tells it and `Retime()` gives a slower version.

## Check a trajectory

`Check()` computes the velocity, acceleration and jerk of each axis as the robot does: positions sampled at the communication cycle, and differences between consecutive positions. It returns the maximum values and the list of violations.

```python
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.geometry.joint_values import JointValues
from underautomation.robotics.motion.joint_limits import JointLimits
from underautomation.robotics.motion.cartesian_limits import CartesianLimits
from underautomation.robotics.motion.trajectory import Trajectory

# Limits of the robot (example values). Read them with robot.stream_motion.read_limits().reference_limits
joint_limits = JointLimits(
    [120, 120, 180, 180, 180, 180],
    [300, 300, 450, 675, 675, 675],
    [1125, 1125, 1687, 2530, 1265, 2530])
cartesian_limits = CartesianLimits(500, 2000, 10000, 90, 360, 1800)

trajectory = Trajectory.from_timed_joints(
    [JointValues([0, 0, 0, 0, -90, 0]), JointValues([90, 0, 0, 0, -90, 0])],
    [0.0, 0.5])

# Velocity, acceleration and jerk computed as the robot does, at its communication cycle.
# Last parameter: True with protocol version 1, where positions are sent in single precision.
report = trajectory.check(joint_limits, 0.008, True)
if not report.is_valid:
    first = report.violations[0]
    print(f"J{first.axis} {first.type.name} {first.value:.1f} > {first.limit:.1f} at {first.time:.3f} s")

    # Same path, played slower so that the limits are respected
    trajectory = trajectory.retime(joint_limits, 0.008, True)

# Cartesian trajectories: linear and angular limits
points = [XYZWPRPosition(500, 0, 300, 180, 0, 0), XYZWPRPosition(600, 0, 300, 180, 0, 0)]
cartesian_report = Trajectory.from_timed_cartesian(
    [FanucMotion.to_cartesian_pose(p) for p in points],
    [0.0, 1.0]).check_cartesian(cartesian_limits, 0.008)
```

![Velocity and position of J1 before and after Retime(). The retimed trajectory stays within the velocity, acceleration and jerk limits.](https://underautomation.com/fanuc/documentation/diagrams/motion-check-retime.svg)

- `singlePrecision`: set it to true for protocol version 1, where positions are sent in single precision. The rounding adds a small noise to the jerk.
- `CheckCartesian()` checks the linear and angular limits of a Cartesian trajectory. The joint limits of a Cartesian trajectory cannot be checked: the robot checks them after its own conversion to joint positions.
- `Retime()` and `RetimeCartesian()` return the same path played slower, so that the limits are respected. The positions do not change, only the time. They fail when the trajectory does not start at rest. For protocol version 1, set the `singlePrecision` parameter of `Retime()` to true, as for `Check()`: the rounding can add a few percent to the jerk.

Trajectories created by the motion planner already respect the limits given to the planner.

## Compute your own profile

`DoubleSProfile` is the jerk limited profile used by the planner. Use it to move one value, for example a position along your own path, from one position to another with velocity, acceleration and jerk limits.

```python
import underautomation.fanuc  # loads the library
from underautomation.robotics.motion.double_s_profile import DoubleSProfile

# Jerk limited profile (7 phases) from 0 to 100 mm, from rest to rest
profile = DoubleSProfile(0, 100, 0, 0, 200, 1000, 10000)
print(f"Duration: {profile.duration:.3f} s, peak velocity: {profile.peak_velocity:.1f}")

position = profile.get_position(0.25)
velocity = profile.get_velocity(0.25)
acceleration = profile.get_acceleration(0.25)

# Same profile, played in 2 seconds
slower = profile.stretch_to(2.0)
```

![The 7 phases of the profile: the jerk is constant in each phase, so the acceleration changes progressively. StretchTo() gives the same shape in a longer time.](https://underautomation.com/fanuc/documentation/diagrams/motion-double-s.svg)

The start and end velocities can be different from 0. `StretchTo()` gives the same profile in a longer time.

## API reference

**TrajectoryReport** ([reference](../api/underautomation.robotics.motion.md#trajectoryreport))

- `is_valid: bool (read only)`: True when no limit is exceeded
- `sample_count: int (read only)`: Number of samples checked
- `cycle_time: float (read only)`: Period used for the check, in seconds
- `max_velocity: typing.List[float] (read only)`: Highest velocity of each axis (9 values)
- `max_acceleration: typing.List[float] (read only)`: Highest acceleration of each axis (9 values)
- `max_jerk: typing.List[float] (read only)`: Highest jerk of each axis (9 values)
- `violation_count: int (read only)`: Total number of values that exceed a limit
- `violations: typing.List[TrajectoryViolation] (read only)`: First violations (at most 100)

**DoubleSProfile** ([reference](../api/underautomation.robotics.motion.md#doublesprofile))

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
