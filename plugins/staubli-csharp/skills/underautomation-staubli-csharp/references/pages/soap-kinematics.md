# Kinematics

Compute the forward and inverse kinematics of a Staubli robot on the controller, with the configuration of the arm and the joint ranges.

Web page: https://underautomation.com/staubli/documentation/soap-kinematics

This page shows how to compute the forward and inverse kinematics of a Staubli robot with the SDK. The controller computes them with the geometry of the real arm: the result is the one that the CS8 or CS9 controller uses for its own moves.

## Forward kinematics

`ForwardKinematics(robot, joints)` returns the flange frame for joint values in radians, and the configuration of the arm for these joints.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class KinematicsForward
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Joint values in radians, here the current ones
        double[] joints = controller.Soap.GetCurrentJointPosition(robot: 0);

        // The controller computes the flange frame for these joints
        IForwardKinematics fk = controller.Soap.ForwardKinematics(robot: 0, joints);

        // Position of the frame origin, and its orientation as a rotation matrix
        Frame frame = fk.Position;
        Console.WriteLine($"P = [{frame.Px}, {frame.Py}, {frame.Pz}]");

        // Configuration of the arm for this position (shoulder, elbow, wrist)
        Config config = fk.Config;
        Console.WriteLine(config);

        controller.Disconnect();
    }
}
```

The result is a `Frame`: the origin `Px`, `Py`, `Pz` in meters, and a rotation matrix given by its three columns:

| Column | Properties       | Axis of the frame     |
| ------ | ---------------- | --------------------- |
| N      | `Nx`, `Ny`, `Nz` | X axis                |
| O      | `Ox`, `Oy`, `Oz` | Y axis                |
| A      | `Ax`, `Ay`, `Az` | Z axis, approach axis |

## Configuration

A Cartesian position can be reached with several joint positions: shoulder on the left or on the right, elbow up or down, wrist flipped or not. The `Config` object selects one of them. It has one part per type of arm:

- `AnthroConfig` for 6 axis arms: `Shoulder` (`Lefty`, `Righty`), `Elbow` and `Wrist` (`Positive`, `Negative`);
- `ScaraConfig` for SCARA arms: `Shoulder`;
- `VrbxConfig` for the other kinematics.

Each value can also be `Same` (keep the current configuration) or `Free` (any configuration).

## Inverse kinematics

`ReverseKinematics(robot, joints, target, config, jointRange)` returns the joints for a target frame. The controller starts from `joints`, keeps the configuration `config`, and rejects a solution out of `jointRange`.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class KinematicsInverse
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        double[] current = controller.Soap.GetCurrentJointPosition(robot: 0);
        JointRange range = controller.Soap.GetJointRange(robot: 0);

        // Target: the current flange frame, 50 mm higher
        IForwardKinematics fk = controller.Soap.ForwardKinematics(robot: 0, current);
        Frame target = fk.Position;
        target.Pz += 0.050;

        // Keep the current configuration of the arm
        IReverseKinematics ik = controller.Soap.ReverseKinematics(robot: 0, current, target, fk.Config, range);

        if (ik.Result == ReversingResult.Success)
            Console.WriteLine(string.Join(", ", ik.Joint));
        else
            Console.WriteLine($"No solution: {ik.Result}"); // OutOfWorkspace, JointOutOfRange...

        controller.Disconnect();
    }
}
```

Always test `Result` before you use the joints:

| `ReversingResult`      | Meaning                                 |
| ---------------------- | --------------------------------------- |
| `Success`              | `Joint` holds the solution              |
| `OutOfWorkspace`       | The target is out of reach              |
| `JointOutOfRange`      | The solution is out of the joint ranges |
| `InvalidConfiguration` | No solution with this configuration     |
| `NoConvergence`        | The computation did not find a solution |

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/UnderAutomation.Staubli.Soap.Internal.md#soapclientbase-controllersoap))

- `IForwardKinematics ForwardKinematics(int robot, double[] joints)`: Calculate the forward kinematics of a robot based on its joint positions
- `IReverseKinematics ReverseKinematics(int robot, double[] joint, Frame target, Config config, JointRange jointRange)`: Calculate the reverse kinematics of a robot to reach a target position and orientation

**IForwardKinematics** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#iforwardkinematics))

- `Config Config { get; }`: Robot configuration associated with the computed position.
- `Frame Position { get; }`: Cartesian position resulting from the forward kinematics computation.

**IReverseKinematics** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#ireversekinematics))

- `double[] Joint { get; }`: Joint angles resulting from the reverse kinematics computation.
- `ReversingResult Result { get; }`: Result code indicating the outcome of the reverse kinematics computation.

**ReversingResult** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#reversingresult))

- InvalidConfiguration: The specified configuration is invalid.
- InvalidErrorCode: Invalid error code returned.
- InvalidOrientation: The specified orientation is invalid.
- JointOutOfRange: The computed joint position is out of range.
- NoConvergence: The algorithm did not converge to a solution.
- OutOfWorkspace: The target is outside the robot workspace.
- Success: Reverse kinematics succeeded.
- UnconstrainedFrame: The frame is unconstrained.
- UnsupportedKinematics: The robot kinematics type is not supported.

**Frame** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#frame))

- `Frame()`: Default constructor.
- `double Ax { get; set; }`: X component of the local Z-axis vector (Approach X).
- `double Ay { get; set; }`: Y component of the local Z-axis vector (Approach Y).
- `double Az { get; set; }`: Z component of the local Z-axis vector (Approach Z).
- `double Nx { get; set; }`: X component of the local X-axis vector (Normal X).
- `double Ny { get; set; }`: Y component of the local X-axis vector (Normal Y).
- `double Nz { get; set; }`: Z component of the local X-axis vector (Normal Z).
- `double Ox { get; set; }`: X component of the local Y-axis vector (Orientation X).
- `double Oy { get; set; }`: Y component of the local Y-axis vector (Orientation Y).
- `double Oz { get; set; }`: Z component of the local Y-axis vector (Orientation Z).
- `double Px { get; set; }`: X coordinate of the frame's origin in global space (Pose X).
- `double Py { get; set; }`: Y coordinate of the frame's origin in global space (Pose Y).
- `double Pz { get; set; }`: Z coordinate of the frame's origin in global space (Pose Z).

**Config** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#config))

- `Config()`: Initializes a new instance of the Data.Config class.
- `AnthroConfig AnthroConfig { get; set; }`: Anthropomorphic robot configuration.
- `ScaraConfig ScaraConfig { get; set; }`: SCARA robot configuration.
- `VrbxConfig VrbxConfig { get; set; }`: VRBX robot configuration.

**AnthroConfig** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#anthroconfig))

- `AnthroConfig()`: Initializes a new instance of the Data.AnthroConfig class.
- `PositiveNegativeConfig Elbow { get; set; }`: Elbow configuration.
- `ShoulderConfig Shoulder { get; set; }`: Shoulder configuration.
- `PositiveNegativeConfig Wrist { get; set; }`: Wrist configuration.

**ScaraConfig** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#scaraconfig))

- `ScaraConfig()`: Initializes a new instance of the Data.ScaraConfig class.
- `ShoulderConfig Shoulder { get; set; }`: Shoulder configuration.
