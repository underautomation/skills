# UnderAutomation.UniversalRobots.InterpreterMode.Internal

## InterpreterModeClientBase (robot.InterpreterMode)

`abstract class InterpreterModeClientBase : URServiceBase`

Base class for the Interpreter Mode client, providing TCP communication and built-in interpreter commands.

- `CommandResponse Abort()`: The interpreter mode offers a mechanism to abort limited number of script functions, even if they are called from the main program. Currently only movej and movel can be aborted. Aborting a movement will result in a controlled stop if no blend radius is defined. If a blend radius is defined then...
- `CommandResponse ClearInterpreter()`: Clears all interpreted statements, objects, functions, threads, etc. generated in the current interpreter mode.Threads started in current interpreter session will be stopped, and deleted. Variables defined outside of the current interpreter mode will not be affected by a call to thisfunction. Onl...
- `bool Connected { get; }`: Indicates that the interpreter mode client is connected and ready to send commands
- `void Disconnect()`: Disconnect interpreter mode socket connection
- `CommandResponse EndInterpreter()`: Ends the interpreter mode, and causes the interpreter_mode() function to return. This function can be compiled into the program by sending it to the interpreter socket(30020) as any other statement, or can be called from anywhere else in the program. By default everything interpreted will be clea...
- `CommandResponse ExecuteCommand(string command)`: Executes a command on the Interpreter Mode
- `string IP { get; }`: IP of the robot to connect to for sending commands
- `int Port { get; set; }`: Interpreter mode server port
- `CommandResponse SkipBuffer()`: The interpreter mode furthermore supports the opportunity to skip already sent but not executed statements.The interpreter thread will then(after finishing the currently executing statement) skip all received but not executed statements. After the skip, the interpreter thread will idle until new...
- `CommandResponse StateLastCleared()`: Replies with the id for the latest statement to be cleared from the interpreter mode. This clear can happen when ending interpreter mode, or by calls to clear_interpreter()
- `CommandResponse StateLastExecuted()`: Replies with the largest id of a statement that has started being executed.
- `CommandResponse StateLastInterpreted()`: Replies with the latest interpreted id, i.e. the highest number of interpreted statement so far.
- `CommandResponse StateLastUnexecuted()`: Replies with the number of non executed statements, i.e. the number of statements that would have be skipped if skipbuffer was called instead.
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## InterpreterModeClientParametersBase

`abstract class InterpreterModeClientParametersBase`

Base class for Interpreter Mode connection parameters.

- `const int DEFAULT_PORT = 30020`: Default Interpreter Mode server TCP port
- `int Port { get; set; }`: Interpreter Mode client TCP port. Default : 30020
