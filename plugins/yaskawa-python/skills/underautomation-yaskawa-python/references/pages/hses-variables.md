# Variables and registers

Read and write the B, I, D, R and S variables, the P, BP and EX position variables and the M registers of a Yaskawa controller.

Web page: https://underautomation.com/yaskawa/documentation/hses-variables

This page shows how to read and write the variables and the registers of a Yaskawa Motoman controller with the SDK. A job and a PC exchange data through these variables: counters, offsets, recipe numbers, positions.

## Variable types

| Variable | Content                               | Read                   | Write                   | .NET type                 |
| -------- | ------------------------------------- | ---------------------- | ----------------------- | ------------------------- |
| `B`      | Byte, 0 to 255                        | `ReadByte`             | `WriteByte`             | `byte[]`                  |
| `I`      | Integer, 16 bits                      | `ReadInteger`          | `WriteInteger`          | `short[]`                 |
| `D`      | Double integer, 32 bits               | `ReadDoubleInteger`    | `WriteDoubleInteger`    | `int[]`                   |
| `R`      | Real, 32 bit floating point           | `ReadReal`             | `WriteReal`             | `float[]`                 |
| `S`      | String of 16 bytes                    | `Read16BytesChar`      | `Write16BytesChar`      | `string[]`                |
| `S`      | String of 32 bytes                    | `Read32BytesChar`      | `Write32BytesChar`      | `string[]`                |
| `P`      | Robot position                        | `ReadPositionVariable` | `WritePositionVariable` | `RobotPositionIntData[]`  |
| `BP`     | Base axis position                    | `ReadBasePosition`     | `WriteBasePosition`     | `RobotBasePositionData[]` |
| `EX`     | Station axis position                 | `ReadExternalPosition` | `WriteExternalPosition` | `RobotExternalAxisData[]` |
| `M`      | Register of the concurrent I/O ladder | `ReadRegister`         | `WriteRegister`         | `short[]`                 |

Every read method takes the number of the first variable and a count: `ReadInteger(10, 2)` reads `I010` and `I011`. It returns an object whose `Value` is an array, one item per variable. Every write method takes the number of the first variable and an array: one call writes several variables in a row.

The numbers start at `0` (`B000`, `I000`...). The number of variables of each type depends on the controller and on its settings.

## Numeric variables

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# B000 to B003: byte variables (0 to 255)
b = list(robot.high_speed_e_server.read_byte(0, 4).value)
robot.high_speed_e_server.write_byte(0, [1, 2, 3, 4])

# I010 and I011: integer variables (16 bits)
i = list(robot.high_speed_e_server.read_integer(10, 2).value)
robot.high_speed_e_server.write_integer(10, [-100, 200])

# D000: double integer variable (32 bits)
d = list(robot.high_speed_e_server.read_double_integer(0, 1).value)
robot.high_speed_e_server.write_double_integer(0, [100000])

# R005 to R007: real variables (32 bit floating point)
r = list(robot.high_speed_e_server.read_real(5, 3).value)
robot.high_speed_e_server.write_real(5, [1.5, -2.25, 3.0])

robot.disconnect()
```

- `D` variables are 32 bit integers, not floating point values. Use `R` variables for decimal values.

## String variables

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# S000 and S001: string variables of 16 bytes
texts = list(robot.high_speed_e_server.read16_bytes_char(0, 2).value)

# Longer strings are cut to 16 characters
robot.high_speed_e_server.write16_bytes_char(0, ["PART-A", "BATCH 12"])

# String variables of 32 bytes, on the controllers that have them
long_texts = list(robot.high_speed_e_server.read32_bytes_char(0, 1).value)
robot.high_speed_e_server.write32_bytes_char(0, ["Reference 2026-10-01 line 4"])

robot.disconnect()
```

A string longer than the size of the variable is cut. Write ASCII characters only.

The 32 byte strings exist on the controllers that store their `S` variables in 32 bytes. On the others, the controller refuses the request.

## Position variables

A `P` variable holds a robot position: in pulses, or in a Cartesian frame with a tool, a user frame and a posture.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.robot_position_int_data import RobotPositionIntData
from underautomation.yaskawa.high_speed_e_server.robot_position_data_type import RobotPositionDataType
from underautomation.yaskawa.high_speed_e_server.robot_posture import RobotPosture

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# P000: a position variable
p0 = robot.high_speed_e_server.read_position_variable(0, 1).value[0]

# PulseValue: axes are pulses. Otherwise: X, Y, Z in micrometers, Rx, Ry, Rz in 1/10000 degree
print(f"{p0.data_type.name}, tool {p0.tool_number}: {list(p0.axes)}")

# P001: a Cartesian position in the robot frame
p1 = RobotPositionIntData(None)
p1.data_type = RobotPositionDataType.RobotCoordinateValue
p1.form = RobotPosture.from_integer(0)
p1.tool_number = 0
p1.user_coordinate_number = 0
p1.axis1 = 850000   # X = 850 mm
p1.axis2 = 0        # Y
p1.axis3 = 400000   # Z = 400 mm
p1.axis4 = 1800000  # Rx = 180 degrees
p1.axis5 = 0        # Ry
p1.axis6 = 0        # Rz

robot.high_speed_e_server.write_position_variable(1, [p1])

robot.disconnect()
```

| `DataType`                                                                                  | `Axes`                                                    |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `PulseValue`                                                                                | One value per axis, in pulses                             |
| `BaseCoordinateValue`, `RobotCoordinateValue`, `UserCoordinateValue`, `ToolCoordinateValue` | X, Y, Z in micrometers, then Rx, Ry, Rz in 1/10000 degree |

The units of a `P` variable are the raw units of the controller: 850 mm is `850000`. They differ from `GetRobotCartesianPosition()`, which returns mm and degrees.

To write a variable, set `Form`: `new RobotPosture()` is the default posture. In Python, use `RobotPosture.from_integer(0)`.

A variable that was never taught has `IsDefined` set to `false`, and all its values are 0. `ToCartesian()` converts a Cartesian variable to mm and degrees, the units of `GetRobotCartesianPosition()`. It throws an `InvalidOperationException` for a variable in pulses.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.robot_position_data_type import RobotPositionDataType

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

p10 = robot.high_speed_e_server.read_position_variable(10, 1).value[0]

# A variable never taught: all values are 0
if not p10.is_defined:
    print("P010 is not taught")
elif p10.data_type != RobotPositionDataType.PulseValue:
    # Raw units (micrometers, 1/10000 degree) to mm and degrees
    mm = p10.to_cartesian()
    print(f"X={mm.x} Y={mm.y} Z={mm.z} Rx={mm.rx} Ry={mm.ry} Rz={mm.rz}")

robot.disconnect()
```

`IsDefined` also exists on the base (`BP`) and station (`EX`) position variables.

## Base and station position variables

`BP` variables hold the position of base axes (travel tracks), `EX` variables the position of station axes (positioners). The values are in pulses, up to 8 axes.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# BP000: base axis position variable (travel track)
bp0 = robot.high_speed_e_server.read_base_position(0, 1).value[0]
print(f"{bp0.data_type.name}: {list(bp0.axes)}")

# Change the first axis and write the variable back
bp0.axis1 += 1000
robot.high_speed_e_server.write_base_position(0, [bp0])

# EX000: station axis position variable (positioner), in pulses
ex0 = robot.high_speed_e_server.read_external_position(0, 1).value[0]
ex0.axis1 = 0
robot.high_speed_e_server.write_external_position(0, [ex0])

robot.disconnect()
```

The data type of a `BP` variable (pulses or base frame) cannot be set by the SDK: read the variable, change its axes and write it back, as above.

## Registers

`M` registers are the 16 bit registers of the concurrent I/O ladder of the controller.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# M000 to M009: registers of the concurrent I/O ladder (16 bits)
registers = list(robot.high_speed_e_server.read_register(0, 10).value)
print(registers)

# Write M560 and M561. The controller refuses the registers reserved for the system
robot.high_speed_e_server.write_register(560, [12, 34])

robot.disconnect()
```

The controller reserves some registers for its own use, and refuses to write them. Check the free registers in the concurrent I/O manual of your controller.

## Errors

- A variable number out of range makes the controller refuse the request: the SDK throws an `InvalidDataAnswerException`.
- One write call takes a limited number of values, for example 120 `D` variables. Beyond, the SDK throws an exception that gives the maximum: split the array in several calls.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/underautomation.yaskawa.high_speed_e_server.internal.md#highspeedeserverclientbase-robothigh_speed_e_server))

- `read_register(firstIndex: int, count: int) -> RobotRegisterData`: Reads multiple 16-bit register values (M variables) from the robot controller. Registers are used for general-purpose integer storage in robot programs.
- `write_register(firstIndex: int, data: typing.List[int]) -> RobotDataHeader`: Writes multiple 16-bit register values (M variables) to the robot controller.
- `read_byte(firstIndex: int, count: int) -> RobotByteVariableData`: Reads multiple byte variables (B variables) from the robot controller. Byte variables are 8-bit unsigned values used for compact data storage.
- `write_byte(firstIndex: int, data: typing.List[int]) -> RobotDataHeader`: Writes byte variables (B variables) to the robot controller.
- `read_integer(firstIndex: int, count: int) -> RobotIntegerVariableData`: Reads multiple integer variables (I variables) from the robot controller. Integer variables are 16-bit signed values (-32768 to 32767).
- `write_integer(firstIndex: int, data: typing.List[int]) -> RobotDataHeader`: Writes integer variables (I variables) to the robot controller.
- `read_double_integer(firstIndex: int, count: int) -> RobotDoubleIntegerVariableData`: Reads multiple double-precision variables (D variables) from the robot controller. Note: The protocol actually transmits float values which are then cast to double.
- `write_double_integer(firstIndex: int, data: typing.List[int]) -> RobotDataHeader`: Writes double-precision variables (D variables) to the robot controller.
- `read_real(firstIndex: int, count: int) -> RobotRealVariableData`: Reads multiple real (single-precision float) variables (R variables) from the robot controller. Real variables are 32-bit IEEE 754 floating-point values.
- `write_real(firstIndex: int, data: typing.List[float]) -> RobotDataHeader`: Writes real (single-precision float) variables (R variables) to the robot controller.
- `read16_bytes_char(firstIndex: int, count: int) -> RobotStringVariableData`: Reads multiple 16-byte string variables (S variables) from the robot controller. String variables are fixed-length, null-terminated ASCII strings.
- `write16_bytes_char(firstIndex: int, data: typing.List[str]) -> RobotDataHeader`: Writes 16-byte string variables (S variables) to the robot controller. Strings longer than 16 characters will be truncated.
- `read32_bytes_char(firstIndex: int, count: int) -> RobotStringVariableData`: Reads multiple 32-byte string variables (S variables) from the robot controller. Available on the controllers that store their S variables in 32 bytes (DX200, YRC1000...). Extended string variables for longer text storage than 16-byte variants.
- `write32_bytes_char(firstIndex: int, data: typing.List[str]) -> RobotDataHeader`: Writes 32-byte string variables (S variables) to the robot controller. Strings longer than 32 characters will be truncated.

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

**RobotPositionDataType** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotpositiondatatype))

- PulseValue: Position in encoder pulse values (joint space).
- BaseCoordinateValue: Position in base coordinate system (world frame, value 16).
- RobotCoordinateValue: Position in robot coordinate system (robot base frame, value 17).
- ToolCoordinateValue: Position in tool coordinate system (value 18).
- UserCoordinateValue: Position in user-defined coordinate system (value 19).

**RobotBasePositionData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotbasepositiondata))

- `RobotBasePositionData(header: RobotDataHeader)`: Creates a new instance of RobotBasePositionData with the specified header information.
- `data_type: RobotBasePositionType (read only)`: Gets the data type indicating whether values are pulse or coordinate values.
- `is_defined: bool (read only)`: Gets whether the variable is taught on the controller. False for a variable read with read_base_position() that is not defined: its values are then all 0.
- `axes: typing.List[int] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: int`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: int`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: int`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: int`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: int`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: int`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: int`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: int`: Gets or sets the value for axis 8 (optional additional axis).

**RobotExternalAxisData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotexternalaxisdata))

- `RobotExternalAxisData(header: RobotDataHeader)`: Creates a new instance of RobotExternalAxisData with the specified header information.
- `is_defined: bool (read only)`: Gets whether the variable is taught on the controller. False for a variable read with read_external_position() that is not defined: its values are then all 0.
- `axes: typing.List[int] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: int`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: int`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: int`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: int`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: int`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: int`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: int`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: int`: Gets or sets the value for axis 8 (optional additional axis).
