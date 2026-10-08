# UnderAutomation.UniversalRobots.Ssh.Tools

## ExpectAction

`class ExpectAction`

Specifies behavior for expected expression

- `ExpectAction(string expect, Action<string> action)`: Initializes a new instance of the Tools.ExpectAction class.
- `ExpectAction(Regex expect, Action<string> action)`: Initializes a new instance of the Tools.ExpectAction class.
- `Action<string> Action { get; }`: Gets the action to perform when expected expression is found.
- `Regex Expect { get; }`: Gets the expected regular expression.

## Shell

`class Shell : IDisposable`

Represents instance of the SSH shell object

- `void Dispose()`: Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources.
- `event EventHandler<ExceptionEventArgs> ErrorOccurred`: Occurs when an error occurred.
- `bool IsStarted { get; }`: Gets a value indicating whether this shell is started.
- `void Start()`: Starts this shell.
- `event EventHandler<EventArgs> Started`: Occurs when shell is started.
- `event EventHandler<EventArgs> Starting`: Occurs when shell is starting.
- `void Stop()`: Stops this shell.
- `event EventHandler<EventArgs> Stopped`: Occurs when shell is stopped.
- `event EventHandler<EventArgs> Stopping`: Occurs when shell is stopping.

## ShellStream

`class ShellStream : Stream, IDisposable, IAsyncDisposable`

Contains operation for working with SSH Shell.

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

## SshCommand

`class SshCommand : IDisposable`

Represents SSH command that can be executed.

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
