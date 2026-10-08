# Positions and torque

Read the joint pulses and the Cartesian position in the base, robot, user or tool frame, the posture, the torque and the encoder temperatures through the Ethernet Server.

Web page: https://underautomation.com/yaskawa/documentation/eserver-positions

This page shows how to read the position of a Yaskawa Motoman robot through the Ethernet Server: joint pulses, Cartesian position in the base, robot, user or tool frame, posture, torque and encoder temperatures. It covers the YRC1000 and YRC1000micro controllers.

## Read the position

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerPositions
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Joints, in encoder pulses
        HostControlJointPositionData joints = robot.EServer.GetRobotJointPosition();
        Console.WriteLine($"S={joints.S} L={joints.L} U={joints.U} R={joints.R} B={joints.B} T={joints.T}");

        // Cartesian position in the base frame (default), mm and degrees
        HostControlCartesianPositionData tcp = robot.EServer.GetRobotCartesianPosition();
        Console.WriteLine($"X={tcp.X} Y={tcp.Y} Z={tcp.Z} Rx={tcp.Rx} Ry={tcp.Ry} Rz={tcp.Rz}");

        // Posture of the arm and tool of the position
        Console.WriteLine($"Front: {tcp.IsFront}, upper arm: {tcp.IsUpperArm}, flip: {tcp.IsFlip}, tool: {tcp.ToolNumber}");

        // Same position in the robot frame, or in a user frame
        var inRobot = robot.EServer.GetRobotCartesianPosition(HostControlCoordinateSystem.Robot);
        var inUser1 = robot.EServer.GetRobotCartesianPosition(HostControlCoordinateSystem.User1);

        // With the external axes (Re, Axis8...)
        var withExternal = robot.EServer.GetRobotCartesianPosition(HostControlCoordinateSystem.Base, true);

        robot.Disconnect();
    }
}
```

### Joint position

`GetRobotJointPosition()` reads the encoder pulses of each axis: `S`, `L`, `U`, `R`, `B`, `T`, then `E` and `Axis8` to `Axis12` for the external axes. `Axes` gives the same values in one array of 12 values.

The number of pulses per degree depends on the axis and on the robot model. To compute a position from joint angles, see [Offline kinematics](kinematics.md).

### Cartesian position

`GetRobotCartesianPosition(coordinateSystem, includeExternalAxes)` reads the position of the tool center point, in mm and degrees.

| `HostControlCoordinateSystem` | Frame of the values      |
| ----------------------------- | ------------------------ |
| `Base` (default)              | Base frame               |
| `Robot`                       | Robot frame              |
| `User1` to `User8`            | User frame 1 to 8        |
| `Tool`                        | Tool frame               |

`ToolNumber` gives the tool of the position. On a 7-axis robot, `Re` holds the elbow angle.

With `includeExternalAxes` set to `true`, `Axis8` to `Axis12` also hold the positions of the external axes. On a 6-axis robot, `Re` holds the 7th axis.

On a robot without base axis, the base frame and the robot frame give the same values.

### Posture

The same Cartesian position can be reached with several postures of the arm. `Type` holds the posture, and these properties decode it:

| Property                                         | Meaning                                       |
| ------------------------------------------------ | --------------------------------------------- |
| `IsFront`                                        | The wrist is in front of the S axis           |
| `IsUpperArm`                                     | The elbow is above the line shoulder to wrist |
| `IsFlip`                                         | Flip posture of the wrist                     |
| `IsRLessThan180`, `IsTLessThan180`, `IsSLessThan180` | The angle of the axis is less than 180 degrees |

Pass the `Type` to `MoveJoint` and `MoveLinear` to send the robot back to a position with the same posture. See [Motion](eserver-motion.md).

## Torque and encoder temperatures

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerTorque
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Torque of each axis, in percent of the rated torque
        HostControlTorqueData torque = robot.EServer.GetTorque();
        HostControlTorqueData maxTorque = robot.EServer.GetMaxTorque();

        // Temperature of the encoder of each axis, in degrees Celsius
        HostControlEncoderTemperatureData temperatures = robot.EServer.GetEncoderTemperature();

        for (int axis = 0; axis < 6; axis++)
            Console.WriteLine($"Axis {axis + 1}: {torque.Values[axis]} % (max {maxTorque.Values[axis]} %), {temperatures.Values[axis]} C");

        robot.Disconnect();
    }
}
```

| Method                    | Values                                                    |
| ------------------------- | --------------------------------------------------------- |
| `GetTorque()`             | Torque of each axis, in percent of the rated torque       |
| `GetMaxTorque()`          | Maximum torque of each axis, in percent                   |
| `GetEncoderTemperature()` | Temperature of the encoder of each axis, in degrees Celsius |

Each array has 12 values: the 6 axes of the robot, then the external axes. With the servo off, the torques are 0. A log of the encoder temperatures over a shift shows which axis heats up in a cycle.

## Control group and task

`GetControlGroup()` reads the robot group, the station group and the task selected for the next commands. `SetControlGroup(robotGroup, stationGroup)` and `SetTask(task)` change them, on a controller with several robots, stations or tasks.

## Reference

**Methods of HostControlClientBase** ([reference](../api/UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolclientbase-roboteserver))

- `HostControlGroupData GetControlGroup()`: Reads the current control group configuration. Returns robot group bits, station group bits, and current task number.
- `HostControlEncoderTemperatureData GetEncoderTemperature()`: Reads the encoder temperature values of all robot axes.
- `HostControlTorqueData GetMaxTorque()`: Reads the maximum torque values of all robot axes. Returns values as a percentage of the maximum rated torque.
- `HostControlCartesianPositionData GetRobotCartesianPosition(HostControlCoordinateSystem coordinateSystem = HostControlCoordinateSystem.Base, bool includeExternalAxes = false)`: Reads the current robot Cartesian position (TCP position and orientation). Coordinates are returned in millimeters for X, Y, Z and degrees for Rx, Ry, Rz.
- `HostControlJointPositionData GetRobotJointPosition()`: Reads the current robot joint position in pulse (encoder) values. Returns raw pulse values for all robot axes (S, L, U, R, B, T, and external axes).
- `HostControlTorqueData GetTorque()`: Reads the current torque values of all robot axes. Returns values as a percentage of the maximum rated torque.
- `HostControlUserFrameData GetUserFrame(int userCoordinateNumber)`: Reads user coordinate frame data from the robot controller. Returns the three reference points (ORG, XX, XY) defining the user coordinate system.
- `HostControlResponse SetControlGroup(int robotGroup, int stationGroup)`: Changes the control group selection.
- `HostControlResponse SetTask(int task)`: Changes the current task selection.
- `HostControlResponse SetUserFrame(int userCoordinateNumber, HostControlUserFrameData frame)`: Writes user coordinate frame data to the robot controller. Defines a user coordinate system using three reference points (ORG, XX, XY).

**HostControlJointPositionData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontroljointpositiondata))

- `int[] Axes { get; }`: Gets all axis values as an array of encoder pulse values. Array contains 12 elements: S, L, U, R, B, T, E, Axis8 through Axis12.
- `int Axis10 { get; }`: Gets or sets the 10th axis position in pulses.
- `int Axis11 { get; }`: Gets or sets the 11th axis position in pulses.
- `int Axis12 { get; }`: Gets or sets the 12th axis position in pulses.
- `int Axis8 { get; }`: Gets or sets the 8th axis position in pulses.
- `int Axis9 { get; }`: Gets or sets the 9th axis position in pulses.
- `int B { get; }`: Gets or sets the B axis position in pulses.
- `int E { get; }`: Gets or sets the E axis (7th axis) position in pulses.
- `int L { get; }`: Gets or sets the L axis position in pulses.
- `int R { get; }`: Gets or sets the R axis position in pulses.
- `int S { get; }`: Gets or sets the S axis position in pulses.
- `int T { get; }`: Gets or sets the T axis position in pulses.
- `int U { get; }`: Gets or sets the U axis position in pulses.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

**HostControlCartesianPositionData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolcartesianpositiondata))

- `double Axis10 { get; }`: Gets or sets the 10th external axis value.
- `double Axis11 { get; }`: Gets or sets the 11th external axis value.
- `double Axis12 { get; }`: Gets or sets the 12th external axis value.
- `double Axis8 { get; }`: Gets or sets the 8th external axis value.
- `double Axis9 { get; }`: Gets or sets the 9th external axis value.
- `int CoordinateSystem { get; }`: Gets or sets the coordinate system index. 0: Base, 1-65: User coordinates.
- `bool IsFlip { get; }`: Gets whether the robot is in flip configuration.
- `bool IsFront { get; }`: Gets whether the robot is in front configuration.
- `bool IsRLessThan180 { get; }`: Gets whether R axis is less than 180 degrees.
- `bool IsSLessThan180 { get; }`: Gets whether S axis is less than 180 degrees.
- `bool IsTLessThan180 { get; }`: Gets whether T axis is less than 180 degrees.
- `bool IsUpperArm { get; }`: Gets whether the robot is in upper arm configuration.
- `double Re { get; }`: Gets or sets the Re (7th axis rotation) in degrees or millimeters.
- `double Rx { get; }`: Gets or sets the Rx (rotation around X axis) in degrees.
- `double Ry { get; }`: Gets or sets the Ry (rotation around Y axis) in degrees.
- `double Rz { get; }`: Gets or sets the Rz (rotation around Z axis) in degrees.
- `int Type { get; }`: Gets or sets the robot posture/configuration type. Defines arm configuration (flip, upper/lower arm, front/back, etc.).
- `double X { get; }`: Gets or sets the X position in millimeters.
- `double Y { get; }`: Gets or sets the Y position in millimeters.
- `double Z { get; }`: Gets or sets the Z position in millimeters.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

**HostControlCoordinateSystem** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolcoordinatesystem))

- Base: Base coordinate system (robot base frame).
- Robot: Robot coordinate system.
- Tool: Tool coordinate system.
- User1: User coordinate system 1.
- User2: User coordinate system 2.
- User3: User coordinate system 3.
- User4: User coordinate system 4.
- User5: User coordinate system 5.
- User6: User coordinate system 6.
- User7: User coordinate system 7.
- User8: User coordinate system 8.

**HostControlTorqueData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontroltorquedata))

- `double[] Values { get; }`: Gets the torque values for each axis (up to 12 axes). Values are in percentage of maximum rated torque.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

**HostControlEncoderTemperatureData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolencodertemperaturedata))

- `double[] Values { get; }`: Gets the temperature values for each axis encoder (up to 12 axes). Values are in degrees Celsius.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

**HostControlGroupData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolgroupdata))

- `int RobotGroup { get; }`: Gets or sets the robot group bits. Each bit represents a robot control group (R1, R2, etc.).
- `int StationGroup { get; }`: Gets or sets the station group bits. Each bit represents a station control group (S1, S2, etc.).
- `int Task { get; }`: Gets or sets the current task number. 0: Master task, 1-15: Sub tasks.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## What to read next

- [Get the robot position](how-to-get-position.md): which protocol and which method to choose.
- [Motion](eserver-motion.md): send the robot to a position.
