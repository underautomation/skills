# Move the robot from a PC

Switch the servo on and move a Yaskawa robot in a straight line from C# or Python, without a job. Which move to choose, how to wait for the end, and the frequent errors.

Web page: https://underautomation.com/yaskawa/documentation/how-to-move-robot

This article shows how to move a Yaskawa Motoman robot from a PC, without a job, in C# or Python. It gives a complete program that switches the servo on, moves the tool 50 mm up in a straight line, waits for the end of the move and goes back.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- The controller accepts the remote commands. See [Prepare the controller](connect.md#prepare_the_controller).
- The cell is safe for a move: nobody in the cell, the safety functions active. Test at low speed first.

## Which move to choose

| Need                                          | Method and command type                                           |
| --------------------------------------------- | ----------------------------------------------------------------- |
| Go to a Cartesian position in a straight line | `MoveCartesian`, `StraightAbsolute`                               |
| Go to a Cartesian position, fastest path      | `MoveCartesian`, `LinkAbsolute`                                   |
| Move by an offset (approach, retract)         | `MoveCartesian`, `StraightIncrement`                              |
| Go back to a position read in pulses          | `MoveJoints`, `LinkAbsolute`                                      |
| Run a taught path                             | A job: see [Run a job](how-to-run-program.md) |

## Example

```python
import time
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.alarm_reset_type import AlarmResetType
from underautomation.yaskawa.high_speed_e_server.position_command_classification import PositionCommandClassification
from underautomation.yaskawa.high_speed_e_server.position_command_operation_coordinate import PositionCommandOperationCoordinate
from underautomation.yaskawa.high_speed_e_server.position_command_type import PositionCommandType

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))
hses = robot.high_speed_e_server

# 1. Remote mode, no alarm
status = hses.get_status_information()
if not status.command_remote:
    raise RuntimeError("Enable the remote mode")
if status.alarming:
    hses.alarm_reset(AlarmResetType.Reset)

# 2. Servo on
hses.set_servo(True)

# 3. Read the current position, then move 50 mm up in a straight line, at 20 mm/s
start = hses.get_robot_cartesian_position()

hses.move_cartesian(
    start.x, start.y, start.z + 50, start.rx, start.ry, start.rz,
    PositionCommandClassification.Cartesian_MM_S, 20,
    PositionCommandOperationCoordinate.Robot,
    posture=start.form,
    commandtype=PositionCommandType.StraightAbsolute)

# 4. The method returns when the controller accepts the move: wait for the target, 30 s at most
timeout = time.monotonic() + 30
while abs(hses.get_robot_cartesian_position().z - (start.z + 50)) > 0.5:
    if time.monotonic() > timeout:
        raise TimeoutError("Target not reached")
    time.sleep(0.1)

# 5. Back to the start, joint interpolated, at 10 %
hses.move_cartesian(
    start.x, start.y, start.z, start.rx, start.ry, start.rz,
    PositionCommandClassification.LinkPercent, 10,
    PositionCommandOperationCoordinate.Robot,
    posture=start.form,
    commandtype=PositionCommandType.LinkAbsolute)

robot.disconnect()
```

The program:

1. checks the remote mode and resets a pending alarm;
2. switches the servo on;
3. reads the current position and sends a straight move 50 mm above it, at 20 mm/s, with the same posture;
4. reads the position every 100 ms until the robot is within 0.5 mm of the target, with a timeout of 30 s;
5. goes back to the start with a joint move at 10 % of the maximum speed.

## Wait for the end of a move

`MoveCartesian` and `MoveJoints` return when the controller accepts the move. To chain moves or to act after a move, wait for the target as in the example. Send the next move only after the end of the previous one.

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) has the same moves, with one method per type: `MoveLinear`, `MoveJoint`, `MoveIncremental`, `MovePulseJoint` and `MovePulseLinear`. The speed of a linear move is in mm/s or in percent, and the target can be in a user frame or in the tool frame.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.host_control.host_control_coordinate_system import HostControlCoordinateSystem
from underautomation.yaskawa.host_control.host_control_speed_type import HostControlSpeedType

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

robot.e_server.set_servo(True)

# Straight line to X=400 Y=0 Z=300 (mm), Rx=180 Ry=0 Rz=0 (degrees), at 50 mm/s, tool 0
robot.e_server.move_linear(HostControlSpeedType.MillimetersPerSecond, 50,
    HostControlCoordinateSystem.Base, 400, 0, 300, 180, 0, 0)

# Joint move to another target, at 10 % of the maximum speed
robot.e_server.move_joint(10, HostControlCoordinateSystem.Base, 400, 100, 300, 180, 0, 0)

robot.disconnect()
```

## Check the target before the move

The [offline kinematics](kinematics-inverse.md) tell if a target can be reached, and with which joint angles, before you send it. An empty list of solutions means that the robot cannot reach the target.

## Troubleshooting

- **The robot moves by the values instead of going to them:** `MoveCartesian` uses `StraightIncrement` when `commandtype` is not given. Pass `StraightAbsolute` or `LinkAbsolute`.
- **`Servo OFF` or `Turn ON the servo power`:** switch the servo on before the move.
- **`Command remote not set`:** see [Prepare the controller](connect.md#prepare_the_controller).
- **The robot takes another configuration:** pass the posture of the start position (`Form`) to `MoveCartesian`.
- **A speed or frame setting error:** check the pair of `PositionCommandClassification` and command type, and the tool and user frame numbers.

## What to read next

- [Motion](hses-motion.md): all the arguments of the moves.
- [Get the robot position](how-to-get-position.md).
