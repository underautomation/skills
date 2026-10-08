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

```csharp
using UnderAutomation.UniversalRobots.Common;

class PoseConvert
{
  static void Main(string[] args)
  {
    // X, Y, Z in meters, then a rotation vector RX, RY, RZ in radians
    var pose = new Pose(0.4, -0.1, 0.3, 0, 3.14, 0);

    // Rotation in degrees, computed from RX, RY, RZ
    double rxDegrees = pose.RxDegrees;

    // Same position, rotation as roll, pitch, yaw
    Pose rpy = pose.FromRotationVectorToRPY();

    // And back to a rotation vector
    Pose rotationVector = rpy.FromRPYToRotationVector();

    // 4x4 homogeneous transforms
    double[,] matrix = pose.FromRotationVectorTo4x4Matrix();
    Pose fromMatrix = Pose.From4x4MatrixToRotationVector(matrix);

    // Quaternion
    pose.FromRotationVectorToQuaternion(out double qx, out double qy, out double qz, out double qw);
    Pose fromQuaternion = Pose.FromQuaternionToRotationVector(qx, qy, qz, qw);

    // Text of the form "p[0.4, -0.1, 0.3, 0, 3.14, 0]"
    bool ok = Pose.TryParse("p[0.4, -0.1, 0.3, 0, 3.14, 0]", out Pose parsed);
  }
}
```

In Python, `FromRotationVectorToQuaternion` and `TryParse` are not usable: they have `out` parameters.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Pose** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#pose-robotrtdeoutputdatavaluesactualtcppose))

- `Pose()`: Creates a new pose with all coordinates set to zero.
- `Pose(double x, double y, double z)`: Creates a new pose with the specified translation and zero rotation.
- `Pose(double x, double y, double z, double rx, double ry, double rz)`: Creates a new pose with the specified translation and rotation.
- `Pose(Pose pose)`: Creates a new pose by copying values from another pose.
- `static Pose From4x4MatrixToRPY(double[,] matrixTransform)`: Convert a transformation 4x4 matrix to RPY pose
- `static Pose From4x4MatrixToRotationVector(double[,] matrixTransform)`: Convert a transformation 4x4 matrix to rotation vector
- `static Pose FromQuaternionToRotationVector(double x, double y, double z, double w)`: Converts a quaternion to UR rotation vector
- `double[,] FromRPYTo4x4Matrix()`: Consider this pose as a RPY (Roll-Pitch-Yaw) representation and return a 4x4 homogeneous transformation matrix.
- `Pose FromRPYToRotationVector()`: Consider this pose as RPY And convert it to a new Rotation Vector
- `double[,] FromRotationVectorTo4x4Matrix()`: Consider this pose as a rotation vector and return a 4x4 homogeneous transformation matrix.
- `void FromRotationVectorToQuaternion(out double x, out double y, out double z, out double w)`: Converts a rotation vector to quaternion
- `Pose FromRotationVectorToRPY()`: Consider this pose as a Rotation Vector And convert it to a new RPY position
- `double RxDegrees { get; set; }`: RX rotation in degrees or °/s
- `double RyDegrees { get; set; }`: RY rotation in degrees or °/s
- `double RzDegrees { get; set; }`: RZ rotation in degrees or °/s
- `static bool TryParse(string value, out Pose pose)`: Parse a pose from its string representation
- Inherited from [CartesianCoordinates](../api/UnderAutomation.UniversalRobots.Common.md#cartesiancoordinates-robotrtdeoutputdatavaluesactualtcpforce): `Values`, `X`, `Y`, `Z`, `Rx`, `Ry`, `Rz`

## What to read next

- [Kinematics](kinematics.md): from joint positions to a pose, and back.
- [Get the robot position](how-to-get-position.md).
