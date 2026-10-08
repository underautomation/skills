# Stream Motion overview

Stream Motion (J519 option) gives the position of the robot at every communication cycle (2 to 8 ms). Requirements, TP program, protocol versions and quick start.

Web page: https://underautomation.com/fanuc/documentation/stream-motion

Stream Motion (option **J519**) lets an external application give the position of the robot at every communication cycle (2, 4 or 8 ms depending on the controller). The robot follows these positions in real time. Typical uses:

- trajectories computed outside the robot (path planning, CAD/CAM, simulation)
- sensor guided motion: vision, force sensor, seam tracking
- teleoperation with a joystick or a haptic device

The SDK does the real-time part for you: it synchronizes the positions with the status of the robot, keeps a few positions in advance, stops the robot smoothly if your application stops giving positions, and provides a motion planner that respects the velocity, acceleration and jerk limits of the robot.

## Stream Motion or RMI?

| Need | Use |
| --- | --- |
| Send a few moves (J, L, C) and let the robot plan them | [RMI](rmi.md) |
| Follow a path or a target that changes in real time | Stream Motion |
| Control the position at every cycle (2 to 8 ms) | Stream Motion |

## Requirements on the robot

- Option **J519 Stream Motion**. Check it with `Features.HasStreamMotion` ([FTP diagnostics](ftp-diagnostics.md)).
- A TP program with the instructions `IBGN start[n]` and `IBGN end[n]` (see below), run in **AUTO** mode at **100% override**.
- `$PARAM_GROUP[1].$SV_OFF_ENB[*]` set to `FALSE`, otherwise the robot raises MOTN-615.
- Resume offset disabled, otherwise the robot raises MOTN-623.
- Only motion group 1 is controlled (robot and up to 3 extended axes).
- The robot listens on UDP port 60015 on the Ethernet port set in `$STMO.$PHYS_PORT`.

## TP program

The robot only accepts positions while a program waits on `IBGN start[n]`. When your application finishes the session, the program continues after `IBGN end[n]`. This program loops, so each loop is a new session:

```plaintext
/PROG  START_STREAM_MOTION_J519
/ATTR
OWNER		= MNEDITOR;
PROTECT		= READ_WRITE;
TCD:  STACK_SIZE	= 0,
      TASK_PRIORITY	= 50,
      TIME_SLICE	= 0,
      BUSY_LAMP_OFF	= 0,
      ABORT_REQUEST	= 0,
      PAUSE_REQUEST	= 0;
DEFAULT_GROUP	= 1,*,*,*,*;
CONTROL_CODE	= 00000000 00000000;
/MN
   1:  LBL[1] ;
   2:  IBGN start[1] ;
   3:  IBGN end[1] ;
   4:  JMP LBL[1] ;
/POS
/END
```

You can add your own instructions before `IBGN start` or after `IBGN end`, for example to set an output or to wait for a signal. The program can be started from the teach pendant, or remotely (see [Run a program remotely](run-program-remotely.md)).

`IBGN start` and `IBGN end` instructions are located in the `ASCII INTERFACE` section of the TP program editor. If you don't see this section, please ensure J519 Stream Motion is enabled.

![Add IBGN Start and End Instructions to TP Program](https://underautomation.com/fanuc/documentation/add-tp-program-ibgn-start-end.gif)

## Quick start

This example moves J1 by 10 degrees and back, with a smooth motion planned within the limits of the robot:

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

# Read the limits of the robot and start to receive its status
sm.start_monitoring()

# Plan a smooth joint motion: J1 +10 degrees then back, at 20% of the velocity limits
start = sm.queue_end_joint_position
values = list(start.values)
values[0] += 10
target = JointsPosition(*values)
planner = MotionPlanner(sm.joint_limits, None)
trajectory = planner.create_joint_path(FanucMotion.to_joint_values(start)) \
    .move_joint(FanucMotion.to_joint_values(target), 20, FanucMotion.cnt(100)) \
    .move_joint(FanucMotion.to_joint_values(start), 20, FanucMotion.fine()) \
    .build()

# The motion starts when the TP program reaches IBGN start
motion_id = sm.enqueue(trajectory)
sm.wait_for_motion(motion_id, 60000)

# Release the TP program: it continues after IBGN end
sm.finish(10000)

robot.disconnect()
```

![J1 during this trajectory, relative to its start position.](https://underautomation.com/fanuc/documentation/diagrams/stream-motion-quick-start.svg)

## Try it in the demo application

The [demo application](demo-app.md) (Windows) has a Stream Motion page to test this feature without writing code.

Connect to your robot or to a ROBOGUIDE virtual robot, start the monitoring, then run the TP program described above. Once the robot reaches `IBGN start`, a session starts and the page shows:

- the client state, the cycle time measured on the robot, the protocol version and the number of active sessions
- the robot status at each cycle: joint and Cartesian position, and whether the robot is moving
- two demo motions built with the motion planner: a joint move of J1 back and forth, and a horizontal circle in Cartesian space
- pause, resume, abort and override applied to the current session
- a log of the sessions and motions, with counters for lost status messages and underruns

![Stream Motion page of the Showcase demo application](https://underautomation.com/fanuc/documentation/demo-stream-motion-showcase-forms.gif)

The C# source of this page is in the `StreamMotionControl.cs` file of the [Fanuc.NET repository](https://github.com/underautomation/Fanuc.NET/blob/main/UnderAutomation.Fanuc.Showcase.Forms/Components/StreamMotionControl.cs).

## How it works

1. `StartMonitoring()` reads the limits of the robot, starts the status output of the robot and measures the communication cycle.
2. When the TP program reaches `IBGN start`, the client state becomes `Ready`.
3. As soon as positions are available, a session starts. Positions come from one source at a time:
   - a **queue of trajectories** (`Enqueue`), see [Send trajectories](stream-motion-trajectories.md)
   - a **target** that the robot follows (`StartTracking`), see [Real-time control](stream-motion-real-time.md)
   - your own **callback**, called at each cycle (`StartCallbackStreaming`)
4. `Finish()` waits until the robot is at rest, then the TP program continues after `IBGN end`.

Trajectories are created with the motion planner of the SDK, described in the [Motion](motion.md) section.

During a session, the robot sends its status at every cycle and the SDK answers with the next position. The positions are sent a little in advance (`BufferLeadTime`), so that a late answer of the PC does not stop the robot:

![Exchange between the robot and the SDK at each communication cycle, with 3 cycles of BufferLeadTime.](https://underautomation.com/fanuc/documentation/diagrams/stream-motion-cycle.svg)

## Protocol versions

Set the version in `ConnectionParameters.StreamMotion.ProtocolVersion`. It must not be higher than the system variable `$STMO.$USABLE_VER` (this variable does not exist on older software, which only support version 1).

| Version | Difference |
| --- | --- |
| 1 (default) | Supported by all controllers. Positions are sent in single precision. |
| 2 | Joint positions are sent in double precision. Recommended for joint motions when available. |
| 3 | The robot can slow down its status output during an automatic stop. Handled by the SDK. |

A version 4 exists on some recent controllers for ROS 2 only. It is not supported.

## Useful system variables

| Variable | Description |
| --- | --- |
| `$STMO.$USABLE_VER` | Highest protocol version of the controller |
| `$STMO.$COM_INT` | Theoretical communication cycle (the SDK measures the real one) |
| `$STMO.$PKT_STACK` | Size of the position buffer of the robot. Use the same value for `PacketStackSize` |
| `$STMO.$START_MOVE` | Number of positions received before the robot starts to move. Keep it low (default 1) |
| `$STMO.$PHYS_PORT` | Ethernet port used by Stream Motion |
| `$STMO.$THRS_ABNPOS` | Threshold of the abnormal position alarm (MOTN-625) |
| `$STMO_GRP[1].$FLTR_LN` | Filter applied by the robot to the positions: smoother motion, with a small delay |
| `$STMO_GRP[1].$JNT_VEL_LIM`, `$JNT_ACC_LIM`, `$JNT_JRK_LIM` | Reference limits of each axis, also given by `ReadLimits()` |
| `$MCR.$GENOVERRIDE` | General override, must be 100 |

These variables can be read with [CGTP, SNPX or Telnet](read-write-system-variables.md).

## Next steps

- [Connection, status & session](stream-motion-session.md): connect, read the status and the limits, run several sessions.
- [Send trajectories](stream-motion-trajectories.md): queue trajectories, override, pause and abort.
- [Real-time control](stream-motion-real-time.md): follow a target, or compute each position.
- [I/O during motion](stream-motion-io.md): read and write I/O synchronized with the motion.
- [Troubleshooting](stream-motion-troubleshooting.md): alarms and best practices.

## API reference

**StreamMotionClientBase** ([reference](../api/underautomation.fanuc.stream_motion.internal.md#streammotionclientbase-robotstream_motion))

- `status_received(handler)`: Raised when a status is received. It is raised on a dedicated thread and only with the latest status: if the handler is slow, some status are skipped.
- `session_started(handler)`: Raised when a session starts (first position sent after an IBGN start instruction)
- `session_ended(handler)`: Raised when a session ends
- `motion_completed(handler)`: Raised when the robot received the last position of a queued trajectory
- `underrun(handler)`: Raised when the queue becomes empty while the robot is moving. The robot is then stopped smoothly.
- `error_occurred(handler)`: Raised when an error occurs in the communication thread
- `setpoint_requested(handler)`: Raised in callback streaming mode (see start_callback_streaming()) each time a position must be sent. The handler must give the next position with SetJoints or SetCartesian. It runs on the communication thread, a few cycles before the robot executes the position, and must return quickly. The firs...
- `disconnect() -> None`: Disconnects from the robot. If a session is active, the robot is stopped smoothly and the session is finished first.
- `start_monitoring() -> None`: Starts the status output of the robot. The robot then sends its status every communication cycle. The limits of the robot are read first when they are not known yet, and this method returns when the communication cycle is measured.
- `stop_monitoring() -> None`: Stops the status output of the robot. Not allowed during a session: call finish() first.
- `wait_for_ready(timeoutMs: int) -> bool`: Waits until a program executes an IBGN start instruction and the robot accepts positions.
- `read_limits() -> StreamMotionLimits`: Reads the velocity, acceleration and jerk limits of all axes from the robot. The status output is stopped during the reading and started again. Some controllers do not answer while a program waits on an IBGN start instruction: read the limits before. Not allowed during a session.
- `enqueue(trajectory: Trajectory) -> int`: Adds a trajectory at the end of the queue. The session starts automatically when the robot accepts positions, and the trajectories are sent one after the other, without any change between them.
- `wait_for_motion(motionId: int, timeoutMs: int) -> bool`: Waits until the robot received the last position of a queued trajectory
- `wait_for_idle(timeoutMs: int) -> bool`: Waits until the queue is empty and the robot does not move. During target tracking, waits until the robot is stopped on the target.
- `finish(timeoutMs: int) -> bool`: Finishes the session when the queue is empty and the robot is at rest: the last position is sent with the end flag, and the program continues after the IBGN end instruction. If a program waits on IBGN start without session, it is released at the current position. The callback streaming and the ta...
- `pause() -> None`: Stops smoothly on the path of the current trajectory. The queue is kept and resume() continues the motion. Use it instead of a HOLD, which is not available during Stream Motion.
- `resume() -> None`: Continues the queued trajectories after pause()
- `abort() -> None`: Stops smoothly on the path of the current trajectory, then cancels the current and the queued trajectories. The session stays open and the robot keeps its position. The callback streaming and the target tracking are stopped, and the robot stops as fast as the limits allow.
- `start_callback_streaming(format: PositionFormat) -> None`: Starts to take the positions from the setpoint_requested event instead of the queue. The session starts automatically when the robot accepts positions.
- `stop_callback_streaming() -> None`: Stops the callback streaming. The last position is kept, and the robot stops smoothly if it was moving.
- `start_tracking(format: PositionFormat, speedPercent: float=100, accelerationPercent: float=100) -> None`: Starts to follow a target position: the robot goes to the last target given by set_joint_tracking_target() or set_cartesian_tracking_target() as fast as the limits allow, and stops on it. The target can change at any time, even during the motion: the robot then goes smoothly to the new target. Th...
- `set_joint_tracking_target(target: JointsPosition) -> None`: Gives a new joint target to follow (see start_tracking())
- `set_cartesian_tracking_target(target: XYZWPRPosition) -> None`: Gives a new Cartesian target to follow (see start_tracking()). Extended axes are used when the target is an ExtendedCartesianPosition, otherwise they keep their target.
- `stop_tracking() -> None`: Stops the target tracking. If the robot was moving, it stops as fast as the limits allow, then it keeps its position.
- `add_io_monitor(type: IOType, index: int) -> None`: Adds a range of 16 consecutive I/O to read. Each position sent to the robot reads one range, so several ranges are read one after the other. Values are only read during a session.
- `clear_io_monitors() -> None`: Removes all ranges of I/O to read
- `get_io(type: IOType, index: int) -> bool`: Returns the last read state of one I/O. The I/O must be in a range added with add_io_monitor(). It returns false while the range was never read.
- `write_io(type: IOType, index: int, value: bool) -> None`: Writes one digital I/O with the next position sent to the robot (only during a session)
- `write_io_group(type: IOType, index: int, mask: int, value: int) -> None`: Writes up to 16 consecutive digital I/O with the next position sent to the robot (only during a session)
- `dispose() -> None`: Disconnects and releases the resources
- `ip: str (read only)`: IP address of the robot
- `port: int (read only)`: UDP port of the robot
- `protocol_version: int (read only)`: Protocol version used by this client
- `connected: bool (read only)`: Indicates whether the client is connected
- `state: StreamMotionState (read only)`: Current state of the client
- `last_status: StreamMotionStatus (read only)`: Last status received from the robot, or null if no status was received
- `cycle_time: float (read only)`: Communication cycle of the robot measured from the status, in seconds (for example 0.008 or 0.002). 0 while it is not known. Trajectories are sampled at this period.
- `buffer_lead: int (read only)`: Number of positions sent in advance and kept in the robot buffer during the current session
- `session_count: int (read only)`: Number of sessions started since the connection. A session starts when positions are sent after an IBGN start instruction.
- `statistics: StreamMotionStatistics (read only)`: Communication statistics since the status output was started
- `limits: StreamMotionLimits (read only)`: Limits read from the robot by read_limits() or when the status output starts. Null if they were not read.
- `joint_limits: JointLimits`: Joint limits used to stop the robot smoothly when the positions stop in joint format. It is set to the reference limits of the robot when the limits are read.
- `cartesian_limits: CartesianLimits`: Cartesian limits used to stop the robot smoothly when the positions stop in Cartesian format. When it is null, conservative values are used.
- `start_tolerance: float`: Maximum distance between the first position of a trajectory and the position where it starts, in mm or degrees (default 0.01).
- `io_anticipation: float`: Time in seconds by which the I/O events of trajectories are sent before their position (default 0). It compensates the delay between the reception of a position by the robot and the real motion.
- `queue_end_joint_position: JointsPosition (read only)`: Position where the next queued joint trajectory must start: end of the queue, or current position when the queue is empty. Null if no status was received.
- `queue_end_cartesian_position: ExtendedCartesianPosition (read only)`: Position where the next queued Cartesian trajectory must start: end of the queue, or last position sent when the queue is empty. Before any Cartesian position was sent, it is the Cartesian position of the status (flange center in the world frame by default). Some controllers expect Cartesian posi...
- `queued_motion_count: int (read only)`: Number of trajectories waiting or running
- `is_callback_streaming: bool (read only)`: Indicates if positions are given by the setpoint_requested event
- `is_tracking: bool (read only)`: Indicates if the robot follows a target given by set_joint_tracking_target() or set_cartesian_tracking_target()
- `has_active_format: bool (read only)`: Indicates if the format of the positions is fixed. A session uses only one format, chosen by the first queued trajectory, start_tracking() or start_callback_streaming(). While this is true, positions in the other format throw a StreamMotionException with FormatMismatch. It becomes false when the...
- `active_format: PositionFormat (read only)`: Format of the positions of the current session or of the queued trajectories. Only valid when has_active_format is true.
- `override: float`: Speed of the queued trajectories in percent (greater than 0, up to 100, default 100). The robot itself must run at 100% override, so this value slows down the trajectories on their path: the positions are the same, only the time is stretched. A change is applied progressively.
- `is_paused: bool (read only)`: Indicates if the queued trajectories are paused
- `io_values: typing.List[IOValue] (read only)`: Last values of the ranges of I/O added with add_io_monitor()
