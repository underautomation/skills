# underautomation.universal_robots.interpreter_mode

## CommandResponse

`from underautomation.universal_robots.interpreter_mode.command_response import CommandResponse`

Response to an Interpreter Mode command

- `status: CommandResponseStatus (read only)`: Response type to check if command succeed
- `id: int (read only)`: Command unique identifier
- `body: str (read only)`: Answer from the interpreter mode
- `raw_answer: str (read only)`: Raw line sent from the controller
- `command: str (read only)`: Command sent to the interpreter mode

## CommandResponseStatus

`from underautomation.universal_robots.interpreter_mode.command_response_status import CommandResponseStatus`

Type of response of an Interpreter Mode command

- Error: Something went wrong when receiving response
- Ack: The command compilation succeed and Interpreter mode will execute the statement
- Discard: Program is not running or the statement results in a compilation or linker error
- State: Answer from a state command

## InterpreterModeClient

`from underautomation.universal_robots.interpreter_mode.interpreter_mode_client import InterpreterModeClient`

Client for the Universal Robots Interpreter Mode, allowing real-time execution of URScript commands over TCP.

- `InterpreterModeClient()`
- `connect(ip: str, port: int=30020) -> None`: Specifies the IP address of the robot. No TCP connection is maintained. A new connection is created when sending each command.
- Inherited from [InterpreterModeClientBase](underautomation.universal_robots.interpreter_mode.internal.md#interpretermodeclientbase-robotinterpreter_mode): `execute_command`, `end_interpreter`, `clear_interpreter`, `abort`, `skip_buffer`, `state_last_executed`, `state_last_interpreted`, `state_last_cleared`, `state_last_unexecuted`, `disconnect`, `ip`, `port`, `connected`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`
