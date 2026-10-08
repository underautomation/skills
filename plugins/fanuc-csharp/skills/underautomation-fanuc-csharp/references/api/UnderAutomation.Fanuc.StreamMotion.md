# UnderAutomation.Fanuc.StreamMotion

## StreamMotionClient

`class StreamMotionClient : StreamMotionClientBase, IDisposable`

Stream Motion client for standalone use (J519 option): real-time control of the robot by sending a position every communication cycle.

- `StreamMotionClient()`: Creates a new Stream Motion client
- `void Connect(string ip, StreamMotionConnectParametersBase parameters = null)`: Connects to the robot. Call StreamMotionClientBase.StartMonitoring next to receive the robot status.
- Inherited from [StreamMotionClientBase](UnderAutomation.Fanuc.StreamMotion.Internal.md#streammotionclientbase-robotstreammotion): `Disconnect`, `StartMonitoring`, `StopMonitoring`, `WaitForReady`, `ReadLimits`, `Enqueue`, `WaitForMotion`, `WaitForIdle`, `Finish`, `Pause`, `Resume`, `Abort`, `StartCallbackStreaming`, `StopCallbackStreaming`, `StartTracking`, `SetJointTrackingTarget`, `SetCartesianTrackingTarget`, `StopTracking`, `AddIOMonitor`, `ClearIOMonitors`, `GetIO`, `WriteIO`, `WriteIOGroup`, `Dispose`, `Ip`, `Port`, `ProtocolVersion`, `Connected`, `State`, `LastStatus`, `CycleTime`, `BufferLead`, `SessionCount`, `Statistics`, `Limits`, `JointLimits`, `CartesianLimits`, `StartTolerance`, `IOAnticipation`, `QueueEndJointPosition`, `QueueEndCartesianPosition`, `QueuedMotionCount`, `IsCallbackStreaming`, `IsTracking`, `HasActiveFormat`, `ActiveFormat`, `Override`, `IsPaused`, `IOValues`, `StatusReceived`, `SessionStarted`, `SessionEnded`, `MotionCompleted`, `Underrun`, `ErrorOccurred`, `SetpointRequested`

## StreamMotionError

`enum StreamMotionError`

Kind of Stream Motion error

- CallbackFailed: The callback did not give a position
- CommunicationError: Error during the communication with the robot
- CycleTimeMismatch: The trajectory was sampled with a period that is not the communication cycle of the robot
- FormatMismatch: The position format does not match the format of the session. A session uses only one format: call Finish(System.Int32) and use the other format in the next session.
- LimitsUnavailable: The robot did not send its limits
- NoStatus: No status was received from the robot
- NotConnected: The client is not connected
- NotMonitoring: The robot status output is not started (call StartMonitoring)
- NotTracking: The target tracking is not started (call StartTracking)
- SessionActive: The operation is not allowed while a session is active
- SessionEnded: The session ended before the end of the operation
- SourceBusy: Another source of positions is active
- StartMismatch: The first position of the trajectory is too far from the position where it starts
- VersionMismatch: The robot uses another protocol version than the one requested

## StreamMotionException

`class StreamMotionException : Exception, ISerializable, _Exception`

Error raised by the Stream Motion client

- `StreamMotionException(StreamMotionError error, string message)`: Creates a Stream Motion exception
- `StreamMotionException(StreamMotionError error, string message, Exception inner)`: Creates a Stream Motion exception with an inner exception
- `StreamMotionError Error { get; }`: Kind of error
