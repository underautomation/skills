# Current position

Read the current robot position in world coordinates or user frame coordinates, for single or multi-group controllers.

Web page: https://underautomation.com/fanuc/documentation/snpx-position

Read the current robot position in world coordinates or in a specific user frame, for any motion group.

Note: The current position is that of the current tool (UTOOL).

## World current position

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True

# Connect to the robot
robot.connect(parameters)

# Read current world position
world_position = robot.snpx.current_position.read_world_position()

# Access the Cartesian position
x = world_position.cartesian_position.x

# Access the user tool at this position
user_tool = world_position.user_tool

# Access the joint positions
j1 = world_position.joints_position.j1

# Read current world position of group 2
world_position_g2 = robot.snpx.current_position.read_world_position(2)
```

## User frame current position

`ReadUserFramePosition` returns the position relative to a specific user frame. Use user frame 15 to get the currently selected user frame from the pendant.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True

# Connect to the robot
robot.connect(parameters)

# Read user frame 1 position
user_frame = robot.snpx.current_position.read_user_frame_position(1)

# Access the Cartesian position
x = user_frame.cartesian_position.x

# Access the user tool at this position
user_tool = user_frame.user_tool

# Access the user frame id
frame_id = user_frame.user_frame

# Access the joint positions
j1 = user_frame.joints_position.j1

# Read user frame position of group 2
user_frame_g2 = robot.snpx.current_position.read_user_frame_position(1, 2)
```

## Multi-group controllers

For controllers with multiple motion groups (e.g., robot + positioner), specify the group number:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Read world position of group 2
group2_pos = robot.snpx.current_position.read_world_position(2)

# Read user frame position of group 2
group2_frame = robot.snpx.current_position.read_user_frame_position(1, 2)
```

## API reference

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

**XYZPosition** ([reference](../api/underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position))

- `XYZPosition(x: float, y: float, z: float)`: Constructor with X, Y, Z coordinates in millimeters
- `x: float`: X coordinate in millimeters
- `y: float`: Y coordinate in millimeters
- `z: float`: Z coordinate in millimeters
