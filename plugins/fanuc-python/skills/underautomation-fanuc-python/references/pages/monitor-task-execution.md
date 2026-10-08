# Monitor task execution

Supervise running programs, check task states, line numbers, and calling programs using SNPX, FTP, or Telnet.

Web page: https://underautomation.com/fanuc/documentation/monitor-task-execution

Monitor running tasks, program names, line numbers, and execution state on your Fanuc robot.

## SNPX

SNPX provides direct task monitoring with program name, line number, state, and caller:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read task 1 status
task = robot.snpx.current_task_status.read(1)
print(f"Program: {task.program_name}")
print(f"Line: {task.line_number}")
print(f"State: {task.state}")       # Running, Paused, Stopped
print(f"Caller: {task.caller}")
```

See also: [SNPX Alarms & task status](snpx-alarms-tasks.md)

## FTP (offline parsing)

Download and parse the task information file:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

program_states = robot.ftp.get_program_states()
for task in program_states.task_states:
    print(f"Task {task.name}: {task.status}")
    for call in task.history:
        print(f"  {call.program_name} - Line {call.line_number}")
```

See also: [FTP Diagnostics & variables](ftp-diagnostics.md)

## Telnet KCL

Query task information using KCL commands:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Get task information for a program like line number, state, and more
result = robot.telnet.get_task_information("MY_PROGRAM")
```

See also: [Telnet Debugging & breakpoints](telnet-debugging.md)

## Protocol comparison

| Feature | SNPX | FTP | Telnet |
|---------|------|-----|--------|
| **Speed** | ~2 ms | ~100 ms | ~30 ms |
| **Program name** | Yes | Yes | Yes |
| **Line number** | Yes | Yes | Yes |
| **Task state** | Yes | Yes | Yes |
| **Caller info** | Yes | No | No |
| **Multiple tasks** | Yes (by index) | Yes (all) | Yes (all) |
