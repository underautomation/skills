# underautomation.fanuc.telnet

## CommandSentEventArgs

`from underautomation.fanuc.telnet.command_sent_event_args import CommandSentEventArgs`

Event arguments for command sent events.

- `CommandSentEventArgs()`
- `command: str`: Gets the command that was sent.

## KclClientErrorEventArgs

`from underautomation.fanuc.telnet.kcl_client_error_event_args import KclClientErrorEventArgs`

Event arguments for KCL client error events.

- `KclClientErrorEventArgs()`
- `exception: typing.Any`: Gets the exception that occurred.

## KclCommandReceived

`from underautomation.fanuc.telnet.kcl_command_received import KclCommandReceived`

Event arguments for KCL command received events.

- `KclCommandReceived()`
- `result: Result`: Gets the result of the received command.

## MessageReceivedEventArgs

`from underautomation.fanuc.telnet.message_received_event_args import MessageReceivedEventArgs`

Event arguments for message received events.

- `MessageReceivedEventArgs()`
- `is_reset: bool (read only)`: Gets a value indicating whether the message is a reset (empty message).
- `message: str`: Gets the message received from the controller.

## RawDataReceivedEventArgs

`from underautomation.fanuc.telnet.raw_data_received_event_args import RawDataReceivedEventArgs`

Event arguments for raw data received events.

- `RawDataReceivedEventArgs()`
- `data: str`: Gets the raw data received.

## TelnetClient

`from underautomation.fanuc.telnet.telnet_client import TelnetClient`

Main class that represents a connection to a Fanuc Motoman industrial robot

- `TelnetClient()`: Create a new instance of a robot communication
- `connect(ip: str, telnetKclPassword: str) -> None`: Connect to a robot
- Inherited from [TelnetClientBase](underautomation.fanuc.telnet.internal.md#telnetclientbase-robottelnet): `poll_and_get_updated_connected_state`, `disconnect`, `ip`, `language`, `tp_coordinates`, `connected`, `raw_data_received`, `string_data_received`, `tp_coordinates_received`, `message_received`, `error_occured`, `command_sent`, `command_received`
- Inherited from [KclClientBase](underautomation.fanuc.common.kcl.md#kclclientbase-robottelnet): `abort`, `abort_all`, `clear_all`, `clear_program`, `clear_vars`, `continue_`, `hold`, `pause`, `reset`, `run`, `set_port`, `set_variable`, `get_current_pose`, `get_variable`, `simulate`, `unsimulate_all`, `unsimulate`, `send_custom_command`, `get_task_information`, `add_breakpoint`, `remove_breakpoint`, `remove_all_breakpoints`, `get_breakpoints`, `step_on`, `step_off`

## TpCoordinates (robot.telnet.tp_coordinates)

`from underautomation.fanuc.telnet.tp_coordinates import TpCoordinates`

Enumeration of TP (Teach Pendant) coordinate systems.

- Unknown: Unknown coordinate system.
- Tool: Tool coordinate system.
- User: User coordinate system.
- Joint: Joint coordinate system.
- JogFrame: Jog frame coordinate system.
- World: World coordinate system.

## TpCoordinatesReceivedEventArgs

`from underautomation.fanuc.telnet.tp_coordinates_received_event_args import TpCoordinatesReceivedEventArgs`

Event arguments for TP coordinates received events.

- `TpCoordinatesReceivedEventArgs()`
- `coord: TpCoordinates`: Gets the TP coordinate system received.
