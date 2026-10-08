# underautomation.fanuc.stream_motion

## StreamMotionClient

`from underautomation.fanuc.stream_motion.stream_motion_client import StreamMotionClient`

Stream Motion client for standalone use (J519 option): real-time control of the robot by sending a position every communication cycle.

- `StreamMotionClient()`: Creates a new Stream Motion client
- `connect(ip: str, parameters: StreamMotionConnectParametersBase=None) -> None`: Connects to the robot. Call start_monitoring() next to receive the robot status.
- Inherited from [StreamMotionClientBase](underautomation.fanuc.stream_motion.internal.md#streammotionclientbase-robotstream_motion): `disconnect`, `start_monitoring`, `stop_monitoring`, `wait_for_ready`, `read_limits`, `enqueue`, `wait_for_motion`, `wait_for_idle`, `finish`, `pause`, `resume`, `abort`, `start_callback_streaming`, `stop_callback_streaming`, `start_tracking`, `set_joint_tracking_target`, `set_cartesian_tracking_target`, `stop_tracking`, `add_io_monitor`, `clear_io_monitors`, `get_io`, `write_io`, `write_io_group`, `dispose`, `ip`, `port`, `protocol_version`, `connected`, `state`, `last_status`, `cycle_time`, `buffer_lead`, `session_count`, `statistics`, `limits`, `joint_limits`, `cartesian_limits`, `start_tolerance`, `io_anticipation`, `queue_end_joint_position`, `queue_end_cartesian_position`, `queued_motion_count`, `is_callback_streaming`, `is_tracking`, `has_active_format`, `active_format`, `override`, `is_paused`, `io_values`, `status_received`, `session_started`, `session_ended`, `motion_completed`, `underrun`, `error_occurred`, `setpoint_requested`

## StreamMotionError

`from underautomation.fanuc.stream_motion.stream_motion_error import StreamMotionError`

Kind of Stream Motion error

- NotConnected: The client is not connected
- NotMonitoring: The robot status output is not started (call StartMonitoring)
- NoStatus: No status was received from the robot
- VersionMismatch: The robot uses another protocol version than the one requested
- SessionActive: The operation is not allowed while a session is active
- SourceBusy: Another source of positions is active
- FormatMismatch: The position format does not match the format of the session. A session uses only one format: call finish() and use the other format in the next session.
- CycleTimeMismatch: The trajectory was sampled with a period that is not the communication cycle of the robot
- StartMismatch: The first position of the trajectory is too far from the position where it starts
- LimitsUnavailable: The robot did not send its limits
- SessionEnded: The session ended before the end of the operation
- CallbackFailed: The callback did not give a position
- CommunicationError: Error during the communication with the robot
- NotTracking: The target tracking is not started (call StartTracking)

## StreamMotionException

`from UnderAutomation.Fanuc.StreamMotion import StreamMotionException`

Error raised by the Stream Motion client

The SDK raises this .NET type: catch it with `except StreamMotionException as e` after the import above. Its members keep their .NET names. The class `StreamMotionException` of the module `underautomation.fanuc.stream_motion.stream_motion_exception` is not a Python exception and cannot be caught.

- `Error: StreamMotionError (read only)`: Kind of error
- Inherited from System.Exception: `Message`, `InnerException`
