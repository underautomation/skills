# Read and write I/O

Find the I/O names, wait for an input and switch an output of a Staubli CS8 or CS9 controller from C# or Python.

Web page: https://underautomation.com/staubli/documentation/how-to-read-write-io

This article shows how to read and write the inputs and outputs of a Staubli CS8 or CS9 controller from a PC, in C# or Python. It gives a complete program that finds the I/O names, waits for an input and switches an output on, without any VAL 3 program on the controller.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- To write an output, the user of the connection has the right to write it.

## Three calls

| Step                  | Method                    | Returns                                      |
| --------------------- | ------------------------- | -------------------------------------------- |
| Find the names        | `GetAllPhysicalIos()`     | Name, type and description of every I/O      |
| Read one or more I/O  | `ReadIos(names)`          | One state per name: value, locked, simulated |
| Write one or more I/O | `WriteIos(names, values)` | One answer per name: found, success          |

`ReadIos` and `WriteIos` take arrays: read or write several I/O in one request instead of one request per I/O.

## Example

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class HowToReadWriteIo
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // 1. Find the exact names of the I/O
        foreach (PhysicalIo io in controller.Soap.GetAllPhysicalIos())
            Console.WriteLine($"{io.Name} [{io.TypeStr}] {io.Description}");

        string input = @"BasicIO-1\%I0";
        string output = @"BasicIO-1\%Q0";

        // 2. Wait for the input, at most 10 seconds
        DateTime timeout = DateTime.Now.AddSeconds(10);
        while (controller.Soap.ReadIos(new[] { input })[0].Value == 0)
        {
            if (DateTime.Now > timeout) throw new TimeoutException($"{input} stayed off");
            Thread.Sleep(50);
        }

        // 3. Switch the output on, and check the answer of the controller
        PhysicalIoWriteResponse response = controller.Soap.WriteIos(new[] { output }, new[] { 1.0 })[0];
        if (!response.Found || !response.Success)
            Console.WriteLine($"Write of {output} failed: found={response.Found}");

        controller.Disconnect();
    }
}
```

The program:

1. prints the name of every I/O, to copy the exact names into the code;
2. reads the input every 50 ms until it is on, with a timeout of 10 s;
3. writes the output, and checks that the controller found it and accepted the value.

## I/O names

A name contains the board and the I/O, separated by a backslash: `BasicIO-1\%I0`. The boards depend on the configuration of the controller, so the names of your cell can differ from the ones of this example. Always take them from `GetAllPhysicalIos()`.

Write the backslash as it is: with a verbatim string in C# (`@"BasicIO-1\%I0"`) and a raw string in Python (`r"BasicIO-1\%I0"`).

## Troubleshooting

- **`State` is `Undefined` or `InvalidName`:** the name does not exist on this controller. Compare it with the output of `GetAllPhysicalIos()`, including the case and the backslash.
- **`Found` is `true` but `Success` is `false`:** the controller refused the write. Check that the I/O is an output, and the rights of the user.
- **The value changes back:** a VAL 3 program writes the same output. Stop it, or agree on which side owns each output.

## What to read next

- [Inputs and outputs](soap-io.md): the reference of the I/O methods.
- [Monitor the state of the robot](how-to-monitor-state.md).
