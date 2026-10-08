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

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Ssh.Tools;

class SshRunCommand
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // SSH is disabled by default
    parameters.Ssh.EnableSsh = true;

    // "ur" and "easybot" by default
    parameters.Ssh.Username = "root";
    parameters.Ssh.Password = "easybot";

    robot.Connect(parameters);

    // Run a command and wait for its end
    SshCommand command = robot.Ssh.RunCommand("df -h /programs");

    string output = command.Result;  // standard output
    int exitStatus = command.ExitStatus;
  }
}
```

`SshClient` also works without `UR`: `new SshClient()`, then `Connect(ip, username, password)`.

## Open a shell

A shell keeps its session and its working directory, like a terminal. `CreateShellStream` opens one, with a terminal name, a size and a buffer size. `DataReceived` is raised when the shell writes text.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Ssh.Tools;

class SshCreateShell
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");
    parameters.Ssh.EnableSsh = true;

    robot.Connect(parameters);

    // A shell keeps its session and its working directory, like a terminal.
    // Terminal name, columns, rows, width, height, buffer size
    ShellStream shell = robot.Ssh.CreateShellStream("xterm", 80, 24, 800, 600, 1024);

    // Raised for each text written by the shell
    shell.DataReceived += (sender, e) => Console.Write(e.Line);

    shell.WriteLine("cd /programs");
    shell.WriteLine("ls -l");
  }
}
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**SshClient** ([reference](../api/UnderAutomation.UniversalRobots.Ssh.md#sshclient))

- `SshClient()`
- `void Connect(string ip, string username, string password, int port = 22)`: Connects to the robot
- Inherited from [SshClientBase](../api/UnderAutomation.UniversalRobots.Ssh.Internal.md#sshclientbase-robotssh): `Disconnect`, `CreateCommand`, `RunCommand`, `CreateShell`, `CreateShellStream`, `Connected`
- Inherited from [URServiceBase](../api/UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

**ShellStream** ([reference](../api/UnderAutomation.UniversalRobots.Ssh.Tools.md#shellstream))

- `IAsyncResult BeginExpect(AsyncCallback callback, object state, params ExpectAction[] expectActions)`: Begins the expect.
- `IAsyncResult BeginExpect(AsyncCallback callback, params ExpectAction[] expectActions)`: Begins the expect.
- `IAsyncResult BeginExpect(TimeSpan timeout, AsyncCallback callback, object state, params ExpectAction[] expectActions)`: Begins the expect.
- `IAsyncResult BeginExpect(params ExpectAction[] expectActions)`: Begins the expect.
- `bool CanRead { get; }`: Gets a value indicating whether the current stream supports reading.
- `bool CanSeek { get; }`: Gets a value indicating whether the current stream supports seeking.
- `bool CanWrite { get; }`: Gets a value indicating whether the current stream supports writing.
- `bool DataAvailable { get; }`: Gets a value that indicates whether data is available on the Tools.ShellStream to be read.
- `event EventHandler<ShellDataEventArgs> DataReceived`: Occurs when data was received.
- `string EndExpect(IAsyncResult asyncResult)`: Ends the execute.
- `event EventHandler<ExceptionEventArgs> ErrorOccurred`: Occurs when an error occurred.
- `string Expect(string text)`: Expects the expression specified by text.
- `string Expect(string text, TimeSpan timeout)`: Expects the expression specified by text.
- `string Expect(Regex regex)`: Expects the expression specified by regular expression.
- `string Expect(Regex regex, TimeSpan timeout)`: Expects the expression specified by regular expression.
- `void Expect(TimeSpan timeout, params ExpectAction[] expectActions)`: Expects the specified expression and performs action when one is found.
- `void Expect(params ExpectAction[] expectActions)`: Expects the specified expression and performs action when one is found.
- `void Flush()`: Clears all buffers for this stream and causes any buffered data to be written to the underlying device.
- `long Length { get; }`: Gets the length in bytes of the stream.
- `long Position { get; set; }`: Gets or sets the position within the current stream.
- `string Read()`: Reads text available in the shell.
- `int Read(byte[] buffer, int offset, int count)`: Reads a sequence of bytes from the current stream and advances the position within the stream by the number of bytes read.
- `string ReadLine()`: Reads the line from the shell. If line is not available it will block the execution and will wait for new line.
- `string ReadLine(TimeSpan timeout)`: Reads a line from the shell. If line is not available it will block the execution and will wait for new line.
- `long Seek(long offset, SeekOrigin origin)`: This method is not supported.
- `void SetLength(long value)`: This method is not supported.
- `void Write(byte[] buffer, int offset, int count)`: Writes a sequence of bytes to the current stream and advances the current position within this stream by the number of bytes written.
- `void Write(string text)`: Writes the specified text to the shell.
- `void WriteLine(string line)`: Writes the line to the shell.

**SshCommand** ([reference](../api/UnderAutomation.UniversalRobots.Ssh.Tools.md#sshcommand))

- `IAsyncResult BeginExecute()`: Begins an asynchronous command execution.
- `IAsyncResult BeginExecute(AsyncCallback callback)`: Begins an asynchronous command execution.
- `IAsyncResult BeginExecute(AsyncCallback callback, object state)`: Begins an asynchronous command execution.
- `IAsyncResult BeginExecute(string commandText, AsyncCallback callback, object state)`: Begins an asynchronous command execution.
- `void CancelAsync()`: Cancels command execution in asynchronous scenarios.
- `string CommandText { get; }`: Gets the command text.
- `TimeSpan CommandTimeout { get; set; }`: Gets or sets the command timeout.
- `void Dispose()`: Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources.
- `string EndExecute(IAsyncResult asyncResult)`: Waits for the pending asynchronous command execution to complete.
- `string Error { get; }`: Gets the command execution error.
- `string Execute()`: Executes command specified by SshCommand.CommandText property.
- `string Execute(string commandText)`: Executes the specified command text.
- `int ExitStatus { get; }`: Gets the command exit status.
- `Stream ExtendedOutputStream { get; }`: Gets the extended output stream.
- `Stream OutputStream { get; }`: Gets the output stream.
- `string Result { get; }`: Gets the command execution result.
