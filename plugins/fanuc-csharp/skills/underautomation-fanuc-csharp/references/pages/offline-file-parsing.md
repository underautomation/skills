# Offline file parsing

Parse and decode Fanuc variable files (.va), error lists (.ls), I/O state, safety status, and current position files without a robot connection.

Web page: https://underautomation.com/fanuc/documentation/offline-file-parsing

The SDK includes offline file parsers for reading and editing Fanuc controller files without a network connection. Download files from the robot via FTP, then parse them locally.

The offline parsers are available in .NET. The Python package does not wrap them yet: in Python, read these files from the controller with the FTP client (`robot.ftp.known_variable_files`, `robot.ftp.get_safety_status()`...), see [Diagnostics & variables](ftp-diagnostics.md).

## Variable files (.va)

Parse any variable file (.va) into a hierarchical list of typed variables:

```csharp
using UnderAutomation.Fanuc.Common.Files.Variables;
using UnderAutomation.Fanuc.Common.Files;
using UnderAutomation.Fanuc.Common;

public class OfflineFileParsingVariable
{
    static void Main()
    {
        // Parse a variable file
        GenericVariableFile vaFile = FanucFileReaders.VariableReader.ReadFile("C:/backup/numreg.va", Languages.English);

        // Browse variables
        foreach (var variable in vaFile.Variables)
        {
            Console.WriteLine($"{variable.Name} = {variable.Value} [{variable.Type}]");
        }

        // Re-generate the .va file
        vaFile.GenerateVa("C:/backup/numreg_modified.va");
    }
}
```

This works with all .va files: `numreg.va`, `posreg.va`, `strreg.va`, `sysvars.va`, `sysmotn.va`, etc.

## Error log (errall.ls)

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Ftp;

public class OfflineFileParsingReaders
{
    static void Main()
    {
        // Error log
        var errors = FanucFileReaders.ErrorListReader.ReadFile("C:/backup/errall.ls", Languages.English);
        foreach (var error in errors.Items)
        {
            Console.WriteLine($"{error.OccurringTime} [{error.ErrorCode}] {error.Message}");
        }

        // I/O state
        var ioState = FanucFileReaders.IOStateReader.ReadFile("C:/backup/iostate.dg", Languages.English);

        // Safety status
        var safety = FanucFileReaders.SafetyStatusReader.ReadFile("C:/backup/safety.dg", Languages.English);

        // Current position
        var currentPos = FanucFileReaders.CurrentPositionReader.ReadFile("C:/backup/curpos.dg", Languages.English);
    }
}
```


## Workflow: FTP download + offline parse

A common pattern is to download files via FTP and parse them locally:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Ftp;

public class OfflineFileParsingWorkflow
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Download a file from the robot
        robot.Ftp.DirectFileHandling.DownloadFileFromController("numreg.va", "md:/numreg.va");

        // Parse offline
        var vaFile = FanucFileReaders.VariableReader.ReadFile("numreg.va", Languages.English);

        // Or use the built-in helpers
        var numRegs = robot.Ftp.KnownVariableFiles.GetNumregFile();
        var posRegs = robot.Ftp.KnownVariableFiles.GetPosregFile();
    }
}
```

## Complete example

```csharp
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Common.Files;
using UnderAutomation.Fanuc.Common.Files.Variables;

public class OfflineFileParsing
{
  static void Main()
  {
    // Parse a variable file and extract a hierarchical list of variables
    GenericVariableFile vaFile = FanucFileReaders.VariableReader.ReadFile("C:/path/to/variable.va", Languages.English);
    foreach (var variable in vaFile.Variables)
      Console.WriteLine($"{variable.Name} = {variable.Value} [{variable.Type}]");

    // Edit and regenerate the variable file
    vaFile.GenerateVa("C:/path/to/variable_modified.va\"");

    // Parse several types of files 
    FanucFileReaders.ErrorListReader.ReadFile("C:/path/to/errall.ls", Languages.English);
    FanucFileReaders.IOStateReader.ReadFile("C:/path/to/iostate.dg", Languages.English);
    FanucFileReaders.SafetyStatusReader.ReadFile("C:/path/to/safety.dg", Languages.English);
    FanucFileReaders.CurrentPositionReader.ReadFile("C:/path/to/curpos.dg", Languages.English);
  }

}
```

## API reference

**GenericVariableFile** ([reference](../api/UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile))

- `GenericVariableFile()`
- `void GenerateVa(Stream stream)`: Generates a .va file and writes it to the specified stream
- `void GenerateVa(string pathToVa)`: Generates a .va file and writes it to the specified path
- `string GeneratedVa()`: Generates the content of a .va variable file as a string.
- `GenericVariable GetField(string name)`: Gets a variable by name (case-insensitive)
- `string Name { get; }`: File name
- `IGenericVariableType Parent { get; set; }`: Parent container
- `GenericVariable[] Variables { get; }`: Variables declared in this file

**FanucFileReaders** ([reference](../api/UnderAutomation.Fanuc.Common.Files.md#fanucfilereaders))

- `static readonly DiagnosisReader<CurrentPosition, CurrentPositionReader> CurrentPositionReader`: Decode current position file curpos.dg
- `static readonly ErrorListReader ErrorListReader`: Helper to read error files like errall.ls
- `static readonly DiagnosisReader<IOState, IOStateParser> IOStateReader`: Decode IO Status file iostate.dg
- `static readonly DiagnosisReader<ProgramStates, ProgramStatesParser> ProgramStates`: Decode task and program states prgstate.dg
- `static IFanucContent ReadFile(Stream fileStream, string fileName, Languages language)`: Read any file by path on disc, recognize it by name and decode it
- `static IFanucContent ReadFile(string fileName, Languages language)`: Read any file by path on disc, recognize it by name and decode it
- `static IFileReader<IFanucContent>[] Readers { get; }`: Get the collection of all parsers
- `static readonly DiagnosisReader<SafetyStatus, SafetyStatusParser> SafetyStatusReader`: Decode IO Status file iostate.dg
- `static readonly SummaryDiagnosisReader SummaryDiagnosticReader`: Helper to read summary diagnosis file summary.dg
- `static readonly VariableReader VariableReader`: Helper to read variable files *.va
