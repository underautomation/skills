# Read and write variables

Exchange data with a Yaskawa job from C# or Python: integer, real, byte and string variables, which type to choose, and the frequent errors.

Web page: https://underautomation.com/yaskawa/documentation/how-to-read-write-variables

This article shows how to exchange data between a PC and a job of a Yaskawa Motoman controller, in C# or Python, with the variables of the controller. It gives a complete program that reads a counter and writes offsets, a recipe number and a reference.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- The job uses the variables that the PC reads and writes. Agree on the numbers of these variables with the author of the job.

## Which variable to choose

| Data                                  | Variable | Methods                                         |
| ------------------------------------- | -------- | ----------------------------------------------- |
| A flag, a small number (0 to 255)     | `B`      | `ReadByte`, `WriteByte`                         |
| A counter, an index (-32768 to 32767) | `I`      | `ReadInteger`, `WriteInteger`                   |
| A large integer                       | `D`      | `ReadDoubleInteger`, `WriteDoubleInteger`       |
| A measure, an offset in mm            | `R`      | `ReadReal`, `WriteReal`                         |
| A text, a reference                   | `S`      | `Read16BytesChar`, `Write16BytesChar`           |
| A position                            | `P`      | `ReadPositionVariable`, `WritePositionVariable` |

Each method reads or writes several variables in a row, in one request.

## Example

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class HowToReadWriteVariables
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Integer I000: a part counter written by the job
        short count = robot.HighSpeedEServer.ReadInteger(0, 1).Value[0];
        Console.WriteLine($"Parts: {count}");

        // Real R000 and R001: offsets used by the job, in mm
        robot.HighSpeedEServer.WriteReal(0, new[] { 2.5f, -1.0f });

        // Byte B000 and B001: a recipe number and a flag
        robot.HighSpeedEServer.WriteByte(0, new byte[] { 7, 1 });

        // String S000: the reference of the part
        robot.HighSpeedEServer.Write16BytesChar(0, new[] { "REF-2026-118" });

        // Check what the controller stored
        byte[] bytes = robot.HighSpeedEServer.ReadByte(0, 2).Value;
        float[] reals = robot.HighSpeedEServer.ReadReal(0, 2).Value;
        Console.WriteLine($"B000={bytes[0]} B001={bytes[1]} R000={reals[0]} R001={reals[1]}");

        robot.Disconnect();
    }
}
```

The program:

1. reads `I000`, a counter of the job;
2. writes two offsets in `R000` and `R001`;
3. writes a recipe number and a flag in `B000` and `B001`;
4. writes a reference in `S000`;
5. reads the variables back to check them.

## A handshake with the job

A job and a PC read and write the same variables at the same time. Use one variable as a flag: the PC writes the data, then sets the flag. The job waits for the flag, reads the data, then clears the flag. The PC waits for the cleared flag before it writes again.

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) reads and writes the B, I, D, R and S variables with the same method names, over TCP. It returns the values directly, as arrays. The P variables are not available through the Ethernet Server.

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

## Troubleshooting

- **`InvalidDataAnswerException` on a variable number:** the number is out of the range of the controller. The ranges depend on the controller and on its settings.
- **A text is cut:** a 16 byte string keeps 16 characters. Use the 32 byte strings when the controller has them.

## What to read next

- [Variables and registers](hses-variables.md): all the variable types, including positions.
- [Run a job](how-to-run-program.md).
