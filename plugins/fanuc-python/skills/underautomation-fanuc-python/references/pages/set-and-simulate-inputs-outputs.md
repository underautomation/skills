# Control inputs & outputs

Set, read, simulate, and unsimulate I/O ports on a Fanuc robot using SNPX, CGTP, or Telnet. Compare port types and methods.

Web page: https://underautomation.com/fanuc/documentation/set-and-simulate-inputs-outputs

Control digital and analog I/O signals on your Fanuc robot: read values, write outputs, simulate inputs, and manage I/O descriptions.

## SNPX (fastest : ~2 ms)

SNPX supports 13 digital and 5 numeric I/O types with single and range operations.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True

# Connect to the robot
robot.connect(parameters)

# --- Digital signals (boolean) ---

# Read a single digital input
sdi10 = robot.snpx.sdi.read(10)

# Write a single digital output
robot.snpx.rdo.write(1, True)

# Read a range of digital inputs (100 signals starting at index 1)
sdi_range = robot.snpx.sdi.read(1, 100)

# Write a range of digital outputs
robot.snpx.sdo.write(1, [True, False, True])

# Other digital signal types: UI, UO, SI, SO, WI, WO, WSI, PMC_K, PMC_R
ui5 = robot.snpx.ui.read(5)
robot.snpx.so.write(3, False)

# --- Numeric I/O (ushort) ---

# Read Group Input
gi1 = robot.snpx.gi.read(1)

# Write Group Output
robot.snpx.go.write(1, 500)

# Read Analog Input
ai1 = robot.snpx.ai.read(1)

# Write Analog Output
robot.snpx.ao.write(2, 32767)

# Read a range of numeric I/O
gi_range = robot.snpx.gi.read(1, 100)

# Other numeric I/O types: PMC_D
pmc_d = robot.snpx.pmc_d.read(1)
```

See also: [SNPX Inputs & Outputs](snpx-io.md)

## CGTP Web Server

CGTP provides read/write/simulate for all standard I/O types:

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

See also: [CGTP Inputs & Outputs](cgtp-io.md)

## Telnet KCL

Telnet can set, simulate, and unsimulate I/O ports:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Set a port value
robot.telnet.set_port("DO", 1, True)

# Simulate a port
robot.telnet.simulate("DI", 5, True)

# Unsimulate a port
robot.telnet.unsimulate("DI", 5)
```

See also: [Telnet Variables & I/O](telnet-variables-io.md)

## Protocol comparison

| Feature | SNPX | CGTP | Telnet |
|---------|------|------|--------|
| **Speed** | ~2 ms | ~50 ms | ~30 ms |
| **Digital I/O types** | 13 types | 5 types + Flag | SDI/SDO/RDI/RDO/UI/UO/SI/SO/WI/WO |
| **Numeric I/O types** | 5 types | AI/AO/GI/GO | GI/GO/AI/AO |
| **Range read/write** | Yes | No | No |
| **Simulate/Unsimulate** | No | Yes | Yes |
| **Batch read** | Yes | No | No |
