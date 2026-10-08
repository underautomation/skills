# Get current position

Retrieve the current robot position (joint and Cartesian) using SNPX, FTP, CGTP, or Telnet. Compare approaches and choose the best for your use case.

Web page: https://underautomation.com/fanuc/documentation/get-current-position

Read the current tool position of your Fanuc robot in Cartesian (X, Y, Z, W, P, R) or joint (J1–J6) format using different protocols.

## SNPX (fastest : ~2 ms)

SNPX provides the fastest position reading, in world or user frame coordinates.

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

# Read current world position
world_position = robot.snpx.current_position.read_world_position()

# Access the Cartesian position
x = world_position.cartesian_position.x

# Access the user tool at this position
user_tool = world_position.user_tool

# Access the joint positions
j1 = world_position.joints_position.j1

# Read current world position of group 2
world_position_g2 = robot.snpx.current_position.read_world_position(2)
```

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

# Read user frame 1 position
user_frame = robot.snpx.current_position.read_user_frame_position(1)

# Access the Cartesian position
x = user_frame.cartesian_position.x

# Access the user tool at this position
user_tool = user_frame.user_tool

# Access the user frame id
frame_id = user_frame.user_frame

# Access the joint positions
j1 = user_frame.joints_position.j1

# Read user frame position of group 2
user_frame_g2 = robot.snpx.current_position.read_user_frame_position(1, 2)
```

See also: [SNPX Current position](snpx-position.md)

## CGTP Web Server

CGTP returns Cartesian and joint positions separately:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read Cartesian position
cartesian = robot.cgtp.read_cartesian_position()
print(f"X={cartesian.x}, Y={cartesian.y}, Z={cartesian.z}")

# Read joint position
joints = robot.cgtp.read_joint_position()
print(f"J1={joints.j1}, J2={joints.j2}, J3={joints.j3}")

# Multi-group
group2 = robot.cgtp.read_cartesian_position(group_num=2)
```

See also: [CGTP Position & kinematics](cgtp-position-kinematics.md)

## FTP (offline parsing)

Download and parse the current position diagnostic file:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

cur_pos = robot.ftp.get_summary_diagnostic().current_position
```

See also: [FTP Diagnostics & variables](ftp-diagnostics.md)

## Telnet KCL

Read position-related system variables:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

curpos = robot.telnet.get_variable("$CURPOS")
curjpos = robot.telnet.get_variable("$CURJPOS")
```

## Protocol comparison

| Feature | SNPX | CGTP | FTP | Telnet |
|---------|------|------|-----|--------|
| **Speed** | ~2 ms | ~50 ms | ~100 ms | ~30 ms |
| **World frame** | Yes | Yes | Yes | Yes |
| **User frame** | Yes | No | No | No |
| **Joint position** | Yes | Yes | Yes | Yes |
| **Multi-group** | Yes | Yes | No | No |
