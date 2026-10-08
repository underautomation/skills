# Position

Read the current joints and the Cartesian position of a Staubli robot, for the flange or a tool, in the world frame or in another frame.

Web page: https://underautomation.com/staubli/documentation/soap-position

This page shows how to read the current position of a Staubli robot on a CS8 or CS9 controller: the joint values, and the Cartesian position of the flange or of a tool, in the world or in another frame.

## Joints and Cartesian position

`GetCurrentCartesianJointPosition(robot)` returns the joints and the Cartesian position of the flange in the world frame, in one request.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class PositionRead
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Joints and flange position of the first robot, in one request
        CartesianJointPosition position = controller.Soap.GetCurrentCartesianJointPosition(robot: 0);

        // Joint values, in radians
        double[] joints = position.JointsPosition;

        // Flange position in the world frame: X, Y, Z in meters, Rx, Ry, Rz in radians
        CartesianPosition flange = position.CartesianPosition;
        Console.WriteLine($"X={flange.X} Y={flange.Y} Z={flange.Z}");
        Console.WriteLine($"Rx={flange.Rx} Ry={flange.Ry} Rz={flange.Rz}");

        controller.Disconnect();
    }
}
```

| Value                                | Unit    |
| ------------------------------------ | ------- |
| `JointsPosition`, one value per axis | radians |
| `X`, `Y`, `Z`                        | meters  |
| `Rx`, `Ry`, `Rz`                     | radians |

## Joints only

`GetCurrentJointPosition(robot)` returns only the joint values. Use it when you do not need the Cartesian position.

```csharp
using UnderAutomation.Staubli;

public class PositionJoints
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Only the joints, in radians
        double[] joints = controller.Soap.GetCurrentJointPosition(robot: 0);

        for (int i = 0; i < joints.Length; i++)
            Console.WriteLine($"J{i + 1} = {joints[i] * 180 / Math.PI:F2} deg");

        controller.Disconnect();
    }
}
```

## With a tool and a frame

By default, the Cartesian position is the one of the flange, in the world frame. Pass a tool and a frame to get the position of the tool center point in the frame of your part or table.

- `tool`: position of the tool center point, given in the flange frame.
- `frame`: position of the reference frame, given in the world frame.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class PositionTool
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Tool center point, given in the flange frame: 120 mm along Z
        var tool = new CartesianPosition { Z = 0.120 };

        // Reference frame, given in the world frame: a table 500 mm in front of the robot
        var frame = new CartesianPosition { X = 0.500 };

        CartesianJointPosition position = controller.Soap.GetCurrentCartesianJointPosition(robot: 0, tool, frame);

        // Position of the tool center point in the table frame
        CartesianPosition tcp = position.CartesianPosition;

        controller.Disconnect();
    }
}
```

Pass `null` (`None` in Python) for the flange or for the world frame.

## Position of a joint configuration

To get the Cartesian position of joint values that are not the current ones, use the forward kinematics: see [Kinematics](soap-kinematics.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/UnderAutomation.Staubli.Soap.Internal.md#soapclientbase-controllersoap))

- `CartesianJointPosition GetCurrentCartesianJointPosition(int robot = 0, CartesianPosition tool = null, CartesianPosition frame = null)`: Get the Cartesian position and joint positions of a robot
- `double[] GetCurrentJointPosition(int robot = 0)`: Get the current joint position of a robot

**CartesianJointPosition** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#cartesianjointposition))

- `CartesianJointPosition()`
- `CartesianPosition CartesianPosition { get; set; }`: The Cartesian position of the robot end effector.
- `double[] JointsPosition { get; set; }`: The joint positions in radians.

**CartesianPosition** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#cartesianposition))

- `CartesianPosition()`: Initializes a new instance of the Data.CartesianPosition class.
- `double Rx { get; set; }`: Rotation around the X axis (radians).
- `double Ry { get; set; }`: Rotation around the Y axis (radians).
- `double Rz { get; set; }`: Rotation around the Z axis (radians).
- `double X { get; set; }`: X translation component (m).
- `double Y { get; set; }`: Y translation component (m).
- `double Z { get; set; }`: Z translation component (m).
