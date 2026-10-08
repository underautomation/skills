# Send trajectories

Queue joint or Cartesian trajectories, send your own positions, and control the motion with override, pause and abort.

Web page: https://underautomation.com/fanuc/documentation/stream-motion-trajectories

The easiest way to move the robot with Stream Motion is to give it complete trajectories. The client keeps them in a queue and sends them one after the other, at the communication cycle of the robot.

## Queue trajectories

Create a trajectory with the [motion planner](motion.md), then call `Enqueue()`. It returns an identifier to wait for this motion.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.joints_position import JointsPosition
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.motion.motion_planner import MotionPlanner

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion
sm.start_monitoring()

def on_motion_completed(sender, e):
    print(f"Motion {e.motion_id} completed")

sm.motion_completed(on_motion_completed)

planner = MotionPlanner(sm.joint_limits, None)

# Each trajectory starts where the previous one ends: queue_end_joint_position
home = sm.queue_end_joint_position
values = list(home.values)
values[0] += 15
p1 = JointsPosition(*values)
def move(target):
    # The planner uses its own position type: FanucMotion converts the FANUC positions
    start = FanucMotion.to_joint_values(sm.queue_end_joint_position)
    return planner.create_joint_path(start).move_joint(FanucMotion.to_joint_values(target), 50, FanucMotion.fine()).build()

first = sm.enqueue(move(p1))

values[1] += 10
p2 = JointsPosition(*values)
second = sm.enqueue(move(p2))

back = sm.enqueue(move(home))

# Wait for one motion, or for the whole queue
sm.wait_for_motion(first, 30000)
sm.wait_for_idle(60000)

robot.disconnect()
```

![The three trajectories of this example, played one after the other.](https://underautomation.com/fanuc/documentation/diagrams/stream-motion-queue.svg)

Rules of the queue:

- Each trajectory must start where the previous one ends. Use `QueueEndJointPosition` or `QueueEndCartesianPosition` as start position: when the queue is empty, it is the current position of the robot.
- Trajectories are played one after the other without any change. To join two motions without stop, put them in the same trajectory (CNT, CR or spline).
- All trajectories of a session use the same format, joint or Cartesian. To change the format, finish the session first (see [one format per session](stream-motion-session.md#one_format_per_session)). `ActiveFormat` gives the current format.
- The session starts when the first trajectory is queued and a program waits on `IBGN start`. You can queue trajectories before.

`WaitForMotion()` returns when the robot received the last position of the trajectory, `WaitForIdle()` when the queue is empty and the robot is at rest. The `MotionCompleted` event is raised for each trajectory.

## Cartesian trajectories

Cartesian trajectories work the same way. Give Cartesian limits to the planner, because the robot does not provide them:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.motion.cartesian_limits import CartesianLimits
from underautomation.robotics.motion.motion_planner import MotionPlanner

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion
sm.start_monitoring()

# Cartesian limits are not known by the robot: give yours
cartesian_limits = CartesianLimits(250, 1000, 5000, 45, 180, 900)
planner = MotionPlanner(sm.joint_limits, cartesian_limits)

# Cartesian positions sent to the robot: flange center in the world frame
start = sm.queue_end_cartesian_position
down = XYZWPRPosition(start.x, start.y, start.z - 50, start.w, start.p, start.r)

trajectory = planner.create_cartesian_path(FanucMotion.to_cartesian_pose(start)) \
    .move_linear(FanucMotion.to_cartesian_pose(down), 100, FanucMotion.fine()) \
    .move_linear(FanucMotion.to_cartesian_pose(start), 100, FanucMotion.fine()) \
    .build()

sm.wait_for_motion(sm.enqueue(trajectory), 30000)

robot.disconnect()
```

Good to know:

- The positions are the flange center in the world frame. Some controllers (for example the CRX) expect the position of the active tool: select a tool frame equal to zero, or give the planner the tool of the robot (see [tool and user frames](motion-moves.md#tool_and_user_frames)).
- The robot converts each position into joint positions and checks the joint limits. The SDK cannot check them for Cartesian positions: choose prudent Cartesian limits and validate them on the robot.
- Cartesian positions are always sent in single precision. At 2 ms, changes of orientation can exceed the jerk limit of the wrist because of rounding. Prefer joint trajectories for large changes of orientation.

## Send your own positions

If your application already computes one position per cycle, create the trajectory from these samples. They are sent without any change, so check them first:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
import math
from underautomation.robotics.geometry.joint_values import JointValues
from underautomation.robotics.motion.trajectory import Trajectory

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion
sm.start_monitoring()

# Your own positions, one per communication cycle
cycle = sm.cycle_time
start = sm.queue_end_joint_position
samples = []
count = int(3.0 / cycle)
for i in range(count + 1):
    # J1 +10 degrees with a smooth cosine profile
    s = (1 - math.cos(math.pi * i / count)) / 2
    values = list(start.values)
    values[0] += 10 * s
    samples.append(JointValues(values))
trajectory = Trajectory.from_joint_samples(samples, cycle)

# The positions are sent as they are: check them against the limits of the robot first
report = trajectory.check(sm.joint_limits, cycle, sm.protocol_version == 1)
if not report.is_valid:
    trajectory = trajectory.retime(sm.joint_limits, cycle, sm.protocol_version == 1)

sm.wait_for_motion(sm.enqueue(trajectory), 30000)

robot.disconnect()
```

The period of the samples must be the communication cycle of the robot (`CycleTime`). To give positions at other times, use timed points (see [Trajectories from points](motion-trajectory-from-points.md)).

## Override, pause and abort

The robot runs at 100% override during Stream Motion. The client can slow down the trajectories on their path:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
import time
from underautomation.fanuc.common.joints_position import JointsPosition
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.motion.motion_planner import MotionPlanner

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion
sm.start_monitoring()
planner = MotionPlanner(sm.joint_limits, None)
start = sm.queue_end_joint_position
values = list(start.values)
values[0] += 30
sm.enqueue(planner.create_joint_path(FanucMotion.to_joint_values(start))
           .move_joint(FanucMotion.to_joint_values(JointsPosition(*values)), 10, FanucMotion.fine()).build())

# Slow down the queued trajectories on their path (the robot runs at 100% override)
sm.override = 50

# Stop smoothly on the path, then continue
sm.pause()
time.sleep(2)
sm.resume()

# Stop smoothly on the path and cancel all queued trajectories. The session stays open.
sm.abort()
sm.wait_for_idle(10000)

# The next trajectory starts from the stop position
stopped_at = sm.queue_end_joint_position

robot.disconnect()
```

![Speed and progress on the queued trajectories with Override, Pause(), Resume() and Abort().](https://underautomation.com/fanuc/documentation/diagrams/stream-motion-override.svg)

- `Override` (1 to 100%) changes the speed progressively. The positions are the same, only the time changes.
- `Pause()` stops the robot smoothly on its path. `Resume()` continues.
- `Abort()` stops the robot smoothly on its path, then cancels the current and the queued trajectories. The session stays open.

The HOLD button of the teach pendant is not available during a session: use `Pause()`.

## When the queue is empty

- If the robot is at rest, the client keeps sending the last position and the session stays open.
- If the robot is moving (the trajectories were not queued fast enough), the client stops the robot smoothly within its limits and raises the `Underrun` event.

## API reference

**Trajectory** ([reference](../api/underautomation.robotics.motion.md#trajectory))

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
