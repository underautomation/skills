# Program control via Telnet

Run, pause, hold, continue, and abort TP and Karel programs remotely using Telnet KCL commands.

Web page: https://underautomation.com/fanuc/documentation/telnet-program-control

> **Telnet KCL is a legacy protocol.** It is not secured: the password and the commands are sent in clear text. It is hard to maintain: the answers of the controller change with the firmware version, and ROBOGUIDE behaves differently from a real controller. The KCL commands of `robot.Telnet` are also available with `robot.Cgtp.Kcl`, through the web server of the controller (firmware V8.30 and later), without Telnet setup. Prefer it for new developments: see [KCL commands over CGTP](cgtp-kcl.md).

Run, pause, hold, continue, and abort TP and Karel programs remotely using Telnet KCL commands.

## Run, pause, hold, continue

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Run the default program
robot.telnet.run()

# Run a specific program
robot.telnet.run("MyProgram")

# Pause a running program (stops at the next fine point)
robot.telnet.pause("MyProgram")

# Force pause immediately
robot.telnet.pause("MyProgram", force=True)

# Hold a program (stops at the current position)
robot.telnet.hold("MyProgram")

# Resume a paused or held program
robot.telnet.continue_("MyProgram")
```

**Pause** stops at the next motion fine point. **Hold** decelerates the robot to stop at the current position.

## Abort, clear, and reset

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Abort a specific program
robot.telnet.abort("MyProgram", force=True)

# Abort all running programs
robot.telnet.abort_all(force=True)

# Clear all programs from memory
robot.telnet.clear_all()

# Clear a specific program
robot.telnet.clear_program("MyProgram")

# Clear variables of a specific program
robot.telnet.clear_vars("MyProgram")

# Reset alarms and re-enable servo power
robot.telnet.reset()
```

The `Reset()` command has the same effect as the FAULT RESET button on the operator panel. The error message remains displayed if the error condition still exists.

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Run a program
robot.telnet.run("MyProgram")

# Pause (stops at next fine point)
robot.telnet.pause("MyProgram")

# Hold (decelerates and stops at current position)
robot.telnet.hold("MyProgram")

# Resume a paused or held program
robot.telnet.continue_("MyProgram")

# Abort a program
robot.telnet.abort("MyProgram", force=True)

# Abort all running programs
robot.telnet.abort_all(force=True)

# Reset alarms (same as FAULT RESET button)
robot.telnet.reset()

# Clear program variables
robot.telnet.clear_vars("MyProgram")
```

## API reference

**RunResult** ([reference](../api/underautomation.fanuc.common.kcl.md#runresult))

- `RunResult()`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**ProgramCommandResult** ([reference](../api/underautomation.fanuc.common.kcl.md#programcommandresult))

- `ProgramCommandResult()`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`
