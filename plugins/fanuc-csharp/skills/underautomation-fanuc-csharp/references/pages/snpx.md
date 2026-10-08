# SNPX overview

SNPX (also known as RobotIF or SRTP) is a high-speed protocol for reading and writing registers, variables, I/O signals, alarms, and positions in less than 2 ms.

Web page: https://underautomation.com/fanuc/documentation/snpx

SNPX (also known as RobotIF, Robot Interface, or SRTP) is a high-performance binary protocol for reading and writing data on a Fanuc robot controller in less than 2 ms.

## Key features

- **Registers**: Read/write numeric (R[]), position (PR[]), string (SR[]), and flag (F[]) registers
- **I/O signals**: Read/write 13 digital signal types and 5 numeric I/O types
- **System variables**: Read/write integer, real, position, and string variables
- **Current position**: Read world and user frame positions for any group
- **Alarms**: Read active alarm, alarm history, clear alarms
- **Task monitoring**: Read running program status, line number, and caller
- **Batch reading**: Read groups of data in a single command for maximum throughput
- **Comments**: Read/write descriptions for registers and I/O

## Quick example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

  public class Snpx
  {
    static void Main()
    {
      // Create a new Fanuc robot instance
      FanucRobot robot = new FanucRobot();

      // Set connection parameters
      ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
      parameters.Snpx.Enable = true;

      // Connect to the robot
      robot.Connect(parameters);

      // Read a register
      Position posReg1 = robot.Snpx.PositionRegisters.Read(1);
      float numReg5 = robot.Snpx.NumericRegisters.Read(5);
      string strReg10 = robot.Snpx.StringRegisters.Read(10);

      // Write a register
      posReg1.CartesianPosition.X = 100;
      robot.Snpx.PositionRegisters.Write(1, posReg1);
      robot.Snpx.NumericRegisters.Write(2, 123.45f);
      robot.Snpx.StringRegisters.Write(3, "Hello, world!");

      // Read a variable
      int rmtMaster = robot.Snpx.IntegerSystemVariables.Read("$RMT_MASTER");
      string lastAlm = robot.Snpx.StringSystemVariables.Read("$ALM_IF.$LAST_ALM");
      Position cellFloor = robot.Snpx.PositionSystemVariables.Read("$CELL_FLOOR");

      // Write a system variable
      robot.Snpx.IntegerSystemVariables.Write("$RMT_MASTER", 1);
      robot.Snpx.StringSystemVariables.Write("$ALM_IF.$LAST_ALM", "No alarms");
      robot.Snpx.PositionSystemVariables.Write("$CELL_FLOOR", cellFloor);

      // Write a Karel program variable
      robot.Snpx.IntegerSystemVariables.Write("$[KarelProgram]KarelVariable", 1);

      // Read and Write I/O (SDI,SDO,RDI,RDO,UI,UO,SI,SO,WI,WO,WSI,PMC_K,PMC_R)
      robot.Snpx.RDO.Write(1, true);
      ushort ai5 = robot.Snpx.AI.Read(5);

      // Read and Write analogs (AI,AO,GI,GO,PMC_D)
      robot.Snpx.AO.Write(2, 5);
      ushort ao3 = robot.Snpx.AO.Read(3);

      // Clear alarms
      robot.Snpx.ClearAlarms();
    }

  }
```

## Differences with official Fanuc Robot Interface

Fanuc provides its own Robot Interface client (FRRJIF.DLL). Here are the main differences:

|  | **UnderAutomation SDK** | **Fanuc FRRJIF.DLL** |
| --- | --- | --- |
| **Publisher** | UnderAutomation | Fanuc Ltd. |
| **Technology** | 100% managed .NET assembly | Native ActiveX / COM |
| **Dependencies** | No dependencies, single DLL | Requires PCDK installation |
| **Typical read time** | 2 ms | 30 ms |
| **Cross platform** | Windows, Linux, macOS | Windows only |
| **Languages** | C#, Python, LabVIEW | COM-compatible languages |

## Robot options

To enable SNPX on your robot, you need one of the following:

- **FANUC America (R650 FRA)**: Option R553 "HMI Device SNPX" is required
- **FANUC Ltd. (R651 FRL)**: No additional option needed

TCP port **60008** (Robot IF Server) must be accessible on your controller.

## Performance

SNPX is the fastest protocol in the SDK. Regardless of the amount of data transported in a single command, execution time remains constant at approximately **2 ms**.

For example, you can read 80 position registers in a single batch in the same time as reading a single variable.

When used with ROBOGUIDE, execution times under 1 ms can be achieved.

## Connection

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Snpx;

public class SnpxConnection
{
    static void Main()
    {
        // Via FanucRobot
        var robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Or standalone
        var snpx = new SnpxClient();
        snpx.Connect("192.168.0.1");
    }
}
```

## Check if SNPX is available

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common.Files.Diagnosis;

public class SnpxFeatures
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
    bool isSnpxAvailable = features.HasSnpx;
  }
}
```

## Next steps

- [Registers](snpx-registers.md) : R[], PR[], SR[], F[]
- [Inputs & Outputs](snpx-io.md) : Digital and numeric signals
- [System variables](snpx-variables.md) : Integer, real, position, string variables
- [Current position](snpx-position.md) : World and user frame positions
- [Alarms & task status](snpx-alarms-tasks.md) : Alarm management and task monitoring
- [Batch reading](snpx-batch.md) : High-performance batch operations

## Demonstration

The SNPX page of the demo application reads and writes registers, variables and signals without writing code.

![SNPX](https://underautomation.com/fanuc/snpx.gif)

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**SnpxClient** ([reference](../api/UnderAutomation.Fanuc.Snpx.md#snpxclient))

- `SnpxClient()`: Initializes a new instance of the Snpx.SnpxClient class.
- `void Connect(string ip, int port = 60008)`: Connects to a Fanuc robot using the SNPX protocol.
- Inherited from [SnpxClientBase](../api/UnderAutomation.Fanuc.Snpx.Internal.md#snpxclientbase-robotsnpx): `PollAndGetUpdatedConnectedState`, `Disconnect`, `ClearAlarms`, `SetVariable`, `ClearAssignments`, `GetAssignments`, `Ip`, `NumericRegisters`, `NumericRegistersInt32`, `NumericRegistersInt16`, `PositionRegisters`, `StringRegisters`, `IntegerSystemVariables`, `RealSystemVariables`, `PositionSystemVariables`, `StringSystemVariables`, `DigitalSignals`, `SDI`, `SDO`, `RDI`, `RDO`, `UI`, `UO`, `SI`, `SO`, `WI`, `WO`, `WSI`, `PMC_K`, `PMC_R`, `NumericIOs`, `GI`, `GO`, `AI`, `AO`, `PMC_D`, `Flags`, `CurrentPosition`, `CurrentTaskStatus`, `ActiveAlarm`, `AlarmHistory`, `Comments`, `SimulationStatus`, `Language`, `Connected`

**SnpxClientBase** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#snpxclientbase-robotsnpx))

- `NumericIO AI { get; }`: Analog Inputs
- `NumericIO AO { get; }`: Analog Outputs
- `AlarmAccess ActiveAlarm { get; }`: Current active alarms
- `AlarmAccess AlarmHistory { get; }`: Alarm history
- `void ClearAlarms()`: Clear all active alarms
- `void ClearAssignments()`: Clear all assignments
- `Comments Comments { get; }`: Comments of registers, I/O signals and other data
- `bool Connected { get; }`: Indicates if the SNPX underlying TCP client is connected to the robot
- `CurrentPosition CurrentPosition { get; }`: Current position in world or user frame
- `CurrentTaskStatus CurrentTaskStatus { get; }`: Current program tasks status. Index starts from 1.
- `DigitalSignals[] DigitalSignals { get; }`: List of all digital signal accessors (SDI, SDO, RDI, RDO, ...)
- `void Disconnect()`: Disconnect from the robot
- `Flags Flags { get; }`: Flags
- `NumericIO GI { get; }`: Group Inputs
- `NumericIO GO { get; }`: Group Outputs
- `Assignment[] GetAssignments()`: Gets all current assignments.
- `IntegerSystemVariables IntegerSystemVariables { get; }`: Integer variables
- `string Ip { get; }`: IP address of the connected robot.
- `Languages Language { get; set; }`: Controller language (default is English)
- `NumericIO[] NumericIOs { get; }`: List of all Numeric IOs accessors (GI, GO, AI, AO, ...)
- `NumericRegisters NumericRegisters { get; }`: Number registers R[] as floating point values
- `NumericRegistersInt16 NumericRegistersInt16 { get; }`: Number registers R[] as 16-bit integer values
- `NumericRegistersInt32 NumericRegistersInt32 { get; }`: Number registers R[] as 32-bit integer values
- `NumericIO PMC_D { get; }`: Programmable Machine Controller Data
- `DigitalSignals PMC_K { get; }`: Programmable Machine Controller Constants
- `DigitalSignals PMC_R { get; }`: Programmable Machine Controller Relays
- `bool PollAndGetUpdatedConnectedState()`: Checks the actual connection status via an active socket polling
- `PositionRegisters PositionRegisters { get; }`: Position registers
- `PositionSystemVariables PositionSystemVariables { get; }`: Position variables
- `DigitalSignals RDI { get; }`: Remote Digital Inputs
- `DigitalSignals RDO { get; }`: Remote Digital Outputs
- `RealSystemVariables RealSystemVariables { get; }`: Real variables
- `DigitalSignals SDI { get; }`: Safety Digital Inputs
- `DigitalSignals SDO { get; }`: Safety Digital Outputs
- `DigitalSignals SI { get; }`: System Inputs
- `DigitalSignals SO { get; }`: System Outputs
- `void SetVariable(string name, bool value)`: Set boolean variable without assignments.
- `void SetVariable(string name, double value)`: Set double variable without assignments.
- `void SetVariable(string name, int value)`: Set integer variable without assignments.
- `void SetVariable(string name, string value)`: Set string variable without assignments.
- `SimulationStatus SimulationStatus { get; }`: I/O simulation status
- `StringRegisters StringRegisters { get; }`: String registers
- `StringSystemVariables StringSystemVariables { get; }`: String variables
- `DigitalSignals UI { get; }`: User Inputs
- `DigitalSignals UO { get; }`: User Outputs
- `DigitalSignals WI { get; }`: Weld Inputs
- `DigitalSignals WO { get; }`: Weld Outputs
- `DigitalSignals WSI { get; }`: Weld System Inputs
