# Inputs and outputs

List the physical I/O of a Staubli controller, read several I/O in one request and write outputs, without a VAL 3 program.

Web page: https://underautomation.com/staubli/documentation/soap-io

This page shows how to list, read and write the physical inputs and outputs of a Staubli CS8 or CS9 controller with the SDK: digital, analog and the other I/O of the boards of the controller. No VAL 3 program is needed.

## List the I/O

`GetAllPhysicalIos()` returns every physical I/O of the controller, with its name, its type and its description.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class IoList
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Every physical I/O of the controller
        PhysicalIo[] ios = controller.Soap.GetAllPhysicalIos();

        foreach (PhysicalIo io in ios)
        {
            // TypeStr: din, dout, ain, serial...
            Console.WriteLine($"{io.Name} [{io.TypeStr}] {io.Description} lockable={io.Lockable}");
        }

        controller.Disconnect();
    }
}
```

The name identifies the I/O in the read and write methods. It contains the board and the I/O, separated by a backslash, for example `BasicIO-1\%I0`. The boards depend on the configuration of each controller: read the names with `GetAllPhysicalIos()`, do not guess them. In C#, write the name as a verbatim string (`@"BasicIO-1\%I0"`), in Python as a raw string (`r"BasicIO-1\%I0"`).

`TypeStr` gives the type, for example `din` or `dout` for a digital input or output, `ain` for an analog input, `serial` for a serial line.

## Read I/O

`ReadIos(names)` reads several I/O in one request. It returns one `PhysicalIoState` per name, in the same order.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class IoRead
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Names as returned by GetAllPhysicalIos
        string[] names = { @"BasicIO-1\%I0", @"BasicIO-1\%Q0" };

        // One state per name, in the same order
        PhysicalIoState[] states = controller.Soap.ReadIos(names);

        for (int i = 0; i < names.Length; i++)
        {
            PhysicalIoState state = states[i];

            // State tells if the name exists on this controller
            if (state.State != PhysicalIoEnumState.Defined)
            {
                Console.WriteLine($"{names[i]}: {state.State}");
                continue;
            }

            Console.WriteLine($"{names[i]} = {state.Value} locked={state.Locked} simulated={state.Simulated}");
        }

        controller.Disconnect();
    }
}
```

- `State` is `Defined` when the name exists, `Undefined` or `InvalidName` otherwise. Test it before you use the value.
- `Value` is a number: `0` or `1` for a digital I/O.
- `Locked` and `Simulated` tell if the I/O is locked or simulated on the controller.

## Write I/O

`WriteIos(names, values)` writes several outputs in one request. The two arrays have the same length.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class IoWrite
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        string[] names = { @"BasicIO-1\%Q0", @"BasicIO-1\%Q1" };

        // One value per name. Digital outputs: 1 is on, 0 is off
        double[] values = { 1, 0 };

        PhysicalIoWriteResponse[] responses = controller.Soap.WriteIos(names, values);

        for (int i = 0; i < names.Length; i++)
        {
            if (!responses[i].Found)
                Console.WriteLine($"{names[i]}: unknown name");
            else if (!responses[i].Success)
                Console.WriteLine($"{names[i]}: write refused");
        }

        controller.Disconnect();
    }
}
```

The answer has one `PhysicalIoWriteResponse` per name:

- `Found` is `false` when the name does not exist.
- `Success` is `false` when the controller refused the write, for example for an input.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/UnderAutomation.Staubli.Soap.Internal.md#soapclientbase-controllersoap))

- `PhysicalIo[] GetAllPhysicalIos()`: Get all the physical I/O values of the controller
- `PhysicalIoState[] ReadIos(string[] ios)`: Read the state of specified physical I/Os
- `PhysicalIoWriteResponse[] WriteIos(string[] ios, double[] values)`: Write values to specified physical I/Os

**PhysicalIo** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#physicalio))

- `PhysicalIo()`
- `string Description { get; set; }`: Description of the physical I/O.
- `bool Lockable { get; set; }`: Indicates whether the physical I/O is lockable.
- `string Name { get; set; }`: Name of the physical I/O.
- `string TypeStr { get; set; }`: Type of the physical I/O (e.g., din, dout, ain, serial, ...).

**PhysicalIoState** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#physicaliostate))

- `PhysicalIoState()`: Initializes a new instance of the Data.PhysicalIoState class.
- `PhysicalIoAttribute Attribute { get; set; }`: I/O type-specific attributes (analog or digital).
- `bool Locked { get; set; }`: Indicates whether the I/O is locked.
- `bool Simulated { get; set; }`: Indicates whether the I/O is in simulation mode.
- `PhysicalIoEnumState State { get; set; }`: Definition state of the I/O.
- `double Value { get; set; }`: Current numeric value of the I/O.

**PhysicalIoEnumState** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#physicalioenumstate))

- Defined: The I/O is defined and available.
- InvalidName: The I/O name is invalid.
- Undefined: The I/O is not defined.

**PhysicalIoWriteResponse** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#physicaliowriteresponse))

- `PhysicalIoWriteResponse()`: Initializes a new instance of the Data.PhysicalIoWriteResponse class.
- `bool Found { get; set; }`: Indicates whether the specified I/O was found.
- `bool Success { get; set; }`: Indicates whether the write operation succeeded.

**PhysicalIoAttribute** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#physicalioattribute))

- `PhysicalIoAttribute()`: Initializes a new instance of the Data.PhysicalIoAttribute class.
- `PhysicalAioAttribute AioAttribute { get; set; }`: Analog I/O specific attributes (null if digital).
- `PhysicalDioAttribute DioAttribute { get; set; }`: Digital I/O specific attributes (null if analog).
