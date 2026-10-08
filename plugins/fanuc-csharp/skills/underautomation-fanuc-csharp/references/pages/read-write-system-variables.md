# Read & write system variables

Access and modify Fanuc system variables ($RMT_MASTER, $MCR.$GENOVERRIDE, etc.) using Telnet, SNPX, CGTP, or FTP.

Web page: https://underautomation.com/fanuc/documentation/read-write-system-variables

Read and write system variables ($RMT_MASTER, $MCR.$GENOVERRIDE, etc.) on your Fanuc robot using different protocols.

## SNPX (fastest : ~2 ms)

SNPX supports 4 typed variable categories: integer, real, position, and string.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxVariables
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Snpx.Enable = true;

    robot.Connect(parameters);

    // --- Integer system variables ---
    int rmtMaster = robot.Snpx.IntegerSystemVariables.Read("$RMT_MASTER");
    robot.Snpx.IntegerSystemVariables.Write("$RMT_MASTER", 1);

    // --- Real (float) system variables ---
    float genOverride = robot.Snpx.RealSystemVariables.Read("$MCR.$GENOVERRIDE");
    robot.Snpx.RealSystemVariables.Write("$MCR.$GENOVERRIDE", 50.0f);

    // --- Position system variables ---
    Position cellFloor = robot.Snpx.PositionSystemVariables.Read("$CELL_FLOOR");
    robot.Snpx.PositionSystemVariables.Write("$CELL_FLOOR", cellFloor);

    // --- String system variables ---
    string lastAlm = robot.Snpx.StringSystemVariables.Read("$ALM_IF.$LAST_ALM");
    robot.Snpx.StringSystemVariables.Write("$ALM_IF.$LAST_ALM", "No alarms");

    // --- Karel program variables ---
    int karelVar = robot.Snpx.IntegerSystemVariables.Read("$[MyKarelProg]my_variable");
    robot.Snpx.IntegerSystemVariables.Write("$[MyKarelProg]my_variable", 42);

    // --- Set variable (auto-detects type) ---
    robot.Snpx.SetVariable("$RMT_MASTER", 1);
  }
}
```

See also: [SNPX System variables](snpx-variables.md)

## Telnet KCL

Telnet reads and writes any variable using KCL commands:

```csharp
using UnderAutomation.Fanuc;

public class ReadWriteSystemVariablesTelnet
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read a variable
        var result = robot.Telnet.GetVariable("$RMT_MASTER");
        string value = result.RawValue;

        // Write a variable
        robot.Telnet.SetVariable("$RMT_MASTER", "1");
        robot.Telnet.SetVariable("$MCR.$GENOVERRIDE", "50");
    }
}
```

See also: [Telnet Variables & I/O](telnet-variables-io.md)

## CGTP Web Server

CGTP provides typed variable reading and string-based writing:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class ReadWriteSystemVariablesCgtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read with automatic type detection
        CgtpVariableValue var = robot.Cgtp.ReadVariable("$RMT_MASTER");
        int intVal = var.IntegerValue;

        // Write
        robot.Cgtp.WriteVariable("$RMT_MASTER", 1);
        robot.Cgtp.WriteVariable("$MCR.$GENOVERRIDE", 50.0);

        // Read and decode system.va
        SystemFile system = robot.Cgtp.Http.KnownVariableFiles.GetSystemFile();
        int rmtMaster = system.RmtMaster;

        // get all variables with their value and types
        VariableFileList filelist = robot.Cgtp.Http.GetAllVariables();
    }
}
```

See also: [CGTP Registers & variables](cgtp-registers-variables.md)

## FTP (offline parsing)

Download variable files and parse them offline:

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class ReadWriteSystemVariablesFtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read and decode system.va
        SystemFile system = robot.Ftp.KnownVariableFiles.GetSystemFile();
        int rmtMaster = system.RmtMaster;

        // get all variables with their value and types
        VariableFileList filelist = robot.Ftp.GetAllVariables();
    }
}
```

See also: [Offline file parsing](offline-file-parsing.md)

## Protocol comparison

| Feature | SNPX | Telnet | CGTP | FTP |
|---------|------|--------|------|-----|
| **Speed** | ~2 ms | ~30 ms | ~50 ms | ~100 ms |
| **Typed read** | Yes (4 types) | No (string) | Yes (auto-detect) | Yes (file parse) |
| **Write** | Yes | Yes | Yes | No |
| **Batch read** | Yes | No | Yes | Yes (all at once) |
| **Karel variables** | Yes | Yes | Yes | No |
| **Batch read all variables** | No | No | Yes | Yes |
