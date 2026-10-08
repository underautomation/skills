# underautomation.universal_robots.rest

## ProgramStateAction

`from underautomation.universal_robots.rest.program_state_action import ProgramStateAction`

Actions available for changing the program state via REST API

- play: Start or resume playing the program
- pause: Pause the running program
- stop: Stop the running program
- resume: Resume a paused program

## ProgramStateResponse

`from underautomation.universal_robots.rest.program_state_response import ProgramStateResponse`

State of the program, returned by get_program_state().

- `ProgramStateResponse()`
- `state: RestProgramState`: Current state of the program

## RestApiResponse1

`from underautomation.universal_robots.rest.rest_api_response_1 import RestApiResponse1`

Generic response from a REST API call with typed value

- `RestApiResponse1(baseResponse: RestApiResponse)`: Creates a new RestApiResponse from a base response
- `value: T`: Typed value from the response
- Inherited from [RestApiResponse](underautomation.universal_robots.rest.md#restapiresponse): `succeed`, `status_code`, `message`, `raw_response`

## RestApiResponse

`from underautomation.universal_robots.rest.rest_api_response import RestApiResponse`

Response from a REST API call

- `RestApiResponse()`
- `succeed: bool`: Indicates whether the API call succeeded (HTTP 200)
- `status_code: typing.Any`: HTTP status code returned by the API
- `message: str`: Response message or error description
- `raw_response: str`: Raw JSON response body

## RestApiVersion (robot.rest.version)

`from underautomation.universal_robots.rest.rest_api_version import RestApiVersion`

REST API version for PolyscopeX robots

- V1: API Version 1
- Latest: Latest API version (currently V1)

## RestClient

`from underautomation.universal_robots.rest.rest_client import RestClient`

Standalone REST API client for PolyscopeX robots. Use this class when you want to interact with the REST API independently from the main UR class.

- `RestClient()`
- `enable(ip: str, port: int=80, version: RestApiVersion=RestApiVersion.V1, timeoutMs: int=5000) -> None`: Enable the REST client with the specified connection parameters.
- Inherited from [RestClientBase](underautomation.universal_robots.rest.internal.md#restclientbase-robotrest): `disable`, `change_robot_state`, `unlock_protective_stop`, `restart_safety`, `power_off`, `power_on`, `brake_release`, `load_program`, `change_program_state`, `play`, `pause`, `stop`, `resume`, `get_program_state`, `ip`, `port`, `version`, `timeout_ms`, `initialized`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## RestProgramState

`from underautomation.universal_robots.rest.rest_program_state import RestProgramState`

Program state values returned by the REST API

- Unknown: Unknown state
- Stopped: Program is stopped
- Playing: Program is playing
- Paused: Program is paused

## RobotStateAction

`from underautomation.universal_robots.rest.robot_state_action import RobotStateAction`

Actions available for changing the robot's operational state via REST API

- UNLOCK_PROTECTIVE_STOP: Unlocks the robot from a protective stop state
- RESTART_SAFETY: Restarts the safety system
- POWER_OFF: Powers off the robot
- POWER_ON: Powers on the robot
- BRAKE_RELEASE: Releases the robot brakes
