# underautomation.robotics.geometry

## CartesianPose

`from underautomation.robotics.geometry.cartesian_pose import CartesianPose`

Cartesian pose: position X, Y, Z in mm, orientation, and optional values of external axes (mm or degrees). It can describe a position of the robot or a frame.

- `CartesianPose(x: float, y: float, z: float, orientation: Orientation)`: Creates a pose from a position and an orientation, without external axes
- `static from_euler(x: float, y: float, z: float, a: float, b: float, c: float, convention: EulerConvention) -> 'CartesianPose'`: Creates a pose from a position and three Euler angles, without external axes
- `multiply(other: 'CartesianPose') -> 'CartesianPose'`: Returns the composition of this frame with another pose: the pose other, expressed in this frame, converted to the frame where this pose is expressed. The external axes of the result are the ones of other.
- `inverse() -> 'CartesianPose'`: Returns the inverse of this frame. The result has no external axes.
- `x: float`: X in mm
- `y: float`: Y in mm
- `z: float`: Z in mm
- `orientation: Orientation`: Orientation. Setting null gives the identity orientation.
- `external_axes: typing.List[float]`: Values of the external axes, in mm or degrees. Empty when the pose has no external axes. Setting null gives an empty array.

## EulerConvention

`from underautomation.robotics.geometry.euler_convention import EulerConvention`

Convention of three Euler angles (a, b, c) that describe an orientation. Angles are in degrees.

- FixedXYZ: Rotation a around the fixed X axis, then b around the fixed Y axis, then c around the fixed Z axis: R = Rz(c) * Ry(b) * Rx(a).
- MobileXYZ: Rotation a around X, then b around the new Y axis, then c around the new Z axis: R = Rx(a) * Ry(b) * Rz(c).
- MobileZYX: Rotation a around Z, then b around the new Y axis, then c around the new X axis: R = Rz(a) * Ry(b) * Rx(c). It is the same orientation as FixedXYZ with the angles in reverse order.
- MobileZYZ: Rotation a around Z, then b around the new Y axis, then c around the new Z axis: R = Rz(a) * Ry(b) * Rz(c).

## JointValues

`from underautomation.robotics.geometry.joint_values import JointValues`

Position of the axes of a robot: one value per axis, in degrees for rotary axes and in mm for linear axes

- `JointValues(values: typing.List[float])`: Creates a joint position from the values of the axes. The array is copied.
- `values: typing.List[float] (read only)`: Value of each axis, in degrees or mm
- `count: int (read only)`: Number of axes

## Orientation

`from underautomation.robotics.geometry.orientation import Orientation`

Orientation in space, stored as a unit quaternion (Qw + Qx.i + Qy.j + Qz.k). It can be created from and converted to Euler angles, a rotation vector, an axis and an angle, or a rotation matrix.

- `Orientation()`: Creates the identity orientation (no rotation)
- `static from_quaternion(qw: float, qx: float, qy: float, qz: float) -> 'Orientation'`: Creates an orientation from a quaternion. The quaternion is normalized.
- `static from_euler(a: float, b: float, c: float, convention: EulerConvention) -> 'Orientation'`: Creates an orientation from three Euler angles
- `to_euler(convention: EulerConvention) -> typing.List[float]`: Returns the three Euler angles [a, b, c] of this orientation, in degrees. For MobileZYZ, b is between 0 and 180. For the other conventions, b is between -90 and 90. When the orientation is singular (b = 0 or 180 for ZYZ, b = -90 or 90 for the others), only a combination of a and c is defined: a i...
- `static from_axis_angle(x: float, y: float, z: float, angle: float) -> 'Orientation'`: Creates a rotation around an axis
- `to_axis_angle() -> typing.List[float]`: Returns the rotation axis and angle: [x, y, z, angle in degrees]. The axis is a unit vector and the angle is between 0 and 180.
- `static from_rotation_vector(x: float, y: float, z: float) -> 'Orientation'`: Creates an orientation from a rotation vector: its direction is the rotation axis and its norm is the angle in degrees
- `to_rotation_vector() -> typing.List[float]`: Returns the rotation vector [x, y, z] of this orientation: its direction is the rotation axis and its norm is the angle in degrees (0 to 180)
- `static from_rotation_matrix(matrix: typing.List[float]) -> 'Orientation'`: Creates an orientation from a rotation matrix (3x3, or 4x4 homogeneous matrix)
- `to_rotation_matrix() -> typing.List[float]`: Returns the 3x3 rotation matrix of this orientation
- `multiply(other: 'Orientation') -> 'Orientation'`: Returns the composition this x other: the orientation other, expressed in the frame of this orientation, converted to the reference frame
- `inverse() -> 'Orientation'`: Returns the inverse rotation
- `angle_to(other: 'Orientation') -> float`: Angle of the rotation between the two orientations, in degrees (0 to 180)
- `static slerp(start: 'Orientation', end: 'Orientation', t: float) -> 'Orientation'`: Spherical linear interpolation between two orientations, on the shortest way
- `qw: float (read only)`: Scalar part of the unit quaternion
- `qx: float (read only)`: X component of the vector part of the unit quaternion
- `qy: float (read only)`: Y component of the vector part of the unit quaternion
- `qz: float (read only)`: Z component of the vector part of the unit quaternion
