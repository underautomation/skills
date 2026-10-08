# Variables and I/O

Read and write the B, I, D, R and S variables, read the I/O signals and write the network inputs of a Yaskawa controller through the Ethernet Server.

Web page: https://underautomation.com/yaskawa/documentation/eserver-variables-io

This page shows how to read and write the variables and the I/O of a Yaskawa Motoman controller through the Ethernet Server: B, I, D, R and S variables, I/O groups and network inputs. It covers the YRC1000 and YRC1000micro controllers.

## Variables

```csharp
using UnderAutomation.Yaskawa;

public class EServerVariables
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Read 4 variables from index 0: B000 to B003, I000 to I003...
        byte[] b = robot.EServer.ReadByte(0, 4);
        short[] i = robot.EServer.ReadInteger(0, 4);
        int[] d = robot.EServer.ReadDoubleInteger(0, 4);
        float[] r = robot.EServer.ReadReal(0, 4);
        string[] s = robot.EServer.Read16BytesChar(0, 4);

        // Write from index 10: B010 = 1, B011 = 2
        robot.EServer.WriteByte(10, new byte[] { 1, 2 });
        robot.EServer.WriteInteger(10, new short[] { -100 });
        robot.EServer.WriteDoubleInteger(10, new[] { 123456 });
        robot.EServer.WriteReal(10, new[] { 1.5f });
        robot.EServer.Write16BytesChar(10, new[] { "PART-42" });

        robot.Disconnect();
    }
}
```

| Variable | Read                    | Write                         | .NET type  | Range of a value                |
| -------- | ----------------------- | ----------------------------- | ---------- | ------------------------------- |
| `B`      | `ReadByte`              | `WriteByte`                   | `byte`     | 0 to 255                        |
| `I`      | `ReadInteger`           | `WriteInteger`                | `short`    | -32768 to 32767                 |
| `D`      | `ReadDoubleInteger`     | `WriteDoubleInteger`          | `int`      | -2147483648 to 2147483647       |
| `R`      | `ReadReal`              | `WriteReal`                   | `float`    | 32 bit floating point           |
| `S`      | `Read16BytesChar`       | `Write16BytesChar`            | `string`   | 16 characters                   |

Reads take `(firstIndex, count)` and return one value per variable. Writes take `(firstIndex, values)` and write the variables from `firstIndex`. The number of variables depends on the settings of the controller. An index that does not exist throws a `HostControlException`.

The position variables (P, BP, EX) are not available through the Ethernet Server: read them with the [High Speed Ethernet Server](hses-variables.md).

## Inputs and outputs

### Read the signals

`ReadIO(startAddress, count)` reads `count` bytes of signals. Each byte holds 8 signals. `startAddress` is the number of the first signal, as shown on the pendant: `10010` for `#10010`. Use a number that ends with 0, so that each byte is one group of 8 signals.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerIo
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // 2 bytes from the signal #10010: #10010 to #10017, then #10020 to #10027
        HostControlIOData outputs = robot.EServer.ReadIO(10010, 2);
        Console.WriteLine($"#10010: {outputs.GetBit(0)}, #10011: {outputs.GetBit(1)}");
        Console.WriteLine($"#10020 to #10027: {outputs.Data[1]}");

        // Network inputs #27010 to #27017: bits 0 and 2 on (value 5)
        robot.EServer.WriteIO(27010, new byte[] { 5 });

        robot.Disconnect();
    }
}
```

`Data[0]` holds `#10010` to `#10017`: bit 0 is `#10010`, bit 7 is `#10017`. `GetBit(n)` reads bit `n` of the result, from 0 for the first signal of the first byte.

| Signals            | Example number |
| ------------------ | -------------- |
| General inputs     | `#00010`       |
| General outputs    | `#10010`       |
| External inputs    | `#20010`       |
| Network inputs     | `#27010`       |
| Network outputs    | `#37010`       |
| Specific outputs   | `#50010`       |
| Auxiliary relays   | `#70010`       |

The numbers are the same as with the High Speed Ethernet Server: the full table is in [Inputs and outputs](hses-io.md#signals_groups_and_bits). The signals that exist depend on the I/O boards of the controller.

### Write the network inputs

`WriteIO(startAddress, values)` writes bytes of signals. By default, the controller accepts only the network inputs (`#27010` to `#29567`). They are the signals to use to send an order or a state to a job. A write to another signal throws a `HostControlException`.

## Reference

**Methods of HostControlClientBase** ([reference](../api/UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolclientbase-roboteserver))

- `string[] Read16BytesChar(int firstIndex, int count)`: Reads 16-byte string (S) variables starting at the specified index.
- `byte[] ReadByte(int firstIndex, int count)`: Reads byte (B) variables starting at the specified index.
- `int[] ReadDoubleInteger(int firstIndex, int count)`: Reads double integer (D) variables starting at the specified index.
- `HostControlIOData ReadIO(int startAddress, int count)`: Reads I/O signals from the robot controller. Each byte holds 8 signals.
- `short[] ReadInteger(int firstIndex, int count)`: Reads integer (I) variables starting at the specified index.
- `float[] ReadReal(int firstIndex, int count)`: Reads real (R) variables starting at the specified index.
- `void Write16BytesChar(int firstIndex, string[] data)`: Writes 16-byte string (S) variables starting at the specified index.
- `void WriteByte(int firstIndex, byte[] data)`: Writes byte (B) variables starting at the specified index.
- `void WriteDoubleInteger(int firstIndex, int[] data)`: Writes double integer (D) variables starting at the specified index.
- `HostControlResponse WriteIO(int startAddress, byte[] data)`: Writes I/O signals to the robot controller. Each byte holds 8 signals. By default, the controller accepts only the network input signals (#27010 to #29567).
- `void WriteInteger(int firstIndex, short[] data)`: Writes integer (I) variables starting at the specified index.
- `void WriteReal(int firstIndex, float[] data)`: Writes real (R) variables starting at the specified index.

**HostControlIOData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontroliodata))

- `int Count { get; }`: Gets or sets the number of I/O bytes read.
- `byte[] Data { get; }`: Gets or sets the I/O data bytes.
- `bool GetBit(int bitOffset)`: Gets the bit value at the specified offset from the start address.
- `int StartAddress { get; }`: Gets or sets the starting I/O contact number.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## What to read next

- [Read and write variables](how-to-read-write-variables.md): which protocol and which variable type to choose.
- [Read and write I/O](how-to-read-write-io.md): switch a network input and wait for an output.
