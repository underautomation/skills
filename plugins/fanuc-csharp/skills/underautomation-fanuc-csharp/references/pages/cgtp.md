# CGTP overview

CGTP is an HTTP-based protocol providing the richest feature set: program management, variables, registers, I/O, kinematics, batch operations, and file access.

Web page: https://underautomation.com/fanuc/documentation/cgtp

CGTP is the web server running on Fanuc robots (port 80/3080). It provides HTTP-based access to programs, variables, registers, I/O, positions, and files.

## Key features

- **Program management**: Create, delete, rename, run, pause, abort programs
- **Variables & registers**: Read/write any variable, numeric/position/string registers
- **I/O control**: Read, write, simulate, and unsimulate I/O ports
- **Position reading**: Read current Cartesian and joint positions
- **Online kinematics**: Forward and inverse kinematics on the controller
- **Batch operations**: Read/write groups of registers and variables in one request
- **Comments**: Read/write register, I/O, and user alarm descriptions
- **File access**: List and download controller files via HTTP
- **KCL commands**: Execute KCL commands over CGTP, in place of Telnet KCL

## Quick example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Cgtp;

public class Cgtp
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Cgtp.Enable = true;

    robot.Connect(parameters);

    // Read a variable
    CgtpVariableValue var = robot.Cgtp.ReadVariable("$RMT_MASTER");
    int rmtMaster = var.IntegerValue;

    // Write a variable
    robot.Cgtp.WriteVariable("$RMT_MASTER", 1);

    // Read a numeric register with comment
    NumericRegisterWithComment reg = robot.Cgtp.ReadNumericRegisterWithComment(1);

    // Read I/O
    int di1 = robot.Cgtp.ReadIo(CgtpIoPortType.DI, 1);

    // Write I/O
    robot.Cgtp.WriteIo(CgtpIoPortType.DO, 1, 1);

    // Read current Cartesian position
    CartesianPosition pos = robot.Cgtp.ReadCartesianPosition();

    // Run a program
    robot.Cgtp.RunProgram("MY_PROGRAM");
  }
}
```

## Robot options

CGTP does not require any additional options. The robot typically listens on port **80** or **3080**.

Most features require firmware **V8.30** or later. Some features (program management, position reading) require **V9.10+**.

## Firmware compatibility

| Feature | Min. firmware |
|---------|--------------|
| Variable read/write | V8.30 |
| I/O read/write/simulate | V8.30 |
| Program management | V9.10 |
| Position reading | V9.10 |
| Program execution (Run) | V9.30 |
| KCL commands with a result | V8.30 |
| KCL commands without result (Unsafe) | V9.30 |
| File listing | V9.40 |

## Connection

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpConnection
{
    static void Main()
    {
        // Via FanucRobot
        var robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Cgtp.Enable = true;           // enabled by default
        parameters.Cgtp.Port = 80;              // default port
        parameters.Cgtp.RequestTimeoutMs = 3000; // default timeout
        robot.Connect(parameters);

        // Or standalone
        var cgtp = new CgtpClient();
        cgtp.Connect("192.168.0.1");
    }
}
```

## Authentication

Some robots require authentication. Pass credentials during connection:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpAuth
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");

        // Via FanucRobot
        parameters.Cgtp.Login = "admin";
        parameters.Cgtp.Password = "password";
        robot.Connect(parameters);

        // Or standalone
        var cgtp = new CgtpClient();
        cgtp.Connect("192.168.0.1", login: "admin", password: "password");
    }
}
```

## KCL over CGTP

CGTP provides an embedded KCL client accessible via `robot.Cgtp.Kcl`. It executes the KCL commands of `robot.Telnet` without a Telnet connection, and replaces Telnet KCL for new developments:

```csharp
using UnderAutomation.Fanuc;

public class CgtpKcl
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        robot.Cgtp.Kcl.SetVariable("$RMT_MASTER", 1);

        TaskInformationResult taskInfo = robot.Cgtp.Kcl.GetTaskInformation("MY_PROGRAM");

        robot.Cgtp.Kcl.AddBreakpoint("MY_PROGRAM", line: 10);
    }
}
```

Some commands (`Run`, `Pause`, `Abort`...) return no result through CGTP. See [KCL commands](cgtp-kcl.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Next steps

- [Program management](cgtp-programs.md) : Create, run, pause, abort programs
- [Registers & variables](cgtp-registers-variables.md) : Read/write registers and variables
- [Inputs & Outputs](cgtp-io.md) : Read, write, simulate I/O
- [Position & kinematics](cgtp-position-kinematics.md) : Read position, FK/IK
- [Alarms, comments & files](cgtp-alarms-files.md) : Comments, user alarms, file listing
- [KCL commands](cgtp-kcl.md) : KCL commands in place of Telnet KCL

## API reference

**CgtpClient** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpclient))

- `CgtpClient()`: Creates a new instance of the CGTP Web Server client.
- `void Connect(string ip, int port = 3080, int requestTimeoutMs = 3000, string login = null, string password = null)`: Connect to the CGTP Web Server on the controller.
- Inherited from [CgtpClientBase](../api/UnderAutomation.Fanuc.Cgtp.Internal.md#cgtpclientbase-robotcgtp): `Disconnect`, `AbortTask`, `SelectProgram`, `DeleteProgram`, `GetProgramComment`, `SetProgramComment`, `GetProgramOwner`, `SetProgramOwner`, `GetProgramStackSize`, `SetProgramStackSize`, `GetProgramIgnorePause`, `SetProgramIgnorePause`, `GetProgramWriteProtect`, `SetProgramWriteProtect`, `GetProgramSubType`, `SetProgramSubType`, `CreateProgram`, `RenameProgram`, `ListPrograms`, `ListTpPrograms`, `DeleteSourceLines`, `InsertSourceLine`, `ReplaceSourceLine`, `SetProgramPositionToCurrentCartesianPosition`, `SetProgramPosition`, `RunProgram`, `ChangeActiveProgram`, `PauseAllPrograms`, `ReadVariableAsString`, `ReadVariable`, `WriteVariable`, `SetComment`, `WriteNumericRegisterAsDouble`, `WriteNumericRegisterAsInteger`, `WriteStringRegister`, `SetUserAlarmSeverity`, `ReadNumericRegistersWithComment`, `ReadStringRegistersWithComment`, `ReadUserAlarms`, `GetIoComments`, `GetComments`, `ReadNumericRegisterWithComment`, `ReadPositionRegisterWithComment`, `ReadBatchVariables`, `WritePositionRegisterAsCartesian`, `WritePositionRegisterAsJoint`, `WriteBatchVariables`, `ReadIo`, `WriteIo`, `GetIoSimulationStatus`, `SimulateIo`, `UnsimulateIo`, `ReadCartesianPosition`, `ReadJointPosition`, `InvertKinematics`, `ForwardKinematics`, `ListFiles`, `GetFileAsString`, `Kcl`, `Http`, `Language`, `Enabled`

**CgtpClientBase** ([reference](../api/UnderAutomation.Fanuc.Cgtp.Internal.md#cgtpclientbase-robotcgtp))

- `void AbortTask(string progName = null)`: Abort the task specified by progName. Set to null to abort all user tasks. From firmware 9.10
- `void ChangeActiveProgram(string progName)`: Change the active TP program to progName. From firmware 9.10
- `void CreateProgram(string progName, string owner = null, string comment = null, int defaultGroup = 0, CgtpProgramSubType subType = CgtpProgramSubType.None)`: Create a new TP program on the controller. From firmware 9.10
- `void DeleteProgram(string progName)`: Delete the program progName from the controller. From firmware 9.10
- `void DeleteSourceLines(string progName, int lineNum, int count = 1)`: Delete count lines starting at lineNum in program progName. From firmware 9.10
- `void Disconnect()`: Disconnect from the CGTP Web Server. After calling this method, the client must be reconnected before it can be used again.
- `bool Enabled { get; }`: Indicates whether the client is currently connected to the CGTP Web Server.
- `CartesianPosition ForwardKinematics(int group, JointsPosition jointPosition, int userTool = -1, int userFrame = -1)`: Compute the forward kinematics on the controller: convert joint angles to a Cartesian position.
- `string[] GetComments(CgtpCommentType type)`: Read all comments for the specified element type. For I/O types (RI, RO, DI, DO, GI, GO, AI, AO), returns the input or output comments accordingly.
- `string GetFileAsString(string pathName)`: Download the content of a file from the controller as a string. From firmware 9.10
- `IOComments GetIoComments(CgtpCommentIoType type)`: Read all I/O comments for the specified I/O type.
- `bool GetIoSimulationStatus(CgtpIoPortType portType, int index)`: Check whether I/O port at index of type portType is simulated. From firmware 8.30
- `string GetProgramComment(string progName)`: Get the comment of program progName. From firmware 9.10
- `bool GetProgramIgnorePause(string progName)`: Get whether program progName ignores pause requests. From firmware 9.10
- `string GetProgramOwner(string progName)`: Get the owner of program progName. From firmware 9.10
- `int GetProgramStackSize(string progName)`: Get the stack size of program progName. From firmware 9.10
- `CgtpProgramSubType GetProgramSubType(string progName)`: Get the sub-type of program progName. From firmware 9.10
- `bool GetProgramWriteProtect(string progName)`: Get whether program progName is write-protected. From firmware 9.10
- `CgtpHttpClient Http { get; }`: Provides methods to download and decode files from the controller via HTTP.
- `void InsertSourceLine(string progName, string lineContent, int lineNum)`: Insert a source line before lineNum in program progName. From firmware 9.10
- `JointsPosition InvertKinematics(int group, CartesianPosition cartesianPosition, int userTool = -1, int userFrame = -1)`: Compute the inverse kinematics on the controller: convert a Cartesian position to joint angles.
- `CgtpKclClient Kcl { get; }`: KCL client for executing KCL commands over CGTP. Use it instead of the Telnet KCL client, which is a legacy protocol. Some commands are sent in Unsafe mode: the controller returns no status, so the result cannot tell if the command was executed. To start a program, prefer RunProgram().
- `Languages Language { get; set; }`: Controller language (default is English)
- `string[] ListFiles(string pathName = "MD:")`: List files at the specified path on the controller. From firmware 9.40
- `string[] ListPrograms(CgtpProgramType type, CgtpProgramSubType subType)`: List all TP or Karel programs on the controller
- `string[] ListTpPrograms()`: List all TP programs on the controller, regardless of their sub-type.
- `void PauseAllPrograms()`: Pause program execution on the controller. From firmware 9.10
- `CgtpBatchReadResult ReadBatchVariables(CgtpBatchVariables variables)`: Read multiple variables from the controller in a single batch operation. Each variable in variables will be updated with the value read from the controller.
- `CartesianPosition ReadCartesianPosition(int groupNum = 1)`: Read the current Cartesian position of motion group groupNum. From firmware 9.10
- `int ReadIo(CgtpIoPortType portType, int index)`: Read the value of I/O port at index of type portType. From firmware 8.30
- `JointsPosition ReadJointPosition(int groupNum = 1)`: Read the current joint angles of motion group groupNum. From firmware 9.10
- `NumericRegisterWithComment ReadNumericRegisterWithComment(int index)`: Read the numeric register (R[]) at index. From firmware 9.10
- `NumericRegisterWithComment[] ReadNumericRegistersWithComment()`: Read all numeric registers (R[]) with their comments and values.
- `PositionRegisterWithComment ReadPositionRegisterWithComment(int index, int groupNum = 1)`: Read the position register (PR[]) at index for motion group groupNum. From firmware 9.10
- `StringRegisterWithComment[] ReadStringRegistersWithComment()`: Read all string registers (SR[]) with their comments and values.
- `UserAlarmDefinition[] ReadUserAlarms()`: Read all user alarm definitions with their comments and severity.
- `CgtpVariableValue ReadVariable(string varName, string progName = null)`: Read the typed value of variable varName in program progName. From firmware 9.10
- `string ReadVariableAsString(string varName, string progName = null)`: Read the value of variable varName in program progName. From firmware 9.10
- `void RenameProgram(string sourceName, string newName)`: Rename program sourceName to newName. From firmware 9.10
- `void ReplaceSourceLine(string progName, string lineContent, int lineNum)`: Replace the source line at lineNum in program progName. From firmware 9.10
- `void RunProgram(string progName, int lineNum = 1)`: Run the specified program starting at lineNum. From firmware 9.30
- `void SelectProgram(string progName, int lineNum = 1)`: Open the TP program progName and move cursor to lineNum. From firmware 9.10
- `void SetComment(CgtpCommentType type, int index, string comment)`: Set the comment of a register or I/O port identified by type and index.
- `void SetProgramComment(string progName, string comment)`: Set the comment of program progName. From firmware 9.10
- `void SetProgramIgnorePause(string progName, bool ignorePause)`: Set whether program progName ignores pause requests. From firmware 9.10
- `void SetProgramOwner(string progName, string owner)`: Set the owner of program progName. From firmware 9.10
- `void SetProgramPosition(string progName, int positionIndex, Position position)`: Set position at index positionIndex in program progName to the given position. Supports both joint and Cartesian representations. Only the first motion group is supported via CGTP. From firmware 9.10
- `CartesianPosition SetProgramPositionToCurrentCartesianPosition(string progName, int positionIndex, int groupNumber = 1)`: Set position at index positionIndex to the current Cartesian position in program progName and return the updated position.
- `void SetProgramStackSize(string progName, int stackSize)`: Set the stack size of program progName. From firmware 9.10
- `void SetProgramSubType(string progName, CgtpProgramSubType subType)`: Set the sub-type of program progName. From firmware 9.10
- `void SetProgramWriteProtect(string progName, bool writeProtect)`: Set whether program progName is write-protected. From firmware 9.10
- `void SetUserAlarmSeverity(int index, int severity)`: Set the severity of a user alarm.
- `void SimulateIo(CgtpIoPortType portType, int index)`: Set I/O port at index of type portType to simulated. From firmware 8.30
- `void UnsimulateIo(CgtpIoPortType portType, int index)`: Remove simulation from I/O port at index of type portType. From firmware 8.30
- `CgtpBatchWriteResult WriteBatchVariables(CgtpBatchVariables variables)`: Write multiple variables to the controller in a single batch operation.
- `void WriteIo(CgtpIoPortType portType, int index, int value)`: Set the value of I/O port at index of type portType. From firmware 8.30
- `void WriteNumericRegisterAsDouble(int index, double value)`: Write a real (double) value to numeric register R[index].
- `void WriteNumericRegisterAsInteger(int index, int value)`: Write an integer value to numeric register R[index].
- `void WritePositionRegisterAsCartesian(int index, CartesianPosition value, int groupNum = 1)`: Write a cartesian position value to a position register (PR[])
- `void WritePositionRegisterAsJoint(int index, JointsPosition value, int groupNum = 1)`: Write a joint position value to a position register (PR[])
- `void WriteStringRegister(int index, string value)`: Write a string value to string register SR[index].
- `void WriteVariable(string varName, double value, string progName = null)`: Write a real (double) value to variable varName in program progName. From firmware 8.30
- `void WriteVariable(string varName, int value, string progName = null)`: Write an integer value to variable varName in program progName. From firmware 8.30
- `void WriteVariable(string varName, string value, string progName = null)`: Write value to variable varName in program progName. From firmware 8.30
