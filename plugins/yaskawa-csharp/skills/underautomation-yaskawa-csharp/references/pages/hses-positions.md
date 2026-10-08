# Positions

Read the Cartesian position in mm and degrees, the joint pulses, the position error and the torque of a Yaskawa robot, a station or a base axis.

Web page: https://underautomation.com/yaskawa/documentation/hses-positions

This page shows how to read the position of a Yaskawa Motoman robot with the SDK: the Cartesian position of the tool, the joint positions, the position error and the torque, for the robot, a station or base axes. All these methods only read: they work in any mode.

## Cartesian position

`GetRobotCartesianPosition()` reads the position of the tool center point of the first robot, in mm and degrees.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class PositionCartesian
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        RobotPositionCartesianData position = robot.HighSpeedEServer.GetRobotCartesianPosition();

        // Tool center point in mm, orientation in degrees
        Console.WriteLine($"X={position.X} Y={position.Y} Z={position.Z}");
        Console.WriteLine($"Rx={position.Rx} Ry={position.Ry} Rz={position.Rz}");

        // Frame, tool and posture of the position
        Console.WriteLine($"{position.DataType}, tool {position.ToolNumber}, user frame {position.UserCoordinateNumber}");
        Console.WriteLine(position.Form);

        robot.Disconnect();
    }
}
```

| Property               | Content                                                                        |
| ---------------------- | ------------------------------------------------------------------------------ |
| `X`, `Y`, `Z`          | Position, in mm                                                                |
| `Rx`, `Ry`, `Rz`       | Orientation, in degrees                                                        |
| `DataType`             | Frame of the values, for example `RobotCoordinateValue`                        |
| `ToolNumber`           | Tool used for the position                                                     |
| `UserCoordinateNumber` | User frame, when `DataType` is `UserCoordinateValue`                           |
| `Form`                 | Posture of the robot, see [Motion](hses-motion.md#posture) |

Keep the `Form` of a position when you send the robot back to it: the same Cartesian position can be reached with several postures.

## Joint positions

`GetRobotJointPosition()` reads the position of each axis of the first robot, in encoder pulses.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class PositionJoints
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        RobotPositionIntData joints = robot.HighSpeedEServer.GetRobotJointPosition();

        // One value per axis, in encoder pulses. Index 0 is the S axis
        int[] pulses = joints.Axes;
        Console.WriteLine(string.Join(", ", pulses));

        // The same values, axis by axis
        Console.WriteLine($"S={joints.Axis1} L={joints.Axis2} U={joints.Axis3} R={joints.Axis4} B={joints.Axis5} T={joints.Axis6}");

        robot.Disconnect();
    }
}
```

`Axes` has 8 values. On a 6 axis robot, the indexes 0 to 5 are the axes S, L, U, R, B and T, and the indexes 6 and 7 are `0`. `Axis1` to `Axis8` give the same values. [Axis names](hses-system.md#axis_names) gives the axes of your robot.

The pulses are the unit of the controller for the joints. The number of pulses per degree depends on the axis and on the robot model: it is a parameter of the controller. Send the pulses back to `MoveJoints` as they are, without conversion.

## Position error and torque

`GetPositionError()` reads the difference between the command and the feedback of each axis, in pulses. `GetTorque()` reads the torque of each axis, in percent of the rated torque.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class PositionErrorTorque
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Difference between the command and the feedback of each axis, in pulses
        RobotAxisIntData error = robot.HighSpeedEServer.GetPositionError();
        Console.WriteLine(string.Join(", ", error.Axes));

        // Torque of each axis, in percent of the rated torque
        RobotAxisIntData torque = robot.HighSpeedEServer.GetTorque();
        Console.WriteLine(string.Join(", ", torque.Axes));

        robot.Disconnect();
    }
}
```

Read them in a loop during a move to see the load of each axis, or to detect a collision or a wear in your application.

In Python 2.2.0, these two methods take the control group, as in the code above.

## Other control groups

A controller can drive several robots, base axes (travel tracks) and stations (positioners). `GetRobotPosition(group)`, `GetPositionError(group)` and `GetTorque(group)` read the axes of one control group.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class PositionControlGroup
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Second robot of the controller, in pulses
        var r2 = new RobotControlGroup(ControlGroup.RobotPulseValue, 2);
        RobotPositionIntData r2Joints = robot.HighSpeedEServer.GetRobotPosition(r2);

        // First base axis group (travel track), in pulses
        var b1 = new RobotControlGroup(ControlGroup.BasePulseValue, 1);
        RobotPositionIntData b1Axes = robot.HighSpeedEServer.GetRobotPosition(b1);

        // Torque of the base axes
        RobotAxisIntData b1Torque = robot.HighSpeedEServer.GetTorque(b1);

        robot.Disconnect();
    }
}
```

| `ControlGroup`    | Axes, unit                                | Number                |
| ----------------- | ----------------------------------------- | --------------------- |
| `RobotPulseValue` | Robot, in pulses                          | `1` to `8` (R1 to R8) |
| `RobotCartesian`  | Robot, Cartesian values of the controller | `1` to `8`            |
| `BasePulseValue`  | Base axes, in pulses                      | `1` to `8` (B1 to B8) |
| `BaseCartesian`   | Base axes, Cartesian values               | `1` to `8`            |

`GetRobotPosition` returns the raw values of the controller. With a Cartesian group, `Axes` holds X, Y, Z in micrometers and Rx, Ry, Rz in 1/10000 degree. `GetRobotCartesianPosition()` does this conversion for the first robot.

`RobotControlGroup.DefaultRobotCartesian` and `RobotControlGroup.DefaultRobotPulse` are the groups of the first robot, in .NET.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md#highspeedeserverclientbase-robothighspeedeserver))

- `RobotAxisIntData GetPositionError()`: Reads the position error (difference between commanded and actual position) for the default robot. Values indicate servo tracking error in pulse units.
- `RobotAxisIntData GetPositionError(RobotControlGroup type)`: Reads the position error for a specified control group. Position error indicates the difference between commanded and actual position.
- `RobotPositionCartesianData GetRobotCartesianPosition()`: Reads the current robot Cartesian position (TCP position and orientation). Coordinates are returned in millimeters for X, Y, Z and degrees for Rx, Ry, Rz.
- `RobotPositionIntData GetRobotJointPosition()`: Reads the current robot joint position in pulse (encoder) values. Returns raw pulse values for all robot axes.
- `RobotPositionIntData GetRobotPosition(RobotControlGroup type)`: Reads position data for a specified control group. Can read robot, base, or station position data depending on the control group specified.
- `RobotAxisIntData GetTorque()`: Reads the current torque values for the default robot's servo motors. Torque values indicate motor load as a percentage of rated torque.
- `RobotAxisIntData GetTorque(RobotControlGroup type)`: Reads the current torque values for a specified control group's servo motors. Torque values indicate motor load as a percentage of rated torque.

**RobotPositionCartesianData** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotpositioncartesiandata))

- `RobotPositionDataType DataType { get; }`: Gets the position data type indicating the coordinate system used.
- `RobotPosture Form { get; }`: Gets the robot posture (form) data defining the kinematic configuration.
- `double Rx { get; }`: Gets the rotation around X axis (Rx) in degrees.
- `double Ry { get; }`: Gets the rotation around Y axis (Ry) in degrees.
- `double Rz { get; }`: Gets the rotation around Z axis (Rz) in degrees.
- `int ToolNumber { get; }`: Gets the tool number (TCP) used for this position.
- `int UserCoordinateNumber { get; }`: Gets the user coordinate system number used for this position.
- `double X { get; }`: Gets the X coordinate in millimeters.
- `double Y { get; }`: Gets the Y coordinate in millimeters.
- `double Z { get; }`: Gets the Z coordinate in millimeters.

**RobotPositionIntData** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotpositionintdata))

- `RobotPositionIntData()`: Creates a blank instance of RobotPositionIntData
- `RobotPositionIntData(RobotDataHeader header)`: Creates a new instance of RobotPositionIntData with the specified header information.
- `RobotPositionCartesianData ToCartesian()`: Converts a Cartesian position to millimeters and degrees.
- `RobotPosture Form { get; set; }`: Gets or sets the robot posture (form) data defining the robot's kinematic configuration. This includes flip/no-flip state, arm configuration (upper/lower), and axis angle ranges.
- `RobotPositionDataType DataType { get; set; }`: Gets or sets the position data type indicating the coordinate system used. Determines how axis values should be interpreted (pulse, base, robot, user, or tool coordinates).
- `int ToolNumber { get; set; }`: Gets or sets the tool number (TCP - Tool Center Point) used for this position. Tool numbers typically range from 0-63, where 0 is often the robot flange center.
- `int UserCoordinateNumber { get; set; }`: Gets or sets the user coordinate system number used for this position. User coordinates define custom reference frames for specific workpiece locations.
- `bool IsDefined { get; }`: Gets whether the variable is taught on the controller. False for a variable read with Int32%2cSystem.Int32) that is not defined: its values are then all 0.
- `int[] Axes { get; }`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `int Axis1 { get; set; }`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `int Axis2 { get; set; }`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `int Axis3 { get; set; }`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `int Axis4 { get; set; }`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `int Axis5 { get; set; }`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `int Axis6 { get; set; }`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `int Axis7 { get; set; }`: Gets or sets the value for axis 7 (optional additional axis).
- `int Axis8 { get; set; }`: Gets or sets the value for axis 8 (optional additional axis).

**RobotAxisIntData** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotaxisintdata))

- `int[] Axes { get; }`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `int Axis1 { get; set; }`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `int Axis2 { get; set; }`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `int Axis3 { get; set; }`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `int Axis4 { get; set; }`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `int Axis5 { get; set; }`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `int Axis6 { get; set; }`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `int Axis7 { get; set; }`: Gets or sets the value for axis 7 (optional additional axis).
- `int Axis8 { get; set; }`: Gets or sets the value for axis 8 (optional additional axis).

**RobotControlGroup** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotcontrolgroup))

- `RobotControlGroup(ControlGroup group, int index)`: Creates a new RobotControlGroup with the specified group type and index.
- `readonly byte ByteValue`: The combined byte value sent to the robot controller (Group + Index).
- `static readonly RobotControlGroup DefaultRobotCartesian`: Default control group for Cartesian position of robot 1.
- `static readonly RobotControlGroup DefaultRobotPulse`: Default control group for pulse position of robot 1.
- `readonly ControlGroup Group`: The control group type (robot, base, station).
- `readonly int Index`: The index within the control group (e.g., robot number 1-8).

**ControlGroup** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#controlgroup))

- BaseCartesian: Base axes in Cartesian coordinates. Valid index: 1-8.
- BasePulseValue: Base axes in pulse values. Valid index: 1-8.
- RobotCartesian: Robot axes in Cartesian coordinates. Valid index: 1-8.
- RobotPulseValue: Robot axes in pulse (encoder) values. Valid index: 1-8.
- StationPulseValue: Station axes in pulse values. Valid index: 1-24 (S1 to S24).

**RobotPositionDataType** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotpositiondatatype))

- BaseCoordinateValue: Position in base coordinate system (world frame, value 16).
- PulseValue: Position in encoder pulse values (joint space).
- RobotCoordinateValue: Position in robot coordinate system (robot base frame, value 17).
- ToolCoordinateValue: Position in tool coordinate system (value 18).
- UserCoordinateValue: Position in user-defined coordinate system (value 19).
