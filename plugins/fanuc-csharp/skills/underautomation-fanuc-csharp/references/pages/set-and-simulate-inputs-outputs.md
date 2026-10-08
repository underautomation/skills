# Control inputs & outputs

Set, read, simulate, and unsimulate I/O ports on a Fanuc robot using SNPX, CGTP, or Telnet. Compare port types and methods.

Web page: https://underautomation.com/fanuc/documentation/set-and-simulate-inputs-outputs

Control digital and analog I/O signals on your Fanuc robot: read values, write outputs, simulate inputs, and manage I/O descriptions.

## SNPX (fastest : ~2 ms)

SNPX supports 13 digital and 5 numeric I/O types with single and range operations.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxIo
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Snpx.Enable = true;

    robot.Connect(parameters);

    // --- Digital signals (boolean) ---

    // Read a single digital input
    bool sdi10 = robot.Snpx.SDI.Read(10);

    // Write a single digital output
    robot.Snpx.RDO.Write(1, true);

    // Read a range of digital inputs (100 signals starting at index 1)
    bool[] sdiRange = robot.Snpx.SDI.Read(1, 100);

    // Write a range of digital outputs
    robot.Snpx.SDO.Write(1, new[] { true, false, true });

    // Other digital signal types: UI, UO, SI, SO, WI, WO, WSI, PMC_K, PMC_R
    bool ui5 = robot.Snpx.UI.Read(5);
    robot.Snpx.SO.Write(3, false);

    // --- Numeric I/O (ushort) ---

    // Read Group Input
    ushort gi1 = robot.Snpx.GI.Read(1);

    // Write Group Output
    robot.Snpx.GO.Write(1, 500);

    // Read Analog Input
    ushort ai1 = robot.Snpx.AI.Read(1);

    // Write Analog Output
    robot.Snpx.AO.Write(2, 32767);

    // Read a range of numeric I/O
    ushort[] giRange = robot.Snpx.GI.Read(1, 100);

    // Other numeric I/O types: PMC_D
    ushort pmcD = robot.Snpx.PMC_D.Read(1);
  }
}
```

See also: [SNPX Inputs & Outputs](snpx-io.md)

## CGTP Web Server

CGTP provides read/write/simulate for all standard I/O types:

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

See also: [CGTP Inputs & Outputs](cgtp-io.md)

## Telnet KCL

Telnet can set, simulate, and unsimulate I/O ports:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class SetAndSimulateInputsOutputsTelnet
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Set a port value
        robot.Telnet.SetPort(KCLPorts.DOUT, 1, 1);

        // Simulate a port
        robot.Telnet.Simulate(KCLPorts.DIN, 5, 1);

        // Unsimulate a port
        robot.Telnet.Unsimulate(KCLPorts.DIN, 5);
    }
}
```

See also: [Telnet Variables & I/O](telnet-variables-io.md)

## Protocol comparison

| Feature | SNPX | CGTP | Telnet |
|---------|------|------|--------|
| **Speed** | ~2 ms | ~50 ms | ~30 ms |
| **Digital I/O types** | 13 types | 5 types + Flag | SDI/SDO/RDI/RDO/UI/UO/SI/SO/WI/WO |
| **Numeric I/O types** | 5 types | AI/AO/GI/GO | GI/GO/AI/AO |
| **Range read/write** | Yes | No | No |
| **Simulate/Unsimulate** | No | Yes | Yes |
| **Batch read** | Yes | No | No |
