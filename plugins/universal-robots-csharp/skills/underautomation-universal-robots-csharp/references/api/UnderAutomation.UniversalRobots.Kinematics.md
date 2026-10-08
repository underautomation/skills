# UnderAutomation.UniversalRobots.Kinematics

## CustomUrDhParameters

`class CustomUrDhParameters : IUrDhParameters`

Mutable Denavit-Hartenberg parameters for a Universal Robots arm, allowing custom DH values.

- `CustomUrDhParameters(double a2, double a3, double d1, double d4, double d5, double d6)`: Creates a new instance with the specified DH parameters.
- `CustomUrDhParameters(IUrDhParameters parameters)`: Creates a new instance by copying values from an existing Common.IUrDhParameters instance.
- `double A2 { get; set; }`: DH parameter a2 (shoulder link length) in meters.
- `double A3 { get; set; }`: DH parameter a3 (elbow link length) in meters.
- `double D1 { get; set; }`: DH parameter d1 (base height offset) in meters.
- `double D4 { get; set; }`: DH parameter d4 (wrist 1 offset) in meters.
- `double D5 { get; set; }`: DH parameter d5 (wrist 2 offset) in meters.
- `double D6 { get; set; }`: DH parameter d6 (wrist 3 / tool offset) in meters.

## KinematicsResult

`class KinematicsResult`

Result of a forward kinematics calculation

- `KinematicsResult()`
- `TransformationSet CumulativeGlobalTransforms { get; set; }`: Cumulative global transformation matrices of each joint
- `TransformationSet IndividualLocalTransforms { get; set; }`: Individual local transformation matrices of each joint
- `double[,] ToolTransform { get; set; }`: 4x4 transformation matrix of the tool

## KinematicsUtils

`static class KinematicsUtils`

========================================================================================================= Implementation notes : --------------------------------------------------------------------------------------------------------- This class implements forward and inverse kinematics for a 6-D...

- `static double[,] DHTransform(double theta, double d, double a, double alpha)`: Computes the 4×4 Denavit-Hartenberg homogeneous transformation matrix for one joint.
- `static KinematicsResult ForwardKinematics(double[] jointAnglesRad, IUrDhParameters dhParameters)`: Forward kinematics : compute tool transform and intermediate transforms from joint angles (radians) and DH parameters.
- `static IUrDhParameters GetDhParametersFromModel(RobotModelsExtended model)`: Returns the factory Denavit-Hartenberg parameters for a given UR robot model.
- `static double[] GetNearestSolution(double[][] jointSolutions, double[] jointReference)`: Pick the solution nearest to a reference joint vector (L1 distance). Null if invalid inputs.
- `static SingularityType GetSingularity(double elbow, double shoulder, double wrist1, double wrist2, IUrDhParameters dhParameters)`: Detects singularities using Jacobian determinant factors: sin(q5)≈0 (wrist), sin(q3)≈0 (elbow), and c2·a2 + c23·a3 + s234·d5 ≈ 0 (shoulder).
- `static double[,] HomogeneousMultiply(double[,] A, double[,] B)`: Multiplies two 4×4 homogeneous transformation matrices, optimized for DH transforms.
- `static double[][] InverseKinematics(double[,] toolTransform, IUrDhParameters dhParameters)`: Analytical inverse kinematics Returns a list of candidate joint vectors; filters out singularities.

## SingularityType

`enum SingularityType`

Types of singularities

- Elbow: Elbow singularity
- None: No singularity
- Shoulder: Shoulder singularity
- Wrist: Wrist singularity

## TransformationSet

`class TransformationSet`

Set of transformation matrices for each joint

- `TransformationSet()`
- `double[,] Base { get; set; }`: 4x4 transformation matrix of the base joint 1
- `double[,] Elbow { get; set; }`: 4x4 transformation matrix of the elbow joint 3
- `double[,] Shoulder { get; set; }`: 4x4 transformation matrix of the shoulder joint 2
- `double[,] Wrist1 { get; set; }`: 4x4 transformation matrix of the wrist1 joint 4
- `double[,] Wrist2 { get; set; }`: 4x4 transformation matrix of the wrist2 joint 5
- `double[,] Wrist3 { get; set; }`: 4x4 transformation matrix of the wrist3 (Tool) joint 6

## Ur10DhParameters

`class Ur10DhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR10 robot (CB-Series).

- `Ur10DhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur10eDhParameters

`class Ur10eDhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR10e robot (e-Series).

- `Ur10eDhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur12eDhParameters

`class Ur12eDhParameters : Ur10eDhParameters, IUrDhParameters`

Denavit-Hartenberg parameters for the UR12e robot (e-Series). Shares the same DH values as the UR10e.

- `Ur12eDhParameters()`
- Inherited from [Ur10eDhParameters](UnderAutomation.UniversalRobots.Kinematics.md#ur10edhparameters): `A2`, `A3`, `D1`, `D4`, `D5`, `D6`

## Ur15DhParameters

`class Ur15DhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR15 robot.

- `Ur15DhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur16eDhParameters

`class Ur16eDhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR16e robot (e-Series).

- `Ur16eDhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur18DhParameters

`class Ur18DhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR18 robot.

- `Ur18DhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur20DhParameters

`class Ur20DhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR20 robot.

- `Ur20DhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur30DhParameters

`class Ur30DhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR30 robot.

- `Ur30DhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur3DhParameters

`class Ur3DhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR3 robot (CB-Series).

- `Ur3DhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur3eDhParameters

`class Ur3eDhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR3e robot (e-Series).

- `Ur3eDhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur5DhParameters

`class Ur5DhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR5 robot (CB-Series).

- `Ur5DhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur5eDhParameters

`class Ur5eDhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR5e robot (e-Series).

- `Ur5eDhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## Ur7eDhParameters

`class Ur7eDhParameters : Ur5eDhParameters, IUrDhParameters`

Denavit-Hartenberg parameters for the UR7e robot (e-Series). Shares the same DH values as the UR5e.

- `Ur7eDhParameters()`
- Inherited from [Ur5eDhParameters](UnderAutomation.UniversalRobots.Kinematics.md#ur5edhparameters): `A2`, `A3`, `D1`, `D4`, `D5`, `D6`

## Ur8LongDhParameters

`class Ur8LongDhParameters : IUrDhParameters`

Denavit-Hartenberg parameters for the UR8 Long robot.

- `Ur8LongDhParameters()`
- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)
