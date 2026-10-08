# UnderAutomation.UniversalRobots.Rest.Internal

## RestClientBase (robot.Rest)

`abstract class RestClientBase : URServiceBase`

Base implementation of the REST API client for PolyscopeX robots

- `RestApiResponse BrakeRelease()`: Release the robot brakes.
- `RestApiResponse ChangeProgramState(ProgramStateAction action)`: Change the program state. PUT /program/v1/state
- `RestApiResponse ChangeRobotState(RobotStateAction action)`: Change the robot's operational state. PUT /robotstate/v1/state
- `void Disable()`: Disable the REST client
- `RestApiResponse<ProgramStateResponse> GetProgramState()`: Get the current program state. GET /program/v1/state
- `string IP { get; }`: IP address of the robot
- `bool Initialized { get; }`: Indicates whether the REST client has been initialized
- `RestApiResponse LoadProgram(string programName)`: Load a program by name. PUT /program/v1/load
- `RestApiResponse Pause()`: Pause the running program.
- `RestApiResponse Play()`: Start playing the loaded program.
- `int Port { get; }`: HTTP port for REST API
- `RestApiResponse PowerOff()`: Power off the robot.
- `RestApiResponse PowerOn()`: Power on the robot.
- `RestApiResponse RestartSafety()`: Restart the safety system.
- `RestApiResponse Resume()`: Resume a paused program.
- `RestApiResponse Stop()`: Stop the running program.
- `int TimeoutMs { get; }`: Request timeout in milliseconds
- `RestApiResponse UnlockProtectiveStop()`: Unlock the robot from protective stop state.
- `RestApiVersion Version { get; }`: REST API version being used
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## RestClientParametersBase

`abstract class RestClientParametersBase`

Base parameters for REST API client configuration

- `const int DEFAULT_PORT = 80`: Default REST API HTTP port
- `const int DEFAULT_TIMEOUT_MS = 5000`: Default request timeout in milliseconds
- `int Port { get; set; }`: REST API HTTP port. Default: 80
- `int TimeoutMs { get; set; }`: Request timeout in milliseconds. Default: 5000ms
- `RestApiVersion Version { get; set; }`: REST API version to use. Default: Latest
