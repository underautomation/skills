# Inputs & Outputs

Read and write digital signals (SDI, SDO, RDI, RDO, UI, UO, SI, SO, WI, WO) and numeric I/O (GI, GO, AI, AO) via SNPX.

Web page: https://underautomation.com/fanuc/documentation/snpx-io

SNPX supports 13 digital signal types and 5 numeric I/O types, all with single and range read/write operations.

## Digital signals

Digital signals are boolean values. The following types are available:

| Type | Description |
|------|-------------|
| `SDI` / `SDO` | Standard Digital Input / Output |
| `RDI` / `RDO` | Robot Digital Input / Output |
| `UI` / `UO` | User Input / Output |
| `SI` / `SO` | System Input / Output |
| `WI` / `WO` | Weld Input / Output |
| `WSI` | Wire Stick Input |
| `PMC_K` | PMC Keep Relays |
| `PMC_R` | PMC Internal Relays |

### Read and write digital signals

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Read SDI[10]
sdi10 = robot.snpx.sdi.read(10)

# Write RDO[1] = ON
robot.snpx.rdo.write(1, True)

# Read UI[5]
ui5 = robot.snpx.ui.read(5)

# Read 100 SDI signals starting at index 1
values = robot.snpx.sdi.read(1, 100)

# Write 3 SDO signals starting at index 1
robot.snpx.sdo.write(1, [True, False, True])
```

## Numeric I/O

Numeric I/O signals are 16-bit unsigned integers (ushort):

| Type | Description |
|------|-------------|
| `GI` / `GO` | Group Input / Output |
| `AI` / `AO` | Analog Input / Output |
| `PMC_D` | PMC Data |

### Read and write numeric I/O

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Read GI[1]
gi1 = robot.snpx.gi.read(1)

# Write GO[1] = 500
robot.snpx.go.write(1, 500)

# Read AI[1]
ai1 = robot.snpx.ai.read(1)

# Write AO[2] = 32767
robot.snpx.ao.write(2, 32767)

# Read a range of GI values
gi_values = robot.snpx.gi.read(1, 100)
```

## Complete example

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

## API reference

**DigitalSignals** ([reference](../api/underautomation.fanuc.snpx.internal.md#digitalsignals-robotsnpxsdi))

- `read(firstIndex: int, count: int) -> typing.List[bool]`: Reads a range of digital signals.
- `read(index: int) -> bool`: Reads the digital signal at the specified index.
- `write(firstIndex_or_index: int, value_or_values: bool | typing.List[bool]) -> None`: Writes a value to the digital signal at the specified index. Writes values to consecutive digital signals.
- `segment_name: SegmentName (read only)`: Gets the segment name identifying this signal group.

**NumericIO** ([reference](../api/underautomation.fanuc.snpx.internal.md#numericio-robotsnpxgi))

- `read(firstIndex: int, count: int) -> typing.List[int]`: Reads a range of numeric I/O values.
- `read(index: int) -> int`: Reads the numeric I/O value at the specified index.
- `write(firstIndex_or_index: int, value_or_values: int | typing.List[int]) -> None`: Writes a value to the numeric I/O at the specified index. Writes values to consecutive numeric I/O.
- `segment_name: SegmentName (read only)`: Gets the segment name identifying this I/O group.
