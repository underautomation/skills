# I/O during motion

Read and write digital I/O with each position sent to the robot, and switch outputs at a precise point of a trajectory.

Web page: https://underautomation.com/fanuc/documentation/stream-motion-io

Each position sent to the robot can also read a range of I/O and write I/O. This gives I/O synchronized with the motion, without another protocol. I/O are only read and written during a session.

## Read I/O

Add the ranges of I/O to read. A range is 16 consecutive I/O. Each position reads one range, so several ranges are read one after the other.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.stream_motion.data.io_type import IOType

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion
sm.start_monitoring()

# Ranges of 16 I/O read during the session (one range per position sent)
sm.add_io_monitor(IOType.DI, 1)    # DI[1] to DI[16]
sm.add_io_monitor(IOType.DO, 17)   # DO[17] to DO[32]

# ... later, during the session
di3 = sm.get_io(IOType.DI, 3)
for io_range in sm.io_values:
    print(f"{io_range.type.name}[{io_range.index}..{io_range.index + 15}] = {io_range.value} (age {io_range.age} cycles)")

robot.disconnect()
```

`GetIO()` returns false while the range was never read. `Age` gives the number of cycles since the last reading of the range.

## Write I/O

Write an I/O immediately with `WriteIO()`, or up to 16 consecutive I/O with `WriteIOGroup()`. To switch an I/O at a precise point of the motion, add it to the trajectory:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.joints_position import JointsPosition
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.fanuc.stream_motion.data.io_type import IOType
from underautomation.robotics.motion.motion_planner import MotionPlanner

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion
sm.start_monitoring()
planner = MotionPlanner(sm.joint_limits, None)

# Write immediately, with the next position sent
sm.write_io(IOType.DO, 1, True)
sm.write_io_group(IOType.DO, 9, 0x000F, 0x0005)   # DO[9] and DO[11] ON, DO[10] and DO[12] OFF

# Write at a precise point of a trajectory
start = sm.queue_end_joint_position
values = list(start.values)
values[0] += 20
target = JointsPosition(*values)
trajectory = planner.create_joint_path(FanucMotion.to_joint_values(start)) \
    .move_joint(FanucMotion.to_joint_values(target), 30, FanucMotion.fine()) \
    .set_io(FanucMotion.signal(IOType.DO, 2), True) \
    .move_joint(FanucMotion.to_joint_values(start), 30, FanucMotion.fine()) \
    .build()
trajectory.add_io_event(0.5, FanucMotion.signal(IOType.DO, 3), True)   # 0.5 s after the start of the trajectory

# Compensate the delay between the position sent and the real motion
sm.io_anticipation = 0.03
sm.wait_for_motion(sm.enqueue(trajectory), 30000)

robot.disconnect()
```

![When each output of this example is written, compared to the motion of J1.](https://underautomation.com/fanuc/documentation/diagrams/stream-motion-io.svg)

- `SetIO()` in a path builder writes the I/O when the previous motion ends. Create the signal with `FanucMotion.Signal(IOType.DO, 2)`.
- `AddIOEvent()` writes the I/O at a given time of the trajectory.
- `IOAnticipation` sends the I/O events earlier, to compensate the delay between the position sent and the real motion of the robot.

Writing an I/O that is not assigned raises an alarm on the robot (PRIO-023).

## Supported I/O types

| `IOType` | I/O |
| --- | --- |
| `DI`, `DO` | Digital inputs and outputs |
| `RI`, `RO` | Robot inputs and outputs |
| `SI`, `SO` | System inputs and outputs |
| `UI`, `UO` | User operator panel inputs and outputs |
| `WI`, `WO`, `WSI`, `WSO` | Weld inputs and outputs |
| `F` | Flags |
| `M` | Markers |

## API reference

**IOValue** ([reference](../api/underautomation.fanuc.stream_motion.data.md#iovalue))

- `get_state(index: int) -> bool`: Returns the state of one I/O of the range
- `type: IOType (read only)`: I/O type
- `index: int (read only)`: Index of the first I/O of the range
- `value: int (read only)`: State of the 16 I/O. Bit 0 is the I/O at index.
- `age: int (read only)`: Number of status received since this value was read. -1 if it was never read.
- `static RangeSize: int`: Number of I/O read in one range
