# Move the robot from a PC

Move a UR cobot from a PC in C# or Python with URScript, the Interpreter Mode, registers or a program, and check the position reached.

Web page: https://underautomation.com/universal-robots/documentation/how-to-move-robot

This article shows how to move a Universal Robots cobot from a PC, in C# or Python: a linear move or a joint move to a target, then a check of the position reached. It compares the ways to send a move and says which one to choose.

## Which way to choose

| Way                              | How                                                                   | Effect on the running program          | When                                         |
| -------------------------------- | --------------------------------------------------------------------- | -------------------------------------- | -------------------------------------------- |
| URScript, Primary Interface      | `Script.Send("movel(...)")`                                           | It stops: the script runs instead      | A move from the PC, no program on the robot  |
| Interpreter Mode                 | `ExecuteCommand("movel(...)")` in a program in `interpreter_mode()`   | It continues after the moves           | Moves inside a program of the operator       |
| Registers and a robot program    | RTDE writes the target in registers, the program reads them and moves | It runs the moves                      | A fixed program that the PC drives           |
| A `.urp` program                 | SFTP, then Dashboard Server or REST `LoadProgram`, `Play`              | It is replaced                         | Moves taught in PolyScope                    |

For a quick test, URScript is the shortest way. For a cell in production, a program on the robot that reads its targets in registers keeps the control on the robot side, where the operator sees it.

## Prerequisites

- The robot is powered on, its brakes are released, and it is in remote control: see [Run a program](how-to-run-program.md) for the power on.
- The Primary Interface is connected on port 30001 (the default).
- The target is reachable and the path is free. Test with low speeds, and on [URSim](configure-offline-simulator.md) first.

## Example

The program sends a linear move to a target, waits for its end, prints the distance to the target, then starts a joint move and stops it after 1 s.

```python
import math
import time
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.common.pose import Pose

def wait_for(condition, seconds):
    end = time.monotonic() + seconds
    while not condition():
        if time.monotonic() > end:
            raise TimeoutError()
        time.sleep(0.05)

robot = UR()

# Primary Interface and Dashboard Server
robot.connect("192.168.0.1")

# Target of the tool: X, Y, Z in m, rotation vector in rad
target = Pose(0.4, -0.1, 0.3, 0, 3.14, 0)
p = f"p[{target.x},{target.y},{target.z},{target.rx},{target.ry},{target.rz}]"

# A linear move at 0.1 m/s. The script runs as a program:
# a program that runs on the robot stops
robot.primary_interface.script.send(f"movel({p}, a=0.5, v=0.1)")

# Wait for the start, then for the end of the move
wait_for(lambda: robot.primary_interface.robot_mode_data.program_running, 2)
wait_for(lambda: not robot.primary_interface.robot_mode_data.program_running, 60)

# Check the position reached
reached = robot.primary_interface.cartesian_info.as_pose()
error = math.dist((reached.x, reached.y, reached.z), (target.x, target.y, target.z))
print(f"Position error: {error * 1000:.1f} mm")

# A move in the joint space, joint positions in rad
robot.primary_interface.script.send("movej([0, -1.57, 1.57, -1.57, -1.57, 0], a=1.2, v=0.5)")

# To stop it before its end: a new script replaces the running one
time.sleep(1)
robot.primary_interface.script.send("stopj(2)")  # 2 rad/s² deceleration
```

### Units and format

The target of `movel` is a pose `p[x, y, z, rx, ry, rz]`: meters and a rotation vector in radians, in the base frame. `movej` takes 6 joint positions in radians. `a` is the acceleration (m/s² or rad/s²), `v` the speed (m/s or rad/s). Write the numbers with a dot: `CultureInfo.InvariantCulture` in C#.

### End of the move

`Script.Send` returns when the script is sent: the robot does not answer. A script runs as a program, so `RobotModeData.ProgramRunning` is `true` during the move and `false` at its end.

### Compute a target

To move to a pose given by a vision system in another format, convert it with [Pose](tools.md). To choose the joint positions of a pose, use the [inverse kinematics](kinematics.md).

## Troubleshooting

- **Nothing moves:** the robot is in local control, not powered, or its brakes are on. The script can also contain an error: listen to `RuntimeExceptionMessageReceived`.
- **The running program stops:** expected with URScript sent by the Primary Interface. Use the Interpreter Mode to keep it.
- **Protective stop:** the target is not reachable, or the robot hit something. See [Read and reset alarms](how-to-read-reset-alarms.md).

## What to read next

- [Send URScript](remote-send-script.md) and [Interpreter Mode](interpreter-mode.md).
- [Get the robot position](how-to-get-position.md).
