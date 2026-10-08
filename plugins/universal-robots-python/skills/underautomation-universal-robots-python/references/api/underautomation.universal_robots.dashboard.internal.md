# underautomation.universal_robots.dashboard.internal

## DashboardClientBase (robot.dashboard)

`from underautomation.universal_robots.dashboard.internal.dashboard_client_base import DashboardClientBase`

Abstract base class providing Dashboard Server command implementations for the Universal Robots controller. Sends text-based commands over TCP and parses responses. A new TCP connection is created for each command.

- `disable() -> None`: Disable dashboard client
- `load_program(programName: str) -> CommandResponse`: Start loading the specified program. (From FW 1.4) Returns when both program and associated installation has loaded (or failed). The load command fails if the associated installation requires confirmation of safety.The return value in this case will be 'Error while loading program'.
- `play() -> CommandResponse`: Starts program, if any program is loaded and robot is ready. (From FW 1.4) Returns failure if the program fails to start.
- `stop() -> CommandResponse`: Stops running program. (From FW 1.4) Returns failure if the program fails to stop
- `pause() -> CommandResponse`: Pauses the running program . (From FW 1.4) Returns failure if the program fails to pause
- `send_custom_dashboard_command(command: str) -> CommandResponse`: Send a custom command to the Dashboard Server port
- `get_variable(name: str) -> CommandResponse1[GlobalVariable]`: Get variable value and estimate its type
- `shutdown() -> CommandResponse`: Shuts down and turns off robot and controller. Closes the connection. (From FW 1.4)
- `is_program_running() -> CommandResponse1[bool]`: Returns a True value is a program is running. (From FW 1.6)
- `get_robot_mode() -> CommandResponse1[RobotModes]`: Returns the current robot state. (From FW 1.6)
- `get_loaded_program() -> CommandResponse1[str]`: Returns the path of the loaded program. If not program is loaded, Value member is null. (From FW 1.6)
- `show_popup(message: str) -> CommandResponse`: Shows a popup on Polyscope with the specified message. The popup-text will be translated to the selected language, if the text exists in the language file. (From FW 1.6)
- `close_popup() -> CommandResponse`: Closes the popup (From FW 1.6)
- `add_to_log(message: str) -> CommandResponse`: Adds log-message to the Log history. (From FW 1.8.11657)
- `is_program_saved() -> CommandResponse1[ProgramSaveState]`: Returns the save state of the active program and path to loaded program file. (From FW 1.8.11997)
- `get_program_state() -> CommandResponse1[ProgramState]`: Returns the state of the active program and path to loaded program file, or STOPPED if no program is loaded
- `get_polyscope_version() -> CommandResponse1[PolyscopeVersion]`: Returns the version of the Polyscope software (From FW 1.8.14035)
- `set_user_role(role: UserRoles) -> CommandResponse`: Controls the available options on the Welcome screen (From FW 1.8.14035 to 3.12.0)
- `set_operational_mode(mode: OperationalModes) -> CommandResponse`: Controls the operational mode. See User manual for details. If this function is called the operational mode cannot be changed from PolyScope, and the user password is disabled. OperationalModes.None is not a valid operational mode. (From FW 5.0.0)
- `clear_operational_mode() -> CommandResponse`: The operational mode can again be changed from PolyScope, and the user password is enabled. (From FW 5.0.0)
- `get_operational_mode() -> CommandResponse1[OperationalModes]`: Returns the operational mode. (From FW 5.6)
- `is_in_remote_control() -> CommandResponse1[bool]`: Returns the remote control status of the robot. If the robot Is In remote control it returns False And If remote control Is disabled Or robot Is in local control it returns false. (From FW 5.6)
- `power_on() -> CommandResponse`: Powers on the robot arm. (From FW 3.0)
- `power_off() -> CommandResponse`: Powers off the robot arm. (From FW 3.0)
- `release_brake() -> CommandResponse`: Releases the brakes. (From FW 3.0)
- `unlock_protective_stop() -> CommandResponse`: Closes the current popup and unlocks protective stop. (From FW 3.1)
- `close_safety_popup() -> CommandResponse`: Closes a safety popup. (From FW 3.1)
- `load_installation(installation: str) -> CommandResponse`: Loads the specified installation file (From FW 3.2.18654)
- `restart_safety() -> CommandResponse`: Restarts the safety. Used when robot gets a safety fault or violation to restart the safety. After safety has been rebooted the robot will be in Power Off. (From FW 3.7 to 3.12.0 and from 5.1.0)
- `get_safety_status() -> CommandResponse1[SafetyStatus]`: Returns the current safety status. (From FW 3.11 to 3.12 and from FW 5.5)
- `get_serial_number() -> CommandResponse`: Returns serial number of the robot (FW 3.12 and from FW 5.6)
- `get_robot_model() -> CommandResponse1[RobotModels]`: Returns the robot model (UR3, UR5, UR10, UR16, ...). (FW 3.12 and from FW 5.6)
- `ip: str (read only)`: IP of the robot to connect to for sending commands
- `port: int (read only)`: Dashboard server port
- `receive_timeout_ms: int (read only)`: Receive timeout in milliseconds
- `send_timeout_ms: int (read only)`: Send timeout in milliseconds
- `initialized: bool (read only)`: Indicates that the dashboard client has been initialized and is ready to send commands
- `before_shutdown: typing.Any`: Event raised when function shutdown() is called.
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## DashboardClientParametersBase

`from underautomation.universal_robots.dashboard.internal.dashboard_client_parameters_base import DashboardClientParametersBase`

Abstract base class for Dashboard Server connection parameters, providing default port and timeout values.

- `port: int`: Dashboard client TCP port. Default : 29999
- `receive_timeout_ms: int`: Receive timeout in milliseconds. Default : 2000 ms
- `send_timeout_ms: int`: Send timeout in milliseconds. Default : 500 ms
- `static DEFAULT_PORT: int`: Default Dashboard server TCP port
- `static DEFAULT_RECEIVE_TIMEOUT_MS: int`: Default receive timeout in milliseconds
- `static DEFAULT_SEND_TIMEOUT_MS: int`: Default send timeout in milliseconds
