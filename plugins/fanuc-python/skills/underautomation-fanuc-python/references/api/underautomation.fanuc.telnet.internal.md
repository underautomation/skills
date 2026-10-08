# underautomation.fanuc.telnet.internal

## TelnetClientBase (robot.telnet)

`from underautomation.fanuc.telnet.internal.telnet_client_base import TelnetClientBase`

Base class for Telnet KCL client

- `raw_data_received(handler)`: Occurs when raw data is received.
- `string_data_received(handler)`: Occurs when data is received and its content can successfully be parsed as a string message.
- `tp_coordinates_received(handler)`: Occurs when TP coordinates are received.
- `message_received(handler)`: Occurs when a message is received.
- `error_occured(handler)`: Occurs when an error occurs in the KCL client.
- `command_sent(handler)`: Occurs when a command is sent.
- `command_received(handler)`: Occurs when a KCL command is received.
- `poll_and_get_updated_connected_state() -> bool`: Checks the actual connection status via an active socket polling
- `disconnect() -> None`: Disconnect Telnet client from robot
- `ip: str (read only)`: Connect robot IP address or host name
- `language: Languages`: Controller language (default is English)
- `tp_coordinates: TpCoordinates (read only)`: Gets the current Teach Pendant coordinate system.
- `connected: bool (read only)`: Is Telnet client connected
- Inherited from [KclClientBase](underautomation.fanuc.common.kcl.md#kclclientbase-robottelnet): `abort`, `abort_all`, `clear_all`, `clear_program`, `clear_vars`, `continue_`, `hold`, `pause`, `reset`, `run`, `set_port`, `set_variable`, `get_current_pose`, `get_variable`, `simulate`, `unsimulate_all`, `unsimulate`, `send_custom_command`, `get_task_information`, `add_breakpoint`, `remove_breakpoint`, `remove_all_breakpoints`, `get_breakpoints`, `step_on`, `step_off`

## TelnetClientInternal (robot.telnet)

`from underautomation.fanuc.telnet.internal.telnet_client_internal import TelnetClientInternal`

Internal implementation of KCL Client

- Inherited from [TelnetClientBase](underautomation.fanuc.telnet.internal.md#telnetclientbase-robottelnet): `poll_and_get_updated_connected_state`, `disconnect`, `ip`, `language`, `tp_coordinates`, `connected`, `raw_data_received`, `string_data_received`, `tp_coordinates_received`, `message_received`, `error_occured`, `command_sent`, `command_received`
- Inherited from [KclClientBase](underautomation.fanuc.common.kcl.md#kclclientbase-robottelnet): `abort`, `abort_all`, `clear_all`, `clear_program`, `clear_vars`, `continue_`, `hold`, `pause`, `reset`, `run`, `set_port`, `set_variable`, `get_current_pose`, `get_variable`, `simulate`, `unsimulate_all`, `unsimulate`, `send_custom_command`, `get_task_information`, `add_breakpoint`, `remove_breakpoint`, `remove_all_breakpoints`, `get_breakpoints`, `step_on`, `step_off`

## TelnetConnectParametersBase

`from underautomation.fanuc.telnet.internal.telnet_connect_parameters_base import TelnetConnectParametersBase`

Base class for Telnet connection parameters.

- `TelnetConnectParametersBase()`
- `telnet_kcl_password: str`: Gets or sets the Telnet KCL password used for authentication.
