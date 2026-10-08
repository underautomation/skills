# underautomation.universal_robots.kinematics

## CustomUrDhParameters

`from underautomation.universal_robots.kinematics.custom_ur_dh_parameters import CustomUrDhParameters`

Mutable Denavit-Hartenberg parameters for a Universal Robots arm, allowing custom DH values.

- `CustomUrDhParameters(a2: float, a3: float, d1: float, d4: float, d5: float, d6: float)`: Creates a new instance with the specified DH parameters.
- `a2: float`: DH parameter a2 (shoulder link length) in meters.
- `a3: float`: DH parameter a3 (elbow link length) in meters.
- `d1: float`: DH parameter d1 (base height offset) in meters.
- `d4: float`: DH parameter d4 (wrist 1 offset) in meters.
- `d5: float`: DH parameter d5 (wrist 2 offset) in meters.
- `d6: float`: DH parameter d6 (wrist 3 / tool offset) in meters.

## KinematicsResult

`from underautomation.universal_robots.kinematics.kinematics_result import KinematicsResult`

Result of a forward kinematics calculation

- `KinematicsResult()`
- `tool_transform: typing.List[float]`: 4x4 transformation matrix of the tool
- `individual_local_transforms: TransformationSet`: Individual local transformation matrices of each joint
- `cumulative_global_transforms: TransformationSet`: Cumulative global transformation matrices of each joint

## KinematicsUtils

`from underautomation.universal_robots.kinematics.kinematics_utils import KinematicsUtils`

========================================================================================================= Implementation notes : --------------------------------------------------------------------------------------------------------- This class implements forward and inverse kinematics for a 6-D...

- `static dh_transform(theta: float, d: float, a: float, alpha: float) -> typing.List[float]`: Computes the 4×4 Denavit-Hartenberg homogeneous transformation matrix for one joint.
- `static homogeneous_multiply(A: typing.List[float], B: typing.List[float]) -> typing.List[float]`: Multiplies two 4×4 homogeneous transformation matrices, optimized for DH transforms.
- `static forward_kinematics(jointAnglesRad: typing.List[float], dhParameters: IUrDhParameters) -> KinematicsResult`: Forward kinematics : compute tool transform and intermediate transforms from joint angles (radians) and DH parameters.
- `static get_nearest_solution(jointSolutions: typing.List[float], jointReference: typing.List[float]) -> typing.List[float]`: Pick the solution nearest to a reference joint vector (L1 distance). Null if invalid inputs.
- `static inverse_kinematics(toolTransform: typing.List[float], dhParameters: IUrDhParameters) -> typing.List[float]`: Analytical inverse kinematics Returns a list of candidate joint vectors; filters out singularities.
- `static get_singularity(elbow: float, shoulder: float, wrist1: float, wrist2: float, dhParameters: IUrDhParameters) -> SingularityType`: Detects singularities using Jacobian determinant factors: sin(q5)≈0 (wrist), sin(q3)≈0 (elbow), and c2·a2 + c23·a3 + s234·d5 ≈ 0 (shoulder).
- `static get_dh_parameters_from_model(model: RobotModelsExtended) -> IUrDhParameters`: Returns the factory Denavit-Hartenberg parameters for a given UR robot model.

## SingularityType

`from underautomation.universal_robots.kinematics.singularity_type import SingularityType`

Types of singularities

- None_: No singularity
- Wrist: Wrist singularity
- Elbow: Elbow singularity
- Shoulder: Shoulder singularity

## TransformationSet

`from underautomation.universal_robots.kinematics.transformation_set import TransformationSet`

Set of transformation matrices for each joint

- `TransformationSet()`
- `base: typing.List[float]`: 4x4 transformation matrix of the base joint 1
- `shoulder: typing.List[float]`: 4x4 transformation matrix of the shoulder joint 2
- `elbow: typing.List[float]`: 4x4 transformation matrix of the elbow joint 3
- `wrist1: typing.List[float]`: 4x4 transformation matrix of the wrist1 joint 4
- `wrist2: typing.List[float]`: 4x4 transformation matrix of the wrist2 joint 5
- `wrist3: typing.List[float]`: 4x4 transformation matrix of the wrist3 (Tool) joint 6

## Ur10DhParameters

`from underautomation.universal_robots.kinematics.ur10_dh_parameters import Ur10DhParameters`

Denavit-Hartenberg parameters for the UR10 robot (CB-Series).

- `Ur10DhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur10eDhParameters

`from underautomation.universal_robots.kinematics.ur10e_dh_parameters import Ur10eDhParameters`

Denavit-Hartenberg parameters for the UR10e robot (e-Series).

- `Ur10eDhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur12eDhParameters

`from underautomation.universal_robots.kinematics.ur12e_dh_parameters import Ur12eDhParameters`

Denavit-Hartenberg parameters for the UR12e robot (e-Series). Shares the same DH values as the UR10e.

- `Ur12eDhParameters()`
- Inherited from [Ur10eDhParameters](underautomation.universal_robots.kinematics.md#ur10edhparameters): `a2`, `a3`, `d1`, `d4`, `d5`, `d6`

## Ur15DhParameters

`from underautomation.universal_robots.kinematics.ur15_dh_parameters import Ur15DhParameters`

Denavit-Hartenberg parameters for the UR15 robot.

- `Ur15DhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur16eDhParameters

`from underautomation.universal_robots.kinematics.ur16e_dh_parameters import Ur16eDhParameters`

Denavit-Hartenberg parameters for the UR16e robot (e-Series).

- `Ur16eDhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur18DhParameters

`from underautomation.universal_robots.kinematics.ur18_dh_parameters import Ur18DhParameters`

Denavit-Hartenberg parameters for the UR18 robot.

- `Ur18DhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur20DhParameters

`from underautomation.universal_robots.kinematics.ur20_dh_parameters import Ur20DhParameters`

Denavit-Hartenberg parameters for the UR20 robot.

- `Ur20DhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur30DhParameters

`from underautomation.universal_robots.kinematics.ur30_dh_parameters import Ur30DhParameters`

Denavit-Hartenberg parameters for the UR30 robot.

- `Ur30DhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur3DhParameters

`from underautomation.universal_robots.kinematics.ur3_dh_parameters import Ur3DhParameters`

Denavit-Hartenberg parameters for the UR3 robot (CB-Series).

- `Ur3DhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur3eDhParameters

`from underautomation.universal_robots.kinematics.ur3e_dh_parameters import Ur3eDhParameters`

Denavit-Hartenberg parameters for the UR3e robot (e-Series).

- `Ur3eDhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur5DhParameters

`from underautomation.universal_robots.kinematics.ur5_dh_parameters import Ur5DhParameters`

Denavit-Hartenberg parameters for the UR5 robot (CB-Series).

- `Ur5DhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur5eDhParameters

`from underautomation.universal_robots.kinematics.ur5e_dh_parameters import Ur5eDhParameters`

Denavit-Hartenberg parameters for the UR5e robot (e-Series).

- `Ur5eDhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`

## Ur7eDhParameters

`from underautomation.universal_robots.kinematics.ur7e_dh_parameters import Ur7eDhParameters`

Denavit-Hartenberg parameters for the UR7e robot (e-Series). Shares the same DH values as the UR5e.

- `Ur7eDhParameters()`
- Inherited from [Ur5eDhParameters](underautomation.universal_robots.kinematics.md#ur5edhparameters): `a2`, `a3`, `d1`, `d4`, `d5`, `d6`

## Ur8LongDhParameters

`from underautomation.universal_robots.kinematics.ur8_long_dh_parameters import Ur8LongDhParameters`

Denavit-Hartenberg parameters for the UR8 Long robot.

- `Ur8LongDhParameters()`
- `a2: float (read only)`
- `a3: float (read only)`
- `d1: float (read only)`
- `d4: float (read only)`
- `d5: float (read only)`
- `d6: float (read only)`
