# Move the robot from a PC

Power the arm and move a Staubli robot in a straight line from C# or Python, without a VAL 3 program. Which move to choose, and the frequent errors.

Web page: https://underautomation.com/staubli/documentation/how-to-move-robot

This article shows how to move a Staubli robot from a PC, in C# or Python, on a CS8 or CS9 controller, without writing a VAL 3 program. It gives a complete program that powers the arm and moves the tool 20 mm down and back in a straight line.

A robot is dangerous machinery. Run this program on the [emulator of Staubli Robotics Suite](simulator.md) first. On a real robot, keep the speeds low and a person at the emergency stop.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- The controller is in remote mode, and no VAL 3 application moves the arm.
- The user of the connection has the right to move the arm.

## Which move to choose

| Move     | Path                               | Use it to                                                      |
| -------- | ---------------------------------- | -------------------------------------------------------------- |
| `MoveJJ` | joint interpolation, to joints     | go to a known joint position, for example a home position      |
| `MoveJC` | joint interpolation, to a frame    | go fast to a Cartesian position, when the path does not matter |
| `MoveL`  | straight line, to a frame          | approach, insert, follow an edge                               |
| `MoveC`  | circle through a point, to a frame | follow an arc                                                  |

A joint move is usually the fastest when the path does not matter. Use `MoveL` and `MoveC` when the tool must follow a given path.

## Example

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class HowToMoveRobot
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // 1. Start from the current position and configuration
        double[] joints = controller.Soap.GetCurrentJointPosition(robot: 0);
        IForwardKinematics current = controller.Soap.ForwardKinematics(robot: 0, joints);

        // 2. Low speed limits for a first test
        var mdesc = new MotionDesc
        {
            Velocity = 0.1,
            Acceleration = 0.1,
            Deceleration = 0.1,
            TranslationVelocity = 0.05,
            RotationVelocity = 0.05,
            Config = current.Config,
            Frequency = 100, // interpolation frequency in percent, 0 is refused
        };

        // 3. Power the arm. The controller must be in remote mode.
        PowerReturnCode power = controller.Soap.SetPower(true);
        if (power != PowerReturnCode.Success)
            throw new InvalidOperationException($"Power refused: {power}");

        // 4. Straight line 20 mm down, then back
        Frame target = current.Position;
        double startZ = target.Pz;

        target.Pz = startZ - 0.020;
        IMoveResult down = controller.Soap.MoveL(robot: 0, target, mdesc);

        target.Pz = startZ;
        IMoveResult up = controller.Soap.MoveL(robot: 0, target, mdesc);

        if (down.ReturnCode != MotionReturnCode.Success || up.ReturnCode != MotionReturnCode.Success)
            controller.Soap.ResetMotion();

        controller.Disconnect();
    }
}
```

The program:

1. reads the current joints and computes the current frame and configuration of the arm;
2. sets low speed limits in the motion descriptor, and keeps the current configuration;
3. powers the arm, and stops if the controller refuses;
4. moves down 20 mm in a straight line, then back, and cancels the moves if one is refused.

The target is the current frame with a new `Pz`: the orientation of the tool does not change.

## Wait for the end of a move

A move method returns the answer of the controller to the request, with an `Id` for the move. It does not tell that the arm has reached the target. To wait for the arm, read the position until it reaches the target. See [How to get the position](how-to-get-position.md).

## Troubleshooting

- **`SetPower` returns `OnlyInRemoteMode`:** put the controller in remote mode.
- **The move returns `NotReady`:** the arm is not ready to move, for example not powered. Power it, call `ResetMotion()` after an error, and send the move again.
- **The move returns `ParameterError`:** check the target and the values of the motion descriptor.
- **The arm takes an unexpected path to a frame:** set `Config` in the motion descriptor. `fk.Config` of the current position keeps the current configuration.

## What to read next

- [Motion](soap-motion.md): the reference of power, moves and motion descriptor.
- [Kinematics](soap-kinematics.md): check that a target is reachable before you move.
