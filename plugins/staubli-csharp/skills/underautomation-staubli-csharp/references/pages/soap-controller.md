# Controller and robots

List the robots of a Staubli controller, read the controller parameters, the Denavit-Hartenberg parameters and the joint ranges of each arm.

Web page: https://underautomation.com/staubli/documentation/soap-controller

This page shows how to read the description of a Staubli CS8 or CS9 controller and of its robots: the arms, the controller parameters, the Denavit-Hartenberg parameters and the joint ranges. These calls only read: they never change the state of the controller.

## Robots of the controller

`GetRobots()` returns one `Robot` per arm driven by the controller. The index of an arm in this array is the `robot` number that the other methods take.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class ControllerRobots
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // The robots driven by the controller. The index in this array
        // is the robot number that the other methods take.
        Robot[] robots = controller.Soap.GetRobots();

        for (int i = 0; i < robots.Length; i++)
        {
            Robot robot = robots[i];
            Console.WriteLine($"Robot {i}: {robot.Arm}"); // for example TX2-60
            Console.WriteLine($"  Kinematic: {robot.Kinematic}"); // Anthropomorph6, Scara...
            Console.WriteLine($"  Mount type: {robot.MountType}"); // Floor, Ceiling, Wall
            Console.WriteLine($"  Tuning: {robot.Tuning}");
        }

        controller.Disconnect();
    }
}
```

`Kinematic` gives the type of arm: `Anthropomorph6` for a 6 axis arm like the TX2 series, `Scara` for a SCARA like the TS2 series, and the other values of the `Kinematic` enumeration.

## Controller parameters

`GetControllerParameters()` returns the parameters of the controller, as key, name and value.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class ControllerParameters
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        Parameter[] parameters = controller.Soap.GetControllerParameters();

        foreach (Parameter parameter in parameters)
            Console.WriteLine($"{parameter.Key} | {parameter.Name} = {parameter.Value}");

        controller.Disconnect();
    }
}
```

The list and the values depend on the controller and on its version. Read the list once on your controller to find the keys you need.

## Denavit-Hartenberg parameters

`GetDhParameters(robot)` returns one `DhParameters` per joint of the arm, as the controller defines its geometry.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class ControllerDhParameters
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // One entry per joint of the first robot
        DhParameters[] dh = controller.Soap.GetDhParameters(robot: 0);

        for (int i = 0; i < dh.Length; i++)
            Console.WriteLine($"J{i + 1}: theta={dh[i].Theta} d={dh[i].D} a={dh[i].A} alpha={dh[i].Alpha} beta={dh[i].Beta}");

        controller.Disconnect();
    }
}
```

## Joint ranges

`GetJointRange(robot)` returns the software limits of each joint, in radians. The inverse kinematics uses them to reject a solution out of range: see [Kinematics](soap-kinematics.md).

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class ControllerJointRange
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Software limits of each joint of the first robot, in radians
        JointRange range = controller.Soap.GetJointRange(robot: 0);

        for (int i = 0; i < range.Min.Length; i++)
            Console.WriteLine($"J{i + 1}: {range.Min[i]} to {range.Max[i]}");

        controller.Disconnect();
    }
}
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/UnderAutomation.Staubli.Soap.Internal.md#soapclientbase-controllersoap))

- `Parameter[] GetControllerParameters()`: Get the current Cartesian position of a robot end effector
- `DhParameters[] GetDhParameters(int robot = 0)`: Get Robot DH parameters
- `JointRange GetJointRange(int robot = 0)`: Get the range Min-Max of each joint of a robot
- `Robot[] GetRobots()`: Get all the robots handled by this controller

**Robot** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#robot))

- `Robot()`: Initializes a new instance of the Data.Robot class.
- `string Arm { get; set; }`: Arm model identifier.
- `DiameterAxis3 DiameterAxis3 { get; set; }`: Diameter of the third axis.
- `Kinematic Kinematic { get; set; }`: Kinematic type of the robot.
- `LengthAxis3 LengthAxis3 { get; set; }`: Length of the third axis.
- `MountType MountType { get; set; }`: Mounting type of the robot (floor, ceiling, wall).
- `string Tuning { get; set; }`: Tuning identifier.

**Kinematic** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#kinematic))

- Anthrioparallel6: 6-axis anthropomorphic parallel robot.
- Anthropomorph5: 5-axis anthropomorphic robot.
- Anthropomorph6: 6-axis anthropomorphic robot.
- Eisenmann: Eisenmann kinematic type.
- Invalid: Invalid or unknown kinematic type.
- Scara: SCARA robot.

**MountType** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#mounttype))

- Ceiling: Robot is ceiling-mounted.
- Floor: Robot is floor-mounted.
- Invalid: Invalid or unknown mount type.
- Wall: Robot is wall-mounted.

**Parameter** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#parameter))

- `Parameter()`: Initializes a new instance of the Data.Parameter class.
- `string Key { get; set; }`: Parameter key identifier.
- `string Name { get; set; }`: Display name of the parameter.
- `string Value { get; set; }`: Value of the parameter.

**DhParameters** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#dhparameters))

- `DhParameters()`: Initializes a new instance of the Data.DhParameters class.
- `double A { get; set; }`: Link length a (m).
- `double Alpha { get; set; }`: Link twist alpha (radians).
- `double Beta { get; set; }`: Joint twist beta (radians).
- `double D { get; set; }`: Link offset d (m).
- `double Theta { get; set; }`: Joint angle theta (radians).

**JointRange** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#jointrange))

- `JointRange()`: Initializes a new instance of the Data.JointRange class.
- `double[] Max { get; set; }`: Maximum values for each joint (radians).
- `double[] Min { get; set; }`: Minimum values for each joint (radians).
