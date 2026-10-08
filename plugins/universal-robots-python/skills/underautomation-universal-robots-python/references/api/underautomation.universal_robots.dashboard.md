# underautomation.universal_robots.dashboard

## CommandResponse1

`from underautomation.universal_robots.dashboard.command_response_1 import CommandResponse1`

Answer returned by a command which contains a typed value.

- `CommandResponse1(command: CommandResponse)`: Initializes a new instance of CommandResponse by copying the base response data.
- `value: T`: Value return by the command
- Inherited from [CommandResponse](underautomation.universal_robots.dashboard.md#commandresponse): `succeed`, `message`

## CommandResponse

`from underautomation.universal_robots.dashboard.command_response import CommandResponse`

Generic answer returned by a command

- `CommandResponse()`
- `succeed: bool`: The command as succeeded
- `message: str`: A message that described the error or the action done

## DashboardClient

`from underautomation.universal_robots.dashboard.dashboard_client import DashboardClient`

Client for the Universal Robots Dashboard Server protocol. Enables remote control of the robot (load/play/stop programs, power on/off, etc.) via TCP commands on port 29999.

- `DashboardClient()`
- `enable(ip: str, port: int=29999, receiveTimeoutMs: int=2000, sendTimeoutMs: int=500) -> None`: Specifies the IP address of the robot. No TCP connection is maintained. A new connection is created when sending each command.
- Inherited from [DashboardClientBase](underautomation.universal_robots.dashboard.internal.md#dashboardclientbase-robotdashboard): `before_shutdown`, `disable`, `load_program`, `play`, `stop`, `pause`, `send_custom_dashboard_command`, `get_variable`, `shutdown`, `is_program_running`, `get_robot_mode`, `get_loaded_program`, `show_popup`, `close_popup`, `add_to_log`, `is_program_saved`, `get_program_state`, `get_polyscope_version`, `set_user_role`, `set_operational_mode`, `clear_operational_mode`, `get_operational_mode`, `is_in_remote_control`, `power_on`, `power_off`, `release_brake`, `unlock_protective_stop`, `close_safety_popup`, `load_installation`, `restart_safety`, `get_safety_status`, `get_serial_number`, `get_robot_model`, `ip`, `port`, `receive_timeout_ms`, `send_timeout_ms`, `initialized`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## OperationalModes

`from underautomation.universal_robots.dashboard.operational_modes import OperationalModes`

Enumerates all robot operational modes

- Manual: Loading and editing programs is allowed
- Automatic: Loading and editing programs and installations is not allowed, only playing programs
- None_: The password has not been set.

## PolyscopeVersion

`from underautomation.universal_robots.dashboard.polyscope_version import PolyscopeVersion`

Describes a Polyscope version (robot controller firmware).

- `PolyscopeVersion()`
- `date: str`: Release date (example : "Nov 2020")
- `version: typing.Any`: Firmware version
- `description: str`: String description of the firmware version (exemple : "5.0.16.8524 (Nov 2020)")

## ProgramSaveState

`from underautomation.universal_robots.dashboard.program_save_state import ProgramSaveState`

Represents the save state of the currently loaded program on the Universal Robots controller.

- `ProgramSaveState()`
- `is_saved: bool`: Is the program saved
- `name: str`: Name of the loaded program

## ProgramState

`from underautomation.universal_robots.dashboard.program_state import ProgramState`

Describes a program state (its running state and its name)

- `ProgramState()`
- `state: ProgramStates`: Running state of the loaded program
- `name: str`: Name of the loaded program

## ProgramStates

`from underautomation.universal_robots.dashboard.program_states import ProgramStates`

Enumerate possible states of a program.

- Stopped: No program is running.
- Playing: Program is running.
- Paused: Program is paused.

## UserRoles

`from underautomation.universal_robots.dashboard.user_roles import UserRoles`

Enumerates all user roles

- Programmer: In Setup Robot, buttons "Update", "Set Password", "Network", "Time" and "URCaps" are disabled, "Expert Mode" is available (if correct password is supplied)
- Operator: Only "RUN Program" And "SHUTDOWN Robot" buttons are enabled, "Expert Mode" cannot be activated
- None_: All buttons enabled, "Expert Mode" is available (if correct password is supplied)
- Locked: All buttons disabled and "Expert Mode" cannot be activated
- restricted: Works like "operator" but does not give access to the move tab. (From FW 3.1.17136)
