# UnderAutomation.UniversalRobots.Ssh.Tools.Common

## ExceptionEventArgs

`class ExceptionEventArgs : EventArgs`

Provides data for the ErrorOccured events.

- `ExceptionEventArgs(Exception exception)`: Initializes a new instance of the Common.ExceptionEventArgs class.
- `Exception Exception { get; }`: Gets the System.Exception that represents the error that occurred.

## SftpPathNotFoundException

`class SftpPathNotFoundException : SshException, ISerializable`

The exception that is thrown when file or directory is not found.

- `SftpPathNotFoundException()`: Initializes a new instance of the Common.SftpPathNotFoundException class.
- `SftpPathNotFoundException(string message)`: Initializes a new instance of the Common.SftpPathNotFoundException class.
- `SftpPathNotFoundException(string message, Exception innerException)`: Initializes a new instance of the Common.SftpPathNotFoundException class.

## SftpPermissionDeniedException

`class SftpPermissionDeniedException : SshException, ISerializable`

The exception that is thrown when operation permission is denied.

- `SftpPermissionDeniedException()`: Initializes a new instance of the Common.SftpPermissionDeniedException class.
- `SftpPermissionDeniedException(string message)`: Initializes a new instance of the Common.SftpPermissionDeniedException class.
- `SftpPermissionDeniedException(string message, Exception innerException)`: Initializes a new instance of the Common.SftpPermissionDeniedException class.

## ShellDataEventArgs

`class ShellDataEventArgs : EventArgs`

Provides data for Shell DataReceived event

- `ShellDataEventArgs(byte[] data)`: Initializes a new instance of the Common.ShellDataEventArgs class.
- `ShellDataEventArgs(string line)`: Initializes a new instance of the Common.ShellDataEventArgs class.
- `byte[] Data { get; }`: Gets the data.
- `string Line { get; }`: Gets the line data.

## SshAuthenticationException

`class SshAuthenticationException : SshException, ISerializable`

The exception that is thrown when authentication failed.

- `SshAuthenticationException()`: Initializes a new instance of the Common.SshAuthenticationException class.
- `SshAuthenticationException(string message)`: Initializes a new instance of the Common.SshAuthenticationException class.
- `SshAuthenticationException(string message, Exception innerException)`: Initializes a new instance of the Common.SshAuthenticationException class.

## SshConnectionException

`class SshConnectionException : SshException, ISerializable`

The exception that is thrown when connection was terminated.

- `SshConnectionException()`: Initializes a new instance of the Common.SshConnectionException class.
- `SshConnectionException(string message)`: Initializes a new instance of the Common.SshConnectionException class.

## SshException

`class SshException : Exception, ISerializable`

The exception that is thrown when SSH exception occurs.

- `SshException()`: Initializes a new instance of the Common.SshException class.
- `SshException(string message)`: Initializes a new instance of the Common.SshException class.
- `SshException(string message, Exception inner)`: Initializes a new instance of the Common.SshException class.

## SshOperationTimeoutException

`class SshOperationTimeoutException : SshException, ISerializable`

The exception that is thrown when operation is timed out.

- `SshOperationTimeoutException()`: Initializes a new instance of the Common.SshOperationTimeoutException class.
- `SshOperationTimeoutException(string message)`: Initializes a new instance of the Common.SshOperationTimeoutException class.
- `SshOperationTimeoutException(string message, Exception innerException)`: Initializes a new instance of the Common.SshOperationTimeoutException class.

## SshPassPhraseNullOrEmptyException

`class SshPassPhraseNullOrEmptyException : SshException, ISerializable`

The exception that is thrown when pass phrase for key file is empty or null

- `SshPassPhraseNullOrEmptyException()`: Initializes a new instance of the Common.SshPassPhraseNullOrEmptyException class.
- `SshPassPhraseNullOrEmptyException(string message)`: Initializes a new instance of the Common.SshPassPhraseNullOrEmptyException class.
- `SshPassPhraseNullOrEmptyException(string message, Exception innerException)`: Initializes a new instance of the Common.SshPassPhraseNullOrEmptyException class.

## TerminalModes

`enum TerminalModes : byte`

Specifies the initial assignments of the opcode values that are used in the 'encoded terminal modes' valu

- CS7: 7 bit mode.
- CS8: 8 bit mode.
- ECHO: Enable echoing.
- ECHOCTL: Echo control characters as ^(Char).
- ECHOE: Visually erase chars.
- ECHOK: Kill character discards current line.
- ECHOKE: Visual erase for line kill.
- ECHONL: Echo NL even if ECHO is off.
- ICANON: Canonicalize input lines.
- ICRNL: Map CR to NL on input.
- IEXTEN: Enable extensions.
- IGNCR: Ignore CR on input.
- IGNPAR: The ignore parity flag. The parameter SHOULD be 0 if this flag is FALSE, and 1 if it is TRUE.
- IMAXBEL: Ring bell on input queue full.
- INLCR: Map NL into CR on input.
- INPCK: Enable checking of parity errors.
- ISIG: Enable signals INTR, QUIT, [D]SUSP.
- ISTRIP: Strip 8th bit off characters.
- IUCLC: Translate uppercase characters to lowercase.
- IUTF8: Terminal input and output is assumed to be encoded in UTF-8.
- IXANY: Any char will restart after stop.
- IXOFF: Enable input flow control.
- IXON: Enable output flow control.
- NOFLSH: Don't flush after interrupt.
- OCRNL: Translate carriage return to newline (output).
- OLCUC: Convert lowercase to uppercase.
- ONLCR: Map NL to CR-NL.
- ONLRET: Newline performs a carriage return (output).
- ONOCR: Translate newline to carriage return-newline (output).
- OPOST: Enable output processing.
- PARENB: Parity enable.
- PARMRK: Mark parity and framing errors.
- PARODD: Odd parity, else even.
- PENDIN: Retype pending input.
- TOSTOP: Stop background jobs from output.
- TTY_OP_END: Indicates end of options.
- TTY_OP_ISPEED: Specifies the input baud rate in bits per second.
- TTY_OP_OSPEED: Specifies the output baud rate in bits per second.
- VDISCARD: Toggles the flushing of terminal output.
- VDSUSP: Another suspend character.
- VEOF: End-of-file character (sends EOF from the terminal).
- VEOL: End-of-line character in addition to carriage return and/or linefeed.
- VEOL2: Additional end-of-line character.
- VERASE: Erase the character to left of the cursor.
- VFLUSH: Character to flush output.
- VINTR: Interrupt character; 255 if none. Similarly for the other characters. Not all of these characters are supported on all systems.
- VKILL: Kill the current input line.
- VLNEXT: Enter the next character typed literally, even if it is a special character
- VQUIT: The quit character (sends SIGQUIT signal on POSIX systems).
- VREPRINT: Reprints the current input line.
- VSTART: Continues paused output (normally control-Q).
- VSTATUS: Prints system status line (load, command, pid, etc).
- VSTOP: Pauses output (normally control-S).
- VSUSP: Suspends the current program.
- VSWTCH: Switch to a different shell layer.
- VWERASE: Erases a word left of cursor.
- XCASE: Enable input and output of uppercase characters by preceding their lowercase equivalents with "\".
