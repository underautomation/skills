# Current position

Read the current robot position in world coordinates or user frame coordinates, for single or multi-group controllers.

Web page: https://underautomation.com/fanuc/documentation/snpx-position

Read the current robot position in world coordinates or in a specific user frame, for any motion group.

Note: The current position is that of the current tool (UTOOL).

## World current position

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxPositionWorld
{
  static void Main()
  {
    // Create a new Fanuc robot instance
    FanucRobot robot = new FanucRobot();

    // Set connection parameters
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Snpx.Enable = true;

    // Connect to the robot
    robot.Connect(parameters);

    // Read a current world position
    Position worldPosition = robot.Snpx.CurrentPosition.ReadWorldPosition();

    // Access the Cartesian position
    double x = worldPosition.CartesianPosition.X;

    // Access the user tool at this cartesian position
    short usertTool = worldPosition.UserTool;

    // Access the joint positions
    double j1 = worldPosition.JointsPosition.J1;

    // Read a current world position of group 2
    Position worldPositionG2 = robot.Snpx.CurrentPosition.ReadWorldPosition(2);
  }

}
```

## User frame current position

`ReadUserFramePosition` returns the position relative to a specific user frame. Use user frame 15 to get the currently selected user frame from the pendant.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxPositionUserFrame
{
  static void Main()
  {
    // Create a new Fanuc robot instance
    FanucRobot robot = new FanucRobot();

    // Set connection parameters
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Snpx.Enable = true;

    // Connect to the robot
    robot.Connect(parameters);

    // Read user frame 2 position
    Position userFrame = robot.Snpx.CurrentPosition.ReadUserFramePosition(1);

    // Access the Cartesian position
    double x = userFrame.CartesianPosition.X;

    // Access the user tool at this cartesian position
    short usertTool = userFrame.UserTool;

    // Access the user frame id
    short usertFrame = userFrame.UserFrame;

    // Access the joint positions
    double j1 = userFrame.JointsPosition.J1;

    // Read a current world position of group 2
    Position userFrameG2 = robot.Snpx.CurrentPosition.ReadWorldPosition(2);
  }

}
```

## Multi-group controllers

For controllers with multiple motion groups (e.g., robot + positioner), specify the group number:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxPositionMultiGroup
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Read world position of group 2
        Position group2Pos = robot.Snpx.CurrentPosition.ReadWorldPosition(2);

        // Read user frame position of group 2
        Position group2Frame = robot.Snpx.CurrentPosition.ReadUserFramePosition(1, 2);
    }
}
```

## API reference

**Position** ([reference](../api/UnderAutomation.Fanuc.Common.md#position))

- `Position()`: Default constructor
- `Position(short userFrame, short userTool, JointsPosition jointsPosition, ExtendedCartesianPosition cartesianPosition)`: Constructor with user frame, tool, joints and cartesian position
- `ExtendedCartesianPosition CartesianPosition { get; set; }`: Cartesian position with extended axes
- `JointsPosition JointsPosition { get; set; }`: Joint values in degrees
- `short UserFrame { get; set; }`: User frame index
- `short UserTool { get; set; }`: User tool index

**JointsPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#jointsposition-robotstreammotionqueueendjointposition))

- `JointsPosition()`: Default constructor
- `JointsPosition(double j1Deg, double j2Deg, double j3Deg, double j4Deg, double j5Deg, double j6Deg)`: Constructor with 6 joint values in degrees
- `JointsPosition(double j1Deg, double j2Deg, double j3Deg, double j4Deg, double j5Deg, double j6Deg, double j7Deg, double j8Deg, double j9Deg)`: Constructor with 9 joint values in degrees
- `JointsPosition(double[] values)`: Constructor from an array of joint values in degrees
- `static bool IsNear(JointsPosition j1, JointsPosition j2, double degreesTolerance)`: Check if joints position is near to expected joints position with a tolerance value
- `double this[int i] { get; set; }`: Gets or sets the joint value at the specified index
- `double J1 { get; set; }`: Joint 1 in degrees
- `double J2 { get; set; }`: Joint 2 in degrees
- `double J3 { get; set; }`: Joint 3 in degrees
- `double J4 { get; set; }`: Joint 4 in degrees
- `double J5 { get; set; }`: Joint 5 in degrees
- `double J6 { get; set; }`: Joint 6 in degrees
- `double J7 { get; set; }`: Joint 7 in degrees
- `double J8 { get; set; }`: Joint 8 in degrees
- `double J9 { get; set; }`: Joint 9 in degrees
- `double[] Values { get; }`: Numeric values for each joints

**ExtendedCartesianPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#extendedcartesianposition-robotstreammotionqueueendcartesianposition))

- `ExtendedCartesianPosition()`: Default constructor
- `ExtendedCartesianPosition(double x, double y, double z, double w, double p, double r, double e1, double e2, double e3)`: Constructor with position, rotations, and extended axes
- `double E1 { get; set; }`: Extended axis 1 value
- `double E2 { get; set; }`: Extended axis 2 value
- `double E3 { get; set; }`: Extended axis 3 value
- Inherited from [CartesianPosition](../api/UnderAutomation.Fanuc.Common.md#cartesianposition-robotstreammotionqueueendcartesianposition): `FromHomogeneousMatrix`, `NormalizeAngle`, `NormalizeAngles`, `IsNear`, `Configuration`
- Inherited from [XYZWPRPosition](../api/UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](../api/UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`

**CartesianPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#cartesianposition-robotstreammotionqueueendcartesianposition))

- `CartesianPosition()`: Default constructor
- `CartesianPosition(double x, double y, double z, double w, double p, double r)`: Constructor with position and rotations
- `CartesianPosition(double x, double y, double z, double w, double p, double r, Configuration configuration)`: Constructor with position, rotations and configuration
- `CartesianPosition(CartesianPosition position)`: Copy constructor
- `CartesianPosition(XYZPosition position, double w, double p, double r)`: Constructor from an XYZ position with rotations
- `Configuration Configuration { get; set; }`: Position configuration
- `static CartesianPosition FromHomogeneousMatrix(double[,] R)`: Create a CartesianPosition with unknow configuration from a homogeneous rotation and translation 4x4 matrix
- `static bool IsNear(CartesianPosition a, CartesianPosition b, double mmTolerance, double degreesTolerance)`: Check if two Cartesian positions are near each other within specified tolerances
- `static double NormalizeAngle(double angle)`: Normalize an angle to the range ]-180, 180]
- `static void NormalizeAngles(CartesianPosition pose)`: Normalize the W, P, R angles to the range ]-180, 180]
- Inherited from [XYZWPRPosition](../api/UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](../api/UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`

**XYZPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition))

- `XYZPosition()`: Default constructor
- `XYZPosition(double x, double y, double z)`: Constructor with X, Y, Z coordinates in millimeters
- `double X { get; set; }`: X coordinate in millimeters
- `double Y { get; set; }`: Y coordinate in millimeters
- `double Z { get; set; }`: Z coordinate in millimeters
