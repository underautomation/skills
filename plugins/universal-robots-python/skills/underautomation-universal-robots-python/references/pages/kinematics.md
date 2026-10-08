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

```python
from underautomation.universal_robots.kinematics.kinematics_utils import KinematicsUtils
from underautomation.universal_robots.kinematics.custom_ur_dh_parameters import CustomUrDhParameters
from underautomation.universal_robots.common.robot_models_extended import RobotModelsExtended

# Nominal DH parameters of a model
ur5e = KinematicsUtils.get_dh_parameters_from_model(RobotModelsExtended.UR5e)

# Or your own values, in meters: a2, a3, d1, d4, d5, d6
custom = CustomUrDhParameters(-0.425, -0.3922, 0.1625, 0.1333, 0.0997, 0.0996)
```

### Parameters of a connected robot

The Primary Interface sends the DH parameters of the robot, with its calibration, in `KinematicsInfo` and `ConfigurationData`. Both implement `IUrDhParameters`.

```python
import time
from underautomation.universal_robots.ur import UR

robot = UR()

# The Primary Interface is enabled by default
robot.connect("192.168.0.1")

# Wait for the first packages (10 Hz)
time.sleep(0.5)

# DH parameters of this robot, with its calibration
dh = robot.primary_interface.kinematics_info

# Current joint positions, in radians
j = robot.primary_interface.joint_data
joints = [j.base.position, j.shoulder.position, j.elbow.position,
          j.wrist1.position, j.wrist2.position, j.wrist3.position]

# Current position of the tool center point
pose = robot.primary_interface.cartesian_info.as_pose()
```

**IUrDhParameters** ([reference](../api/underautomation.universal_robots.common.md#iurdhparameters))

- `a2: float (read only)`: DH parameter a2 (Shoulder)
- `a3: float (read only)`: DH parameter a3 (Elbow)
- `d1: float (read only)`: DH parameter d1 (Base)
- `d4: float (read only)`: DH parameter d4 (Wrist1)
- `d5: float (read only)`: DH parameter d5 (Wrist2)
- `d6: float (read only)`: DH parameter d6 (Wrist3/Tool)

## Forward kinematics

`ForwardKinematics` takes 6 joint positions in radians. `ToolTransform` is the 4x4 transform of the flange in the base frame: `Pose.From4x4MatrixToRotationVector` converts it to a pose in meters and radians. Add the TCP offset of your tool to get the position of the tool center point.

```python
from underautomation.universal_robots.kinematics.kinematics_utils import KinematicsUtils
from underautomation.universal_robots.common.robot_models_extended import RobotModelsExtended
from underautomation.universal_robots.common.pose import Pose

dh = KinematicsUtils.get_dh_parameters_from_model(RobotModelsExtended.UR5e)

# Joint positions in radians: base, shoulder, elbow, wrist 1, wrist 2, wrist 3
joints = [0, -1.57, 1.57, -1.57, -1.57, 0]

result = KinematicsUtils.forward_kinematics(joints, dh)

# 4x4 transform of the flange, as a pose: X, Y, Z in m, rotation vector in rad
flange = Pose.from4x4_matrix_to_rotation_vector(result.tool_transform)
print(flange.x, flange.y, flange.z)

# Transform of each joint, alone and composed with the previous ones
local = result.individual_local_transforms
cumulated = result.cumulative_global_transforms
```

`IndividualLocalTransforms` gives the transform of each joint alone, and `CumulativeGlobalTransforms` the transform of each joint composed with the previous ones.

**KinematicsResult** ([reference](../api/underautomation.universal_robots.kinematics.md#kinematicsresult))

- `KinematicsResult()`
- `tool_transform: typing.List[float]`: 4x4 transformation matrix of the tool
- `individual_local_transforms: TransformationSet`: Individual local transformation matrices of each joint
- `cumulative_global_transforms: TransformationSet`: Cumulative global transformation matrices of each joint

**TransformationSet** ([reference](../api/underautomation.universal_robots.kinematics.md#transformationset))

- `TransformationSet()`
- `base: typing.List[float]`: 4x4 transformation matrix of the base joint 1
- `shoulder: typing.List[float]`: 4x4 transformation matrix of the shoulder joint 2
- `elbow: typing.List[float]`: 4x4 transformation matrix of the elbow joint 3
- `wrist1: typing.List[float]`: 4x4 transformation matrix of the wrist1 joint 4
- `wrist2: typing.List[float]`: 4x4 transformation matrix of the wrist2 joint 5
- `wrist3: typing.List[float]`: 4x4 transformation matrix of the wrist3 (Tool) joint 6

## Inverse kinematics

`InverseKinematics` takes the 4x4 transform of the flange and returns up to 8 solutions, of 6 joint positions each. `GetNearestSolution` picks the solution nearest to a reference, usually the current joint positions. The solutions close to a singularity are included.

```python
from underautomation.universal_robots.kinematics.kinematics_utils import KinematicsUtils
from underautomation.universal_robots.common.robot_models_extended import RobotModelsExtended
from underautomation.universal_robots.common.pose import Pose

dh = KinematicsUtils.get_dh_parameters_from_model(RobotModelsExtended.UR5e)

# Target of the flange: X, Y, Z in m, rotation vector in rad
target = Pose(0.4, -0.1, 0.3, 0, 3.14, 0)

# Up to 8 solutions, 6 joint positions in radians each
solutions = KinematicsUtils.inverse_kinematics(target.from_rotation_vector_to4x4_matrix(), dh)

# The solution nearest to the current joint positions
current = [0, -1.57, 1.57, -1.57, -1.57, 0]
nearest = KinematicsUtils.get_nearest_solution(solutions, current)
print(list(nearest))
```

## Singularities

Near a singularity, the robot loses a degree of freedom: a small move of the tool needs a large move of a joint, and the inverse kinematics has no unique answer. `GetSingularity` returns the singularities near a set of joint positions: `Wrist`, `Elbow`, `Shoulder`, or `None`.

```python
from underautomation.universal_robots.kinematics.kinematics_utils import KinematicsUtils
from underautomation.universal_robots.kinematics.singularity_type import SingularityType
from underautomation.universal_robots.common.robot_models_extended import RobotModelsExtended

dh = KinematicsUtils.get_dh_parameters_from_model(RobotModelsExtended.UR5e)

# Joint positions in radians
q2 = -1.57  # shoulder
q3 = 0.0    # elbow
q4 = -1.57  # wrist 1
q5 = 1.57   # wrist 2

# The 4 joint positions are given in the order q2, q3, q4, q5
singularity = KinematicsUtils.get_singularity(q2, q3, q4, q5, dh)

# Flags: Wrist, Elbow, Shoulder, or None
if singularity != SingularityType.None_:
    print("Close to a singularity:", singularity)
```

**SingularityType** ([reference](../api/underautomation.universal_robots.kinematics.md#singularitytype))

- None_: No singularity
- Wrist: Wrist singularity
- Elbow: Elbow singularity
- Shoulder: Shoulder singularity

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**KinematicsUtils** ([reference](../api/underautomation.universal_robots.kinematics.md#kinematicsutils))

- `static dh_transform(theta: float, d: float, a: float, alpha: float) -> typing.List[float]`: Computes the 4×4 Denavit-Hartenberg homogeneous transformation matrix for one joint.
- `static homogeneous_multiply(A: typing.List[float], B: typing.List[float]) -> typing.List[float]`: Multiplies two 4×4 homogeneous transformation matrices, optimized for DH transforms.
- `static forward_kinematics(jointAnglesRad: typing.List[float], dhParameters: IUrDhParameters) -> KinematicsResult`: Forward kinematics : compute tool transform and intermediate transforms from joint angles (radians) and DH parameters.
- `static get_nearest_solution(jointSolutions: typing.List[float], jointReference: typing.List[float]) -> typing.List[float]`: Pick the solution nearest to a reference joint vector (L1 distance). Null if invalid inputs.
- `static inverse_kinematics(toolTransform: typing.List[float], dhParameters: IUrDhParameters) -> typing.List[float]`: Analytical inverse kinematics Returns a list of candidate joint vectors; filters out singularities.
- `static get_singularity(elbow: float, shoulder: float, wrist1: float, wrist2: float, dhParameters: IUrDhParameters) -> SingularityType`: Detects singularities using Jacobian determinant factors: sin(q5)≈0 (wrist), sin(q3)≈0 (elbow), and c2·a2 + c23·a3 + s234·d5 ≈ 0 (shoulder).
- `static get_dh_parameters_from_model(model: RobotModelsExtended) -> IUrDhParameters`: Returns the factory Denavit-Hartenberg parameters for a given UR robot model.

## Implementation

The solver is analytical (closed form), with the standard DH convention and the sequence of Chen et al., IEEE ICASI 2017. The forward kinematics is the product of the 6 homogeneous transforms of the joints. The inverse kinematics solves q1, then q5, q6, the sum q2 + q3 + q4, then q2, and q3 and q4 last. The singularities are detected from the factors of the determinant of the Jacobian: sin(q5) for the wrist, sin(q3) for the elbow, and a2·cos(q2) + a3·cos(q2 + q3) + d5·sin(q2 + q3 + q4) for the shoulder.

Reference: Chen et al., IEEE ICASI 2017, [IEEE Xplore](https://ieeexplore.ieee.org/document/7988522).
