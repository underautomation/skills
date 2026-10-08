# Alarms, comments & files

Manage user alarms, read/write register and I/O comments, list and download files from the controller via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-alarms-files

CGTP provides access to register and I/O comments, user alarms, and file listing/download from the controller.

## Register & I/O comments

Read and write descriptive comments for registers:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read register comments
reg_comments = robot.cgtp.get_comments("NumericRegister")
pos_comments = robot.cgtp.get_comments("PositionRegister")
str_comments = robot.cgtp.get_comments("StringRegister")

# Write a register comment
robot.cgtp.set_comment("NumericRegister", 1, "Speed setpoint")
robot.cgtp.set_comment("PositionRegister", 1, "Home position")

# Read I/O comments
robot_io = robot.cgtp.get_io_comments("RobotIO")
digital_io = robot.cgtp.get_io_comments("DigitalIO")
analog_io = robot.cgtp.get_io_comments("AnalogIO")
```

## User alarms

Read and configure user alarm definitions:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read all user alarms
alarms = robot.cgtp.read_user_alarms()
for alarm in alarms:
    print(f"Alarm: {alarm.comment} (Severity: {alarm.severity})")

# Set user alarm severity
robot.cgtp.set_user_alarm_severity(1, 2)
```

## File listing

List files on the controller using CGTP HTTP:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# List files in a directory
files = robot.cgtp.list_files("MD:")

# List TP programs
tp_programs = robot.cgtp.http.list_tp_programs()
for prog in tp_programs:
    print(f"{prog.file} - {prog.comment}")

# List variable files
var_files = robot.cgtp.http.list_variable_files()

# Download as string
content = robot.cgtp.http.download_as_string("numreg.va")

# Download as bytes
data = robot.cgtp.http.download_as_bytes("posreg.va")
```


## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.cgtp.cgtp_comment_type import CgtpCommentType
from underautomation.fanuc.cgtp.cgtp_comment_io_type import CgtpCommentIoType

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.cgtp.enable = True

# Connect to the robot
robot.connect(parameters)

# --- Register comments ---
reg_comments = robot.cgtp.get_comments(CgtpCommentType.NumericRegister)
pos_comments = robot.cgtp.get_comments(CgtpCommentType.PositionRegister)

# Write a comment
robot.cgtp.set_comment(CgtpCommentType.NumericRegister, 1, "Speed setpoint")

# --- I/O comments ---
digital_io = robot.cgtp.get_io_comments(CgtpCommentIoType.DigitalIO)
robot_io = robot.cgtp.get_io_comments(CgtpCommentIoType.RobotIO)

# --- User alarms ---
alarms = robot.cgtp.read_user_alarms()
robot.cgtp.set_user_alarm_severity(1, 2)

# --- File listing ---
files = robot.cgtp.list_files("MD:")

tp_programs = robot.cgtp.http.list_tp_programs()
var_files = robot.cgtp.http.list_variable_files()
diag_files = robot.cgtp.http.list_diagnostic_files()

# --- File download ---
content = robot.cgtp.http.download_as_string("numreg.va")
data = robot.cgtp.http.download_as_bytes("posreg.va")
```

## API reference

**CgtpCommentType** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpcommenttype))

- NumericRegister: Numeric register (R[]).
- PositionRegister: Position register (PR[]).
- UserAlarm: User alarm.
- RI: Robot input.
- RO: Robot output.
- DI: Digital input.
- DO: Digital output.
- GI: Group input.
- GO: Group output.
- AI: Analog input.
- AO: Analog output.
- StringRegister: String register (SR[]).
- Flag: Flag (F[]).

**CgtpCommentIoType** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpcommentiotype))

- RobotIO: Robot I/O (RI/RO).
- DigitalIO: Digital I/O (DI/DO).
- GroupIO: Group I/O (GI/GO).
- AnalogIO: Analog I/O (AI/AO).

**CgtpFileItem** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpfileitem))

- `CgtpFileItem()`
- `file: str (read only)`: File name on the controller.
- `comment: str (read only)`: Comment associated with the file, if any.

**CgtpAsciiFileItem** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpasciifileitem))

- `CgtpAsciiFileItem()`
- `ascii_file: str (read only)`: ASCII format file name, or null if not available.
- Inherited from [CgtpFileItem](../api/underautomation.fanuc.cgtp.md#cgtpfileitem): `file`, `comment`

**CgtpHttpClient** ([reference](../api/underautomation.fanuc.cgtp.internal.md#cgtphttpclient-robotcgtphttp))

- `download_as_bytes(fileName: str) -> typing.List[int]`: Download a file from the controller and return its raw bytes.
- `download_as_string(fileName: str) -> str`: Download a file from the controller and return its content as a string.
- `list_variable_files() -> typing.List[CgtpAsciiFileItem]`: List variable files available on the controller.
- `list_tp_programs() -> typing.List[CgtpAsciiFileItem]`: List TP program files available on the controller.
- `list_diagnostic_files() -> typing.List[CgtpFileItem]`: List diagnostic and error files available on the controller.
- `list_other_files() -> typing.List[CgtpFileItem]`: List other files available on the controller.
- `enumerate_variable_file_names() -> typing.List[str]`
- `ip: str (read only)`
- `base_path: str`: Base path used to build the download URL. Default is "MD".
- Inherited from [FileClientBase](../api/underautomation.fanuc.common.files.md#fileclientbase-robotftp): `get_summary_diagnostic`, `get_all_errors_list`, `get_current_position`, `get_io_state`, `get_safety_status`, `get_program_states`, `get_variables_from_file`, `get_all_variables`, `known_variable_files`

**UserAlarmDefinition** ([reference](../api/underautomation.fanuc.common.md#useralarmdefinition))

- `UserAlarmDefinition()`
- `comment: str`: Comment associated with this alarm.
- `severity: int`: Severity level of the alarm.
