# Inputs & Outputs

Read, write, simulate, and unsimulate digital, analog, group, and robot I/O ports via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-io

CGTP enables reading, writing, simulating, and unsimulating I/O ports on your Fanuc robot. Requires firmware **V8.30+**.

## Supported I/O types

| `CgtpIoPortType` | Description |
|-------------------|-------------|
| `DI` / `DO` | Digital Input / Output |
| `AI` / `AO` | Analog Input / Output |
| `RI` / `RO` | Robot Input / Output |
| `GI` / `GO` | Group Input / Output |
| `Flag` | Flags (F[]) |

## Read & Write I/O

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read I/O
di1 = robot.cgtp.read_io("DI", 1)
ao5 = robot.cgtp.read_io("AO", 5)
flag10 = robot.cgtp.read_io("Flag", 10)

# Write I/O
robot.cgtp.write_io("DO", 1, 1)
robot.cgtp.write_io("AO", 1, 500)
robot.cgtp.write_io("GO", 1, 255)
```


## Simulate and unsimulate

Simulation forces an I/O to a specific value, ignoring the physical signal:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Simulate DI[5]
robot.cgtp.simulate_io("DI", 5)

# Check if DI[5] is simulated
is_simulated = robot.cgtp.get_io_simulation_status("DI", 5)

# Unsimulate DI[5]
robot.cgtp.unsimulate_io("DI", 5)
```

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.cgtp.cgtp_io_port_type import CgtpIoPortType

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.cgtp.enable = True

# Connect to the robot
robot.connect(parameters)

# Read digital input
di1 = robot.cgtp.read_io(CgtpIoPortType.DI, 1)

# Write digital output
robot.cgtp.write_io(CgtpIoPortType.DO, 1, 1)

# Read analog input
ai1 = robot.cgtp.read_io(CgtpIoPortType.AI, 1)

# Write analog output
robot.cgtp.write_io(CgtpIoPortType.AO, 1, 500)

# Read group input
gi1 = robot.cgtp.read_io(CgtpIoPortType.GI, 1)

# Write group output
robot.cgtp.write_io(CgtpIoPortType.GO, 1, 255)

# Read/write robot I/O
ri1 = robot.cgtp.read_io(CgtpIoPortType.RI, 1)
robot.cgtp.write_io(CgtpIoPortType.RO, 1, 1)

# Read/write flag
flag = robot.cgtp.read_io(CgtpIoPortType.Flag, 10)
robot.cgtp.write_io(CgtpIoPortType.Flag, 10, 1)

# Simulate an I/O
robot.cgtp.simulate_io(CgtpIoPortType.DI, 5)

# Check simulation status
is_simulated = robot.cgtp.get_io_simulation_status(CgtpIoPortType.DI, 5)

# Unsimulate
robot.cgtp.unsimulate_io(CgtpIoPortType.DI, 5)
```

## API reference

**CgtpIoPortType** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpioporttype))

- DI: Digital input.
- DO: Digital output.
- AI: Analog input.
- AO: Analog output.
- RI: Robot input.
- RO: Robot output.
- GI: Group input.
- GO: Group output.
- Flag: Flag.
