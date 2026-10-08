# Diagnostics & variables

Read safety status, current position, I/O state, installed features, error history, registers, and system variables via FTP.

Web page: https://underautomation.com/fanuc/documentation/ftp-diagnostics

Read safety status, current position, I/O state, error history, installed features, registers, and system variables from the Fanuc controller via FTP.

## Safety, position, I/O, and errors

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common.Files.Diagnosis;

public class FtpDiagnosticsSafety
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        // Safety status
        SafetyStatus safetyStatus = robot.Ftp.GetSafetyStatus();
        Console.WriteLine($"Emergency Stop: {safetyStatus.ExternalEStop}");
        Console.WriteLine($"Teach Pendant Enabled: {safetyStatus.TPEnable}");

        // Current position
        CurrentPosition currentPosition = robot.Ftp.GetCurrentPosition();

        // I/O state
        IOState ioState = robot.Ftp.GetIOState();

        // Error history
        var errors = robot.Ftp.GetAllErrorsList();
    }
}
```

**SafetyStatus** ([reference](../api/UnderAutomation.Fanuc.Common.Files.Diagnosis.md#safetystatus))

- `SafetyStatus()`
- `bool BeltBroken { get; }`: Belt broken signal is active
- `bool ExternalEStop { get; }`: External emergency stop active
- `bool FenceOpen { get; }`: Safety fence is open
- `bool HandBroken { get; }`: Hand broken signal is active
- `bool LowAirAlarm { get; }`: Low air pressure alarm is active
- `string Name { get; }`: File name : sftysig.dg
- `bool NonTeacherEnb { get; }`: Non-teacher enable signal is active
- `bool OverTravel { get; }`: Over travel limit is active
- `bool SOPEStop { get; }`: Emergency stop active by SOP signal
- `bool SVOFFDetect { get; }`: Servo off detection is active
- `bool TPDeadman { get; }`: The deadman switch of the teach pendant is active
- `bool TPEStop { get; }`: Emergency stop active on teach peandant
- `bool TPEnable { get; }`: Teach pendant is enabled

**CurrentPosition** ([reference](../api/UnderAutomation.Fanuc.Common.Files.Diagnosis.md#currentposition))

- `CurrentPosition()`
- `GroupPosition[] GroupsPosition { get; }`: Position of each robots handled by this controller
- `string Name { get; }`: File name : curpos.dg

**GroupPosition** ([reference](../api/UnderAutomation.Fanuc.Common.Files.Diagnosis.md#groupposition))

- `GroupPosition()`
- `int Id { get; }`: Group ID
- `JointsPosition JointsPosition { get; }`: Joint positions : the position of each robot angles
- `CartesianPositionWithUserFrame[] UserFramePositions { get; }`: Position of each tools in each user frames
- `CartesianPositionWithTool[] WorldPositions { get; }`: Position of each tools in world coordinates

**IOState** ([reference](../api/UnderAutomation.Fanuc.Common.Files.Diagnosis.md#iostate))

- `IOState()`
- `string Name { get; }`: File name : iostate.dg
- `IOStatus[] States { get; }`: Status of all controller inputs and outputs

**IOStatus** ([reference](../api/UnderAutomation.Fanuc.Common.md#iostatus))

- `IOStatus()`
- `int Id { get; }`: Digital port ID
- `string Name { get; }`: IO Name
- `DigitalPorts Port { get; }`: Digital port type
- `bool Value { get; }`: Digital port value

**DigitalPorts** ([reference](../api/UnderAutomation.Fanuc.Common.md#digitalports))

- DIN: Digital input
- DOUT: Digital outputs
- FLG: Flags
- RI: Robot inputs
- RO: Robot outputs
- SI: SI
- SO: SO
- UI: User inputs
- UO: User outputs

## Read variables

Variables are read in bulk from `.va` files stored on the controller.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common.Files.Variables;

public class FtpDiagnosticsVariables
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        // Get all variables from all files
        var allVariables = robot.Ftp.GetAllVariables();
        foreach (var file in allVariables)
            foreach (var variable in file.Variables)
                Console.WriteLine($"{variable.Name} = {variable.Value}");

        // Get variables from a specific file
        var variables = robot.Ftp.GetVariablesFromFile("SYSVARS.va");

        // Access commonly used system variables directly
        int rmtMaster = robot.Ftp.KnownVariableFiles.GetSystemFile().RmtMaster;
    }
}
```

## Read registers

Registers are read in bulk via FTP variable files.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common.Files.Variables;

public class FtpDiagnosticsRegisters
{
  public static void Main()
  {
    // Create a FanucRobot instance
    FanucRobot robot = new FanucRobot();

    // Set connection parameters (example values)
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Ftp.Enable = true;
    parameters.Ftp.FtpUser = "user";
    parameters.Ftp.FtpPassword = "ftp password";

    // Connect to the robot with FTP enabled
    robot.Connect(parameters);

    // 1) Reading Numeric Registers
    ReadNumericRegisters(robot);

    // 2) Reading Position Registers
    ReadPositionRegisters(robot);

    // 3) Reading String Registers
    ReadStringRegisters(robot);
  }

  private static void ReadNumericRegisters(FanucRobot robot)
  {
    NumregFile numregFile = robot.Ftp.KnownVariableFiles.GetNumregFile();

    for (int i = 0; i < numregFile.Numreg.Length; i++)
    {
      double value = numregFile.Numreg[i];
      Console.WriteLine($"📊 Numeric R[{i}] = {value}");
    }
  }

  private static void ReadPositionRegisters(FanucRobot robot)
  {
    PosregFile posregFile = robot.Ftp.KnownVariableFiles.GetPosregFile();

    // posregFile.Posreg is a 3D array: dimension [1] = group, [2] = register index
    for (int group = 0; group < posregFile.Posreg.GetLength(1); group++)
    {
      Console.WriteLine($"\n🤖 Reading position registers for Group {group}:");

      for (int i = 0; i < posregFile.Posreg.GetLength(2); i++)
      {
        PositionRegister value = posregFile.Posreg[group, i];
        Console.WriteLine($" - PR[{i}] :");
        Console.WriteLine($"    X = {value.CartesianPosition.X}");
        Console.WriteLine($"    Y = {value.CartesianPosition.Y}");
        Console.WriteLine($"    Z = {value.CartesianPosition.Z}");
        Console.WriteLine($"    W = {value.CartesianPosition.W}");
        Console.WriteLine($"    P = {value.CartesianPosition.P}");
        Console.WriteLine($"    R = {value.CartesianPosition.R}");
        Console.WriteLine("    Configuration :");
        Console.WriteLine($"       ArmFrontBack = {value.CartesianPosition.Configuration.ArmFrontBack}");
        Console.WriteLine($"       ArmLeftRight = {value.CartesianPosition.Configuration.ArmLeftRight}");
        Console.WriteLine($"       ArmUpDown = {value.CartesianPosition.Configuration.ArmUpDown}");
        Console.WriteLine($"       WristFlip = {value.CartesianPosition.Configuration.WristFlip}");
      }
    }
  }

  private static void ReadStringRegisters(FanucRobot robot)
  {
    StrregFile strregFile = robot.Ftp.KnownVariableFiles.GetStrregFile();

    for (int i = 0; i < strregFile.Strreg.Length; i++)
    {
      string value = strregFile.Strreg[i];
      Console.WriteLine($"💬 String SR[{i}] = '{value}'");
    }
  }
}
```

## Installed features (options)

Detect available options on the controller to check protocol availability.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common.Files.Diagnosis;

public class FtpDiagnosticsFeatures
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        Features features = robot.Ftp.GetSummaryDiagnostic().Features;

        // Check specific capabilities
        bool hasSnpx = features.HasSnpx;
        bool hasTelnet = features.HasTelnet;
        bool hasStreamMotion = features.HasStreamMotion; // J519 option

        // List all installed features
        foreach (var feature in features.FeaturesList)
            Console.WriteLine($"{feature.Name} ({feature.OrderNo})");
    }
}
```

## Asynchronous reading

Each reading method has an asynchronous version with an optional `CancellationToken`: `GetSafetyStatusAsync`, `GetCurrentPositionAsync`, `GetIOStateAsync`, `GetAllErrorsListAsync`, `GetProgramStatesAsync`, `GetVariablesFromFileAsync`, `GetAllVariablesAsync`, and `KnownVariableFiles.Get...Async`. The same methods are available on the web server client, `robot.Cgtp.Http`. They are not available on .NET Framework 3.5 and 4.0.

```csharp
using UnderAutomation.Fanuc;

public class FtpDiagnosticsAsync
{
    static async Task Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        var safetyStatus = await robot.Ftp.GetSafetyStatusAsync();
        var currentPosition = await robot.Ftp.GetCurrentPositionAsync();
        var errors = await robot.Ftp.GetAllErrorsListAsync();

        // Variable files, one known file or all of them
        var posreg = await robot.Ftp.KnownVariableFiles.GetPosregFileAsync();
        var all = await robot.Ftp.GetAllVariablesAsync(p => Console.WriteLine($"{p:F0} %"));

        Console.WriteLine($"Emergency Stop: {safetyStatus.ExternalEStop}");
        robot.Disconnect();
    }
}
```

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common.Files.Diagnosis;

public class FtpDiagnostics
{
  static void Main()
  {
    FanucRobot robot = new FanucRobot();
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Ftp.Enable = true;
    parameters.Ftp.FtpUser = "";
    parameters.Ftp.FtpPassword = "";
    robot.Connect(parameters);

    // Read safety status
    SafetyStatus safetyStatus = robot.Ftp.GetSafetyStatus();
    Console.WriteLine($"Emergency Stop: {safetyStatus.ExternalEStop}");
    Console.WriteLine($"Teach Pendant Enabled: {safetyStatus.TPEnable}");

    // Read current position (joints, world, user frames)
    CurrentPosition currentPosition = robot.Ftp.GetCurrentPosition();

    // Read I/O state
    IOState ioState = robot.Ftp.GetIOState();

    // Read all errors
    var errors = robot.Ftp.GetAllErrorsList();

    // Read all variables from all files
    var allVariables = robot.Ftp.GetAllVariables();
    foreach (var file in allVariables)
      foreach (var variable in file.Variables)
        Console.WriteLine($"{variable.Name} = {variable.Value}");

    // Access well-known system variables
    int rmtMaster = robot.Ftp.KnownVariableFiles.GetSystemFile().RmtMaster;

    // Get installed features
    Features features = robot.Ftp.GetSummaryDiagnostic().Features;
    bool hasSnpx = features.HasSnpx;
  }
}
```

## API reference

**SummaryDiagnosis** ([reference](../api/UnderAutomation.Fanuc.Common.Files.Diagnosis.md#summarydiagnosis))

- `SummaryDiagnosis()`
- `CurrentPosition CurrentPosition { get; }`: Current position of each robots and groups handled by this controller
- `Features Features { get; }`: Controller features status
- `IOState IOs { get; }`: Controller IO status
- `string Name { get; }`: File name : summary.dg
- `ProgramStates ProgramStates { get; }`: Controller program states
- `SafetyStatus Safety { get; }`: Controller safety information

**Features** ([reference](../api/UnderAutomation.Fanuc.Common.Files.Diagnosis.md#features))

- `Features()`
- `Feature[] FeaturesList { get; }`: List of features
- `bool HasAsciiUpload { get; }`: Indicates if the robot has the ASCII upload feature enabled : R507 ("ASCII Upload" on older controllers) or R796 ("ASCII Program Loader" on most recent controllers).
- `bool HasSnpx { get; }`: Indicates if the robot has the SNPX feature enabled (R553 or R651).
- `bool HasStreamMotion { get; }`: Indicates if the robot has the Stream Motion feature enabled (J519).
- `bool HasTelnet { get; }`: Indicates if the robot has the TELNET feature enabled (TELN).
