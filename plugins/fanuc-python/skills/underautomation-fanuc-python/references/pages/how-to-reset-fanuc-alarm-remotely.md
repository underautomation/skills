# Reset alarms remotely

Clear and reset alarms on a Fanuc robot using SNPX, Telnet, or CGTP. Read active alarms and alarm history.

Web page: https://underautomation.com/fanuc/documentation/how-to-reset-fanuc-alarm-remotely

Clear fault conditions and reset alarms on your Fanuc robot remotely using different protocols.

## SNPX

SNPX can clear alarms, read the active alarm, and browse alarm history:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Clear all alarms (equivalent to pressing FAULT RESET)
robot.snpx.clear_alarms()

# Read the active alarm
active_alarm = robot.snpx.active_alarm.read(1)
print(f"Alarm: {active_alarm.message} (Severity: {active_alarm.severity})")

# Read alarm history
hist_alarm = robot.snpx.alarm_history.read(10)
```

See also: [SNPX Alarms & task status](snpx-alarms-tasks.md)

## Telnet KCL

Telnet can reset alarms using KCL commands:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Reset the robot (clears faults, exits HOLD)
robot.telnet.reset()

# Or use a custom KCL command
robot.telnet.send_custom_command("RESET")
```

See also: [Telnet Program control](telnet-program-control.md)

## CGTP Web Server

CGTP can check alarm-related variables:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.cgtp.cgtp_comment_type import CgtpCommentType

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read alarm history
errors = robot.cgtp.http.get_all_errors_list()

# extract active alarms from the full list
activeAlarms = errors.filter_active_alarms()

# reset alarms
robot.cgtp.kcl.reset()

# Read user alarms definitions
alarms = robot.cgtp.read_user_alarms()

# write user alarm definition
robot.cgtp.set_user_alarm_severity(1, 8) # Set user alarm #1 to severity 8 
robot.cgtp.set_comment(CgtpCommentType.UserAlarm, 1, "Overheat alarm") # Set comment for user alarm #1
```

See also: [CGTP Alarms, comments & files](cgtp-alarms-files.md)

## FTP (offline)

Download and parse the error log:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""       
parameters.ftp.ftp_password = ""  
robot.connect(parameters)

#  Read alarm history via FTP 
errors = robot.ftp.get_all_errors_list()

# extract active alarms from the full list
active_alarms = errors.filter_active_alarms()
```

## Protocol comparison

| Feature | SNPX | Telnet | CGTP | FTP |
|---------|------|--------|------|-----|
| **Clear alarms** | Yes | Yes | Yes | No |
| **Read active alarm** | Yes | No | Yes | Yes |
| **Alarm history** | Yes | No | Yes | Yes |
| **User alarms** | No | No | Yes | No |
