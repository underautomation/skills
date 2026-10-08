# Forward and inverse kinematics

Compute the forward and inverse kinematics of UR cobots without a robot: DH parameters of each model, flange pose, up to 8 solutions, singularities.

Web page: https://underautomation.com/universal-robots/documentation/kinematics

The namespace `UnderAutomation.UniversalRobots.Kinematics` computes the forward and inverse kinematics of Universal Robots cobots, without a connection to a robot. This page shows how to get the DH parameters of a robot, compute the position of the flange from the joint positions and back, and detect the singularities.

- **Forward kinematics:** 6 joint positions give the position and the orientation of the flange.
- **Inverse kinematics:** a position and an orientation of the flange give up to 8 sets of joint positions.

## DH parameters

The Denavit-Hartenberg (DH) parameters describe the geometry of the arm. Each joint has four parameters: θ (rotation around z, the joint variable), d (offset along z), a (length along x) and α (rotation around x). On UR cobots, only a2, a3, d1, d4, d5 and d6 change between the models:

| Joint | a [m]  | d [m]  | α [rad] | θ [rad] |
| ----: | :----: | :----: | :-----: | :-----: |
|    J1 |   0    | **d1** |  +π/2   | **θ1**  |
|    J2 | **a2** |   0    |    0    | **θ2**  |
|    J3 | **a3** |   0    |    0    | **θ3**  |
|    J4 |   0    | **d4** |  +π/2   | **θ4**  |
|    J5 |   0    | **d5** |  −π/2   | **θ5**  |
|    J6 |   0    | **d6** |    0    | **θ6**  |

See the [DH parameters of each model](https://www.universal-robots.com/articles/ur/application-installation/dh-parameters-for-calculations-of-kinematics-and-dynamics/) by Universal Robots.

### Nominal or custom parameters

`GetDhParametersFromModel` returns the nominal parameters of a model (UR3 to UR30, CB-Series and e-Series). `CustomUrDhParameters` takes your own values.

```csharp
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.Kinematics;

class KinematicsDhParameters
{
  static void Main(string[] args)
  {
    // Nominal DH parameters of a model
    IUrDhParameters ur5e = KinematicsUtils.GetDhParametersFromModel(RobotModelsExtended.UR5e);

    // Or your own values, in meters
    IUrDhParameters custom = new CustomUrDhParameters(
      a2: -0.425,
      a3: -0.3922,
      d1: 0.1625,
      d4: 0.1333,
      d5: 0.0997,
      d6: 0.0996);
  }
}
```

### Parameters of a connected robot

The Primary Interface sends the DH parameters of the robot, with its calibration, in `KinematicsInfo` and `ConfigurationData`. Both implement `IUrDhParameters`.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.PrimaryInterface;

class KinematicsFromRobot
{
  static void Main(string[] args)
  {
    var robot = new UR();

    // The Primary Interface is enabled by default
    robot.Connect("192.168.0.1");

    // Wait for the first packages (10 Hz)
    Thread.Sleep(500);

    // DH parameters of this robot, with its calibration
    IUrDhParameters dh = robot.PrimaryInterface.KinematicsInfo;

    // Current joint positions, in radians
    JointDataPackageEventArgs j = robot.PrimaryInterface.JointData;
    double[] joints =
    {
      j.Base.Position, j.Shoulder.Position, j.Elbow.Position,
      j.Wrist1.Position, j.Wrist2.Position, j.Wrist3.Position
    };

    // Current position of the tool center point
    Pose pose = robot.PrimaryInterface.CartesianInfo.AsPose();
  }
}
```

**IUrDhParameters** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#iurdhparameters))

- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Forward kinematics

`ForwardKinematics` takes 6 joint positions in radians. `ToolTransform` is the 4x4 transform of the flange in the base frame: `Pose.From4x4MatrixToRotationVector` converts it to a pose in meters and radians. Add the TCP offset of your tool to get the position of the tool center point.

```csharp
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.Kinematics;

class KinematicsForward
{
  static void Main(string[] args)
  {
    IUrDhParameters dh = KinematicsUtils.GetDhParametersFromModel(RobotModelsExtended.UR5e);

    // Joint positions in radians: base, shoulder, elbow, wrist 1, wrist 2, wrist 3
    double[] joints = { 0, -1.57, 1.57, -1.57, -1.57, 0 };

    KinematicsResult result = KinematicsUtils.ForwardKinematics(joints, dh);

    // 4x4 transform of the flange, as a pose: X, Y, Z in m, rotation vector in rad
    Pose flange = Pose.From4x4MatrixToRotationVector(result.ToolTransform);

    // Transform of each joint, alone and composed with the previous ones
    TransformationSet local = result.IndividualLocalTransforms;
    TransformationSet global = result.CumulativeGlobalTransforms;
  }
}
```

`IndividualLocalTransforms` gives the transform of each joint alone, and `CumulativeGlobalTransforms` the transform of each joint composed with the previous ones.

**KinematicsResult** ([reference](../api/UnderAutomation.UniversalRobots.Kinematics.md#kinematicsresult))

- `KinematicsResult()`
- `TransformationSet CumulativeGlobalTransforms { get; set; }`: Cumulative global transformation matrices of each joint
- `TransformationSet IndividualLocalTransforms { get; set; }`: Individual local transformation matrices of each joint
- `double[,] ToolTransform { get; set; }`: 4x4 transformation matrix of the tool

**TransformationSet** ([reference](../api/UnderAutomation.UniversalRobots.Kinematics.md#transformationset))

- `TransformationSet()`
- `double[,] Base { get; set; }`: 4x4 transformation matrix of the base joint 1
- `double[,] Elbow { get; set; }`: 4x4 transformation matrix of the elbow joint 3
- `double[,] Shoulder { get; set; }`: 4x4 transformation matrix of the shoulder joint 2
- `double[,] Wrist1 { get; set; }`: 4x4 transformation matrix of the wrist1 joint 4
- `double[,] Wrist2 { get; set; }`: 4x4 transformation matrix of the wrist2 joint 5
- `double[,] Wrist3 { get; set; }`: 4x4 transformation matrix of the wrist3 (Tool) joint 6

## Inverse kinematics

`InverseKinematics` takes the 4x4 transform of the flange and returns up to 8 solutions, of 6 joint positions each. `GetNearestSolution` picks the solution nearest to a reference, usually the current joint positions. The solutions close to a singularity are included.

```csharp
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.Kinematics;

class KinematicsInverse
{
  static void Main(string[] args)
  {
    IUrDhParameters dh = KinematicsUtils.GetDhParametersFromModel(RobotModelsExtended.UR5e);

    // Target of the flange: X, Y, Z in m, rotation vector in rad
    var target = new Pose(0.4, -0.1, 0.3, 0, 3.14, 0);

    // Up to 8 solutions, 6 joint positions in radians each
    double[][] solutions = KinematicsUtils.InverseKinematics(target.FromRotationVectorTo4x4Matrix(), dh);

    // The solution nearest to the current joint positions
    double[] current = { 0, -1.57, 1.57, -1.57, -1.57, 0 };
    double[] nearest = KinematicsUtils.GetNearestSolution(solutions, current);
  }
}
```

## Singularities

Near a singularity, the robot loses a degree of freedom: a small move of the tool needs a large move of a joint, and the inverse kinematics has no unique answer. `GetSingularity` returns the singularities near a set of joint positions: `Wrist`, `Elbow`, `Shoulder`, or `None`.

```csharp
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.Kinematics;

class KinematicsSingularity
{
  static void Main(string[] args)
  {
    IUrDhParameters dh = KinematicsUtils.GetDhParametersFromModel(RobotModelsExtended.UR5e);

    // Joint positions in radians
    double q2 = -1.57; // shoulder
    double q3 = 0.0;   // elbow
    double q4 = -1.57; // wrist 1
    double q5 = 1.57;  // wrist 2

    // The 4 joint positions are given in the order q2, q3, q4, q5
    SingularityType singularity = KinematicsUtils.GetSingularity(q2, q3, q4, q5, dh);

    // Flags: Wrist, Elbow, Shoulder, or None
    if (singularity != SingularityType.None)
      Console.WriteLine("Close to a singularity: " + singularity);
  }
}
```

**SingularityType** ([reference](../api/UnderAutomation.UniversalRobots.Kinematics.md#singularitytype))

- Elbow: Elbow singularity
- None: No singularity
- Shoulder: Shoulder singularity
- Wrist: Wrist singularity

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**KinematicsUtils** ([reference](../api/UnderAutomation.UniversalRobots.Kinematics.md#kinematicsutils))

- `static double[,] DHTransform(double theta, double d, double a, double alpha)`: Computes the 4×4 Denavit-Hartenberg homogeneous transformation matrix for one joint.
- `static KinematicsResult ForwardKinematics(double[] jointAnglesRad, IUrDhParameters dhParameters)`: Forward kinematics : compute tool transform and intermediate transforms from joint angles (radians) and DH parameters.
- `static IUrDhParameters GetDhParametersFromModel(RobotModelsExtended model)`: Returns the factory Denavit-Hartenberg parameters for a given UR robot model.
- `static double[] GetNearestSolution(double[][] jointSolutions, double[] jointReference)`: Pick the solution nearest to a reference joint vector (L1 distance). Null if invalid inputs.
- `static SingularityType GetSingularity(double elbow, double shoulder, double wrist1, double wrist2, IUrDhParameters dhParameters)`: Detects singularities using Jacobian determinant factors: sin(q5)≈0 (wrist), sin(q3)≈0 (elbow), and c2·a2 + c23·a3 + s234·d5 ≈ 0 (shoulder).
- `static double[,] HomogeneousMultiply(double[,] A, double[,] B)`: Multiplies two 4×4 homogeneous transformation matrices, optimized for DH transforms.
- `static double[][] InverseKinematics(double[,] toolTransform, IUrDhParameters dhParameters)`: Analytical inverse kinematics Returns a list of candidate joint vectors; filters out singularities.

## Implementation

The solver is analytical (closed form), with the standard DH convention and the sequence of Chen et al., IEEE ICASI 2017. The forward kinematics is the product of the 6 homogeneous transforms of the joints. The inverse kinematics solves q1, then q5, q6, the sum q2 + q3 + q4, then q2, and q3 and q4 last. The singularities are detected from the factors of the determinant of the Jacobian: sin(q5) for the wrist, sin(q3) for the elbow, and a2·cos(q2) + a3·cos(q2 + q3) + d5·sin(q2 + q3 + q4) for the shoulder.

Reference: Chen et al., IEEE ICASI 2017, [IEEE Xplore](https://ieeexplore.ieee.org/document/7988522).
