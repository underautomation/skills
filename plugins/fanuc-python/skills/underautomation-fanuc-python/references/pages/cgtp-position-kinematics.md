# Position & kinematics

Read current Cartesian and joint positions, and compute forward and inverse kinematics directly on the controller via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-position-kinematics

CGTP can read the current robot position in Cartesian or joint format, and perform forward and inverse kinematics directly on the controller.

## Read current position

Read the live position of the robot (requires firmware **V9.10+**):

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read Cartesian position
cartesian = robot.cgtp.read_cartesian_position()
print(f"X={cartesian.x}, Y={cartesian.y}, Z={cartesian.z}")
print(f"W={cartesian.w}, P={cartesian.p}, R={cartesian.r}")

# Read joint position
joints = robot.cgtp.read_joint_position()
print(f"J1={joints.j1}, J2={joints.j2}, J3={joints.j3}")

# Multi-group
group2 = robot.cgtp.read_cartesian_position(group_num=2)
joints2 = robot.cgtp.read_joint_position(group_num=2)
```

### Multi-group

For controllers with multiple motion groups, specify the group number.

## Record current position into a program

`SetProgramPositionToCurrentCartesianPosition` writes the robot's current Cartesian position to a given position index inside a TP program. The updated position is returned.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Set position index 1 of "MY_PROG" to the current Cartesian position
pos = robot.cgtp.set_program_position_to_current_cartesian_position("MY_PROG", 1)
print(f"Recorded: X={pos.x}, Y={pos.y}, Z={pos.z}")
print(f"           W={pos.w}, P={pos.p}, R={pos.r}")

# Specify a motion group (default is 1)
pos_group2 = robot.cgtp.set_program_position_to_current_cartesian_position("MY_PROG", 2, group_number=2)
```

## Write a specific position into a program

`SetProgramPosition` writes an arbitrary Cartesian or joint position to a position index (P[n]) inside a TP program. Only the first motion group is supported via CGTP. Requires firmware **V9.10+**.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.position import Position
from underautomation.fanuc.common.extended_cartesian_position import ExtendedCartesianPosition
from underautomation.fanuc.common.joints_position import JointsPosition

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.cgtp.enable = True
robot.connect(parameters)

# Write a Cartesian position to P[1] in "MY_PROG"
# Only the first motion group is supported via CGTP
cart_position = Position(0, 1, None, ExtendedCartesianPosition(500, 200, 300, 0, 90, 0, 0, 0, 0))
robot.cgtp.set_program_position("MY_PROG", 1, cart_position)

# Write a joint position to P[2] in "MY_PROG"
joint_position = Position(0, 1, JointsPosition(j1=0, j2=-30, j3=45, j4=0, j5=-90, j6=0), None)
robot.cgtp.set_program_position("MY_PROG", 2, joint_position)
```

## Online kinematics

Perform forward and inverse kinematics using the controller's own kinematic model. This guarantees the same results as the robot itself.


```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.common.cartesian_position import CartesianPosition
from underautomation.fanuc.common.joints_position import JointsPosition

robot = FanucRobot()
robot.connect("192.168.0.1")

# Inverse kinematics: Cartesian → Joints
target = CartesianPosition(500, 200, 300, 0, 90, 0)
joints = robot.cgtp.invert_kinematics(
    group=1,
    cartesian_position=target,
    user_tool=1,
    user_frame=0
)

# Forward kinematics: Joints → Cartesian
joint_pos = JointsPosition(j1=0, j2=0, j3=0, j4=0, j5=-90, j6=0)
cart_pos = robot.cgtp.forward_kinematics(
    group=1,
    joint_position=joint_pos,
    user_tool=1,
    user_frame=0
)
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
parameters.cgtp.enable = True

# Connect to the robot
robot.connect(parameters)

# Read current Cartesian position
cartesian = robot.cgtp.read_cartesian_position()
print(f"X={cartesian.x}, Y={cartesian.y}, Z={cartesian.z}")

# Read current joint position
joints = robot.cgtp.read_joint_position()
print(f"J1={joints.j1}, J2={joints.j2}, J3={joints.j3}")

# Multi-group: read position of group 2
group2 = robot.cgtp.read_cartesian_position(group_num=2)

# Inverse kinematics: Cartesian -> Joints
target = CartesianPosition(500, 200, 300, 0, 90, 0)
ik_result = robot.cgtp.invert_kinematics(
    group=1,
    cartesian_position=target,
    user_tool=1,
    user_frame=0
)

# Forward kinematics: Joints -> Cartesian
joint_target = JointsPosition(j1=0, j2=0, j3=0, j4=0, j5=-90, j6=0)
fk_result = robot.cgtp.forward_kinematics(
    group=1,
    joint_position=joint_target,
    user_tool=1,
    user_frame=0
)

# Write a position into a TP program (first motion group only)
from underautomation.fanuc.common.position import Position
from underautomation.fanuc.common.extended_cartesian_position import ExtendedCartesianPosition
prog_position = Position(0, 1, None, ExtendedCartesianPosition(500, 200, 300, 0, 90, 0, 0, 0, 0))
robot.cgtp.set_program_position("MY_PROG", 1, prog_position)
```

## API reference

**CartesianPosition** ([reference](../api/underautomation.fanuc.common.md#cartesianposition-robotstream_motionqueue_end_cartesian_position))

- `CartesianPosition(x: float, y: float, z: float, w: float, p: float, r: float, configuration: Configuration)`: Constructor with position, rotations and configuration
- `static from_homogeneous_matrix(R: typing.List[float]) -> 'CartesianPosition'`: Create a CartesianPosition with unknow configuration from a homogeneous rotation and translation 4x4 matrix
- `static normalize_angle(angle: float) -> float`: Normalize an angle to the range ]-180, 180]
- `static normalize_angles(pose: 'CartesianPosition') -> None`: Normalize the W, P, R angles to the range ]-180, 180]
- `static is_near(a: 'CartesianPosition', b: 'CartesianPosition', mmTolerance: float, degreesTolerance: float) -> bool`: Check if two Cartesian positions are near each other within specified tolerances
- `configuration: Configuration`: Position configuration
- Inherited from [XYZWPRPosition](../api/underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position): `to_homogeneous_matrix`, `get_quaternion`, `set_quaternion`, `multiply`, `inverse`, `flange_to_tcp`, `tcp_to_flange`, `user_frame_to_world`, `world_to_user_frame`, `w`, `p`, `r`
- Inherited from [XYZPosition](../api/underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`

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
