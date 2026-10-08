# underautomation.universal_robots.interpreter_mode.internal

## InterpreterModeClientBase (robot.interpreter_mode)

`from underautomation.universal_robots.interpreter_mode.internal.interpreter_mode_client_base import InterpreterModeClientBase`

Base class for the Interpreter Mode client, providing TCP communication and built-in interpreter commands.

- `execute_command(command: str) -> CommandResponse`: Executes a command on the Interpreter Mode
- `end_interpreter() -> CommandResponse`: Ends the interpreter mode, and causes the interpreter_mode() function to return. This function can be compiled into the program by sending it to the interpreter socket(30020) as any other statement, or can be called from anywhere else in the program. By default everything interpreted will be clea...
- `clear_interpreter() -> CommandResponse`: Clears all interpreted statements, objects, functions, threads, etc. generated in the current interpreter mode.Threads started in current interpreter session will be stopped, and deleted. Variables defined outside of the current interpreter mode will not be affected by a call to thisfunction. Onl...
- `abort() -> CommandResponse`: The interpreter mode offers a mechanism to abort limited number of script functions, even if they are called from the main program. Currently only movej and movel can be aborted. Aborting a movement will result in a controlled stop if no blend radius is defined. If a blend radius is defined then...
- `skip_buffer() -> CommandResponse`: The interpreter mode furthermore supports the opportunity to skip already sent but not executed statements.The interpreter thread will then(after finishing the currently executing statement) skip all received but not executed statements. After the skip, the interpreter thread will idle until new...
- `state_last_executed() -> CommandResponse`: Replies with the largest id of a statement that has started being executed.
- `state_last_interpreted() -> CommandResponse`: Replies with the latest interpreted id, i.e. the highest number of interpreted statement so far.
- `state_last_cleared() -> CommandResponse`: Replies with the id for the latest statement to be cleared from the interpreter mode. This clear can happen when ending interpreter mode, or by calls to clear_interpreter()
- `state_last_unexecuted() -> CommandResponse`: Replies with the number of non executed statements, i.e. the number of statements that would have be skipped if skipbuffer was called instead.
- `disconnect() -> None`: Disconnect interpreter mode socket connection
- `ip: str (read only)`: IP of the robot to connect to for sending commands
- `port: int`: Interpreter mode server port
- `connected: bool (read only)`: Indicates that the interpreter mode client is connected and ready to send commands
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## InterpreterModeClientParametersBase

`from underautomation.universal_robots.interpreter_mode.internal.interpreter_mode_client_parameters_base import InterpreterModeClientParametersBase`

Base class for Interpreter Mode connection parameters.

- `port: int`: Interpreter Mode client TCP port. Default : 30020
- `static DEFAULT_PORT: int`: Default Interpreter Mode server TCP port
