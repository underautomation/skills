# Inverse kinematics solutions

Why a position has up to 8 or 16 joint solutions on a Yaskawa robot, what they look like, which positions are reachable, and how to choose a solution.

Web page: https://underautomation.com/yaskawa/documentation/kinematics-inverse

This page explains the inverse kinematics of the Yaskawa SDK in detail: why one position has several joint solutions, how the solutions of a GP7 and of an HC10 look, and how to choose the solution to send to the robot. The computation is offline and works for the 169 models of the catalog.

## Several solutions for one position

A 6-axis arm reaches most positions with several postures. `InverseKinematics` returns all of them:

- **Front or back**: the S axis turns the arm toward the target, or the opposite way and the arm reaches over its base.
- **Elbow up or elbow down**: the U axis is above or below the line from the L axis to the wrist.
- **Wrist flip**: the R axis turns by 180 degrees, the B axis changes its sign. The flange has the same position.

These 3 choices give up to 8 solutions for a robot with a spherical wrist (GP7, MH, ES...). The example of the snippet below gives 8 solutions for a GP7:

![The 8 solutions of the GP7 for the target X=400 Y=100 Z=300 Rx=180 Ry=0 Rz=0, seen from the side of the arm. Each view holds 2 solutions that differ only by the wrist flip.](https://underautomation.com/yaskawa/documentation/diagrams/kinematics-ik-solutions.svg)

```csharp
using UnderAutomation.Yaskawa.Common;
using UnderAutomation.Yaskawa.Kinematics;

public class KinematicsInverse
{
    static void Main()
    {
        DhParameters dh = DhParameters.FromArmKinematicModel(ArmKinematicModels.GP7);

        // Flange position in the robot frame: mm and degrees
        var target = new CartesianPosition(400, 100, 300, 180, 0, 0);

        // Every joint solution, angles in (-180, 180]. Empty if the position cannot be reached.
        JointsAngles[] solutions = KinematicsUtils.InverseKinematics(target, dh);

        foreach (JointsAngles solution in solutions)
            Console.WriteLine(solution); // S=..., L=..., U=..., R=..., B=..., T=...
    }
}
```

A cobot with a wrist offset along the B axis (HC10, HC10DT, HC20SDT) has more solutions, up to 16, because the offset of the wrist adds other ways to place the arm.

## Reachable positions

The number of solutions changes with the position. The map below counts the solutions in the vertical plane Y = 0, with the flange pointing down:

![Number of solutions found by InverseKinematics in the plane Y = 0, flange pointing down. GP7 on the left, HC10 on the right. The offset wrist of the HC10 cannot put the flange on the S axis with this orientation.](https://underautomation.com/yaskawa/documentation/diagrams/kinematics-reach-map.svg)

- Outside the reach of the arm, the array is empty.
- At the border of the reach, the elbow is straight and some solutions merge.
- For the HC10, the flange cannot be on the S axis with the flange pointing down: the wrist offset of 162 mm keeps it away.

The joint limits are not applied: a part of these solutions is outside the limits of the real robot.

## Choose a solution

### Closest to the current position

To move the robot with the smallest joint motion, keep the solution closest to the current joint angles. The snippet below keeps the solution with the smallest largest joint move:

```csharp
using UnderAutomation.Yaskawa.Common;
using UnderAutomation.Yaskawa.Kinematics;

public class KinematicsClosestSolution
{
    static void Main()
    {
        DhParameters dh = DhParameters.FromArmKinematicModel(ArmKinematicModels.GP7);
        var target = new CartesianPosition(400, 100, 300, 180, 0, 0);

        // The current joint angles of the robot, in degrees
        var current = new JointsAngles(10, 20, -10, 0, -60, 0);

        // Keep the solution with the smallest joint move
        JointsAngles best = null;
        double bestDistance = double.MaxValue;
        foreach (JointsAngles solution in KinematicsUtils.InverseKinematics(target, dh))
        {
            double distance = 0;
            for (int i = 0; i < 6; i++)
                distance = Math.Max(distance, Math.Abs(solution.Values[i] - current.Values[i]));

            if (distance < bestDistance)
            {
                best = solution;
                bestDistance = distance;
            }
        }

        Console.WriteLine(best == null ? "Not reachable" : $"{best}, largest joint move {bestDistance:F1} deg");
    }
}
```

### Other criteria

- **Joint limits**: remove the solutions outside the limits of your robot (from its data sheet or from the soft limits of the controller).
- **Posture**: keep the front and elbow up solutions to stay in the same posture along a path.
- **Wrist singularity**: a B angle close to 0 makes the R and T axes aligned. Prefer the solutions far from it for linear moves.

## Errors

- `InverseKinematics` returns an empty array when the position cannot be reached. It does not throw.
- It throws a `NotSupportedException` for a structure that is not supported. See [Supported robots](kinematics.md#supported_robots).
- It throws an `ArgumentNullException` when the position or the parameters are null.

## Reference

**KinematicsUtils** ([reference](../api/UnderAutomation.Yaskawa.Kinematics.md#kinematicsutils))

- `static CartesianPosition ForwardKinematics(IJointAngles joints, IDhParameters parameters)`: Computes the flange position for the given joint angles.
- `static JointsAngles[] InverseKinematics(ICartesianPosition position, IDhParameters parameters)`: Computes all the joint solutions that put the flange at the given position. Joint limits are not checked. Angles are returned in the range (-180, 180].

**JointsAngles** ([reference](../api/UnderAutomation.Yaskawa.Common.md#jointsangles))

- `JointsAngles()`: Initializes a new instance of Common.JointsAngles with all angles at 0.
- `JointsAngles(double s, double l, double u, double r, double b, double t)`: Initializes a new instance of Common.JointsAngles with the specified angles (degrees).
- `JointsAngles(double[] values)`: Initializes a new instance of Common.JointsAngles from an array of at least 6 angles (degrees). The array is copied.
- `double B { get; set; }`: B axis angle (degrees).
- `double L { get; set; }`: L axis angle (degrees).
- `double R { get; set; }`: R axis angle (degrees).
- `double S { get; set; }`: S axis angle (degrees).
- `double T { get; set; }`: T axis angle (degrees).
- `double U { get; set; }`: U axis angle (degrees).
- `double[] Values { get; }`: Angles of axes S, L, U, R, B, T in degrees.

## What to read next

- [Kinematics models](kinematics-models.md): the DH parameters of your robot.
- [Move the robot from a PC](how-to-move-robot.md): send the target to the robot.
