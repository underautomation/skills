# Access Karel program variables

Read and write Karel program variables using SNPX ($[Program]Variable syntax), CGTP, or FTP variable files.

Web page: https://underautomation.com/fanuc/documentation/access-karel-program-variables

Read and write variables inside Karel programs running on your Fanuc robot.

## SNPX

SNPX accesses Karel variables using the `$[ProgramName]VariableName` naming convention:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read a Karel integer variable
my_var = robot.snpx.integer_system_variables.read("$[MyKarelProg]my_variable")

# Write a Karel integer variable
robot.snpx.integer_system_variables.write("$[MyKarelProg]my_variable", 42)

# Read a Karel real variable
real_var = robot.snpx.real_system_variables.read("$[MyKarelProg]speed_ratio")

# Read a Karel position variable
pos_var = robot.snpx.position_system_variables.read("$[MyKarelProg]target_pos")

# Read a Karel string variable
str_var = robot.snpx.string_system_variables.read("$[MyKarelProg]status_msg")
```

See also: [SNPX System variables](snpx-variables.md)

## CGTP Web Server

CGTP reads and writes Karel program variables using the `progName` parameter:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read a Karel variable
var = robot.cgtp.read_variable("my_variable", prog_name="MyKarelProg")
int_val = var.integer_value

# Write a Karel variable
robot.cgtp.write_variable("my_variable", 42, prog_name="MyKarelProg")

# Read as string
raw = robot.cgtp.read_variable_as_string("speed_ratio", prog_name="MyKarelProg")
```

See also: [CGTP Registers & variables](cgtp-registers-variables.md)

## Telnet

Telnet allows you to read and write a karel program variable 

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

result = robot.telnet.get_variable("VAR_NAME", "KarelProgramName")
```


## Protocol comparison

| Feature | SNPX | CGTP | Telnet |
|---------|------|------|-----|
| **Speed** | ~2 ms | ~50 ms | ~100 ms |
| **Typed read** | Yes (4 types) | Yes (auto-detect) | Yes (file parse) |
| **Write** | Yes | Yes | No |
| **Batch read** | Yes | Yes | Yes (all at once) |
| **All variable types** | Integer, Real, Position, String | All | All |
