# Get the robot position

Read the joint positions and the TCP position of a UR cobot in C# or Python, with RTDE up to 500 Hz or with the Primary Interface.

Web page: https://underautomation.com/universal-robots/documentation/how-to-get-position

This article shows how to read the current position of a Universal Robots cobot from a PC, in C# or Python: the 6 joint positions and the position of the tool center point (TCP). It compares the interfaces that give it and shows a complete program.

## Which way to choose

| Way                | Frequency          | Joint positions             | TCP position                       | When                                       |
| ------------------ | ------------------ | --------------------------- | ---------------------------------- | ------------------------------------------ |
| RTDE               | Up to 500 Hz       | `ActualQ`                   | `ActualTcpPose`                    | Fast monitoring, logging, closed loop      |
| Primary Interface  | 10 Hz              | `JointData.Base.Position`...| `CartesianInfo.AsPose()`           | Display, no setup, enabled by default      |
| Forward kinematics | No robot           | Your values                 | `KinematicsUtils.ForwardKinematics`| Offline computation, simulation            |

RTDE also gives the target positions (`TargetQ`, `TargetTcpPose`), the speeds and the forces. The Primary Interface also gives the TCP offset of the active tool (`CartesianInfo.TCPOffsetX`...).

## Units

| Value                  | Unit                                                        |
| ---------------------- | ----------------------------------------------------------- |
| Joint positions        | rad                                                         |
| X, Y, Z of the TCP     | m, in the base frame of the robot                           |
| RX, RY, RZ of the TCP  | rad, a rotation vector, as in URScript and PolyScope        |

To get roll, pitch and yaw, call `FromRotationVectorToRPY()`. See [Convert position types](tools.md).

## Prerequisites

- RTDE: the service `RTDE` is enabled on the robot. The Primary Interface: the service `Primary Client Interface`. See [Prepare the robot](connect.md#prepare_the_robot).
- No remote control is needed to read data.

## Example

The program connects with RTDE at 125 Hz and the Primary Interface, and prints the positions given by both.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.Rtde;

class HowToGetPosition
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // RTDE: joint and tool positions, 125 times per second
    parameters.Rtde.Enable = true;
    parameters.Rtde.Frequency = 125;
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ActualQ);
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ActualTcpPose);

    // The Primary Interface is enabled by default: 10 packages per second
    robot.Connect(parameters);

    // Wait for the first packages
    Thread.Sleep(500);

    // 1. RTDE. Joint positions in rad, tool center point in m and rad
    JointsDoubleValues q = robot.Rtde.OutputDataValues.ActualQ;
    Pose tcp = robot.Rtde.OutputDataValues.ActualTcpPose;
    Console.WriteLine($"RTDE joints: {q.Base:F4} {q.Shoulder:F4} {q.Elbow:F4} {q.Wrist1:F4} {q.Wrist2:F4} {q.Wrist3:F4}");
    Console.WriteLine($"RTDE TCP: X={tcp.X:F4} Y={tcp.Y:F4} Z={tcp.Z:F4} RX={tcp.Rx:F4} RY={tcp.Ry:F4} RZ={tcp.Rz:F4}");

    // 2. Primary Interface. Same values, less often
    Pose tcp10Hz = robot.PrimaryInterface.CartesianInfo.AsPose();
    double shoulder = robot.PrimaryInterface.JointData.Shoulder.Position;
    Console.WriteLine($"Primary Interface TCP: X={tcp10Hz.X:F4} Y={tcp10Hz.Y:F4} Z={tcp10Hz.Z:F4}");

    // The orientation as roll, pitch, yaw, in degrees
    Pose rpy = tcp.FromRotationVectorToRPY();
    Console.WriteLine($"Roll={rpy.RxDegrees:F2} Pitch={rpy.RyDegrees:F2} Yaw={rpy.RzDegrees:F2}");

    robot.Disconnect();
  }
}
```

To follow the position continuously, use the event `OutputDataReceived` of RTDE: see [Receive data](rtde.md#receive_data).

## Troubleshooting

- **The values are 0 or `null`:** no package is received yet. Wait about 100 ms after the connection.
- **`ConnectException` on RTDE:** the service `RTDE` is disabled, or port 30004 is blocked.
- **The pose differs from PolyScope:** PolyScope shows the TCP of the active tool, in the base frame or in a feature. The SDK gives the TCP in the base frame.

## What to read next

- [RTDE](rtde.md): the setup and the events.
- [Kinematics](kinematics.md): from joint positions to a pose, and back.
- [Move the robot from a PC](how-to-move-robot.md).
