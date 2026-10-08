# UnderAutomation.Fanuc.StreamMotion.Internal

## StreamMotionClientBase (robot.StreamMotion)

`abstract class StreamMotionClientBase : IDisposable`

Stream Motion client (J519 option): real-time control of the robot by sending a position every communication cycle.

- `void Abort()`: Stops smoothly on the path of the current trajectory, then cancels the current and the queued trajectories. The session stays open and the robot keeps its position. The callback streaming and the target tracking are stopped, and the robot stops as fast as the limits allow.
- `PositionFormat ActiveFormat { get; }`: Format of the positions of the current session or of the queued trajectories. Only valid when StreamMotionClientBase.HasActiveFormat is true.
- `void AddIOMonitor(IOType type, int index)`: Adds a range of 16 consecutive I/O to read. Each position sent to the robot reads one range, so several ranges are read one after the other. Values are only read during a session.
- `int BufferLead { get; }`: Number of positions sent in advance and kept in the robot buffer during the current session
- `CartesianLimits CartesianLimits { get; set; }`: Cartesian limits used to stop the robot smoothly when the positions stop in Cartesian format. When it is null, conservative values are used.
- `void ClearIOMonitors()`: Removes all ranges of I/O to read
- `bool Connected { get; }`: Indicates whether the client is connected
- `double CycleTime { get; }`: Communication cycle of the robot measured from the status, in seconds (for example 0.008 or 0.002). 0 while it is not known. Trajectories are sampled at this period.
- `void Disconnect()`: Disconnects from the robot. If a session is active, the robot is stopped smoothly and the session is finished first.
- `void Dispose()`: Disconnects and releases the resources
- `int Enqueue(Trajectory trajectory)`: Adds a trajectory at the end of the queue. The session starts automatically when the robot accepts positions, and the trajectories are sent one after the other, without any change between them.
- `event EventHandler<StreamMotionErrorEventArgs> ErrorOccurred`: Raised when an error occurs in the communication thread
- `bool Finish(int timeoutMs)`: Finishes the session when the queue is empty and the robot is at rest: the last position is sent with the end flag, and the program continues after the IBGN end instruction. If a program waits on IBGN start without session, it is released at the current position. The callback streaming and the ta...
- `bool GetIO(IOType type, int index)`: Returns the last read state of one I/O. The I/O must be in a range added with IOType%2cSystem.Int32). It returns false while the range was never read.
- `bool HasActiveFormat { get; }`: Indicates if the format of the positions is fixed. A session uses only one format, chosen by the first queued trajectory, Double%2cSystem.Double) or Motion.PositionFormat). While this is true, positions in the other format throw a StreamMotion.StreamMotionException with StreamMotionError.FormatMi...
- `double IOAnticipation { get; set; }`: Time in seconds by which the I/O events of trajectories are sent before their position (default 0). It compensates the delay between the reception of a position by the robot and the real motion.
- `IOValue[] IOValues { get; }`: Last values of the ranges of I/O added with IOType%2cSystem.Int32)
- `string Ip { get; }`: IP address of the robot
- `bool IsCallbackStreaming { get; }`: Indicates if positions are given by the StreamMotionClientBase.SetpointRequested event
- `bool IsPaused { get; }`: Indicates if the queued trajectories are paused
- `bool IsTracking { get; }`: Indicates if the robot follows a target given by Common.JointsPosition) or Common.XYZWPRPosition)
- `JointLimits JointLimits { get; set; }`: Joint limits used to stop the robot smoothly when the positions stop in joint format. It is set to the reference limits of the robot when the limits are read.
- `StreamMotionStatus LastStatus { get; }`: Last status received from the robot, or null if no status was received
- `StreamMotionLimits Limits { get; }`: Limits read from the robot by StreamMotionClientBase.ReadLimits or when the status output starts. Null if they were not read.
- `event EventHandler<MotionEventArgs> MotionCompleted`: Raised when the robot received the last position of a queued trajectory
- `double Override { get; set; }`: Speed of the queued trajectories in percent (greater than 0, up to 100, default 100). The robot itself must run at 100% override, so this value slows down the trajectories on their path: the positions are the same, only the time is stretched. A change is applied progressively.
- `void Pause()`: Stops smoothly on the path of the current trajectory. The queue is kept and StreamMotionClientBase.Resume continues the motion. Use it instead of a HOLD, which is not available during Stream Motion.
- `int Port { get; }`: UDP port of the robot
- `int ProtocolVersion { get; }`: Protocol version used by this client
- `ExtendedCartesianPosition QueueEndCartesianPosition { get; }`: Position where the next queued Cartesian trajectory must start: end of the queue, or last position sent when the queue is empty. Before any Cartesian position was sent, it is the Cartesian position of the status (flange center in the world frame by default). Some controllers expect Cartesian posi...
- `JointsPosition QueueEndJointPosition { get; }`: Position where the next queued joint trajectory must start: end of the queue, or current position when the queue is empty. Null if no status was received.
- `int QueuedMotionCount { get; }`: Number of trajectories waiting or running
- `StreamMotionLimits ReadLimits()`: Reads the velocity, acceleration and jerk limits of all axes from the robot. The status output is stopped during the reading and started again. Some controllers do not answer while a program waits on an IBGN start instruction: read the limits before. Not allowed during a session.
- `void Resume()`: Continues the queued trajectories after StreamMotionClientBase.Pause
- `int SessionCount { get; }`: Number of sessions started since the connection. A session starts when positions are sent after an IBGN start instruction.
- `event EventHandler<SessionEndedEventArgs> SessionEnded`: Raised when a session ends
- `event EventHandler<SessionEventArgs> SessionStarted`: Raised when a session starts (first position sent after an IBGN start instruction)
- `void SetCartesianTrackingTarget(XYZWPRPosition target)`: Gives a new Cartesian target to follow (see Double%2cSystem.Double)). Extended axes are used when the target is an Common.ExtendedCartesianPosition, otherwise they keep their target.
- `void SetJointTrackingTarget(JointsPosition target)`: Gives a new joint target to follow (see Double%2cSystem.Double))
- `event EventHandler<SetpointRequestEventArgs> SetpointRequested`: Raised in callback streaming mode (see Motion.PositionFormat)) each time a position must be sent. The handler must give the next position with SetJoints or SetCartesian. It runs on the communication thread, a few cycles before the robot executes the position, and must return quickly. The first re...
- `void StartCallbackStreaming(PositionFormat format)`: Starts to take the positions from the StreamMotionClientBase.SetpointRequested event instead of the queue. The session starts automatically when the robot accepts positions.
- `void StartMonitoring()`: Starts the status output of the robot. The robot then sends its status every communication cycle. The limits of the robot are read first when they are not known yet, and this method returns when the communication cycle is measured.
- `double StartTolerance { get; set; }`: Maximum distance between the first position of a trajectory and the position where it starts, in mm or degrees (default 0.01).
- `void StartTracking(PositionFormat format, double speedPercent = 100, double accelerationPercent = 100)`: Starts to follow a target position: the robot goes to the last target given by Common.JointsPosition) or Common.XYZWPRPosition) as fast as the limits allow, and stops on it. The target can change at any time, even during the motion: the robot then goes smoothly to the new target. The limits are S...
- `StreamMotionState State { get; }`: Current state of the client
- `StreamMotionStatistics Statistics { get; }`: Communication statistics since the status output was started
- `event EventHandler<StatusReceivedEventArgs> StatusReceived`: Raised when a status is received. It is raised on a dedicated thread and only with the latest status: if the handler is slow, some status are skipped.
- `void StopCallbackStreaming()`: Stops the callback streaming. The last position is kept, and the robot stops smoothly if it was moving.
- `void StopMonitoring()`: Stops the status output of the robot. Not allowed during a session: call Finish(System.Int32) first.
- `void StopTracking()`: Stops the target tracking. If the robot was moving, it stops as fast as the limits allow, then it keeps its position.
- `event EventHandler<MotionEventArgs> Underrun`: Raised when the queue becomes empty while the robot is moving. The robot is then stopped smoothly.
- `bool WaitForIdle(int timeoutMs)`: Waits until the queue is empty and the robot does not move. During target tracking, waits until the robot is stopped on the target.
- `bool WaitForMotion(int motionId, int timeoutMs)`: Waits until the robot received the last position of a queued trajectory
- `bool WaitForReady(int timeoutMs)`: Waits until a program executes an IBGN start instruction and the robot accepts positions.
- `void WriteIO(IOType type, int index, bool value)`: Writes one digital I/O with the next position sent to the robot (only during a session)
- `void WriteIOGroup(IOType type, int index, int mask, int value)`: Writes up to 16 consecutive digital I/O with the next position sent to the robot (only during a session)

## StreamMotionClientInternal (robot.StreamMotion)

`class StreamMotionClientInternal : StreamMotionClientBase, IDisposable`

Stream Motion client used by Fanuc.FanucRobot

- Inherited from [StreamMotionClientBase](UnderAutomation.Fanuc.StreamMotion.Internal.md#streammotionclientbase-robotstreammotion): `Disconnect`, `StartMonitoring`, `StopMonitoring`, `WaitForReady`, `ReadLimits`, `Enqueue`, `WaitForMotion`, `WaitForIdle`, `Finish`, `Pause`, `Resume`, `Abort`, `StartCallbackStreaming`, `StopCallbackStreaming`, `StartTracking`, `SetJointTrackingTarget`, `SetCartesianTrackingTarget`, `StopTracking`, `AddIOMonitor`, `ClearIOMonitors`, `GetIO`, `WriteIO`, `WriteIOGroup`, `Dispose`, `Ip`, `Port`, `ProtocolVersion`, `Connected`, `State`, `LastStatus`, `CycleTime`, `BufferLead`, `SessionCount`, `Statistics`, `Limits`, `JointLimits`, `CartesianLimits`, `StartTolerance`, `IOAnticipation`, `QueueEndJointPosition`, `QueueEndCartesianPosition`, `QueuedMotionCount`, `IsCallbackStreaming`, `IsTracking`, `HasActiveFormat`, `ActiveFormat`, `Override`, `IsPaused`, `IOValues`, `StatusReceived`, `SessionStarted`, `SessionEnded`, `MotionCompleted`, `Underrun`, `ErrorOccurred`, `SetpointRequested`

## StreamMotionConnectParametersBase

`class StreamMotionConnectParametersBase`

Connection parameters for Stream Motion (J519 option)

- `StreamMotionConnectParametersBase()`
- `double BufferLeadTime { get; set; }`: Time of positions sent in advance and kept in the robot buffer, in seconds. It protects against late packets from the PC, but adds the same delay to the motion. It is converted to a number of communication cycles, limited by StreamMotionConnectParametersBase.PacketStackSize minus 2. 0 disables th...
- `const double DEFAULT_BUFFER_LEAD_TIME = 0.024`: Default time of positions kept in advance in the robot buffer, in seconds
- `const int DEFAULT_PACKET_STACK_SIZE = 10`: Default size of the robot buffer (default value of the system variable $STMO.$PKT_STACK)
- `const int DEFAULT_PORT = 60015`: Default UDP port of the robot for Stream Motion
- `const int DEFAULT_PROTOCOL_VERSION = 1`: Default protocol version. Version 1 is accepted by all controllers.
- `const int DEFAULT_STATUS_TIMEOUT_MS = 1000`: Default maximum time without status from the robot, in milliseconds
- `bool HighPriority { get; set; }`: Runs the communication thread with a high priority to reduce delays (default: true)
- `int PacketStackSize { get; set; }`: Size of the robot buffer. It must be equal to the system variable $STMO.$PKT_STACK of the robot (2 to 10).
- `int Port { get; set; }`: UDP port of the robot for Stream Motion
- `int ProtocolVersion { get; set; }`: Protocol version, from 1 to 3. The highest version accepted by a controller is in the system variable $STMO.$USABLE_VER. A higher version raises an alarm on the robot and no status is received. Version 2 sends joint positions in double precision. Version 3 lets the robot send its status less ofte...
- `int StatusTimeoutMs { get; set; }`: Maximum time without status from the robot before the connection is considered lost, in milliseconds
