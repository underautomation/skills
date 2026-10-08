# underautomation.fanuc.rmi

## RmiClient

`from underautomation.fanuc.rmi.rmi_client import RmiClient`

RMI client for connecting to and controlling FANUC robots via the Remote Motion Interface protocol.

- `RmiClient()`: Creates a new instance of the RMI client.
- `connect(ip: str, port: int=16001, readTimeoutMs: int=2000) -> None`: Connect to the FANUC controller using the RMI protocol.
- Inherited from [RmiClientBase](underautomation.fanuc.rmi.internal.md#rmiclientbase-robotrmi): `disconnect`, `initialize`, `abort`, `pause`, `continue_`, `reset`, `read_error`, `get_u_frame_u_tool`, `set_u_frame_u_tool`, `get_status`, `auto_set_next_sequence_id`, `get_extended_status`, `read_u_frame`, `write_u_frame`, `read_u_tool`, `write_u_tool`, `read_din`, `write_dout`, `read_io_port`, `write_io_port`, `read_cartesian_position`, `read_joint_angles`, `set_override`, `read_position_register`, `write_position_register_cartesian`, `read_numeric_register`, `write_numeric_register_as_integer`, `write_numeric_register_as_double`, `read_variable`, `write_variable_as_integer`, `write_variable_as_double`, `read_tcp_speed`, `set_payload_schedule`, `set_payload_value`, `set_payload_compensation`, `clear_completed_instructions`, `clear_local_queued_instructions`, `send_tp_instruction`, `dispose`, `connected`, `major_version`, `minor_version`, `working_port`, `last_sequence_id`, `check_sequence_id`, `is_in_hold_state`, `read_timeout_ms`, `instructions`, `connection_terminated`, `system_fault_received`, `recorded_cartesian_position_received`, `recorded_joint_position_received`, `unknown_packet_received`

## RmiException

`from UnderAutomation.Fanuc.Rmi import RmiException`

Represents an error reported by the FANUC RMI controller or thrown by the client runtime.

The SDK raises this .NET type: catch it with `except RmiException as e` after the import above. Its members keep their .NET names. The class `RmiException` of the module `underautomation.fanuc.rmi.rmi_exception` is not a Python exception and cannot be caught.

- `ErrorId: int (read only)`: Gets the controller error id when available (0 means no error id was attached).
- Inherited from System.Exception: `Message`, `InnerException`
