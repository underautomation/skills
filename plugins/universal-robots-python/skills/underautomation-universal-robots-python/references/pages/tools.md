# Convert position types

Convert the orientation of a UR pose between rotation vector, roll pitch yaw, 4x4 transform and quaternion with the Pose class.

Web page: https://underautomation.com/universal-robots/documentation/tools

The class `Pose` holds a Cartesian position of a Universal Robots cobot, and converts its orientation between the formats used by robots and vision systems. This page lists the conversions. They run on the PC, without a robot.

## The Pose class

A `Pose` has 6 values, as in URScript: X, Y, Z in meters, then RX, RY, RZ, a rotation vector in radians. `RxDegrees`, `RyDegrees` and `RzDegrees` give the rotation in degrees: they are computed from RX, RY, RZ, not stored.

The SDK returns a `Pose` for the positions of the robot (RTDE `ActualTcpPose`, Primary Interface `CartesianInfo.AsPose()`), and accepts one as the answer of an XML-RPC call.

## Conversions

| From                    | To                      | Method                                          |
| ----------------------- | ----------------------- | ----------------------------------------------- |
| Rotation vector         | Roll, pitch, yaw        | `FromRotationVectorToRPY()`                     |
| Roll, pitch, yaw        | Rotation vector         | `FromRPYToRotationVector()`                     |
| Rotation vector         | 4x4 transform           | `FromRotationVectorTo4x4Matrix()`               |
| Roll, pitch, yaw        | 4x4 transform           | `FromRPYTo4x4Matrix()`                          |
| 4x4 transform           | Rotation vector         | `Pose.From4x4MatrixToRotationVector(matrix)`    |
| 4x4 transform           | Roll, pitch, yaw        | `Pose.From4x4MatrixToRPY(matrix)`               |
| Rotation vector         | Quaternion              | `FromRotationVectorToQuaternion(out x, out y, out z, out w)` |
| Quaternion              | Rotation vector         | `Pose.FromQuaternionToRotationVector(x, y, z, w)` |
| Text `p[x, y, z, rx, ry, rz]` | Pose              | `Pose.TryParse(text, out pose)`                 |

The roll, pitch and yaw are stored in RX, RY and RZ of the returned `Pose`. The X, Y, Z do not change.

```python
from underautomation.universal_robots.common.pose import Pose

# X, Y, Z in meters, then a rotation vector RX, RY, RZ in radians
pose = Pose(0.4, -0.1, 0.3, 0, 3.14, 0)

# Rotation in degrees, computed from RX, RY, RZ
rx_degrees = pose.rx_degrees

# Same position, rotation as roll, pitch, yaw
rpy = pose.from_rotation_vector_to_rpy()

# And back to a rotation vector
rotation_vector = rpy.from_rpy_to_rotation_vector()

# 4x4 homogeneous transforms
matrix = pose.from_rotation_vector_to4x4_matrix()
from_matrix = Pose.from4x4_matrix_to_rotation_vector(matrix)

# Quaternion to rotation vector
from_quaternion = Pose.from_quaternion_to_rotation_vector(0, 1, 0, 0)
```

In Python, `FromRotationVectorToQuaternion` and `TryParse` are not usable: they have `out` parameters.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Pose** ([reference](../api/underautomation.universal_robots.common.md#pose-robotrtdeoutput_data_valuesactual_tcp_pose))

- `Pose(x: float, y: float, z: float, rx: float, ry: float, rz: float)`: Creates a new pose with the specified translation and rotation.
- `from_rotation_vector_to_rpy() -> 'Pose'`: Consider this pose as a Rotation Vector And convert it to a new RPY position
- `from_rpy_to_rotation_vector() -> 'Pose'`: Consider this pose as RPY And convert it to a new Rotation Vector
- `static try_parse(value: str, pose: 'Pose') -> bool`: Parse a pose from its string representation
- `from_rotation_vector_to_quaternion(x: float, y: float, z: float, w: float) -> None`: Converts a rotation vector to quaternion
- `from_rpy_to4x4_matrix() -> typing.List[float]`: Consider this pose as a RPY (Roll-Pitch-Yaw) representation and return a 4x4 homogeneous transformation matrix.
- `from_rotation_vector_to4x4_matrix() -> typing.List[float]`: Consider this pose as a rotation vector and return a 4x4 homogeneous transformation matrix.
- `static from_quaternion_to_rotation_vector(x: float, y: float, z: float, w: float) -> 'Pose'`: Converts a quaternion to UR rotation vector
- `static from4x4_matrix_to_rotation_vector(matrixTransform: typing.List[float]) -> 'Pose'`: Convert a transformation 4x4 matrix to rotation vector
- `static from4x4_matrix_to_rpy(matrixTransform: typing.List[float]) -> 'Pose'`: Convert a transformation 4x4 matrix to RPY pose
- `rx_degrees: float`: RX rotation in degrees or °/s
- `ry_degrees: float`: RY rotation in degrees or °/s
- `rz_degrees: float`: RZ rotation in degrees or °/s
- Inherited from [CartesianCoordinates](../api/underautomation.universal_robots.common.md#cartesiancoordinates-robotrtdeoutput_data_valuesactual_tcp_force): `values`, `x`, `y`, `z`, `rx`, `ry`, `rz`

## What to read next

- [Kinematics](kinematics.md): from joint positions to a pose, and back.
- [Get the robot position](how-to-get-position.md).
