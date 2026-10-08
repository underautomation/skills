# underautomation.universal_robots.ssh.tools

## ExpectAction

`from underautomation.universal_robots.ssh.tools.expect_action import ExpectAction`

Specifies behavior for expected expression

- `ExpectAction(expect: typing.Any, action: typing.Callable[[str], None])`: Initializes a new instance of the ExpectAction class.
- `expect: typing.Any (read only)`: Gets the expected regular expression.
- `action: typing.Callable[[str], None] (read only)`: Gets the action to perform when expected expression is found.

## Shell

`from underautomation.universal_robots.ssh.tools.shell import Shell`

Represents instance of the SSH shell object

- `starting(handler)`: Occurs when shell is starting.
- `started(handler)`: Occurs when shell is started.
- `stopping(handler)`: Occurs when shell is stopping.
- `stopped(handler)`: Occurs when shell is stopped.
- `error_occurred(handler)`: Occurs when an error occurred.
- `start() -> None`: Starts this shell.
- `stop() -> None`: Stops this shell.
- `dispose() -> None`: Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources.
- `is_started: bool (read only)`: Gets a value indicating whether this shell is started.

## ShellStream

`from underautomation.universal_robots.ssh.tools.shell_stream import ShellStream`

Contains operation for working with SSH Shell.

- `data_received(handler)`: Occurs when data was received.
- `error_occurred(handler)`: Occurs when an error occurred.
- `flush() -> None`: Clears all buffers for this stream and causes any buffered data to be written to the underlying device.
- `read(buffer: typing.List[int], offset: int, count: int) -> int`: Reads a sequence of bytes from the current stream and advances the position within the stream by the number of bytes read.
- `read() -> str`: Reads text available in the shell.
- `set_length(value: int) -> None`: This method is not supported.
- `write(buffer: typing.List[int], offset: int, count: int) -> None`: Writes a sequence of bytes to the current stream and advances the current position within this stream by the number of bytes written.
- `write(text: str) -> None`: Writes the specified text to the shell.
- `expect(expectActions_or_text: str | typing.List[ExpectAction]) -> str | None`: Expects the expression specified by text. Expects the specified expression and performs action when one is found.
- `read_line() -> str`: Reads the line from the shell. If line is not available it will block the execution and will wait for new line.
- `write_line(line: str) -> None`: Writes the line to the shell.
- `data_available: bool (read only)`: Gets a value that indicates whether data is available on the ShellStream to be read.
- `can_read: bool (read only)`: Gets a value indicating whether the current stream supports reading.
- `can_seek: bool (read only)`: Gets a value indicating whether the current stream supports seeking.
- `can_write: bool (read only)`: Gets a value indicating whether the current stream supports writing.
- `length: int (read only)`: Gets the length in bytes of the stream.
- `position: int`: Gets or sets the position within the current stream.

## SshCommand

`from underautomation.universal_robots.ssh.tools.ssh_command import SshCommand`

Represents SSH command that can be executed.

- `execute(commandText: str) -> str`: Executes the specified command text.
- `execute() -> str`: Executes command specified by command_text property.
- `cancel_async() -> None`: Cancels command execution in asynchronous scenarios.
- `dispose() -> None`: Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources.
- `command_text: str (read only)`: Gets the command text.
- `command_timeout: typing.Any`: Gets or sets the command timeout.
- `exit_status: int (read only)`: Gets the command exit status.
- `output_stream: typing.Any (read only)`: Gets the output stream.
- `extended_output_stream: typing.Any (read only)`: Gets the extended output stream.
- `result: str (read only)`: Gets the command execution result.
- `error: str (read only)`: Gets the command execution error.
