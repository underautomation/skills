# CGTP overview

CGTP is an HTTP-based protocol providing the richest feature set: program management, variables, registers, I/O, kinematics, batch operations, and file access.

Web page: https://underautomation.com/fanuc/documentation/cgtp

CGTP is the web server running on Fanuc robots (port 80/3080). It provides HTTP-based access to programs, variables, registers, I/O, positions, and files.

## Key features

- **Program management**: Create, delete, rename, run, pause, abort programs
- **Variables & registers**: Read/write any variable, numeric/position/string registers
- **I/O control**: Read, write, simulate, and unsimulate I/O ports
- **Position reading**: Read current Cartesian and joint positions
- **Online kinematics**: Forward and inverse kinematics on the controller
- **Batch operations**: Read/write groups of registers and variables in one request
- **Comments**: Read/write register, I/O, and user alarm descriptions
- **File access**: List and download controller files via HTTP
- **KCL commands**: Execute KCL commands over CGTP, in place of Telnet KCL

## Quick example

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

# Read a variable
var = robot.cgtp.read_variable("$RMT_MASTER")
rmt_master = var.integer_value

# Write a variable
robot.cgtp.write_variable("$RMT_MASTER", 1)

# Read a numeric register with comment
reg = robot.cgtp.read_numeric_register_with_comment(1)

# Read I/O
di1 = robot.cgtp.read_io(CgtpIoPortType.DI, 1)

# Write I/O
robot.cgtp.write_io(CgtpIoPortType.DO, 1, 1)

# Read current Cartesian position
pos = robot.cgtp.read_cartesian_position()

# Run a program
robot.cgtp.run_program("MY_PROGRAM")
```

## Robot options

CGTP does not require any additional options. The robot typically listens on port **80** or **3080**.

Most features require firmware **V8.30** or later. Some features (program management, position reading) require **V9.10+**.

## Firmware compatibility

| Feature | Min. firmware |
|---------|--------------|
| Variable read/write | V8.30 |
| I/O read/write/simulate | V8.30 |
| Program management | V9.10 |
| Position reading | V9.10 |
| Program execution (Run) | V9.30 |
| KCL commands with a result | V8.30 |
| KCL commands without result (Unsafe) | V9.30 |
| File listing | V9.40 |

## Connection

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.cgtp.cgtp_client import CgtpClient

# Via FanucRobot
robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.cgtp.enable = True           # enabled by default
parameters.cgtp.port = 80              # default port
parameters.cgtp.request_timeout_ms = 3000
robot.connect(parameters)

# Or standalone
cgtp = CgtpClient()
cgtp.connect("192.168.0.1")
```

## Authentication

Some robots require authentication. Pass credentials during connection:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.cgtp.cgtp_client import CgtpClient

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")

# Via FanucRobot
parameters.cgtp.login = "admin"
parameters.cgtp.password = "password"
robot.connect(parameters)

# Or standalone
cgtp = CgtpClient()
cgtp.connect("192.168.0.1", login="admin", password="password")
```

## KCL over CGTP

CGTP provides an embedded KCL client accessible via `robot.Cgtp.Kcl`. It executes the KCL commands of `robot.Telnet` without a Telnet connection, and replaces Telnet KCL for new developments:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

robot.cgtp.kcl.set_variable("$RMT_MASTER", 1)

task_info = robot.cgtp.kcl.get_task_information("MY_PROGRAM")

robot.cgtp.kcl.add_breakpoint("MY_PROGRAM", line=10)
```

Some commands (`Run`, `Pause`, `Abort`...) return no result through CGTP. See [KCL commands](cgtp-kcl.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Next steps

- [Program management](cgtp-programs.md) : Create, run, pause, abort programs
- [Registers & variables](cgtp-registers-variables.md) : Read/write registers and variables
- [Inputs & Outputs](cgtp-io.md) : Read, write, simulate I/O
- [Position & kinematics](cgtp-position-kinematics.md) : Read position, FK/IK
- [Alarms, comments & files](cgtp-alarms-files.md) : Comments, user alarms, file listing
- [KCL commands](cgtp-kcl.md) : KCL commands in place of Telnet KCL

## API reference

**CgtpClient** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpclient))

- `CgtpClient()`: Creates a new instance of the CGTP Web Server client.
- `connect(ip: str, port: int=3080, requestTimeoutMs: int=3000, login: str=None, password: str=None) -> None`: Connect to the CGTP Web Server on the controller.
- Inherited from [CgtpClientBase](../api/underautomation.fanuc.cgtp.internal.md#cgtpclientbase-robotcgtp): `disconnect`, `abort_task`, `select_program`, `delete_program`, `get_program_comment`, `set_program_comment`, `get_program_owner`, `set_program_owner`, `get_program_stack_size`, `set_program_stack_size`, `get_program_ignore_pause`, `set_program_ignore_pause`, `get_program_write_protect`, `set_program_write_protect`, `get_program_sub_type`, `set_program_sub_type`, `create_program`, `rename_program`, `list_programs`, `list_tp_programs`, `delete_source_lines`, `insert_source_line`, `replace_source_line`, `set_program_position_to_current_cartesian_position`, `set_program_position`, `run_program`, `change_active_program`, `pause_all_programs`, `read_variable_as_string`, `read_variable`, `write_variable`, `set_comment`, `write_numeric_register_as_double`, `write_numeric_register_as_integer`, `write_string_register`, `set_user_alarm_severity`, `read_numeric_registers_with_comment`, `read_string_registers_with_comment`, `read_user_alarms`, `get_io_comments`, `get_comments`, `read_numeric_register_with_comment`, `read_position_register_with_comment`, `read_batch_variables`, `write_position_register_as_cartesian`, `write_position_register_as_joint`, `write_batch_variables`, `read_io`, `write_io`, `get_io_simulation_status`, `simulate_io`, `unsimulate_io`, `read_cartesian_position`, `read_joint_position`, `invert_kinematics`, `forward_kinematics`, `list_files`, `get_file_as_string`, `kcl`, `http`, `language`, `enabled`

**CgtpClientBase** ([reference](../api/underautomation.fanuc.cgtp.internal.md#cgtpclientbase-robotcgtp))

- `disconnect() -> None`: Disconnect from the CGTP Web Server. After calling this method, the client must be reconnected before it can be used again.
- `abort_task(progName: str=None) -> None`: Abort the task specified by progName. Set to null to abort all user tasks. From firmware 9.10
- `select_program(progName: str, lineNum: int=1) -> None`: Open the TP program progName and move cursor to lineNum. From firmware 9.10
- `delete_program(progName: str) -> None`: Delete the program progName from the controller. From firmware 9.10
- `get_program_comment(progName: str) -> str`: Get the comment of program progName. From firmware 9.10
- `set_program_comment(progName: str, comment: str) -> None`: Set the comment of program progName. From firmware 9.10
- `get_program_owner(progName: str) -> str`: Get the owner of program progName. From firmware 9.10
- `set_program_owner(progName: str, owner: str) -> None`: Set the owner of program progName. From firmware 9.10
- `get_program_stack_size(progName: str) -> int`: Get the stack size of program progName. From firmware 9.10
- `set_program_stack_size(progName: str, stackSize: int) -> None`: Set the stack size of program progName. From firmware 9.10
- `get_program_ignore_pause(progName: str) -> bool`: Get whether program progName ignores pause requests. From firmware 9.10
- `set_program_ignore_pause(progName: str, ignorePause: bool) -> None`: Set whether program progName ignores pause requests. From firmware 9.10
- `get_program_write_protect(progName: str) -> bool`: Get whether program progName is write-protected. From firmware 9.10
- `set_program_write_protect(progName: str, writeProtect: bool) -> None`: Set whether program progName is write-protected. From firmware 9.10
- `get_program_sub_type(progName: str) -> CgtpProgramSubType`: Get the sub-type of program progName. From firmware 9.10
- `set_program_sub_type(progName: str, subType: CgtpProgramSubType) -> None`: Set the sub-type of program progName. From firmware 9.10
- `create_program(progName: str, owner: str=None, comment: str=None, defaultGroup: int=0, subType: CgtpProgramSubType=CgtpProgramSubType.None_) -> None`: Create a new TP program on the controller. From firmware 9.10
- `rename_program(sourceName: str, newName: str) -> None`: Rename program sourceName to newName. From firmware 9.10
- `list_programs(type: CgtpProgramType, subType: CgtpProgramSubType) -> typing.List[str]`: List all TP or Karel programs on the controller
- `list_tp_programs() -> typing.List[str]`: List all TP programs on the controller, regardless of their sub-type.
- `delete_source_lines(progName: str, lineNum: int, count: int=1) -> None`: Delete count lines starting at lineNum in program progName. From firmware 9.10
- `insert_source_line(progName: str, lineContent: str, lineNum: int) -> None`: Insert a source line before lineNum in program progName. From firmware 9.10
- `replace_source_line(progName: str, lineContent: str, lineNum: int) -> None`: Replace the source line at lineNum in program progName. From firmware 9.10
- `set_program_position_to_current_cartesian_position(progName: str, positionIndex: int, groupNumber: int=1) -> CartesianPosition`: Set position at index positionIndex to the current Cartesian position in program progName and return the updated position.
- `set_program_position(progName: str, positionIndex: int, position: Position) -> None`: Set position at index positionIndex in program progName to the given position. Supports both joint and Cartesian representations. Only the first motion group is supported via CGTP. From firmware 9.10
- `run_program(progName: str, lineNum: int=1) -> None`: Run the specified program starting at lineNum. From firmware 9.30
- `change_active_program(progName: str) -> None`: Change the active TP program to progName. From firmware 9.10
- `pause_all_programs() -> None`: Pause program execution on the controller. From firmware 9.10
- `read_variable_as_string(varName: str, progName: str=None) -> str`: Read the value of variable varName in program progName. From firmware 9.10
- `read_variable(varName: str, progName: str=None) -> CgtpVariableValue`: Read the typed value of variable varName in program progName. From firmware 9.10
- `write_variable(varName: str, value: float | int | str, progName: str=None) -> None`: Write a real (double) value to variable varName in program progName. From firmware 8.30 Write an integer value to variable varName in program progName. From firmware 8.30 Write value to variable varName in program progName. From firmware 8.30
- `set_comment(type: CgtpCommentType, index: int, comment: str) -> None`: Set the comment of a register or I/O port identified by type and index.
- `write_numeric_register_as_double(index: int, value: float) -> None`: Write a real (double) value to numeric register R[index].
- `write_numeric_register_as_integer(index: int, value: int) -> None`: Write an integer value to numeric register R[index].
- `write_string_register(index: int, value: str) -> None`: Write a string value to string register SR[index].
- `set_user_alarm_severity(index: int, severity: int) -> None`: Set the severity of a user alarm.
- `read_numeric_registers_with_comment() -> typing.List[NumericRegisterWithComment]`: Read all numeric registers (R[]) with their comments and values.
- `read_string_registers_with_comment() -> typing.List[StringRegisterWithComment]`: Read all string registers (SR[]) with their comments and values.
- `read_user_alarms() -> typing.List[UserAlarmDefinition]`: Read all user alarm definitions with their comments and severity.
- `get_io_comments(type: CgtpCommentIoType) -> IOComments`: Read all I/O comments for the specified I/O type.
- `get_comments(type: CgtpCommentType) -> typing.List[str]`: Read all comments for the specified element type. For I/O types (RI, RO, DI, DO, GI, GO, AI, AO), returns the input or output comments accordingly.
- `read_numeric_register_with_comment(index: int) -> NumericRegisterWithComment`: Read the numeric register (R[]) at index. From firmware 9.10
- `read_position_register_with_comment(index: int, groupNum: int=1) -> PositionRegisterWithComment`: Read the position register (PR[]) at index for motion group groupNum. From firmware 9.10
- `read_batch_variables(variables: CgtpBatchVariables) -> CgtpBatchReadResult`: Read multiple variables from the controller in a single batch operation. Each variable in variables will be updated with the value read from the controller.
- `write_position_register_as_cartesian(index: int, value: CartesianPosition, groupNum: int=1) -> None`: Write a cartesian position value to a position register (PR[])
- `write_position_register_as_joint(index: int, value: JointsPosition, groupNum: int=1) -> None`: Write a joint position value to a position register (PR[])
- `write_batch_variables(variables: CgtpBatchVariables) -> CgtpBatchWriteResult`: Write multiple variables to the controller in a single batch operation.
- `read_io(portType: CgtpIoPortType, index: int) -> int`: Read the value of I/O port at index of type portType. From firmware 8.30
- `write_io(portType: CgtpIoPortType, index: int, value: int) -> None`: Set the value of I/O port at index of type portType. From firmware 8.30
- `get_io_simulation_status(portType: CgtpIoPortType, index: int) -> bool`: Check whether I/O port at index of type portType is simulated. From firmware 8.30
- `simulate_io(portType: CgtpIoPortType, index: int) -> None`: Set I/O port at index of type portType to simulated. From firmware 8.30
- `unsimulate_io(portType: CgtpIoPortType, index: int) -> None`: Remove simulation from I/O port at index of type portType. From firmware 8.30
- `read_cartesian_position(groupNum: int=1) -> CartesianPosition`: Read the current Cartesian position of motion group groupNum. From firmware 9.10
- `read_joint_position(groupNum: int=1) -> JointsPosition`: Read the current joint angles of motion group groupNum. From firmware 9.10
- `invert_kinematics(group: int, cartesianPosition: CartesianPosition, userTool: int=-1, userFrame: int=-1) -> JointsPosition`: Compute the inverse kinematics on the controller: convert a Cartesian position to joint angles.
- `forward_kinematics(group: int, jointPosition: JointsPosition, userTool: int=-1, userFrame: int=-1) -> CartesianPosition`: Compute the forward kinematics on the controller: convert joint angles to a Cartesian position.
- `list_files(pathName: str="MD:") -> typing.List[str]`: List files at the specified path on the controller. From firmware 9.40
- `get_file_as_string(pathName: str) -> str`: Download the content of a file from the controller as a string. From firmware 9.10
- `kcl: CgtpKclClient (read only)`: KCL client for executing KCL commands over CGTP.
- `http: CgtpHttpClient (read only)`: Provides methods to download and decode files from the controller via HTTP.
- `language: Languages`: Controller language (default is English)
- `enabled: bool (read only)`: Indicates whether the client is currently connected to the CGTP Web Server.
