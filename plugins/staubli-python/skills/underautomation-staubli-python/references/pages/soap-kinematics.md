# Kinematics

Compute the forward and inverse kinematics of a Staubli robot on the controller, with the configuration of the arm and the joint ranges.

Web page: https://underautomation.com/staubli/documentation/soap-kinematics

This page shows how to compute the forward and inverse kinematics of a Staubli robot with the SDK. The controller computes them with the geometry of the real arm: the result is the one that the CS8 or CS9 controller uses for its own moves.

## Forward kinematics

`ForwardKinematics(robot, joints)` returns the flange frame for joint values in radians, and the configuration of the arm for these joints.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# Joint values in radians, here the current ones
joints = controller.soap.get_current_joint_position(0)

# The controller computes the flange frame for these joints
fk = controller.soap.forward_kinematics(0, joints)

# Position of the frame origin, and its orientation as a rotation matrix
frame = fk.position
print(f"P = [{frame.px}, {frame.py}, {frame.pz}]")

# Configuration of the arm for this position (shoulder, elbow, wrist)
config = fk.config
print(config)

controller.disconnect()
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

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.soap.data.reversing_result import ReversingResult

controller = StaubliController()
controller.connect("192.168.0.254")

current = controller.soap.get_current_joint_position(0)
joint_range = controller.soap.get_joint_range(0)

# Target: the current flange frame, 50 mm higher
fk = controller.soap.forward_kinematics(0, current)
target = fk.position
target.pz += 0.050

# Keep the current configuration of the arm
ik = controller.soap.reverse_kinematics(0, current, target, fk.config, joint_range)

if ik.result == ReversingResult.Success:
    print(list(ik.joint))
else:
    print(f"No solution: {ik.result.name}")  # OutOfWorkspace, JointOutOfRange...

controller.disconnect()
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

**Methods of SoapClientBase** ([reference](../api/underautomation.staubli.soap.internal.md#soapclientbase-controllersoap))

- `forward_kinematics(robot: int, joints: typing.List[float]) -> IForwardKinematics`: Calculate the forward kinematics of a robot based on its joint positions
- `reverse_kinematics(robot: int, joint: typing.List[float], target: Frame, config: Config, jointRange: JointRange) -> IReverseKinematics`: Calculate the reverse kinematics of a robot to reach a target position and orientation

**IForwardKinematics** ([reference](../api/underautomation.staubli.soap.data.md#iforwardkinematics))

- `position: Frame (read only)`: Cartesian position resulting from the forward kinematics computation.
- `config: Config (read only)`: Robot configuration associated with the computed position.

**IReverseKinematics** ([reference](../api/underautomation.staubli.soap.data.md#ireversekinematics))

- `joint: typing.List[float] (read only)`: Joint angles resulting from the reverse kinematics computation.
- `result: ReversingResult (read only)`: Result code indicating the outcome of the reverse kinematics computation.

**ReversingResult** ([reference](../api/underautomation.staubli.soap.data.md#reversingresult))

- Success: Reverse kinematics succeeded.
- NoConvergence: The algorithm did not converge to a solution.
- JointOutOfRange: The computed joint position is out of range.
- OutOfWorkspace: The target is outside the robot workspace.
- InvalidConfiguration: The specified configuration is invalid.
- InvalidOrientation: The specified orientation is invalid.
- UnsupportedKinematics: The robot kinematics type is not supported.
- UnconstrainedFrame: The frame is unconstrained.
- InvalidErrorCode: Invalid error code returned.

**Frame** ([reference](../api/underautomation.staubli.soap.data.md#frame))

- `Frame()`: Default constructor.
- `nx: float`: X component of the local X-axis vector (Normal X).
- `ny: float`: Y component of the local X-axis vector (Normal Y).
- `nz: float`: Z component of the local X-axis vector (Normal Z).
- `ox: float`: X component of the local Y-axis vector (Orientation X).
- `oy: float`: Y component of the local Y-axis vector (Orientation Y).
- `oz: float`: Z component of the local Y-axis vector (Orientation Z).
- `ax: float`: X component of the local Z-axis vector (Approach X).
- `ay: float`: Y component of the local Z-axis vector (Approach Y).
- `az: float`: Z component of the local Z-axis vector (Approach Z).
- `px: float`: X coordinate of the frame's origin in global space (Pose X).
- `py: float`: Y coordinate of the frame's origin in global space (Pose Y).
- `pz: float`: Z coordinate of the frame's origin in global space (Pose Z).

**Config** ([reference](../api/underautomation.staubli.soap.data.md#config))

- `Config()`: Initializes a new instance of the Config class.
- `anthro_config: AnthroConfig`: Anthropomorphic robot configuration.
- `scara_config: ScaraConfig`: SCARA robot configuration.
- `vrbx_config: VrbxConfig`: VRBX robot configuration.

**AnthroConfig** ([reference](../api/underautomation.staubli.soap.data.md#anthroconfig))

- `AnthroConfig()`: Initializes a new instance of the AnthroConfig class.
- `shoulder: ShoulderConfig`: Shoulder configuration.
- `elbow: PositiveNegativeConfig`: Elbow configuration.
- `wrist: PositiveNegativeConfig`: Wrist configuration.

**ScaraConfig** ([reference](../api/underautomation.staubli.soap.data.md#scaraconfig))

- `ScaraConfig()`: Initializes a new instance of the ScaraConfig class.
- `shoulder: ShoulderConfig`: Shoulder configuration.
