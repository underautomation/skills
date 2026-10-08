# Telnet overview

Telnet KCL (Keyboard Command Line) sends commands to a Fanuc robot: run programs, reset alarms, read and write variables, control I/O ports.

Web page: https://underautomation.com/fanuc/documentation/telnet

> **Telnet KCL is a legacy protocol.** It is not secured: the password and the commands are sent in clear text. It is hard to maintain: the answers of the controller change with the firmware version, and ROBOGUIDE behaves differently from a real controller. The KCL commands of `robot.Telnet` are also available with `robot.Cgtp.Kcl`, through the web server of the controller (firmware V8.30 and later), without Telnet setup. Prefer it for new developments: see [KCL commands over CGTP](cgtp-kcl.md).

Telnet KCL is a text-based protocol that lets you send commands to a Fanuc robot controller. It requires no paid option and is available on all controllers and ROBOGUIDE.

## Key features

- **Program control**: Run, pause, hold, continue, abort programs
- **Variable access**: Read and write system variables
- **I/O control**: Set output ports, simulate and unsimulate inputs
- **Alarm management**: Reset alarms and errors
- **Debugging**: Add breakpoints, step through code line by line
- **Custom commands**: Send any raw KCL command

## Prerequisites

Telnet must be enabled on your robot controller. See [Enable Telnet on your robot](telnet-enable-on-robot.md) for setup instructions.

## Quick example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Reset alarms
robot.telnet.reset()

# Run a program
robot.telnet.run("MyProgram")
robot.telnet.pause("MyProgram")
robot.telnet.hold("MyProgram")
robot.telnet.continue_("MyProgram")
robot.telnet.abort("MyProgram", force=True)

# Set a variable
robot.telnet.set_variable("$RMT_MASTER", 1)

# Set an output port (DOUT port 2 = 0)
robot.telnet.set_port("DOUT", 2, 0)

# Simulate an input port (DIN port 3 = 1)
robot.telnet.simulate("DIN", 3, 1)
robot.telnet.unsimulate("DIN", 3)
```

## Connection

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.telnet.telnet_client import TelnetClient

# Via FanucRobot
robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "your_password"
robot.connect(parameters)

# Or standalone
telnet = TelnetClient()
telnet.connect("192.168.0.1", "your_password")
```

For ROBOGUIDE, pass the workcell folder path instead of an IP address. The SDK reads `services.txt` to find the correct Telnet port.

## Events

The Telnet client raises events for real-time monitoring:

- `MessageReceived` : Fired when a message is received from the controller
- `RawDataReceived` : Raw byte data from the TCP socket
- `ErrorOccured` : Connection or communication errors
- `CommandSent` / `CommandReceived` : Track sent and received KCL commands
- `TpCoordinatesReceived` : Teach pendant coordinate system changes

## Check if Telnet is available

Via FTP, you can check if Telnet is available on the controller:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

features = robot.ftp.get_summary_diagnostic().features
is_telnet_available = features.has_telnet
```

## Limitations

- **Text-based protocol**: Slower than binary protocols like SNPX for bulk data operations
- **Sequential commands**: Commands are sent one at a time over a single TCP connection
- **No bulk register read**: Variable reading is done by name, not by index. Use SNPX, FTP or CGTP for reading registers in bulk

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Next steps

- [Program control](telnet-program-control.md) : Run, pause, abort programs
- [Variables & I/O](telnet-variables-io.md) : Read/write variables and control ports
- [Debugging & breakpoints](telnet-debugging.md) : Step-by-step debugging

## API reference

**TelnetClient** ([reference](../api/underautomation.fanuc.telnet.md#telnetclient))

- `TelnetClient()`: Create a new instance of a robot communication
- `connect(ip: str, telnetKclPassword: str) -> None`: Connect to a robot
- Inherited from [TelnetClientBase](../api/underautomation.fanuc.telnet.internal.md#telnetclientbase-robottelnet): `poll_and_get_updated_connected_state`, `disconnect`, `ip`, `language`, `tp_coordinates`, `connected`, `raw_data_received`, `string_data_received`, `tp_coordinates_received`, `message_received`, `error_occured`, `command_sent`, `command_received`
- Inherited from [KclClientBase](../api/underautomation.fanuc.common.kcl.md#kclclientbase-robottelnet): `abort`, `abort_all`, `clear_all`, `clear_program`, `clear_vars`, `continue_`, `hold`, `pause`, `reset`, `run`, `set_port`, `set_variable`, `get_current_pose`, `get_variable`, `simulate`, `unsimulate_all`, `unsimulate`, `send_custom_command`, `get_task_information`, `add_breakpoint`, `remove_breakpoint`, `remove_all_breakpoints`, `get_breakpoints`, `step_on`, `step_off`

**TelnetClientBase** ([reference](../api/underautomation.fanuc.telnet.internal.md#telnetclientbase-robottelnet))

- `raw_data_received(handler)`: Occurs when raw data is received.
- `string_data_received(handler)`: Occurs when data is received and its content can successfully be parsed as a string message.
- `tp_coordinates_received(handler)`: Occurs when TP coordinates are received.
- `message_received(handler)`: Occurs when a message is received.
- `error_occured(handler)`: Occurs when an error occurs in the KCL client.
- `command_sent(handler)`: Occurs when a command is sent.
- `command_received(handler)`: Occurs when a KCL command is received.
- `poll_and_get_updated_connected_state() -> bool`: Checks the actual connection status via an active socket polling
- `disconnect() -> None`: Disconnect Telnet client from robot
- `ip: str (read only)`: Connect robot IP address or host name
- `language: Languages`: Controller language (default is English)
- `tp_coordinates: TpCoordinates (read only)`: Gets the current Teach Pendant coordinate system.
- `connected: bool (read only)`: Is Telnet client connected
- Inherited from [KclClientBase](../api/underautomation.fanuc.common.kcl.md#kclclientbase-robottelnet): `abort`, `abort_all`, `clear_all`, `clear_program`, `clear_vars`, `continue_`, `hold`, `pause`, `reset`, `run`, `set_port`, `set_variable`, `get_current_pose`, `get_variable`, `simulate`, `unsimulate_all`, `unsimulate`, `send_custom_command`, `get_task_information`, `add_breakpoint`, `remove_breakpoint`, `remove_all_breakpoints`, `get_breakpoints`, `step_on`, `step_off`
