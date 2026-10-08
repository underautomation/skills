# Motion

Move a Yaskawa robot from a PC: linear and joint moves to a Cartesian target, relative moves, moves in pulses, speed units, frames and posture.

Web page: https://underautomation.com/yaskawa/documentation/hses-motion

This page shows how to move a Yaskawa Motoman robot from a PC with the SDK, without a job: Cartesian moves in mm and degrees, relative moves, and joint moves in pulses. The moves need the remote mode and the servo power.

## Prerequisites

- The controller accepts the remote commands: see [Connect to your robot](connect.md#prepare_the_controller).
- No alarm is active, and the robot is not held.
- The servo power is on: `SetServo(true)`.

A move sent by the SDK is a real move of the robot. Test at low speed, in a cell with its safety functions active.

## Cartesian move

`MoveCartesian` moves the tool center point to a position given in mm and degrees, in a frame.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class MotionMoveCartesian
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // The servo must be on, the controller in remote mode
        robot.HighSpeedEServer.SetServo(true);

        // Linear move to an absolute position of the robot frame, at 50 mm/s
        robot.HighSpeedEServer.MoveCartesian(
            x: 850, y: 0, z: 400,    // mm
            rx: 180, ry: 0, rz: 0,   // degrees
            PositionCommandClassification.Cartesian_MM_S,
            speed: 50,
            PositionCommandOperationCoordinate.Robot,
            commandtype: PositionCommandType.StraightAbsolute);

        // Joint interpolated move to the same target, at 10 % of the maximum speed
        robot.HighSpeedEServer.MoveCartesian(
            850, 0, 400, 180, 0, 0,
            PositionCommandClassification.LinkPercent,
            speed: 10,
            PositionCommandOperationCoordinate.Robot,
            commandtype: PositionCommandType.LinkAbsolute);

        robot.Disconnect();
    }
}
```

| Argument                                   | Meaning                                                            |
| ------------------------------------------ | ------------------------------------------------------------------ |
| `x`, `y`, `z`                              | Position, in mm                                                    |
| `rx`, `ry`, `rz`                           | Orientation, in degrees                                            |
| `classification`                           | Unit of `speed`, see below                                         |
| `speed`                                    | Speed of the move                                                  |
| `coordinate`                               | Frame of the position: `Base`, `Robot`, `User` or `Tool`           |
| `posture`                                  | Posture of the target, see below. `null`: the default posture      |
| `commandtype`                              | Absolute or relative move, see below. Default: `StraightIncrement` |
| `RobotControlGroup`, `StationControlGroup` | Robot and station that move. Default: robot 1, no station          |
| `tool`                                     | Tool number. Default: `0`                                          |
| `userCoordinate`                           | User frame number, when `coordinate` is `User`. Default: `0`       |

### Command type

| `PositionCommandType` | Path               | Target                                     |
| --------------------- | ------------------ | ------------------------------------------ |
| `LinkAbsolute`        | Joint interpolated | The position given                         |
| `StraightAbsolute`    | Straight line      | The position given                         |
| `StraightIncrement`   | Straight line      | The current position plus the values given |

The default command type of `MoveCartesian` is `StraightIncrement`: without `commandtype`, the values are an offset from the current position. Always pass `commandtype` when you give an absolute position.

### Speed

| `PositionCommandClassification` | Unit of `speed`                    |
| ------------------------------- | ---------------------------------- |
| `LinkPercent`                   | Percent of the maximum joint speed |
| `Cartesian_MM_S`                | mm/s of the tool center point      |
| `Cartesian_DEG_S`               | Degrees/s of the orientation       |

Use `LinkPercent` with `LinkAbsolute`, and a Cartesian speed with the straight moves.

## Relative move

With `StraightIncrement`, the values are an offset. The frame gives the direction of the offset: `Base` to move along the axes of the base, `Tool` to move along the axes of the tool.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class MotionMoveIncrement
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        robot.HighSpeedEServer.SetServo(true);

        // Move the tool 20 mm up in the base frame, in a straight line at 20 mm/s.
        // StraightIncrement is the default command type of MoveCartesian
        robot.HighSpeedEServer.MoveCartesian(
            0, 0, 20, 0, 0, 0,
            PositionCommandClassification.Cartesian_MM_S,
            speed: 20,
            PositionCommandOperationCoordinate.Base,
            commandtype: PositionCommandType.StraightIncrement);

        // Move 10 mm along the Z axis of tool 1
        robot.HighSpeedEServer.MoveCartesian(
            0, 0, 10, 0, 0, 0,
            PositionCommandClassification.Cartesian_MM_S,
            speed: 20,
            PositionCommandOperationCoordinate.Tool,
            commandtype: PositionCommandType.StraightIncrement,
            tool: 1);

        robot.Disconnect();
    }
}
```

## Joint move

`MoveJoints` moves each axis to a position in pulses, the unit of [GetRobotJointPosition](hses-positions.md#joint_positions).

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class MotionMoveJoints
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        robot.HighSpeedEServer.SetServo(true);

        // Read the current pulses and change the first axis
        int[] target = robot.HighSpeedEServer.GetRobotJointPosition().Axes;
        target[0] += 10000;

        // Joint interpolated move to absolute pulses, at 5 % of the maximum speed
        robot.HighSpeedEServer.MoveJoints(
            target,
            PositionCommandClassification.LinkPercent,
            speed: 5,
            PositionCommandType.LinkAbsolute,
            RobotControlGroup: 1,
            StationControlGroup: 0);

        robot.Disconnect();
    }
}
```

Pass the command type `LinkAbsolute` and the speed in `LinkPercent`, as above. `axesPulse` has one value per axis, up to 8: start from the current pulses and change the axes you want to move.

## Posture

A Cartesian position can be reached with several postures: arm in front or behind, upper or lower arm, wrist flipped or not, and the ranges of some axes. `RobotPosture` selects one. The posture of the current position is the `Form` of `GetRobotCartesianPosition()`: pass it to stay in the same configuration.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class MotionPosture
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // The posture of the current position
        RobotPosture current = robot.HighSpeedEServer.GetRobotCartesianPosition().Form;
        Console.WriteLine(current);

        // A posture written field by field
        var posture = new RobotPosture(
            orientation: OrientationFlipInformation.Front,
            arm: ArmFlipInformation.Upper,
            flip: FlipNoFlipInformation.Flip);

        // The posture selects one of the joint solutions of the Cartesian target
        robot.HighSpeedEServer.MoveCartesian(
            850, 0, 400, 180, 0, 0,
            PositionCommandClassification.Cartesian_MM_S, 50,
            PositionCommandOperationCoordinate.Robot,
            posture: posture,
            commandtype: PositionCommandType.StraightAbsolute);

        robot.Disconnect();
    }
}
```

In Python, create a posture with `RobotPosture.from_integer(0)`, then set its fields.

## End of the move

`MoveCartesian` and `MoveJoints` return when the controller accepts the move, not at the end of the move. To wait for the end, read the position until it reaches the target: see [Move the robot from a PC](how-to-move-robot.md).

To stop a move, hold the robot: `SetHold(true)`.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md#highspeedeserverclientbase-robothighspeedeserver))

- `RobotDataHeader MoveCartesian(double x, double y, double z, double rx, double ry, double rz, PositionCommandClassification classification, double speed, PositionCommandOperationCoordinate coordinate, RobotPosture posture = null, PositionCommandType commandtype = PositionCommandType.StraightIncrement, int RobotControlGroup = 1, int StationControlGroup = 0, int tool = 0, int userCoordinate = 0)`: Commands the robot to move to a Cartesian position (X, Y, Z, Rx, Ry, Rz). Movement is relative to the specified coordinate system.
- `RobotDataHeader MoveJoints(int[] axesPulse, PositionCommandClassification classification, double speed, PositionCommandType commandtype = PositionCommandType.StraightIncrement, int RobotControlGroup = 1, int StationControlGroup = 1, int tool = 0)`: Commands the robot to move using joint (pulse) positions. This specifies the position of each axis directly in encoder pulses.

**PositionCommandType** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#positioncommandtype))

- LinkAbsolute: Link (joint interpolated) motion to an absolute position. All joints move simultaneously to reach the target, resulting in non-linear TCP path.
- StraightAbsolute: Straight (linear interpolated) motion to an absolute position. TCP moves in a straight line to the target position.
- StraightIncrement: Straight (linear interpolated) motion by an incremental offset. TCP moves in a straight line relative to current position.

**PositionCommandClassification** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#positioncommandclassification))

- Cartesian_DEG_S: Speed in degrees per second for rotational motion. Valid range depends on robot model.
- Cartesian_MM_S: Speed in millimeters per second for linear motion. Valid range depends on robot model.
- LinkPercent: Speed as percentage of maximum link (joint) speed. Valid range: 0.01 to 100.00 percent.

**PositionCommandOperationCoordinate** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#positioncommandoperationcoordinate))

- Base: Base coordinate system (world frame at robot base). Fixed reference frame typically aligned with robot mounting.
- Robot: Robot coordinate system. Reference frame at the robot's origin point.
- Tool: Tool coordinate system. Reference frame at the tool center point (TCP).
- User: User-defined coordinate system. Custom reference frame defined for specific workpiece or fixture.

**RobotPosture** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotposture))

- `RobotPosture()`: Creates a new RobotPosture with default values.
- `RobotPosture(int form, int extendedForm)`: Creates a new RobotPosture with specified form values.
- `RobotPosture(OrientationFlipInformation orientation = OrientationFlipInformation.Front, ArmFlipInformation arm = ArmFlipInformation.Upper, FlipNoFlipInformation flip = FlipNoFlipInformation.Flip, AxisFlipInformation rAxis = AxisFlipInformation.LT180, AxisFlipInformation tAxis = AxisFlipInformation.LT180, AxisFlipInformation sAxis = AxisFlipInformation.LT180, OrientationFlipInformation redundant = OrientationFlipInformation.Front, RegardedReversePositionSpecified regardedReversePositionSpecified = RegardedReversePositionSpecified.Previous, AxisFlipInformation lAxis = AxisFlipInformation.LT180, AxisFlipInformation uAxis = AxisFlipInformation.LT180, AxisFlipInformation bAxis = AxisFlipInformation.LT180, AxisFlipInformation eAxis = AxisFlipInformation.LT180, AxisFlipInformation wAxis = AxisFlipInformation.LT180)`: Creates a new RobotPosture with specified configuration values.
- `ArmFlipInformation Arm { get; set; }`: Gets or sets the upper/lower arm configuration based on L and U axis positions.
- `AxisFlipInformation BAxis { get; set; }`: Gets or sets the B-axis (wrist bend) angle range configuration from extended form.
- `static readonly RobotPosture Default`: Default posture with Form=0 and ExtendedForm=0.
- `AxisFlipInformation EAxis { get; set; }`: Gets or sets the E-axis (external/elbow) angle range configuration from extended form.
- `int ExtendedForm { get; set; }`: Gets or sets the extended form byte for additional axis configurations. Bit-encoded: L-axis, U-axis, B-axis, E-axis, W-axis range flags.
- `FlipNoFlipInformation Flip { get; set; }`: Gets or sets the flip/no-flip wrist configuration.
- `int Form { get; set; }`: Gets or sets the primary form byte encoding basic posture flags. Bit-encoded: orientation, arm, flip, R-axis, T-axis, S-axis, redundant, reverse position.
- `static RobotPosture FromInteger(int value)`: Creates a RobotPosture from a combined 16-bit integer value.
- `AxisFlipInformation LAxis { get; set; }`: Gets or sets the L-axis (lower arm) angle range configuration from extended form.
- `OrientationFlipInformation Orientation { get; set; }`: Gets or sets the front/back orientation configuration. Specifies where the B-axis rotation center locates relative to the S-axis when viewing the L and U axes from the right-hand side.
- `AxisFlipInformation RAxis { get; set; }`: Gets or sets the R-axis (wrist rotation) angle range configuration.
- `OrientationFlipInformation Redundant { get; set; }`: Gets or sets the redundant axis orientation configuration (for 7+ axis robots).
- `RegardedReversePositionSpecified RegardedReversePositionSpecified { get; set; }`: Gets or sets the reverse position specification mode.
- `AxisFlipInformation SAxis { get; set; }`: Gets or sets the S-axis (base rotation) angle range configuration.
- `AxisFlipInformation TAxis { get; set; }`: Gets or sets the T-axis (tool rotation) angle range configuration.
- `int ToInteger()`: Converts the posture to a single 16-bit integer value. Form is stored in the low byte, ExtendedForm in the high byte.
- `AxisFlipInformation UAxis { get; set; }`: Gets or sets the U-axis (upper arm) angle range configuration from extended form.
- `AxisFlipInformation WAxis { get; set; }`: Gets or sets the W-axis angle range configuration from extended form.
