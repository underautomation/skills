# underautomation.fanuc.stream_motion.internal

## StreamMotionClientBase (robot.stream_motion)

`from underautomation.fanuc.stream_motion.internal.stream_motion_client_base import StreamMotionClientBase`

Stream Motion client (J519 option): real-time control of the robot by sending a position every communication cycle.

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

## StreamMotionClientInternal (robot.stream_motion)

`from underautomation.fanuc.stream_motion.internal.stream_motion_client_internal import StreamMotionClientInternal`

Stream Motion client used by FanucRobot

- Inherited from [StreamMotionClientBase](underautomation.fanuc.stream_motion.internal.md#streammotionclientbase-robotstream_motion): `disconnect`, `start_monitoring`, `stop_monitoring`, `wait_for_ready`, `read_limits`, `enqueue`, `wait_for_motion`, `wait_for_idle`, `finish`, `pause`, `resume`, `abort`, `start_callback_streaming`, `stop_callback_streaming`, `start_tracking`, `set_joint_tracking_target`, `set_cartesian_tracking_target`, `stop_tracking`, `add_io_monitor`, `clear_io_monitors`, `get_io`, `write_io`, `write_io_group`, `dispose`, `ip`, `port`, `protocol_version`, `connected`, `state`, `last_status`, `cycle_time`, `buffer_lead`, `session_count`, `statistics`, `limits`, `joint_limits`, `cartesian_limits`, `start_tolerance`, `io_anticipation`, `queue_end_joint_position`, `queue_end_cartesian_position`, `queued_motion_count`, `is_callback_streaming`, `is_tracking`, `has_active_format`, `active_format`, `override`, `is_paused`, `io_values`, `status_received`, `session_started`, `session_ended`, `motion_completed`, `underrun`, `error_occurred`, `setpoint_requested`

## StreamMotionConnectParametersBase

`from underautomation.fanuc.stream_motion.internal.stream_motion_connect_parameters_base import StreamMotionConnectParametersBase`

Connection parameters for Stream Motion (J519 option)

- `StreamMotionConnectParametersBase()`
- `port: int`: UDP port of the robot for Stream Motion
- `protocol_version: int`: Protocol version, from 1 to 3. The highest version accepted by a controller is in the system variable $STMO.$USABLE_VER. A higher version raises an alarm on the robot and no status is received. Version 2 sends joint positions in double precision. Version 3 lets the robot send its status less ofte...
- `buffer_lead_time: float`: Time of positions sent in advance and kept in the robot buffer, in seconds. It protects against late packets from the PC, but adds the same delay to the motion. It is converted to a number of communication cycles, limited by packet_stack_size minus 2. 0 disables the advance.
- `packet_stack_size: int`: Size of the robot buffer. It must be equal to the system variable $STMO.$PKT_STACK of the robot (2 to 10).
- `status_timeout_ms: int`: Maximum time without status from the robot before the connection is considered lost, in milliseconds
- `high_priority: bool`: Runs the communication thread with a high priority to reduce delays (default: true)
- `static DEFAULT_PORT: int`: Default UDP port of the robot for Stream Motion
- `static DEFAULT_PROTOCOL_VERSION: int`: Default protocol version. Version 1 is accepted by all controllers.
- `static DEFAULT_BUFFER_LEAD_TIME: float`: Default time of positions kept in advance in the robot buffer, in seconds
- `static DEFAULT_PACKET_STACK_SIZE: int`: Default size of the robot buffer (default value of the system variable $STMO.$PKT_STACK)
- `static DEFAULT_STATUS_TIMEOUT_MS: int`: Default maximum time without status from the robot, in milliseconds
