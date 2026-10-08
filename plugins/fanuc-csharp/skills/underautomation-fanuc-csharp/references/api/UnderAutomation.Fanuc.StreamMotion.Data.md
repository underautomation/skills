# UnderAutomation.Fanuc.StreamMotion.Data

## IOType (robot.StreamMotion.LastStatus.ReadIOType)

`enum IOType : byte`

I/O types supported by Stream Motion protocol

- DI: Digital Input
- DO: Digital Output
- F: Flag
- M: Marker
- None: No I/O operation
- RI: Robot Input
- RO: Robot Output
- SI: System Input
- SO: System Output
- UI: User Input
- UO: User Output
- WI: Weld Input
- WO: Weld Output
- WSI: Weld System Input
- WSO: Weld System Output

## IOValue

`class IOValue`

State of 16 consecutive I/O read by Stream Motion

- `int Age { get; }`: Number of status received since this value was read. -1 if it was never read.
- `bool GetState(int index)`: Returns the state of one I/O of the range
- `int Index { get; }`: Index of the first I/O of the range
- `const int RangeSize = 16`: Number of I/O read in one range
- `IOType Type { get; }`: I/O type
- `int Value { get; }`: State of the 16 I/O. Bit 0 is the I/O at IOValue.Index.

## LimitTable

`class LimitTable`

Table of allowable limits of one axis for one type of limit. The limit depends on the speed of the flange center: the table gives 20 values, for speeds up to 1/20, 2/20, ... 20/20 of LimitTable.MaxSpeed, with no payload and with the maximum payload.

- `int Axis { get; }`: Axis number (1 to 9)
- `double GetValue(double flangeSpeed, double payload, double maxPayload)`: Computes the limit for a given flange speed and payload, as the robot does when $STMO_GRP[1].$LMT_MODE is 0: linear interpolation between the speed stages (the first stage applies below Vmax/20, and values are extrapolated above Vmax), then linear interpolation between no payload and maximum payl...
- `double IntermediateCheckTime { get; }`: Time interval of the intermediate check of the limits, in seconds
- `bool IsAxisPresent { get; }`: Indicates if the axis exists (at least one value is not 0)
- `double[] MaxPayload { get; }`: Limits with the maximum payload, for flange speeds up to 1/20, 2/20, ... 20/20 of LimitTable.MaxSpeed (20 values)
- `double MaxSpeed { get; }`: Maximum speed of the flange center (Vmax, system variable $STMO_GRP[1].$MAX_SPD), in mm/s
- `double[] NoPayload { get; }`: Limits with no payload, for flange speeds up to 1/20, 2/20, ... 20/20 of LimitTable.MaxSpeed (20 values)
- `double ReferenceValue { get; }`: Reference limit: value with the maximum payload at the maximum speed. It is the value of the system variables $STMO_GRP[1].$JNT_VEL_LIM, $JNT_ACC_LIM or $JNT_JRK_LIM.
- `const int StageCount = 20`: Number of speed stages of a table
- `LimitType Type { get; }`: Type of limit

## MotionEventArgs

`class MotionEventArgs : EventArgs`

Arguments of the motion events

- `int MotionId { get; }`: Identifier of the motion, returned by Enqueue. 0 if there is no motion.

## SessionEndReason

`enum SessionEndReason`

Reason of the end of a Stream Motion session

- Disconnected: The client was disconnected
- Finished: The session was finished normally. The program continues after the IBGN end instruction.
- ProgramStopped: The robot left the IBGN start instruction before the end of the session: program stopped, aborted, or alarm on the robot.
- StatusLost: No status was received from the robot during the configured timeout

## SessionEndedEventArgs

`class SessionEndedEventArgs : SessionEventArgs`

Arguments of the SessionEnded event

- `SessionEndReason Reason { get; }`: Reason of the end of the session
- Inherited from [SessionEventArgs](UnderAutomation.Fanuc.StreamMotion.Data.md#sessioneventargs): `SessionIndex`

## SessionEventArgs

`class SessionEventArgs : EventArgs`

Arguments of the session events

- `int SessionIndex { get; }`: Index of the session since the connection (starts at 1)

## SetpointRequestEventArgs

`class SetpointRequestEventArgs : EventArgs`

Arguments of the SetpointRequested event. Call Common.JointsPosition), Common.XYZWPRPosition) or SetpointRequestEventArgs.Hold to give the next position to send. The object is only valid during the call of the event handler.

- `long CycleIndex { get; }`: Index of the requested position since the start of the callback streaming (starts at 0)
- `void Hold()`: Keeps the last position. If the robot is moving, it stops smoothly.
- `void SetCartesian(XYZWPRPosition position)`: Gives the next Cartesian position to send (flange center in the world frame). The callback streaming must be in Cartesian format. Extended axes values are used when the position is an Common.ExtendedCartesianPosition, otherwise they are 0.
- `void SetJoints(JointsPosition position)`: Gives the next joint position to send. The callback streaming must be in joint format.
- `StreamMotionStatus Status { get; }`: Last status received from the robot
- `double Time { get; }`: Time of the requested position since the start of the callback streaming, in seconds (CycleIndex x cycle time)

## StatusReceivedEventArgs

`class StatusReceivedEventArgs : EventArgs`

Arguments of the StatusReceived event

- `StreamMotionStatus Status { get; }`: Last status received from the robot

## StreamMotionErrorEventArgs

`class StreamMotionErrorEventArgs : EventArgs`

Arguments of the ErrorOccurred event

- `Exception Exception { get; }`: Error that occurred

## StreamMotionLimits (robot.StreamMotion.Limits)

`class StreamMotionLimits`

Allowable velocity, acceleration and jerk limits of the robot axes, read from the robot. The robot stops with an alarm when a position sent to it exceeds these limits.

- `int AxisCount { get; }`: Number of axes of the robot (axes with limits)
- `JointLimits ComputeLimits(double flangeSpeed, double payload, double maxPayload)`: Computes the limits of all axes for a given flange speed and payload, as the robot does when $STMO_GRP[1].$LMT_MODE is 0.
- `LimitTable GetTable(int axis, LimitType type)`: Returns the table of limits of one axis
- `double IntermediateCheckTime { get; }`: Time interval of the intermediate check of the limits, in seconds
- `double MaxSpeed { get; }`: Maximum speed of the flange center (Vmax, system variable $STMO_GRP[1].$MAX_SPD), in mm/s
- `JointLimits ReferenceLimits { get; }`: Reference limits of each axis: values with the maximum payload at the maximum speed. They are equal to the system variables $STMO_GRP[1].$JNT_VEL_LIM, $JNT_ACC_LIM and $JNT_JRK_LIM, and they are always safe.

## StreamMotionState (robot.StreamMotion.State)

`enum StreamMotionState`

State of a Stream Motion client

- Connected: The client is connected but the robot does not send its status (call StartMonitoring)
- Disconnected: The client is not connected
- Finishing: The last position was sent. The client waits for the robot to leave the IBGN start instruction.
- Monitoring: The robot sends its status, but no program is waiting on an IBGN start instruction
- Ready: A program is waiting on an IBGN start instruction and the robot accepts positions
- Streaming: Positions are sent to the robot every communication cycle

## StreamMotionStatistics (robot.StreamMotion.Statistics)

`class StreamMotionStatistics`

Communication statistics of a Stream Motion client, since the status output was started

- `long CatchUpCommandCount { get; }`: Number of extra positions sent to fill the robot buffer again after lost or late status
- `long CommandCount { get; }`: Number of positions sent to the robot
- `int EstimatedBufferLevel { get; }`: Estimated number of positions waiting in the robot buffer
- `long LostStatusCount { get; }`: Number of status sent by the robot but not received (detected with the sequence numbers)
- `double MaxProcessingTime { get; }`: Maximum time spent to process a status and send the positions, in seconds
- `double MaxStatusInterval { get; }`: Maximum time between two received status, measured with the PC clock, in seconds
- `double MeanStatusInterval { get; }`: Mean time between two received status, measured with the PC clock, in seconds
- `long StatusCount { get; }`: Number of status received from the robot
- `long UnderrunCount { get; }`: Number of times the queue became empty while the robot was moving

## StreamMotionStatus (robot.StreamMotion.LastStatus)

`class StreamMotionStatus`

Status sent by the robot every communication cycle

- `ExtendedCartesianPosition CartesianPosition { get; }`: Current Cartesian position of the robot (servo position) in the world frame, with extended axes. It is the flange center, or the tool center point when the system variable $STMO.$STAT_US_TCP is TRUE.
- `bool IsCommandReceived { get; }`: The robot received at least one position during the current IBGN start instruction
- `bool IsMoving { get; }`: The robot is moving
- `bool IsSystemReady { get; }`: System ready (SYSRDY) is ON
- `bool IsWaitingForCommand { get; }`: The robot executes an IBGN start instruction and waits for positions
- `JointsPosition JointPosition { get; }`: Current joint position of the robot (servo position), in degrees (mm for linear axes)
- `double[] MotorCurrents { get; }`: Motor current of each axis, in A (9 values)
- `int OutputDivider { get; }`: With protocol version 3 or later, the robot sends a status once every n communication cycles when it slows down by itself, and this value is n. It is 1 in normal operation and with older protocol versions.
- `int RawStatus { get; }`: Raw status byte
- `int ReadIOIndex { get; }`: Index of the first I/O read in this status
- `int ReadIOMask { get; }`: Mask of the I/O read in this status
- `IOType ReadIOType { get; }`: Type of the I/O read in this status
- `int ReadIOValue { get; }`: State of the 16 I/O read in this status. Bit 0 is the I/O at StreamMotionStatus.ReadIOIndex.
- `long SequenceNumber { get; }`: Sequence number of this status. It starts at 1 when the status output starts.
- `long Timestamp { get; }`: Time stamp of the robot when the position and the motor currents were read, in ms (resolution 2 ms)
