# Diagnostics & variables

Read safety status, current position, I/O state, installed features, error history, registers, and system variables via FTP.

Web page: https://underautomation.com/fanuc/documentation/ftp-diagnostics

Read safety status, current position, I/O state, error history, installed features, registers, and system variables from the Fanuc controller via FTP.

## Safety, position, I/O, and errors

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Safety status
safety_status = robot.ftp.get_safety_status()
print(f"Emergency Stop: {safety_status.external_e_stop}")
print(f"Teach Pendant Enabled: {safety_status.tp_enable}")

# Current position
current_position = robot.ftp.get_current_position()

# I/O state
io_state = robot.ftp.get_io_state()

# Error history
errors = robot.ftp.get_all_errors_list()
```

**SafetyStatus** ([reference](../api/underautomation.fanuc.common.files.diagnosis.md#safetystatus))

- `SafetyStatus()`
- `external_e_stop: bool (read only)`: External emergency stop active
- `sope_stop: bool (read only)`: Emergency stop active by SOP signal
- `tpe_stop: bool (read only)`: Emergency stop active on teach peandant
- `hand_broken: bool (read only)`: Hand broken signal is active
- `over_travel: bool (read only)`: Over travel limit is active
- `low_air_alarm: bool (read only)`: Low air pressure alarm is active
- `fence_open: bool (read only)`: Safety fence is open
- `belt_broken: bool (read only)`: Belt broken signal is active
- `tp_enable: bool (read only)`: Teach pendant is enabled
- `tp_deadman: bool (read only)`: The deadman switch of the teach pendant is active
- `svoff_detect: bool (read only)`: Servo off detection is active
- `non_teacher_enb: bool (read only)`: Non-teacher enable signal is active
- `name: str (read only)`: File name : sftysig.dg

**CurrentPosition** ([reference](../api/underautomation.fanuc.common.files.diagnosis.md#currentposition))

- `CurrentPosition()`
- `groups_position: typing.List[GroupPosition] (read only)`: Position of each robots handled by this controller
- `name: str (read only)`: File name : curpos.dg

**GroupPosition** ([reference](../api/underautomation.fanuc.common.files.diagnosis.md#groupposition))

- `GroupPosition()`
- `id: int (read only)`: Group ID
- `joints_position: JointsPosition (read only)`: Joint positions : the position of each robot angles
- `user_frame_positions: typing.List[CartesianPositionWithUserFrame] (read only)`: Position of each tools in each user frames
- `world_positions: typing.List[CartesianPositionWithTool] (read only)`: Position of each tools in world coordinates

**IOState** ([reference](../api/underautomation.fanuc.common.files.diagnosis.md#iostate))

- `IOState()`
- `states: typing.List[IOStatus] (read only)`: Status of all controller inputs and outputs
- `name: str (read only)`: File name : iostate.dg

**IOStatus** ([reference](../api/underautomation.fanuc.common.md#iostatus))

- `IOStatus()`
- `port: DigitalPorts (read only)`: Digital port type
- `id: int (read only)`: Digital port ID
- `value: bool (read only)`: Digital port value
- `name: str (read only)`: IO Name

**DigitalPorts** ([reference](../api/underautomation.fanuc.common.md#digitalports))

- DIN: Digital input
- DOUT: Digital outputs
- UI: User inputs
- UO: User outputs
- SI: SI
- SO: SO
- RI: Robot inputs
- RO: Robot outputs
- FLG: Flags

## Read variables

Variables are read in bulk from `.va` files stored on the controller.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Get all variables from all files
all_variables = robot.ftp.get_all_variables()
for file in all_variables:
    for variable in file.variables:
        print(f"{variable.name} = {variable.value}")

# Get variables from a specific file
variables = robot.ftp.get_variables_from_file("SYSVARS.va")

# Access commonly used system variables directly
rmt_master = robot.ftp.known_variable_files.get_system_file().rmt_master
```

## Read registers

Registers are read in bulk via FTP variable files.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Read numeric registers
numreg_file = robot.ftp.known_variable_files.get_numreg_file()
for i in range(len(numreg_file.numreg)):
    value = numreg_file.numreg[i]
    print(f"R[{i}] = {value}")

# Read position registers
posreg_file = robot.ftp.known_variable_files.get_posreg_file()

# Read string registers
strreg_file = robot.ftp.known_variable_files.get_strreg_file()
for i in range(len(strreg_file.strreg)):
    value = strreg_file.strreg[i]
    print(f"SR[{i}] = '{value}'")
```

## Installed features (options)

Detect available options on the controller to check protocol availability.

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

# Check specific capabilities
has_snpx = features.has_snpx
has_telnet = features.has_telnet
has_stream_motion = features.has_stream_motion  # J519 option

# List all installed features
for feature in features.features_list:
    print(f"{feature.name} ({feature.order_no})")
```

## Asynchronous reading

Each reading method has an asynchronous version with an optional `CancellationToken`: `GetSafetyStatusAsync`, `GetCurrentPositionAsync`, `GetIOStateAsync`, `GetAllErrorsListAsync`, `GetProgramStatesAsync`, `GetVariablesFromFileAsync`, `GetAllVariablesAsync`, and `KnownVariableFiles.Get...Async`. The same methods are available on the web server client, `robot.Cgtp.Http`. They are not available on .NET Framework 3.5 and 4.0.



## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Read safety status
safety_status = robot.ftp.get_safety_status()
print(f"Emergency Stop: {safety_status.external_e_stop}")
print(f"Teach Pendant Enabled: {safety_status.tp_enable}")

# Read current position (joints, world, user frames)
current_position = robot.ftp.get_current_position()

# Read I/O state
io_state = robot.ftp.get_io_state()

# Read all errors
errors = robot.ftp.get_all_errors_list()

# Read all variables from all files
all_variables = robot.ftp.get_all_variables()
for file in all_variables:
    for variable in file.variables:
        print(f"{variable.name} = {variable.value}")

# Access well-known system variables
rmt_master = robot.ftp.known_variable_files.get_system_file().rmt_master

# Get installed features
features = robot.ftp.get_summary_diagnostic().features
has_snpx = features.has_snpx
```

## API reference

**SummaryDiagnosis** ([reference](../api/underautomation.fanuc.common.files.diagnosis.md#summarydiagnosis))

- `SummaryDiagnosis()`
- `name: str (read only)`: File name : summary.dg
- `current_position: CurrentPosition (read only)`: Current position of each robots and groups handled by this controller
- `safety: SafetyStatus (read only)`: Controller safety information
- `i_os: IOState (read only)`: Controller IO status
- `features: Features (read only)`: Controller features status
- `program_states: ProgramStates (read only)`: Controller program states

**Features** ([reference](../api/underautomation.fanuc.common.files.diagnosis.md#features))

- `Features()`
- `features_list: typing.List[Feature] (read only)`: List of features
- `has_telnet: bool (read only)`: Indicates if the robot has the TELNET feature enabled (TELN).
- `has_snpx: bool (read only)`: Indicates if the robot has the SNPX feature enabled (R553 or R651).
- `has_ascii_upload: bool (read only)`: Indicates if the robot has the ASCII upload feature enabled : R507 ("ASCII Upload" on older controllers) or R796 ("ASCII Program Loader" on most recent controllers).
- `has_stream_motion: bool (read only)`: Indicates if the robot has the Stream Motion feature enabled (J519).
