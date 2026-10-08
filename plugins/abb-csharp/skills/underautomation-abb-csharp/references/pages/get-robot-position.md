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

These calculations are pure computation, they do not move the robot and they work on positions the robot is not at.

## Millimetres, metres, degrees and radians

The readings answer in millimetres and degrees. The four kinematics calculations work in **metres and radians**, in both directions. Nothing in the answer says which one it is, so convert explicitly when you feed one into the other.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Common;

public class HowToPositionUnits
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The readings answer in millimetres and degrees
        RobTarget reading = robot.Rws.MotionSystem.GetRobTarget("ROB_1");
        JointTarget joints = robot.Rws.MotionSystem.GetJointTarget("ROB_1");

        Console.WriteLine($"{reading.X} mm, axis 5 = {joints.RobotAxes.Axis5} deg");

        // The four kinematics calculations work in metres and radians, in both directions.
        // Convert the joints before sending them.
        JointTarget inRadians = new JointTarget(ToRadians(joints.RobotAxes), joints.ExternalAxes);
        Pose toolFrame = new Pose(0, 0, 0, new Quaternion(1, 0, 0, 0));

        RobTarget computed = robot.Rws.MotionSystem.GetPoseFromJoints("ROB_1", toolFrame, inRadians);

        // And convert the answer back to millimetres to compare it with the reading
        Console.WriteLine($"{computed.X * 1000} mm computed, {reading.X} mm read");

        robot.Disconnect();
    }

    static RobotJoints ToRadians(RobotJoints degrees)
    {
        double f = Math.PI / 180.0;

        return new RobotJoints(degrees.Axis1 * f, degrees.Axis2 * f, degrees.Axis3 * f,
                               degrees.Axis4 * f, degrees.Axis5 * f, degrees.Axis6 * f);
    }

    static RobotJoints ToDegrees(RobotJoints radians)
    {
        double f = 180.0 / Math.PI;

        return new RobotJoints(radians.Axis1 * f, radians.Axis2 * f, radians.Axis3 * f,
                               radians.Axis4 * f, radians.Axis5 * f, radians.Axis6 * f);
    }
}
```

## Going further

- [Motion system, position & kinematics](rws-motion.md), the complete reference
- [Read & write RAPID variables](read-write-rapid-variables.md), to read a taught `robtarget` from the program
- [RAPID tasks & program execution](rws-rapid-tasks.md)

**Methods of MotionSystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#motionsystemservice-robotrwsmotionsystem))

- `JointTarget GetJointTarget(string mechanicalUnit, bool alwaysRead = false)`: Gets the joint values a mechanical unit currently stands at (synchronous) The robot axes are expressed in degrees.
  - async: `Task<JointTarget> GetJointTargetAsync(string mechanicalUnit, bool alwaysRead = false, CancellationToken cancellationToken = default)`
- `RobTarget GetRobTarget(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null)`: Gets where the tool of a mechanical unit currently is (synchronous) The position is expressed in millimetres.
  - async: `Task<RobTarget> GetRobTargetAsync(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null, CancellationToken cancellationToken = default)`
- `void SetPositionTarget(RobTarget target)`: Sends the robot to a cartesian target (synchronous) The position is expressed in millimetres, in the coordinate system currently active for the mechanical unit selected for jogging.
  - async: `Task SetPositionTargetAsync(RobTarget target, CancellationToken cancellationToken = default)`

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

**RobotConfiguration** ([reference](../api/UnderAutomation.ABB.Common.md#robotconfiguration))

- `RobotConfiguration()`: Initializes a new configuration with every quarter revolution set to zero
- `RobotConfiguration(int quarter1, int quarter4, int quarter6, int quarterX)`: Initializes a new configuration
- `int Quarter1 { get; set; }`: Quarter revolution axis 1 sits in
- `int Quarter4 { get; set; }`: Quarter revolution axis 4 sits in
- `int Quarter6 { get; set; }`: Quarter revolution axis 6 sits in
- `int QuarterX { get; set; }`: Index of the arm configuration, which tells the remaining joint combinations apart

**CoordinateSystem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#coordinatesystem))

- Base: The base frame of the mechanical unit
- Tool: The frame of the active tool
- Unknown: The controller reported a frame this library does not know
- WorkObject: The frame of the active work object
- World: The world frame, shared by every mechanical unit of the system
