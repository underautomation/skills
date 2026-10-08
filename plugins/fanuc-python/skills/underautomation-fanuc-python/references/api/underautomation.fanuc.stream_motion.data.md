# underautomation.fanuc.stream_motion.data

## IOType (robot.stream_motion.last_status.read_io_type)

`from underautomation.fanuc.stream_motion.data.io_type import IOType`

I/O types supported by Stream Motion protocol

- None_: No I/O operation
- DI: Digital Input
- DO: Digital Output
- RI: Robot Input
- RO: Robot Output
- SI: System Input
- SO: System Output
- WI: Weld Input
- WO: Weld Output
- UI: User Input
- UO: User Output
- WSI: Weld System Input
- WSO: Weld System Output
- F: Flag
- M: Marker

## IOValue

`from underautomation.fanuc.stream_motion.data.io_value import IOValue`

State of 16 consecutive I/O read by Stream Motion

- `get_state(index: int) -> bool`: Returns the state of one I/O of the range
- `type: IOType (read only)`: I/O type
- `index: int (read only)`: Index of the first I/O of the range
- `value: int (read only)`: State of the 16 I/O. Bit 0 is the I/O at index.
- `age: int (read only)`: Number of status received since this value was read. -1 if it was never read.
- `static RangeSize: int`: Number of I/O read in one range

## LimitTable

`from underautomation.fanuc.stream_motion.data.limit_table import LimitTable`

Table of allowable limits of one axis for one type of limit. The limit depends on the speed of the flange center: the table gives 20 values, for speeds up to 1/20, 2/20, ... 20/20 of max_speed, with no payload and with the maximum payload.

- `get_value(flangeSpeed: float, payload: float, maxPayload: float) -> float`: Computes the limit for a given flange speed and payload, as the robot does when $STMO_GRP[1].$LMT_MODE is 0: linear interpolation between the speed stages (the first stage applies below Vmax/20, and values are extrapolated above Vmax), then linear interpolation between no payload and maximum payl...
- `axis: int (read only)`: Axis number (1 to 9)
- `type: LimitType (read only)`: Type of limit
- `max_speed: float (read only)`: Maximum speed of the flange center (Vmax, system variable $STMO_GRP[1].$MAX_SPD), in mm/s
- `intermediate_check_time: float (read only)`: Time interval of the intermediate check of the limits, in seconds
- `no_payload: typing.List[float] (read only)`: Limits with no payload, for flange speeds up to 1/20, 2/20, ... 20/20 of max_speed (20 values)
- `max_payload: typing.List[float] (read only)`: Limits with the maximum payload, for flange speeds up to 1/20, 2/20, ... 20/20 of max_speed (20 values)
- `reference_value: float (read only)`: Reference limit: value with the maximum payload at the maximum speed. It is the value of the system variables $STMO_GRP[1].$JNT_VEL_LIM, $JNT_ACC_LIM or $JNT_JRK_LIM.
- `is_axis_present: bool (read only)`: Indicates if the axis exists (at least one value is not 0)
- `static StageCount: int`: Number of speed stages of a table

## MotionEventArgs

`from underautomation.fanuc.stream_motion.data.motion_event_args import MotionEventArgs`

Arguments of the motion events

- `motion_id: int (read only)`: Identifier of the motion, returned by Enqueue. 0 if there is no motion.

## SessionEndReason

`from underautomation.fanuc.stream_motion.data.session_end_reason import SessionEndReason`

Reason of the end of a Stream Motion session

- Finished: The session was finished normally. The program continues after the IBGN end instruction.
- ProgramStopped: The robot left the IBGN start instruction before the end of the session: program stopped, aborted, or alarm on the robot.
- StatusLost: No status was received from the robot during the configured timeout
- Disconnected: The client was disconnected

## SessionEndedEventArgs

`from underautomation.fanuc.stream_motion.data.session_ended_event_args import SessionEndedEventArgs`

Arguments of the SessionEnded event

- `reason: SessionEndReason (read only)`: Reason of the end of the session
- Inherited from [SessionEventArgs](underautomation.fanuc.stream_motion.data.md#sessioneventargs): `session_index`

## SessionEventArgs

`from underautomation.fanuc.stream_motion.data.session_event_args import SessionEventArgs`

Arguments of the session events

- `session_index: int (read only)`: Index of the session since the connection (starts at 1)

## SetpointRequestEventArgs

`from underautomation.fanuc.stream_motion.data.setpoint_request_event_args import SetpointRequestEventArgs`

Arguments of the SetpointRequested event. Call set_joints(), set_cartesian() or hold() to give the next position to send. The object is only valid during the call of the event handler.

- `set_joints(position: JointsPosition) -> None`: Gives the next joint position to send. The callback streaming must be in joint format.
- `set_cartesian(position: XYZWPRPosition) -> None`: Gives the next Cartesian position to send (flange center in the world frame). The callback streaming must be in Cartesian format. Extended axes values are used when the position is an ExtendedCartesianPosition, otherwise they are 0.
- `hold() -> None`: Keeps the last position. If the robot is moving, it stops smoothly.
- `status: StreamMotionStatus (read only)`: Last status received from the robot
- `cycle_index: int (read only)`: Index of the requested position since the start of the callback streaming (starts at 0)
- `time: float (read only)`: Time of the requested position since the start of the callback streaming, in seconds (CycleIndex x cycle time)

## StatusReceivedEventArgs

`from underautomation.fanuc.stream_motion.data.status_received_event_args import StatusReceivedEventArgs`

Arguments of the StatusReceived event

- `status: StreamMotionStatus (read only)`: Last status received from the robot

## StreamMotionErrorEventArgs

`from underautomation.fanuc.stream_motion.data.stream_motion_error_event_args import StreamMotionErrorEventArgs`

Arguments of the ErrorOccurred event

- `exception: typing.Any (read only)`: Error that occurred

## StreamMotionLimits (robot.stream_motion.limits)

`from underautomation.fanuc.stream_motion.data.stream_motion_limits import StreamMotionLimits`

Allowable velocity, acceleration and jerk limits of the robot axes, read from the robot. The robot stops with an alarm when a position sent to it exceeds these limits.

- `get_table(axis: int, type: LimitType) -> LimitTable`: Returns the table of limits of one axis
- `compute_limits(flangeSpeed: float, payload: float, maxPayload: float) -> JointLimits`: Computes the limits of all axes for a given flange speed and payload, as the robot does when $STMO_GRP[1].$LMT_MODE is 0.
- `axis_count: int (read only)`: Number of axes of the robot (axes with limits)
- `max_speed: float (read only)`: Maximum speed of the flange center (Vmax, system variable $STMO_GRP[1].$MAX_SPD), in mm/s
- `intermediate_check_time: float (read only)`: Time interval of the intermediate check of the limits, in seconds
- `reference_limits: JointLimits (read only)`: Reference limits of each axis: values with the maximum payload at the maximum speed. They are equal to the system variables $STMO_GRP[1].$JNT_VEL_LIM, $JNT_ACC_LIM and $JNT_JRK_LIM, and they are always safe.

## StreamMotionState (robot.stream_motion.state)

`from underautomation.fanuc.stream_motion.data.stream_motion_state import StreamMotionState`

State of a Stream Motion client

- Disconnected: The client is not connected
- Connected: The client is connected but the robot does not send its status (call StartMonitoring)
- Monitoring: The robot sends its status, but no program is waiting on an IBGN start instruction
- Ready: A program is waiting on an IBGN start instruction and the robot accepts positions
- Streaming: Positions are sent to the robot every communication cycle
- Finishing: The last position was sent. The client waits for the robot to leave the IBGN start instruction.

## StreamMotionStatistics (robot.stream_motion.statistics)

`from underautomation.fanuc.stream_motion.data.stream_motion_statistics import StreamMotionStatistics`

Communication statistics of a Stream Motion client, since the status output was started

- `status_count: int (read only)`: Number of status received from the robot
- `lost_status_count: int (read only)`: Number of status sent by the robot but not received (detected with the sequence numbers)
- `command_count: int (read only)`: Number of positions sent to the robot
- `catch_up_command_count: int (read only)`: Number of extra positions sent to fill the robot buffer again after lost or late status
- `underrun_count: int (read only)`: Number of times the queue became empty while the robot was moving
- `estimated_buffer_level: int (read only)`: Estimated number of positions waiting in the robot buffer
- `mean_status_interval: float (read only)`: Mean time between two received status, measured with the PC clock, in seconds
- `max_status_interval: float (read only)`: Maximum time between two received status, measured with the PC clock, in seconds
- `max_processing_time: float (read only)`: Maximum time spent to process a status and send the positions, in seconds

## StreamMotionStatus (robot.stream_motion.last_status)

`from underautomation.fanuc.stream_motion.data.stream_motion_status import StreamMotionStatus`

Status sent by the robot every communication cycle

- `sequence_number: int (read only)`: Sequence number of this status. It starts at 1 when the status output starts.
- `timestamp: int (read only)`: Time stamp of the robot when the position and the motor currents were read, in ms (resolution 2 ms)
- `raw_status: int (read only)`: Raw status byte
- `is_waiting_for_command: bool (read only)`: The robot executes an IBGN start instruction and waits for positions
- `is_command_received: bool (read only)`: The robot received at least one position during the current IBGN start instruction
- `is_system_ready: bool (read only)`: System ready (SYSRDY) is ON
- `is_moving: bool (read only)`: The robot is moving
- `output_divider: int (read only)`: With protocol version 3 or later, the robot sends a status once every n communication cycles when it slows down by itself, and this value is n. It is 1 in normal operation and with older protocol versions.
- `joint_position: JointsPosition (read only)`: Current joint position of the robot (servo position), in degrees (mm for linear axes)
- `cartesian_position: ExtendedCartesianPosition (read only)`: Current Cartesian position of the robot (servo position) in the world frame, with extended axes. It is the flange center, or the tool center point when the system variable $STMO.$STAT_US_TCP is TRUE.
- `motor_currents: typing.List[float] (read only)`: Motor current of each axis, in A (9 values)
- `read_io_type: IOType (read only)`: Type of the I/O read in this status
- `read_io_index: int (read only)`: Index of the first I/O read in this status
- `read_io_mask: int (read only)`: Mask of the I/O read in this status
- `read_io_value: int (read only)`: State of the 16 I/O read in this status. Bit 0 is the I/O at read_io_index.
