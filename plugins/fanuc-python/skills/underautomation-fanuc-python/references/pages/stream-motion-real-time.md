# Real-time control

Make the robot follow a target that changes at any time, or compute the position of the robot at every cycle with a callback.

Web page: https://underautomation.com/fanuc/documentation/stream-motion-real-time

When the motion is not known in advance, for example with a camera, a force sensor or a joystick, the robot must react to new data while it moves. Stream Motion offers two ways to do this.

| Need | Use |
| --- | --- |
| The robot goes to a target that changes at any time | Target tracking |
| Your application computes the position at every cycle | Callback streaming |

## Follow a target

With target tracking, the robot goes to the last target as fast as the limits allow, and stops on it. You can change the target at any time, from any thread, even during the motion: the robot then goes smoothly to the new target.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
import time
from underautomation.fanuc.common.joints_position import JointsPosition
from underautomation.robotics.motion.position_format import PositionFormat

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion
sm.start_monitoring()

# The robot follows a target at 30% of its velocity limits
sm.start_tracking(PositionFormat.Joint, 30)

# Change the target at any time, from any thread
start = sm.queue_end_joint_position
values = list(start.values)
values[0] = start.j1 + 10
sm.set_joint_tracking_target(JointsPosition(*values))
time.sleep(0.5)
values[0] = start.j1 - 5
sm.set_joint_tracking_target(JointsPosition(*values))

# Wait until the robot is stopped on the target
sm.wait_for_idle(10000)

# Stop following targets. A moving robot stops as fast as the limits allow.
sm.stop_tracking()

robot.disconnect()
```

![J1 with this example: the target changes during the motion, and the robot turns back smoothly within its limits.](https://underautomation.com/fanuc/documentation/diagrams/stream-motion-tracking.svg)

- The limits are `JointLimits` of the client (read from the robot by `StartMonitoring()`), scaled by the speed and acceleration percentages of `StartTracking()`.
- The first target is the current position. The robot does not move before the first call to `SetJointTrackingTarget()`.
- Each axis moves on its own, so the path to the target is not a straight line.
- `WaitForIdle()` returns when the robot is stopped on the target.
- The delay between a new target and the start of the motion is about `BufferLeadTime` plus the delay of the robot. Reduce `BufferLeadTime` in the connection parameters for a faster reaction.

### Follow a Cartesian target

Set `CartesianLimits` before starting a Cartesian tracking. The linear limits are shared between X, Y and Z, and the angular limits between the 3 rotation axes.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition
from underautomation.robotics.motion.cartesian_limits import CartesianLimits
from underautomation.robotics.motion.position_format import PositionFormat

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion
sm.start_monitoring()

# Cartesian tracking needs Cartesian limits
sm.cartesian_limits = CartesianLimits(250, 1000, 5000, 45, 180, 900)
sm.start_tracking(PositionFormat.Cartesian, 50, 50)

# For example, a target given by a sensor
start = sm.queue_end_cartesian_position
sm.set_cartesian_tracking_target(XYZWPRPosition(start.x + 20, start.y, start.z - 10, start.w, start.p, start.r))
sm.wait_for_idle(10000)

sm.stop_tracking()

robot.disconnect()
```

## Compute each position

With callback streaming, the `SetpointRequested` event asks your application for the next position at every cycle. Give it with `SetJoints()` or `SetCartesian()`:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
import math
import time
from underautomation.fanuc.common.joints_position import JointsPosition
from underautomation.robotics.motion.position_format import PositionFormat

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion
sm.start_monitoring()

start = sm.queue_end_joint_position

# Called on the communication thread, a few cycles before the robot uses the position
def on_setpoint(sender, e):
    # e.time: time of this position since the start, in seconds
    values = list(start.values)
    values[0] += 5 * (1 - math.cos(2 * math.pi * e.time / 4)) / 2
    e.set_joints(JointsPosition(*values))

sm.setpoint_requested(on_setpoint)

sm.start_callback_streaming(PositionFormat.Joint)
time.sleep(8)

# The robot keeps its last position, or stops smoothly if it was moving
sm.stop_callback_streaming()

robot.disconnect()
```

Rules of the callback:

- The event runs on the communication thread, a few cycles before the robot uses the position. It must return quickly, in less than one cycle.
- The first position (`CycleIndex` 0) must be the current position of the robot, and the next positions must respect the limits of the robot. Use [Check](motion-trajectory-from-points.md#check_a_trajectory) on recorded positions to validate your algorithm.
- If the handler throws an exception or gives no position, the robot keeps its position, or stops smoothly if it was moving, and `ErrorOccurred` is raised. Call `Hold()` to keep the position on purpose.
- With Python, the callback works, but its timing depends on the interpreter: prefer target tracking.

Only one source of positions is active at a time: the queue, the target tracking or the callback. `Abort()`, `Finish()` and the end of the session stop the target tracking and the callback streaming.

The format given to `StartTracking()` or `StartCallbackStreaming()` must be the format of the current session. To use the other format, call `Finish()` and start in the next session (see [one format per session](stream-motion-session.md#one_format_per_session)).
