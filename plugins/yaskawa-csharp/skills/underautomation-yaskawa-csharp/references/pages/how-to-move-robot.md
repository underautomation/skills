# Move the robot from a PC

Switch the servo on and move a Yaskawa robot in a straight line from C# or Python, without a job. Which move to choose, how to wait for the end, and the frequent errors.

Web page: https://underautomation.com/yaskawa/documentation/how-to-move-robot

This article shows how to move a Yaskawa Motoman robot from a PC, without a job, in C# or Python. It gives a complete program that switches the servo on, moves the tool 50 mm up in a straight line, waits for the end of the move and goes back.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- The controller accepts the remote commands. See [Prepare the controller](connect.md#prepare_the_controller).
- The cell is safe for a move: nobody in the cell, the safety functions active. Test at low speed first.

## Which move to choose

| Need                                          | Method and command type                                           |
| --------------------------------------------- | ----------------------------------------------------------------- |
| Go to a Cartesian position in a straight line | `MoveCartesian`, `StraightAbsolute`                               |
| Go to a Cartesian position, fastest path      | `MoveCartesian`, `LinkAbsolute`                                   |
| Move by an offset (approach, retract)         | `MoveCartesian`, `StraightIncrement`                              |
| Go back to a position read in pulses          | `MoveJoints`, `LinkAbsolute`                                      |
| Run a taught path                             | A job: see [Run a job](how-to-run-program.md) |

## Example

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class HowToMoveRobot
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // 1. Remote mode, no alarm
        RobotStatusData status = robot.HighSpeedEServer.GetStatusInformation();
        if (!status.CommandRemote) throw new InvalidOperationException("Enable the remote mode");
        if (status.Alarming) robot.HighSpeedEServer.AlarmReset(AlarmResetType.Reset);

        // 2. Servo on
        robot.HighSpeedEServer.SetServo(true);

        // 3. Read the current position, then move 50 mm up in a straight line, at 20 mm/s
        RobotPositionCartesianData start = robot.HighSpeedEServer.GetRobotCartesianPosition();

        robot.HighSpeedEServer.MoveCartesian(
            start.X, start.Y, start.Z + 50, start.Rx, start.Ry, start.Rz,
            PositionCommandClassification.Cartesian_MM_S, 20,
            PositionCommandOperationCoordinate.Robot,
            posture: start.Form,
            commandtype: PositionCommandType.StraightAbsolute);

        // 4. The method returns when the controller accepts the move: wait for the target, 30 s at most
        DateTime timeout = DateTime.Now.AddSeconds(30);
        while (Math.Abs(robot.HighSpeedEServer.GetRobotCartesianPosition().Z - (start.Z + 50)) > 0.5)
        {
            if (DateTime.Now > timeout) throw new TimeoutException("Target not reached");
            Thread.Sleep(100);
        }

        // 5. Back to the start, joint interpolated, at 10 %
        robot.HighSpeedEServer.MoveCartesian(
            start.X, start.Y, start.Z, start.Rx, start.Ry, start.Rz,
            PositionCommandClassification.LinkPercent, 10,
            PositionCommandOperationCoordinate.Robot,
            posture: start.Form,
            commandtype: PositionCommandType.LinkAbsolute);

        robot.Disconnect();
    }
}
```

The program:

1. checks the remote mode and resets a pending alarm;
2. switches the servo on;
3. reads the current position and sends a straight move 50 mm above it, at 20 mm/s, with the same posture;
4. reads the position every 100 ms until the robot is within 0.5 mm of the target, with a timeout of 30 s;
5. goes back to the start with a joint move at 10 % of the maximum speed.

## Wait for the end of a move

`MoveCartesian` and `MoveJoints` return when the controller accepts the move. To chain moves or to act after a move, wait for the target as in the example. Send the next move only after the end of the previous one.

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) has the same moves, with one method per type: `MoveLinear`, `MoveJoint`, `MoveIncremental`, `MovePulseJoint` and `MovePulseLinear`. The speed of a linear move is in mm/s or in percent, and the target can be in a user frame or in the tool frame.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerMoveCartesian
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        robot.EServer.SetServo(true);

        // Straight line to X=400 Y=0 Z=300 (mm), Rx=180 Ry=0 Rz=0 (degrees), at 50 mm/s, tool 0
        robot.EServer.MoveLinear(HostControlSpeedType.MillimetersPerSecond, 50,
            HostControlCoordinateSystem.Base, 400, 0, 300, 180, 0, 0);

        // Joint move to another target, at 10 % of the maximum speed
        robot.EServer.MoveJoint(10, HostControlCoordinateSystem.Base, 400, 100, 300, 180, 0, 0);

        robot.Disconnect();
    }
}
```

## Check the target before the move

The [offline kinematics](kinematics-inverse.md) tell if a target can be reached, and with which joint angles, before you send it. An empty list of solutions means that the robot cannot reach the target.

## Troubleshooting

- **The robot moves by the values instead of going to them:** `MoveCartesian` uses `StraightIncrement` when `commandtype` is not given. Pass `StraightAbsolute` or `LinkAbsolute`.
- **`Servo OFF` or `Turn ON the servo power`:** switch the servo on before the move.
- **`Command remote not set`:** see [Prepare the controller](connect.md#prepare_the_controller).
- **The robot takes another configuration:** pass the posture of the start position (`Form`) to `MoveCartesian`.
- **A speed or frame setting error:** check the pair of `PositionCommandClassification` and command type, and the tool and user frame numbers.

## What to read next

- [Motion](hses-motion.md): all the arguments of the moves.
- [Get the robot position](how-to-get-position.md).
