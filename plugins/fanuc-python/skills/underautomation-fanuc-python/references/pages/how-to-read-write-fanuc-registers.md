# Read & write registers

Compare all methods to read and write numeric, position, and string registers on a Fanuc robot: SNPX, FTP, CGTP, and Telnet.

Web page: https://underautomation.com/fanuc/documentation/how-to-read-write-fanuc-registers

Registers are the primary data exchange mechanism on Fanuc robots. This guide shows how to read and write numeric (R[]), position (PR[]), string (SR[]), and flag (F[]) registers using different protocols.

## SNPX (fastest : ~2 ms)

SNPX provides the fastest register access with typed read/write operations.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.cartesian_position import CartesianPosition
from underautomation.fanuc.common.joints_position import JointsPosition

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True

# Connect to the robot
robot.connect(parameters)

# --- Numeric Registers (R[]) ---

# Read R[1]
num_reg1 = robot.snpx.numeric_registers.read(1)
print(f"R[1] = {num_reg1}")

# Write R[1]
robot.snpx.numeric_registers.write(1, 123.45)

# --- Position Registers (PR[]) ---

# Read PR[1]
pos_reg1 = robot.snpx.position_registers.read(1)
print(f"PR[1] UserFrame={pos_reg1.user_frame}, UserTool={pos_reg1.user_tool}")

# Access Cartesian values
if pos_reg1.cartesian_position is not None:
    print(f"  X={pos_reg1.cartesian_position.x}")
    print(f"  Y={pos_reg1.cartesian_position.y}")
    print(f"  Z={pos_reg1.cartesian_position.z}")

# Access joint values
if pos_reg1.joints_position is not None:
    print(f"  J1={pos_reg1.joints_position.j1}")

# Write Cartesian position to PR[1]
robot.snpx.position_registers.write(1, CartesianPosition(100, 200, 300, 0, 90, 0))

# Write Joint position to PR[1]
joints = JointsPosition()
joints.j1 = 0
joints.j2 = 0
joints.j3 = 0
joints.j4 = 0
joints.j5 = 0
joints.j6 = 45
robot.snpx.position_registers.write(1, joints)

# --- String Registers (SR[]) ---

# Read SR[1]
str_reg1 = robot.snpx.string_registers.read(1)
print(f"SR[1] = '{str_reg1}'")

# Write SR[1]
robot.snpx.string_registers.write(1, "Hello, Robot!")

# --- Flag Registers (F[]) ---

# Read F[1]
flag1 = robot.snpx.flags.read(1)
print(f"F[1] = {flag1}")

# Write F[1]
robot.snpx.flags.write(1, True)
```

See also: [SNPX Registers](snpx-registers.md)

## CGTP Web Server

CGTP reads registers with their comments in a single request.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read R[1] with comment
reg = robot.cgtp.read_numeric_register_with_comment(1)
print(f"R[1] = {reg.real_value} ({reg.comment})")

# Write R[5]
robot.cgtp.write_numeric_register_as_double(5, 123.45)

# Read PR[1] with comment
pos_reg = robot.cgtp.read_position_register_with_comment(1)

# Write PR[1] as Cartesian
robot.cgtp.write_position_register_as_cartesian(1, [100, 200, 300, 0, 90, 0])

# Write SR[1]
robot.cgtp.write_string_register(1, "Hello")
```

See also: [CGTP Registers & variables](cgtp-registers-variables.md)

## FTP (offline parsing)

FTP lets you download register files and parse them locally:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Get all numeric registers with comments
num_regs = robot.ftp.known_variable_files.get_numreg_file()

# Get all position registers with comments
pos_regs = robot.ftp.known_variable_files.get_posreg_file()

# Get all string registers with comments
str_regs = robot.ftp.known_variable_files.get_strreg_file()
```

See also: [FTP Diagnostics & variables](ftp-diagnostics.md)

## Protocol comparison

| Feature | SNPX | CGTP | FTP |     
|---------|------|------|-----|
| **Speed** | ~2 ms | ~10 ms | ~100 ms | 
| **Read with comment** | Via Comments API | Yes (single request) | Yes (file parse) | 
| **Batch read** | Yes (same speed) | Yes (batch API) | Yes (all at once) | 
| **Write** | Yes | Yes | No |
| **Position registers** | Yes | Yes | Yes (read only) | 
| **String registers** | Yes | Yes | Yes (read only) |
| **Flags** | Yes | Via I/O API | Yes (read only) |
