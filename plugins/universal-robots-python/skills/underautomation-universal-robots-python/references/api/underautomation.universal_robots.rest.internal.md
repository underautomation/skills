# underautomation.universal_robots.rest.internal

## RestClientBase (robot.rest)

`from underautomation.universal_robots.rest.internal.rest_client_base import RestClientBase`

Base implementation of the REST API client for PolyscopeX robots

- `disable() -> None`: Disable the REST client
- `change_robot_state(action: RobotStateAction) -> RestApiResponse`: Change the robot's operational state.
- `unlock_protective_stop() -> RestApiResponse`: Unlock the robot from protective stop state.
- `restart_safety() -> RestApiResponse`: Restart the safety system.
- `power_off() -> RestApiResponse`: Power off the robot.
- `power_on() -> RestApiResponse`: Power on the robot.
- `brake_release() -> RestApiResponse`: Release the robot brakes.
- `load_program(programName: str) -> RestApiResponse`: Load a program by name.
- `change_program_state(action: ProgramStateAction) -> RestApiResponse`: Change the program state.
- `play() -> RestApiResponse`: Start playing the loaded program.
- `pause() -> RestApiResponse`: Pause the running program.
- `stop() -> RestApiResponse`: Stop the running program.
- `resume() -> RestApiResponse`: Resume a paused program.
- `get_program_state() -> RestApiResponse1[ProgramStateResponse]`: Get the current program state.
- `ip: str (read only)`: IP address of the robot
- `port: int (read only)`: HTTP port for REST API
- `version: RestApiVersion (read only)`: REST API version being used
- `timeout_ms: int (read only)`: Request timeout in milliseconds
- `initialized: bool (read only)`: Indicates whether the REST client has been initialized
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## RestClientParametersBase

`from underautomation.universal_robots.rest.internal.rest_client_parameters_base import RestClientParametersBase`

Base parameters for REST API client configuration

- `port: int`: REST API HTTP port. Default: 80
- `version: RestApiVersion`: REST API version to use. Default: Latest
- `timeout_ms: int`: Request timeout in milliseconds. Default: 5000ms
- `static DEFAULT_PORT: int`: Default REST API HTTP port
- `static DEFAULT_TIMEOUT_MS: int`: Default request timeout in milliseconds
