# Motion

Power the arm, set the motion descriptor, send MoveJJ, MoveJC, MoveL and MoveC moves, then stop, restart or cancel them.

Web page: https://underautomation.com/staubli/documentation/soap-motion

This page shows how to move a Staubli robot from a PC with the SDK: power the arm, describe the motion, send joint, linear and circular moves, then stop, restart or cancel them. The moves are executed by the motion planner of the CS8 or CS9 controller.

A robot is dangerous machinery. Test your code on the [emulator of Staubli Robotics Suite](simulator.md) first, then on the real robot with low speeds and a person at the emergency stop.

## Prerequisites

- The controller is in remote mode. Otherwise the power and the moves are refused.
- The user of the connection has the right to move the arm.
- The arm is powered: see below.

## Power

`SetPower(true)` powers the arm, `SetPower(false)` switches it off. The answer tells if the controller accepted the request.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class MotionPower
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // The controller must be in remote mode
        PowerReturnCode code = controller.Soap.SetPower(true);

        if (code != PowerReturnCode.Success)
            Console.WriteLine($"Arm not powered: {code}"); // OnlyInRemoteMode, EnableTimeout...

        // Power off at the end
        controller.Soap.SetPower(false);

        controller.Disconnect();
    }
}
```

| `PowerReturnCode`  | Meaning                                     |
| ------------------ | ------------------------------------------- |
| `Success`          | Done                                        |
| `OnlyInRemoteMode` | The controller is not in remote mode        |
| `RobotNotStopped`  | The power cannot change while the arm moves |
| `EnableTimeout`    | The arm was not powered in time             |
| `DisableTimeout`   | The arm was not switched off in time        |

## Motion descriptor

Every move takes a `MotionDesc`: the speed limits, the blending, the tool, the reference frame and the configuration of the arm.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class MotionDescriptor
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        double[] joints = controller.Soap.GetCurrentJointPosition(robot: 0);
        IForwardKinematics fk = controller.Soap.ForwardKinematics(robot: 0, joints);

        var mdesc = new MotionDesc
        {
            // Limits of the joint speed, acceleration and deceleration
            Velocity = 0.5,
            Acceleration = 0.5,
            Deceleration = 0.5,

            // Limits of the speed of the tool center point
            TranslationVelocity = 0.1,
            RotationVelocity = 0.1,

            // Stop at each point, no blending
            BlendType = BlendType.BlendOff,

            // Absolute target, flange as tool, world as reference frame
            AbsRel = MoveType.Absolute,
            Tool = new Frame(),
            Frame = new Frame(),

            // Keep the configuration of the arm (shoulder, elbow, wrist)
            Config = fk.Config,

            // Interpolation frequency in percent. 0 is refused by the controller (invalid motion descriptor)
            Frequency = 100,
        };

        controller.Disconnect();
    }
}
```

- `Velocity`, `Acceleration`, `Deceleration`: limits of the joints.
- `TranslationVelocity`, `RotationVelocity`: limits of the tool center point.
- `BlendType`: `BlendOff` stops at each point. `BlendJoint` and `BlendCartesian` join the moves without a stop, from `DistanceBlendPrevious` before the point to `DistanceBlendNext` after it.
- `Tool` and `Frame`: the tool center point and the reference frame of the Cartesian targets. `new Frame()` is the identity: the flange, and the world frame.
- `AbsRel`: `Absolute` targets, or `Relative` to the current position.
- `Config`: the configuration of the arm. See [Kinematics](soap-kinematics.md).

Start with low values and increase them step by step. Check on the emulator that the speeds and distances are the ones you expect before the first move of a real robot.

## Moves

| Method                                | Path                    | Target                       |
| ------------------------------------- | ----------------------- | ---------------------------- |
| `MoveJJ(robot, joints, mdesc)`        | joint interpolation     | joint values, in radians     |
| `MoveJC(robot, frame, mdesc)`         | joint interpolation     | a Cartesian frame            |
| `MoveL(robot, frame, mdesc)`          | straight line           | a Cartesian frame            |
| `MoveC(robot, frameB, frameC, mdesc)` | circle through `frameB` | the Cartesian frame `frameC` |

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class MotionMoves
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        double[] joints = controller.Soap.GetCurrentJointPosition(robot: 0);
        IForwardKinematics fk = controller.Soap.ForwardKinematics(robot: 0, joints);
        var mdesc = new MotionDesc { Velocity = 0.5, Acceleration = 0.5, Deceleration = 0.5, TranslationVelocity = 0.1, RotationVelocity = 0.1, Config = fk.Config, Frequency = 100 };

        Frame target = controller.Soap.ForwardKinematics(robot: 0, joints).Position;
        target.Px += 0.1;
        Frame intermediate = controller.Soap.ForwardKinematics(robot: 0, joints).Position;
        intermediate.Py += 0.05;

        controller.Soap.SetPower(true);

        // Joint move to joint values, in radians
        IMoveResult result = controller.Soap.MoveJJ(robot: 0, joints, mdesc);

        // Joint move to a Cartesian frame
        result = controller.Soap.MoveJC(robot: 0, target, mdesc);

        // Straight line to a Cartesian frame
        result = controller.Soap.MoveL(robot: 0, target, mdesc);

        // Circle through an intermediate frame, to a target frame
        result = controller.Soap.MoveC(robot: 0, intermediate, target, mdesc);

        // The controller accepted the move, or tells why not
        if (result.ReturnCode != MotionReturnCode.Success)
            Console.WriteLine($"Move {result.Id} refused: {result.ReturnCode}");

        controller.Disconnect();
    }
}
```

A move method returns the answer of the controller to the request. It does not tell that the arm has reached the target. `IMoveResult.ReturnCode` tells if the move was accepted, and `Id` identifies it:

| `MotionReturnCode` | Meaning                                               |
| ------------------ | ----------------------------------------------------- |
| `Success`          | The move is accepted                                  |
| `NotReady`         | The arm is not ready to move, for example not powered |
| `ParameterError`   | A value of the target or of the descriptor is wrong   |
| `MisuseError`      | The request is not allowed in this state              |
| `UnexpectedError`  | Another error of the controller                       |

To wait for the end of a move, read the position until it reaches the target: see [Position](soap-position.md).

## Stop, restart and cancel

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class MotionControl
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Stop the arm now
        MotionReturnCode code = controller.Soap.StopMotion();

        // Continue the moves that were stopped
        code = controller.Soap.RestartMotion();

        // Or cancel all the moves that are not finished
        code = controller.Soap.ResetMotion();

        controller.Disconnect();
    }
}
```

- `StopMotion()` stops the arm on its path.
- `RestartMotion()` continues the moves that were stopped.
- `ResetMotion()` cancels every move that is not finished. Call it after an error, before new moves.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/UnderAutomation.Staubli.Soap.Internal.md#soapclientbase-controllersoap))

- `IMoveResult MoveC(int robot, Frame frameB, Frame frameC, MotionDesc mdesc)`: Move the robot to a target position using a Cartesian path
- `IMoveResult MoveJC(int robot, Frame frame, MotionDesc mdesc)`: Move the robot to a target position using a Cartesian path with joint constraints
- `IMoveResult MoveJJ(int robot, double[] joints, MotionDesc mdesc)`: Move the robot to a target position using joint positions
- `IMoveResult MoveL(int robot, Frame frame, MotionDesc mdesc)`: Move the robot to a target position using a linear path in Cartesian space
- `MotionReturnCode ResetMotion()`: Reset the motion of the robot
- `MotionReturnCode RestartMotion()`: Restart the motion of the robot
- `PowerReturnCode SetPower(bool power)`: Set the power state of the robot (controller mut be in remote mode)
- `MotionReturnCode StopMotion()`: Stop the motion of the robot immediately

**MotionDesc** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#motiondesc))

- `MotionDesc()`: Initializes a new instance of the Data.MotionDesc class.
- `MoveType AbsRel { get; set; }`: Specifies whether the motion is defined in absolute or relative terms.
- `double Acceleration { get; set; }`: Maximum allowed joint acceleration, as a percentage of the robot's nominal acceleration.
- `BlendType BlendType { get; set; }`: Specifies the type of blending to be applied when transitioning between motion segments.
- `Config Config { get; set; }`: Contains additional configuration parameters specific to the robot type, such as anthropomorphic, SCARA, or VRBX configurations.
- `double Deceleration { get; set; }`: Maximum allowed joint deceleration, as a percentage of the robot's nominal deceleration.
- `double DistanceBlendNext { get; set; }`: In joint and Cartesian blending modes, the distance between the target point where blending ends and the next point, in millimeters or inches, depending on the length unit of the application.
- `double DistanceBlendPrevious { get; set; }`: In the joint and Cartesian blending modes, the distance between the target point where blending begins and the next point, in millimeters or inches, depending on the length unit used in the application.
- `Frame Frame { get; set; }`: Defines the frame in which the tool position is located, including both position and orientation.
- `double Frequency { get; set; }`: Frequency of motion in Hz.
- `double RotationVelocity { get; set; }`: Maximum permitted tool rotation speed, in degrees per second.
- `Frame Tool { get; set; }`: Defines the pose of the robot's tool center point (TCP) in flange, including both position and orientation.
- `double TranslationVelocity { get; set; }`: Maximum allowed feed rate of the tool center, in mm/s or inches/s depending on the length unit of the application.
- `double Velocity { get; set; }`: Maximum allowable joint speed, as a percentage of the robot's nominal speed.

**IMoveResult** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#imoveresult))

- `int Id { get; }`: Identifier of the motion command.
- `MotionReturnCode ReturnCode { get; }`: Return code indicating the outcome of the motion command.

**MotionReturnCode** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#motionreturncode))

- MisuseError: Motion command misuse error.
- NotReady: The robot is not ready to execute motion.
- ParameterError: Invalid parameter provided to the motion command.
- Success: Success, no error occurred.
- UnexpectedError: An unexpected error occurred during motion.

**PowerReturnCode** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#powerreturncode))

- DisableTimeout: Timeout while disabling power.
- EnableTimeout: Timeout while enabling power.
- OnlyInRemoteMode: Power can only be changed in remote mode.
- RobotNotStopped: Cannot change power while the robot is not stopped.
- Success: Success, no error occurred.

**BlendType** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#blendtype))

- BlendCartesian: Cartesian-space blending between motion segments.
- BlendJoint: Joint-space blending between motion segments.
- BlendOff: No blending; the robot stops at each target point.

**MoveType** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#movetype))

- Absolute: Absolute motion in the reference frame.
- Relative: Relative motion from the current position.
