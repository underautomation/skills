# Motion planner overview

Create smooth robot trajectories offline, with velocity, acceleration and jerk limits, using FANUC motion instructions (J, L, C, FINE, CNT, CR).

Web page: https://underautomation.com/fanuc/documentation/motion

The Motion module creates smooth robot trajectories that respect velocity, acceleration and jerk limits. It works offline, without robot connection, and its trajectories can be sent with [Stream Motion](stream-motion.md), used in a simulation, or checked before use.

Motions are described as in a TP program: joint (J), linear (L) and circular (C) motions, with a speed and a FINE, CNT or CR termination. The module also creates splines through points, geometric shapes, and trajectories from your own positions.

The planner is in the `UnderAutomation.Robotics.Motion` namespace. This namespace is the same in all UnderAutomation robot SDKs, so the same code can plan trajectories for other robot brands. The `FanucMotion` class of `UnderAutomation.Fanuc.Motion` converts FANUC positions, FINE, CNT and CR terminations and I/O to the types of the planner.

## Quick start

```csharp
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Motion;
using UnderAutomation.Robotics.Geometry;
using UnderAutomation.Robotics.Motion;

public class MotionQuickStart
{
    static void Main()
    {
        // Limits of the robot (example values). Read them with robot.StreamMotion.ReadLimits().ReferenceLimits
        var jointLimits = new JointLimits(
            new double[] { 120, 120, 180, 180, 180, 180 },
            new double[] { 300, 300, 450, 675, 675, 675 },
            new double[] { 1125, 1125, 1687, 2530, 1265, 2530 });
        var cartesianLimits = new CartesianLimits(500, 2000, 10000, 90, 360, 1800);

        var planner = new MotionPlanner(jointLimits, cartesianLimits);

        // Joint motions, as J instructions of a TP program
        var home = new JointValues(0, 0, 0, 0, -90, 0);
        var pick = new JointValues(30, 20, -10, 0, -70, 30);
        Trajectory trajectory = planner.CreateJointPath(home)
            .MoveJoint(pick, 50, FanucMotion.Cnt(100))   // 50% speed, CNT100
            .MoveJoint(home, 50, FanucMotion.Fine())
            .Build();

        Console.WriteLine($"Duration: {trajectory.Duration:0.000} s");

        // Position at any time, or one position per communication cycle
        JointValues middle = trajectory.GetJoints(trajectory.Duration / 2);
        JointValues[] samples = trajectory.SampleJoints(0.008);

        // FANUC joint position, when needed
        JointsPosition fanucMiddle = FanucMotion.ToJointsPosition(middle);

        // Velocity, acceleration and jerk of each axis, computed as the robot does
        TrajectoryReport report = trajectory.Check(jointLimits, 0.008, false);
        Console.WriteLine(report.IsValid);
    }
}
```

![Joint positions of this trajectory. With CNT100, the robot passes near pick without stopping. With FINE, it stops at home.](https://underautomation.com/fanuc/documentation/diagrams/motion-quick-start.svg)

## Try it in the demo application

The [demo application](demo-app.md) (Windows) has a Stream Motion page with two buttons that build trajectories with the motion planner and send them to the robot with [Stream Motion](stream-motion.md).

- **Joint demo** uses a `JointPathBuilder`: J1 moves to +amplitude, then to -amplitude with a `Cnt` termination between the two moves, then back to the start with `Fine`.
- **Cartesian demo** uses a `CartesianPathBuilder`: a horizontal circle of the given radius, starting and ending at the current position.

Change the amplitude, the radius or the speed and send the demo again: the duration of the resulting trajectory is shown in the log, and the joint and Cartesian positions update in real time while the robot moves.

![Stream Motion page of the Showcase demo application, with the joint and Cartesian demo motions](https://underautomation.com/fanuc/documentation/demo-stream-motion-showcase-forms.gif)

The C# source of this page is in the `StreamMotionControl.cs` file of the [Fanuc.NET repository](https://github.com/underautomation/Fanuc.NET/blob/main/UnderAutomation.Fanuc.Showcase.Forms/Components/StreamMotionControl.cs).

## Main concepts

| Class | Role |
| --- | --- |
| `JointLimits` | Velocity, acceleration and jerk of each axis (9 axes). Read them from the robot with `StreamMotion.ReadLimits()` |
| `CartesianLimits` | Linear and angular velocity, acceleration and jerk, for Cartesian motions. You choose them |
| `MotionPlanner` | Creates joint and Cartesian paths with the limits, and optional tool and user frames |
| `JointPathBuilder`, `CartesianPathBuilder` | Chain motions, waits and I/O, then `Build()` the trajectory |
| `Trajectory` | Result: position at any time, samples at a fixed period, I/O events, limit checks |
| `JointValues`, `CartesianPose` | Joint and Cartesian positions of the planner. A `CartesianPose` has X, Y, Z, an `Orientation` and optional external axes |
| `FanucMotion` | Conversions with `JointsPosition` and `XYZWPRPosition`, FINE, CNT and CR terminations, I/O signals, FANUC positions of a trajectory |

All motions use jerk limited profiles: the acceleration changes progressively, which gives smooth motions and avoids the jerk alarms of the robot. 100% speed means the velocity limits, and the acceleration percentage (ACC) scales the acceleration and the jerk.

![Velocity of J1 for the same joint motion. The speed percentage limits the velocity, ACC changes the slopes.](https://underautomation.com/fanuc/documentation/diagrams/motion-speed-acceleration.svg)

## What do you want to do?

| Need | Page |
| --- | --- |
| Move to positions with J, L, C motions, FINE, CNT, CR | [Joint & Cartesian motions](motion-moves.md) |
| Pass through a list of points, draw a circle, a rectangle or a helix | [Splines & shapes](motion-splines-shapes.md) |
| Use positions computed by your application, check or slow down a trajectory | [Trajectories from points](motion-trajectory-from-points.md) |
| Convert orientations and positions between frames | [Frames & orientations](motion-frames-orientations.md) |

## Units and conventions

- Joint positions in degrees (mm for linear axes), Cartesian positions in mm, angles in degrees.
- Velocities per second, accelerations per second squared, jerks per second cubed.
- The W, P, R angles of FANUC use the fixed XYZ convention: `CartesianPose.FromEuler(x, y, z, w, p, r, EulerConvention.FixedXYZ)` gives the same pose as `FanucMotion.ToCartesianPose(new XYZWPRPosition(x, y, z, w, p, r))`.
- `FanucMotion.SampleCartesian()` gives FANUC positions whose W, P, R angles stay continuous: an angle can go beyond 180 degrees instead of jumping to -180.

## API reference

**MotionPlanner** ([reference](../api/UnderAutomation.Robotics.Motion.md#motionplanner))

- `MotionPlanner(JointLimits jointLimits, CartesianLimits cartesianLimits)`: Creates a planner
- `CartesianLimits CartesianLimits { get; set; }`: Limits for Cartesian motions
- `CartesianPathBuilder CreateCartesianPath(CartesianPose start)`: Starts a Cartesian path
- `JointPathBuilder CreateJointPath(JointValues start)`: Starts a joint path
- `JointLimits JointLimits { get; set; }`: Limits for joint motions. 100% speed uses the velocity limits of this object. The limits of axes 7 to 9 are also used for the external axes of Cartesian motions.
- `CartesianPose ToolFrame { get; set; }`: Tool frame, relative to the flange. When it is set, the targets of Cartesian motions are poses of this tool, and the trajectory gives the flange poses. Null when the targets are flange poses.
- `CartesianPose UserFrame { get; set; }`: User frame, relative to the world frame. When it is set, the targets of Cartesian motions are expressed in this frame, and the trajectory gives poses in the world frame. Null when the targets are in the world frame.

**JointLimits** ([reference](../api/UnderAutomation.Robotics.Motion.md#jointlimits-robotstreammotionjointlimits))

- `JointLimits()`: Creates limits with all values set to 0
- `JointLimits(double[] velocity, double[] acceleration, double[] jerk)`: Creates limits from arrays of values. Arrays can contain less than 9 values, missing values are set to 0.
- `double[] Acceleration { get; }`: Acceleration limit of each axis (9 values)
- `const int AxisCount = 9`: Number of axes handled by this class
- `double[] Jerk { get; }`: Jerk limit of each axis (9 values)
- `JointLimits Scale(double velocityFactor, double accelerationFactor, double jerkFactor)`: Returns a copy of these limits where each value is multiplied by the given factors
- `double[] Velocity { get; }`: Velocity limit of each axis (9 values)

**CartesianLimits** ([reference](../api/UnderAutomation.Robotics.Motion.md#cartesianlimits-robotstreammotioncartesianlimits))

- `CartesianLimits()`: Creates limits with all values set to 0
- `CartesianLimits(double linearVelocity, double linearAcceleration, double linearJerk, double angularVelocity, double angularAcceleration, double angularJerk)`: Creates limits with the given values
- `double AngularAcceleration { get; set; }`: Angular acceleration limit in deg/s²
- `double AngularJerk { get; set; }`: Angular jerk limit in deg/s³
- `double AngularVelocity { get; set; }`: Angular velocity limit in deg/s
- `double LinearAcceleration { get; set; }`: Linear acceleration limit in mm/s²
- `double LinearJerk { get; set; }`: Linear jerk limit in mm/s³
- `double LinearVelocity { get; set; }`: Linear velocity limit in mm/s

**FanucMotion** ([reference](../api/UnderAutomation.Fanuc.Motion.md#fanucmotion))

- `static Termination Cnt(int value)`: CNT termination: the next motion starts during the deceleration of this one
- `static Termination Cr(double distance)`: CR termination (corner region): the corner is replaced by a smooth curve at constant speed. Only between Cartesian motions.
- `static Termination Fine()`: FINE termination: the robot stops at the target position
- `static Trajectory FromCartesianSamples(XYZWPRPosition[] samples, double cycleTime)`: Creates a Cartesian trajectory from FANUC positions taken at a fixed period. The W, P, R angles are kept without any change, and the extended axes are used when the positions are Common.ExtendedCartesianPosition.
- `static ExtendedCartesianPosition[] SampleCartesian(Trajectory trajectory, double cycleTime)`: Samples a Cartesian trajectory at a fixed period and returns FANUC positions. The W, P, R angles stay continuous from one position to the next.
- `static DigitalSignal Signal(IOType type, int index)`: Returns the digital signal of an I/O, to write it during a trajectory (for example DO[5])
- `static CartesianPose ToCartesianPose(XYZWPRPosition position)`: Converts a FANUC position to a pose. The extended axes E1, E2 and E3 are copied when the position is an Common.ExtendedCartesianPosition.
- `static ExtendedCartesianPosition ToExtendedCartesianPosition(CartesianPose pose, XYZWPRPosition reference)`: Converts a pose to a FANUC position with extended axes (0 when the pose has no external axes).
- `static JointValues ToJointValues(JointsPosition position)`: Converts a FANUC joint position (J1 to J9) to joint values
- `static JointsPosition ToJointsPosition(JointValues values)`: Converts joint values to a FANUC joint position. Missing axes are 0.
- `static EulerConvention WprConvention { get; }`: Convention of the W, P, R angles of FANUC positions: rotation W around the fixed X axis, then P around the fixed Y axis, then R around the fixed Z axis
