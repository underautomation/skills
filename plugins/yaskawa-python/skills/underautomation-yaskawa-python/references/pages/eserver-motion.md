# Motion

Move a Yaskawa robot through the Ethernet Server: linear and joint moves to a Cartesian target in a frame, relative moves and moves to a target in pulses.

Web page: https://underautomation.com/yaskawa/documentation/eserver-motion

This page shows how to move a Yaskawa Motoman robot from a PC through the Ethernet Server, without a job: joint and linear moves to a Cartesian target, relative moves, and moves to a target in pulses. It covers the YRC1000 and YRC1000micro controllers.

## Prerequisites

- The controller is in play mode and in remote mode, without alarm.
- The servo power is on: `SetServo(true)`.
- The target is checked: the controller moves the real robot. Test at low speed first, in a cell with its safety functions active.

## Move to a Cartesian target

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

| Method       | Path                                    | Speed                                              |
| ------------ | --------------------------------------- | -------------------------------------------------- |
| `MoveLinear` | Straight line of the tool center point  | `HostControlSpeedType.MillimetersPerSecond` or `Percentage` |
| `MoveJoint`  | Each joint moves to its target, the tool path is a curve | Percent of the maximum speed           |

The target is X, Y, Z in mm and Rx, Ry, Rz in degrees, in the frame given by `HostControlCoordinateSystem` (base, robot, user frame 1 to 8 or tool). The last two optional parameters are:

- `type`: the posture of the arm. Pass the `Type` of a position read with `GetRobotCartesianPosition()` to keep its posture. See [Positions](eserver-positions.md#posture).
- `toolNumber`: the tool, 0 to 63.

## Relative move

`MoveIncremental` moves the robot by an offset from its current position, in a straight line. In the `Tool` frame, the offset follows the axes of the tool: `X = 20` moves the tool 20 mm along its own X axis.

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

# 50 mm up from the current position, at 20 mm/s
robot.e_server.move_incremental(HostControlSpeedType.MillimetersPerSecond, 20,
    HostControlCoordinateSystem.Base, 0, 0, 50, 0, 0, 0)

# 20 mm along the X axis of the tool
robot.e_server.move_incremental(HostControlSpeedType.MillimetersPerSecond, 20,
    HostControlCoordinateSystem.Tool, 20, 0, 0, 0, 0, 0)

robot.disconnect()
```

## Move to a target in pulses

`MovePulseJoint` and `MovePulseLinear` take the target of each axis in encoder pulses (S, L, U, R, B, T), as read with `GetRobotJointPosition()`.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.host_control.host_control_speed_type import HostControlSpeedType

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

robot.e_server.set_servo(True)

# Joint move to a target in pulses (S, L, U, R, B, T), at 5 % of the maximum speed
robot.e_server.move_pulse_joint(5, 0, 0, 0, 0, 0, 0)

# Linear move to a target in pulses, at 30 mm/s
current = robot.e_server.get_robot_joint_position()
robot.e_server.move_pulse_linear(HostControlSpeedType.MillimetersPerSecond, 30,
    current.s + 1000, current.l, current.u, current.r, current.b, current.t)

robot.disconnect()
```

## End of the move

A move method returns when the controller answers. The SDK waits for this answer up to `MotionTimeoutMilliseconds` (30 s by default). To know that the robot has stopped, read `GetStatusInformation().Running` until it is `false`. To stop a move, hold the robot with `SetHold(true)`.

## Reference

**Methods of HostControlClientBase** ([reference](../api/underautomation.yaskawa.host_control.internal.md#hostcontrolclientbase-robote_server))

- `move_joint(speedPercent: int, coordinateSystem: HostControlCoordinateSystem, x: float, y: float, z: float, rx: float, ry: float, rz: float, type: int=0, toolNumber: int=0) -> HostControlResponse`: Moves the robot to a Cartesian position using joint interpolation. Joint motion is faster but the path is not linear.
- `move_linear(speedType: HostControlSpeedType, speed: float, coordinateSystem: HostControlCoordinateSystem, x: float, y: float, z: float, rx: float, ry: float, rz: float, type: int=0, toolNumber: int=0) -> HostControlResponse`: Moves the robot to a Cartesian position using linear interpolation. Linear motion follows a straight line path.
- `move_incremental(speedType: HostControlSpeedType, speed: float, coordinateSystem: HostControlCoordinateSystem, dx: float, dy: float, dz: float, drx: float, dry: float, drz: float, toolNumber: int=0) -> HostControlResponse`: Moves the robot incrementally using linear interpolation. Movement is relative to the current position.
- `move_pulse_joint(speedPercent: int, s: int, l: int, u: int, r: int, b: int, t: int, toolNumber: int=0) -> HostControlResponse`: Moves the robot to a pulse position using joint interpolation.
- `move_pulse_linear(speedType: HostControlSpeedType, speed: float, s: int, l: int, u: int, r: int, b: int, t: int, toolNumber: int=0) -> HostControlResponse`: Moves the robot to a pulse position using linear interpolation.

**HostControlSpeedType** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolspeedtype))

- Percentage: Speed is specified as a percentage of maximum speed (V).
- MillimetersPerSecond: Speed is specified in mm/s (VE).

**HostControlCoordinateSystem** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolcoordinatesystem))

- Base: Base coordinate system (robot base frame).
- Robot: Robot coordinate system.
- User1: User coordinate system 1.
- User2: User coordinate system 2.
- User3: User coordinate system 3.
- User4: User coordinate system 4.
- User5: User coordinate system 5.
- User6: User coordinate system 6.
- User7: User coordinate system 7.
- User8: User coordinate system 8.
- Tool: Tool coordinate system.

## What to read next

- [Move the robot from a PC](how-to-move-robot.md): which protocol to choose, and a complete program.
- [Offline kinematics](kinematics.md): check that a target can be reached before you send it.
