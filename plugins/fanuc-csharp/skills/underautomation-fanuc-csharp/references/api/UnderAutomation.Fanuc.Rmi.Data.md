# UnderAutomation.Fanuc.Rmi.Data

## RmiCartesianPositionResponse

`class RmiCartesianPositionResponse : RmiTimedResponse`

Result of reading the current Cartesian position.

- `RmiCartesianPositionResponse()`
- `CartesianPositionWithUserFrame Position { get; set; }`: Current TCP position including configuration and active frame/tool numbers.
- Inherited from [RmiTimedResponse](UnderAutomation.Fanuc.Rmi.Data.md#rmitimedresponse): `TimeTag`
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiControllerErrorTextResponse

`class RmiControllerErrorTextResponse : RmiResponseBase`

Result of reading the most recent controller error text.

- `RmiControllerErrorTextResponse()`
- `string ErrorData { get; }`: First error entry, or an empty string when none.
- `string[] ErrorDataEntries { get; set; }`: Error entries in the form XXXX-NNN (up to 5 entries).
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiControllerStatusResponse

`class RmiControllerStatusResponse : RmiResponseBase`

Status snapshot returned by FRC_GetStatus.

- `RmiControllerStatusResponse()`
- `bool CheckSequenceId { get; }`: Indicates the value of $RMI_CFG.$Chk_seqID, which is the configuration value that determines whether the controller checks valid incremented sequence IDs on incoming instructions.
- `int? NextSequenceId { get; set; }`: The next valid sequence ID. This key is only valid if the system variable $RMI_CFG.$Chk_seqID = TRUE
- `byte NumberUFrame { get; set; }`: Number of user frames available in the robot controller
- `byte NumberUTool { get; set; }`: Number of user tools available in the robot controller
- `TaskStatus ProgramStatus { get; set; }`: RMI_MOVE program status
- `bool RmiMotionStatus { get; set; }`: The Remote Motion Interface is running
- `bool ServoReady { get; set; }`: The robot controller is ready for motion
- `bool SingleStepMode { get; set; }`: Single step mode
- `byte SpeedOverride { get; set; }`: The current speed override setting (1–100).
- `bool TPEnabled { get; set; }`: Teach Pendant Enabled (Switch on position ON) The Remote Motion interface only works when the teach pendant is disabled
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiDigitalInputValueResponse

`class RmiDigitalInputValueResponse : RmiResponseBase`

Result of reading a digital input.

- `RmiDigitalInputValueResponse()`
- `short PortNumber { get; set; }`: Port number.
- `RmiOnOff PortValue { get; set; }`: Port value
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiExtendedControllerStatusResponse

`class RmiExtendedControllerStatusResponse : RmiResponseBase`

Extended controller status returned by FRC_GetExtStatus.

- `RmiExtendedControllerStatusResponse()`
- `string ControlMode { get; set; }`: Active control mode string (e.g. "AUTO"), or null when unavailable.
- `bool DrivesPowered { get; set; }`: Whether the servo drives are powered on.
- `string ErrorCode { get; set; }`: Last reported error code text, or null when no error is active.
- `int GenOverride { get; set; }`: General speed override percentage.
- `bool InMotion { get; set; }`: Whether the robot is currently executing a motion.
- `double? SpeedClampLimit { get; set; }`: Speed clamp limit in mm/s, or null when not configured.
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiIndexedFrameResponse

`class RmiIndexedFrameResponse : RmiResponseBase`

Cartesian frame data paired with an index (UFRAME or UTOOL number).

- `RmiIndexedFrameResponse()`
- `XYZWPRPosition Frame { get; set; }`: Frame data.
- `byte Index { get; set; }`: Index (UFRAME or UTOOL number).
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiInitializeResponse

`class RmiInitializeResponse : RmiResponseBase`

Response to the Initialize command, which starts the RMI motion program on the controller.

- `RmiInitializeResponse()`
- `byte? GroupMask { get; set; }`: Motion group mask echoed back by the controller. null when the controller does not return this field (single-group systems or MajorVersion &lt; 2).
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiInstructionResponse

`class RmiInstructionResponse : RmiResponseBase`

Response returned immediately when a motion instruction is queued. The RmiInstructionResponse.Status property and RmiResponseBase.ErrorId are updated in the background as the controller processes the instruction. Use WaitForCompletion(System.Int32) to block until the instruction reaches a termina...

- `RmiInstructionResponse()`
- `RmiInstructionBase Instruction { get; }`: Sent instruction
- `int SequenceId { get; }`: Sequence identifier assigned to this instruction. 0 until the instruction has been dispatched to the controller.
- `RmiInstructionStatus Status { get; }`: Current execution state of the instruction.
- `event Action<RmiInstructionStatus> StatusChanged`: Fired each time RmiInstructionResponse.Status changes. The argument is the new status value. This event may be raised from a background thread.
- `bool WaitForCompletion(int timeoutMs = -1)`: Blocks the calling thread until the instruction reaches a terminal state (RmiInstructionStatus.Completed or RmiInstructionStatus.Error), or until timeoutMs milliseconds have elapsed. Pass -1 (or omit) to wait indefinitely.
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiInstructionStatus

`enum RmiInstructionStatus`

Execution state of an RMI instruction in the pipeline.

- Completed: The instruction completed without error.
- ControllerQueued: The instruction has been sent to the controller and is waiting in its 8-slot execution queue.
- Error: The instruction ended with a controller error or was cancelled. Check RmiResponseBase.ErrorId.
- Executing: The controller is currently executing this instruction.
- LocalQueued: The instruction is held in the local client buffer and has not been sent to the controller yet.

## RmiIoPortType

`enum RmiIoPortType`

IO port type for generic read/write operations.

- AI: Analog Input.
- AO: Analog Output.
- DI: Digital Input.
- DO: Digital Output.
- FLAG: Internal flag register.
- GO: Group Output.
- RI: Robot Input.
- RO: Robot Output.
- UI: User Interface Input.
- UO: User Interface Output.

## RmiIoPortValueResponse

`class RmiIoPortValueResponse : RmiResponseBase`

Result of reading a generic IO port.

- `RmiIoPortValueResponse()`
- `int PortNumber { get; set; }`: Port number.
- `RmiIoPortType PortType { get; set; }`: Port type (DI, DO, AI, AO, GO, etc.).
- `double Value { get; set; }`: Current port value.
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiJointAnglesSampleResponse

`class RmiJointAnglesSampleResponse : RmiTimedResponse`

Result of reading the current joint angles.

- `RmiJointAnglesSampleResponse()`
- `JointsPosition JointAngle { get; set; }`: Joint angle set in degrees.
- Inherited from [RmiTimedResponse](UnderAutomation.Fanuc.Rmi.Data.md#rmitimedresponse): `TimeTag`
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiJointSpeedType

`enum RmiJointSpeedType`

Speed type for joint motion commands.

- MSec: Duration-based speed in milliseconds.
- Percent: Joint speed as a percentage of maximum (1–100 %).
- Time: Duration-based speed (0.1-second units).

## RmiLinearSpeedType

`enum RmiLinearSpeedType`

Speed type for linear and circular motion commands.

- InchMin: Linear speed in inches per minute.
- MSec: Duration-based speed in milliseconds.
- MmSec: Linear speed in millimeters per second.
- Time: Duration-based speed (0.1-second units).

## RmiNumericRegisterValueResponse

`class RmiNumericRegisterValueResponse : RmiResponseBase`

Result of reading a numeric register.

- `RmiNumericRegisterValueResponse()`
- `int RegisterNumber { get; set; }`: Register number.
- `NumericRegister Value { get; set; }`: Register value.
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiOnOff

`enum RmiOnOff`

Generic ON/OFF string values used by RMI.

- OFF: OFF state.
- ON: ON state.

## RmiPltzMode

`enum RmiPltzMode`

Palletizing motion mode passed to Data.RmiPltzMode%7d). Requires MajorVersion &gt;= 7.

- MspiDown: Multi-spine descent.
- MspiUp: Multi-spine ascent.
- PspiDown: Palletizing-spine descent.
- PspiUp: Palletizing-spine ascent.
- ZeroDown: Zero-approach descent.
- ZeroUp: Zero-approach ascent.

## RmiPortType

`enum RmiPortType`

Digital port type used with Local Condition Block (LCB).

- DOUT: Digital Output (DO/DOUT).
- ROUT: Robot Output (RO/ROUT).

## RmiPositionRegisterDataResponse

`class RmiPositionRegisterDataResponse : RmiResponseBase`

Position register data paired with its register number.

- `RmiPositionRegisterDataResponse()`
- `CartesianPositionWithUserFrame CartesianPosition { get; set; }`: Position register value.
- `short RegisterNumber { get; set; }`: Register number
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiRecordedCartesianPosition

`class RmiRecordedCartesianPosition`

Cartesian position received from the controller via the RMI Position Record menu (TouchUp).

- `RmiRecordedCartesianPosition()`
- `CartesianPositionWithUserFrame Position { get; set; }`: Recorded Cartesian position including arm configuration and active frame/tool numbers.
- `ushort PositionId { get; set; }`: Position identifier assigned by the controller.

## RmiRecordedJointPosition

`class RmiRecordedJointPosition`

Joint position received from the controller via the RMI Position Record menu (TouchUp).

- `RmiRecordedJointPosition()`
- `JointsPosition Joints { get; set; }`: Recorded joint angles in degrees.
- `ushort PositionId { get; set; }`: Position identifier assigned by the controller.

## RmiResponseBase

`class RmiResponseBase`

Base class for RMI responses that return an error id from the controller.

- `RmiResponseBase()`
- `int ErrorId { get; set; }`: Error identifier. 0 means success; non-zero indicates a controller error.
- `string ErrorText { get; }`: Human-readable description of RmiResponseBase.ErrorId. Empty string when there is no error.

## RmiSetPayloadCompensationParameters

`class RmiSetPayloadCompensationParameters`

Parameters for defining payload compensation for a payload schedule. Used by Data.RmiSetPayloadCompensationParameters). All positional values are in meters; mass in kg; inertia in kg·m².

- `RmiSetPayloadCompensationParameters()`
- `float CgXm { get; set; }`: Center-of-gravity X offset in meters.
- `float CgYm { get; set; }`: Center-of-gravity Y offset in meters.
- `float CgZm { get; set; }`: Center-of-gravity Z offset in meters.
- `byte? Group { get; set; }`: Optional motion group number. null uses the active group.
- `float InertiaXkgm2 { get; set; }`: Inertia around the X axis in kg·m².
- `float InertiaYkgm2 { get; set; }`: Inertia around the Y axis in kg·m².
- `float InertiaZkgm2 { get; set; }`: Inertia around the Z axis in kg·m².
- `float MassKg { get; set; }`: Payload mass in kilograms.
- `byte ScheduleNumber { get; set; }`: Payload schedule number to configure.

## RmiSetPayloadParameters

`class RmiSetPayloadParameters`

Parameters for defining payload mass, center of gravity, and optionally inertia for a payload schedule. Used by Data.RmiSetPayloadParameters). All positional values are in meters; mass in kg; inertia in kg·m².

- `RmiSetPayloadParameters()`
- `float CgXm { get; set; }`: Center-of-gravity X offset in meters.
- `float CgYm { get; set; }`: Center-of-gravity Y offset in meters.
- `float CgZm { get; set; }`: Center-of-gravity Z offset in meters.
- `byte? Group { get; set; }`: Optional motion group number. null uses the active group.
- `float? InertiaXkgm2 { get; set; }`: Inertia around the X axis in kg·m². null omits this field from the command.
- `float? InertiaYkgm2 { get; set; }`: Inertia around the Y axis in kg·m². null omits this field from the command.
- `float? InertiaZkgm2 { get; set; }`: Inertia around the Z axis in kg·m². null omits this field from the command.
- `float MassKg { get; set; }`: Payload mass in kilograms.
- `byte ScheduleNumber { get; set; }`: Payload schedule number to configure.

## RmiTcpSpeedResponse

`class RmiTcpSpeedResponse : RmiTimedResponse`

Result of reading TCP speed.

- `RmiTcpSpeedResponse()`
- `double Speed { get; set; }`: Current tool center point speed in mm/s.
- Inherited from [RmiTimedResponse](UnderAutomation.Fanuc.Rmi.Data.md#rmitimedresponse): `TimeTag`
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiTerminationType

`enum RmiTerminationType`

Termination type for motion.

- Cnt: Continuous termination; blend motions (1-100).
- Cr: Constant path mode (requires option).
- Fine: FINE termination; precise stop.

## RmiTimedResponse

`class RmiTimedResponse : RmiResponseBase`

Base class for responses with a controller RmiTimedResponse.TimeTag value.

- `RmiTimedResponse()`
- `int TimeTag { get; set; }`: Controller time tick for the data sample.
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiUFrameUToolNumbersResponse

`class RmiUFrameUToolNumbersResponse : RmiResponseBase`

Current UFRAME and UTOOL numbers, optionally scoped to a motion group.

- `RmiUFrameUToolNumbersResponse()`
- `byte Frame { get; set; }`: Current user frame number.
- `byte? Group { get; set; }`: Motion group number, or null when not applicable.
- `byte Tool { get; set; }`: Current user tool number.
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

## RmiVariableValueResponse

`class RmiVariableValueResponse : RmiResponseBase`

Result of reading a system variable.

- `RmiVariableValueResponse()`
- `int IntegerValue { get; set; }`: Gets or sets the value as an integer. Internally stored as a double.
- `bool IsInteger { get; set; }`: Whether the variable holds a floating-point value.
- `string Name { get; set; }`: Variable name, including the leading $ character.
- `double RealValue { get; set; }`: Gets or sets the value as a double-precision floating-point number.
- Inherited from [RmiResponseBase](UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`
