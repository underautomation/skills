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

**Position** ([reference](../api/UnderAutomation.ABB.Common.md#position))

- `Position()`: Initializes a new position at the origin
- `Position(double x, double y, double z)`: Initializes a new position
- `double X { get; set; }`: Coordinate along the X axis
- `double Y { get; set; }`: Coordinate along the Y axis
- `double Z { get; set; }`: Coordinate along the Z axis

**Quaternion** ([reference](../api/UnderAutomation.ABB.Common.md#quaternion))

- `Quaternion()`: Initializes a new quaternion with no rotation at all (1, 0, 0, 0)
- `Quaternion(double q1, double q2, double q3, double q4)`: Initializes a new quaternion
- `double Q1 { get; set; }`: Real component of the quaternion
- `double Q2 { get; set; }`: First imaginary component of the quaternion
- `double Q3 { get; set; }`: Second imaginary component of the quaternion
- `double Q4 { get; set; }`: Third imaginary component of the quaternion

**Pose** ([reference](../api/UnderAutomation.ABB.Common.md#pose))

- `Pose()`: Initializes a new pose at the origin, with no rotation
- `Pose(double x, double y, double z, double q1, double q2, double q3, double q4)`: Initializes a new pose
- `Pose(double x, double y, double z, Quaternion orientation)`: Initializes a new pose
- `Quaternion Orientation { get; set; }`: Orientation held at this position. Never null: a pose built without one carries the identity rotation.
- Inherited from [Position](../api/UnderAutomation.ABB.Common.md#position): `X`, `Y`, `Z`

**RobotConfiguration** ([reference](../api/UnderAutomation.ABB.Common.md#robotconfiguration))

- `RobotConfiguration()`: Initializes a new configuration with every quarter revolution set to zero
- `RobotConfiguration(int quarter1, int quarter4, int quarter6, int quarterX)`: Initializes a new configuration
- `int Quarter1 { get; set; }`: Quarter revolution axis 1 sits in
- `int Quarter4 { get; set; }`: Quarter revolution axis 4 sits in
- `int Quarter6 { get; set; }`: Quarter revolution axis 6 sits in
- `int QuarterX { get; set; }`: Index of the arm configuration, which tells the remaining joint combinations apart

**RobotJoints** ([reference](../api/UnderAutomation.ABB.Common.md#robotjoints))

- `RobotJoints()`: Initializes the six axes to zero
- `RobotJoints(double axis1, double axis2, double axis3, double axis4, double axis5, double axis6)`: Initializes the six axes
- `double Axis1 { get; set; }`: Value of axis 1
- `double Axis2 { get; set; }`: Value of axis 2
- `double Axis3 { get; set; }`: Value of axis 3
- `double Axis4 { get; set; }`: Value of axis 4
- `double Axis5 { get; set; }`: Value of axis 5
- `double Axis6 { get; set; }`: Value of axis 6

**ExternalJoints** ([reference](../api/UnderAutomation.ABB.Common.md#externaljoints))

- `ExternalJoints()`: Initializes the six external axes to zero
- `ExternalJoints(double axisA, double axisB, double axisC, double axisD, double axisE, double axisF)`: Initializes the six external axes
- `double AxisA { get; set; }`: Value of external axis A
- `double AxisB { get; set; }`: Value of external axis B
- `double AxisC { get; set; }`: Value of external axis C
- `double AxisD { get; set; }`: Value of external axis D
- `double AxisE { get; set; }`: Value of external axis E
- `double AxisF { get; set; }`: Value of external axis F
- `const double NotInUse = 9000000000`: Value the controller reports for an external axis that is not in use

**RobTarget** ([reference](../api/UnderAutomation.ABB.Common.md#robtarget))

- `RobTarget()`: Initializes a new target at the origin, with no rotation
- `RobTarget(double x, double y, double z, Quaternion orientation, RobotConfiguration configuration, ExternalJoints externalAxes)`: Initializes a new target
- `RobotConfiguration Configuration { get; set; }`: Axis configuration used to reach the pose. Never null.
- `ExternalJoints ExternalAxes { get; set; }`: Values of the six external axes, null when the reading does not report them
- Inherited from [Pose](../api/UnderAutomation.ABB.Common.md#pose): `Orientation`
- Inherited from [Position](../api/UnderAutomation.ABB.Common.md#position): `X`, `Y`, `Z`

**JointTarget** ([reference](../api/UnderAutomation.ABB.Common.md#jointtarget))

- `JointTarget()`: Initializes a new joint target with every axis at zero
- `JointTarget(RobotJoints robotAxes, ExternalJoints externalAxes)`: Initializes a new joint target
- `ExternalJoints ExternalAxes { get; set; }`: Values of the six external axes. Never null.
- `RobotJoints RobotAxes { get; set; }`: Values of the six axes of the robot arm. Never null.

## Mechanical units

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

A mechanical unit is anything the controller drives: the robot arm itself, a track, a positioner. `GetMechanicalUnits` lists them, `GetMechanicalUnit` describes one of them, and `SetMechanicalUnit` changes its properties.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Common;
using UnderAutomation.ABB.Rws.Data;

public class MotionUnits
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Every mechanical unit of the system, with its activation state
        foreach (MechanicalUnitItem unit in robot.Rws.MotionSystem.GetMechanicalUnits())
        {
            Console.WriteLine($"{unit.Name} : {unit.Mode}, drive module {unit.DriveModule}");
        }

        // Everything the controller knows about one unit
        MechanicalUnitInfo info = robot.Rws.MotionSystem.GetMechanicalUnit("ROB_1");
        Console.WriteLine($"{info.Type}, task {info.TaskName}, status {info.Status}");
        Console.WriteLine($"tool {info.ToolName}, work object {info.WorkObjectName}, payload {info.PayloadName}");
        Console.WriteLine($"{info.Axes} axes, jog mode {info.JogMode}, frame {info.CoordinateSystem}");

        // Axis by axis. Axes are numbered from 1.
        int axisCount = robot.Rws.MotionSystem.GetAxisCount("ROB_1");

        for (int axis = 1; axis <= axisCount; axis++)
        {
            AxisInfo axisInfo = robot.Rws.MotionSystem.GetAxis("ROB_1", axis);
            Pose axisPose = robot.Rws.MotionSystem.GetAxisPose("ROB_1", axis);

            Console.WriteLine($"axis {axisInfo.Number} : {axisInfo.Status}, at {axisPose}");
        }

        // Where the base of the unit stands, in millimetres
        BaseFrame baseFrame = robot.Rws.MotionSystem.GetBaseFrame("ROB_1");
        Console.WriteLine($"base frame {baseFrame}, type {baseFrame.Type}");

        // Changing a property of a unit needs the mastership of the motion domain.
        // Give only the properties you want to change, leave the others null.
        robot.Rws.Mastership.Request(MastershipDomain.Motion);

        try
        {
            robot.Rws.MotionSystem.SetMechanicalUnit("ROB_1",
                                                     tool: "tGripper",
                                                     jogMode: JogMode.Cartesian,
                                                     coordinateSystem: CoordinateSystem.Base);
        }
        finally
        {
            robot.Rws.Mastership.Release();
        }

        // The controller answers success even when it could not apply one of the properties.
        // Read the unit back to see what it really did.
        Console.WriteLine(robot.Rws.MotionSystem.GetMechanicalUnit("ROB_1").ToolName);

        // Declaring where a base or an axis sits changes the calibration of the cell.
        // The user account needs the matching UAS grant.
        Pose newBase = new Pose(0, 0, 0, new Quaternion(1, 0, 0, 0));
        robot.Rws.MotionSystem.SetBaseFrame("ROB_1", newBase);
        robot.Rws.MotionSystem.SetAxisPose("ROB_1", 1, newBase);

        robot.Disconnect();
    }
}
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

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `AxisInfo GetAxis(string mechanicalUnit, int axis)`: Gets the state of one axis of a mechanical unit (synchronous)
  - async: `Task<AxisInfo> GetAxisAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `int GetAxisCount(string mechanicalUnit)`: Gets how many axes a mechanical unit has (synchronous)
  - async: `Task<int> GetAxisCountAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `Pose GetAxisPose(string mechanicalUnit, int axis)`: Gets where one axis of a mechanical unit sits (synchronous) The position is expressed in millimetres.
  - async: `Task<Pose> GetAxisPoseAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `BaseFrame GetBaseFrame(string mechanicalUnit)`: Gets where the base of a mechanical unit sits (synchronous) The position is expressed in millimetres.
  - async: `Task<BaseFrame> GetBaseFrameAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `MechanicalUnitInfo GetMechanicalUnit(string mechanicalUnit)`: Gets everything the controller knows about one mechanical unit (synchronous)
  - async: `Task<MechanicalUnitInfo> GetMechanicalUnitAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `MechanicalUnitItem[] GetMechanicalUnits()`: Lists the mechanical units of the motion system (synchronous)
  - async: `Task<MechanicalUnitItem[]> GetMechanicalUnitsAsync(CancellationToken cancellationToken = default)`
- `void SetAxisPose(string mechanicalUnit, int axis, Pose pose)`: Declares where one axis of a mechanical unit sits (synchronous) The position is expressed in millimetres.
  - async: `Task SetAxisPoseAsync(string mechanicalUnit, int axis, Pose pose, CancellationToken cancellationToken = default)`
- `void SetBaseFrame(string mechanicalUnit, Pose baseFrame)`: Declares where the base of a mechanical unit sits (synchronous) The position is expressed in millimetres.
  - async: `Task SetBaseFrameAsync(string mechanicalUnit, Pose baseFrame, CancellationToken cancellationToken = default)`
- `void SetMechanicalUnit(string mechanicalUnit, string tool = null, string workObject = null, string payload = null, string totalPayload = null, MechanicalUnitMode? mode = null, JogMode? jogMode = null, CoordinateSystem? coordinateSystem = null)`: Changes one or several properties of a mechanical unit (synchronous) Every argument but the unit name is optional; leave the ones you do not want to touch null. At least one of them has to be given.
  - async: `Task SetMechanicalUnitAsync(string mechanicalUnit, string tool = null, string workObject = null, string payload = null, string totalPayload = null, MechanicalUnitMode? mode = null, JogMode? jogMode = null, CoordinateSystem? coordinateSystem = null, CancellationToken cancellationToken = default)`
- `void SetMechanicalUnitPosition(string mechanicalUnit, JointTarget position)`: Places a mechanical unit at the given joint values without moving it there (synchronous) Only a virtual controller accepts this: it teleports the simulated robot, which a real one cannot do.
  - async: `Task SetMechanicalUnitPositionAsync(string mechanicalUnit, JointTarget position, CancellationToken cancellationToken = default)`

**MechanicalUnitItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#mechanicalunititem))

- `MechanicalUnitItem()`: Initializes a new instance of the Data.MechanicalUnitItem class
- `bool? ActivationAllowed { get; set; }`: Whether the unit can be activated, null when the controller did not report it
- `int? DriveModule { get; set; }`: Number of the drive module the unit is connected to, null when the controller did not report it
- `MechanicalUnitMode Mode { get; set; }`: Whether the unit is activated
- `string Name { get; set; }`: Name of the mechanical unit, for example "ROB_1"

**MechanicalUnitInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#mechanicalunitinfo))

- `MechanicalUnitInfo()`: Initializes a new instance of the Data.MechanicalUnitInfo class
- `int? Axes { get; set; }`: Number of axes of the unit, null when the controller did not report it
- `CoordinateSystem CoordinateSystem { get; set; }`: Reference frame the cartesian positions of the unit are expressed in
- `string HasIntegratedUnit { get; set; }`: Name of the mechanical unit integrated into this one. A unit that integrates no other one is reported with a placeholder name rather than an empty value.
- `string IsIntegratedUnit { get; set; }`: Name of the mechanical unit this one is integrated into. A unit that is integrated into no other one is reported with a placeholder name rather than an empty value.
- `JogMode JogMode { get; set; }`: How the jogging commands sent to the unit are interpreted
- `MechanicalUnitMode Mode { get; set; }`: Whether the unit is activated
- `string Name { get; set; }`: Name of the mechanical unit, for example "ROB_1"
- `string PayloadName { get; set; }`: Name of the active payload
- `MechanicalUnitStatus Status { get; set; }`: Calibration and synchronization state of the unit
- `string TaskName { get; set; }`: Name of the RAPID task that drives the unit
- `string ToolName { get; set; }`: Name of the active tool
- `int? TotalAxes { get; set; }`: Number of axes of the unit and of the units integrated with it, null when the controller did not report it
- `string TotalPayloadName { get; set; }`: Name of the active total payload, which is the payload plus the load of the tool
- `MechanicalUnitType Type { get; set; }`: Kind of mechanical unit
- `string WorkObjectName { get; set; }`: Name of the active work object

**MechanicalUnitMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#mechanicalunitmode))

- Activated: The mechanical unit is activated and takes part in the motion
- Deactivated: The mechanical unit is deactivated and stays where it is
- Unknown: The controller reported a mode this library does not know

**MechanicalUnitType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#mechanicalunittype))

- None: No mechanical unit
- Robot: A robot arm without a tool center point, which can only be moved axis by axis
- Single: A single external axis, such as a track or a positioner
- TcpRobot: A robot arm holding a tool center point, which can be moved in cartesian coordinates
- Undefined: The controller knows the unit but does not report what it is
- Unknown: The controller reported a type this library does not know

**MechanicalUnitStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#mechanicalunitstatus))

- Initiated: The unit is starting up
- Locked: The unit is locked and refuses to move
- LockedShow: The unit is locked, and the controller shows it as such
- NotAbsoluteSynchronized: One or several absolute measurement axes are not synchronized
- NotCalibrated: The unit has never been calibrated
- NotCommutated: One or several motors have not been commutated
- NotRelativeSynchronized: One or several relative measurement axes are not synchronized
- Synchronized: The unit is calibrated and synchronized, and can be moved
- Undefined: The controller knows the unit but does not report its state
- Unknown: The controller reported a state this library does not know

**AxisInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#axisinfo))

- `AxisInfo()`: Initializes a new instance of the Data.AxisInfo class
- `int? LogicalAxis { get; set; }`: Logical joint number of the axis, null when the controller did not report it
- `int Number { get; set; }`: Number of the axis inside its mechanical unit, starting at 1
- `MechanicalUnitStatus Status { get; set; }`: Calibration and synchronization state of the axis

**BaseFrame** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#baseframe))

- `BaseFrame()`: Initializes a new base frame at the origin, with no rotation
- `string Type { get; set; }`: Kind of base frame the controller reports, for example "IRBRobot"
- Inherited from [Pose](../api/UnderAutomation.ABB.Common.md#pose): `Orientation`
- Inherited from [Position](../api/UnderAutomation.ABB.Common.md#position): `X`, `Y`, `Z`

**CoordinateSystem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#coordinatesystem))

- Base: The base frame of the mechanical unit
- Tool: The frame of the active tool
- Unknown: The controller reported a frame this library does not know
- WorkObject: The frame of the active work object
- World: The world frame, shared by every mechanical unit of the system

**JogMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#jogmode))

- Align: The tool is aligned with the closest axis of the active coordinate system
- AxisGroup1: Each command moves one axis of the first axis group
- AxisGroup2: Each command moves one axis of the second axis group
- Cartesian: The tool is moved along the axes of the active coordinate system
- ConfigurationJog: The robot changes axis configuration without moving the tool center point
- GoToPosition: The robot moves to a given position
- Unknown: The controller reported a mode this library does not know

## Read the robot position

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

Four readings answer the same question in four ways. All of them are read only and need no mastership.

| Method                       | Returns                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------- |
| `GetRobTarget(unit)`         | `RobTarget`, the Cartesian position with the axis configuration and the external axes |
| `GetCartesianPosition(unit)` | `RobTarget` without the external axes, `ExternalAxes` is then null                    |
| `GetJointTarget(unit)`       | `JointTarget`, the joint values                                                       |
| `GetPhysicalJoints(unit)`    | `RobotJoints`, the raw values of the measurement system of the unit                   |

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Common;
using UnderAutomation.ABB.Rws.Data;

public class PositionRead
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Where the tool is, in millimetres, with the axis configuration and the external axes
        RobTarget target = robot.Rws.MotionSystem.GetRobTarget("ROB_1");
        Console.WriteLine($"X={target.X} Y={target.Y} Z={target.Z}");
        Console.WriteLine($"orientation {target.Orientation}");
        Console.WriteLine($"configuration {target.Configuration}");
        Console.WriteLine($"external axes {target.ExternalAxes}");

        // The same reading in another frame, with a given tool and work object
        RobTarget inWorld = robot.Rws.MotionSystem.GetRobTarget("ROB_1", CoordinateSystem.World,
                                                                tool: "tGripper", workObject: "wobj0");
        Console.WriteLine(inWorld);

        // The joint values, robot axes in degrees
        JointTarget joints = robot.Rws.MotionSystem.GetJointTarget("ROB_1");
        Console.WriteLine($"axis 1 = {joints.RobotAxes.Axis1} deg");
        Console.WriteLine($"axis 2 = {joints.RobotAxes.Axis2} deg");

        // An external axis the system does not define comes back as ExternalJoints.NotInUse
        if (joints.ExternalAxes.AxisA != ExternalJoints.NotInUse)
        {
            Console.WriteLine($"external axis A = {joints.ExternalAxes.AxisA}");
        }

        // alwaysRead asks the controller to measure again instead of answering with the value it holds
        JointTarget measured = robot.Rws.MotionSystem.GetJointTarget("ROB_1", alwaysRead: true);
        Console.WriteLine(measured);

        // Cartesian position without the external axes. ExternalAxes is null here.
        RobTarget cartesian = robot.Rws.MotionSystem.GetCartesianPosition("ROB_1");
        Console.WriteLine(cartesian);

        // The raw values of the measurement system of the unit
        RobotJoints physical = robot.Rws.MotionSystem.GetPhysicalJoints("ROB_1");
        Console.WriteLine(physical);

        // The same two positions seen from a RAPID task instead of a mechanical unit
        RobTarget taskTarget = robot.Rws.Rapid.GetRobTarget("T_ROB1");
        JointTarget taskJoints = robot.Rws.Rapid.GetJointTarget("T_ROB1");

        // Which external joints of the task carry a real value
        RapidExternalJointStates states = robot.Rws.Rapid.GetExternalJointStates("T_ROB1");
        Console.WriteLine($"external joint 1 : {states.Joint1}");

        // The units the task can move
        foreach (RapidMechanicalUnitItem unit in robot.Rws.Rapid.GetMechanicalUnits("T_ROB1"))
        {
            Console.WriteLine($"{unit.Name} : {unit.Type}, {unit.Mode}");
        }

        robot.Disconnect();
    }
}
```

`GetRobTarget` takes a `CoordinateSystem`, a tool and a work object. Without them it answers in the base frame of the unit, with the tool and the work object currently active on it. Passing a tool that does not exist is refused by the controller.

`GetJointTarget` has an `alwaysRead` parameter. By default the controller answers with the value it already holds. With `alwaysRead: true` it measures the position again, which costs more and is what you want when the robot has just moved.

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `RobTarget GetCartesianPosition(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null, bool logErrors = false)`: Gets where the tool of a mechanical unit currently is, without the external axes (synchronous) The position is expressed in millimetres.
  - async: `Task<RobTarget> GetCartesianPositionAsync(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null, bool logErrors = false, CancellationToken cancellationToken = default)`
- `JointTarget GetJointTarget(string mechanicalUnit, bool alwaysRead = false)`: Gets the joint values a mechanical unit currently stands at (synchronous) The robot axes are expressed in degrees.
  - async: `Task<JointTarget> GetJointTargetAsync(string mechanicalUnit, bool alwaysRead = false, CancellationToken cancellationToken = default)`
- `RobotJoints GetPhysicalJoints(string mechanicalUnit)`: Gets the physical joint values of a mechanical unit, as its measurement system reads them (synchronous)
  - async: `Task<RobotJoints> GetPhysicalJointsAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `RobTarget GetRobTarget(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null)`: Gets where the tool of a mechanical unit currently is (synchronous) The position is expressed in millimetres.
  - async: `Task<RobTarget> GetRobTargetAsync(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null, CancellationToken cancellationToken = default)`

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

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidExternalJointStates GetExternalJointStates(string task)`: Gets what each of the six external joints of a task is doing (synchronous) This is what says how to read the corresponding value of GetJointTarget(System.String): a joint reported as not active carries no meaningful position.
  - async: `Task<RapidExternalJointStates> GetExternalJointStatesAsync(string task, CancellationToken cancellationToken = default)`
- `JointTarget GetJointTarget(string task)`: Gets the joint values of the robot of a task (synchronous)
  - async: `Task<JointTarget> GetJointTargetAsync(string task, CancellationToken cancellationToken = default)`
- `RapidMechanicalUnitItem[] GetMechanicalUnits(string task)`: Gets the mechanical units the positions of a task are expressed in (synchronous)
  - async: `Task<RapidMechanicalUnitItem[]> GetMechanicalUnitsAsync(string task, CancellationToken cancellationToken = default)`
- `RobTarget GetRobTarget(string task, string tool = null, string workObject = null)`: Gets where the tool of a task currently stands, as a position and an orientation (synchronous)
  - async: `Task<RobTarget> GetRobTargetAsync(string task, string tool = null, string workObject = null, CancellationToken cancellationToken = default)`

**RapidExternalJointStates** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidexternaljointstates))

- `RapidExternalJointStates()`: Initializes a new instance of the Data.RapidExternalJointStates class
- `RapidJointState Joint1 { get; set; }`: State of the first external joint
- `RapidJointState Joint2 { get; set; }`: State of the second external joint
- `RapidJointState Joint3 { get; set; }`: State of the third external joint
- `RapidJointState Joint4 { get; set; }`: State of the fourth external joint
- `RapidJointState Joint5 { get; set; }`: State of the fifth external joint
- `RapidJointState Joint6 { get; set; }`: State of the sixth external joint

**RapidJointState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidjointstate))

- Linear: The joint moves along a line
- NoPosition: The joint is active but has no position
- NotActive: The joint is not active
- Rotating: The joint turns
- Unknown: The controller reported a state this library does not know

**RapidMechanicalUnitItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmechanicalunititem))

- `RapidMechanicalUnitItem()`: Initializes a new instance of the Data.RapidMechanicalUnitItem class
- `MechanicalUnitMode Mode { get; set; }`: Whether the unit is activated
- `string Name { get; set; }`: Name of the unit, for example "ROB_1"
- `MechanicalUnitType Type { get; set; }`: Kind of unit

## Move to a target

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

`SetPositionTarget` sends the robot to a Cartesian target. It really moves the arm. The preconditions are the same as for jogging: the controller in manual mode, the motors on, this client as the local client of the controller, and the mastership of the `Motion` domain.

`SetMechanicalUnitPosition` does not move anything. It places the unit at the given joint values. Only a virtual controller accepts it, a real one refuses the call.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Common;
using UnderAutomation.ABB.Rws.Data;

public class PositionSet
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // SetPositionTarget really moves the robot to a cartesian target.
        // Same preconditions as jogging: manual mode, motors on, local client, motion mastership.
        RobTarget target = robot.Rws.MotionSystem.GetRobTarget("ROB_1");
        target.Z += 10; // 10 mm up

        robot.Rws.Mastership.Request(MastershipDomain.Motion);

        try
        {
            robot.Rws.MotionSystem.SetPositionTarget(target);
        }
        finally
        {
            robot.Rws.Mastership.Release();
        }

        // SetMechanicalUnitPosition does not move anything: it places the unit at the given joint
        // values. Only a virtual controller accepts it, a real one refuses the call.
        JointTarget joints = new JointTarget(new RobotJoints(0, 0, 0, 0, 30, 0), new ExternalJoints());

        robot.Rws.Mastership.Request(MastershipDomain.Motion);

        try
        {
            robot.Rws.MotionSystem.SetMechanicalUnitPosition("ROB_1", joints);
        }
        finally
        {
            robot.Rws.Mastership.Release();
        }

        robot.Disconnect();
    }
}
```

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `void SetMechanicalUnitPosition(string mechanicalUnit, JointTarget position)`: Places a mechanical unit at the given joint values without moving it there (synchronous) Only a virtual controller accepts this: it teleports the simulated robot, which a real one cannot do.
  - async: `Task SetMechanicalUnitPositionAsync(string mechanicalUnit, JointTarget position, CancellationToken cancellationToken = default)`
- `void SetPositionTarget(RobTarget target)`: Sends the robot to a cartesian target (synchronous) The position is expressed in millimetres, in the coordinate system currently active for the mechanical unit selected for jogging.
  - async: `Task SetPositionTargetAsync(RobTarget target, CancellationToken cancellationToken = default)`

## Jog the robot

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

Jogging moves the robot step by step, the way the operator does from the FlexPendant. Four conditions have to be met, and none of them can be arranged by a request:

1. The controller is in manual mode. In automatic mode the request is refused with the HTTP status code 403.
2. The motors are on.
3. This client is the local client of the controller.
4. This connection holds the mastership of the `Motion` domain.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Common;
using UnderAutomation.ABB.Rws.Data;

public class JogRobot
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Check the preconditions before asking the robot to move
        OperationMode mode = robot.Rws.Panel.GetOperationMode();
        ControllerState state = robot.Rws.Panel.GetControllerState();

        if (mode == OperationMode.Automatic || state != ControllerState.MotorsOn)
        {
            Console.WriteLine("Jogging is refused in this state");
            return;
        }

        robot.Rws.Mastership.Request(MastershipDomain.Motion);

        try
        {
            // Which unit the jogging commands apply to
            robot.Rws.MotionSystem.SetJoggingMechanicalUnit("ROB_1");

            // How the six values are read depends on the jog mode of that unit
            robot.Rws.MotionSystem.SetMechanicalUnit("ROB_1", jogMode: JogMode.AxisGroup1);

            // The change count of the last reading. The controller refuses a command
            // built on a state that has moved on since.
            MotionSystemInfo info = robot.Rws.MotionSystem.GetInfo();

            // One small step on axis 1, nothing on the other five
            RobotJoints step = new RobotJoints(100, 0, 0, 0, 0, 0);

            robot.Rws.MotionSystem.Jog(step, info.ChangeCount.Value, JogIncrementMode.Small);
        }
        finally
        {
            robot.Rws.Mastership.Release();
        }

        // With JogIncrementMode.None the robot moves for as long as the command is repeated,
        // so the loop itself is what stops the motion.
        MotionSystemInfo current = robot.Rws.MotionSystem.GetInfo();
        RobotJoints speed = new RobotJoints(50, 0, 0, 0, 0, 0);

        for (int i = 0; i < 20; i++)
        {
            robot.Rws.MotionSystem.Jog(speed, current.ChangeCount.Value, JogIncrementMode.None);
            System.Threading.Thread.Sleep(100);
        }

        // Some jogging requests are accepted by the controller and still not honoured.
        // The error state says what went wrong.
        MotionSystemErrorState error = robot.Rws.MotionSystem.GetErrorState();
        Console.WriteLine($"{error.State}, {error.Count} error(s)");

        robot.Disconnect();
    }
}
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

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `void Jog(RobotJoints axes, int changeCount, JogIncrementMode incrementMode = JogIncrementMode.None)`: Moves the mechanical unit currently selected for jogging (synchronous) The unit is the one SetJoggingMechanicalUnit(System.String) chose, and how the six values are interpreted depends on its jog mode: axis by axis, along the axes of a coordinate system, and so on.
  - async: `Task JogAsync(RobotJoints axes, int changeCount, JogIncrementMode incrementMode = JogIncrementMode.None, CancellationToken cancellationToken = default)`
- `void SetJoggingMechanicalUnit(string mechanicalUnit)`: Chooses which mechanical unit the jogging commands apply to (synchronous)
  - async: `Task SetJoggingMechanicalUnitAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`

**JogIncrementMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#jogincrementmode))

- Large: One large step
- Medium: One medium step
- None: The robot moves for as long as the command is repeated, with no fixed step
- Small: One small step
- User: One step of the size configured in the system parameters

## Kinematics

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

The controller can compute where the tool would be for a set of joint values, and which joint values put the tool at a given pose. Nothing moves, and no mastership is needed.

**These four calculations work in metres and radians**, unlike every other reading of the service. The values are passed and returned in the same classes, only the unit changes.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Common;
using UnderAutomation.ABB.Rws.Data;

public class Kinematics
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // These four calculations work in metres and radians, not in millimetres and degrees.

        // Tool relative to the mounting flange. Here the flange itself, with no rotation.
        Pose toolFrame = new Pose(0, 0, 0, new Quaternion(1, 0, 0, 0));

        // Forward kinematics: where the tool would be for these joint values
        JointTarget joints = new JointTarget(new RobotJoints(0, 0, 0, 0, 0.5, 0), new ExternalJoints());

        RobTarget pose = robot.Rws.MotionSystem.GetPoseFromJoints("ROB_1", toolFrame, joints);
        Console.WriteLine($"tool at {pose.X} {pose.Y} {pose.Z} metres, configuration {pose.Configuration}");

        // Inverse kinematics: which joint values put the tool at that pose.
        // previousJoints decides between the solutions the pose admits.
        JointTarget solution = robot.Rws.MotionSystem.GetJointsFromPose("ROB_1", pose, new ExternalJoints(),
                                                                       toolFrame, joints, pose.Configuration);
        Console.WriteLine($"axis 5 = {solution.RobotAxes.Axis5} rad");

        // The controller has a second calculation for the same question. It does not always
        // pick the same solution.
        JointTarget other = robot.Rws.MotionSystem.GetJointsFromCartesian("ROB_1", pose, new ExternalJoints(),
                                                                         toolFrame, joints, pose.Configuration);
        Console.WriteLine(other);

        // Every way of reaching the pose. A six axis robot usually has eight.
        JointSolution[] solutions = robot.Rws.MotionSystem.GetAllJointSolutions("ROB_1", pose, new ExternalJoints(),
                                                                               toolFrame, pose.Configuration);

        foreach (JointSolution s in solutions)
        {
            Console.WriteLine($"{s.Configuration} : {s.RobotAxes}");
        }

        // Set robotHoldsWorkObject to true when the tool is fixed in the cell and the robot
        // carries the work object. Set logErrors to true to have the controller write an
        // event log message when the calculation fails.
        RobTarget held = robot.Rws.MotionSystem.GetPoseFromJoints("ROB_1", toolFrame, joints,
                                                                 robotHoldsWorkObject: true, logErrors: true);
        Console.WriteLine(held);

        robot.Disconnect();
    }
}
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

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `JointSolution[] GetAllJointSolutions(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, RobotConfiguration configuration, bool robotHoldsWorkObject = false)`: Asks the controller for every joint combination that puts the tool at the given pose (synchronous) A six axis robot usually reaches the same pose in eight different ways, each one in a different axis configuration.
  - async: `Task<JointSolution[]> GetAllJointSolutionsAsync(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, RobotConfiguration configuration, bool robotHoldsWorkObject = false, CancellationToken cancellationToken = default)`
- `JointTarget GetJointsFromCartesian(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, JointTarget previousJoints, RobotConfiguration configuration, bool robotHoldsWorkObject = false, bool logErrors = false)`: Asks the controller which joint values put the tool at the given pose, staying close to the joint values the robot is already in (synchronous)
  - async: `Task<JointTarget> GetJointsFromCartesianAsync(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, JointTarget previousJoints, RobotConfiguration configuration, bool robotHoldsWorkObject = false, bool logErrors = false, CancellationToken cancellationToken = default)`
- `JointTarget GetJointsFromPose(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, JointTarget previousJoints, RobotConfiguration configuration, bool robotHoldsWorkObject = false, bool logErrors = false)`: Asks the controller which joint values put the tool at the given pose (synchronous)
  - async: `Task<JointTarget> GetJointsFromPoseAsync(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, JointTarget previousJoints, RobotConfiguration configuration, bool robotHoldsWorkObject = false, bool logErrors = false, CancellationToken cancellationToken = default)`
- `RobTarget GetPoseFromJoints(string mechanicalUnit, Pose toolFrame, JointTarget joints, bool robotHoldsWorkObject = false, bool logErrors = false)`: Asks the controller where the tool would be if the robot stood at the given joint values, without moving it there (synchronous)
  - async: `Task<RobTarget> GetPoseFromJointsAsync(string mechanicalUnit, Pose toolFrame, JointTarget joints, bool robotHoldsWorkObject = false, bool logErrors = false, CancellationToken cancellationToken = default)`

**JointSolution** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#jointsolution))

- `JointSolution()`: Initializes a new solution with every axis at zero
- `RobotConfiguration Configuration { get; set; }`: Axis configuration this solution corresponds to. Never null.
- Inherited from [JointTarget](../api/UnderAutomation.ABB.Common.md#jointtarget): `RobotAxes`, `ExternalAxes`

## Collision supervision

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

The controller watches the torque of the axes and stops the robot when it meets an unexpected resistance. There is one setting for jogging and one for a programmed path, per mechanical unit.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class MotionCollisionDetection
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Collision detection while the unit is jogged
        MotionSupervision jogging = robot.Rws.MotionSystem.GetMotionSupervision("ROB_1");
        Console.WriteLine($"jogging supervision {jogging.Enabled}, sensitivity {jogging.Level} %");

        // Collision detection while the unit follows a programmed path
        PathSupervision path = robot.Rws.MotionSystem.GetPathSupervision("ROB_1");
        Console.WriteLine($"path supervision {path.Enabled}, sensitivity {path.Level} %");

        // Writing these four values needs the mastership of the motion domain.
        // The lower the percentage, the sooner the controller reports a collision.
        robot.Rws.Mastership.Request(MastershipDomain.Motion);

        try
        {
            robot.Rws.MotionSystem.SetMotionSupervisionMode("ROB_1", true);
            robot.Rws.MotionSystem.SetMotionSupervisionLevel("ROB_1", 80);

            robot.Rws.MotionSystem.SetPathSupervisionMode("ROB_1", true);
            robot.Rws.MotionSystem.SetPathSupervisionLevel("ROB_1", 80);
        }
        finally
        {
            robot.Rws.Mastership.Release();
        }

        // Collision prediction stops the robot before it hits something the controller
        // knows about. It is a separate setting, and it needs no mastership.
        bool predicting = robot.Rws.MotionSystem.GetCollisionPredictionMode();

        if (!predicting)
        {
            // Refused when the collision detection option is not installed.
            // The error message then names the missing option.
            robot.Rws.MotionSystem.SetCollisionPredictionMode(true);
        }

        robot.Disconnect();
    }
}
```

| Setting             | Applies while                      |
| ------------------- | ---------------------------------- |
| `MotionSupervision` | The unit is jogged                 |
| `PathSupervision`   | The unit follows a programmed path |

The level is a percentage. The lower the value, the sooner the controller reports a collision. The four write methods need the mastership of the `Motion` domain.

Collision prediction is a different feature: it stops the robot before it hits something the controller already knows about, where the supervision only reacts once the arm meets a resistance. `GetCollisionPredictionMode` and `SetCollisionPredictionMode` need no mastership.

All of this belongs to the Collision Detection option. On a controller built without it, switching the feature on is refused with the HTTP status code 403 and the SDK reports an error naming the missing option. Writing back the value the controller already holds is accepted.

`SetNonMotionExecutionMode` is nearby but different: it runs the RAPID program while skipping every motion instruction, which is how a program is tested without the robot leaving its position. It belongs to the editing domain, not to the motion one, so take every domain before calling it.

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `bool GetCollisionPredictionMode()`: Tells whether the controller predicts collisions before they happen (synchronous) Collision prediction stops the robot before it hits something it knows about, where the motion supervision only reacts once the arm meets an unexpected resistance.
  - async: `Task<bool> GetCollisionPredictionModeAsync(CancellationToken cancellationToken = default)`
- `MotionSupervision GetMotionSupervision(string mechanicalUnit)`: Gets the collision detection settings that apply while a mechanical unit is jogged (synchronous)
  - async: `Task<MotionSupervision> GetMotionSupervisionAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `bool GetNonMotionExecutionMode()`: Tells whether the controller runs RAPID programs without moving the robot (synchronous) In that mode the program executes normally but every motion instruction is skipped, which is how a program is tested without the robot leaving its position.
  - async: `Task<bool> GetNonMotionExecutionModeAsync(CancellationToken cancellationToken = default)`
- `PathSupervision GetPathSupervision(string mechanicalUnit)`: Gets the collision detection settings that apply while a mechanical unit follows a programmed path (synchronous)
  - async: `Task<PathSupervision> GetPathSupervisionAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `void SetCollisionPredictionMode(bool enabled)`: Switches collision prediction on or off (synchronous)
  - async: `Task SetCollisionPredictionModeAsync(bool enabled, CancellationToken cancellationToken = default)`
- `void SetMotionSupervisionLevel(string mechanicalUnit, int sensitivity)`: Sets how sensitive the jogging collision detection of a mechanical unit is (synchronous)
  - async: `Task SetMotionSupervisionLevelAsync(string mechanicalUnit, int sensitivity, CancellationToken cancellationToken = default)`
- `void SetMotionSupervisionMode(string mechanicalUnit, bool enabled)`: Switches the jogging collision detection of a mechanical unit on or off (synchronous)
  - async: `Task SetMotionSupervisionModeAsync(string mechanicalUnit, bool enabled, CancellationToken cancellationToken = default)`
- `void SetNonMotionExecutionMode(bool enabled)`: Chooses whether the controller runs RAPID programs without moving the robot (synchronous)
  - async: `Task SetNonMotionExecutionModeAsync(bool enabled, CancellationToken cancellationToken = default)`
- `void SetPathSupervisionLevel(string mechanicalUnit, int level)`: Sets how sensitive the path collision detection of a mechanical unit is (synchronous)
  - async: `Task SetPathSupervisionLevelAsync(string mechanicalUnit, int level, CancellationToken cancellationToken = default)`
- `void SetPathSupervisionMode(string mechanicalUnit, bool enabled)`: Switches the path collision detection of a mechanical unit on or off (synchronous)
  - async: `Task SetPathSupervisionModeAsync(string mechanicalUnit, bool enabled, CancellationToken cancellationToken = default)`

**MotionSupervision** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#motionsupervision))

- `MotionSupervision()`: Initializes a new instance of the Data.MotionSupervision class
- `bool? Enabled { get; set; }`: Whether the supervision is switched on, null when the controller did not report it
- `int? Level { get; set; }`: Sensitivity of the supervision, as a percentage: the lower the value, the sooner a collision is reported. Null when the controller did not report it.

**PathSupervision** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#pathsupervision))

- `PathSupervision()`: Initializes a new instance of the Data.PathSupervision class
- `bool? Enabled { get; set; }`: Whether the supervision is switched on, null when the controller did not report it
- `int? Level { get; set; }`: Sensitivity of the supervision, as a percentage: the lower the value, the sooner a collision is reported. Null when the controller did not report it.

## Lead through

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

Lead through releases the arm so an operator can push it around by hand. The motors have to be on and the robot has to support the feature. This is one of the two writes of the service that need no mastership.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class MotionLeadThrough
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Is the arm free to be pushed by hand right now
        LeadThroughStatus status = robot.Rws.MotionSystem.GetLeadThrough("ROB_1");
        Console.WriteLine(status);

        // Switching it on releases the arm: the motors have to be on, and the robot
        // has to support lead through. This call needs no mastership.
        robot.Rws.MotionSystem.SetLeadThrough("ROB_1", true);

        // Switching it off makes the arm hold its position again
        robot.Rws.MotionSystem.SetLeadThrough("ROB_1", false);

        robot.Disconnect();
    }
}
```

`GetLeadThrough` returns `Active` when the arm gives way when pushed, and `Inactive` when it holds its position.

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `LeadThroughStatus GetLeadThrough(string mechanicalUnit)`: Tells whether an operator can push the arm of a mechanical unit around by hand (synchronous)
  - async: `Task<LeadThroughStatus> GetLeadThroughAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `void SetLeadThrough(string mechanicalUnit, bool active)`: Lets an operator push the arm of a mechanical unit around by hand, or stops letting them (synchronous)
  - async: `Task SetLeadThroughAsync(string mechanicalUnit, bool active, CancellationToken cancellationToken = default)`

**LeadThroughStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#leadthroughstatus))

- Active: The arm gives way when pushed
- Inactive: The arm holds its position
- Unknown: The controller reported a state this library does not know

## Calibration

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

The calibration says where each axis really is. Reading it is safe and tells you why a unit reports something else than `Synchronized`.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class CalibrationRead
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // How each joint of the unit was calibrated
        CalibrationInfo calibration = robot.Rws.MotionSystem.GetCalibrationInfo("ROB_1");
        Console.WriteLine($"method {calibration.CalibrationMethodUsed}, {calibration.ExistingJointCount} joint(s)");

        // The controller always answers with more joint slots than the unit has.
        // The extra ones carry no name and are marked as not existing.
        foreach (CalibrationJointInfo joint in calibration.Joints)
        {
            if (!joint.Exists) continue;

            Console.WriteLine($"{joint.JointName} : factory {joint.FactoryCalibrationMethod}, now {joint.CurrentCalibrationMethod}");
        }

        // The name each joint carries, and the name of its calibration data
        foreach (MotorCalibrationName name in robot.Rws.MotionSystem.GetMotorCalibrationNames("ROB_1"))
        {
            Console.WriteLine($"joint {name.Number} : {name.JointName}, data {name.CalibrationName}");
        }

        // The calibration is stored twice: in the controller cabinet and in the robot itself.
        // The two copies are meant to agree.
        SmbData smb = robot.Rws.MotionSystem.GetSmbData("ROB_1");

        Console.WriteLine($"cabinet calibration {smb.CabinetCalibrationStatus}");
        Console.WriteLine($"robot calibration   {smb.RobotCalibrationStatus}");

        if (smb.CabinetCalibrationStatus == SmbDataStatus.ValidNotEqual)
        {
            Console.WriteLine("the two copies do not hold the same data");
        }

        robot.Disconnect();
    }
}
```

`GetCalibrationInfo` always answers with a fixed number of joint slots, larger than the number of joints the unit really has. The extra ones carry no name and have `Exists` set to false. `ExistingJointCount` counts the real ones.

The calibration data is stored twice, once in the controller cabinet and once in the robot itself. `GetSmbData` returns both copies with a status per block of data. `ValidNotEqual` means the two copies are present but do not agree.

The write operations replace the calibration of an axis. RWS offers no way to put the previous one back, so a wrong calibration leaves the robot moving to the wrong place until somebody recalibrates it from the FlexPendant. They need the mastership of the `Motion` domain, and the measurement board operations also need the controller in manual mode with this client as its local client.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class CalibrationAxis
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // These four operations replace the calibration of an axis. RWS has no way to
        // put the previous one back, so read the state first and be sure of the position
        // the axis is standing in.
        MechanicalUnitInfo unit = robot.Rws.MotionSystem.GetMechanicalUnit("ROB_1");

        if (unit.Status != MechanicalUnitStatus.Synchronized)
        {
            Console.WriteLine($"ROB_1 is {unit.Status}");
        }

        robot.Rws.Mastership.Request(MastershipDomain.Motion);

        try
        {
            // Teaches the controller how the rotor of the motor is oriented.
            // Needed once after a motor has been replaced.
            robot.Rws.MotionSystem.Commutate("ROB_1", 1);

            // Move the axis to its synchronization mark first: the controller stores
            // the position the axis is in right now.
            robot.Rws.MotionSystem.SynchronizeAxisRevolutionCounter("ROB_1", 1);
            robot.Rws.MotionSystem.UpdateRevolutionCounter("ROB_1", 1);

            // Takes the current position of the axis as its new calibration position
            robot.Rws.MotionSystem.FineCalibrate("ROB_1", 1);
        }
        finally
        {
            robot.Rws.Mastership.Release();
        }

        // Copy one of the two calibration data stores over the other. The overwritten
        // one is gone, so read both first and keep the good one.
        robot.Rws.MotionSystem.SetSmbData("ROB_1", SmbDataTransfer.RobotToController);

        // Erase one of them. The controller cannot recover it.
        robot.Rws.MotionSystem.ClearSmbData("ROB_1", SmbDataMemory.Controller);

        robot.Disconnect();
    }
}
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

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `void ClearSmbData(string mechanicalUnit, SmbDataMemory memory)`: Erases one of the two serial measurement board data stores (synchronous)
  - async: `Task ClearSmbDataAsync(string mechanicalUnit, SmbDataMemory memory, CancellationToken cancellationToken = default)`
- `void Commutate(string mechanicalUnit, int axis)`: Commutates the motor of one axis, which teaches the controller how the rotor of that motor is oriented (synchronous) Needed once after a motor has been replaced, before the axis can be calibrated.
  - async: `Task CommutateAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `void FineCalibrate(string mechanicalUnit, int axis)`: Fine calibrates one axis of a mechanical unit (synchronous)
  - async: `Task FineCalibrateAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `CalibrationInfo GetCalibrationInfo(string mechanicalUnit)`: Gets how each joint of a mechanical unit was calibrated (synchronous)
  - async: `Task<CalibrationInfo> GetCalibrationInfoAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `MotorCalibrationName[] GetMotorCalibrationNames(string mechanicalUnit)`: Gets the name each joint of a mechanical unit carries, and the name of its calibration data (synchronous)
  - async: `Task<MotorCalibrationName[]> GetMotorCalibrationNamesAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `SmbData GetSmbData(string mechanicalUnit)`: Gets the serial measurement board data of a mechanical unit, as held by the controller cabinet and by the robot itself (synchronous) The two copies are meant to agree. When they do not, one of them is written over the other with Data.SmbDataTransfer).
  - async: `Task<SmbData> GetSmbDataAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `void SetSmbData(string mechanicalUnit, SmbDataTransfer direction)`: Copies one of the two serial measurement board data stores over the other (synchronous)
  - async: `Task SetSmbDataAsync(string mechanicalUnit, SmbDataTransfer direction, CancellationToken cancellationToken = default)`
- `void SynchronizeAxisRevolutionCounter(string mechanicalUnit, int axis)`: Synchronizes the revolution counter of one axis, telling the controller that the axis stands at its synchronization mark (synchronous)
  - async: `Task SynchronizeAxisRevolutionCounterAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `void UpdateRevolutionCounter(string mechanicalUnit, int axis)`: Updates the revolution counter of one axis of a mechanical unit (synchronous)
  - async: `Task UpdateRevolutionCounterAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`

**CalibrationInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#calibrationinfo))

- `CalibrationInfo()`: Initializes a new instance of the Data.CalibrationInfo class
- `int? ActiveJointCount { get; set; }`: Number of joints of the unit that are in use, null when the controller did not report it
- `string CalibrationMethodUsed { get; set; }`: Name of the calibration method the unit was last calibrated with, for example "AxisCalibration"
- `int? CalibrationWindowType { get; set; }`: Kind of calibration window the controller offers for this unit, null when the controller did not report it
- `int ExistingJointCount { get; }`: Number of joints that exist on the unit, counted from CalibrationInfo.Joints
- `int? JointCount { get; set; }`: Number of entries in CalibrationInfo.Joints, which is fixed and larger than CalibrationInfo.ActiveJointCount. Null when the controller did not report it.
- `CalibrationJointInfo[] Joints { get; set; }`: One entry per joint slot of the unit, the unused ones marked as such. Never null.

**CalibrationJointInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#calibrationjointinfo))

- `CalibrationJointInfo()`: Initializes a new instance of the Data.CalibrationJointInfo class
- `string CurrentCalibrationMethod { get; set; }`: Method the joint is currently calibrated with
- `bool Exists { get; set; }`: Whether the joint exists on this mechanical unit. The controller always answers with a fixed number of entries and marks the unused ones, which carry no name at all.
- `string FactoryCalibrationMethod { get; set; }`: Method the joint was calibrated with in the factory
- `string JointName { get; set; }`: Name of the joint, for example "rob1_1", empty for an entry that does not exist

**MotorCalibrationName** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#motorcalibrationname))

- `MotorCalibrationName()`: Initializes a new instance of the Data.MotorCalibrationName class
- `string CalibrationName { get; set; }`: Name of the calibration data of the joint, usually the same as MotorCalibrationName.JointName
- `string JointName { get; set; }`: Name of the joint, for example "rob1_1"
- `int Number { get; set; }`: Number of the joint inside its mechanical unit, starting at 1

**SmbData** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#smbdata))

- `SmbData()`: Initializes a new instance of the Data.SmbData class
- `SmbDataStatus CabinetAbsoluteAccuracyStatus { get; set; }`: State of the absolute accuracy data stored in the cabinet
- `SmbDataStatus CabinetAxisCalibrationStatus { get; set; }`: State of the axis calibration data stored in the cabinet
- `SmbDataStatus CabinetCalibrationStatus { get; set; }`: State of the calibration data stored in the cabinet
- `string CabinetSerialNumberHighPart { get; set; }`: High part of the serial number stored in the cabinet
- `string CabinetSerialNumberLowPart { get; set; }`: Low part of the serial number stored in the cabinet
- `bool? CabinetSerialNumberValid { get; set; }`: Whether the serial number stored in the cabinet is usable, null when the controller did not report it
- `SmbDataStatus CabinetServiceInformationStatus { get; set; }`: State of the service information data stored in the cabinet
- `int? DriveModule { get; set; }`: Number of the drive module the data belongs to, null when the controller did not report it
- `int? MeasurementBoard { get; set; }`: Number of the measurement board the data belongs to, null when the controller did not report it
- `int? MeasurementLink { get; set; }`: Number of the measurement link the data belongs to, null when the controller did not report it
- `SmbDataStatus RobotAbsoluteAccuracyStatus { get; set; }`: State of the absolute accuracy data stored in the robot
- `SmbDataStatus RobotAxisCalibrationStatus { get; set; }`: State of the axis calibration data stored in the robot
- `SmbDataStatus RobotCalibrationStatus { get; set; }`: State of the calibration data stored in the robot
- `string RobotSerialNumberHighPart { get; set; }`: High part of the serial number stored in the robot
- `string RobotSerialNumberLowPart { get; set; }`: Low part of the serial number stored in the robot
- `bool? RobotSerialNumberValid { get; set; }`: Whether the serial number stored in the robot is usable, null when the controller did not report it
- `SmbDataStatus RobotServiceInformationStatus { get; set; }`: State of the service information data stored in the robot

**SmbDataStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#smbdatastatus))

- NotUsed: The robot system does not use this block of data
- NotValid: The data is missing or unusable
- Unknown: The controller reported a state this library does not know
- Valid: The data is present and the two copies agree
- ValidNotEqual: The data is present on both sides, but the two copies differ

**SmbDataTransfer** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#smbdatatransfer))

- ControllerToRobot: The copy held by the controller cabinet is written into the robot
- RobotToController: The copy held by the robot is written into the controller cabinet

**SmbDataMemory** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#smbdatamemory))

- Controller: The copy held by the controller cabinet
- Robot: The copy held by the robot itself

## State of the motion system

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

`GetInfo` gives the overview: which unit the jogging commands apply to, whether absolute accuracy is on, and the change count.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class MotionState
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Overview of the motion system: which unit the jogging commands apply to,
        // and the counter the controller increments on every change
        MotionSystemInfo info = robot.Rws.MotionSystem.GetInfo();
        Console.WriteLine($"jogging applies to {info.MechanicalUnitName}");
        Console.WriteLine($"change count {info.ChangeCount}, absolute accuracy {info.AbsoluteAccuracyActive}");

        // Ask whether anything moved since that reading, instead of reading everything again
        if (info.ChangeCount.HasValue && robot.Rws.MotionSystem.HasChanged(info.ChangeCount.Value))
        {
            Console.WriteLine("the motion system changed");
        }

        // The last error the motion system ran into. Most of them come from a jogging
        // request the controller accepted and could not honour.
        MotionSystemErrorState error = robot.Rws.MotionSystem.GetErrorState();

        if (error.State != MotionErrorState.Ok)
        {
            Console.WriteLine($"{error.State} ({error.RawState}), {error.Count} error(s)");
        }

        // Run the RAPID program without moving the robot. The instructions execute,
        // the motion ones are skipped.
        bool skipped = robot.Rws.MotionSystem.GetNonMotionExecutionMode();

        robot.Rws.Mastership.Request();

        try
        {
            robot.Rws.MotionSystem.SetNonMotionExecutionMode(true);
        }
        finally
        {
            robot.Rws.Mastership.Release();
        }

        robot.Disconnect();
    }
}
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

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `MotionSystemErrorState GetErrorState()`: Gets the last error the motion system ran into, and how many errors it has counted (synchronous) Most of these errors are raised by a jogging request the controller could not honour, and stay reported until a new one replaces them.
  - async: `Task<MotionSystemErrorState> GetErrorStateAsync(CancellationToken cancellationToken = default)`
- `MotionSystemInfo GetInfo()`: Gets an overview of the motion system: the mechanical unit jogging applies to, the change counter and the payload and accuracy settings (synchronous)
  - async: `Task<MotionSystemInfo> GetInfoAsync(CancellationToken cancellationToken = default)`
- `bool HasChanged(int changeCount)`: Tells whether the motion system changed since it reported the given change count (synchronous) Reading MotionSystemInfo.ChangeCount once and asking this afterwards is cheaper than fetching the whole state again to find out that nothing moved.
  - async: `Task<bool> HasChangedAsync(int changeCount, CancellationToken cancellationToken = default)`

**MotionSystemInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#motionsysteminfo))

- `MotionSystemInfo()`: Initializes a new instance of the Data.MotionSystemInfo class
- `bool? AbsoluteAccuracyActive { get; set; }`: Whether absolute accuracy is switched on, null when the controller did not report it
- `int? ChangeCount { get; set; }`: Counter the controller increments on every change of the motion system. Pass it to MotionSystemService.HasChanged() to find out whether anything moved since a previous reading, without fetching the whole state again.
- `string MechanicalUnitName { get; set; }`: Name of the mechanical unit the jogging commands currently apply to
- `bool? ModalPayloadMode { get; set; }`: Whether the payload of the robot is set by the running program rather than by the mechanical unit, null when the controller did not report it
- `int? PollRate { get; set; }`: Rate at which the controller refreshes the motion system state, null when it did not report it

**MotionSystemErrorState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#motionsystemerrorstate))

- `MotionSystemErrorState()`: Initializes a new instance of the Data.MotionSystemErrorState class
- `int? Count { get; set; }`: Number of errors counted since the controller started, incremented on every new error, null when the controller did not report it
- `string RawState { get; set; }`: Error state exactly as the controller reported it, useful when MotionSystemErrorState.State is MotionErrorState.Unknown
- `MotionErrorState State { get; set; }`: Last error the motion system ran into

**MotionErrorState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#motionerrorstate))

- ErroneousToolMass: A load definition carries a negative mass
- InvalidJogMotionType: The requested jogging mode is not valid
- MechanicalUnitNotActive: A mechanical unit was jogged whose activation failed
- Ok: No error
- RobotHoldMismatch: The tool and the work object disagree on which one the robot holds
- UncalibratedJogMotionType: An uncalibrated robot was jogged in a mode that needs its calibration
- Unknown: The controller reported an error this library does not know
- UnnormalizedQuaternion: A quaternion that is not normalized reached the jogging task, from a tool, a load or a work object
- WorkObjectMechanicalUnitNotFound: A mechanical unit used in coordinated jogging was not found

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).
