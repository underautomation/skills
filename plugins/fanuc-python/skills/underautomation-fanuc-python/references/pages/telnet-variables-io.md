# Variables & I/O via Telnet

Read and write system variables, set output ports, simulate and unsimulate input ports using Telnet KCL.

Web page: https://underautomation.com/fanuc/documentation/telnet-variables-io

> **Telnet KCL is a legacy protocol.** It is not secured: the password and the commands are sent in clear text. It is hard to maintain: the answers of the controller change with the firmware version, and ROBOGUIDE behaves differently from a real controller. The KCL commands of `robot.Telnet` are also available with `robot.Cgtp.Kcl`, through the web server of the controller (firmware V8.30 and later), without Telnet setup. Prefer it for new developments: see [KCL commands over CGTP](cgtp-kcl.md).

Read and write system variables, set output ports, simulate and unsimulate input ports using Telnet KCL.

## Read and write variables

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Read a variable
result = robot.telnet.get_variable("$RMT_MASTER")
value = result.raw_value

# Write a variable
robot.telnet.set_variable("$RMT_MASTER", 1)
robot.telnet.set_variable("$MCR.$GENOVERRIDE", 50)
robot.telnet.set_variable("$[MY_PROG]my_var", "hello")

# Get current pose
pose = robot.telnet.get_current_pose()
```

You can read any system variable, program variable, or user-defined variable by name. The value must match the declared data type. Use brackets (`[]`) after the variable name to specify an array element.

## Set and simulate I/O ports

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.kcl.kcl_ports import KCLPorts

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Set an output port (DOUT port 2 = OFF)
robot.telnet.set_port(KCLPorts.DOUT, 2, 0)

# Set an output port (DOUT port 5 = ON)
robot.telnet.set_port(KCLPorts.DOUT, 5, 1)

# Simulate an input port (DIN port 3 = ON)
robot.telnet.simulate(KCLPorts.DIN, 3, 1)

# Stop simulating DIN port 3
robot.telnet.unsimulate(KCLPorts.DIN, 3)

# Stop simulating all ports
robot.telnet.unsimulate_all()
```

## Available port types

The `KCLPorts` enum defines the available port types:

| Port | Description |
|------|-------------|
| `DIN` / `DOUT` | Digital Input / Output |
| `GIN` / `GOUT` | Group Input / Output |
| `AIN` / `AOUT` | Analog Input / Output |
| `OPIN` / `OPOUT` | Operator Panel Input / Output |
| `RDI` / `RDO` | Robot Digital Input / Output |
| `WDI` / `WDO` | Weld Digital Input / Output |
| `PLCIN` / `PLCOUT` | PLC Input / Output |
| `FLAG` | Flag register |

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.kcl.kcl_ports import KCLPorts

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Read a system variable
result = robot.telnet.get_variable("$RMT_MASTER")
value = result.raw_value

# Write system variables
robot.telnet.set_variable("$RMT_MASTER", 1)
robot.telnet.set_variable("$MCR.$GENOVERRIDE", 50)

# Get current TCP pose
pose = robot.telnet.get_current_pose()

# Set an output port
robot.telnet.set_port(KCLPorts.DOUT, 2, 0)
robot.telnet.set_port(KCLPorts.DOUT, 5, 1)

# Simulate an input port
robot.telnet.simulate(KCLPorts.DIN, 3, 1)

# Stop simulating a port
robot.telnet.unsimulate(KCLPorts.DIN, 3)

# Stop simulating all ports
robot.telnet.unsimulate_all()
```

## API reference

**GetVariableResult** ([reference](../api/underautomation.fanuc.common.kcl.md#getvariableresult))

- `GetVariableResult()`
- `parse_result() -> GenericVariable`: Returns a structured object which represents the variable (not supported with Telnet)
- `raw_value: str (read only)`: Gets the raw value of the variable as a string.
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**SetVariableResult** ([reference](../api/underautomation.fanuc.common.kcl.md#setvariableresult))

- `SetVariableResult()`
- Inherited from [SetValueResult](../api/underautomation.fanuc.common.kcl.md#setvalueresult): `former_value`, `new_value`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**SetPortResult** ([reference](../api/underautomation.fanuc.common.kcl.md#setportresult))

- `SetPortResult()`
- Inherited from [SetValueResult](../api/underautomation.fanuc.common.kcl.md#setvalueresult): `former_value`, `new_value`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**SimulateResult** ([reference](../api/underautomation.fanuc.common.kcl.md#simulateresult))

- `SimulateResult()`
- Inherited from [Result](../api/underautomation.fanuc.common.kcl.md#result): `error_text`, `succeed`, `kcl_command`

**KCLPorts** ([reference](../api/underautomation.fanuc.common.kcl.md#kclports))

- DIN: Digital Input port.
- DOUT: Digital Output port.
- RDO: Robot Digital Output port.
- OPOUT: Operator Panel Output port.
- TPOUT: Teach Pendant Output port.
- WDI: Weld Digital Input port.
- WDO: Weld Digital Output port.
- AIN: Analog Input port.
- AOUT: Analog Output port.
- GIN: General Input port.
- GOUT: General Output port.
