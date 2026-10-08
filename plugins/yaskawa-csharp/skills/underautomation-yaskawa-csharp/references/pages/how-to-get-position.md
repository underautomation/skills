# Get the robot position

Read the position of a Yaskawa robot from C# or Python: Cartesian position or joint pulses, which method to choose, and a polling loop. Complete program included.

Web page: https://underautomation.com/yaskawa/documentation/how-to-get-position

This article shows how to read the position of a Yaskawa Motoman robot from a PC, in C# or Python. It gives a complete program that reads the Cartesian position and the joint pulses, then polls the position 10 times per second.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- Nothing else: reading the position works in teach mode and in play mode, without the remote mode.

## Which method to choose

| Need                                       | Method                              | Unit                           |
| ------------------------------------------ | ----------------------------------- | ------------------------------ |
| Where the tool is, to log it or to compute | `GetRobotCartesianPosition()`       | mm and degrees, robot frame    |
| A position to send back with `MoveJoints`  | `GetRobotJointPosition()`           | Encoder pulses per axis        |
| The load of the axes during a move         | `GetTorque()`, `GetPositionError()` | Percent, pulses                |
| A position taught in a job                 | `ReadPositionVariable(n, 1)`        | Raw units of the `P` variable  |
| A second robot, base axes                  | `GetRobotPosition(group)`           | Pulses or raw Cartesian values |

## Example

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class HowToGetPosition
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Tool center point in the robot frame: mm and degrees
        RobotPositionCartesianData tcp = robot.HighSpeedEServer.GetRobotCartesianPosition();
        Console.WriteLine($"X={tcp.X:F3} Y={tcp.Y:F3} Z={tcp.Z:F3} Rx={tcp.Rx:F4} Ry={tcp.Ry:F4} Rz={tcp.Rz:F4}");
        Console.WriteLine($"Tool {tcp.ToolNumber}, posture {tcp.Form}");

        // Joints: encoder pulses, one value per axis
        RobotPositionIntData joints = robot.HighSpeedEServer.GetRobotJointPosition();
        Console.WriteLine("Pulses: " + string.Join(", ", joints.Axes));

        // Poll the position 10 times per second for 5 seconds
        for (int i = 0; i < 50; i++)
        {
            tcp = robot.HighSpeedEServer.GetRobotCartesianPosition();
            Console.WriteLine($"{DateTime.Now:HH:mm:ss.fff} X={tcp.X:F1} Y={tcp.Y:F1} Z={tcp.Z:F1}");
            Thread.Sleep(100);
        }

        robot.Disconnect();
    }
}
```

The program:

1. reads the Cartesian position of the tool, with its tool number and its posture;
2. reads the pulses of each axis;
3. reads the Cartesian position every 100 ms for 5 seconds.

## Polling period

Each read is one request and one answer over the network. On a local network, a request takes a few milliseconds: measure it on your cell before you choose the period. Read only what you need in a loop: the Cartesian position alone is one request, the position and the joints are two.

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) reads the same positions over TCP, and also in a user frame or in the tool frame. It also gives the posture of the arm and the temperature of the encoders.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerPositions
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Joints, in encoder pulses
        HostControlJointPositionData joints = robot.EServer.GetRobotJointPosition();
        Console.WriteLine($"S={joints.S} L={joints.L} U={joints.U} R={joints.R} B={joints.B} T={joints.T}");

        // Cartesian position in the base frame (default), mm and degrees
        HostControlCartesianPositionData tcp = robot.EServer.GetRobotCartesianPosition();
        Console.WriteLine($"X={tcp.X} Y={tcp.Y} Z={tcp.Z} Rx={tcp.Rx} Ry={tcp.Ry} Rz={tcp.Rz}");

        // Posture of the arm and tool of the position
        Console.WriteLine($"Front: {tcp.IsFront}, upper arm: {tcp.IsUpperArm}, flip: {tcp.IsFlip}, tool: {tcp.ToolNumber}");

        // Same position in the robot frame, or in a user frame
        var inRobot = robot.EServer.GetRobotCartesianPosition(HostControlCoordinateSystem.Robot);
        var inUser1 = robot.EServer.GetRobotCartesianPosition(HostControlCoordinateSystem.User1);

        // With the external axes (Re, Axis8...)
        var withExternal = robot.EServer.GetRobotCartesianPosition(HostControlCoordinateSystem.Base, true);

        robot.Disconnect();
    }
}
```

## From joint angles, without the robot

To compute the position of the flange from joint angles in degrees, or every set of joint angles for a position, use the [offline kinematics](kinematics.md). The computation runs on the PC, without a connection.

## Troubleshooting

- **The values are all `0`:** check the control group and the number of axes with [GetConfigurationInformation](hses-system.md#axis_names).
- **The Cartesian position differs from the pendant:** compare the frame and the tool. `DataType` and `ToolNumber` give the ones of the answer.
- **The first call fails after a pause:** a `SocketException` means that the controller did not answer before `DataTimeoutMilliseconds`. Check the network, then call again.

## What to read next

- [Positions](hses-positions.md): the reference of the position methods.
- [Move the robot from a PC](how-to-move-robot.md).
