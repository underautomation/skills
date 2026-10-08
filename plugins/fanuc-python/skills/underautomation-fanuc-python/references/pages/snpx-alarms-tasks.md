# Alarms & task status

Read active alarms, alarm history, clear alarms, monitor running tasks, and read/write comments via SNPX.

Web page: https://underautomation.com/fanuc/documentation/snpx-alarms-tasks

SNPX lets you read active alarms, browse alarm history, clear alarms, monitor running tasks, and read/write register and I/O comments.

## Alarms

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Active alarm
active_alarm = robot.snpx.active_alarm.read(1)
print(f"Alarm: {active_alarm.message}")
print(f"Severity: {active_alarm.severity}")
print(f"Time: {active_alarm.time}")

# Alarm history
hist_alarm = robot.snpx.alarm_history.read(10)

# Clear alarms
robot.snpx.clear_alarms()
```

## Task status and comments

Monitor running program tasks by index (1-based). Comments are short descriptions associated with registers or I/O ports.

Available comment types: `Register`, `PositionRegister`, `StringRegister`, `DI`, `DO`, `RI`, `RO`, `UI`, `UO`, `SI`, `SO`, `WI`, `WO`, `WSI`, `WSO`, `GI`, `GO`, `AI`, `AO`, `Flag`.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.snpx.internal.comment_type import CommentType

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Task status
task = robot.snpx.current_task_status.read(1)
print(f"Program: {task.program_name}")
print(f"Line: {task.line_number}")
print(f"State: {task.state}")       # Stopped, Paused, Running
print(f"Caller: {task.caller}")

# Read and write comments
comment = robot.snpx.comments.read(CommentType.Register, 5)
long_comment = robot.snpx.comments.read(CommentType.Register, 5, 24)
robot.snpx.comments.write(CommentType.PositionRegister, 1, "Home Position", 16)
```

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.snpx.internal.comment_type import CommentType

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True

# Connect to the robot
robot.connect(parameters)

# --- Active alarm ---
active_alarm = robot.snpx.active_alarm.read(1)
print(f"Alarm: {active_alarm.message}")
print(f"Severity: {active_alarm.severity}")
print(f"Time: {active_alarm.time}")

# --- Alarm history ---
hist_alarm = robot.snpx.alarm_history.read(10)
print(f"History #10: {hist_alarm.message}")

# --- Clear alarms ---
robot.snpx.clear_alarms()

# --- Task status ---
task = robot.snpx.current_task_status.read(1)
print(f"Program: {task.program_name}")
print(f"Line: {task.line_number}")
print(f"State: {task.state}")
print(f"Caller: {task.caller}")

# --- Read and write comments ---
comment = robot.snpx.comments.read(CommentType.Register, 5)
robot.snpx.comments.write(CommentType.PositionRegister, 1, "Home Position", 16)
```

## API reference

**RobotAlarm** ([reference](../api/underautomation.fanuc.snpx.internal.md#robotalarm))

- `RobotAlarm()`
- `static from_bytes(bytes: typing.List[int], language: Languages, start: int=0) -> 'RobotAlarm'`: Creates a RobotAlarm from a byte array.
- `id: AlarmId`: Alarm Category
- `number: int`: Alarm Number
- `cause_id: AlarmId`: Cause Category
- `cause_number: int`: Cause Number
- `severity: AlarmSeverity`: Alarm Severity
- `time: datetime`: Occurrence Time
- `message: str`: Error Message
- `cause_message: str`: Cause message
- `severity_message: str`: Severity message

**AlarmSeverity** ([reference](../api/underautomation.fanuc.snpx.internal.md#alarmseverity))

- NONE_: No severity.
- WARN: Warning level alarm.
- PAUSE_L: Local pause level alarm.
- PAUSE_G: Global pause level alarm.
- STOP_L: Local stop level alarm.
- STOP_G: Global stop level alarm.
- SERVO: Servo error alarm.
- ABORT_L: Local abort level alarm.
- ABORT_G: Global abort level alarm.
- SERVO2: Servo error level 2 alarm.
- SYSTEM: System level alarm.

**RobotTaskStatus** ([reference](../api/underautomation.fanuc.snpx.internal.md#robottaskstatus))

- `RobotTaskStatus()`
- `static from_bytes(bytes: typing.List[int], language: Languages, start: int=0) -> 'RobotTaskStatus'`: Creates a RobotTaskStatus from a byte array.
- `program_name: str`: Gets or sets the name of the program being executed.
- `line_number: int`: Gets or sets the current line number in the program.
- `state: RobotTaskState`: Gets or sets the current execution state of the task.
- `caller: str`: Gets or sets the name of the calling program.

**RobotTaskState** ([reference](../api/underautomation.fanuc.snpx.internal.md#robottaskstate))

- Stopped: Task is stopped.
- Paused: Task is paused.
- Running: Task is running.

**CommentType** ([reference](../api/underautomation.fanuc.snpx.internal.md#commenttype))

- Register: Numeric register R[].
- PositionRegister: Position register PR[].
- StringRegister: String register SR[].
- DI: Digital Input.
- DO: Digital Output.
- RI: Remote Input.
- RO: Remote Output.
- UI: User Input.
- UO: User Output.
- SI: System Input.
- SO: System Output.
- WI: Weld Input.
- WO: Weld Output.
- WSI: Wire Stick Input.
- WSO: Wire Stick Output.
- GI: Group Input.
- GO: Group Output.
- AI: Analog Input.
- AO: Analog Output.
- Flag: Flag
