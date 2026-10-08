# Motion system, position & kinematics

Read the robot position as a robtarget or a jointtarget, jog the robot, compute forward and inverse kinematics, and manage mechanical units and calibration.

Web page: https://underautomation.com/abb/documentation/rws-motion

`robot.Rws.MotionSystem` covers everything about how the robot stands and how it moves: the mechanical units of the system and their axes, where the tool currently is, jogging, the kinematics calculations, the collision supervision and the calibration.

This is the service that moves a real robot. Reading is always safe. Writing needs the [mastership](rws-mastership.md) of the `Motion` domain, and most of the time also a controller in manual mode with the motors on, which is read and changed through the [control panel](rws-panel.md).

## Geometry types

The positions of the SDK are built from a few small classes of the `UnderAutomation.ABB.Common` namespace. They are the same types everywhere, so a position read here can be written into a RAPID variable without conversion.

| Type                 | Holds                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------- |
| `Position`           | `X`, `Y`, `Z`                                                                           |
| `Quaternion`         | `Q1` to `Q4`, an orientation as a unit quaternion                                       |
| `Pose`               | a `Position` plus an `Orientation`                                                      |
| `RobotConfiguration` | `Quarter1`, `Quarter4`, `Quarter6` and `QuarterX`, which say in which turn the axes sit |
| `RobotJoints`        | `Axis1` to `Axis6`, the six axes of the arm                                             |
| `ExternalJoints`     | `AxisA` to `AxisF`, the six external axes                                               |
| `RobTarget`          | a `Pose` plus a `Configuration` and the `ExternalAxes`                                  |
| `JointTarget`        | `RobotAxes` plus `ExternalAxes`                                                         |

A pose alone does not say how the robot reaches it. The same point in space is usually reachable in several ways, and `RobotConfiguration` is what tells them apart.

An external axis the system does not use is reported with a large value instead of a real one. Compare it with the constant `ExternalJoints.NotInUse` rather than with zero.

Units are not the same everywhere, and this is the convention of the controller, not a choice of the SDK:

| Where                                 | Units                                   |
| ------------------------------------- | --------------------------------------- |
| Positions, axis poses and base frames | millimetres, and degrees for the joints |
| The four kinematics calculations      | metres and radians                      |

**Position** ([reference](../api/underautomation.abb.common.md#position))

- `Position(x: float, y: float, z: float)`: Initializes a new position
- `x: float`: Coordinate along the X axis
- `y: float`: Coordinate along the Y axis
- `z: float`: Coordinate along the Z axis

**Quaternion** ([reference](../api/underautomation.abb.common.md#quaternion))

- `Quaternion(q1: float, q2: float, q3: float, q4: float)`: Initializes a new quaternion
- `q1: float`: Real component of the quaternion
- `q2: float`: First imaginary component of the quaternion
- `q3: float`: Second imaginary component of the quaternion
- `q4: float`: Third imaginary component of the quaternion

**Pose** ([reference](../api/underautomation.abb.common.md#pose))

- `Pose(x: float, y: float, z: float, q1: float, q2: float, q3: float, q4: float)`: Initializes a new pose
- `orientation: Quaternion`: Orientation held at this position. Never null: a pose built without one carries the identity rotation.
- Inherited from [Position](../api/underautomation.abb.common.md#position): `x`, `y`, `z`

**RobotConfiguration** ([reference](../api/underautomation.abb.common.md#robotconfiguration))

- `RobotConfiguration(quarter1: int, quarter4: int, quarter6: int, quarterX: int)`: Initializes a new configuration
- `quarter1: int`: Quarter revolution axis 1 sits in
- `quarter4: int`: Quarter revolution axis 4 sits in
- `quarter6: int`: Quarter revolution axis 6 sits in
- `quarter_x: int`: Index of the arm configuration, which tells the remaining joint combinations apart

**RobotJoints** ([reference](../api/underautomation.abb.common.md#robotjoints))

- `RobotJoints(axis1: float, axis2: float, axis3: float, axis4: float, axis5: float, axis6: float)`: Initializes the six axes
- `axis1: float`: Value of axis 1
- `axis2: float`: Value of axis 2
- `axis3: float`: Value of axis 3
- `axis4: float`: Value of axis 4
- `axis5: float`: Value of axis 5
- `axis6: float`: Value of axis 6

**ExternalJoints** ([reference](../api/underautomation.abb.common.md#externaljoints))

- `ExternalJoints(axisA: float, axisB: float, axisC: float, axisD: float, axisE: float, axisF: float)`: Initializes the six external axes
- `axis_a: float`: Value of external axis A
- `axis_b: float`: Value of external axis B
- `axis_c: float`: Value of external axis C
- `axis_d: float`: Value of external axis D
- `axis_e: float`: Value of external axis E
- `axis_f: float`: Value of external axis F
- `static NotInUse: float`: Value the controller reports for an external axis that is not in use

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

## Mechanical units

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

A mechanical unit is anything the controller drives: the robot arm itself, a track, a positioner. `GetMechanicalUnits` lists them, `GetMechanicalUnit` describes one of them, and `SetMechanicalUnit` changes its properties.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.common.pose import Pose
from underautomation.abb.rws.data.coordinate_system import CoordinateSystem
from underautomation.abb.rws.data.jog_mode import JogMode
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# Every mechanical unit of the system, with its activation state
for unit in robot.rws.motion_system.get_mechanical_units():
    print(f"{unit.name} : {unit.mode}, drive module {unit.drive_module}")

# Everything the controller knows about one unit
info = robot.rws.motion_system.get_mechanical_unit("ROB_1")
print(f"{info.type}, task {info.task_name}, status {info.status}")
print(f"tool {info.tool_name}, work object {info.work_object_name}, payload {info.payload_name}")
print(f"{info.axes} axes, jog mode {info.jog_mode}, frame {info.coordinate_system}")

# Axis by axis. Axes are numbered from 1.
axis_count = robot.rws.motion_system.get_axis_count("ROB_1")

for axis in range(1, axis_count + 1):
    axis_info = robot.rws.motion_system.get_axis("ROB_1", axis)
    axis_pose = robot.rws.motion_system.get_axis_pose("ROB_1", axis)

    print(f"axis {axis_info.number} : {axis_info.status}, at {axis_pose}")

# Where the base of the unit stands, in millimetres
base_frame = robot.rws.motion_system.get_base_frame("ROB_1")
print(f"base frame {base_frame}, type {base_frame.type}")

# Changing a property of a unit needs the mastership of the motion domain.
# Give only the properties you want to change, leave the others None.
robot.rws.mastership.request(MastershipDomain.Motion)

try:
    robot.rws.motion_system.set_mechanical_unit("ROB_1",
                                                tool="tGripper",
                                                jogMode=JogMode.Cartesian,
                                                coordinateSystem=CoordinateSystem.Base)
finally:
    robot.rws.mastership.release(MastershipDomain.Motion)

# The controller answers success even when it could not apply one of the properties.
# Read the unit back to see what it really did.
print(robot.rws.motion_system.get_mechanical_unit("ROB_1").tool_name)

# Declaring where a base or an axis sits changes the calibration of the cell.
# The user account needs the matching UAS grant.
new_base = Pose(0, 0, 0, 1, 0, 0, 0)
robot.rws.motion_system.set_base_frame("ROB_1", new_base)
robot.rws.motion_system.set_axis_pose("ROB_1", 1, new_base)

robot.disconnect()
```

`MechanicalUnitInfo.Status` says whether the unit can move at all:

| `MechanicalUnitStatus`                               | Meaning                                                              |
| ---------------------------------------------------- | -------------------------------------------------------------------- |
| `Synchronized`                                       | Calibrated and synchronized, the unit can be moved                   |
| `NotCommutated`                                      | One or several motors have not been commutated                       |
| `NotCalibrated`                                      | The unit has never been calibrated                                   |
| `NotAbsoluteSynchronized`, `NotRelativeSynchronized` | The measurement of one or several axes is not synchronized           |
| `Locked`, `LockedShow`                               | The unit is locked and refuses to move                               |
| `Initiated`, `Undefined`, `Unknown`                  | The unit is starting up, or the controller does not report its state |

`SetMechanicalUnit` needs the mastership of the `Motion` domain. Give only the properties you want to change and leave the others null. The controller answers with a success status even when it could not apply one of them, so read the unit back to see what it really did.

`SetBaseFrame` and `SetAxisPose` declare where a unit or an axis sits in the cell. They do not move anything, they change the calibration of the cell, and the user account needs the matching UAS grant. The controller takes the request and applies the frame afterwards, so a success means the request was accepted, not that the new frame is already in use.



**MechanicalUnitItem** ([reference](../api/underautomation.abb.rws.data.md#mechanicalunititem))

- `MechanicalUnitItem()`: Initializes a new instance of the MechanicalUnitItem class
- `name: str`: Name of the mechanical unit, for example "ROB_1"
- `mode: MechanicalUnitMode`: Whether the unit is activated
- `activation_allowed: bool | None`: Whether the unit can be activated, null when the controller did not report it
- `drive_module: int | None`: Number of the drive module the unit is connected to, null when the controller did not report it

**MechanicalUnitInfo** ([reference](../api/underautomation.abb.rws.data.md#mechanicalunitinfo))

- `MechanicalUnitInfo()`: Initializes a new instance of the MechanicalUnitInfo class
- `name: str`: Name of the mechanical unit, for example "ROB_1"
- `tool_name: str`: Name of the active tool
- `work_object_name: str`: Name of the active work object
- `payload_name: str`: Name of the active payload
- `total_payload_name: str`: Name of the active total payload, which is the payload plus the load of the tool
- `status: MechanicalUnitStatus`: Calibration and synchronization state of the unit
- `mode: MechanicalUnitMode`: Whether the unit is activated
- `jog_mode: JogMode`: How the jogging commands sent to the unit are interpreted
- `type: MechanicalUnitType`: Kind of mechanical unit
- `task_name: str`: Name of the RAPID task that drives the unit
- `coordinate_system: CoordinateSystem`: Reference frame the cartesian positions of the unit are expressed in
- `axes: int | None`: Number of axes of the unit, null when the controller did not report it
- `total_axes: int | None`: Number of axes of the unit and of the units integrated with it, null when the controller did not report it
- `is_integrated_unit: str`: Name of the mechanical unit this one is integrated into. A unit that is integrated into no other one is reported with a placeholder name rather than an empty value.
- `has_integrated_unit: str`: Name of the mechanical unit integrated into this one. A unit that integrates no other one is reported with a placeholder name rather than an empty value.

**MechanicalUnitMode** ([reference](../api/underautomation.abb.rws.data.md#mechanicalunitmode))

- Unknown: The controller reported a mode this library does not know
- Activated: The mechanical unit is activated and takes part in the motion
- Deactivated: The mechanical unit is deactivated and stays where it is

**MechanicalUnitType** ([reference](../api/underautomation.abb.rws.data.md#mechanicalunittype))

- Unknown: The controller reported a type this library does not know
- None_: No mechanical unit
- TcpRobot: A robot arm holding a tool center point, which can be moved in cartesian coordinates
- Robot: A robot arm without a tool center point, which can only be moved axis by axis
- Single: A single external axis, such as a track or a positioner
- Undefined: The controller knows the unit but does not report what it is

**MechanicalUnitStatus** ([reference](../api/underautomation.abb.rws.data.md#mechanicalunitstatus))

- Unknown: The controller reported a state this library does not know
- Initiated: The unit is starting up
- NotCommutated: One or several motors have not been commutated
- NotCalibrated: The unit has never been calibrated
- NotAbsoluteSynchronized: One or several absolute measurement axes are not synchronized
- NotRelativeSynchronized: One or several relative measurement axes are not synchronized
- Synchronized: The unit is calibrated and synchronized, and can be moved
- Locked: The unit is locked and refuses to move
- LockedShow: The unit is locked, and the controller shows it as such
- Undefined: The controller knows the unit but does not report its state

**AxisInfo** ([reference](../api/underautomation.abb.rws.data.md#axisinfo))

- `AxisInfo()`: Initializes a new instance of the AxisInfo class
- `number: int`: Number of the axis inside its mechanical unit, starting at 1
- `status: MechanicalUnitStatus`: Calibration and synchronization state of the axis
- `logical_axis: int | None`: Logical joint number of the axis, null when the controller did not report it

**BaseFrame** ([reference](../api/underautomation.abb.rws.data.md#baseframe))

- `BaseFrame()`: Initializes a new base frame at the origin, with no rotation
- `type: str`: Kind of base frame the controller reports, for example "IRBRobot"
- Inherited from [Pose](../api/underautomation.abb.common.md#pose): `orientation`
- Inherited from [Position](../api/underautomation.abb.common.md#position): `x`, `y`, `z`

**CoordinateSystem** ([reference](../api/underautomation.abb.rws.data.md#coordinatesystem))

- Unknown: The controller reported a frame this library does not know
- World: The world frame, shared by every mechanical unit of the system
- Base: The base frame of the mechanical unit
- Tool: The frame of the active tool
- WorkObject: The frame of the active work object

**JogMode** ([reference](../api/underautomation.abb.rws.data.md#jogmode))

- Unknown: The controller reported a mode this library does not know
- AxisGroup1: Each command moves one axis of the first axis group
- AxisGroup2: Each command moves one axis of the second axis group
- Cartesian: The tool is moved along the axes of the active coordinate system
- Align: The tool is aligned with the closest axis of the active coordinate system
- GoToPosition: The robot moves to a given position
- ConfigurationJog: The robot changes axis configuration without moving the tool center point

## Read the robot position

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

Four readings answer the same question in four ways. All of them are read only and need no mastership.

| Method                       | Returns                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------- |
| `GetRobTarget(unit)`         | `RobTarget`, the Cartesian position with the axis configuration and the external axes |
| `GetCartesianPosition(unit)` | `RobTarget` without the external axes, `ExternalAxes` is then null                    |
| `GetJointTarget(unit)`       | `JointTarget`, the joint values                                                       |
| `GetPhysicalJoints(unit)`    | `RobotJoints`, the raw values of the measurement system of the unit                   |

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

`GetRobTarget` takes a `CoordinateSystem`, a tool and a work object. Without them it answers in the base frame of the unit, with the tool and the work object currently active on it. Passing a tool that does not exist is refused by the controller.

`GetJointTarget` has an `alwaysRead` parameter. By default the controller answers with the value it already holds. With `alwaysRead: true` it measures the position again, which costs more and is what you want when the robot has just moved.



## Position of a RAPID task

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

The same two positions can also be read from a RAPID task instead of a mechanical unit. Those methods are on `robot.Rws.Rapid`, and the last block of the snippet above shows them.

| Method                                         | Returns                                              |
| ---------------------------------------------- | ---------------------------------------------------- |
| `robot.Rws.Rapid.GetRobTarget(task)`           | `RobTarget` of the robot of that task                |
| `robot.Rws.Rapid.GetJointTarget(task)`         | `JointTarget` of the robot of that task              |
| `robot.Rws.Rapid.GetExternalJointStates(task)` | What each external joint of the task is doing        |
| `robot.Rws.Rapid.GetMechanicalUnits(task)`     | The units the positions of the task are expressed in |

Which one to use:

- Read from the motion system when you work with a mechanical unit by name, when you need another coordinate system, another tool or another work object, or when you want the raw measurement.
- Read from the RAPID task when your code already works with tasks, or when you want the position exactly as the running program sees it.

`GetExternalJointStates` is what says how to read the external axis values of the task: a joint can be linear, rotating, inactive, or active without a position. A `RobTarget` read from a task reports an inactive external axis with the same large value as `ExternalJoints.NotInUse`.



**RapidExternalJointStates** ([reference](../api/underautomation.abb.rws.data.md#rapidexternaljointstates))

- `RapidExternalJointStates()`: Initializes a new instance of the RapidExternalJointStates class
- `joint1: RapidJointState`: State of the first external joint
- `joint2: RapidJointState`: State of the second external joint
- `joint3: RapidJointState`: State of the third external joint
- `joint4: RapidJointState`: State of the fourth external joint
- `joint5: RapidJointState`: State of the fifth external joint
- `joint6: RapidJointState`: State of the sixth external joint

**RapidJointState** ([reference](../api/underautomation.abb.rws.data.md#rapidjointstate))

- Unknown: The controller reported a state this library does not know
- Linear: The joint moves along a line
- Rotating: The joint turns
- NotActive: The joint is not active
- NoPosition: The joint is active but has no position

**RapidMechanicalUnitItem** ([reference](../api/underautomation.abb.rws.data.md#rapidmechanicalunititem))

- `RapidMechanicalUnitItem()`: Initializes a new instance of the RapidMechanicalUnitItem class
- `name: str`: Name of the unit, for example "ROB_1"
- `mode: MechanicalUnitMode`: Whether the unit is activated
- `type: MechanicalUnitType`: Kind of unit

## Move to a target

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

`SetPositionTarget` sends the robot to a Cartesian target. It really moves the arm. The preconditions are the same as for jogging: the controller in manual mode, the motors on, this client as the local client of the controller, and the mastership of the `Motion` domain.

`SetMechanicalUnitPosition` does not move anything. It places the unit at the given joint values. Only a virtual controller accepts it, a real one refuses the call.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.common.external_joints import ExternalJoints
from underautomation.abb.common.joint_target import JointTarget
from underautomation.abb.common.robot_joints import RobotJoints
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# set_position_target really moves the robot to a cartesian target.
# Same preconditions as jogging: manual mode, motors on, local client, motion mastership.
target = robot.rws.motion_system.get_rob_target("ROB_1")
target.z += 10  # 10 mm up

robot.rws.mastership.request(MastershipDomain.Motion)

try:
    robot.rws.motion_system.set_position_target(target)
finally:
    robot.rws.mastership.release(MastershipDomain.Motion)

# set_mechanical_unit_position does not move anything: it places the unit at the given joint
# values. Only a virtual controller accepts it, a real one refuses the call.
joints = JointTarget(RobotJoints(0, 0, 0, 0, 30, 0), ExternalJoints(0, 0, 0, 0, 0, 0))

robot.rws.mastership.request(MastershipDomain.Motion)

try:
    robot.rws.motion_system.set_mechanical_unit_position("ROB_1", joints)
finally:
    robot.rws.mastership.release(MastershipDomain.Motion)

robot.disconnect()
```



## Jog the robot

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

Jogging moves the robot step by step, the way the operator does from the FlexPendant. Four conditions have to be met, and none of them can be arranged by a request:

1. The controller is in manual mode. In automatic mode the request is refused with the HTTP status code 403.
2. The motors are on.
3. This client is the local client of the controller.
4. This connection holds the mastership of the `Motion` domain.

```python
import time

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.common.robot_joints import RobotJoints
from underautomation.abb.rws.data.controller_state import ControllerState
from underautomation.abb.rws.data.jog_increment_mode import JogIncrementMode
from underautomation.abb.rws.data.jog_mode import JogMode
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from underautomation.abb.rws.data.operation_mode import OperationMode

robot = AbbController()
robot.connect("192.168.0.1")

# Check the preconditions before asking the robot to move
mode = robot.rws.panel.get_operation_mode()
state = robot.rws.panel.get_controller_state()

if mode == OperationMode.Automatic or state != ControllerState.MotorsOn:
    print("Jogging is refused in this state")
    raise SystemExit(0)

robot.rws.mastership.request(MastershipDomain.Motion)

try:
    # Which unit the jogging commands apply to
    robot.rws.motion_system.set_jogging_mechanical_unit("ROB_1")

    # How the six values are read depends on the jog mode of that unit
    robot.rws.motion_system.set_mechanical_unit("ROB_1", jogMode=JogMode.AxisGroup1)

    # The change count of the last reading. The controller refuses a command
    # built on a state that has moved on since.
    info = robot.rws.motion_system.get_info()

    # One small step on axis 1, nothing on the other five
    step = RobotJoints(100, 0, 0, 0, 0, 0)

    robot.rws.motion_system.jog(step, info.change_count, JogIncrementMode.Small)
finally:
    robot.rws.mastership.release(MastershipDomain.Motion)

# With JogIncrementMode.None_ the robot moves for as long as the command is repeated,
# so the loop itself is what stops the motion.
current = robot.rws.motion_system.get_info()
speed = RobotJoints(50, 0, 0, 0, 0, 0)

for i in range(20):
    robot.rws.motion_system.jog(speed, current.change_count, JogIncrementMode.None_)
    time.sleep(0.1)

# Some jogging requests are accepted by the controller and still not honoured.
# The error state says what went wrong.
error = robot.rws.motion_system.get_error_state()
print(f"{error.state}, {error.count} errors")

robot.disconnect()
```

`SetJoggingMechanicalUnit` chooses which unit the following jogging commands apply to. `Jog` then sends six values. How they are read depends on the jog mode of that unit, which `SetMechanicalUnit` sets:

| `JogMode`                  | The six values are                                                             |
| -------------------------- | ------------------------------------------------------------------------------ |
| `AxisGroup1`, `AxisGroup2` | One value per axis of the group                                                |
| `Cartesian`                | A motion of the tool along the axes of the active coordinate system            |
| `Align`                    | An alignment of the tool with the closest axis of the active coordinate system |
| `GoToPosition`             | A position to move to                                                          |
| `ConfigurationJog`         | A change of axis configuration that does not move the tool center point        |

`Jog` also takes the change count of the last reading of the motion system. The controller refuses a command built on a state that has moved on since, so read `GetInfo().ChangeCount` before jogging.

| `JogIncrementMode`         | Effect                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| `None`                     | The robot moves for as long as the command is repeated. The loop is what stops the motion. |
| `User`                     | One step of the size configured in the system parameters                                   |
| `Small`, `Medium`, `Large` | One step of the corresponding size                                                         |

A jogging request can be accepted by the controller and still not honoured. `GetErrorState` then says why, see the last section of this page.

**Methods of MotionSystemService** ([reference](../api/underautomation.abb.rws.services.md#motionsystemservice-robotrwsmotion_system))

- `jog(axes: RobotJoints, changeCount: int, incrementMode: JogIncrementMode=JogIncrementMode.None_) -> None`: Moves the mechanical unit currently selected for jogging (synchronous) The unit is the one chose, and how the six values are interpreted depends on its jog mode: axis by axis, along the axes of a coordinate system, and so on.
- `set_jogging_mechanical_unit(mechanicalUnit: str) -> None`: Chooses which mechanical unit the jogging commands apply to (synchronous)

**JogIncrementMode** ([reference](../api/underautomation.abb.rws.data.md#jogincrementmode))

- None_: The robot moves for as long as the command is repeated, with no fixed step
- User: One step of the size configured in the system parameters
- Small: One small step
- Medium: One medium step
- Large: One large step

## Kinematics

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

The controller can compute where the tool would be for a set of joint values, and which joint values put the tool at a given pose. Nothing moves, and no mastership is needed.

**These four calculations work in metres and radians**, unlike every other reading of the service. The values are passed and returned in the same classes, only the unit changes.

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

| Method                   | Answers                                                                   |
| ------------------------ | ------------------------------------------------------------------------- |
| `GetPoseFromJoints`      | Forward kinematics: the pose for these joint values                       |
| `GetJointsFromPose`      | Inverse kinematics: the joint values for this pose                        |
| `GetJointsFromCartesian` | The same question, through a second calculation of the controller         |
| `GetAllJointSolutions`   | Every joint combination that reaches the pose, one per axis configuration |

`GetJointsFromPose` and `GetJointsFromCartesian` take the same arguments and do not always return the same solution. Both are exposed because a controller can accept one and refuse the other. Compare the pose they reach rather than the joint values themselves.

`previousJoints` is what decides between the solutions a pose admits. Pass the joint values the robot is currently in, so the answer is the closest one.

Set `robotHoldsWorkObject` to true when the tool is fixed in the cell and the robot carries the work object. Set `logErrors` to true to have the controller write an event log message when the calculation fails.

A pose that cannot be reached is refused by the controller and reported as an `RwsException`.



**JointSolution** ([reference](../api/underautomation.abb.rws.data.md#jointsolution))

- `JointSolution()`: Initializes a new solution with every axis at zero
- `configuration: RobotConfiguration`: Axis configuration this solution corresponds to. Never null.
- Inherited from [JointTarget](../api/underautomation.abb.common.md#jointtarget): `robot_axes`, `external_axes`

## Collision supervision

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

The controller watches the torque of the axes and stops the robot when it meets an unexpected resistance. There is one setting for jogging and one for a programmed path, per mechanical unit.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# Collision detection while the unit is jogged
jogging = robot.rws.motion_system.get_motion_supervision("ROB_1")
print(f"jogging supervision {jogging.enabled}, sensitivity {jogging.level} %")

# Collision detection while the unit follows a programmed path
path = robot.rws.motion_system.get_path_supervision("ROB_1")
print(f"path supervision {path.enabled}, sensitivity {path.level} %")

# Writing these four values needs the mastership of the motion domain.
# The lower the percentage, the sooner the controller reports a collision.
robot.rws.mastership.request(MastershipDomain.Motion)

try:
    robot.rws.motion_system.set_motion_supervision_mode("ROB_1", True)
    robot.rws.motion_system.set_motion_supervision_level("ROB_1", 80)

    robot.rws.motion_system.set_path_supervision_mode("ROB_1", True)
    robot.rws.motion_system.set_path_supervision_level("ROB_1", 80)
finally:
    robot.rws.mastership.release(MastershipDomain.Motion)

# Collision prediction stops the robot before it hits something the controller
# knows about. It is a separate setting, and it needs no mastership.
predicting = robot.rws.motion_system.get_collision_prediction_mode()

if not predicting:
    # Refused when the collision detection option is not installed.
    # The error message then names the missing option.
    robot.rws.motion_system.set_collision_prediction_mode(True)

robot.disconnect()
```

| Setting             | Applies while                      |
| ------------------- | ---------------------------------- |
| `MotionSupervision` | The unit is jogged                 |
| `PathSupervision`   | The unit follows a programmed path |

The level is a percentage. The lower the value, the sooner the controller reports a collision. The four write methods need the mastership of the `Motion` domain.

Collision prediction is a different feature: it stops the robot before it hits something the controller already knows about, where the supervision only reacts once the arm meets a resistance. `GetCollisionPredictionMode` and `SetCollisionPredictionMode` need no mastership.

All of this belongs to the Collision Detection option. On a controller built without it, switching the feature on is refused with the HTTP status code 403 and the SDK reports an error naming the missing option. Writing back the value the controller already holds is accepted.

`SetNonMotionExecutionMode` is nearby but different: it runs the RAPID program while skipping every motion instruction, which is how a program is tested without the robot leaving its position. It belongs to the editing domain, not to the motion one, so take every domain before calling it.

**Methods of MotionSystemService** ([reference](../api/underautomation.abb.rws.services.md#motionsystemservice-robotrwsmotion_system))

- `get_motion_supervision(mechanicalUnit: str) -> MotionSupervision`: Gets the collision detection settings that apply while a mechanical unit is jogged (synchronous)
- `set_motion_supervision_mode(mechanicalUnit: str, enabled: bool) -> None`: Switches the jogging collision detection of a mechanical unit on or off (synchronous)
- `set_motion_supervision_level(mechanicalUnit: str, sensitivity: int) -> None`: Sets how sensitive the jogging collision detection of a mechanical unit is (synchronous)
- `get_path_supervision(mechanicalUnit: str) -> PathSupervision`: Gets the collision detection settings that apply while a mechanical unit follows a programmed path (synchronous)
- `set_path_supervision_mode(mechanicalUnit: str, enabled: bool) -> None`: Switches the path collision detection of a mechanical unit on or off (synchronous)
- `set_path_supervision_level(mechanicalUnit: str, level: int) -> None`: Sets how sensitive the path collision detection of a mechanical unit is (synchronous)

**MotionSupervision** ([reference](../api/underautomation.abb.rws.data.md#motionsupervision))

- `MotionSupervision()`: Initializes a new instance of the MotionSupervision class
- `enabled: bool | None`: Whether the supervision is switched on, null when the controller did not report it
- `level: int | None`: Sensitivity of the supervision, as a percentage: the lower the value, the sooner a collision is reported. Null when the controller did not report it.

**PathSupervision** ([reference](../api/underautomation.abb.rws.data.md#pathsupervision))

- `PathSupervision()`: Initializes a new instance of the PathSupervision class
- `enabled: bool | None`: Whether the supervision is switched on, null when the controller did not report it
- `level: int | None`: Sensitivity of the supervision, as a percentage: the lower the value, the sooner a collision is reported. Null when the controller did not report it.

## Lead through

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

Lead through releases the arm so an operator can push it around by hand. The motors have to be on and the robot has to support the feature. This is one of the two writes of the service that need no mastership.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Is the arm free to be pushed by hand right now
status = robot.rws.motion_system.get_lead_through("ROB_1")
print(status)

# Switching it on releases the arm: the motors have to be on, and the robot
# has to support lead through. This call needs no mastership.
robot.rws.motion_system.set_lead_through("ROB_1", True)

# Switching it off makes the arm hold its position again
robot.rws.motion_system.set_lead_through("ROB_1", False)

robot.disconnect()
```

`GetLeadThrough` returns `Active` when the arm gives way when pushed, and `Inactive` when it holds its position.



**LeadThroughStatus** ([reference](../api/underautomation.abb.rws.data.md#leadthroughstatus))

- Unknown: The controller reported a state this library does not know
- Active: The arm gives way when pushed
- Inactive: The arm holds its position

## Calibration

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

The calibration says where each axis really is. Reading it is safe and tells you why a unit reports something else than `Synchronized`.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.smb_data_status import SmbDataStatus

robot = AbbController()
robot.connect("192.168.0.1")

# How each joint of the unit was calibrated
calibration = robot.rws.motion_system.get_calibration_info("ROB_1")
print(f"method {calibration.calibration_method_used}, {calibration.existing_joint_count} joints")

# The controller always answers with more joint slots than the unit has.
# The extra ones carry no name and are marked as not existing.
for joint in calibration.joints:
    if not joint.exists:
        continue

    print(f"{joint.joint_name} : factory {joint.factory_calibration_method}, now {joint.current_calibration_method}")

# The name each joint carries, and the name of its calibration data
for name in robot.rws.motion_system.get_motor_calibration_names("ROB_1"):
    print(f"joint {name.number} : {name.joint_name}, data {name.calibration_name}")

# The calibration is stored twice: in the controller cabinet and in the robot itself.
# The two copies are meant to agree.
smb = robot.rws.motion_system.get_smb_data("ROB_1")

print(f"cabinet calibration {smb.cabinet_calibration_status}")
print(f"robot calibration   {smb.robot_calibration_status}")

if smb.cabinet_calibration_status == SmbDataStatus.ValidNotEqual:
    print("the two copies do not hold the same data")

robot.disconnect()
```

`GetCalibrationInfo` always answers with a fixed number of joint slots, larger than the number of joints the unit really has. The extra ones carry no name and have `Exists` set to false. `ExistingJointCount` counts the real ones.

The calibration data is stored twice, once in the controller cabinet and once in the robot itself. `GetSmbData` returns both copies with a status per block of data. `ValidNotEqual` means the two copies are present but do not agree.

The write operations replace the calibration of an axis. RWS offers no way to put the previous one back, so a wrong calibration leaves the robot moving to the wrong place until somebody recalibrates it from the FlexPendant. They need the mastership of the `Motion` domain, and the measurement board operations also need the controller in manual mode with this client as its local client.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from underautomation.abb.rws.data.mechanical_unit_status import MechanicalUnitStatus
from underautomation.abb.rws.data.smb_data_memory import SmbDataMemory
from underautomation.abb.rws.data.smb_data_transfer import SmbDataTransfer

robot = AbbController()
robot.connect("192.168.0.1")

# These four operations replace the calibration of an axis. RWS has no way to
# put the previous one back, so read the state first and be sure of the position
# the axis is standing in.
unit = robot.rws.motion_system.get_mechanical_unit("ROB_1")

if unit.status != MechanicalUnitStatus.Synchronized:
    print(f"ROB_1 is {unit.status}")

robot.rws.mastership.request(MastershipDomain.Motion)

try:
    # Teaches the controller how the rotor of the motor is oriented.
    # Needed once after a motor has been replaced.
    robot.rws.motion_system.commutate("ROB_1", 1)

    # Move the axis to its synchronization mark first: the controller stores
    # the position the axis is in right now.
    robot.rws.motion_system.synchronize_axis_revolution_counter("ROB_1", 1)
    robot.rws.motion_system.update_revolution_counter("ROB_1", 1)

    # Takes the current position of the axis as its new calibration position
    robot.rws.motion_system.fine_calibrate("ROB_1", 1)
finally:
    robot.rws.mastership.release(MastershipDomain.Motion)

# Copy one of the two calibration data stores over the other. The overwritten
# one is gone, so read both first and keep the good one.
robot.rws.motion_system.set_smb_data("ROB_1", SmbDataTransfer.RobotToController)

# Erase one of them. The controller cannot recover it.
robot.rws.motion_system.clear_smb_data("ROB_1", SmbDataMemory.Controller)

robot.disconnect()
```

| Method                             | Effect                                                                                                      |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `Commutate`                        | Teaches the controller how the rotor of the motor is oriented. Needed once after a motor has been replaced. |
| `SynchronizeAxisRevolutionCounter` | Tells the controller the axis stands at its synchronization mark                                            |
| `UpdateRevolutionCounter`          | Updates the revolution counter of the axis                                                                  |
| `FineCalibrate`                    | Takes the current position of the axis as its new calibration position                                      |
| `SetSmbData`                       | Copies one of the two data stores over the other                                                            |
| `ClearSmbData`                     | Erases one of the two data stores                                                                           |

For the three operations that store a position, move the axis to its synchronization mark first. The controller stores the position the axis is in at the moment of the call.

**Methods of MotionSystemService** ([reference](../api/underautomation.abb.rws.services.md#motionsystemservice-robotrwsmotion_system))

- `get_calibration_info(mechanicalUnit: str) -> CalibrationInfo`: Gets how each joint of a mechanical unit was calibrated (synchronous)
- `get_motor_calibration_names(mechanicalUnit: str) -> typing.List[MotorCalibrationName]`: Gets the name each joint of a mechanical unit carries, and the name of its calibration data (synchronous)
- `get_smb_data(mechanicalUnit: str) -> SmbData`: Gets the serial measurement board data of a mechanical unit, as held by the controller cabinet and by the robot itself (synchronous) The two copies are meant to agree. When they do not, one of them is written over the other with .
- `set_smb_data(mechanicalUnit: str, direction: SmbDataTransfer) -> None`: Copies one of the two serial measurement board data stores over the other (synchronous)
- `clear_smb_data(mechanicalUnit: str, memory: SmbDataMemory) -> None`: Erases one of the two serial measurement board data stores (synchronous)
- `commutate(mechanicalUnit: str, axis: int) -> None`: Commutates the motor of one axis, which teaches the controller how the rotor of that motor is oriented (synchronous) Needed once after a motor has been replaced, before the axis can be calibrated.
- `fine_calibrate(mechanicalUnit: str, axis: int) -> None`: Fine calibrates one axis of a mechanical unit (synchronous)

**CalibrationInfo** ([reference](../api/underautomation.abb.rws.data.md#calibrationinfo))

- `CalibrationInfo()`: Initializes a new instance of the CalibrationInfo class
- `calibration_window_type: int | None`: Kind of calibration window the controller offers for this unit, null when the controller did not report it
- `active_joint_count: int | None`: Number of joints of the unit that are in use, null when the controller did not report it
- `joint_count: int | None`: Number of entries in joints, which is fixed and larger than active_joint_count. Null when the controller did not report it.
- `calibration_method_used: str`: Name of the calibration method the unit was last calibrated with, for example "AxisCalibration"
- `joints: typing.List[CalibrationJointInfo]`: One entry per joint slot of the unit, the unused ones marked as such. Never null.
- `existing_joint_count: int (read only)`: Number of joints that exist on the unit, counted from joints

**CalibrationJointInfo** ([reference](../api/underautomation.abb.rws.data.md#calibrationjointinfo))

- `CalibrationJointInfo()`: Initializes a new instance of the CalibrationJointInfo class
- `exists: bool`: Whether the joint exists on this mechanical unit. The controller always answers with a fixed number of entries and marks the unused ones, which carry no name at all.
- `joint_name: str`: Name of the joint, for example "rob1_1", empty for an entry that does not exist
- `factory_calibration_method: str`: Method the joint was calibrated with in the factory
- `current_calibration_method: str`: Method the joint is currently calibrated with

**MotorCalibrationName** ([reference](../api/underautomation.abb.rws.data.md#motorcalibrationname))

- `MotorCalibrationName()`: Initializes a new instance of the MotorCalibrationName class
- `number: int`: Number of the joint inside its mechanical unit, starting at 1
- `joint_name: str`: Name of the joint, for example "rob1_1"
- `calibration_name: str`: Name of the calibration data of the joint, usually the same as joint_name

**SmbData** ([reference](../api/underautomation.abb.rws.data.md#smbdata))

- `SmbData()`: Initializes a new instance of the SmbData class
- `cabinet_serial_number_valid: bool | None`: Whether the serial number stored in the cabinet is usable, null when the controller did not report it
- `cabinet_serial_number_high_part: str`: High part of the serial number stored in the cabinet
- `cabinet_serial_number_low_part: str`: Low part of the serial number stored in the cabinet
- `cabinet_service_information_status: SmbDataStatus`: State of the service information data stored in the cabinet
- `cabinet_absolute_accuracy_status: SmbDataStatus`: State of the absolute accuracy data stored in the cabinet
- `cabinet_calibration_status: SmbDataStatus`: State of the calibration data stored in the cabinet
- `cabinet_axis_calibration_status: SmbDataStatus`: State of the axis calibration data stored in the cabinet
- `robot_serial_number_valid: bool | None`: Whether the serial number stored in the robot is usable, null when the controller did not report it
- `robot_serial_number_high_part: str`: High part of the serial number stored in the robot
- `robot_serial_number_low_part: str`: Low part of the serial number stored in the robot
- `robot_service_information_status: SmbDataStatus`: State of the service information data stored in the robot
- `robot_absolute_accuracy_status: SmbDataStatus`: State of the absolute accuracy data stored in the robot
- `robot_calibration_status: SmbDataStatus`: State of the calibration data stored in the robot
- `robot_axis_calibration_status: SmbDataStatus`: State of the axis calibration data stored in the robot
- `drive_module: int | None`: Number of the drive module the data belongs to, null when the controller did not report it
- `measurement_link: int | None`: Number of the measurement link the data belongs to, null when the controller did not report it
- `measurement_board: int | None`: Number of the measurement board the data belongs to, null when the controller did not report it

**SmbDataStatus** ([reference](../api/underautomation.abb.rws.data.md#smbdatastatus))

- Unknown: The controller reported a state this library does not know
- Valid: The data is present and the two copies agree
- ValidNotEqual: The data is present on both sides, but the two copies differ
- NotValid: The data is missing or unusable
- NotUsed: The robot system does not use this block of data

**SmbDataTransfer** ([reference](../api/underautomation.abb.rws.data.md#smbdatatransfer))

- RobotToController: The copy held by the robot is written into the controller cabinet
- ControllerToRobot: The copy held by the controller cabinet is written into the robot

**SmbDataMemory** ([reference](../api/underautomation.abb.rws.data.md#smbdatamemory))

- Robot: The copy held by the robot itself
- Controller: The copy held by the controller cabinet

## State of the motion system

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

`GetInfo` gives the overview: which unit the jogging commands apply to, whether absolute accuracy is on, and the change count.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.motion_error_state import MotionErrorState

robot = AbbController()
robot.connect("192.168.0.1")

# Overview of the motion system: which unit the jogging commands apply to,
# and the counter the controller increments on every change
info = robot.rws.motion_system.get_info()
print(f"jogging applies to {info.mechanical_unit_name}")
print(f"change count {info.change_count}, absolute accuracy {info.absolute_accuracy_active}")

# Ask whether anything moved since that reading, instead of reading everything again
if info.change_count is not None and robot.rws.motion_system.has_changed(info.change_count):
    print("the motion system changed")

# The last error the motion system ran into. Most of them come from a jogging
# request the controller accepted and could not honour.
error = robot.rws.motion_system.get_error_state()

if error.state != MotionErrorState.Ok:
    print(f"{error.state} ({error.raw_state}), {error.count} errors")

# Run the RAPID program without moving the robot. The instructions execute,
# the motion ones are skipped.
skipped = robot.rws.motion_system.get_non_motion_execution_mode()

# The motion domain alone is not enough here, the controller answers 403.
# In Python the domains are taken one by one, so take the ones it exposes.
domains = robot.rws.mastership.get_domains()

for domain in domains:
    robot.rws.mastership.request(domain)

try:
    robot.rws.motion_system.set_non_motion_execution_mode(True)
finally:
    for domain in domains:
        robot.rws.mastership.release(domain)

robot.disconnect()
```

The change count is a counter the controller increments on every change of the motion system. Reading it once and asking `HasChanged` afterwards is cheaper than fetching the whole state again to find out that nothing moved. Only pass a count a previous reading gave: the controller does not track how two counts relate, so a count it never reported comes back as changed.

`GetErrorState` returns the last error the motion system ran into and how many it has counted. Most of them come from a jogging request the controller accepted and could not honour, and they stay reported until a new one replaces them.

| `MotionErrorState`                 | Meaning                                                                              |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| `Ok`                               | No error                                                                             |
| `MechanicalUnitNotActive`          | A mechanical unit was jogged whose activation failed                                 |
| `UncalibratedJogMotionType`        | An uncalibrated robot was jogged in a mode that needs its calibration                |
| `UnnormalizedQuaternion`           | A tool, a load or a work object carries an orientation that is not normalized        |
| `ErroneousToolMass`                | A load definition carries a negative mass                                            |
| `RobotHoldMismatch`                | The tool and the work object disagree on which one the robot holds                   |
| `WorkObjectMechanicalUnitNotFound` | A unit used in coordinated jogging was not found                                     |
| `InvalidJogMotionType`             | The requested jogging mode is not valid                                              |
| `Unknown`                          | The controller reported an error the library does not know, `RawState` then holds it |



**MotionSystemInfo** ([reference](../api/underautomation.abb.rws.data.md#motionsysteminfo))

- `MotionSystemInfo()`: Initializes a new instance of the MotionSystemInfo class
- `change_count: int | None`: Counter the controller increments on every change of the motion system. Pass it to MotionSystemService.HasChanged() to find out whether anything moved since a previous reading, without fetching the whole state again.
- `mechanical_unit_name: str`: Name of the mechanical unit the jogging commands currently apply to
- `poll_rate: int | None`: Rate at which the controller refreshes the motion system state, null when it did not report it
- `modal_payload_mode: bool | None`: Whether the payload of the robot is set by the running program rather than by the mechanical unit, null when the controller did not report it
- `absolute_accuracy_active: bool | None`: Whether absolute accuracy is switched on, null when the controller did not report it

**MotionSystemErrorState** ([reference](../api/underautomation.abb.rws.data.md#motionsystemerrorstate))

- `MotionSystemErrorState()`: Initializes a new instance of the MotionSystemErrorState class
- `state: MotionErrorState`: Last error the motion system ran into
- `raw_state: str`: Error state exactly as the controller reported it, useful when state is Unknown
- `count: int | None`: Number of errors counted since the controller started, incremented on every new error, null when the controller did not report it

**MotionErrorState** ([reference](../api/underautomation.abb.rws.data.md#motionerrorstate))

- Unknown: The controller reported an error this library does not know
- Ok: No error
- MechanicalUnitNotActive: A mechanical unit was jogged whose activation failed
- UncalibratedJogMotionType: An uncalibrated robot was jogged in a mode that needs its calibration
- UnnormalizedQuaternion: A quaternion that is not normalized reached the jogging task, from a tool, a load or a work object
- ErroneousToolMass: A load definition carries a negative mass
- RobotHoldMismatch: The tool and the work object disagree on which one the robot holds
- WorkObjectMechanicalUnitNotFound: A mechanical unit used in coordinated jogging was not found
- InvalidJogMotionType: The requested jogging mode is not valid

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).
