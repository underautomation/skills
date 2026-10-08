# Positions and torque

Read the joint pulses and the Cartesian position in the base, robot, user or tool frame, the posture, the torque and the encoder temperatures through the Ethernet Server.

Web page: https://underautomation.com/yaskawa/documentation/eserver-positions

This page shows how to read the position of a Yaskawa Motoman robot through the Ethernet Server: joint pulses, Cartesian position in the base, robot, user or tool frame, posture, torque and encoder temperatures. It covers the YRC1000 and YRC1000micro controllers.

## Read the position

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.host_control.host_control_coordinate_system import HostControlCoordinateSystem

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Joints, in encoder pulses
joints = robot.e_server.get_robot_joint_position()
print(f"S={joints.s} L={joints.l} U={joints.u} R={joints.r} B={joints.b} T={joints.t}")

# Cartesian position in the base frame (default), mm and degrees
tcp = robot.e_server.get_robot_cartesian_position()
print(f"X={tcp.x} Y={tcp.y} Z={tcp.z} Rx={tcp.rx} Ry={tcp.ry} Rz={tcp.rz}")

# Posture of the arm and tool of the position
print(f"Front: {tcp.is_front}, upper arm: {tcp.is_upper_arm}, flip: {tcp.is_flip}, tool: {tcp.tool_number}")

# Same position in the robot frame, or in a user frame
in_robot = robot.e_server.get_robot_cartesian_position(HostControlCoordinateSystem.Robot)
in_user1 = robot.e_server.get_robot_cartesian_position(HostControlCoordinateSystem.User1)

# With the external axes (re, axis8...)
with_external = robot.e_server.get_robot_cartesian_position(HostControlCoordinateSystem.Base, True)

robot.disconnect()
```

### Joint position

`GetRobotJointPosition()` reads the encoder pulses of each axis: `S`, `L`, `U`, `R`, `B`, `T`, then `E` and `Axis8` to `Axis12` for the external axes. `Axes` gives the same values in one array of 12 values.

The number of pulses per degree depends on the axis and on the robot model. To compute a position from joint angles, see [Offline kinematics](kinematics.md).

### Cartesian position

`GetRobotCartesianPosition(coordinateSystem, includeExternalAxes)` reads the position of the tool center point, in mm and degrees.

| `HostControlCoordinateSystem` | Frame of the values      |
| ----------------------------- | ------------------------ |
| `Base` (default)              | Base frame               |
| `Robot`                       | Robot frame              |
| `User1` to `User8`            | User frame 1 to 8        |
| `Tool`                        | Tool frame               |

`ToolNumber` gives the tool of the position. On a 7-axis robot, `Re` holds the elbow angle.

With `includeExternalAxes` set to `true`, `Axis8` to `Axis12` also hold the positions of the external axes. On a 6-axis robot, `Re` holds the 7th axis.

On a robot without base axis, the base frame and the robot frame give the same values.

### Posture

The same Cartesian position can be reached with several postures of the arm. `Type` holds the posture, and these properties decode it:

| Property                                         | Meaning                                       |
| ------------------------------------------------ | --------------------------------------------- |
| `IsFront`                                        | The wrist is in front of the S axis           |
| `IsUpperArm`                                     | The elbow is above the line shoulder to wrist |
| `IsFlip`                                         | Flip posture of the wrist                     |
| `IsRLessThan180`, `IsTLessThan180`, `IsSLessThan180` | The angle of the axis is less than 180 degrees |

Pass the `Type` to `MoveJoint` and `MoveLinear` to send the robot back to a position with the same posture. See [Motion](eserver-motion.md).

## Torque and encoder temperatures

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Torque of each axis, in percent of the rated torque
torque = robot.e_server.get_torque()
max_torque = robot.e_server.get_max_torque()

# Temperature of the encoder of each axis, in degrees Celsius
temperatures = robot.e_server.get_encoder_temperature()

for axis in range(6):
    print(f"Axis {axis + 1}: {torque.values[axis]} % (max {max_torque.values[axis]} %), {temperatures.values[axis]} C")

robot.disconnect()
```

| Method                    | Values                                                    |
| ------------------------- | --------------------------------------------------------- |
| `GetTorque()`             | Torque of each axis, in percent of the rated torque       |
| `GetMaxTorque()`          | Maximum torque of each axis, in percent                   |
| `GetEncoderTemperature()` | Temperature of the encoder of each axis, in degrees Celsius |

Each array has 12 values: the 6 axes of the robot, then the external axes. With the servo off, the torques are 0. A log of the encoder temperatures over a shift shows which axis heats up in a cycle.

## Control group and task

`GetControlGroup()` reads the robot group, the station group and the task selected for the next commands. `SetControlGroup(robotGroup, stationGroup)` and `SetTask(task)` change them, on a controller with several robots, stations or tasks.

## Reference



**HostControlJointPositionData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontroljointpositiondata))

- `s: int (read only)`: Gets or sets the S axis position in pulses.
- `l: int (read only)`: Gets or sets the L axis position in pulses.
- `u: int (read only)`: Gets or sets the U axis position in pulses.
- `r: int (read only)`: Gets or sets the R axis position in pulses.
- `b: int (read only)`: Gets or sets the B axis position in pulses.
- `t: int (read only)`: Gets or sets the T axis position in pulses.
- `e: int (read only)`: Gets or sets the E axis (7th axis) position in pulses.
- `axis8: int (read only)`: Gets or sets the 8th axis position in pulses.
- `axis9: int (read only)`: Gets or sets the 9th axis position in pulses.
- `axis10: int (read only)`: Gets or sets the 10th axis position in pulses.
- `axis11: int (read only)`: Gets or sets the 11th axis position in pulses.
- `axis12: int (read only)`: Gets or sets the 12th axis position in pulses.
- `axes: typing.List[int] (read only)`: Gets all axis values as an array of encoder pulse values. Array contains 12 elements: S, L, U, R, B, T, E, Axis8 through Axis12.
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

**HostControlCartesianPositionData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolcartesianpositiondata))

- `x: float (read only)`: Gets or sets the X position in millimeters.
- `y: float (read only)`: Gets or sets the Y position in millimeters.
- `z: float (read only)`: Gets or sets the Z position in millimeters.
- `rx: float (read only)`: Gets or sets the Rx (rotation around X axis) in degrees.
- `ry: float (read only)`: Gets or sets the Ry (rotation around Y axis) in degrees.
- `rz: float (read only)`: Gets or sets the Rz (rotation around Z axis) in degrees.
- `re: float (read only)`: Gets the elbow angle Re of a 7-axis robot, in degrees. On a 6-axis robot, value of the 7th axis (degrees or millimeters) when the external axes are read, 0 otherwise.
- `tool_number: int (read only)`: Gets the tool number (0 to 63) of the position.
- `axis8: float (read only)`: Gets or sets the 8th external axis value.
- `axis9: float (read only)`: Gets or sets the 9th external axis value.
- `axis10: float (read only)`: Gets or sets the 10th external axis value.
- `axis11: float (read only)`: Gets or sets the 11th external axis value.
- `axis12: float (read only)`: Gets or sets the 12th external axis value.
- `type: int (read only)`: Gets or sets the robot posture/configuration type. Defines arm configuration (flip, upper/lower arm, front/back, etc.). Use is_flip, is_upper_arm, is_front... to read it.
- `coordinate_system: int (read only)`: Gets or sets the coordinate system index. 0: Base, 1-65: User coordinates.
- `is_flip: bool (read only)`: Gets whether the robot is in flip configuration.
- `is_upper_arm: bool (read only)`: Gets whether the robot is in upper arm configuration.
- `is_front: bool (read only)`: Gets whether the robot is in front configuration.
- `is_r_less_than180: bool (read only)`: Gets whether R axis is less than 180 degrees.
- `is_t_less_than180: bool (read only)`: Gets whether T axis is less than 180 degrees.
- `is_s_less_than180: bool (read only)`: Gets whether S axis is less than 180 degrees.
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

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

**HostControlTorqueData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontroltorquedata))

- `values: typing.List[float] (read only)`: Gets the torque values for each axis (up to 12 axes). Values are in percentage of maximum rated torque.
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

**HostControlEncoderTemperatureData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolencodertemperaturedata))

- `values: typing.List[float] (read only)`: Gets the temperature values for each axis encoder (up to 12 axes). Values are in degrees Celsius.
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

**HostControlGroupData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolgroupdata))

- `robot_group: int (read only)`: Gets or sets the robot group bits. Each bit represents a robot control group (R1, R2, etc.).
- `station_group: int (read only)`: Gets or sets the station group bits. Each bit represents a station control group (S1, S2, etc.).
- `task: int (read only)`: Gets or sets the current task number. 0: Master task, 1-15: Sub tasks.
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## What to read next

- [Get the robot position](how-to-get-position.md): which protocol and which method to choose.
- [Motion](eserver-motion.md): send the robot to a position.
