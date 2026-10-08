# Read & write I/O comments

Read and write comments (descriptions) for registers and I/O ports using SNPX or CGTP.

Web page: https://underautomation.com/fanuc/documentation/read-write-io-comments

Read and write descriptive comments (labels) for registers and I/O ports on your Fanuc robot.

## SNPX

SNPX reads and writes comments for all register and I/O types:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read a comment (default 16 characters)
comment = robot.snpx.comments.read("Register", 5)

# Read with custom length (must be even, >= 2)
long_comment = robot.snpx.comments.read("Register", 5, 24)

# Write a comment
robot.snpx.comments.write("PositionRegister", 1, "Home Position", 16)
robot.snpx.comments.write("DI", 1, "Start Button", 16)
```

Available comment types: `Register`, `PositionRegister`, `StringRegister`, `DI`, `DO`, `RI`, `RO`, `UI`, `UO`, `SI`, `SO`, `WI`, `WO`, `WSI`, `WSO`, `GI`, `GO`, `AI`, `AO`, `Flag`.

See also: [SNPX Alarms & task status](snpx-alarms-tasks.md)

## CGTP Web Server

CGTP provides bulk comment reading and individual writing:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read all register comments
reg_comments = robot.cgtp.get_comments("NumericRegister")
pos_comments = robot.cgtp.get_comments("PositionRegister")

# Write a comment
robot.cgtp.set_comment("NumericRegister", 1, "Speed setpoint")

# Read I/O comments by category
digital_io = robot.cgtp.get_io_comments("DigitalIO")
robot_io = robot.cgtp.get_io_comments("RobotIO")
group_io = robot.cgtp.get_io_comments("GroupIO")
analog_io = robot.cgtp.get_io_comments("AnalogIO")
```

See also: [CGTP Alarms, comments & files](cgtp-alarms-files.md)

## Protocol comparison

| Feature | SNPX | CGTP |
|---------|------|------|
| **Read individual** | Yes | No (bulk only) |
| **Read all** | No | Yes |
| **Write** | Yes | Yes |
| **Register comments** | Yes | Yes |
| **I/O comments** | Yes | Yes (by category) |
| **Custom length** | Yes (even, ≥ 2) | No (fixed) |
