# SNPX overview

SNPX (also known as RobotIF or SRTP) is a high-speed protocol for reading and writing registers, variables, I/O signals, alarms, and positions in less than 2 ms.

Web page: https://underautomation.com/fanuc/documentation/snpx

SNPX (also known as RobotIF, Robot Interface, or SRTP) is a high-performance binary protocol for reading and writing data on a Fanuc robot controller in less than 2 ms.

## Key features

- **Registers**: Read/write numeric (R[]), position (PR[]), string (SR[]), and flag (F[]) registers
- **I/O signals**: Read/write 13 digital signal types and 5 numeric I/O types
- **System variables**: Read/write integer, real, position, and string variables
- **Current position**: Read world and user frame positions for any group
- **Alarms**: Read active alarm, alarm history, clear alarms
- **Task monitoring**: Read running program status, line number, and caller
- **Batch reading**: Read groups of data in a single command for maximum throughput
- **Comments**: Read/write descriptions for registers and I/O

## Quick example

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

# Read a register
pos_reg1 = robot.snpx.position_registers.read(1)
num_reg5 = robot.snpx.numeric_registers.read(5)
str_reg10 = robot.snpx.string_registers.read(10)

# Write a register
pos_reg1.cartesian_position.x = 100
robot.snpx.position_registers.write(1, pos_reg1)
robot.snpx.numeric_registers.write(2, 123.45)
robot.snpx.string_registers.write(3, "Hello, world!")

# Read a variable
rmt_master = robot.snpx.integer_system_variables.read("$RMT_MASTER")
last_alm = robot.snpx.string_system_variables.read("$ALM_IF.$LAST_ALM")
cell_floor = robot.snpx.position_system_variables.read("$CELL_FLOOR")

# Write a system variable
robot.snpx.integer_system_variables.write("$RMT_MASTER", 1)
robot.snpx.string_system_variables.write("$ALM_IF.$LAST_ALM", "No alarms")
robot.snpx.position_system_variables.write("$CELL_FLOOR", cell_floor)

# Write a Karel program variable
robot.snpx.integer_system_variables.write("$[KarelProgram]KarelVariable", 1)

# Read and Write I/O (SDI,SDO,RDI,RDO,UI,UO,SI,SO,WI,WO,WSI,PMC_K,PMC_R)
robot.snpx.rdo.write(1, True)
ai5 = robot.snpx.ai.read(5)

# Read and Write analogs (AI,AO,GI,GO,PMC_D)
robot.snpx.ao.write(2, 5)
ao3 = robot.snpx.ao.read(3)

# Clear alarms
robot.snpx.clear_alarms()
```

## Differences with official Fanuc Robot Interface

Fanuc provides its own Robot Interface client (FRRJIF.DLL). Here are the main differences:

|  | **UnderAutomation SDK** | **Fanuc FRRJIF.DLL** |
| --- | --- | --- |
| **Publisher** | UnderAutomation | Fanuc Ltd. |
| **Technology** | 100% managed .NET assembly | Native ActiveX / COM |
| **Dependencies** | No dependencies, single DLL | Requires PCDK installation |
| **Typical read time** | 2 ms | 30 ms |
| **Cross platform** | Windows, Linux, macOS | Windows only |
| **Languages** | C#, Python, LabVIEW | COM-compatible languages |

## Robot options

To enable SNPX on your robot, you need one of the following:

- **FANUC America (R650 FRA)**: Option R553 "HMI Device SNPX" is required
- **FANUC Ltd. (R651 FRL)**: No additional option needed

TCP port **60008** (Robot IF Server) must be accessible on your controller.

## Performance

SNPX is the fastest protocol in the SDK. Regardless of the amount of data transported in a single command, execution time remains constant at approximately **2 ms**.

For example, you can read 80 position registers in a single batch in the same time as reading a single variable.

When used with ROBOGUIDE, execution times under 1 ms can be achieved.

## Connection

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.snpx.snpx_client import SnpxClient

# Via FanucRobot
robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Or standalone
snpx = SnpxClient()
snpx.connect("192.168.0.1")
```

## Check if SNPX is available

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
is_snpx_available = features.has_snpx
```

## Next steps

- [Registers](snpx-registers.md) : R[], PR[], SR[], F[]
- [Inputs & Outputs](snpx-io.md) : Digital and numeric signals
- [System variables](snpx-variables.md) : Integer, real, position, string variables
- [Current position](snpx-position.md) : World and user frame positions
- [Alarms & task status](snpx-alarms-tasks.md) : Alarm management and task monitoring
- [Batch reading](snpx-batch.md) : High-performance batch operations

## Demonstration

The SNPX page of the demo application reads and writes registers, variables and signals without writing code.

![SNPX](https://underautomation.com/fanuc/snpx.gif)

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**SnpxClient** ([reference](../api/underautomation.fanuc.snpx.md#snpxclient))

- `SnpxClient()`: Initializes a new instance of the SnpxClient class.
- `connect(ip: str, port: int=60008) -> None`: Connects to a Fanuc robot using the SNPX protocol.
- Inherited from [SnpxClientBase](../api/underautomation.fanuc.snpx.internal.md#snpxclientbase-robotsnpx): `poll_and_get_updated_connected_state`, `disconnect`, `clear_alarms`, `set_variable`, `clear_assignments`, `get_assignments`, `ip`, `numeric_registers`, `numeric_registers_int32`, `numeric_registers_int16`, `position_registers`, `string_registers`, `integer_system_variables`, `real_system_variables`, `position_system_variables`, `string_system_variables`, `digital_signals`, `sdi`, `sdo`, `rdi`, `rdo`, `ui`, `uo`, `si`, `so`, `wi`, `wo`, `wsi`, `pmc_k`, `pmc_r`, `numeric_i_os`, `gi`, `go`, `ai`, `ao`, `pmc_d`, `flags`, `current_position`, `current_task_status`, `active_alarm`, `alarm_history`, `comments`, `simulation_status`, `language`, `connected`

**SnpxClientBase** ([reference](../api/underautomation.fanuc.snpx.internal.md#snpxclientbase-robotsnpx))

- `poll_and_get_updated_connected_state() -> bool`: Checks the actual connection status via an active socket polling
- `disconnect() -> None`: Disconnect from the robot
- `clear_alarms() -> None`: Clear all active alarms
- `set_variable(name: str, value: bool | float | int | str) -> None`: Set boolean variable without assignments. Set double variable without assignments. Set integer variable without assignments. Set string variable without assignments.
- `clear_assignments() -> None`: Clear all assignments
- `get_assignments() -> typing.List[Assignment]`: Gets all current assignments.
- `ip: str (read only)`: IP address of the connected robot.
- `numeric_registers: NumericRegisters (read only)`: Number registers R[] as floating point values
- `numeric_registers_int32: NumericRegistersInt32 (read only)`: Number registers R[] as 32-bit integer values
- `numeric_registers_int16: NumericRegistersInt16 (read only)`: Number registers R[] as 16-bit integer values
- `position_registers: PositionRegisters (read only)`: Position registers
- `string_registers: StringRegisters (read only)`: String registers
- `integer_system_variables: IntegerSystemVariables (read only)`: Integer variables
- `real_system_variables: RealSystemVariables (read only)`: Real variables
- `position_system_variables: PositionSystemVariables (read only)`: Position variables
- `string_system_variables: StringSystemVariables (read only)`: String variables
- `digital_signals: typing.List[DigitalSignals] (read only)`: List of all digital signal accessors (SDI, SDO, RDI, RDO, ...)
- `sdi: DigitalSignals (read only)`: Safety Digital Inputs
- `sdo: DigitalSignals (read only)`: Safety Digital Outputs
- `rdi: DigitalSignals (read only)`: Remote Digital Inputs
- `rdo: DigitalSignals (read only)`: Remote Digital Outputs
- `ui: DigitalSignals (read only)`: User Inputs
- `uo: DigitalSignals (read only)`: User Outputs
- `si: DigitalSignals (read only)`: System Inputs
- `so: DigitalSignals (read only)`: System Outputs
- `wi: DigitalSignals (read only)`: Weld Inputs
- `wo: DigitalSignals (read only)`: Weld Outputs
- `wsi: DigitalSignals (read only)`: Weld System Inputs
- `pmc_k: DigitalSignals (read only)`: Programmable Machine Controller Constants
- `pmc_r: DigitalSignals (read only)`: Programmable Machine Controller Relays
- `numeric_i_os: typing.List[NumericIO] (read only)`: List of all Numeric IOs accessors (GI, GO, AI, AO, ...)
- `gi: NumericIO (read only)`: Group Inputs
- `go: NumericIO (read only)`: Group Outputs
- `ai: NumericIO (read only)`: Analog Inputs
- `ao: NumericIO (read only)`: Analog Outputs
- `pmc_d: NumericIO (read only)`: Programmable Machine Controller Data
- `flags: Flags (read only)`: Flags
- `current_position: CurrentPosition (read only)`: Current position in world or user frame
- `current_task_status: CurrentTaskStatus (read only)`: Current program tasks status. Index starts from 1.
- `active_alarm: AlarmAccess (read only)`: Current active alarms
- `alarm_history: AlarmAccess (read only)`: Alarm history
- `comments: Comments (read only)`: Comments of registers, I/O signals and other data
- `simulation_status: SimulationStatus (read only)`: I/O simulation status
- `language: Languages`: Controller language (default is English)
- `connected: bool (read only)`: Indicates if the SNPX underlying TCP client is connected to the robot
