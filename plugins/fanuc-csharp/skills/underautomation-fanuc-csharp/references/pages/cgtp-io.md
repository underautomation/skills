# Inputs & Outputs

Read, write, simulate, and unsimulate digital, analog, group, and robot I/O ports via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-io

CGTP enables reading, writing, simulating, and unsimulating I/O ports on your Fanuc robot. Requires firmware **V8.30+**.

## Supported I/O types

| `CgtpIoPortType` | Description |
|-------------------|-------------|
| `DI` / `DO` | Digital Input / Output |
| `AI` / `AO` | Analog Input / Output |
| `RI` / `RO` | Robot Input / Output |
| `GI` / `GO` | Group Input / Output |
| `Flag` | Flags (F[]) |

## Read & Write I/O

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpIoReadWrite
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read I/O
        int di1 = robot.Cgtp.ReadIo(CgtpIoPortType.DI, 1);
        int ao5 = robot.Cgtp.ReadIo(CgtpIoPortType.AO, 5);
        int flag10 = robot.Cgtp.ReadIo(CgtpIoPortType.Flag, 10);

        // Write I/O
        robot.Cgtp.WriteIo(CgtpIoPortType.DO, 1, 1);
        robot.Cgtp.WriteIo(CgtpIoPortType.AO, 1, 500);
        robot.Cgtp.WriteIo(CgtpIoPortType.GO, 1, 255);
    }
}
```


## Simulate and unsimulate

Simulation forces an I/O to a specific value, ignoring the physical signal:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpIoSimulate
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Simulate DI[5]
        robot.Cgtp.SimulateIo(CgtpIoPortType.DI, 5);

        // Check if DI[5] is simulated
        bool isSimulated = robot.Cgtp.GetIoSimulationStatus(CgtpIoPortType.DI, 5);

        // Unsimulate DI[5]
        robot.Cgtp.UnsimulateIo(CgtpIoPortType.DI, 5);
    }
}
```

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpIo
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Cgtp.Enable = true;

    robot.Connect(parameters);

    // Read digital input
    int di1 = robot.Cgtp.ReadIo(CgtpIoPortType.DI, 1);

    // Write digital output
    robot.Cgtp.WriteIo(CgtpIoPortType.DO, 1, 1);

    // Read analog input
    int ai1 = robot.Cgtp.ReadIo(CgtpIoPortType.AI, 1);

    // Write analog output
    robot.Cgtp.WriteIo(CgtpIoPortType.AO, 1, 500);

    // Read group input
    int gi1 = robot.Cgtp.ReadIo(CgtpIoPortType.GI, 1);

    // Write group output
    robot.Cgtp.WriteIo(CgtpIoPortType.GO, 1, 255);

    // Read/write robot I/O
    int ri1 = robot.Cgtp.ReadIo(CgtpIoPortType.RI, 1);
    robot.Cgtp.WriteIo(CgtpIoPortType.RO, 1, 1);

    // Read/write flag
    int flag = robot.Cgtp.ReadIo(CgtpIoPortType.Flag, 10);
    robot.Cgtp.WriteIo(CgtpIoPortType.Flag, 10, 1);

    // Simulate an I/O
    robot.Cgtp.SimulateIo(CgtpIoPortType.DI, 5);

    // Check simulation status
    bool isSimulated = robot.Cgtp.GetIoSimulationStatus(CgtpIoPortType.DI, 5);

    // Unsimulate
    robot.Cgtp.UnsimulateIo(CgtpIoPortType.DI, 5);
  }
}
```

## API reference

**CgtpIoPortType** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpioporttype))

- AI: Analog input.
- AO: Analog output.
- DI: Digital input.
- DO: Digital output.
- Flag: Flag.
- GI: Group input.
- GO: Group output.
- RI: Robot input.
- RO: Robot output.
