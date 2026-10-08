# Program management

Create, delete, rename, run, pause, abort programs and manage their attributes (comment, owner, subtype) via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-programs

CGTP provides rich program management features: create, delete, rename, run, pause, configure program properties, list programs, and edit source code.

## List programs

Retrieve all TP or Karel programs on the controller, filtered by type and sub-type. You can also list all TP programs at once, regardless of their sub-type.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.cgtp.cgtp_program_type import CgtpProgramType
from underautomation.fanuc.cgtp.cgtp_program_sub_type import CgtpProgramSubType

robot = FanucRobot()
robot.connect("192.168.0.1")

# List all TP programs on the controller (all sub-types)
all_tp_programs = robot.cgtp.list_tp_programs()
for prog in all_tp_programs:
    print(prog)

# List TP programs of a specific sub-type
jobs = robot.cgtp.list_programs(CgtpProgramType.Tp, CgtpProgramSubType.Job)
macros = robot.cgtp.list_programs(CgtpProgramType.Tp, CgtpProgramSubType.Macro)

# List Karel programs
karel_programs = robot.cgtp.list_programs(CgtpProgramType.Karel, CgtpProgramSubType.None_)
```

## Source code editing

Insert, replace, or delete lines in a TP program directly on the controller. Requires firmware **V9.10+**.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Insert a new line before line 3 in program MY_PROGRAM
robot.cgtp.insert_source_line("MY_PROGRAM", "L P[5] 100mm/sec FINE", 3)

# Replace the content of line 5
robot.cgtp.replace_source_line("MY_PROGRAM", "J P[1] 50% FINE", 5)

# Delete 2 lines starting at line 4
robot.cgtp.delete_source_lines("MY_PROGRAM", 4, 2)

# Delete a single line
robot.cgtp.delete_source_lines("MY_PROGRAM", 1)
```

## Run a program

Run a specific program starting from a given line (default: line 1). Requires firmware **V9.30+**.

Prefer `RunProgram` to `robot.Cgtp.Kcl.Run`: it can start at a given line, and it throws a `CgtpException` when the controller refuses the command. `Kcl.Run` returns no result. See [KCL commands](cgtp-kcl.md).

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Run program from line 1
robot.cgtp.run_program("MY_PROGRAM")

# Run from a specific line
robot.cgtp.run_program("MY_PROGRAM", line_num=10)

# Select a program
robot.cgtp.select_program("MY_PROGRAM")

# Change the currently active program
robot.cgtp.change_active_program("MY_PROGRAM")

# Abort a specific task
robot.cgtp.abort_task("MY_PROGRAM")

# Pause all running programs
robot.cgtp.pause_all_programs()
```


## Create a program

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.cgtp.cgtp_program_sub_type import CgtpProgramSubType

robot = FanucRobot()
robot.connect("192.168.0.1")

# Create a program
robot.cgtp.create_program(
    prog_name="NEW_PROG",
    owner="UnderAutomation",
    comment="Created via CGTP",
    default_group=1,
    sub_type=CgtpProgramSubType.Job)

# Delete
robot.cgtp.delete_program("OLD_PROG")

# Rename
robot.cgtp.rename_program("OLD_NAME", "NEW_NAME")

# Program properties
comment = robot.cgtp.get_program_comment("MY_PROGRAM")
robot.cgtp.set_program_comment("MY_PROGRAM", "Updated comment")
owner = robot.cgtp.get_program_owner("MY_PROGRAM")
robot.cgtp.set_program_owner("MY_PROGRAM", "Admin")
stack = robot.cgtp.get_program_stack_size("MY_PROGRAM")
robot.cgtp.set_program_stack_size("MY_PROGRAM", 200)
robot.cgtp.set_program_ignore_pause("MY_PROGRAM", True)
robot.cgtp.set_program_write_protect("MY_PROGRAM", True)
robot.cgtp.set_program_sub_type("MY_PROGRAM", CgtpProgramSubType.Macro)
```

Available sub-types: `None`, `Job`, `Process`, `Macro`, `Condition`.

## Pause, abort, resume, get and set attributes

CGTP allows you to completely manage programs on the robot, including creation, deletion, renaming, and execution control. Here's a complete example demonstrating these features:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.cgtp.cgtp_program_sub_type import CgtpProgramSubType

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.cgtp.enable = True

# Connect to the robot
robot.connect(parameters)

# Run a program
robot.cgtp.run_program("MY_PROGRAM")

# Run from a specific line
robot.cgtp.run_program("MY_PROGRAM", line_num=10)

# Select a program
robot.cgtp.select_program("MY_PROGRAM")

# Abort a task
robot.cgtp.abort_task("MY_PROGRAM")

# Pause all programs
robot.cgtp.pause_all_programs()

# Create a program
robot.cgtp.create_program(
    prog_name="NEW_PROG",
    owner="UnderAutomation",
    comment="Created via CGTP",
    sub_type=CgtpProgramSubType.Job
)

# Delete a program
robot.cgtp.delete_program("OLD_PROG")

# Rename a program
robot.cgtp.rename_program("OLD_NAME", "NEW_NAME")

# List all TP programs
programs = robot.cgtp.list_tp_programs()

# Edit source code (firmware V9.10+)
robot.cgtp.insert_source_line("MY_PROGRAM", "L P[5] 100mm/sec FINE", 3)
robot.cgtp.replace_source_line("MY_PROGRAM", "J P[1] 50% FINE", 5)
robot.cgtp.delete_source_lines("MY_PROGRAM", 4, 2)

# Read program properties
comment = robot.cgtp.get_program_comment("MY_PROGRAM")
owner = robot.cgtp.get_program_owner("MY_PROGRAM")
ignore_pause = robot.cgtp.get_program_ignore_pause("MY_PROGRAM")

# Write program properties
robot.cgtp.set_program_comment("MY_PROGRAM", "Updated comment")
robot.cgtp.set_program_sub_type("MY_PROGRAM", CgtpProgramSubType.Macro)
```

## API reference

**CgtpProgramType** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpprogramtype))

- Tp: TP program
- Karel: Karel program
**CgtpProgramSubType** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpprogramsubtype))

- None_: No specific sub-type.
- Job: Job program.
- Process: Process program.
- Macro: Macro program.
- Condition: Condition handler program.
