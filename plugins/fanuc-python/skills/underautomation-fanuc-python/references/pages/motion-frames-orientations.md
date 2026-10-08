# Frames & orientations

Convert W, P, R angles to quaternions, interpolate orientations, and change frames between flange, tool, user frame and world frame.

Web page: https://underautomation.com/fanuc/documentation/motion-frames-orientations

FANUC controllers give orientations as W, P, R angles, in degrees: rotation W around X, then P around Y, then R around Z, all around the axes of the reference frame. `XYZWPRPosition` gives conversions to quaternions and the usual frame operations. These functions work offline and can be used with any protocol of the SDK.

![W, P and R: rotations around the X, Y and Z axes of the reference frame.](https://underautomation.com/fanuc/documentation/diagrams/motion-wpr.svg)

## Quaternions

Quaternions are easier than angles to interpolate and to compare orientations.

```python
from underautomation.fanuc.common.quaternion import Quaternion
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition

position = XYZWPRPosition(500, 0, 300, 180, 0, 45)

# W, P, R angles to quaternion, and back
q = position.get_quaternion()
position.set_quaternion(Quaternion.from_axis_angle(0, 0, 1, 90))   # 90 degrees around Z

# Interpolation and angle between two orientations
a = XYZWPRPosition(0, 0, 0, 180, 0, 0).get_quaternion()
b = XYZWPRPosition(0, 0, 0, 180, 30, 0).get_quaternion()
half_way = Quaternion.slerp(a, b, 0.5)
angle = a.angle_to(b)                # 30 degrees
axis_angle = half_way.to_axis_angle()  # x, y, z, angle in degrees
```

- `GetQuaternion()` and `SetQuaternion()` convert between W, P, R and a quaternion (`Qw`, `Qx`, `Qy`, `Qz`).
- `Quaternion.Slerp()` interpolates on the shortest way between two orientations.
- `AngleTo()` gives the angle between two orientations, in degrees.
- `FromAxisAngle()`, `ToAxisAngle()`, `FromRotationMatrix()` and `ToRotationMatrix()` convert to and from other representations.

## Change of frame

A position is a frame: its X, Y, Z give the origin and its W, P, R the orientation. The same functions work for the positions of the robot, tool frames and user frames.

```python
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition

tool = XYZWPRPosition(0, 0, 150, 0, 0, 0)            # tool frame, relative to the flange
user_frame = XYZWPRPosition(800, -200, 0, 0, 0, 90)  # user frame, relative to the world frame
flange = XYZWPRPosition(700, 0, 400, 180, 0, 0)      # flange in the world frame

# Flange <-> tool center point
tcp = flange.flange_to_tcp(tool)
flange_again = tcp.tcp_to_flange(tool)

# World frame <-> user frame
tcp_in_user_frame = tcp.world_to_user_frame(user_frame)
tcp_in_world = tcp_in_user_frame.user_frame_to_world(user_frame)

# General frame operations
composed = user_frame.multiply(tcp_in_user_frame)   # same as tcp_in_world
inverse = user_frame.inverse()
matrix = flange.to_homogeneous_matrix()             # 4 x 4
```

![World frame, user frame, flange and tool center point (TCP).](https://underautomation.com/fanuc/documentation/diagrams/motion-frames.svg)

| Need | Method |
| --- | --- |
| Position of the tool center point from the flange position | `flange.FlangeToTcp(tool)` |
| Flange position from the tool center point | `tcp.TcpToFlange(tool)` |
| Position in the world frame from a position in a user frame | `position.UserFrameToWorld(userFrame)` |
| Position in a user frame from a position in the world frame | `position.WorldToUserFrame(userFrame)` |
| Composition of two frames (A x B) | `a.Multiply(b)` |
| Inverse frame | `frame.Inverse()` |
| 4 x 4 homogeneous matrix | `position.ToHomogeneousMatrix()` |

The motion planner does these conversions for you when `ToolFrame` and `UserFrame` are set (see [Joint & Cartesian motions](motion-moves.md#tool_and_user_frames)).

## API reference

**Quaternion** ([reference](../api/underautomation.fanuc.common.md#quaternion))

- `Quaternion(qw: float, qx: float, qy: float, qz: float)`: Creates a quaternion from its components
- `normalize() -> 'Quaternion'`: Returns this quaternion with a norm of 1
- `conjugate() -> 'Quaternion'`: Returns the conjugate of this quaternion. For a rotation, it is the inverse rotation.
- `multiply(other: 'Quaternion') -> 'Quaternion'`: Returns the product this x other: the rotation other applied after the rotation this, in the frame of this.
- `dot(other: 'Quaternion') -> float`: Dot product of the two quaternions
- `angle_to(other: 'Quaternion') -> float`: Angle of the rotation between the two orientations, in degrees (0 to 180)
- `static slerp(start: 'Quaternion', end: 'Quaternion', t: float) -> 'Quaternion'`: Spherical linear interpolation between two orientations, on the shortest way
- `static from_axis_angle(x: float, y: float, z: float, angle: float) -> 'Quaternion'`: Creates a rotation around an axis
- `to_axis_angle() -> typing.List[float]`: Returns the rotation axis and angle: [x, y, z, angle in degrees]. The axis is a unit vector and the angle is between 0 and 180.
- `static from_rotation_matrix(matrix: typing.List[float]) -> 'Quaternion'`: Creates a quaternion from a rotation matrix (3x3, or 4x4 homogeneous matrix)
- `to_rotation_matrix() -> typing.List[float]`: Returns the 3x3 rotation matrix of this orientation
- `qw: float`: Scalar part
- `qx: float`: X component of the vector part
- `qy: float`: Y component of the vector part
- `qz: float`: Z component of the vector part
- `norm: float (read only)`: Norm of the quaternion (1 for a rotation)

**XYZWPRPosition** ([reference](../api/underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position))

- `XYZWPRPosition(x: float, y: float, z: float, w: float, p: float, r: float)`: Constructor with position and rotations
- `to_homogeneous_matrix() -> typing.List[float]`: Convert position to a homogeneous rotation and translation 4x4 matrix
- `get_quaternion() -> Quaternion`: Returns the orientation W, P, R as a quaternion
- `set_quaternion(quaternion: Quaternion) -> None`: Sets the orientation W, P, R from a quaternion. Angles are between -180 and 180 degrees.
- `multiply(other: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Returns the composition of this frame with another one: the pose other, expressed in this frame, converted to the frame where this position is expressed.
- `inverse() -> 'XYZWPRPosition'`: Returns the inverse of this frame
- `flange_to_tcp(tool: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Converts a flange position to the position of the tool center point (TCP)
- `tcp_to_flange(tool: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Converts a position of the tool center point (TCP) to the flange position
- `user_frame_to_world(userFrame: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Converts this position, expressed in a user frame, to the world frame
- `world_to_user_frame(userFrame: 'XYZWPRPosition') -> 'XYZWPRPosition'`: Converts this position, expressed in the world frame, to a user frame
- `w: float`: W rotation in degrees (Rx)
- `p: float`: P rotation in degrees (Ry)
- `r: float`: R rotation in degrees (Rz)
- Inherited from [XYZPosition](../api/underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`
