# underautomation.universal_robots.ssh.tools.common

## ExceptionEventArgs

`from underautomation.universal_robots.ssh.tools.common.exception_event_args import ExceptionEventArgs`

Provides data for the ErrorOccured events.

- `ExceptionEventArgs(exception: typing.Any)`: Initializes a new instance of the ExceptionEventArgs class.
- `exception: typing.Any (read only)`: Gets the System.Exception that represents the error that occurred.

## SftpPathNotFoundException

`from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SftpPathNotFoundException`

The exception that is thrown when file or directory is not found.

The SDK raises this .NET type: catch it with `except SftpPathNotFoundException as e` after the import above. Its members keep their .NET names. The class `SftpPathNotFoundException` of the module `underautomation.universal_robots.ssh.tools.common.sftp_path_not_found_exception` is not a Python exception and cannot be caught.

- Inherited from System.Exception: `Message`, `InnerException`

## SftpPermissionDeniedException

`from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SftpPermissionDeniedException`

The exception that is thrown when operation permission is denied.

The SDK raises this .NET type: catch it with `except SftpPermissionDeniedException as e` after the import above. Its members keep their .NET names. The class `SftpPermissionDeniedException` of the module `underautomation.universal_robots.ssh.tools.common.sftp_permission_denied_exception` is not a Python exception and cannot be caught.

- Inherited from System.Exception: `Message`, `InnerException`

## ShellDataEventArgs

`from underautomation.universal_robots.ssh.tools.common.shell_data_event_args import ShellDataEventArgs`

Provides data for Shell DataReceived event

- `ShellDataEventArgs(data: typing.List[int])`: Initializes a new instance of the ShellDataEventArgs class.
- `data: typing.List[int] (read only)`: Gets the data.
- `line: str (read only)`: Gets the line data.

## SshAuthenticationException

`from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshAuthenticationException`

The exception that is thrown when authentication failed.

The SDK raises this .NET type: catch it with `except SshAuthenticationException as e` after the import above. Its members keep their .NET names. The class `SshAuthenticationException` of the module `underautomation.universal_robots.ssh.tools.common.ssh_authentication_exception` is not a Python exception and cannot be caught.

- Inherited from System.Exception: `Message`, `InnerException`

## SshConnectionException

`from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshConnectionException`

The exception that is thrown when connection was terminated.

The SDK raises this .NET type: catch it with `except SshConnectionException as e` after the import above. Its members keep their .NET names. The class `SshConnectionException` of the module `underautomation.universal_robots.ssh.tools.common.ssh_connection_exception` is not a Python exception and cannot be caught.

- Inherited from System.Exception: `Message`, `InnerException`

## SshException

`from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshException`

The exception that is thrown when SSH exception occurs.

The SDK raises this .NET type: catch it with `except SshException as e` after the import above. Its members keep their .NET names. The class `SshException` of the module `underautomation.universal_robots.ssh.tools.common.ssh_exception` is not a Python exception and cannot be caught.

- Inherited from System.Exception: `Message`, `InnerException`

## SshOperationTimeoutException

`from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshOperationTimeoutException`

The exception that is thrown when operation is timed out.

The SDK raises this .NET type: catch it with `except SshOperationTimeoutException as e` after the import above. Its members keep their .NET names. The class `SshOperationTimeoutException` of the module `underautomation.universal_robots.ssh.tools.common.ssh_operation_timeout_exception` is not a Python exception and cannot be caught.

- Inherited from System.Exception: `Message`, `InnerException`

## SshPassPhraseNullOrEmptyException

`from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshPassPhraseNullOrEmptyException`

The exception that is thrown when pass phrase for key file is empty or null

The SDK raises this .NET type: catch it with `except SshPassPhraseNullOrEmptyException as e` after the import above. Its members keep their .NET names. The class `SshPassPhraseNullOrEmptyException` of the module `underautomation.universal_robots.ssh.tools.common.ssh_pass_phrase_null_or_empty_exception` is not a Python exception and cannot be caught.

- Inherited from System.Exception: `Message`, `InnerException`

## TerminalModes

`from underautomation.universal_robots.ssh.tools.common.terminal_modes import TerminalModes`

Specifies the initial assignments of the opcode values that are used in the 'encoded terminal modes' valu

- TTY_OP_END: Indicates end of options.
- VINTR: Interrupt character; 255 if none. Similarly for the other characters. Not all of these characters are supported on all systems.
- VQUIT: The quit character (sends SIGQUIT signal on POSIX systems).
- VERASE: Erase the character to left of the cursor.
- VKILL: Kill the current input line.
- VEOF: End-of-file character (sends EOF from the terminal).
- VEOL: End-of-line character in addition to carriage return and/or linefeed.
- VEOL2: Additional end-of-line character.
- VSTART: Continues paused output (normally control-Q).
- VSTOP: Pauses output (normally control-S).
- VSUSP: Suspends the current program.
- VDSUSP: Another suspend character.
- VREPRINT: Reprints the current input line.
- VWERASE: Erases a word left of cursor.
- VLNEXT: Enter the next character typed literally, even if it is a special character
- VFLUSH: Character to flush output.
- VSWTCH: Switch to a different shell layer.
- VSTATUS: Prints system status line (load, command, pid, etc).
- VDISCARD: Toggles the flushing of terminal output.
- IGNPAR: The ignore parity flag. The parameter SHOULD be 0 if this flag is FALSE, and 1 if it is TRUE.
- PARMRK: Mark parity and framing errors.
- INPCK: Enable checking of parity errors.
- ISTRIP: Strip 8th bit off characters.
- INLCR: Map NL into CR on input.
- IGNCR: Ignore CR on input.
- ICRNL: Map CR to NL on input.
- IUCLC: Translate uppercase characters to lowercase.
- IXON: Enable output flow control.
- IXANY: Any char will restart after stop.
- IXOFF: Enable input flow control.
- IMAXBEL: Ring bell on input queue full.
- IUTF8: Terminal input and output is assumed to be encoded in UTF-8.
- ISIG: Enable signals INTR, QUIT, [D]SUSP.
- ICANON: Canonicalize input lines.
- XCASE: Enable input and output of uppercase characters by preceding their lowercase equivalents with "\".
- ECHO: Enable echoing.
- ECHOE: Visually erase chars.
- ECHOK: Kill character discards current line.
- ECHONL: Echo NL even if ECHO is off.
- NOFLSH: Don't flush after interrupt.
- TOSTOP: Stop background jobs from output.
- IEXTEN: Enable extensions.
- ECHOCTL: Echo control characters as ^(Char).
- ECHOKE: Visual erase for line kill.
- PENDIN: Retype pending input.
- OPOST: Enable output processing.
- OLCUC: Convert lowercase to uppercase.
- ONLCR: Map NL to CR-NL.
- OCRNL: Translate carriage return to newline (output).
- ONOCR: Translate newline to carriage return-newline (output).
- ONLRET: Newline performs a carriage return (output).
- CS7: 7 bit mode.
- CS8: 8 bit mode.
- PARENB: Parity enable.
- PARODD: Odd parity, else even.
- TTY_OP_ISPEED: Specifies the input baud rate in bits per second.
- TTY_OP_OSPEED: Specifies the output baud rate in bits per second.
