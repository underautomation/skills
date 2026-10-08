# Joint & Cartesian motions

Chain joint, linear and circular motions with FINE, CNT and CR terminations, waits and I/O, in tool and user frames.

Web page: https://underautomation.com/fanuc/documentation/motion-moves

Path builders describe a trajectory as the instructions of a TP program. Each method adds a motion and returns the builder, so the calls can be chained. `Build()` creates the trajectory.

![The same start and target with a joint (J), a linear (L) and a circular (C) motion, seen from above.](https://underautomation.com/fanuc/documentation/diagrams/motion-joint-linear-circular.svg)

## Joint motions

A joint motion moves all axes together on a straight line in joint space: they start and stop at the same time.

```python
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.fanuc.stream_motion.data.io_type import IOType
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

planner = MotionPlanner(joint_limits, None)
start = JointValues([0, 0, 0, 0, -90, 0])
p1 = JointValues([40, 0, 0, 0, -90, 0])
p2 = JointValues([40, 30, -20, 0, -60, 0])

trajectory = (planner.create_joint_path(start)
    .move_joint(p1, 100, FanucMotion.cnt(50))            # J P[1] 100% CNT50
    .move_joint(p2, 30, FanucMotion.fine(), 50)          # J P[2] 30% FINE ACC50
    .set_io(FanucMotion.signal(IOType.DO, 1), True)      # DO[1]=ON when the robot is at P[2]
    .wait(0.5)                                           # WAIT 0.50(sec)
    .move_joint_time(start, 2.0, FanucMotion.fine())     # back in 2 s
    .build())
```

![Joint positions of this trajectory. J4 and J6 do not move.](https://underautomation.com/fanuc/documentation/diagrams/motion-moves-joint.svg)

| Method | TP equivalent |
| --- | --- |
| `MoveJoint(target, speedPercent, termination, accelerationPercent)` | `J P[1] 50% CNT100 ACC80` |
| `MoveJointTime(target, duration, termination)` | Joint motion in a given time (longer if the limits need it) |
| `Wait(duration)` | `WAIT 0.50(sec)` |
| `SetIO(FanucMotion.Signal(IOType.DO, 1), true)` | `DO[1]=ON` after the previous motion |
| `MoveJointSpline(points, speedPercent, termination)` | Smooth motion through several positions, see [Splines & shapes](motion-splines-shapes.md) |

## Cartesian motions

Linear and circular motions move the tool center point at the given speed in mm/s. The orientation turns progressively from the start orientation to the target orientation.

```python
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.geometry.cartesian_pose import CartesianPose
from underautomation.robotics.geometry.euler_convention import EulerConvention
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

# X, Y, Z, W, P, R: the W, P, R angles of FANUC use the fixed XYZ convention
def wpr(x, y, z, w, p, r):
    return CartesianPose.from_euler(x, y, z, w, p, r, EulerConvention.FixedXYZ)

start = wpr(500, 0, 300, 180, 0, 0)

trajectory = (planner.create_cartesian_path(start)
    .move_linear(wpr(600, 0, 300, 180, 0, 0), 200, FanucMotion.cr(10))       # L 200mm/sec CR10
    .move_linear(wpr(600, 100, 300, 180, 0, 0), 200, FanucMotion.cnt(100))   # L 200mm/sec CNT100
    .move_circular(wpr(550, 150, 300, 180, 0, 0),                            # C via point
                   wpr(500, 100, 300, 180, 0, 30), 150, FanucMotion.fine())  # target, 150mm/sec FINE
    .move_linear_time(start, 1.5, FanucMotion.fine())                        # back in 1.5 s
    .build())

# FANUC positions of the trajectory (W, P, R stay continuous)
samples = FanucMotion.sample_cartesian(trajectory, 0.008)
```

![Path of the tool seen from above, and its speed. Z, W and P do not change.](https://underautomation.com/fanuc/documentation/diagrams/motion-moves-cartesian.svg)

| Method | TP equivalent |
| --- | --- |
| `MoveLinear(target, speed, termination, accelerationPercent)` | `L P[1] 200mm/sec CR10` |
| `MoveCircular(via, target, speed, termination, accelerationPercent)` | `C P[1] P[2] 150mm/sec FINE` |
| `MoveLinearTime(target, duration, termination)` | Linear motion in a given time |

The speed is reduced when the change of orientation, the curvature or the extended axes need it.

## Terminations

| Termination | Behavior |
| --- | --- |
| `FanucMotion.Fine()` | The robot stops at the target |
| `FanucMotion.Cnt(0..100)` | The next motion starts during the deceleration of this one. CNT100 gives the smoothest motion. Joint and Cartesian |
| `FanucMotion.Cr(distance)` | Corner region: the corner is replaced by a smooth curve that starts at this distance (mm) from the target, whatever the speed. Cartesian only, between L and C motions and splines |

These methods return a `Termination` of the planner: `Termination.Stop()`, `Termination.Overlap(percent)` and `Termination.Corner(distance)` give the same result.

![FINE, CNT and CR between two linear motions at 200 mm per second. Top: path near the corner. Bottom: speed.](https://underautomation.com/fanuc/documentation/diagrams/motion-terminations.svg)

With CNT, the size of the rounded corner depends on the speed, as on a FANUC controller:

- Joint motions: the next motion starts during the deceleration of this one. The overlap is reduced automatically when the combination of both motions would exceed the limits.
- Linear and circular motions: the corner is replaced by a smooth curve that starts where the robot would start to decelerate (CNT100), or closer to the target (CNT50: half of this distance).

With CR, the corner geometry is fixed: the curve passes at about 0.12 x distance from the corner for a change of direction of 45 degrees, 0.25 x distance for 90 degrees and 0.4 x distance for 135 degrees. The distance is limited to half of the length of each motion.

In a CNT or CR curve, the speed is constant, and reduced when the curvature needs it: a sharp corner with a small distance is followed slowly. For a fast motion, use a larger CNT or CR distance.

## Tool and user frames

By default, Cartesian positions are flange positions in the world frame. Set `ToolFrame` and `UserFrame` to give the targets as positions of a tool in a user frame, as with UTOOL and UFRAME on the teach pendant:

```python
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.geometry.cartesian_pose import CartesianPose
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

# Targets are positions of this tool, in this user frame
planner.tool_frame = FanucMotion.to_cartesian_pose(XYZWPRPosition(0, 0, 150, 0, 0, 0))      # UTOOL: 150 mm along Z of the flange
planner.user_frame = FanucMotion.to_cartesian_pose(XYZWPRPosition(800, -200, 0, 0, 0, 90))  # UFRAME, relative to the world frame

# The start is the position of the robot (flange in the world frame)
builder = planner.create_cartesian_path(FanucMotion.to_cartesian_pose(XYZWPRPosition(700, 0, 400, 180, 0, 0)))

# end_position gives the same position as a tool position in the user frame
tcp = builder.end_position
target = CartesianPose(tcp.x + 50, tcp.y, tcp.z, tcp.orientation)

# The trajectory gives flange positions in the world frame, ready to send to the robot
trajectory = builder.move_linear(target, 100, FanucMotion.fine()).build()
```

![World frame, user frame, flange and tool center point (TCP).](https://underautomation.com/fanuc/documentation/diagrams/motion-frames.svg)

- The start of `CreateCartesianPath()` is the position of the robot: flange in the world frame, for example `FanucMotion.ToCartesianPose(StreamMotion.QueueEndCartesianPosition)`.
- `EndPosition` gives the end of the motions added so far, in the tool and user frames, as a `CartesianPose`.
- The trajectory gives flange positions in the world frame, ready to send to the robot. The Cartesian limits apply to the tool center point.

## API reference

**JointPathBuilder** ([reference](../api/underautomation.robotics.motion.md#jointpathbuilder))

- `move_joint(target: JointValues, speedPercent: float, termination: Termination, accelerationPercent: float=100) -> 'JointPathBuilder'`: Adds a joint motion: all axes move on a straight line in joint space and arrive at the same time
- `move_joint_time(target: JointValues, duration: float, termination: Termination) -> 'JointPathBuilder'`: Adds a joint motion that lasts a given time. The motion takes more time when the limits do not allow this duration.
- `move_joint_spline(points: typing.List[JointValues], speedPercent: float, termination: Termination, accelerationPercent: float=100) -> 'JointPathBuilder'`: Adds a smooth joint motion that passes through a list of positions (cubic spline) and ends at the last one. The speed changes along the path so that the velocity, acceleration and jerk of each axis stay within the limits. The points must describe a smooth path: close or noisy points give high cur...
- `wait(duration: float) -> 'JointPathBuilder'`: Keeps the current position during a given time
- `set_io(signal: DigitalSignal, value: bool) -> 'JointPathBuilder'`: Writes a digital signal when the previous motion ends
- `build() -> Trajectory`: Creates the trajectory
- `end_position: JointValues (read only)`: Position at the end of the motions added so far

**CartesianPathBuilder** ([reference](../api/underautomation.robotics.motion.md#cartesianpathbuilder))

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

**Termination** ([reference](../api/underautomation.robotics.motion.md#termination))

- `static stop() -> 'Termination'`: The robot stops at the target position
- `static overlap(percent: float) -> 'Termination'`: The next motion starts during the deceleration of this one
- `static corner(distance: float) -> 'Termination'`: Corner region: the corner is replaced by a smooth curve at constant speed. Only between Cartesian motions.
- `type: TerminationType (read only)`: Type of termination
- `value: float (read only)`: Overlap in percent (0 to 100), or corner distance in mm. 0 for a stop.
