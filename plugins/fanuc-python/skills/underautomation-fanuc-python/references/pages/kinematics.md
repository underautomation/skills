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

```python
from underautomation.fanuc.kinematics.kinematics_utils import KinematicsUtils
from underautomation.fanuc.kinematics.dh_parameters import DhParameters
from underautomation.fanuc.common.joints_position import JointsPosition

# Load robot geometry
dh = DhParameters.from_arm_kinematic_model("CRX10iA")

# Joint angles in degrees (Fanuc convention)
joints_deg = JointsPosition(j1=0, j2=-30, j3=45, j4=0, j5=60, j6=90)

# Compute pose: returns XYZ + WPR
pose = KinematicsUtils.forward_kinematics(joints_deg, dh)
```

### Solve inverse kinematics (IK) for an OPW robot

```python
from underautomation.fanuc.kinematics.kinematics_utils import KinematicsUtils
from underautomation.fanuc.kinematics.dh_parameters import DhParameters
from underautomation.fanuc.common.cartesian_position import CartesianPosition

# OPW industrial robot
dh = DhParameters.from_arm_kinematic_model("ARCMate120iD")
target = CartesianPosition(x=800, y=0, z=450, w=180, p=0, r=90)
solutions = KinematicsUtils.inverse_kinematics(target, dh)

# CRX cobot with dual solutions
dh_crx = DhParameters.from_arm_kinematic_model("CRX10iAL")
target_crx = CartesianPosition(x=400, y=250, z=650, w=0, p=90, r=0)
crx_solutions = KinematicsUtils.inverse_kinematics(
    target_crx, dh_crx,
    include_duals=True
)
```

### Solve inverse kinematics (IK) for a CRX cobot

The CRX solver uses a closed-form geometric approach and returns all valid joint solutions directly. No seed position is required. Pass `includeDuals: true` (C#) or `include_duals=True` (Python) to also include the dual configurations defined by the CRX kinematics.

```python
from underautomation.fanuc.kinematics.kinematics_utils import KinematicsUtils
from underautomation.fanuc.kinematics.dh_parameters import DhParameters
from underautomation.fanuc.common.cartesian_position import CartesianPosition

# OPW industrial robot
dh = DhParameters.from_arm_kinematic_model("ARCMate120iD")
target = CartesianPosition(x=800, y=0, z=450, w=180, p=0, r=90)
solutions = KinematicsUtils.inverse_kinematics(target, dh)

# CRX cobot with dual solutions
dh_crx = DhParameters.from_arm_kinematic_model("CRX10iAL")
target_crx = CartesianPosition(x=400, y=250, z=650, w=0, p=90, r=0)
crx_solutions = KinematicsUtils.inverse_kinematics(
    target_crx, dh_crx,
    include_duals=True
)
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

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.common.joints_position import JointsPosition
from underautomation.fanuc.common.cartesian_position import CartesianPosition

robot = FanucRobot()
robot.connect("192.168.0.1")

# Forward kinematics via SNPX: joints → Cartesian
joints_position = JointsPosition(10, 12, 50, 20, 12, 16)
robot.snpx.position_registers.write(1, joints_position)
cartesian_position = robot.snpx.position_registers.read(1).cartesian_position

# Inverse kinematics via SNPX: Cartesian → joints
target_position = CartesianPosition(x=100, y=100, z=100)
target_position.configuration.wrist_flip = "Flip"
target_position.configuration.arm_up_down = "Down"
target_position.configuration.arm_left_right = "Left"
robot.snpx.position_registers.write(1, target_position)
result_joints = robot.snpx.position_registers.read(1).joints_position
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

**KinematicsUtils** ([reference](../api/underautomation.fanuc.kinematics.md#kinematicsutils))

- `static forward_kinematics(jointAnglesDeg_or_jointAnglesRad: typing.List[float] | JointsPosition, dhParameters_or_parameters: DhParameters) -> CartesianPosition`: Compute FK for given joint angles (rad) and DH parameters Compute FK for given joint angles (deg) and DH parameters
- `static inverse_kinematics(position: CartesianPosition, parameters: DhParameters) -> typing.List[JointsPosition]`: Compute all inverse kinematics solutions for a desired end effector pose.
- `static mul(A: typing.List[float], B: typing.List[float]) -> typing.List[float]`: Multiply two 4x4 homogeneous transformation matrices.

**DhParameters** ([reference](../api/underautomation.fanuc.kinematics.md#dhparameters))

- `DhParameters(d4: float, d5: float, d6: float, a1: float, a2: float, a3: float)`: Initializes a new instance of DhParameters with the specified values.
- `static from_arm_kinematic_model(model_or_modelName: str | ArmKinematicModels) -> 'DhParameters'`: Returns DH parameters from a known Arm Kinematic Model name. Returns null if not found in enum ArmKinematicModels. Returns DH parameters from a known Arm Kinematic Model.
- `static from_opw_parameters(a1: float, a2: float, c2: float, c3: float, c4: float) -> 'DhParameters'`: Creates DH parameters from OPW parameters (in meters) C1 and B are ignored because B is always 0 and C1 is not used in the DH representation.
- `static from_def_file(path: str) -> typing.List['DhParameters']`: Loads DH parameters of each robots described in a ROBOGUIDE definition file (*.def). By default, this file is located in "C:\ProgramData\FANUC\ROBOGUIDE\Robot Library".
- `static from_symotn_file(file: SymotnFile) -> typing.List['DhParameters']`: Loads DH parameters of each group from a parsed symotn.va file.
- `static from_mrr_grp(mrrGrp: MrrGrpVariableType) -> 'DhParameters'`: Loads DH parameters from parsed variable $MRR_GRP located in symotn.va.
- `d4: float`: DH parameter D4 (mm).
- `d5: float`: DH parameter D5 (mm).
- `d6: float`: DH parameter D6 (mm).
- `a1: float`: DH parameter A1 (mm).
- `a2: float`: DH parameter A2 (mm).
- `a3: float`: DH parameter A3 (mm).
- `kinematics_category: KinematicsCategory (read only)`: Gets the kinematics category determined from the DH parameter values.
- `tag: typing.Any`: User-defined tag for associating additional data with this instance.

**KinematicsCategory** ([reference](../api/underautomation.fanuc.kinematics.md#kinematicscategory))

- Invalid: Invalid or unsupported kinematics configuration.
- Crx: CRX collaborative robot kinematics.
- Opw: OPW (ortho-parallel wrist) kinematics for standard industrial robots.

**IDhParameters** ([reference](../api/underautomation.fanuc.kinematics.md#idhparameters))

- `d4: float (read only)`: DH parameter D4 (mm).
- `d5: float (read only)`: DH parameter D5 (mm).
- `d6: float (read only)`: DH parameter D6 (mm).
- `a1: float (read only)`: DH parameter A1 (mm).
- `a2: float (read only)`: DH parameter A2 (mm).
- `a3: float (read only)`: DH parameter A3 (mm).

**JointsPosition** ([reference](../api/underautomation.fanuc.common.md#jointsposition-robotstream_motionqueue_end_joint_position))

- `JointsPosition(j1Deg: float, j2Deg: float, j3Deg: float, j4Deg: float, j5Deg: float, j6Deg: float, j7Deg: float, j8Deg: float, j9Deg: float)`: Constructor with 9 joint values in degrees
- `static is_near(j1: 'JointsPosition', j2: 'JointsPosition', degreesTolerance: float) -> bool`: Check if joints position is near to expected joints position with a tolerance value
- `values: typing.List[float] (read only)`: Numeric values for each joints
- `j1: float`: Joint 1 in degrees
- `j2: float`: Joint 2 in degrees
- `j3: float`: Joint 3 in degrees
- `j4: float`: Joint 4 in degrees
- `j5: float`: Joint 5 in degrees
- `j6: float`: Joint 6 in degrees
- `j7: float`: Joint 7 in degrees
- `j8: float`: Joint 8 in degrees
- `j9: float`: Joint 9 in degrees

**CartesianPosition** ([reference](../api/underautomation.fanuc.common.md#cartesianposition-robotstream_motionqueue_end_cartesian_position))

- `CartesianPosition(x: float, y: float, z: float, w: float, p: float, r: float, configuration: Configuration)`: Constructor with position, rotations and configuration
- `static from_homogeneous_matrix(R: typing.List[float]) -> 'CartesianPosition'`: Create a CartesianPosition with unknow configuration from a homogeneous rotation and translation 4x4 matrix
- `static normalize_angle(angle: float) -> float`: Normalize an angle to the range ]-180, 180]
- `static normalize_angles(pose: 'CartesianPosition') -> None`: Normalize the W, P, R angles to the range ]-180, 180]
- `static is_near(a: 'CartesianPosition', b: 'CartesianPosition', mmTolerance: float, degreesTolerance: float) -> bool`: Check if two Cartesian positions are near each other within specified tolerances
- `configuration: Configuration`: Position configuration
- Inherited from [XYZWPRPosition](../api/underautomation.fanuc.common.md#xyzwprposition-robotstream_motionqueue_end_cartesian_position): `to_homogeneous_matrix`, `get_quaternion`, `set_quaternion`, `multiply`, `inverse`, `flange_to_tcp`, `tcp_to_flange`, `user_frame_to_world`, `world_to_user_frame`, `w`, `p`, `r`
- Inherited from [XYZPosition](../api/underautomation.fanuc.common.md#xyzposition-robotstream_motionqueue_end_cartesian_position): `x`, `y`, `z`
