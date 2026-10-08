# underautomation.fanuc.rmi.data

## RmiCartesianPositionResponse

`from underautomation.fanuc.rmi.data.rmi_cartesian_position_response import RmiCartesianPositionResponse`

Result of reading the current Cartesian position.

- `RmiCartesianPositionResponse()`
- `position: CartesianPositionWithUserFrame`: Current TCP position including configuration and active frame/tool numbers.
- Inherited from [RmiTimedResponse](underautomation.fanuc.rmi.data.md#rmitimedresponse): `time_tag`
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiControllerErrorTextResponse

`from underautomation.fanuc.rmi.data.rmi_controller_error_text_response import RmiControllerErrorTextResponse`

Result of reading the most recent controller error text.

- `RmiControllerErrorTextResponse()`
- `error_data_entries: typing.List[str]`: Error entries in the form XXXX-NNN (up to 5 entries).
- `error_data: str (read only)`: First error entry, or an empty string when none.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiControllerStatusResponse

`from underautomation.fanuc.rmi.data.rmi_controller_status_response import RmiControllerStatusResponse`

Status snapshot returned by FRC_GetStatus.

- `RmiControllerStatusResponse()`
- `servo_ready: bool`: The robot controller is ready for motion
- `tp_enabled: bool`: Teach Pendant Enabled (Switch on position ON) The Remote Motion interface only works when the teach pendant is disabled
- `rmi_motion_status: bool`: The Remote Motion Interface is running
- `program_status: TaskStatus`: RMI_MOVE program status
- `single_step_mode: bool`: Single step mode
- `number_u_tool: int`: Number of user tools available in the robot controller
- `next_sequence_id: int | None`: The next valid sequence ID. This key is only valid if the system variable $RMI_CFG.$Chk_seqID = TRUE
- `number_u_frame: int`: Number of user frames available in the robot controller
- `speed_override: int`: The current speed override setting (1–100).
- `check_sequence_id: bool (read only)`: Indicates the value of $RMI_CFG.$Chk_seqID, which is the configuration value that determines whether the controller checks valid incremented sequence IDs on incoming instructions.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiDigitalInputValueResponse

`from underautomation.fanuc.rmi.data.rmi_digital_input_value_response import RmiDigitalInputValueResponse`

Result of reading a digital input.

- `RmiDigitalInputValueResponse()`
- `port_number: int`: Port number.
- `port_value: RmiOnOff`: Port value
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiExtendedControllerStatusResponse

`from underautomation.fanuc.rmi.data.rmi_extended_controller_status_response import RmiExtendedControllerStatusResponse`

Extended controller status returned by FRC_GetExtStatus.

- `RmiExtendedControllerStatusResponse()`
- `error_code: str`: Last reported error code text, or null when no error is active.
- `in_motion: bool`: Whether the robot is currently executing a motion.
- `control_mode: str`: Active control mode string (e.g. "AUTO"), or null when unavailable.
- `drives_powered: bool`: Whether the servo drives are powered on.
- `gen_override: int`: General speed override percentage.
- `speed_clamp_limit: float | None`: Speed clamp limit in mm/s, or null when not configured.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiIndexedFrameResponse

`from underautomation.fanuc.rmi.data.rmi_indexed_frame_response import RmiIndexedFrameResponse`

Cartesian frame data paired with an index (UFRAME or UTOOL number).

- `RmiIndexedFrameResponse()`
- `index: int`: Index (UFRAME or UTOOL number).
- `frame: XYZWPRPosition`: Frame data.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiInitializeResponse

`from underautomation.fanuc.rmi.data.rmi_initialize_response import RmiInitializeResponse`

Response to the Initialize command, which starts the RMI motion program on the controller.

- `RmiInitializeResponse()`
- `group_mask: int | None`: Motion group mask echoed back by the controller. null when the controller does not return this field (single-group systems or MajorVersion < 2).
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiInstructionResponse

`from underautomation.fanuc.rmi.data.rmi_instruction_response import RmiInstructionResponse`

Response returned immediately when a motion instruction is queued. The status property and error_id are updated in the background as the controller processes the instruction. Use wait_for_completion() to block until the instruction reaches a terminal state.

- `RmiInstructionResponse()`
- `status_changed(handler)`: Fired each time status changes. The argument is the new status value. This event may be raised from a background thread.
- `wait_for_completion(timeoutMs: int=-1) -> bool`: Blocks the calling thread until the instruction reaches a terminal state (Completed or Error), or until timeoutMs milliseconds have elapsed. Pass -1 (or omit) to wait indefinitely.
- `sequence_id: int (read only)`: Sequence identifier assigned to this instruction. 0 until the instruction has been dispatched to the controller.
- `status: RmiInstructionStatus (read only)`: Current execution state of the instruction.
- `instruction: RmiInstructionBase (read only)`: Sent instruction
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiInstructionStatus

`from underautomation.fanuc.rmi.data.rmi_instruction_status import RmiInstructionStatus`

Execution state of an RMI instruction in the pipeline.

- LocalQueued: The instruction is held in the local client buffer and has not been sent to the controller yet.
- ControllerQueued: The instruction has been sent to the controller and is waiting in its 8-slot execution queue.
- Executing: The controller is currently executing this instruction.
- Completed: The instruction completed without error.
- Error: The instruction ended with a controller error or was cancelled. Check error_id.

## RmiIoPortType

`from underautomation.fanuc.rmi.data.rmi_io_port_type import RmiIoPortType`

IO port type for generic read/write operations.

- DI: Digital Input.
- DO: Digital Output.
- AI: Analog Input.
- AO: Analog Output.
- GO: Group Output.
- RO: Robot Output.
- FLAG: Internal flag register.
- RI: Robot Input.
- UI: User Interface Input.
- UO: User Interface Output.

## RmiIoPortValueResponse

`from underautomation.fanuc.rmi.data.rmi_io_port_value_response import RmiIoPortValueResponse`

Result of reading a generic IO port.

- `RmiIoPortValueResponse()`
- `port_type: RmiIoPortType`: Port type (DI, DO, AI, AO, GO, etc.).
- `port_number: int`: Port number.
- `value: float`: Current port value.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiJointAnglesSampleResponse

`from underautomation.fanuc.rmi.data.rmi_joint_angles_sample_response import RmiJointAnglesSampleResponse`

Result of reading the current joint angles.

- `RmiJointAnglesSampleResponse()`
- `joint_angle: JointsPosition`: Joint angle set in degrees.
- Inherited from [RmiTimedResponse](underautomation.fanuc.rmi.data.md#rmitimedresponse): `time_tag`
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiJointSpeedType

`from underautomation.fanuc.rmi.data.rmi_joint_speed_type import RmiJointSpeedType`

Speed type for joint motion commands.

- Percent: Joint speed as a percentage of maximum (1–100 %).
- Time: Duration-based speed (0.1-second units).
- MSec: Duration-based speed in milliseconds.

## RmiLinearSpeedType

`from underautomation.fanuc.rmi.data.rmi_linear_speed_type import RmiLinearSpeedType`

Speed type for linear and circular motion commands.

- MmSec: Linear speed in millimeters per second.
- InchMin: Linear speed in inches per minute.
- Time: Duration-based speed (0.1-second units).
- MSec: Duration-based speed in milliseconds.

## RmiNumericRegisterValueResponse

`from underautomation.fanuc.rmi.data.rmi_numeric_register_value_response import RmiNumericRegisterValueResponse`

Result of reading a numeric register.

- `RmiNumericRegisterValueResponse()`
- `register_number: int`: Register number.
- `value: NumericRegister`: Register value.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiOnOff

`from underautomation.fanuc.rmi.data.rmi_on_off import RmiOnOff`

Generic ON/OFF string values used by RMI.

- OFF: OFF state.
- ON: ON state.

## RmiPltzMode

`from underautomation.fanuc.rmi.data.rmi_pltz_mode import RmiPltzMode`

Palletizing motion mode passed to initialize(). Requires MajorVersion >= 7.

- ZeroDown: Zero-approach descent.
- ZeroUp: Zero-approach ascent.
- PspiDown: Palletizing-spine descent.
- PspiUp: Palletizing-spine ascent.
- MspiDown: Multi-spine descent.
- MspiUp: Multi-spine ascent.

## RmiPortType

`from underautomation.fanuc.rmi.data.rmi_port_type import RmiPortType`

Digital port type used with Local Condition Block (LCB).

- DOUT: Digital Output (DO/DOUT).
- ROUT: Robot Output (RO/ROUT).

## RmiPositionRegisterDataResponse

`from underautomation.fanuc.rmi.data.rmi_position_register_data_response import RmiPositionRegisterDataResponse`

Position register data paired with its register number.

- `RmiPositionRegisterDataResponse()`
- `register_number: int`: Register number
- `cartesian_position: CartesianPositionWithUserFrame`: Position register value.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiRecordedCartesianPosition

`from underautomation.fanuc.rmi.data.rmi_recorded_cartesian_position import RmiRecordedCartesianPosition`

Cartesian position received from the controller via the RMI Position Record menu (TouchUp).

- `RmiRecordedCartesianPosition()`
- `position_id: int`: Position identifier assigned by the controller.
- `position: CartesianPositionWithUserFrame`: Recorded Cartesian position including arm configuration and active frame/tool numbers.

## RmiRecordedJointPosition

`from underautomation.fanuc.rmi.data.rmi_recorded_joint_position import RmiRecordedJointPosition`

Joint position received from the controller via the RMI Position Record menu (TouchUp).

- `RmiRecordedJointPosition()`
- `position_id: int`: Position identifier assigned by the controller.
- `joints: JointsPosition`: Recorded joint angles in degrees.

## RmiResponseBase

`from underautomation.fanuc.rmi.data.rmi_response_base import RmiResponseBase`

Base class for RMI responses that return an error id from the controller.

- `RmiResponseBase()`
- `error_id: int`: Error identifier. 0 means success; non-zero indicates a controller error.
- `error_text: str (read only)`: Human-readable description of error_id. Empty string when there is no error.

## RmiSetPayloadCompensationParameters

`from underautomation.fanuc.rmi.data.rmi_set_payload_compensation_parameters import RmiSetPayloadCompensationParameters`

Parameters for defining payload compensation for a payload schedule. Used by set_payload_compensation(). All positional values are in meters; mass in kg; inertia in kg·m².

- `RmiSetPayloadCompensationParameters()`
- `schedule_number: int`: Payload schedule number to configure.
- `mass_kg: float`: Payload mass in kilograms.
- `cg_xm: float`: Center-of-gravity X offset in meters.
- `cg_ym: float`: Center-of-gravity Y offset in meters.
- `cg_zm: float`: Center-of-gravity Z offset in meters.
- `inertia_xkgm2: float`: Inertia around the X axis in kg·m².
- `inertia_ykgm2: float`: Inertia around the Y axis in kg·m².
- `inertia_zkgm2: float`: Inertia around the Z axis in kg·m².
- `group: int | None`: Optional motion group number. null uses the active group.

## RmiSetPayloadParameters

`from underautomation.fanuc.rmi.data.rmi_set_payload_parameters import RmiSetPayloadParameters`

Parameters for defining payload mass, center of gravity, and optionally inertia for a payload schedule. Used by set_payload_value(). All positional values are in meters; mass in kg; inertia in kg·m².

- `RmiSetPayloadParameters()`
- `schedule_number: int`: Payload schedule number to configure.
- `mass_kg: float`: Payload mass in kilograms.
- `cg_xm: float`: Center-of-gravity X offset in meters.
- `cg_ym: float`: Center-of-gravity Y offset in meters.
- `cg_zm: float`: Center-of-gravity Z offset in meters.
- `inertia_xkgm2: float | None`: Inertia around the X axis in kg·m². null omits this field from the command.
- `inertia_ykgm2: float | None`: Inertia around the Y axis in kg·m². null omits this field from the command.
- `inertia_zkgm2: float | None`: Inertia around the Z axis in kg·m². null omits this field from the command.
- `group: int | None`: Optional motion group number. null uses the active group.

## RmiTcpSpeedResponse

`from underautomation.fanuc.rmi.data.rmi_tcp_speed_response import RmiTcpSpeedResponse`

Result of reading TCP speed.

- `RmiTcpSpeedResponse()`
- `speed: float`: Current tool center point speed in mm/s.
- Inherited from [RmiTimedResponse](underautomation.fanuc.rmi.data.md#rmitimedresponse): `time_tag`
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiTerminationType

`from underautomation.fanuc.rmi.data.rmi_termination_type import RmiTerminationType`

Termination type for motion.

- Fine: FINE termination; precise stop.
- Cnt: Continuous termination; blend motions (1-100).
- Cr: Constant path mode (requires option).

## RmiTimedResponse

`from underautomation.fanuc.rmi.data.rmi_timed_response import RmiTimedResponse`

Base class for responses with a controller time_tag value.

- `RmiTimedResponse()`
- `time_tag: int`: Controller time tick for the data sample.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiUFrameUToolNumbersResponse

`from underautomation.fanuc.rmi.data.rmi_u_frame_u_tool_numbers_response import RmiUFrameUToolNumbersResponse`

Current UFRAME and UTOOL numbers, optionally scoped to a motion group.

- `RmiUFrameUToolNumbersResponse()`
- `frame: int`: Current user frame number.
- `tool: int`: Current user tool number.
- `group: int | None`: Motion group number, or null when not applicable.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

## RmiVariableValueResponse

`from underautomation.fanuc.rmi.data.rmi_variable_value_response import RmiVariableValueResponse`

Result of reading a system variable.

- `RmiVariableValueResponse()`
- `name: str`: Variable name, including the leading $ character.
- `is_integer: bool`: Whether the variable holds a floating-point value.
- `integer_value: int`: Gets or sets the value as an integer. Internally stored as a double.
- `real_value: float`: Gets or sets the value as a double-precision floating-point number.
- Inherited from [RmiResponseBase](underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`
