# Interpreter Mode

Send URScript statements to a running UR program in interpreter_mode(), follow their execution, skip or clear the buffer, end the mode.

Web page: https://underautomation.com/universal-robots/documentation/interpreter-mode

The Interpreter Mode of a Universal Robots cobot runs URScript statements sent by your application while a robot program is running. Unlike the URScript of the Primary Interface, it does not stop the program: the statements run in the program, and the program continues after them. This page shows how to send statements and follow their execution.

## How it works

1. The robot program calls the URScript function `interpreter_mode()`. The program waits there.
2. The SDK sends statements. The robot adds them to a buffer and runs them in order.
3. The SDK ends the interpreter mode: the robot program continues after `interpreter_mode()`.

![Interpreter mode in PolyScope](https://underautomation.com/universal-robots/interpreter-mode-polyscope.jpg)

See [Interpreter mode](https://www.universal-robots.com/articles/ur/programming/interpreter-mode/) by Universal Robots, and the PolyScope versions that support it.

## Prerequisites

- The service `Interpreter Mode Socket` is enabled on the robot: see [Prepare the robot](connect.md#prepare_the_robot).
- A program that calls `interpreter_mode()` is running.

## Example

Interpreter Mode is disabled by default: set `InterpreterMode.Enable` in `ConnectParameters`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.interpreter_mode.command_response_status import CommandResponseStatus

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# Interpreter Mode is disabled by default
parameters.interpreter_mode.enable = True

robot.connect(parameters)

# The robot program must be in interpreter_mode()
response = robot.interpreter_mode.execute_command("movej([0.94, -1.31, 2.21, -2.65, -1.08, 4.81], a=1, v=0.5)")

if response.status != CommandResponseStatus.Ack:
    print(response.raw_answer)

robot.interpreter_mode.execute_command("set_standard_digital_out(1, True)")

# Id of the last statement executed by the robot
last_executed = robot.interpreter_mode.state_last_executed()

# Remove the statements not executed yet
robot.interpreter_mode.skip_buffer()

# Leave interpreter_mode(): the robot program continues
robot.interpreter_mode.end_interpreter()

# Close Interpreter Mode only
robot.interpreter_mode.disconnect()
```

## Commands

| Method                    | Role                                                                    |
| ------------------------- | ----------------------------------------------------------------------- |
| `ExecuteCommand(script)`  | Add a statement to the buffer. `Ack` when the robot accepts it, `Discard` when it does not compile or no program runs |
| `StateLastExecuted()`     | Largest id of a statement that has started                              |
| `StateLastInterpreted()`  | Largest id of a statement interpreted                                   |
| `StateLastCleared()`      | Id of the last statement cleared, by the end or by `ClearInterpreter()` |
| `StateLastUnexecuted()`   | Number of statements not executed yet                                   |
| `SkipBuffer()`            | Skip the statements not executed yet, after the one that runs           |
| `ClearInterpreter()`      | Clear the statements, functions and threads interpreted so far          |
| `Abort()`                 | Stop the `movej` or `movel` that runs, with a controlled stop           |
| `EndInterpreter()`        | Leave `interpreter_mode()`: the robot program continues                 |

Each method returns a `CommandResponse`: its `Status`, its `Id` and the raw answer of the robot.

The buffer of the robot has a limited size. For a long sequence, follow `StateLastExecuted()` and call `ClearInterpreter()` from time to time.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**InterpreterModeClientBase** ([reference](../api/underautomation.universal_robots.interpreter_mode.internal.md#interpretermodeclientbase-robotinterpreter_mode))

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
- Inherited from [URServiceBase](../api/underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

**CommandResponse** ([reference](../api/underautomation.universal_robots.interpreter_mode.md#commandresponse))

- `status: CommandResponseStatus (read only)`: Response type to check if command succeed
- `id: int (read only)`: Command unique identifier
- `body: str (read only)`: Answer from the interpreter mode
- `raw_answer: str (read only)`: Raw line sent from the controller
- `command: str (read only)`: Command sent to the interpreter mode

**CommandResponseStatus** ([reference](../api/underautomation.universal_robots.interpreter_mode.md#commandresponsestatus))

- Error: Something went wrong when receiving response
- Ack: The command compilation succeed and Interpreter mode will execute the statement
- Discard: Program is not running or the statement results in a compilation or linker error
- State: Answer from a state command

**InterpreterModeConnectParameters** ([reference](../api/underautomation.universal_robots.common.md#interpretermodeconnectparameters))

- `enable: bool`: Enable Interpreter Mode client communication Default value is false
- Inherited from [InterpreterModeClientParametersBase](../api/underautomation.universal_robots.interpreter_mode.internal.md#interpretermodeclientparametersbase): `DEFAULT_PORT`, `port`

## What to read next

- [Send URScript](remote-send-script.md): run URScript without a running program.
- [Move the robot from a PC](how-to-move-robot.md): which way to choose for a move.
