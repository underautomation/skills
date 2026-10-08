# UnderAutomation.UniversalRobots.Rest

## ProgramStateAction

`enum ProgramStateAction`

Actions available for changing the program state via REST API

- pause: Pause the running program
- play: Start or resume playing the program
- resume: Resume a paused program
- stop: Stop the running program

## ProgramStateResponse

`class ProgramStateResponse`

Response from GET /program/v1/state endpoint

- `ProgramStateResponse()`
- `RestProgramState State { get; set; }`: Current state of the program

## RestApiResponse<T>

`class RestApiResponse<T> : RestApiResponse`

Generic response from a REST API call with typed value

- `RestApiResponse()`: Creates a new RestApiResponse from a base response
- `RestApiResponse(RestApiResponse baseResponse)`: Creates a new RestApiResponse from a base response
- `T Value { get; set; }`: Typed value from the response
- Inherited from [RestApiResponse](UnderAutomation.UniversalRobots.Rest.md#restapiresponse): `Succeed`, `StatusCode`, `Message`, `RawResponse`

## RestApiResponse

`class RestApiResponse`

Response from a REST API call

- `RestApiResponse()`
- `string Message { get; set; }`: Response message or error description
- `string RawResponse { get; set; }`: Raw JSON response body
- `HttpStatusCode StatusCode { get; set; }`: HTTP status code returned by the API
- `bool Succeed { get; set; }`: Indicates whether the API call succeeded (HTTP 200)

## RestApiVersion (robot.Rest.Version)

`enum RestApiVersion`

REST API version for PolyscopeX robots

- Latest: Latest API version (currently V1)
- V1: API Version 1

## RestClient

`class RestClient : RestClientBase`

Standalone REST API client for PolyscopeX robots. Use this class when you want to interact with the REST API independently from the main UR class.

- `RestClient()`
- `void Enable(string ip, int port = 80, RestApiVersion version = RestApiVersion.Latest, int timeoutMs = 5000)`: Enable the REST client with the specified connection parameters.
- Inherited from [RestClientBase](UnderAutomation.UniversalRobots.Rest.Internal.md#restclientbase-robotrest): `Disable`, `ChangeRobotState`, `UnlockProtectiveStop`, `RestartSafety`, `PowerOff`, `PowerOn`, `BrakeRelease`, `LoadProgram`, `ChangeProgramState`, `Play`, `Pause`, `Stop`, `Resume`, `GetProgramState`, `IP`, `Port`, `Version`, `TimeoutMs`, `Initialized`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## RestProgramState

`enum RestProgramState`

Program state values returned by the REST API

- Paused: Program is paused
- Playing: Program is playing
- Stopped: Program is stopped
- Unknown: Unknown state

## RobotStateAction

`enum RobotStateAction`

Actions available for changing the robot's operational state via REST API

- BRAKE_RELEASE: Releases the robot brakes
- POWER_OFF: Powers off the robot
- POWER_ON: Powers on the robot
- RESTART_SAFETY: Restarts the safety system
- UNLOCK_PROTECTIVE_STOP: Unlocks the robot from a protective stop state
