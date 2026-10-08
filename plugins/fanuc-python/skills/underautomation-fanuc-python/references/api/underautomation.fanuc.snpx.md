# underautomation.fanuc.snpx

## SnpxClient

`from underautomation.fanuc.snpx.snpx_client import SnpxClient`

SNPX protocol client for communicating with Fanuc robots.

- `SnpxClient()`: Initializes a new instance of the SnpxClient class.
- `connect(ip: str, port: int=60008) -> None`: Connects to a Fanuc robot using the SNPX protocol.
- Inherited from [SnpxClientBase](underautomation.fanuc.snpx.internal.md#snpxclientbase-robotsnpx): `poll_and_get_updated_connected_state`, `disconnect`, `clear_alarms`, `set_variable`, `clear_assignments`, `get_assignments`, `ip`, `numeric_registers`, `numeric_registers_int32`, `numeric_registers_int16`, `position_registers`, `string_registers`, `integer_system_variables`, `real_system_variables`, `position_system_variables`, `string_system_variables`, `digital_signals`, `sdi`, `sdo`, `rdi`, `rdo`, `ui`, `uo`, `si`, `so`, `wi`, `wo`, `wsi`, `pmc_k`, `pmc_r`, `numeric_i_os`, `gi`, `go`, `ai`, `ao`, `pmc_d`, `flags`, `current_position`, `current_task_status`, `active_alarm`, `alarm_history`, `comments`, `simulation_status`, `language`, `connected`
