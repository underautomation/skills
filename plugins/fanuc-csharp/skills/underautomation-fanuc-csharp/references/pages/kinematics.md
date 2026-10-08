# Forward & Inverse Kinematics

Perform forward and inverse kinematics calculations offline for FANUC industrial robots and CRX cobots using DH parameters.

Web page: https://underautomation.com/fanuc/documentation/kinematics

This page shows how to compute the forward and inverse kinematics of FANUC industrial arms and CRX cobots with the Fanuc SDK, offline or with the controller. Inverse kinematics (IK) and forward kinematics (FK) let you move between joint space and Cartesian space. FK computes the tool pose from known joint angles, while IK finds joint angles for a desired pose. The kinematics utilities in the Fanuc SDK are **offline helpers**: you can evaluate poses and joint solutions without connecting to a controller, for simulation, path validation and checks before deployment.

## Industrial arms and cobots

### Two solvers

The SDK has two analytical solvers and chooses the right one:

- **OPW industrial arms**: Classical 6-axis Fanuc robots with an ortho-parallel base and spherical wrist, based on the paper `An Analytical Solution of the Inverse Kinematics Problem of Industrial Serial Manipulators with an Ortho-parallel Basis and a Spherical Wrist` by Mathias Brandstötter, Arthur Angerer, and Michael Hofbaur.
- **CRX collaborative arms**: Fanuc CRX cobots that have their own closed-form solver and optional dual solutions, based on paper `Geometric Approach for Inverse Kinematics of the FANUC CRX Collaborative Robot` by Manel Abbes and Gérard Poisson.

### Choice of the solver

`KinematicsUtils.InverseKinematics()` reads `DhParameters.KinematicsCategory`:

- `KinematicsCategory.Opw`: it calls `Opw.OpwKinematicsUtils.InverseKinematics` (industrial robots).
- `KinematicsCategory.Crx`: it calls `Crx.CrxKinematicsUtils.InverseKinematics` (CRX cobots).

So one entry point covers every arm.

## Offline kinematics

### Run forward kinematics (FK)

```csharp
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Kinematics;

public class KinematicsFK
{
    static void Main()
    {
        // Load robot geometry
        var dh = DhParameters.FromArmKinematicModel(ArmKinematicModels.CRX10iA);

        // Joint angles in degrees (Fanuc convention)
        var jointsDeg = new JointsPosition { J1 = 0, J2 = -30, J3 = 45, J4 = 0, J5 = 60, J6 = 90 };

        // Compute pose: returns XYZ + WPR
        CartesianPosition pose = KinematicsUtils.ForwardKinematics(jointsDeg, dh);
    }
}
```

### Solve inverse kinematics (IK) for an OPW robot

```csharp
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Kinematics;
using UnderAutomation.Fanuc.Kinematics.Crx;

public class KinematicsIK
{
    static void Main()
    {
        // OPW industrial robot
        var dh = DhParameters.FromArmKinematicModel(ArmKinematicModels.ARCMate120iD);
        var target = new CartesianPosition { X = 800, Y = 0, Z = 450, W = 180, P = 0, R = 90 };
        JointsPosition[] solutions = KinematicsUtils.InverseKinematics(target, dh);

        // CRX cobot with dual solutions
        var dhCrx = DhParameters.FromArmKinematicModel(ArmKinematicModels.CRX10iAL);
        var targetCrx = new CartesianPosition { X = 400, Y = 250, Z = 650, W = 0, P = 90, R = 0 };
        JointsPosition[] crxSolutions = CrxKinematicsUtils.InverseKinematics(
            targetCrx, dhCrx,
            includeDuals: true
        );
    }
}
```

### Solve inverse kinematics (IK) for a CRX cobot

The CRX solver uses a closed-form geometric approach and returns all valid joint solutions directly. No seed position is required. Pass `includeDuals: true` (C#) or `include_duals=True` (Python) to also include the dual configurations defined by the CRX kinematics.

```csharp
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Kinematics;
using UnderAutomation.Fanuc.Kinematics.Crx;

public class KinematicsIK
{
    static void Main()
    {
        // OPW industrial robot
        var dh = DhParameters.FromArmKinematicModel(ArmKinematicModels.ARCMate120iD);
        var target = new CartesianPosition { X = 800, Y = 0, Z = 450, W = 180, P = 0, R = 90 };
        JointsPosition[] solutions = KinematicsUtils.InverseKinematics(target, dh);

        // CRX cobot with dual solutions
        var dhCrx = DhParameters.FromArmKinematicModel(ArmKinematicModels.CRX10iAL);
        var targetCrx = new CartesianPosition { X = 400, Y = 250, Z = 650, W = 0, P = 90, R = 0 };
        JointsPosition[] crxSolutions = CrxKinematicsUtils.InverseKinematics(
            targetCrx, dhCrx,
            includeDuals: true
        );
    }
}
```

### Build DH parameters from multiple sources

- **Built-in catalog**: `DhParameters.FromArmKinematicModel(ArmKinematicModels model)` gives the geometry of many Fanuc arms and cobots.
- **ROBOGUIDE library**: `DhParameters.FromDefFile(path)` parses robot definitions in `ProgramData/FANUC/ROBOGUIDE/Robot Library`.
- **Controller variables**: `DhParameters.FromSymotnFile` and `DhParameters.FromMrrGrp` convert live `$MRR_GRP` or `symotn.va` data to reusable DH structures.
- **OPW data**: `DhParameters.FromOpwParameters` maps OPW parameters (meters) to Fanuc-style DH while keeping the kinematics category consistent.

## Tips

- **Offline**: the solvers need no controller and no connection.
- **Pose normalization**: `OpwKinematicsUtils.InverseKinematics` normalizes angles to `(-180, 180]` to match Fanuc expectations.
- **CRX dual solutions**: Pass `includeDuals: true` to `CrxKinematicsUtils.InverseKinematics` to include the additional configurations defined by the CRX kinematics model.
- **Matrix helpers**: `KinematicsUtils.Mul` multiplies 2D matrices if you need to compose transforms manually.

## Kinematics on the controller

With a connection, the controller can compute the kinematics, without DH parameters. The controller keeps the joint and the Cartesian form of every position register. Write a position in one form with SNPX, then read the same register back to get the other form.

### Forward kinematics using SNPX position registers

Write joint angles and read back the Cartesian pose:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class KinematicsOnline
{
    static void Main()
    {
        FanucRobot _robot = new FanucRobot();
        _robot.Connect("192.168.0.1");

        // Forward kinematics via SNPX: joints → Cartesian
        JointsPosition jointsPosition = new JointsPosition(10, 12, 50, 20, 12, 16);
        _robot.Snpx.PositionRegisters.Write(1, jointsPosition);
        CartesianPosition cartesianPosition = _robot.Snpx.PositionRegisters.Read(1).CartesianPosition;

        // Inverse kinematics via SNPX: Cartesian → joints
        CartesianPosition targetPosition = new CartesianPosition() { X = 100, Y = 100, Z = 100 };
        targetPosition.Configuration.WristFlip = WristFlip.Flip;
        targetPosition.Configuration.ArmUpDown = ArmUpDown.Down;
        targetPosition.Configuration.ArmLeftRight = ArmLeftRight.Left;
        _robot.Snpx.PositionRegisters.Write(1, targetPosition);
        JointsPosition resultJoints = _robot.Snpx.PositionRegisters.Read(1).JointsPosition;
    }
}
```

### Inverse kinematics using SNPX position registers

Write a Cartesian pose and read back the joint angles. There is only one solution, because the Cartesian position contains the configuration.

## Demonstration

### Online 3D tool

[fanuc-kinematics.underautomation.com](https://fanuc-kinematics.underautomation.com) is a 3D page to try the forward and inverse kinematics of the FANUC arms and cobots.

![Fanuc Robot Simulator](https://raw.githubusercontent.com/underautomation/fanuc-kinematics.underautomation.com/refs/heads/main/.github/assets/screenshot.gif)

### Demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**KinematicsUtils** ([reference](../api/UnderAutomation.Fanuc.Kinematics.md#kinematicsutils))

- `static CartesianPosition ForwardKinematics(double[] jointAnglesRad, DhParameters dhParameters)`: Compute FK for given joint angles (rad) and DH parameters
- `static CartesianPosition ForwardKinematics(JointsPosition jointAnglesDeg, DhParameters parameters)`: Compute FK for given joint angles (deg) and DH parameters
- `static JointsPosition[] InverseKinematics(CartesianPosition position, DhParameters parameters)`: Compute all inverse kinematics solutions for a desired end effector pose.
- `static double[,] Mul(double[,] A, double[,] B)`: Multiply two 4x4 homogeneous transformation matrices.

**DhParameters** ([reference](../api/UnderAutomation.Fanuc.Kinematics.md#dhparameters))

- `DhParameters()`: Initializes a new empty instance of Kinematics.DhParameters.
- `DhParameters(double d4, double d5, double d6, double a1, double a2, double a3)`: Initializes a new instance of Kinematics.DhParameters with the specified values.
- `DhParameters(IDhParameters parameters)`: Initializes a new instance of Kinematics.DhParameters by copying from an existing Kinematics.IDhParameters.
- `double A1 { get; set; }`: DH parameter A1 (mm).
- `double A2 { get; set; }`: DH parameter A2 (mm).
- `double A3 { get; set; }`: DH parameter A3 (mm).
- `double D4 { get; set; }`: DH parameter D4 (mm).
- `double D5 { get; set; }`: DH parameter D5 (mm).
- `double D6 { get; set; }`: DH parameter D6 (mm).
- `static DhParameters FromArmKinematicModel(string modelName)`: Returns DH parameters from a known Arm Kinematic Model name. Returns null if not found in enum ArmKinematicModels.
- `static DhParameters FromArmKinematicModel(ArmKinematicModels model)`: Returns DH parameters from a known Arm Kinematic Model.
- `static DhParameters[] FromDefFile(string path)`: Loads DH parameters of each robots described in a ROBOGUIDE definition file (*.def). By default, this file is located in "C:\ProgramData\FANUC\ROBOGUIDE\Robot Library".
- `static DhParameters[] FromDefFile(XDocument doc)`: Loads DH parameters of each robots described in a ROBOGUIDE definition file (*.def). By default, this file is located in "C:\ProgramData\FANUC\ROBOGUIDE\Robot Library".
- `static DhParameters FromMrrGrp(MrrGrpVariableType mrrGrp)`: Loads DH parameters from parsed variable $MRR_GRP located in symotn.va.
- `static DhParameters FromOpwParameters(double a1, double a2, double c2, double c3, double c4)`: Creates DH parameters from OPW parameters (in meters) C1 and B are ignored because B is always 0 and C1 is not used in the DH representation.
- `static DhParameters[] FromSymotnFile(SymotnFile file)`: Loads DH parameters of each group from a parsed symotn.va file.
- `KinematicsCategory KinematicsCategory { get; }`: Gets the kinematics category determined from the DH parameter values.
- `object Tag`: User-defined tag for associating additional data with this instance.

**KinematicsCategory** ([reference](../api/UnderAutomation.Fanuc.Kinematics.md#kinematicscategory))

- Crx: CRX collaborative robot kinematics.
- Invalid: Invalid or unsupported kinematics configuration.
- Opw: OPW (ortho-parallel wrist) kinematics for standard industrial robots.

**IDhParameters** ([reference](../api/UnderAutomation.Fanuc.Kinematics.md#idhparameters))

- `double A1 { get; }`: DH parameter A1 (mm).
- `double A2 { get; }`: DH parameter A2 (mm).
- `double A3 { get; }`: DH parameter A3 (mm).
- `double D4 { get; }`: DH parameter D4 (mm).
- `double D5 { get; }`: DH parameter D5 (mm).
- `double D6 { get; }`: DH parameter D6 (mm).

**JointsPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#jointsposition-robotstreammotionqueueendjointposition))

- `JointsPosition()`: Default constructor
- `JointsPosition(double j1Deg, double j2Deg, double j3Deg, double j4Deg, double j5Deg, double j6Deg)`: Constructor with 6 joint values in degrees
- `JointsPosition(double j1Deg, double j2Deg, double j3Deg, double j4Deg, double j5Deg, double j6Deg, double j7Deg, double j8Deg, double j9Deg)`: Constructor with 9 joint values in degrees
- `JointsPosition(double[] values)`: Constructor from an array of joint values in degrees
- `static bool IsNear(JointsPosition j1, JointsPosition j2, double degreesTolerance)`: Check if joints position is near to expected joints position with a tolerance value
- `double this[int i] { get; set; }`: Gets or sets the joint value at the specified index
- `double J1 { get; set; }`: Joint 1 in degrees
- `double J2 { get; set; }`: Joint 2 in degrees
- `double J3 { get; set; }`: Joint 3 in degrees
- `double J4 { get; set; }`: Joint 4 in degrees
- `double J5 { get; set; }`: Joint 5 in degrees
- `double J6 { get; set; }`: Joint 6 in degrees
- `double J7 { get; set; }`: Joint 7 in degrees
- `double J8 { get; set; }`: Joint 8 in degrees
- `double J9 { get; set; }`: Joint 9 in degrees
- `double[] Values { get; }`: Numeric values for each joints

**CartesianPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#cartesianposition-robotstreammotionqueueendcartesianposition))

- `CartesianPosition()`: Default constructor
- `CartesianPosition(double x, double y, double z, double w, double p, double r)`: Constructor with position and rotations
- `CartesianPosition(double x, double y, double z, double w, double p, double r, Configuration configuration)`: Constructor with position, rotations and configuration
- `CartesianPosition(CartesianPosition position)`: Copy constructor
- `CartesianPosition(XYZPosition position, double w, double p, double r)`: Constructor from an XYZ position with rotations
- `Configuration Configuration { get; set; }`: Position configuration
- `static CartesianPosition FromHomogeneousMatrix(double[,] R)`: Create a CartesianPosition with unknow configuration from a homogeneous rotation and translation 4x4 matrix
- `static bool IsNear(CartesianPosition a, CartesianPosition b, double mmTolerance, double degreesTolerance)`: Check if two Cartesian positions are near each other within specified tolerances
- `static double NormalizeAngle(double angle)`: Normalize an angle to the range ]-180, 180]
- `static void NormalizeAngles(CartesianPosition pose)`: Normalize the W, P, R angles to the range ]-180, 180]
- Inherited from [XYZWPRPosition](../api/UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](../api/UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`
