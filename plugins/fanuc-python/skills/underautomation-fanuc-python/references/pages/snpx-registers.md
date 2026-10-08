# Registers

Read and write numeric registers (R[]), position registers (PR[]), string registers (SR[]), and flags (F[]) via SNPX.

Web page: https://underautomation.com/fanuc/documentation/snpx-registers

SNPX provides fast read and write access to all register types: numeric (R[]), position (PR[]), string (SR[]), and flags (F[]).

## Numeric registers (R[])

Numeric registers store floating-point, 32-bit integer, or 16-bit integer values.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Read R[1] as float (default)
value = robot.snpx.numeric_registers.read(1)

# Write R[1]
robot.snpx.numeric_registers.write(1, 123.45)

# Read as 32-bit integer
int_value = robot.snpx.numeric_registers_int32.read(1)
robot.snpx.numeric_registers_int32.write(1, 999)

# Read as 16-bit integer
short_value = robot.snpx.numeric_registers_int16.read(1)
```

## Position registers (PR[])

Position registers store joint or Cartesian positions with tool and frame info.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.cartesian_position import CartesianPosition
from underautomation.fanuc.common.joints_position import JointsPosition

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Read PR[1]
pos_reg = robot.snpx.position_registers.read(1)

user_frame = pos_reg.user_frame
user_tool = pos_reg.user_tool

# cartesian_position and joints_position are never None in version 7.1.0.
# A representation that the register does not hold converts to an empty string.
if str(pos_reg.cartesian_position):
    x = pos_reg.cartesian_position.x

if str(pos_reg.joints_position):
    j1 = pos_reg.joints_position.j1

# Write Cartesian position to PR[1]
robot.snpx.position_registers.write(1, CartesianPosition(100, 200, 300, 0, 90, 0))

# Write joint position to PR[1]
robot.snpx.position_registers.write(1, JointsPosition(j1=0, j2=0, j3=0, j4=0, j5=0, j6=45))
```

To know if a register holds joint or Cartesian values, test each representation of the `Position` you read:

- C#: `JointsPosition` or `CartesianPosition` is `null` when the register does not hold this representation.
- Python (version 7.1.0): `joints_position` and `cartesian_position` never return `None`. A representation that the register does not hold converts to an empty string with `str()`, and reading one of its values raises `AttributeError`. Test `str(pos_reg.joints_position)` before you read the joint values.

## String registers (SR[]) and flags (F[])

The default string length is 80 characters. You can change it with `StringRegisters.StringLength` (must be even, >= 2).

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Read SR[1]
text = robot.snpx.string_registers.read(1)

# Write SR[1]
robot.snpx.string_registers.write(1, "Hello, Robot!")

# Read F[1]
flag = robot.snpx.flags.read(1)

# Write F[1]
robot.snpx.flags.write(1, True)
```

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.cartesian_position import CartesianPosition
from underautomation.fanuc.common.joints_position import JointsPosition

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True

# Connect to the robot
robot.connect(parameters)

# --- Numeric Registers (R[]) ---

# Read R[1]
num_reg1 = robot.snpx.numeric_registers.read(1)
print(f"R[1] = {num_reg1}")

# Write R[1]
robot.snpx.numeric_registers.write(1, 123.45)

# --- Position Registers (PR[]) ---

# Read PR[1]
pos_reg1 = robot.snpx.position_registers.read(1)
print(f"PR[1] UserFrame={pos_reg1.user_frame}, UserTool={pos_reg1.user_tool}")

# Access Cartesian values
if pos_reg1.cartesian_position is not None:
    print(f"  X={pos_reg1.cartesian_position.x}")
    print(f"  Y={pos_reg1.cartesian_position.y}")
    print(f"  Z={pos_reg1.cartesian_position.z}")

# Access joint values
if pos_reg1.joints_position is not None:
    print(f"  J1={pos_reg1.joints_position.j1}")

# Write Cartesian position to PR[1]
robot.snpx.position_registers.write(1, CartesianPosition(100, 200, 300, 0, 90, 0))

# Write Joint position to PR[1]
joints = JointsPosition()
joints.j1 = 0
joints.j2 = 0
joints.j3 = 0
joints.j4 = 0
joints.j5 = 0
joints.j6 = 45
robot.snpx.position_registers.write(1, joints)

# --- String Registers (SR[]) ---

# Read SR[1]
str_reg1 = robot.snpx.string_registers.read(1)
print(f"SR[1] = '{str_reg1}'")

# Write SR[1]
robot.snpx.string_registers.write(1, "Hello, Robot!")

# --- Flag Registers (F[]) ---

# Read F[1]
flag1 = robot.snpx.flags.read(1)
print(f"F[1] = {flag1}")

# Write F[1]
robot.snpx.flags.write(1, True)
```

## API reference

**NumericRegisters** ([reference](../api/underautomation.fanuc.snpx.internal.md#numericregisters-robotsnpxnumeric_registers))

- `create_batch_assignment(startIndex: int, count: int) -> NumericRegistersBatchAssignment`: Creates a batch assignment for reading multiple numeric registers.
- `write(index: int, value: float) -> None`: Write value at a certain index.
- `read(index: int) -> float`: Reads the value at the specified index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

**PositionRegisters** ([reference](../api/underautomation.fanuc.snpx.internal.md#positionregisters-robotsnpxposition_registers))

- `create_batch_assignment(startIndex: int, count: int) -> PositionRegistersBatchAssignment`: Creates a batch assignment for reading multiple position registers.
- `write(index: int, cartesianPosition_or_extendedCartesianPosition_or_jointsPosition: CartesianPosition | ExtendedCartesianPosition | JointsPosition) -> None`: Writes a Cartesian position to the specified position register. Writes an extended Cartesian position to the specified position register. Writes a joints position to the specified position register.
- `read(index: int) -> Position`: Reads the position at the specified register index.
- `get_or_create_assignment(index: int) -> Assignment1[int]`: Gets or creates an assignment for the specified index.

**Position** ([reference](../api/underautomation.fanuc.common.md#position))

- `Position(userFrame: int, userTool: int, jointsPosition: JointsPosition, cartesianPosition: ExtendedCartesianPosition)`: Constructor with user frame, tool, joints and cartesian position
- `user_frame: int`: User frame index
- `user_tool: int`: User tool index
- `joints_position: JointsPosition`: Joint values in degrees
- `cartesian_position: ExtendedCartesianPosition`: Cartesian position with extended axes

**JointsPosition** ([reference](../api/underautomation.fanuc.common.md#jointsposition-robotstream_motionqueue_end_joint_position))

- `JointsPosition(j1Deg: float, j2Deg: float, j3Deg: float, j4Deg: float, j5Deg: float, j6Deg: float, j7Deg: float, j8Deg: float, j9Deg: float)`: Constructor with 9 joint values in degrees
- `static is_near(j1: 'JointsPosition', j2: 'JointsPosition', degreesTolerance: float) -> bool`: Check if joints position is near to expected joints position with a tolerance value
- `values: typing.List[float] (read only)`: Numeric values for each joints
- `j1: float`: Joint 1 in degrees
- `j2: float`: Joint 2 in degrees
- `j3: float`: Joint 3 in degrees
- `j4: float`: Joint 4 in degrees
- `j5: float`: Joint 5 in degrees
- `j6: float`: Joint 6 in degrees
- `j7: float`: Joint 7 in degrees
- `j8: float`: Joint 8 in degrees
- `j9: float`: Joint 9 in degrees

**ExtendedCartesianPosition** ([reference](../api/underautomation.fanuc.common.md#extendedcartesianposition-robotstream_motionqueue_end_cartesian_position))

- `ExtendedCartesianPosition(x: float, y: float, z: float, w: float, p: float, r: float, e1: float, e2: float, e3: float)`: Constructor with position, rotations, and extended axes
- `e1: float`: Extended axis 1 value
- `e2: float`: Extended axis 2 value
- `e3: float`: Extended axis 3 value
- Inherited from [CartesianPosition](../api/underautomation.fanuc.common.md#cartesianposition-robotstream_motionqueue_end_cartesian_position): `from_homogeneous_matrix`, `normalize_angle`, `normalize_angles`, `is_near`, `configuration`
- Inherited from [XYZWPRPosition](../api/underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position): `to_homogeneous_matrix`, `get_quaternion`, `set_quaternion`, `multiply`, `inverse`, `flange_to_tcp`, `tcp_to_flange`, `user_frame_to_world`, `world_to_user_frame`, `w`, `p`, `r`
- Inherited from [XYZPosition](../api/underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`

**CartesianPosition** ([reference](../api/underautomation.fanuc.common.md#cartesianposition-robotstream_motionqueue_end_cartesian_position))

- `CartesianPosition(x: float, y: float, z: float, w: float, p: float, r: float, configuration: Configuration)`: Constructor with position, rotations and configuration
- `static from_homogeneous_matrix(R: typing.List[float]) -> 'CartesianPosition'`: Create a CartesianPosition with unknow configuration from a homogeneous rotation and translation 4x4 matrix
- `static normalize_angle(angle: float) -> float`: Normalize an angle to the range ]-180, 180]
- `static normalize_angles(pose: 'CartesianPosition') -> None`: Normalize the W, P, R angles to the range ]-180, 180]
- `static is_near(a: 'CartesianPosition', b: 'CartesianPosition', mmTolerance: float, degreesTolerance: float) -> bool`: Check if two Cartesian positions are near each other within specified tolerances
- `configuration: Configuration`: Position configuration
- Inherited from [XYZWPRPosition](../api/underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position): `to_homogeneous_matrix`, `get_quaternion`, `set_quaternion`, `multiply`, `inverse`, `flange_to_tcp`, `tcp_to_flange`, `user_frame_to_world`, `world_to_user_frame`, `w`, `p`, `r`
- Inherited from [XYZPosition](../api/underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`
