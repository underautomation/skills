# Frames & orientations

Convert W, P, R angles to quaternions, interpolate orientations, and change frames between flange, tool, user frame and world frame.

Web page: https://underautomation.com/fanuc/documentation/motion-frames-orientations

FANUC controllers give orientations as W, P, R angles, in degrees: rotation W around X, then P around Y, then R around Z, all around the axes of the reference frame. `XYZWPRPosition` gives conversions to quaternions and the usual frame operations. These functions work offline and can be used with any protocol of the SDK.

![W, P and R: rotations around the X, Y and Z axes of the reference frame.](https://underautomation.com/fanuc/documentation/diagrams/motion-wpr.svg)

## Quaternions

Quaternions are easier than angles to interpolate and to compare orientations.

```csharp
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Motion;
using UnderAutomation.Fanuc.StreamMotion.Data;

public class MotionFramesOrientationsQuaternion
{
    static void Main()
    {

        var position = new XYZWPRPosition(500, 0, 300, 180, 0, 45);

        // W, P, R angles to quaternion, and back
        Quaternion q = position.GetQuaternion();
        position.SetQuaternion(Quaternion.FromAxisAngle(0, 0, 1, 90));   // 90 degrees around Z

        // Interpolation and angle between two orientations
        Quaternion a = new XYZWPRPosition(0, 0, 0, 180, 0, 0).GetQuaternion();
        Quaternion b = new XYZWPRPosition(0, 0, 0, 180, 30, 0).GetQuaternion();
        Quaternion halfWay = Quaternion.Slerp(a, b, 0.5);
        double angle = a.AngleTo(b);                // 30 degrees
        double[] axisAngle = halfWay.ToAxisAngle(); // x, y, z, angle in degrees
    }
}
```

- `GetQuaternion()` and `SetQuaternion()` convert between W, P, R and a quaternion (`Qw`, `Qx`, `Qy`, `Qz`).
- `Quaternion.Slerp()` interpolates on the shortest way between two orientations.
- `AngleTo()` gives the angle between two orientations, in degrees.
- `FromAxisAngle()`, `ToAxisAngle()`, `FromRotationMatrix()` and `ToRotationMatrix()` convert to and from other representations.

## Change of frame

A position is a frame: its X, Y, Z give the origin and its W, P, R the orientation. The same functions work for the positions of the robot, tool frames and user frames.

```csharp
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Motion;
using UnderAutomation.Fanuc.StreamMotion.Data;

public class MotionFramesOrientationsFrames
{
    static void Main()
    {

        var tool = new XYZWPRPosition(0, 0, 150, 0, 0, 0);            // tool frame, relative to the flange
        var userFrame = new XYZWPRPosition(800, -200, 0, 0, 0, 90);    // user frame, relative to the world frame
        var flange = new XYZWPRPosition(700, 0, 400, 180, 0, 0);       // flange in the world frame

        // Flange <-> tool center point
        XYZWPRPosition tcp = flange.FlangeToTcp(tool);
        XYZWPRPosition flangeAgain = tcp.TcpToFlange(tool);

        // World frame <-> user frame
        XYZWPRPosition tcpInUserFrame = tcp.WorldToUserFrame(userFrame);
        XYZWPRPosition tcpInWorld = tcpInUserFrame.UserFrameToWorld(userFrame);

        // General frame operations
        XYZWPRPosition composed = userFrame.Multiply(tcpInUserFrame);   // same as tcpInWorld
        XYZWPRPosition inverse = userFrame.Inverse();
        double[,] matrix = flange.ToHomogeneousMatrix();                // 4 x 4
    }
}
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

**Quaternion** ([reference](../api/UnderAutomation.Fanuc.Common.md#quaternion))

- `Quaternion()`: Creates the identity quaternion (no rotation)
- `Quaternion(double qw, double qx, double qy, double qz)`: Creates a quaternion from its components
- `double AngleTo(Quaternion other)`: Angle of the rotation between the two orientations, in degrees (0 to 180)
- `Quaternion Conjugate()`: Returns the conjugate of this quaternion. For a rotation, it is the inverse rotation.
- `double Dot(Quaternion other)`: Dot product of the two quaternions
- `static Quaternion FromAxisAngle(double x, double y, double z, double angle)`: Creates a rotation around an axis
- `static Quaternion FromRotationMatrix(double[,] matrix)`: Creates a quaternion from a rotation matrix (3x3, or 4x4 homogeneous matrix)
- `Quaternion Multiply(Quaternion other)`: Returns the product this x other: the rotation other applied after the rotation this, in the frame of this.
- `double Norm { get; }`: Norm of the quaternion (1 for a rotation)
- `Quaternion Normalize()`: Returns this quaternion with a norm of 1
- `double Qw { get; set; }`: Scalar part
- `double Qx { get; set; }`: X component of the vector part
- `double Qy { get; set; }`: Y component of the vector part
- `double Qz { get; set; }`: Z component of the vector part
- `static Quaternion Slerp(Quaternion start, Quaternion end, double t)`: Spherical linear interpolation between two orientations, on the shortest way
- `double[] ToAxisAngle()`: Returns the rotation axis and angle: [x, y, z, angle in degrees]. The axis is a unit vector and the angle is between 0 and 180.
- `double[,] ToRotationMatrix()`: Returns the 3x3 rotation matrix of this orientation

**XYZWPRPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition))

- `XYZWPRPosition()`: Default constructor
- `XYZWPRPosition(double x, double y, double z, double w, double p, double r)`: Constructor with position and rotations
- `XYZWPRPosition FlangeToTcp(XYZWPRPosition tool)`: Converts a flange position to the position of the tool center point (TCP)
- `Quaternion GetQuaternion()`: Returns the orientation W, P, R as a quaternion
- `XYZWPRPosition Inverse()`: Returns the inverse of this frame
- `XYZWPRPosition Multiply(XYZWPRPosition other)`: Returns the composition of this frame with another one: the pose other, expressed in this frame, converted to the frame where this position is expressed.
- `double P { get; set; }`: P rotation in degrees (Ry)
- `double R { get; set; }`: R rotation in degrees (Rz)
- `void SetQuaternion(Quaternion quaternion)`: Sets the orientation W, P, R from a quaternion. Angles are between -180 and 180 degrees.
- `XYZWPRPosition TcpToFlange(XYZWPRPosition tool)`: Converts a position of the tool center point (TCP) to the flange position
- `double[,] ToHomogeneousMatrix()`: Convert position to a homogeneous rotation and translation 4x4 matrix
- `XYZWPRPosition UserFrameToWorld(XYZWPRPosition userFrame)`: Converts this position, expressed in a user frame, to the world frame
- `double W { get; set; }`: W rotation in degrees (Rx)
- `XYZWPRPosition WorldToUserFrame(XYZWPRPosition userFrame)`: Converts this position, expressed in the world frame, to a user frame
- Inherited from [XYZPosition](../api/UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`
