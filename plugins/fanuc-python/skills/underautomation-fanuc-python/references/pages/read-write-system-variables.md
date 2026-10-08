# Read & write system variables

Access and modify Fanuc system variables ($RMT_MASTER, $MCR.$GENOVERRIDE, etc.) using Telnet, SNPX, CGTP, or FTP.

Web page: https://underautomation.com/fanuc/documentation/read-write-system-variables

Read and write system variables ($RMT_MASTER, $MCR.$GENOVERRIDE, etc.) on your Fanuc robot using different protocols.

## SNPX (fastest : ~2 ms)

SNPX supports 4 typed variable categories: integer, real, position, and string.

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

# --- Integer system variables ---
rmt_master = robot.snpx.integer_system_variables.read("$RMT_MASTER")
robot.snpx.integer_system_variables.write("$RMT_MASTER", 1)

# --- Real (float) system variables ---
gen_override = robot.snpx.real_system_variables.read("$MCR.$GENOVERRIDE")
robot.snpx.real_system_variables.write("$MCR.$GENOVERRIDE", 50.0)

# --- Position system variables ---
cell_floor = robot.snpx.position_system_variables.read("$CELL_FLOOR")
robot.snpx.position_system_variables.write("$CELL_FLOOR", cell_floor)

# --- String system variables ---
last_alm = robot.snpx.string_system_variables.read("$ALM_IF.$LAST_ALM")
robot.snpx.string_system_variables.write("$ALM_IF.$LAST_ALM", "No alarms")

# --- Karel program variables ---
karel_var = robot.snpx.integer_system_variables.read("$[MyKarelProg]my_variable")
robot.snpx.integer_system_variables.write("$[MyKarelProg]my_variable", 42)

# --- Set variable (auto-detects type) ---
robot.snpx.set_variable("$RMT_MASTER", 1)
```

See also: [SNPX System variables](snpx-variables.md)

## Telnet KCL

Telnet reads and writes any variable using KCL commands:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read a variable
value = robot.telnet.get_variable("$RMT_MASTER")

# Write a variable
robot.telnet.set_variable("$RMT_MASTER", "1")
robot.telnet.set_variable("$MCR.$GENOVERRIDE", "50")
```

See also: [Telnet Variables & I/O](telnet-variables-io.md)

## CGTP Web Server

CGTP provides typed variable reading and string-based writing:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.cgtp.enable = True
robot.connect(parameters)

# Read with automatic type detection
var = robot.cgtp.read_variable("$RMT_MASTER")
int_val = var.integer_value

# Write
robot.cgtp.write_variable("$RMT_MASTER", 1)
robot.cgtp.write_variable("$MCR.$GENOVERRIDE", 50.0)

# Read and decode system.va
system = robot.cgtp.http.known_variable_files.get_system_file()
rmt_master = system.rmt_master

# get all variables with their value and types
filelist = robot.cgtp.http.get_all_variables()
```

See also: [CGTP Registers & variables](cgtp-registers-variables.md)

## FTP (offline parsing)

Download variable files and parse them offline:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)

# Read and decode system.va
system = robot.ftp.known_variable_files.get_system_file()
rmt_master = system.rmt_master

# get all variables with their value and types
filelist = robot.ftp.get_all_variables()
```

See also: [Offline file parsing](offline-file-parsing.md)

## Protocol comparison

| Feature | SNPX | Telnet | CGTP | FTP |
|---------|------|--------|------|-----|
| **Speed** | ~2 ms | ~30 ms | ~50 ms | ~100 ms |
| **Typed read** | Yes (4 types) | No (string) | Yes (auto-detect) | Yes (file parse) |
| **Write** | Yes | Yes | Yes | No |
| **Batch read** | Yes | No | Yes | Yes (all at once) |
| **Karel variables** | Yes | Yes | Yes | No |
| **Batch read all variables** | No | No | Yes | Yes |
