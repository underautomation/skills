# Inputs & Outputs

Read and write digital signals (SDI, SDO, RDI, RDO, UI, UO, SI, SO, WI, WO) and numeric I/O (GI, GO, AI, AO) via SNPX.

Web page: https://underautomation.com/fanuc/documentation/snpx-io

SNPX supports 13 digital signal types and 5 numeric I/O types, all with single and range read/write operations.

## Digital signals

Digital signals are boolean values. The following types are available:

| Type | Description |
|------|-------------|
| `SDI` / `SDO` | Standard Digital Input / Output |
| `RDI` / `RDO` | Robot Digital Input / Output |
| `UI` / `UO` | User Input / Output |
| `SI` / `SO` | System Input / Output |
| `WI` / `WO` | Weld Input / Output |
| `WSI` | Wire Stick Input |
| `PMC_K` | PMC Keep Relays |
| `PMC_R` | PMC Internal Relays |

### Read and write digital signals

```csharp
using UnderAutomation.Fanuc;

public class SnpxIoDigital
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Read SDI[10]
        bool sdi10 = robot.Snpx.SDI.Read(10);

        // Write RDO[1] = ON
        robot.Snpx.RDO.Write(1, true);

        // Read UI[5]
        bool ui5 = robot.Snpx.UI.Read(5);

        // Read 100 SDI signals starting at index 1
        bool[] values = robot.Snpx.SDI.Read(1, 100);

        // Write 3 SDO signals starting at index 1
        robot.Snpx.SDO.Write(1, new[] { true, false, true });
    }
}
```

## Numeric I/O

Numeric I/O signals are 16-bit unsigned integers (ushort):

| Type | Description |
|------|-------------|
| `GI` / `GO` | Group Input / Output |
| `AI` / `AO` | Analog Input / Output |
| `PMC_D` | PMC Data |

### Read and write numeric I/O

```csharp
using UnderAutomation.Fanuc;

public class SnpxIoNumeric
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Read GI[1]
        ushort gi1 = robot.Snpx.GI.Read(1);

        // Write GO[1] = 500
        robot.Snpx.GO.Write(1, 500);

        // Read AI[1]
        ushort ai1 = robot.Snpx.AI.Read(1);

        // Write AO[2] = 32767
        robot.Snpx.AO.Write(2, 32767);

        // Read a range of GI values
        ushort[] giValues = robot.Snpx.GI.Read(1, 100);
    }
}
```

## Complete example

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

## API reference

**DigitalSignals** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#digitalsignals-robotsnpxsdi))

- `bool Read(int index)`: Reads the digital signal at the specified index.
- `bool[] Read(int firstIndex, ushort count)`: Reads a range of digital signals.
- `SegmentName SegmentName { get; }`: Gets the name of the family of signals of this signal group.
- `void Write(int index, bool value)`: Writes a value to the digital signal at the specified index.
- `void Write(int firstIndex, bool[] values)`: Writes values to consecutive digital signals.

**NumericIO** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#numericio-robotsnpxgi))

- `ushort Read(int index)`: Reads the numeric I/O value at the specified index.
- `ushort[] Read(int firstIndex, ushort count)`: Reads a range of numeric I/O values.
- `SegmentName SegmentName { get; }`: Gets the name of the family of signals of this I/O group.
- `void Write(int index, ushort value)`: Writes a value to the numeric I/O at the specified index.
- `void Write(int firstIndex, ushort[] values)`: Writes values to consecutive numeric I/O.
