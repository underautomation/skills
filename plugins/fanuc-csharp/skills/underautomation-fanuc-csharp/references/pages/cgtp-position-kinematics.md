# Position & kinematics

Read current Cartesian and joint positions, and compute forward and inverse kinematics directly on the controller via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-position-kinematics

CGTP can read the current robot position in Cartesian or joint format, and perform forward and inverse kinematics directly on the controller.

## Read current position

Read the live position of the robot (requires firmware **V9.10+**):

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class CgtpPositionKinematicsRead
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read Cartesian position
        CartesianPosition cartesian = robot.Cgtp.ReadCartesianPosition();
        Console.WriteLine($"X={cartesian.X}, Y={cartesian.Y}, Z={cartesian.Z}");
        Console.WriteLine($"W={cartesian.W}, P={cartesian.P}, R={cartesian.R}");

        // Read joint position
        JointsPosition joints = robot.Cgtp.ReadJointPosition();
        Console.WriteLine($"J1={joints.J1}, J2={joints.J2}, J3={joints.J3}");

        // Multi-group
        CartesianPosition group2 = robot.Cgtp.ReadCartesianPosition(groupNum: 2);
        JointsPosition joints2 = robot.Cgtp.ReadJointPosition(groupNum: 2);
    }
}
```

### Multi-group

For controllers with multiple motion groups, specify the group number.

## Record current position into a program

`SetProgramPositionToCurrentCartesianPosition` writes the robot's current Cartesian position to a given position index inside a TP program. The updated position is returned.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class CgtpPositionKinematicsSetToCurrent
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Set position index 1 of "MY_PROG" to the current Cartesian position
        CartesianPosition pos = robot.Cgtp.SetProgramPositionToCurrentCartesianPosition("MY_PROG", 1);
        Console.WriteLine($"Recorded: X={pos.X}, Y={pos.Y}, Z={pos.Z}");
        Console.WriteLine($"           W={pos.W}, P={pos.P}, R={pos.R}");

        // Specify a motion group (default is 1)
        CartesianPosition posGroup2 = robot.Cgtp.SetProgramPositionToCurrentCartesianPosition("MY_PROG", 2, groupNumber: 2);
    }
}
```

## Write a specific position into a program

`SetProgramPosition` writes an arbitrary Cartesian or joint position to a position index (P[n]) inside a TP program. Only the first motion group is supported via CGTP. Requires firmware **V9.10+**.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class CgtpPositionKinematicsSetPosition
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();

        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Cgtp.Enable = true;

        robot.Connect(parameters);

        // Write a Cartesian position to P[1] in "MY_PROG"
        // Only the first motion group is supported via CGTP
        var cartPosition = new Position(
            userFrame: 0,
            userTool: 1,
            jointsPosition: null,
            cartesianPosition: new ExtendedCartesianPosition(500, 200, 300, 0, 90, 0, 0, 0, 0)
        );
        robot.Cgtp.SetProgramPosition("MY_PROG", 1, cartPosition);

        // Write a joint position to P[2] in "MY_PROG"
        var jointPosition = new Position(
            userFrame: 0,
            userTool: 1,
            jointsPosition: new JointsPosition { J1 = 0, J2 = -30, J3 = 45, J4 = 0, J5 = -90, J6 = 0 },
            cartesianPosition: null
        );
        robot.Cgtp.SetProgramPosition("MY_PROG", 2, jointPosition);
    }
}
```

## Online kinematics

Perform forward and inverse kinematics using the controller's own kinematic model. This guarantees the same results as the robot itself.


```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class CgtpPositionKinematicsFK
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Inverse kinematics: Cartesian → Joints
        CartesianPosition target = new CartesianPosition(500, 200, 300, 0, 90, 0);
        JointsPosition joints = robot.Cgtp.InvertKinematics(
            group: 1,
            cartesianPosition: target,
            userTool: 1,
            userFrame: 0
        );

        // Forward kinematics: Joints → Cartesian
        JointsPosition jointPos = new JointsPosition { J1 = 0, J2 = 0, J3 = 0, J4 = 0, J5 = -90, J6 = 0 };
        CartesianPosition cartPos = robot.Cgtp.ForwardKinematics(
            group: 1,
            jointPosition: jointPos,
            userTool: 1,
            userFrame: 0
        );
    }
}
```


## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class CgtpPositionKinematics
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Cgtp.Enable = true;

    robot.Connect(parameters);

    // Read current Cartesian position
    CartesianPosition cartesian = robot.Cgtp.ReadCartesianPosition();
    Console.WriteLine($"X={cartesian.X}, Y={cartesian.Y}, Z={cartesian.Z}");

    // Read current joint position
    JointsPosition joints = robot.Cgtp.ReadJointPosition();
    Console.WriteLine($"J1={joints.J1}, J2={joints.J2}, J3={joints.J3}");

    // Multi-group: read position of group 2
    CartesianPosition group2 = robot.Cgtp.ReadCartesianPosition(groupNum: 2);

    // Inverse kinematics: Cartesian -> Joints
    CartesianPosition target = new CartesianPosition(500, 200, 300, 0, 90, 0);
    JointsPosition ikResult = robot.Cgtp.InvertKinematics(
        group: 1,
        cartesianPosition: target,
        userTool: 1,
        userFrame: 0
    );

    // Forward kinematics: Joints -> Cartesian
    JointsPosition jointTarget = new JointsPosition { J1 = 0, J2 = 0, J3 = 0, J4 = 0, J5 = -90, J6 = 0 };
    CartesianPosition fkResult = robot.Cgtp.ForwardKinematics(
        group: 1,
        jointPosition: jointTarget,
        userTool: 1,
        userFrame: 0
    );

    // Write a position into a TP program (first motion group only)
    var progPosition = new Position(
        userFrame: 0,
        userTool: 1,
        jointsPosition: null,
        cartesianPosition: new ExtendedCartesianPosition(500, 200, 300, 0, 90, 0, 0, 0, 0)
    );
    robot.Cgtp.SetProgramPosition("MY_PROG", 1, progPosition);
  }
}
```

## API reference

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
