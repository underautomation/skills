# SSH Linux commands

Run Linux commands on the controller of a UR cobot with SSH, one by one or in a shell that keeps its session.

Web page: https://underautomation.com/universal-robots/documentation/ssh-commands

The controller of a Universal Robots cobot runs Linux. With SSH (Secure Shell), the SDK runs Linux commands on it, one by one or in a shell that keeps its session. This page shows both. To transfer files, see [SFTP](sftp-file-handling.md).

## Prerequisites

- Secure Shell is enabled on the robot. On PolyScope, open `Settings`, `Security`, `Secure Shell`.
- The Linux user and its password: `root` on a robot, `ur` on URSim, `easybot` by default. The SDK uses `ur` and `easybot` when you set nothing.

A command runs with the rights of this user. A wrong command can stop the controller: test it on URSim first.

## Run a command

SSH is disabled by default: set `Ssh.EnableSsh` in `ConnectParameters`. `RunCommand` runs a command and waits for its end. The returned `SshCommand` holds its output and its exit status.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# SSH is disabled by default
parameters.ssh.enable_ssh = True

# "ur" and "easybot" by default
parameters.ssh.username = "root"
parameters.ssh.password = "easybot"

robot.connect(parameters)

# Run a command and wait for its end
command = robot.ssh.run_command("df -h /programs")

output = command.result  # standard output
exit_status = command.exit_status
```

`SshClient` also works without `UR`: `new SshClient()`, then `Connect(ip, username, password)`.

## Open a shell

A shell keeps its session and its working directory, like a terminal. `CreateShellStream` opens one, with a terminal name, a size and a buffer size. `DataReceived` is raised when the shell writes text.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.ssh.tools.common.shell_data_event_args import ShellDataEventArgs

robot = UR()

parameters = ConnectParameters("192.168.0.1")
parameters.ssh.enable_ssh = True

robot.connect(parameters)

# A shell keeps its session and its working directory, like a terminal.
# Terminal name, columns, rows, width, height, buffer size
shell = robot.ssh.create_shell_stream("xterm", 80, 24, 800, 600, 1024)

# Raised for each text written by the shell
def on_data(sender, e):
    print(ShellDataEventArgs(e._instance).line, end="")

shell.data_received(on_data)

shell.write_line("cd /programs")
shell.write_line("ls -l")
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**SshClient** ([reference](../api/underautomation.universal_robots.ssh.md#sshclient))

- `SshClient()`
- `connect(ip: str, username: str, password: str, port: int=22) -> None`: Connects to the robot
- Inherited from [SshClientBase](../api/underautomation.universal_robots.ssh.internal.md#sshclientbase-robotssh): `disconnect`, `create_command`, `run_command`, `create_shell_stream`, `connected`
- Inherited from [URServiceBase](../api/underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

**ShellStream** ([reference](../api/underautomation.universal_robots.ssh.tools.md#shellstream))

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

**SshCommand** ([reference](../api/underautomation.universal_robots.ssh.tools.md#sshcommand))

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
