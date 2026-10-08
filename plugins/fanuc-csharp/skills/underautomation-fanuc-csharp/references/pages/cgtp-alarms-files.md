# Alarms, comments & files

Manage user alarms, read/write register and I/O comments, list and download files from the controller via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-alarms-files

CGTP provides access to register and I/O comments, user alarms, and file listing/download from the controller.

## Register & I/O comments

Read and write descriptive comments for registers:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;
using UnderAutomation.Fanuc.Common;

public class CgtpAlarmsFilesComments
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read register comments
        string[] regComments = robot.Cgtp.GetComments(CgtpCommentType.NumericRegister);
        string[] posComments = robot.Cgtp.GetComments(CgtpCommentType.PositionRegister);
        string[] strComments = robot.Cgtp.GetComments(CgtpCommentType.StringRegister);

        // Write a register comment
        robot.Cgtp.SetComment(CgtpCommentType.NumericRegister, 1, "Speed setpoint");
        robot.Cgtp.SetComment(CgtpCommentType.PositionRegister, 1, "Home position");

        // Read I/O comments
        IOComments robotIo = robot.Cgtp.GetIoComments(CgtpCommentIoType.RobotIO);
        IOComments digitalIo = robot.Cgtp.GetIoComments(CgtpCommentIoType.DigitalIO);
        IOComments analogIo = robot.Cgtp.GetIoComments(CgtpCommentIoType.AnalogIO);
    }
}
```

## User alarms

Read and configure user alarm definitions:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class CgtpAlarmsFilesAlarms
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read all user alarms
        UserAlarmDefinition[] alarms = robot.Cgtp.ReadUserAlarms();
        foreach (var alarm in alarms)
        {
            Console.WriteLine($"Alarm: {alarm.Comment} (Severity: {alarm.Severity})");
        }

        // Set user alarm severity
        robot.Cgtp.SetUserAlarmSeverity(1, 2);
    }
}
```

## File listing

List files on the controller using CGTP HTTP:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpAlarmsFilesFiles
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // List files in a directory
        string[] files = robot.Cgtp.ListFiles("MD:");

        // List TP programs
        CgtpAsciiFileItem[] tpPrograms = robot.Cgtp.Http.ListTpPrograms();
        foreach (var prog in tpPrograms)
        {
            Console.WriteLine($"{prog.File} - {prog.Comment}");
        }

        // List variable files
        CgtpAsciiFileItem[] varFiles = robot.Cgtp.Http.ListVariableFiles();

        // Download as string
        string content = robot.Cgtp.Http.DownloadAsString("numreg.va");

        // Download as bytes
        byte[] data = robot.Cgtp.Http.DownloadAsBytes("posreg.va");
    }
}
```


## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpAlarmsFiles
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Cgtp.Enable = true;

    robot.Connect(parameters);

    // --- Register comments ---
    string[] regComments = robot.Cgtp.GetComments(CgtpCommentType.NumericRegister);
    string[] posComments = robot.Cgtp.GetComments(CgtpCommentType.PositionRegister);

    // Write a comment
    robot.Cgtp.SetComment(CgtpCommentType.NumericRegister, 1, "Speed setpoint");

    // --- I/O comments ---
    IOComments digitalIo = robot.Cgtp.GetIoComments(CgtpCommentIoType.DigitalIO);
    IOComments robotIo = robot.Cgtp.GetIoComments(CgtpCommentIoType.RobotIO);

    // --- User alarms ---
    UserAlarmDefinition[] alarms = robot.Cgtp.ReadUserAlarms();
    robot.Cgtp.SetUserAlarmSeverity(1, 2);

    // --- File listing ---
    string[] files = robot.Cgtp.ListFiles("MD:");

    CgtpAsciiFileItem[] tpPrograms = robot.Cgtp.Http.ListTpPrograms();
    CgtpAsciiFileItem[] varFiles = robot.Cgtp.Http.ListVariableFiles();
    CgtpFileItem[] diagFiles = robot.Cgtp.Http.ListDiagnosticFiles();

    // --- File download ---
    string content = robot.Cgtp.Http.DownloadAsString("numreg.va");
    byte[] data = robot.Cgtp.Http.DownloadAsBytes("posreg.va");
  }
}
```

## API reference

**CgtpCommentType** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpcommenttype))

- AI: Analog input.
- AO: Analog output.
- DI: Digital input.
- DO: Digital output.
- Flag: Flag (F[]).
- GI: Group input.
- GO: Group output.
- NumericRegister: Numeric register (R[]).
- PositionRegister: Position register (PR[]).
- RI: Robot input.
- RO: Robot output.
- StringRegister: String register (SR[]).
- UserAlarm: User alarm.

**CgtpCommentIoType** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpcommentiotype))

- AnalogIO: Analog I/O (AI/AO).
- DigitalIO: Digital I/O (DI/DO).
- GroupIO: Group I/O (GI/GO).
- RobotIO: Robot I/O (RI/RO).

**CgtpFileItem** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpfileitem))

- `CgtpFileItem()`
- `string Comment { get; }`: Comment associated with the file, if any.
- `string File { get; }`: File name on the controller.

**CgtpAsciiFileItem** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpasciifileitem))

- `CgtpAsciiFileItem()`
- `string AsciiFile { get; }`: ASCII format file name, or null if not available.
- Inherited from [CgtpFileItem](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpfileitem): `File`, `Comment`

**CgtpHttpClient** ([reference](../api/UnderAutomation.Fanuc.Cgtp.Internal.md#cgtphttpclient-robotcgtphttp))

- `string BasePath { get; set; }`: Base path used to build the download URL. Default is "MD".
- `byte[] DownloadAsBytes(string fileName)`: Download a file from the controller and return its raw bytes.
- `Stream DownloadAsStream(string fileName)`: Download a file from the controller and return a readable stream. Otherwise the raw binary response is returned.
- `string DownloadAsString(string fileName)`: Download a file from the controller and return its content as a string.
- `string[] EnumerateVariableFileNames()`: Get the list of all variable file names available on the controller
- `string IP { get; }`: IP address of the controller
- `CgtpFileItem[] ListDiagnosticFiles()`: List diagnostic and error files available on the controller.
- `CgtpFileItem[] ListOtherFiles()`: List other files available on the controller.
- `CgtpAsciiFileItem[] ListTpPrograms()`: List TP program files available on the controller.
- `CgtpAsciiFileItem[] ListVariableFiles()`: List variable files available on the controller.
- Inherited from [FileClientBase](../api/UnderAutomation.Fanuc.Common.Files.md#fileclientbase-robotftp): `GetSummaryDiagnostic`, `GetAllErrorsList`, `GetCurrentPosition`, `GetIOState`, `GetSafetyStatus`, `GetProgramStates`, `GetVariablesFromFile`, `GetAllVariables`, `KnownVariableFiles`

**UserAlarmDefinition** ([reference](../api/UnderAutomation.Fanuc.Common.md#useralarmdefinition))

- `UserAlarmDefinition()`
- `string Comment { get; set; }`: Comment associated with this alarm.
- `int Severity { get; set; }`: Severity level of the alarm.
