# Positions

Read the Cartesian position in mm and degrees, the joint pulses, the position error and the torque of a Yaskawa robot, a station or a base axis.

Web page: https://underautomation.com/yaskawa/documentation/hses-positions

This page shows how to read the position of a Yaskawa Motoman robot with the SDK: the Cartesian position of the tool, the joint positions, the position error and the torque, for the robot, a station or base axes. All these methods only read: they work in any mode.

## Cartesian position

`GetRobotCartesianPosition()` reads the position of the tool center point of the first robot, in mm and degrees.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

p = robot.high_speed_e_server.get_robot_cartesian_position()

# Tool center point in mm, orientation in degrees
print(f"X={p.x} Y={p.y} Z={p.z}")
print(f"Rx={p.rx} Ry={p.ry} Rz={p.rz}")

# Frame, tool and posture of the position
print(f"{p.data_type.name}, tool {p.tool_number}, user frame {p.user_coordinate_number}")
print(p.form)

robot.disconnect()
```

| Property               | Content                                                                        |
| ---------------------- | ------------------------------------------------------------------------------ |
| `X`, `Y`, `Z`          | Position, in mm                                                                |
| `Rx`, `Ry`, `Rz`       | Orientation, in degrees                                                        |
| `DataType`             | Frame of the values, for example `RobotCoordinateValue`                        |
| `ToolNumber`           | Tool used for the position                                                     |
| `UserCoordinateNumber` | User frame, when `DataType` is `UserCoordinateValue`                           |
| `Form`                 | Posture of the robot, see [Motion](hses-motion.md#posture) |

Keep the `Form` of a position when you send the robot back to it: the same Cartesian position can be reached with several postures.

## Joint positions

`GetRobotJointPosition()` reads the position of each axis of the first robot, in encoder pulses.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

joints = robot.high_speed_e_server.get_robot_joint_position()

# One value per axis, in encoder pulses. Index 0 is the S axis
pulses = list(joints.axes)
print(pulses)

# The same values, axis by axis
print(f"S={joints.axis1} L={joints.axis2} U={joints.axis3} R={joints.axis4} B={joints.axis5} T={joints.axis6}")

robot.disconnect()
```

`Axes` has 8 values. On a 6 axis robot, the indexes 0 to 5 are the axes S, L, U, R, B and T, and the indexes 6 and 7 are `0`. `Axis1` to `Axis8` give the same values. [Axis names](hses-system.md#axis_names) gives the axes of your robot.

The pulses are the unit of the controller for the joints. The number of pulses per degree depends on the axis and on the robot model: it is a parameter of the controller. Send the pulses back to `MoveJoints` as they are, without conversion.

## Position error and torque

`GetPositionError()` reads the difference between the command and the feedback of each axis, in pulses. `GetTorque()` reads the torque of each axis, in percent of the rated torque.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.robot_control_group import RobotControlGroup

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# The first robot, in pulses
r1 = RobotControlGroup.DefaultRobotPulse

# Difference between the command and the feedback of each axis, in pulses
error = robot.high_speed_e_server.get_position_error(r1)
print(list(error.axes))

# Torque of each axis, in percent of the rated torque
torque = robot.high_speed_e_server.get_torque(r1)
print(list(torque.axes))

robot.disconnect()
```

Read them in a loop during a move to see the load of each axis, or to detect a collision or a wear in your application.

In Python 2.2.0, these two methods take the control group, as in the code above.

## Other control groups

A controller can drive several robots, base axes (travel tracks) and stations (positioners). `GetRobotPosition(group)`, `GetPositionError(group)` and `GetTorque(group)` read the axes of one control group.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.robot_control_group import RobotControlGroup
from UnderAutomation.Yaskawa.HighSpeedEServer import ControlGroup

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Version 2.2.0: ControlGroup comes from the .NET namespace (see the Python page)

# Second robot of the controller, in pulses
r2 = RobotControlGroup(ControlGroup.RobotPulseValue, 2)
r2_joints = robot.high_speed_e_server.get_robot_position(r2)

# First base axis group (travel track), in pulses
b1 = RobotControlGroup(ControlGroup.BasePulseValue, 1)
b1_axes = robot.high_speed_e_server.get_robot_position(b1)

# Torque of the base axes
b1_torque = robot.high_speed_e_server.get_torque(b1)

robot.disconnect()
```

| `ControlGroup`    | Axes, unit                                | Number                |
| ----------------- | ----------------------------------------- | --------------------- |
| `RobotPulseValue` | Robot, in pulses                          | `1` to `8` (R1 to R8) |
| `RobotCartesian`  | Robot, Cartesian values of the controller | `1` to `8`            |
| `BasePulseValue`  | Base axes, in pulses                      | `1` to `8` (B1 to B8) |
| `BaseCartesian`   | Base axes, Cartesian values               | `1` to `8`            |

`GetRobotPosition` returns the raw values of the controller. With a Cartesian group, `Axes` holds X, Y, Z in micrometers and Rx, Ry, Rz in 1/10000 degree. `GetRobotCartesianPosition()` does this conversion for the first robot.

`RobotControlGroup.DefaultRobotCartesian` and `RobotControlGroup.DefaultRobotPulse` are the groups of the first robot, in .NET.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**RobotPositionCartesianData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotpositioncartesiandata))

- `form: RobotPosture (read only)`: Gets the robot posture (form) data defining the kinematic configuration.
- `data_type: RobotPositionDataType (read only)`: Gets the position data type indicating the coordinate system used.
- `tool_number: int (read only)`: Gets the tool number (TCP) used for this position.
- `user_coordinate_number: int (read only)`: Gets the user coordinate system number used for this position.
- `x: float (read only)`: Gets the X coordinate in millimeters.
- `y: float (read only)`: Gets the Y coordinate in millimeters.
- `z: float (read only)`: Gets the Z coordinate in millimeters.
- `rx: float (read only)`: Gets the rotation around X axis (Rx) in degrees.
- `ry: float (read only)`: Gets the rotation around Y axis (Ry) in degrees.
- `rz: float (read only)`: Gets the rotation around Z axis (Rz) in degrees.

**RobotPositionIntData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotpositionintdata))

- `RobotPositionIntData(header: RobotDataHeader)`: Creates a new instance of RobotPositionIntData with the specified header information.
- `to_cartesian() -> RobotPositionCartesianData`: Converts a Cartesian position to millimeters and degrees.
- `form: RobotPosture`: Gets or sets the robot posture (form) data defining the robot's kinematic configuration. This includes flip/no-flip state, arm configuration (upper/lower), and axis angle ranges.
- `data_type: RobotPositionDataType`: Gets or sets the position data type indicating the coordinate system used. Determines how axis values should be interpreted (pulse, base, robot, user, or tool coordinates).
- `tool_number: int`: Gets or sets the tool number (TCP - Tool Center Point) used for this position. Tool numbers typically range from 0-63, where 0 is often the robot flange center.
- `user_coordinate_number: int`: Gets or sets the user coordinate system number used for this position. User coordinates define custom reference frames for specific workpiece locations.
- `is_defined: bool (read only)`: Gets whether the variable is taught on the controller. False for a variable read with Int32%2cSystem.Int32) that is not defined: its values are then all 0.
- `axes: typing.List[int] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: int`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: int`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: int`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: int`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: int`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: int`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: int`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: int`: Gets or sets the value for axis 8 (optional additional axis).

**RobotAxisIntData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotaxisintdata))

- `axes: typing.List[int] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: int`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: int`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: int`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: int`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: int`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: int`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: int`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: int`: Gets or sets the value for axis 8 (optional additional axis).

**RobotControlGroup** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotcontrolgroup))

- `RobotControlGroup(group: ControlGroup, index: int)`: Creates a new RobotControlGroup with the specified group type and index.
- `group: ControlGroup`: The control group type (robot, base, station).
- `index: int`: The index within the control group (e.g., robot number 1-8).
- `byte_value: int`: The combined byte value sent to the robot controller (Group + Index).
- `static DefaultRobotCartesian: 'RobotControlGroup'`: Default control group for Cartesian position of robot 1.
- `static DefaultRobotPulse: 'RobotControlGroup'`: Default control group for pulse position of robot 1.

**ControlGroup** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#controlgroup))

- RobotPulseValue: Robot axes in pulse (encoder) values. Valid index: 1-8.
- BasePulseValue: Base axes in pulse values. Valid index: 1-8.
- StationPulseValue: Station axes in pulse values. Valid index: 1-24 (S1 to S24).
- RobotCartesian: Robot axes in Cartesian coordinates. Valid index: 1-8.
- BaseCartesian: Base axes in Cartesian coordinates. Valid index: 1-8.

**RobotPositionDataType** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotpositiondatatype))

- PulseValue: Position in encoder pulse values (joint space).
- BaseCoordinateValue: Position in base coordinate system (world frame, value 16).
- RobotCoordinateValue: Position in robot coordinate system (robot base frame, value 17).
- ToolCoordinateValue: Position in tool coordinate system (value 18).
- UserCoordinateValue: Position in user-defined coordinate system (value 19).
