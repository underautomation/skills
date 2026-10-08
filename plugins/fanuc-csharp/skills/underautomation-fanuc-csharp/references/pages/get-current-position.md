# Get current position

Retrieve the current robot position (joint and Cartesian) using SNPX, FTP, CGTP, or Telnet. Compare approaches and choose the best for your use case.

Web page: https://underautomation.com/fanuc/documentation/get-current-position

Read the current tool position of your Fanuc robot in Cartesian (X, Y, Z, W, P, R) or joint (J1–J6) format using different protocols.

## SNPX (fastest : ~2 ms)

SNPX provides the fastest position reading, in world or user frame coordinates.

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

See also: [SNPX Current position](snpx-position.md)

## CGTP Web Server

CGTP returns Cartesian and joint positions separately:

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class GetCurrentPositionCgtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read Cartesian position
        CartesianPosition cartesian = robot.Cgtp.ReadCartesianPosition();
        Console.WriteLine($"X={cartesian.X}, Y={cartesian.Y}, Z={cartesian.Z}");

        // Read joint position
        JointsPosition joints = robot.Cgtp.ReadJointPosition();
        Console.WriteLine($"J1={joints.J1}, J2={joints.J2}, J3={joints.J3}");

        // Multi-group
        CartesianPosition group2 = robot.Cgtp.ReadCartesianPosition(groupNum: 2);
    }
}
```

See also: [CGTP Position & kinematics](cgtp-position-kinematics.md)

## FTP (offline parsing)

Download and parse the current position diagnostic file:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class GetCurrentPositionFtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        CurrentPosition curPos = robot.Ftp.GetSummaryDiagnostic().CurrentPosition;
    }
}
```

See also: [FTP Diagnostics & variables](ftp-diagnostics.md)

## Telnet KCL

Read position-related system variables:

```csharp
using UnderAutomation.Fanuc;

public class GetCurrentPositionTelnet
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        var curpos = robot.Telnet.GetCurrentPose();
    }
}
```

## Protocol comparison

| Feature | SNPX | CGTP | FTP | Telnet |
|---------|------|------|-----|--------|
| **Speed** | ~2 ms | ~50 ms | ~100 ms | ~30 ms |
| **World frame** | Yes | Yes | Yes | Yes |
| **User frame** | Yes | No | No | No |
| **Joint position** | Yes | Yes | Yes | Yes |
| **Multi-group** | Yes | Yes | No | No |
