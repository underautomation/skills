# Run a program remotely

Start, pause, abort, and monitor Fanuc programs remotely using Telnet, CGTP, SNPX system variables, or RMI.

Web page: https://underautomation.com/fanuc/documentation/run-program-remotely

This article compares the ways to start, pause and abort the TP programs of a Fanuc controller from a PC with the Fanuc SDK: Telnet KCL, CGTP, RMI and SNPX. The table at the end says which protocol supports which command.

## Telnet KCL

Telnet provides the most complete program control through KCL commands:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "TELNET_PASS"
robot.connect(parameters)

# Run a program
robot.telnet.run("MyProgram")

# Pause (stops at next fine point)
robot.telnet.pause("MyProgram")

# Hold (decelerates and stops at current position)
robot.telnet.hold("MyProgram")

# Resume a paused or held program
robot.telnet.continue_("MyProgram")

# Abort a program
robot.telnet.abort("MyProgram", force=True)

# Abort all running programs
robot.telnet.abort_all(force=True)

# Reset alarms (same as FAULT RESET button)
robot.telnet.reset()

# Clear program variables
robot.telnet.clear_vars("MyProgram")
```

See also: [Telnet Program control](telnet-program-control.md)

## CGTP Web Server

CGTP can run, select, pause, and abort programs, plus manage program properties:

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

See also: [CGTP Program management](cgtp-programs.md)

## RMI

RMI sends TP-equivalent motion instructions directly, without selecting a program:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.tp_instructions.linear_motion_tp_instruction import LinearMotionTpInstruction
from underautomation.fanuc.rmi.data.rmi_linear_speed_type import RmiLinearSpeedType
from underautomation.fanuc.rmi.data.rmi_termination_type import RmiTerminationType
from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Start the RMI_MOVE program on the controller
robot.rmi.initialize()

# Send a linear motion, the SDK gives the sequence ID
instr = LinearMotionTpInstruction()
instr.speed_type = RmiLinearSpeedType.MmSec
instr.speed = 100
instr.term_type = RmiTerminationType.Fine
instr.target = CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(instr)

# Pause, continue, then stop the RMI_MOVE program
robot.rmi.pause()
robot.rmi.continue_()
robot.rmi.abort()

robot.disconnect()
```

See also: [RMI overview](rmi.md)

## SNPX (indirect)

### Select the program

Set the program name using the `$SHELL_WRK.$CUST_NAME` system variable. Do not include the `.TP` extension. The code is at the end of this section.

### Enable remote control

To allow external control, set the system variable `$RMT_MASTER` to `1`, and `$REMOTE_CFG.$REMOTE_TYPE` to `1`: the master device is then KCL, which allows a program to be started from the PC. The same values are needed to run a program with Telnet KCL or CGTP.

### Option 1: start with a system variable (Production Start Method = OTHER)

When **Production Start Method** is set to **OTHER**, trigger the start by setting `$SHELL_WRK.$CUST_START` to `1`.

The controller automatically clears this bit once it acknowledges the command.

### Option 2: UOP Cycle Start (Production Start Method = UOP)

This method uses the UI (User Input) signals, which also give the other commands of the next section.

**Step 1: map the UI signals to flags.** Open `MENU`, `I/O`, `UOP`, select `UI`, then `CONFIG`.

Link UI signals to Flags (Rack 34, Slot 1):

| Configuration | Result |
|---------------|--------|
| UI[1-8] to Rack 34, Slot 1, Start 1 | UI[1]=F[1], UI[2]=F[2], ... UI[8]=F[8] |
| UI[1-8] to Rack 34, Slot 1, Start 4 | UI[1]=F[4], UI[2]=F[5], ... UI[8]=F[11] |
| UI[6-6] to Rack 34, Slot 1, Start 9 | UI[6]=F[9] |

> The mapping is **bidirectional**: read UI state from flags, or write to flags to change UI state.

**Cold start** the controller after configuration.

**Step 2: pulse the Cycle Start flag.** To start the program, pulse the flag mapped to UI[6:Cycle Start].

## Controlling Program Execution via UOP

The UI signals of the UOP interface control the execution:

| UI Signal | Name | Function | Code Example |
|-----------|------|----------|--------------|
| UI[2] | Hold | Pause program execution | `robot.Snpx.Flags.Write(2, false);` |
| UI[4] | Cycle Stop | Stop the current cycle | `robot.Snpx.Flags.Write(4, false);` |
| UI[5] | Fault Reset | Clear active alarms | `robot.Snpx.Flags.Write(5, true);` |
| UI[6] | Cycle Start | Start/resume program | `robot.Snpx.Flags.Write(6, true);` |
| UI[18] | Prod Start | Alternative production start | `robot.Snpx.Flags.Write(18, true);` |

> **Note:** You can also configure **RSR**, **PNS**, or **STYLE** as the Production Start Method and use UI[9-16] bound to flags to start associated programs. Refer to FANUC manuals for specific bit patterns.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Clear any existing alarms
robot.snpx.clear_alarms()

# Enable remote control (1 = KCL)
robot.snpx.integer_system_variables.write("$RMT_MASTER", 1)

# Select the program to run
programName = "MY_PROGRAM"
robot.snpx.string_system_variables.write("$SHELL_WRK.$CUST_NAME", programName)
print(f"Selected program: {programName}")

# Start the program (using system variable method)
print("Starting program...")
robot.snpx.integer_system_variables.write("$SHELL_WRK.$CUST_START", 1) # or you can set the flag for UOP cycle start if that's your configured method
```

## Protocol comparison

| Feature | Telnet | CGTP | RMI | SNPX |
|---------|--------|------|-----|------|
| **Run program** | Yes | Yes (V9.30+) | Via motion commands | Indirect (variables) |
| **Pause** | Yes (Hold) | Yes | Yes | No |
| **Continue** | Yes | No | Yes | No |
| **Abort** | Yes | Yes | Yes | No |
| **Select/Deselect** | Yes | Yes | N/A | No |
| **Create/Delete** | No | Yes | No | No |
