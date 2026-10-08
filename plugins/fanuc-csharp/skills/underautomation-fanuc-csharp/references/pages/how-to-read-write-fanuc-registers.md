# Read & write registers

Compare all methods to read and write numeric, position, and string registers on a Fanuc robot: SNPX, FTP, CGTP, and Telnet.

Web page: https://underautomation.com/fanuc/documentation/how-to-read-write-fanuc-registers

Registers are the primary data exchange mechanism on Fanuc robots. This guide shows how to read and write numeric (R[]), position (PR[]), string (SR[]), and flag (F[]) registers using different protocols.

## SNPX (fastest : ~2 ms)

SNPX provides the fastest register access with typed read/write operations.

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

See also: [SNPX Registers](snpx-registers.md)

## CGTP Web Server

CGTP reads registers with their comments in a single request.

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;
using UnderAutomation.Fanuc.Common;

public class HowToReadWriteFanucRegistersCgtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read R[1] with comment
        NumericRegisterWithComment reg = robot.Cgtp.ReadNumericRegisterWithComment(1);
        Console.WriteLine($"R[1] = {reg.RealValue} ({reg.Comment})");

        // Write R[5]
        robot.Cgtp.WriteNumericRegisterAsDouble(5, 123.45);

        // Read PR[1] with comment
        PositionRegisterWithComment posReg = robot.Cgtp.ReadPositionRegisterWithComment(1);

        // Write PR[1] as Cartesian
        robot.Cgtp.WritePositionRegisterAsCartesian(1, new CartesianPosition(100, 200, 300, 0, 90, 0));

        // Write SR[1]
        robot.Cgtp.WriteStringRegister(1, "Hello");
    }
}
```

See also: [CGTP Registers & variables](cgtp-registers-variables.md)

## FTP (offline parsing)

FTP lets you download register files and parse them locally:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common.Files.Variables;

public class HowToReadWriteFanucRegistersFtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Get all numeric registers with comments
        NumregFile numRegs = robot.Ftp.KnownVariableFiles.GetNumregFile();

        // Get all position registers with comments
        PosregFile posRegs = robot.Ftp.KnownVariableFiles.GetPosregFile();

        // Get all string registers with comments
        StrregFile strRegs = robot.Ftp.KnownVariableFiles.GetStrregFile();
    }
}
```

See also: [FTP Diagnostics & variables](ftp-diagnostics.md)

## Protocol comparison

| Feature | SNPX | CGTP | FTP |     
|---------|------|------|-----|
| **Speed** | ~2 ms | ~10 ms | ~100 ms | 
| **Read with comment** | Via Comments API | Yes (single request) | Yes (file parse) | 
| **Batch read** | Yes (same speed) | Yes (batch API) | Yes (all at once) | 
| **Write** | Yes | Yes | No |
| **Position registers** | Yes | Yes | Yes (read only) | 
| **String registers** | Yes | Yes | Yes (read only) |
| **Flags** | Yes | Via I/O API | Yes (read only) |
