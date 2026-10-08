# UnderAutomation.Robotics.Geometry

## CartesianPose

`class CartesianPose`

Cartesian pose: position X, Y, Z in mm, orientation, and optional values of external axes (mm or degrees). It can describe a position of the robot or a frame.

- `CartesianPose()`: Creates a pose at the origin, without rotation and without external axes
- `CartesianPose(double x, double y, double z, Orientation orientation)`: Creates a pose from a position and an orientation, without external axes
- `double[] ExternalAxes { get; set; }`: Values of the external axes, in mm or degrees. Empty when the pose has no external axes. Setting null gives an empty array.
- `static CartesianPose FromEuler(double x, double y, double z, double a, double b, double c, EulerConvention convention)`: Creates a pose from a position and three Euler angles, without external axes
- `CartesianPose Inverse()`: Returns the inverse of this frame. The result has no external axes.
- `CartesianPose Multiply(CartesianPose other)`: Returns the composition of this frame with another pose: the pose other, expressed in this frame, converted to the frame where this pose is expressed. The external axes of the result are the ones of other.
- `Orientation Orientation { get; set; }`: Orientation. Setting null gives the identity orientation.
- `double X { get; set; }`: X in mm
- `double Y { get; set; }`: Y in mm
- `double Z { get; set; }`: Z in mm

## EulerConvention

`enum EulerConvention`

Convention of three Euler angles (a, b, c) that describe an orientation. Angles are in degrees.

- FixedXYZ: Rotation a around the fixed X axis, then b around the fixed Y axis, then c around the fixed Z axis: R = Rz(c) * Ry(b) * Rx(a).
- MobileXYZ: Rotation a around X, then b around the new Y axis, then c around the new Z axis: R = Rx(a) * Ry(b) * Rz(c).
- MobileZYX: Rotation a around Z, then b around the new Y axis, then c around the new X axis: R = Rz(a) * Ry(b) * Rx(c). It is the same orientation as EulerConvention.FixedXYZ with the angles in reverse order.
- MobileZYZ: Rotation a around Z, then b around the new Y axis, then c around the new Z axis: R = Rz(a) * Ry(b) * Rz(c).

## JointValues

`class JointValues`

Position of the axes of a robot: one value per axis, in degrees for rotary axes and in mm for linear axes

- `JointValues(params double[] values)`: Creates a joint position from the values of the axes. The array is copied.
- `int Count { get; }`: Number of axes
- `double[] Values { get; }`: Value of each axis, in degrees or mm

## Orientation

`sealed class Orientation`

Orientation in space, stored as a unit quaternion (Qw + Qx.i + Qy.j + Qz.k). It can be created from and converted to Euler angles, a rotation vector, an axis and an angle, or a rotation matrix.

- `Orientation()`: Creates the identity orientation (no rotation)
- `double AngleTo(Orientation other)`: Angle of the rotation between the two orientations, in degrees (0 to 180)
- `static Orientation FromAxisAngle(double x, double y, double z, double angle)`: Creates a rotation around an axis
- `static Orientation FromEuler(double a, double b, double c, EulerConvention convention)`: Creates an orientation from three Euler angles
- `static Orientation FromQuaternion(double qw, double qx, double qy, double qz)`: Creates an orientation from a quaternion. The quaternion is normalized.
- `static Orientation FromRotationMatrix(double[,] matrix)`: Creates an orientation from a rotation matrix (3x3, or 4x4 homogeneous matrix)
- `static Orientation FromRotationVector(double x, double y, double z)`: Creates an orientation from a rotation vector: its direction is the rotation axis and its norm is the angle in degrees
- `Orientation Inverse()`: Returns the inverse rotation
- `Orientation Multiply(Orientation other)`: Returns the composition this x other: the orientation other, expressed in the frame of this orientation, converted to the reference frame
- `double Qw { get; }`: Scalar part of the unit quaternion
- `double Qx { get; }`: X component of the vector part of the unit quaternion
- `double Qy { get; }`: Y component of the vector part of the unit quaternion
- `double Qz { get; }`: Z component of the vector part of the unit quaternion
- `static Orientation Slerp(Orientation start, Orientation end, double t)`: Spherical linear interpolation between two orientations, on the shortest way
- `double[] ToAxisAngle()`: Returns the rotation axis and angle: [x, y, z, angle in degrees]. The axis is a unit vector and the angle is between 0 and 180.
- `double[] ToEuler(EulerConvention convention)`: Returns the three Euler angles [a, b, c] of this orientation, in degrees. For EulerConvention.MobileZYZ, b is between 0 and 180. For the other conventions, b is between -90 and 90. When the orientation is singular (b = 0 or 180 for ZYZ, b = -90 or 90 for the others), only a combination of a and c...
- `double[,] ToRotationMatrix()`: Returns the 3x3 rotation matrix of this orientation
- `double[] ToRotationVector()`: Returns the rotation vector [x, y, z] of this orientation: its direction is the rotation axis and its norm is the angle in degrees (0 to 180)
