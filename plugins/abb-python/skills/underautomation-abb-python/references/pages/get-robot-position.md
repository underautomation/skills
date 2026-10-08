# Get the robot position

Read the current Cartesian position (robtarget) and the joint position (jointtarget) of an ABB robot, and convert between them.

Web page: https://underautomation.com/abb/documentation/get-robot-position

To get where an ABB robot is, call `robot.Rws.MotionSystem.GetRobTarget("ROB_1")` for the Cartesian position of the tool, and `GetJointTarget("ROB_1")` for the value of each axis. Both are read operations, they need no mastership. Positions are in millimetres, joints in degrees.

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

## robtarget or jointtarget

The two describe the same robot at the same moment, from two points of view.

|            | `RobTarget`                                                   | `JointTarget`                             |
| ---------- | ------------------------------------------------------------- | ----------------------------------------- |
| Describes  | where the tool is                                             | where each axis is                        |
| Unit       | millimetres                                                   | degrees, millimetres for a linear axis    |
| Content    | `X`, `Y`, `Z`, `Orientation`, `Configuration`, `ExternalAxes` | `RobotAxes` (axis 1 to 6), `ExternalAxes` |
| Depends on | the tool, the work object and the frame                       | nothing else                              |
| Ambiguous  | no, but several joint sets reach it                           | no                                        |

`Orientation` is a `Quaternion`, the four values RAPID writes as `rot`. `Configuration` is the `RobotConfiguration`, the quarter revolution each deciding axis sits in, which is what tells apart the joint combinations that reach the same pose. An external axis the system does not define comes back as `ExternalJoints.NotInUse`.

## Read the position

`ROB_1` is the usual name of the robot arm. Get the exact name of the mechanical units of your system with `robot.Rws.MotionSystem.GetMechanicalUnits()`.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.common.external_joints import ExternalJoints
from underautomation.abb.rws.data.coordinate_system import CoordinateSystem

robot = AbbController()
robot.connect("192.168.0.1")

# Where the tool is, in millimetres, with the axis configuration and the external axes
target = robot.rws.motion_system.get_rob_target("ROB_1")
print(f"X={target.x} Y={target.y} Z={target.z}")
print(f"orientation {target.orientation}")
print(f"configuration {target.configuration}")
print(f"external axes {target.external_axes}")

# The same reading in another frame, with a given tool and work object
in_world = robot.rws.motion_system.get_rob_target("ROB_1", CoordinateSystem.World,
                                                  tool="tGripper", workObject="wobj0")
print(in_world)

# The joint values, robot axes in degrees
joints = robot.rws.motion_system.get_joint_target("ROB_1")
print(f"axis 1 = {joints.robot_axes.axis1} deg")
print(f"axis 2 = {joints.robot_axes.axis2} deg")

# An external axis the system does not define comes back as ExternalJoints.NotInUse
if joints.external_axes.axis_a != ExternalJoints.NotInUse:
    print(f"external axis A = {joints.external_axes.axis_a}")

# alwaysRead asks the controller to measure again instead of answering with the value it holds
measured = robot.rws.motion_system.get_joint_target("ROB_1", alwaysRead=True)
print(measured)

# Cartesian position without the external axes. external_axes is None here.
cartesian = robot.rws.motion_system.get_cartesian_position("ROB_1")
print(cartesian)

# The raw values of the measurement system of the unit
physical = robot.rws.motion_system.get_physical_joints("ROB_1")
print(physical)

# The same two positions seen from a RAPID task instead of a mechanical unit
task_target = robot.rws.rapid.get_rob_target("T_ROB1")
task_joints = robot.rws.rapid.get_joint_target("T_ROB1")

# Which external joints of the task carry a real value
states = robot.rws.rapid.get_external_joint_states("T_ROB1")
print(f"external joint 1 : {states.joint1}")

# The units the task can move
for unit in robot.rws.rapid.get_mechanical_units("T_ROB1"):
    print(f"{unit.name} : {unit.type}, {unit.mode}")

robot.disconnect()
```

Four things in that example are worth separating:

- `GetRobTarget` gives the position, the orientation, the axis configuration and the external axes. `GetCartesianPosition` gives the same position without the external axes.
- `GetJointTarget` gives the joints. With `alwaysRead: true` the controller measures again instead of answering with the value it holds, which matters when the robot is moved by hand.
- `GetPhysicalJoints` gives the raw values of the measurement system of the unit, before the calibration offsets.
- The same two positions can be read from a RAPID task instead of a mechanical unit, with `robot.Rws.Rapid.GetRobTarget("T_ROB1")` and `GetJointTarget("T_ROB1")`.

## Motion system or RAPID task

Both readings exist because the two services answer different questions.

- `robot.Rws.MotionSystem` reads a **mechanical unit**. Use it when you think in terms of hardware: this arm, this positioner, this external axis. You choose the frame, the tool and the work object in the call.
- `robot.Rws.Rapid` reads a **task**. Use it when you think in terms of the program: the task uses the tool and the work object that are active in it right now, so the answer matches what a `MoveL` of that task would produce.

On a single robot system with one motion task the two give the same numbers. On a MultiMove system, or when the tool active in the task is not the one you want to measure from, they do not.

## Frames, tool and work object

By default the position is expressed in the base frame of the unit, with its active tool and work object. `CoordinateSystem` selects another frame: `World`, `Base`, `Tool` or `WorkObject`. The `tool` and `workObject` arguments name the ones to measure with, without changing what the robot uses.

Reading the same point with two different tools gives two different `RobTarget`. This is the usual cause of an unexplained offset between a value read by the SDK and the same value shown on the teach pendant.

## Convert a jointtarget into a robtarget

The controller does the kinematics for you. Forward kinematics turns joint values into a pose, inverse kinematics turns a pose into joint values. The inverse case has several answers, so you also pass the previous joint values and the axis configuration to pick one.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.common.external_joints import ExternalJoints
from underautomation.abb.common.joint_target import JointTarget
from underautomation.abb.common.pose import Pose
from underautomation.abb.common.robot_joints import RobotJoints

robot = AbbController()
robot.connect("192.168.0.1")

# These four calculations work in metres and radians, not in millimetres and degrees.

# Tool relative to the mounting flange. Here the flange itself, with no rotation.
tool_frame = Pose(0, 0, 0, 1, 0, 0, 0)

# Forward kinematics: where the tool would be for these joint values
joints = JointTarget(RobotJoints(0, 0, 0, 0, 0.5, 0), ExternalJoints(0, 0, 0, 0, 0, 0))

pose = robot.rws.motion_system.get_pose_from_joints("ROB_1", tool_frame, joints)
print(f"tool at {pose.x} {pose.y} {pose.z} metres, configuration {pose.configuration}")

# Inverse kinematics: which joint values put the tool at that pose.
# previousJoints decides between the solutions the pose admits.
solution = robot.rws.motion_system.get_joints_from_pose("ROB_1", pose, ExternalJoints(0, 0, 0, 0, 0, 0),
                                                       tool_frame, joints, pose.configuration)
print(f"axis 5 = {solution.robot_axes.axis5} rad")

# The controller has a second calculation for the same question. It does not always
# pick the same solution.
other = robot.rws.motion_system.get_joints_from_cartesian("ROB_1", pose, ExternalJoints(0, 0, 0, 0, 0, 0),
                                                          tool_frame, joints, pose.configuration)
print(other)

# Every way of reaching the pose. A six axis robot usually has eight.
solutions = robot.rws.motion_system.get_all_joint_solutions("ROB_1", pose, ExternalJoints(0, 0, 0, 0, 0, 0),
                                                            tool_frame, pose.configuration)

for s in solutions:
    print(f"{s.configuration} : {s.robot_axes}")

# Set robotHoldsWorkObject to True when the tool is fixed in the cell and the robot
# carries the work object. Set logErrors to True to have the controller write an
# event log message when the calculation fails.
held = robot.rws.motion_system.get_pose_from_joints("ROB_1", tool_frame, joints,
                                                    robotHoldsWorkObject=True, logErrors=True)
print(held)

robot.disconnect()
```

These calculations are pure computation, they do not move the robot and they work on positions the robot is not at.

## Millimetres, metres, degrees and radians

The readings answer in millimetres and degrees. The four kinematics calculations work in **metres and radians**, in both directions. Nothing in the answer says which one it is, so convert explicitly when you feed one into the other.

```python
import math

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.common.joint_target import JointTarget
from underautomation.abb.common.pose import Pose
from underautomation.abb.common.robot_joints import RobotJoints

robot = AbbController()
robot.connect("192.168.0.1")

def to_radians(degrees):
    f = math.pi / 180.0

    return RobotJoints(degrees.axis1 * f, degrees.axis2 * f, degrees.axis3 * f,
                       degrees.axis4 * f, degrees.axis5 * f, degrees.axis6 * f)

def to_degrees(radians):
    f = 180.0 / math.pi

    return RobotJoints(radians.axis1 * f, radians.axis2 * f, radians.axis3 * f,
                       radians.axis4 * f, radians.axis5 * f, radians.axis6 * f)

# The readings answer in millimetres and degrees
reading = robot.rws.motion_system.get_rob_target("ROB_1")
joints = robot.rws.motion_system.get_joint_target("ROB_1")

print(f"{reading.x} mm, axis 5 = {joints.robot_axes.axis5} deg")

# The four kinematics calculations work in metres and radians, in both directions.
# Convert the joints before sending them.
in_radians = JointTarget(to_radians(joints.robot_axes), joints.external_axes)
tool_frame = Pose(0, 0, 0, 1, 0, 0, 0)

computed = robot.rws.motion_system.get_pose_from_joints("ROB_1", tool_frame, in_radians)

# And convert the answer back to millimetres to compare it with the reading
print(f"{computed.x * 1000} mm computed, {reading.x} mm read")

robot.disconnect()
```

## Going further

- [Motion system, position & kinematics](rws-motion.md), the complete reference
- [Read & write RAPID variables](read-write-rapid-variables.md), to read a taught `robtarget` from the program
- [RAPID tasks & program execution](rws-rapid-tasks.md)

**Methods of MotionSystemService** ([reference](../api/underautomation.abb.rws.services.md#motionsystemservice-robotrwsmotion_system))

- `set_position_target(target: RobTarget) -> None`: Sends the robot to a cartesian target (synchronous) The position is expressed in millimetres, in the coordinate system currently active for the mechanical unit selected for jogging.
- `get_rob_target(mechanicalUnit: str, coordinateSystem: CoordinateSystem=CoordinateSystem.Base, tool: str=None, workObject: str=None) -> RobTarget`: Gets where the tool of a mechanical unit currently is (synchronous) The position is expressed in millimetres.
- `get_joint_target(mechanicalUnit: str, alwaysRead: bool=False) -> JointTarget`: Gets the joint values a mechanical unit currently stands at (synchronous) The robot axes are expressed in degrees.

**RobTarget** ([reference](../api/underautomation.abb.common.md#robtarget))

- `RobTarget(x: float, y: float, z: float, orientation: Quaternion, configuration: RobotConfiguration, externalAxes: ExternalJoints)`: Initializes a new target
- `configuration: RobotConfiguration`: Axis configuration used to reach the pose. Never null.
- `external_axes: ExternalJoints`: Values of the six external axes, null when the reading does not report them
- Inherited from [Pose](../api/underautomation.abb.common.md#pose): `orientation`
- Inherited from [Position](../api/underautomation.abb.common.md#position): `x`, `y`, `z`

**JointTarget** ([reference](../api/underautomation.abb.common.md#jointtarget))

- `JointTarget(robotAxes: RobotJoints, externalAxes: ExternalJoints)`: Initializes a new joint target
- `robot_axes: RobotJoints`: Values of the six axes of the robot arm. Never null.
- `external_axes: ExternalJoints`: Values of the six external axes. Never null.

**RobotConfiguration** ([reference](../api/underautomation.abb.common.md#robotconfiguration))

- `RobotConfiguration(quarter1: int, quarter4: int, quarter6: int, quarterX: int)`: Initializes a new configuration
- `quarter1: int`: Quarter revolution axis 1 sits in
- `quarter4: int`: Quarter revolution axis 4 sits in
- `quarter6: int`: Quarter revolution axis 6 sits in
- `quarter_x: int`: Index of the arm configuration, which tells the remaining joint combinations apart

**CoordinateSystem** ([reference](../api/underautomation.abb.rws.data.md#coordinatesystem))

- Unknown: The controller reported a frame this library does not know
- World: The world frame, shared by every mechanical unit of the system
- Base: The base frame of the mechanical unit
- Tool: The frame of the active tool
- WorkObject: The frame of the active work object
