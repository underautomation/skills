# Registers

Read and write numeric registers (R[]), position registers (PR[]), string registers (SR[]), and flags (F[]) via SNPX.

Web page: https://underautomation.com/fanuc/documentation/snpx-registers

SNPX provides fast read and write access to all register types: numeric (R[]), position (PR[]), string (SR[]), and flags (F[]).

## Numeric registers (R[])

Numeric registers store floating-point, 32-bit integer, or 16-bit integer values.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxRegistersNumeric
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Read R[1] as float (default)
        float value = robot.Snpx.NumericRegisters.Read(1);

        // Write R[1]
        robot.Snpx.NumericRegisters.Write(1, 123.45f);

        // Read as 32-bit integer
        int intValue = robot.Snpx.NumericRegistersInt32.Read(1);
        robot.Snpx.NumericRegistersInt32.Write(1, 999);

        // Read as 16-bit integer
        short shortValue = robot.Snpx.NumericRegistersInt16.Read(1);
    }
}
```

## Position registers (PR[])

Position registers store joint or Cartesian positions with tool and frame info.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxRegistersPosition
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Read PR[1]
        Position posReg = robot.Snpx.PositionRegisters.Read(1);

        short userFrame = posReg.UserFrame;
        short userTool = posReg.UserTool;

        // A representation that the register does not hold is null
        if (posReg.CartesianPosition != null)
        {
            double x = posReg.CartesianPosition.X;
        }

        if (posReg.JointsPosition != null)
        {
            double j1 = posReg.JointsPosition.J1;
        }

        // Write Cartesian position to PR[1]
        robot.Snpx.PositionRegisters.Write(1, new CartesianPosition(100, 200, 300, 0, 90, 0));

        // Write joint position to PR[1]
        robot.Snpx.PositionRegisters.Write(1, new JointsPosition { J1 = 0, J2 = 0, J3 = 0, J4 = 0, J5 = 0, J6 = 45 });
    }
}
```

To know if a register holds joint or Cartesian values, test each representation of the `Position` you read:

- C#: `JointsPosition` or `CartesianPosition` is `null` when the register does not hold this representation.
- Python (version 7.1.0): `joints_position` and `cartesian_position` never return `None`. A representation that the register does not hold converts to an empty string with `str()`, and reading one of its values raises `AttributeError`. Test `str(pos_reg.joints_position)` before you read the joint values.

## String registers (SR[]) and flags (F[])

The default string length is 80 characters. You can change it with `StringRegisters.StringLength` (must be even, >= 2).

```csharp
using UnderAutomation.Fanuc;

public class SnpxRegistersString
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Read SR[1]
        string text = robot.Snpx.StringRegisters.Read(1);

        // Write SR[1]
        robot.Snpx.StringRegisters.Write(1, "Hello, Robot!");

        // Read F[1]
        bool flag = robot.Snpx.Flags.Read(1);

        // Write F[1]
        robot.Snpx.Flags.Write(1, true);
    }
}
```

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxRegisters
{
  public static void Main()
  {
    // Create a FanucRobot instance
    FanucRobot robot = new FanucRobot();

    // Set SNPX connection parameters (example values)
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Snpx.Enable = true;

    // Connect with SNPX enabled
    robot.Connect(parameters);

    // 1) Numeric Registers: Read & Write
    ReadWriteNumericRegisters(robot);

    // 2) Position Registers: Read & Write
    ReadWritePositionRegisters(robot);

    // 3) String Registers: Read & Write
    ReadWriteStringRegisters(robot);
  }

  private static void ReadWriteNumericRegisters(FanucRobot robot)
  {
    // Read numeric register R[1]
    float numReg1 = robot.Snpx.NumericRegisters.Read(1);
    Console.WriteLine($"📊 R[1] = {numReg1}");

    // Write numeric register R[1]
    robot.Snpx.NumericRegisters.Write(1, 123.45f);
    Console.WriteLine("✅ Wrote 123.45 to R[1]");
  }

  private static void ReadWritePositionRegisters(FanucRobot robot)
  {
    // Read position register PR[1]
    Position posReg1 = robot.Snpx.PositionRegisters.Read(1);
    Console.WriteLine("\n🤖 Current PR[1]:");
    Console.WriteLine($"   UserFrame = {posReg1.UserFrame}");
    Console.WriteLine($"   UserTool = {posReg1.UserTool}");

    // If the register is Cartesian
    if (posReg1.CartesianPosition != null)
    {
      Console.WriteLine("   CartesianPosition:");
      Console.WriteLine($"      X = {posReg1.CartesianPosition.X}");
      Console.WriteLine($"      Y = {posReg1.CartesianPosition.Y}");
      Console.WriteLine($"      Z = {posReg1.CartesianPosition.Z}");
      Console.WriteLine($"      W = {posReg1.CartesianPosition.W}");
      Console.WriteLine($"      P = {posReg1.CartesianPosition.P}");
      Console.WriteLine($"      R = {posReg1.CartesianPosition.R}");
      Console.WriteLine("      Configuration :");
      Console.WriteLine($"         ArmFrontBack = {posReg1.CartesianPosition.Configuration.ArmFrontBack}");
      Console.WriteLine($"         ArmLeftRight = {posReg1.CartesianPosition.Configuration.ArmLeftRight}");
      Console.WriteLine($"         ArmUpDown = {posReg1.CartesianPosition.Configuration.ArmUpDown}");
      Console.WriteLine($"         WristFlip = {posReg1.CartesianPosition.Configuration.WristFlip}");
    }

    // If the register is Joint-based
    if (posReg1.JointsPosition != null)
    {
      Console.WriteLine("   JointsPosition:");
      Console.WriteLine($"      J1 = {posReg1.JointsPosition.J1}");
      Console.WriteLine($"      J2 = {posReg1.JointsPosition.J2}");
      Console.WriteLine($"      J3 = {posReg1.JointsPosition.J3}");
      Console.WriteLine($"      J4 = {posReg1.JointsPosition.J4}");
      Console.WriteLine($"      J5 = {posReg1.JointsPosition.J5}");
      Console.WriteLine($"      J6 = {posReg1.JointsPosition.J6}");
    }

    // Write a Cartesian position to PR[1]
    Console.WriteLine("\n✅ Writing Cartesian position to PR[1]...");
    robot.Snpx.PositionRegisters.Write(1, new CartesianPosition(x: 0.1f, y: 0.2f, z: 0.3f, w: 0.4f, p: 0.5f, r: 0.6f));

    // Write a Joint position to PR[1]
    Console.WriteLine("✅ Writing Joint position to PR[1]...");
    robot.Snpx.PositionRegisters.Write(1, new JointsPosition { J1 = 0, J2 = 0, J3 = 0, J4 = 0, J5 = 0, J6 = 45 });
  }

  private static void ReadWriteStringRegisters(FanucRobot robot)
  {
    // Read string register SR[1]
    string strReg1 = robot.Snpx.StringRegisters.Read(1);
    Console.WriteLine($"\n💬 SR[1] = '{strReg1}'");

    // Write string register SR[1]
    robot.Snpx.StringRegisters.Write(1, "Hello, Robot!");
    Console.WriteLine("✅ Wrote 'Hello, Robot!' to SR[1]");
  }
}
```

## API reference

**NumericRegisters** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#numericregisters-robotsnpxnumericregisters))

- `NumericRegistersBatchAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for reading multiple numeric registers.
- `void Write(int index, float value)`: Write value at a certain index.
- `float Read(int index)`: Reads the value at the specified index.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

**PositionRegisters** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#positionregisters-robotsnpxpositionregisters))

- `PositionRegistersBatchAssignment CreateBatchAssignment(int startIndex, int count)`: Creates a batch assignment for reading multiple position registers.
- `Position Read(int index)`: Reads the position at the specified register index.
- `void Write(int index, CartesianPosition cartesianPosition)`: Writes a Cartesian position to the specified position register.
- `void Write(int index, ExtendedCartesianPosition extendedCartesianPosition)`: Writes an extended Cartesian position to the specified position register.
- `void Write(int index, JointsPosition jointsPosition)`: Writes a joints position to the specified position register.
- `Assignment<int> GetOrCreateAssignment(int index)`: Gets or creates an assignment for the specified index.

**Position** ([reference](../api/UnderAutomation.Fanuc.Common.md#position))

- `Position()`: Default constructor
- `Position(short userFrame, short userTool, JointsPosition jointsPosition, ExtendedCartesianPosition cartesianPosition)`: Constructor with user frame, tool, joints and cartesian position
- `ExtendedCartesianPosition CartesianPosition { get; set; }`: Cartesian position with extended axes
- `JointsPosition JointsPosition { get; set; }`: Joint values in degrees
- `short UserFrame { get; set; }`: User frame index
- `short UserTool { get; set; }`: User tool index

**JointsPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#jointsposition-robotstreammotionqueueendjointposition))

- `JointsPosition()`: Default constructor
- `JointsPosition(double j1Deg, double j2Deg, double j3Deg, double j4Deg, double j5Deg, double j6Deg)`: Constructor with 6 joint values in degrees
- `JointsPosition(double j1Deg, double j2Deg, double j3Deg, double j4Deg, double j5Deg, double j6Deg, double j7Deg, double j8Deg, double j9Deg)`: Constructor with 9 joint values in degrees
- `JointsPosition(double[] values)`: Constructor from an array of joint values in degrees
- `static bool IsNear(JointsPosition j1, JointsPosition j2, double degreesTolerance)`: Check if joints position is near to expected joints position with a tolerance value
- `double this[int i] { get; set; }`: Gets or sets the joint value at the specified index
- `double J1 { get; set; }`: Joint 1 in degrees
- `double J2 { get; set; }`: Joint 2 in degrees
- `double J3 { get; set; }`: Joint 3 in degrees
- `double J4 { get; set; }`: Joint 4 in degrees
- `double J5 { get; set; }`: Joint 5 in degrees
- `double J6 { get; set; }`: Joint 6 in degrees
- `double J7 { get; set; }`: Joint 7 in degrees
- `double J8 { get; set; }`: Joint 8 in degrees
- `double J9 { get; set; }`: Joint 9 in degrees
- `double[] Values { get; }`: Numeric values for each joints

**ExtendedCartesianPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#extendedcartesianposition-robotstreammotionqueueendcartesianposition))

- `ExtendedCartesianPosition()`: Default constructor
- `ExtendedCartesianPosition(double x, double y, double z, double w, double p, double r, double e1, double e2, double e3)`: Constructor with position, rotations, and extended axes
- `double E1 { get; set; }`: Extended axis 1 value
- `double E2 { get; set; }`: Extended axis 2 value
- `double E3 { get; set; }`: Extended axis 3 value
- Inherited from [CartesianPosition](../api/UnderAutomation.Fanuc.Common.md#cartesianposition-robotstreammotionqueueendcartesianposition): `FromHomogeneousMatrix`, `NormalizeAngle`, `NormalizeAngles`, `IsNear`, `Configuration`
- Inherited from [XYZWPRPosition](../api/UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](../api/UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`

**CartesianPosition** ([reference](../api/UnderAutomation.Fanuc.Common.md#cartesianposition-robotstreammotionqueueendcartesianposition))

- `CartesianPosition()`: Default constructor
- `CartesianPosition(double x, double y, double z, double w, double p, double r)`: Constructor with position and rotations
- `CartesianPosition(double x, double y, double z, double w, double p, double r, Configuration configuration)`: Constructor with position, rotations and configuration
- `CartesianPosition(CartesianPosition position)`: Copy constructor
- `CartesianPosition(XYZPosition position, double w, double p, double r)`: Constructor from an XYZ position with rotations
- `Configuration Configuration { get; set; }`: Position configuration
- `static CartesianPosition FromHomogeneousMatrix(double[,] R)`: Create a CartesianPosition with unknow configuration from a homogeneous rotation and translation 4x4 matrix
- `static bool IsNear(CartesianPosition a, CartesianPosition b, double mmTolerance, double degreesTolerance)`: Check if two Cartesian positions are near each other within specified tolerances
- `static double NormalizeAngle(double angle)`: Normalize an angle to the range ]-180, 180]
- `static void NormalizeAngles(CartesianPosition pose)`: Normalize the W, P, R angles to the range ]-180, 180]
- Inherited from [XYZWPRPosition](../api/UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](../api/UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`
