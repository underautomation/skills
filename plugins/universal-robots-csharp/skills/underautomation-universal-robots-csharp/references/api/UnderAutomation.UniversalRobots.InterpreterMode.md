# UnderAutomation.UniversalRobots.InterpreterMode

## CommandResponse

`class CommandResponse`

Response to an Interpreter Mode command

- `string Body { get; }`: Answer from the interpreter mode
- `string Command { get; }`: Command sent to the interpreter mode
- `int Id { get; }`: Command unique identifier
- `string RawAnswer { get; }`: Raw line sent from the controller
- `CommandResponseStatus Status { get; }`: Response type to check if command succeed

## CommandResponseStatus

`enum CommandResponseStatus`

Type of response of an Interpreter Mode command

- Ack: The command compilation succeed and Interpreter mode will execute the statement
- Discard: Program is not running or the statement results in a compilation or linker error
- Error: Something went wrong when receiving response
- State: Answer from a state command

## InterpreterModeClient

`class InterpreterModeClient : InterpreterModeClientBase`

Client for the Universal Robots Interpreter Mode, allowing real-time execution of URScript commands over TCP.

- `InterpreterModeClient()`
- `void Connect(string ip, int port = 30020)`: Specifies the IP address of the robot. No TCP connection is maintained. A new connection is created when sending each command.
- Inherited from [InterpreterModeClientBase](UnderAutomation.UniversalRobots.InterpreterMode.Internal.md#interpretermodeclientbase-robotinterpretermode): `ExecuteCommand`, `EndInterpreter`, `ClearInterpreter`, `Abort`, `SkipBuffer`, `StateLastExecuted`, `StateLastInterpreted`, `StateLastCleared`, `StateLastUnexecuted`, `Disconnect`, `IP`, `Port`, `Connected`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`
