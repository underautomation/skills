# underautomation.fanuc.rmi.internal

## RmiClientBase (robot.rmi)

`from underautomation.fanuc.rmi.internal.rmi_client_base import RmiClientBase`

High-level Remote Motion Interface (RMI) client for FANUC controllers. Manages the connection lifecycle, all administrative commands, and the full set of motion instruction packets over the RMI TCP protocol.

- `RmiClientBase()`: Creates a new instance of the RMI client.
- `connection_terminated(handler)`: Fired when the controller closes the session (e.g. communication idle timeout). The client is automatically disconnected after this event fires.
- `system_fault_received(handler)`: Fired when the controller reports a system fault on a given sequence. The argument is the SequenceID of the faulted instruction (0 when unknown).
- `recorded_cartesian_position_received(handler)`: Fired when the controller sends a Cartesian position via the RMI Position Record menu.
- `recorded_joint_position_received(handler)`: Fired when the controller sends a joint position via the RMI Position Record menu.
- `unknown_packet_received(handler)`: Fired when an unknown packet is received from the controller.
- `disconnect() -> None`: Disconnect from the controller by sending the disconnect command on the working port. Safe to call even when already disconnected.
- `initialize(groupMask: int | None=None, rtsa: bool | None=None, pltzMode: RmiPltzMode | None=None) -> None`: Initialize RMI and start the motion program. Must be called before sending any motion instructions. It also Resets last_sequence_id and empty the instruction buffer instructions
- `abort() -> None`: Abort the running motion program. Note that a Reset() will be called automatically if the controller is in the HOLD state.
- `pause() -> None`: Pause the running motion program.
- `continue_() -> None`: Resume a paused motion program.
- `reset() -> None`: Reset controller errors and exit the HOLD state.
- `read_error(count: int | None=None) -> RmiControllerErrorTextResponse`: Read the most recent controller error text. Up to 5 consecutive errors can be requested.
- `get_u_frame_u_tool(group: int | None=None) -> RmiUFrameUToolNumbersResponse`: Get the current UFRAME and UTOOL numbers.
- `set_u_frame_u_tool(uframe: int, utool: int, group: int | None=None) -> None`: Set the current UFRAME and UTOOL numbers.
- `get_status() -> RmiControllerStatusResponse`: Get the current controller and RMI motion status.
- `auto_set_next_sequence_id() -> RmiControllerStatusResponse`: Calls internally get_status() and set last_sequence_id only if $RMI_CFG.$Chk_seqID = FALSE. It also set check_sequence_id to $RMI_CFG.$Chk_seqID.
- `get_extended_status() -> RmiExtendedControllerStatusResponse`: Get extended controller status including drive power state and speed clamp.
- `read_u_frame(number: int, group: int | None=None) -> RmiIndexedFrameResponse`: Read the UFRAME at the given index.
- `write_u_frame(number: int, position: XYZWPRPosition, group: int | None=None) -> None`: Write the UFRAME at the given index.
- `read_u_tool(number: int, group: int | None=None) -> RmiIndexedFrameResponse`: Read the UTOOL at the given index.
- `write_u_tool(number: int, position: XYZWPRPosition, group: int | None=None) -> None`: Write the UTOOL at the given index.
- `read_din(portNumber: int) -> RmiDigitalInputValueResponse`: Read a digital input port value.
- `write_dout(portNumber: int, value: RmiOnOff) -> None`: Write a digital output port value.
- `read_io_port(portType: RmiIoPortType, portNumber: int) -> RmiIoPortValueResponse`: Read a generic IO port (DI, DO, AI, AO, GO, RO, FLAG, RI, UI, UO).
- `write_io_port(portType: RmiIoPortType, portNumber: int, value: float) -> None`: Write a generic IO port (AO, GO, DO, RO, FLAG).
- `read_cartesian_position(group: int | None=None) -> RmiCartesianPositionResponse`: Read current Cartesian TCP position.
- `read_joint_angles(group: int | None=None) -> RmiJointAnglesSampleResponse`: Read current joint angles.
- `set_override(value: int) -> None`: Set the program speed override (1–100 %).
- `read_position_register(number: int, group: int | None=None) -> RmiPositionRegisterDataResponse`: Read a position register
- `write_position_register_cartesian(number: int, target: CartesianPositionWithUserFrame, group: int | None=None) -> None`: Write a Cartesian position register
- `read_numeric_register(number: int) -> RmiNumericRegisterValueResponse`: Read a numeric register
- `write_numeric_register_as_integer(number: int, value: int) -> None`: Write an integer value to a numeric register
- `write_numeric_register_as_double(number: int, value: float) -> None`: Write a float value to a numeric register
- `read_variable(name: str) -> RmiVariableValueResponse`: Read a system variable by name (name must include the leading $ character).
- `write_variable_as_integer(name: str, value: int) -> None`: Write an integer value to a system variable (name must include the leading $).
- `write_variable_as_double(name: str, value: float) -> None`: Write a float value to a system variable (name must include the leading $).
- `read_tcp_speed() -> RmiTcpSpeedResponse`: Read the current TCP speed in mm/s.
- `set_payload_schedule(scheduleNumber: int, group: int | None=None) -> None`: Immediately apply a payload schedule to the active group (command, not an instruction).
- `set_payload_value(scheduleNumber: int, massKg: float, cgXm: float, cgYm: float, cgZm: float, inertiaXkgm2: float | None=None, inertiaYkgm2: float | None=None, inertiaZkgm2: float | None=None, group: int | None=None) -> None`: Define payload mass, center of gravity, and optionally inertia for a payload schedule.
- `set_payload_value(p: RmiSetPayloadParameters) -> None`: Define payload mass, center of gravity, and optionally inertia for a payload schedule.
- `set_payload_compensation(scheduleNumber: int, massKg: float, cgXm: float, cgYm: float, cgZm: float, inertiaXkgm2: float, inertiaYkgm2: float, inertiaZkgm2: float, group: int | None=None) -> None`: Define payload compensation parameters for a payload schedule.
- `set_payload_compensation(p: RmiSetPayloadCompensationParameters) -> None`: Define payload compensation parameters for a payload schedule.
- `clear_completed_instructions() -> None`: Removes all instructions with a terminal status (Completed or Error) from the tracked instruction list. Instructions that are still pending or in progress are not affected.
- `clear_local_queued_instructions() -> None`: Cancels and removes all instructions that are still in the local client buffer (LocalQueued). These instructions have not been sent to the controller yet. Each cancelled instruction is marked with an error so that any thread blocked on wait_for_completion() is unblocked. Instructions already sent...
- `send_tp_instruction(instruction: RmiInstructionBase) -> RmiInstructionResponse`: Serializes the instruction to the RMI wire format and queues it on the controller. Returns an RmiInstructionResponse that tracks execution.
- `dispose() -> None`: Disconnect from the controller and release resources.
- `connected: bool (read only)`: Indicates that the client is currently connected to the controller working port.
- `major_version: int (read only)`: Controller protocol major version reported during the connection handshake.
- `minor_version: int (read only)`: Controller protocol minor version reported during the connection handshake.
- `working_port: int (read only)`: Working port returned by the controller; all commands use this port after connection.
- `last_sequence_id: int (read only)`: Sequence ID used for the last instruction sent to the controller. Reset to 0 by initialize().. Modified by auto_set_next_sequence_id().
- `check_sequence_id: bool`: Indicates whether the controller checks for consecutive sequence IDs in motion instructions ($RMI_CFG.$Chk_seqID). Modified by auto_set_next_sequence_id().
- `is_in_hold_state: bool (read only)`: Indicates that the controller has entered the HOLD state and will not accept new TP instructions until reset() is called. The HOLD state is entered in two situations: An invalid sequence ID was detected (error RMIT-029, error code 2556957). RMI checks that sequence IDs are consecutive. If a gap i...
- `read_timeout_ms: int (read only)`: RMI connection parameters used during Connect().
- `instructions: typing.List[RmiInstructionResponse] (read only)`: All instructions submitted since the last initialize() or explicit clear, in submission order. Includes instructions in all states: LocalQueued, ControllerQueued, Executing, Completed and Error. Returns a snapshot array; the array is not updated after it is returned.

## RmiClientInternal (robot.rmi)

`from underautomation.fanuc.rmi.internal.rmi_client_internal import RmiClientInternal`

Internal RMI client used by the library infrastructure.

- Inherited from [RmiClientBase](underautomation.fanuc.rmi.internal.md#rmiclientbase-robotrmi): `disconnect`, `initialize`, `abort`, `pause`, `continue_`, `reset`, `read_error`, `get_u_frame_u_tool`, `set_u_frame_u_tool`, `get_status`, `auto_set_next_sequence_id`, `get_extended_status`, `read_u_frame`, `write_u_frame`, `read_u_tool`, `write_u_tool`, `read_din`, `write_dout`, `read_io_port`, `write_io_port`, `read_cartesian_position`, `read_joint_angles`, `set_override`, `read_position_register`, `write_position_register_cartesian`, `read_numeric_register`, `write_numeric_register_as_integer`, `write_numeric_register_as_double`, `read_variable`, `write_variable_as_integer`, `write_variable_as_double`, `read_tcp_speed`, `set_payload_schedule`, `set_payload_value`, `set_payload_compensation`, `clear_completed_instructions`, `clear_local_queued_instructions`, `send_tp_instruction`, `dispose`, `connected`, `major_version`, `minor_version`, `working_port`, `last_sequence_id`, `check_sequence_id`, `is_in_hold_state`, `read_timeout_ms`, `instructions`, `connection_terminated`, `system_fault_received`, `recorded_cartesian_position_received`, `recorded_joint_position_received`, `unknown_packet_received`

## RmiConnectParametersBase

`from underautomation.fanuc.rmi.internal.rmi_connect_parameters_base import RmiConnectParametersBase`

Base class for RMI connection parameters.

- `RmiConnectParametersBase()`
- `port: int`: RMI bootstrap port number.
- `read_timeout_ms: int`: RMI read timeout in milliseconds.
- `static DEFAULT_PORT: int`: Default RMI bootstrap port (16001).
- `static DEFAULT_READ_TIMEOUT_MS: int`: Default RMI read timeout (infinite).
