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

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.soap.data.power_return_code import PowerReturnCode

controller = StaubliController()
controller.connect("192.168.0.254")

# The controller must be in remote mode
code = controller.soap.set_power(True)

if code != PowerReturnCode.Success:
    print(f"Arm not powered: {code.name}")  # OnlyInRemoteMode, EnableTimeout...

# Power off at the end
controller.soap.set_power(False)

controller.disconnect()
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

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.soap.data.motion_desc import MotionDesc
from underautomation.staubli.soap.data.frame import Frame
from underautomation.staubli.soap.data.blend_type import BlendType
from underautomation.staubli.soap.data.move_type import MoveType

controller = StaubliController()
controller.connect("192.168.0.254")

joints = controller.soap.get_current_joint_position(0)
fk = controller.soap.forward_kinematics(0, joints)

mdesc = MotionDesc()

# Limits of the joint speed, acceleration and deceleration
mdesc.velocity = 0.5
mdesc.acceleration = 0.5
mdesc.deceleration = 0.5

# Limits of the speed of the tool center point
mdesc.translation_velocity = 0.1
mdesc.rotation_velocity = 0.1

# Stop at each point, no blending
mdesc.blend_type = BlendType.BlendOff

# Absolute target, flange as tool, world as reference frame
mdesc.abs_rel = MoveType.Absolute
mdesc.tool = Frame()
mdesc.frame = Frame()

# Keep the configuration of the arm (shoulder, elbow, wrist)
mdesc.config = fk.config

# Interpolation frequency in percent. 0 is refused by the controller (invalid motion descriptor)
mdesc.frequency = 100

controller.disconnect()
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

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.soap.data.motion_desc import MotionDesc
from underautomation.staubli.soap.data.motion_return_code import MotionReturnCode

controller = StaubliController()
controller.connect("192.168.0.254")

joints = controller.soap.get_current_joint_position(0)
fk = controller.soap.forward_kinematics(0, joints)
mdesc = MotionDesc()
mdesc.velocity = 0.5
mdesc.acceleration = 0.5
mdesc.deceleration = 0.5
mdesc.translation_velocity = 0.1
mdesc.rotation_velocity = 0.1
mdesc.config = fk.config
mdesc.frequency = 100  # interpolation frequency in percent, 0 is refused

target = controller.soap.forward_kinematics(0, joints).position
target.px += 0.1
intermediate = controller.soap.forward_kinematics(0, joints).position
intermediate.py += 0.05

controller.soap.set_power(True)

# Joint move to joint values, in radians
result = controller.soap.move_jj(0, joints, mdesc)

# Joint move to a Cartesian frame
result = controller.soap.move_jc(0, target, mdesc)

# Straight line to a Cartesian frame
result = controller.soap.move_l(0, target, mdesc)

# Circle through an intermediate frame, to a target frame
result = controller.soap.move_c(0, intermediate, target, mdesc)

# The controller accepted the move, or tells why not
if result.return_code != MotionReturnCode.Success:
    print(f"Move {result.id} refused: {result.return_code.name}")

controller.disconnect()
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

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# Stop the arm now
code = controller.soap.stop_motion()

# Continue the moves that were stopped
code = controller.soap.restart_motion()

# Or cancel all the moves that are not finished
code = controller.soap.reset_motion()

controller.disconnect()
```

- `StopMotion()` stops the arm on its path.
- `RestartMotion()` continues the moves that were stopped.
- `ResetMotion()` cancels every move that is not finished. Call it after an error, before new moves.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/underautomation.staubli.soap.internal.md#soapclientbase-controllersoap))

- `move_c(robot: int, frameB: Frame, frameC: Frame, mdesc: MotionDesc) -> IMoveResult`: Move the robot to a target position using a Cartesian path
- `move_jc(robot: int, frame: Frame, mdesc: MotionDesc) -> IMoveResult`: Move the robot to a target position using a Cartesian path with joint constraints
- `move_jj(robot: int, joints: typing.List[float], mdesc: MotionDesc) -> IMoveResult`: Move the robot to a target position using joint positions
- `move_l(robot: int, frame: Frame, mdesc: MotionDesc) -> IMoveResult`: Move the robot to a target position using a linear path in Cartesian space
- `reset_motion() -> MotionReturnCode`: Reset the motion of the robot
- `restart_motion() -> MotionReturnCode`: Restart the motion of the robot
- `stop_motion() -> MotionReturnCode`: Stop the motion of the robot immediately
- `set_power(power: bool) -> PowerReturnCode`: Set the power state of the robot (controller mut be in remote mode)

**MotionDesc** ([reference](../api/underautomation.staubli.soap.data.md#motiondesc))

- `MotionDesc()`: Initializes a new instance of the MotionDesc class.
- `tool: Frame`: Defines the pose of the robot's tool center point (TCP) in flange, including both position and orientation.
- `frame: Frame`: Defines the frame in which the tool position is located, including both position and orientation.
- `abs_rel: MoveType`: Specifies whether the motion is defined in absolute or relative terms.
- `config: Config`: Contains additional configuration parameters specific to the robot type, such as anthropomorphic, SCARA, or VRBX configurations.
- `blend_type: BlendType`: Specifies the type of blending to be applied when transitioning between motion segments.
- `distance_blend_previous: float`: In the joint and Cartesian blending modes, the distance between the target point where blending begins and the next point, in millimeters or inches, depending on the length unit used in the application.
- `distance_blend_next: float`: In joint and Cartesian blending modes, the distance between the target point where blending ends and the next point, in millimeters or inches, depending on the length unit of the application.
- `velocity: float`: Maximum allowable joint speed, as a percentage of the robot's nominal speed.
- `acceleration: float`: Maximum allowed joint acceleration, as a percentage of the robot's nominal acceleration.
- `deceleration: float`: Maximum allowed joint deceleration, as a percentage of the robot's nominal deceleration.
- `translation_velocity: float`: Maximum allowed feed rate of the tool center, in mm/s or inches/s depending on the length unit of the application.
- `rotation_velocity: float`: Maximum permitted tool rotation speed, in degrees per second.
- `frequency: float`: Frequency of motion in Hz.

**IMoveResult** ([reference](../api/underautomation.staubli.soap.data.md#imoveresult))

- `id: int (read only)`: Identifier of the motion command.
- `return_code: MotionReturnCode (read only)`: Return code indicating the outcome of the motion command.

**MotionReturnCode** ([reference](../api/underautomation.staubli.soap.data.md#motionreturncode))

- Success: Success, no error occurred.
- NotReady: The robot is not ready to execute motion.
- ParameterError: Invalid parameter provided to the motion command.
- MisuseError: Motion command misuse error.
- UnexpectedError: An unexpected error occurred during motion.

**PowerReturnCode** ([reference](../api/underautomation.staubli.soap.data.md#powerreturncode))

- Success: Success, no error occurred.
- RobotNotStopped: Cannot change power while the robot is not stopped.
- EnableTimeout: Timeout while enabling power.
- DisableTimeout: Timeout while disabling power.
- OnlyInRemoteMode: Power can only be changed in remote mode.

**BlendType** ([reference](../api/underautomation.staubli.soap.data.md#blendtype))

- BlendOff: No blending; the robot stops at each target point.
- BlendJoint: Joint-space blending between motion segments.
- BlendCartesian: Cartesian-space blending between motion segments.

**MoveType** ([reference](../api/underautomation.staubli.soap.data.md#movetype))

- Absolute: Absolute motion in the reference frame.
- Relative: Relative motion from the current position.
