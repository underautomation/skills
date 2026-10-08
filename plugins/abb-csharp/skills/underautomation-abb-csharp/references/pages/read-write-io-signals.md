# Read & write I/O signals

Read and write digital, analog and group I/O signals of an ABB controller, pulse a signal and simulate one during tests.

Web page: https://underautomation.com/abb/documentation/read-write-io-signals

Reading an I/O signal of an ABB controller is `robot.Rws.Io.GetSignal(network, device, signal)`, and writing one is `robot.Rws.Io.SetSignalValue(network, device, signal, value)`. Digital, analog and group signals all go through the same two methods, only the value changes. I/O needs no mastership, it needs a user account with the write grant.

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

## How a signal is identified

A signal has three parts: the network it belongs to, the device it is connected to, and its name. `Local` is the internal network of the controller, and the signals of the robot itself are usually on it.

`IoSignalItem.Path` gives the three parts joined, for example `Local/Board10/DO_Gripper`. If you only know the name of a signal, find its network and its device with `GetSignals()` or with a search.

## Read a signal

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class IoReadSignal
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // A signal is identified by its network, its device and its name
        IoSignalItem signal = robot.Rws.Io.GetSignal("Local", "Board10", "DO_Gripper");

        Console.WriteLine(signal.Path);          // Local/Board10/DO_Gripper
        Console.WriteLine(signal.Type);          // DigitalOutput
        Console.WriteLine(signal.LogicalValue);  // 1
        Console.WriteLine(signal.LogicalState);  // NotSimulated
        Console.WriteLine(signal.PhysicalValue); // 1
        Console.WriteLine(signal.PhysicalState); // Valid

        // Every signal of the controller, in one call
        IoSignalItem[] signals = robot.Rws.Io.GetSignals();

        foreach (IoSignalItem item in signals)
        {
            Console.WriteLine($"{item.Path} = {item.LogicalValue} ({item.Type})");
        }

        robot.Disconnect();
    }
}
```

A signal has two values. `LogicalValue` is what the program and the network see. `PhysicalValue` is what the device really carries. They differ when the signal is simulated, or inverted in the configuration. `LogicalState` says whether the signal is simulated, `PhysicalState` whether the value can be trusted.

`GetSignals()` returns every signal of the controller in one request. It is the fast way to build a table, but it carries only the name, the type, the category, the logical value and the logical state. Call `GetSignal` on one signal to get everything.

## Digital, analog and group

| `IoSignalType`                  | Value                                     | Written with                 |
| ------------------------------- | ----------------------------------------- | ---------------------------- |
| `DigitalInput`, `DigitalOutput` | 0 or 1                                    | `SetSignalValue(..., 1)`     |
| `AnalogInput`, `AnalogOutput`   | any value inside the configured range     | `SetSignalValue(..., 12.5f)` |
| `GroupInput`, `GroupOutput`     | the integer made of the bits of the group | `SetSignalValue(..., 5)`     |

`LogicalValue` is a `float?`, and `SetSignalValue` takes a `float`. A group of 4 bits written with the value 5 sets the bits 1 and 3. `IoSignalConfiguration.SignalBits` gives the width of a group.

## Write a signal

Only an output can be written, unless the input is simulated. Writing a read only signal fails with an `RwsException`.

```csharp
using UnderAutomation.ABB;

public class IoWriteSignal
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // A digital signal takes 0 or 1
        robot.Rws.Io.SetSignalValue("Local", "Board10", "DO_Gripper", 1);

        // An analog or a group signal takes any value inside its range
        robot.Rws.Io.SetSignalValue("Local", "Board10", "AO_Speed", 12.5f);

        // The last argument writes the change in the event log of the controller
        robot.Rws.Io.SetSignalValue("Local", "Board10", "DO_Gripper", 0, true);

        // The controller applies the value 500 ms later, and answers immediately
        robot.Rws.Io.SetSignalValueDelayed("Local", "Board10", "DO_Gripper", 1, 500);

        robot.Disconnect();
    }
}
```

## Pulse, toggle and invert

A pulse is done by the controller, which is more precise than two writes separated by a `Thread.Sleep` in your application.

```csharp
using UnderAutomation.ABB;

public class IoPulseSignal
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Three pulses to 1, 200 ms active and 200 ms passive
        robot.Rws.Io.PulseSignal("Local", "Board10", "DO_Gripper", 1, 3, 200, 200);

        // Same, with the pulse lengths configured on the controller
        robot.Rws.Io.PulseSignal("Local", "Board10", "DO_Gripper", 1, 1);

        // Toggle pulses the signal by starting from the opposite of its current value
        robot.Rws.Io.ToggleSignal("Local", "Board10", "DO_Gripper", 1, 2, 200, 200);

        // Invert writes the opposite of the current value, once
        robot.Rws.Io.InvertSignal("Local", "Board10", "DO_Gripper", 1);

        robot.Disconnect();
    }
}
```

## Wait for a signal

There is no subscription in this SDK, a value is read by asking for it. To wait for an input, poll it with a period and a timeout. 200 ms is a reasonable period, a shorter one loads the controller for nothing.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class HowToIoWaitSignal
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Ask the robot to work, then wait for its answer
        robot.Rws.Io.SetSignalValue("Local", "Board10", "DO_Start", 1);

        if (!WaitValue(robot, "Local", "Board10", "DI_Done", 1, 10000))
            throw new Exception("The robot did not answer in 10 seconds");

        robot.Rws.Io.SetSignalValue("Local", "Board10", "DO_Start", 0);

        robot.Disconnect();
    }

    // Polls one signal until it reaches the expected value, or the timeout expires.
    // 200 ms is a reasonable period : a shorter one loads the controller for nothing.
    static bool WaitValue(AbbController robot, string network, string device, string signal,
                          float expected, int timeoutMs)
    {
        DateTime limit = DateTime.UtcNow.AddMilliseconds(timeoutMs);

        while (DateTime.UtcNow < limit)
        {
            IoSignalItem item = robot.Rws.Io.GetSignal(network, device, signal);

            if (item.LogicalValue == expected)
                return true;

            Thread.Sleep(200);
        }

        return false;
    }
}
```

When the reaction has to be faster than that, do the waiting in RAPID with a `WaitDI`, and use the SDK to give the program the order to start.

## Simulate a signal during a test

A simulated signal keeps the value written by the client and stops following its device. This is how an input is forced from a test bench, on a real controller as well as on a virtual one.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class IoSimulateSignal
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Simulate an input: it keeps the value written by the client
        robot.Rws.Io.SetSignalState("Local", "Board10", "DI_PartPresent", true);
        robot.Rws.Io.SetSignalValue("Local", "Board10", "DI_PartPresent", 1);

        IoSignalItem signal = robot.Rws.Io.GetSignal("Local", "Board10", "DI_PartPresent");
        Console.WriteLine(signal.LogicalState); // Simulated

        // Give the signal back to its device
        robot.Rws.Io.SetSignalState("Local", "Board10", "DI_PartPresent", false);

        // Or stop simulating every simulated signal of the controller at once
        robot.Rws.Io.UnblockSignals();

        robot.Disconnect();
    }
}
```

Do not leave a signal simulated at the end of a test. `UnblockSignals()` stops the simulation of every simulated signal of the controller at once.

## Who is allowed to write a signal

A signal can be write protected depending on who writes it and in which operation mode. When a write is refused and the mastership is not the reason, read the configuration of the signal.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class IoSignalConfig
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        IoSignalConfiguration config = robot.Rws.Io.GetSignalConfiguration("Local", "Board10", "DO_Gripper");

        Console.WriteLine(config.SignalName);   // DO_Gripper
        Console.WriteLine(config.SignalBits);   // 1

        // Who is allowed to write the signal, and in which operation mode
        Console.WriteLine(config.Rapid);        // a RAPID program
        Console.WriteLine(config.LocalManual);  // the teach pendant, in manual mode
        Console.WriteLine(config.LocalAuto);    // the teach pendant, in auto mode
        Console.WriteLine(config.RemoteManual); // a remote client, in manual mode
        Console.WriteLine(config.RemoteAuto);   // a remote client, in auto mode

        robot.Disconnect();
    }
}
```

## Find the signals you need

`SearchSignals` filters on the name, the device, the network, the type and the category. A second criteria can be inverted to exclude what it matches, which is how the safety signals are left out of a list.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class IoSearchSignals
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Every digital output of one device
        IoSignalSearchCriteria criteria = new IoSignalSearchCriteria();
        criteria.DeviceName = "Board10";
        criteria.Type = IoSignalType.DigitalOutput;

        IoSignalItem[] outputs = robot.Rws.Io.SearchSignals(criteria);

        foreach (IoSignalItem signal in outputs)
        {
            Console.WriteLine($"{signal.Name} = {signal.LogicalValue}");
        }

        // The extended search also reports the physical value and the write access level
        IoSignalItem[] extended = robot.Rws.Io.SearchSignalsExtended(criteria, null, 0, 50);

        Console.WriteLine(extended[0].PhysicalValue);
        Console.WriteLine(extended[0].Quality);
        Console.WriteLine(extended[0].WriteAccessLevel);

        // A second inverted criteria excludes what it matches, here the safety signals
        IoSignalSearchCriteria exclude = new IoSignalSearchCriteria();
        exclude.Category = "safety";
        exclude.Invert = true;

        IoSignalItem[] withoutSafety = robot.Rws.Io.SearchSignals(criteria, exclude);

        robot.Disconnect();
    }
}
```

## Going further

- [I/O signals, devices & networks](rws-io.md), the complete reference
- [Start & stop a RAPID program](start-stop-rapid-program.md), to trigger a program that reacts to your signals
- [Read & write RAPID variables](read-write-rapid-variables.md), the other way of exchanging data with a program

**Methods of IoService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#ioservice-robotrwsio))

- `IoSignalItem GetSignal(string network, string device, string signal)`: Gets a single I/O signal, including its physical value and time stamps (synchronous)
  - async: `Task<IoSignalItem> GetSignalAsync(string network, string device, string signal, CancellationToken cancellationToken = default)`
- `IoSignalConfiguration GetSignalConfiguration(string network, string device, string signal)`: Gets the runtime configuration properties of an I/O signal (synchronous)
  - async: `Task<IoSignalConfiguration> GetSignalConfigurationAsync(string network, string device, string signal, CancellationToken cancellationToken = default)`
- `IoSignalItem[] GetSignals()`: Gets every I/O signal defined in the controller (synchronous) A controller usually exposes several hundreds of signals. Use Nullable%7bSystem.Int32%7d) to narrow the result down to a network, a device, a category or a signal type.
  - async: `Task<IoSignalItem[]> GetSignalsAsync(CancellationToken cancellationToken = default)`
- `void InvertSignal(string network, string device, string signal, float value, bool logToEventLog = false)`: Inverts the value of an I/O signal (synchronous) Only digital and group signals can be inverted.
  - async: `Task InvertSignalAsync(string network, string device, string signal, float value, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `void PulseSignal(string network, string device, string signal, float value, int pulses, int? activePulseLength = null, int? passivePulseLength = null, bool logToEventLog = false)`: Pulses the value of an I/O signal (synchronous) Only digital and group signals can be pulsed.
  - async: `Task PulseSignalAsync(string network, string device, string signal, float value, int pulses, int? activePulseLength = null, int? passivePulseLength = null, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `IoSignalItem[] SearchSignals(IoSignalSearchCriteria criteria = null, IoSignalSearchCriteria secondCriteria = null, int? start = null, int? limit = null)`: Searches the I/O signals matching the given criteria (synchronous) The returned signals carry their name, type, category, logical value and logical state. Use Nullable%7bSystem.Int32%7d) to also get their physical value, time stamps and write access level.
  - async: `Task<IoSignalItem[]> SearchSignalsAsync(IoSignalSearchCriteria criteria = null, IoSignalSearchCriteria secondCriteria = null, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `IoSignalItem[] SearchSignalsExtended(IoSignalSearchCriteria criteria = null, IoSignalSearchCriteria secondCriteria = null, int? start = null, int? limit = null)`: Searches the I/O signals matching the given criteria and returns their extended properties (synchronous) In addition to Nullable%7bSystem.Int32%7d), the returned signals carry their physical value, quality, time stamps and write access level.
  - async: `Task<IoSignalItem[]> SearchSignalsExtendedAsync(IoSignalSearchCriteria criteria = null, IoSignalSearchCriteria secondCriteria = null, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `void SetSignalState(string network, string device, string signal, bool simulated)`: Simulates or stops simulating an I/O signal (synchronous) A simulated signal keeps the logical value written by the client and no longer follows its physical value.
  - async: `Task SetSignalStateAsync(string network, string device, string signal, bool simulated, CancellationToken cancellationToken = default)`
- `void SetSignalValue(string network, string device, string signal, float value, bool logToEventLog = false)`: Writes the value of an I/O signal (synchronous)
  - async: `Task SetSignalValueAsync(string network, string device, string signal, float value, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `void SetSignalValueDelayed(string network, string device, string signal, float value, int delay, bool logToEventLog = false)`: Writes the value of an I/O signal in "queued delayed" mode (synchronous) The controller queues the write and applies it once the delay has elapsed.
  - async: `Task SetSignalValueDelayedAsync(string network, string device, string signal, float value, int delay, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `void ToggleSignal(string network, string device, string signal, float value, int pulses, int? activePulseLength = null, int? passivePulseLength = null, bool logToEventLog = false)`: Pulses an I/O signal by toggling its current value (synchronous) Only digital and group signals can be toggled.
  - async: `Task ToggleSignalAsync(string network, string device, string signal, float value, int pulses, int? activePulseLength = null, int? passivePulseLength = null, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `void UnblockSignals()`: Removes the simulation of every simulated I/O signal of the controller (synchronous)
  - async: `Task UnblockSignalsAsync(CancellationToken cancellationToken = default)`

**IoSignalItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iosignalitem))

- `IoSignalItem()`: Initializes a new instance of the Data.IoSignalItem class
- `string Category { get; set; }`: Category the signal belongs to, for example "safety"
- `string DeviceName { get; set; }`: Name of the device the signal is connected to, for example "DRV_1"
- `IoSignalLogicalState LogicalState { get; set; }`: Logical state of the signal (simulated or not)
- `long? LogicalTimeMicroseconds { get; set; }`: Microseconds part of the global time at which the logical value was updated, null when not reported
- `long? LogicalTimeSeconds { get; set; }`: Seconds part of the global time at which the logical value was updated, null when not reported
- `float? LogicalValue { get; set; }`: Logical value of the signal, null when the controller did not report it
- `string Name { get; set; }`: Name of the signal, for example "DRV1BRAKE"
- `string NetworkName { get; set; }`: Name of the network the signal belongs to, for example "Local"
- `string Path { get; set; }`: Full path of the signal, "{network}/{device}/{signal}" (for example "Local/DRV_1/DRV1BRAKE")
- `IoSignalPhysicalState PhysicalState { get; set; }`: Physical state of the signal. Only reported when reading a single signal with IoService.GetSignal().
- `long? PhysicalTimeMicroseconds { get; set; }`: Microseconds part of the global time at which the physical value was updated, null when not reported
- `long? PhysicalTimeSeconds { get; set; }`: Seconds part of the global time at which the physical value was updated, null when not reported
- `float? PhysicalValue { get; set; }`: Physical value of the signal, null when the controller did not report it. Only reported by IoService.GetSignal() and IoService.SearchSignalsExtended().
- `string Quality { get; set; }`: Quality of the signal, reported as a numeric code by IoService.GetSignal() and as a textual value (for example "good") by IoService.SearchSignalsExtended()
- `IoSignalType Type { get; set; }`: Type of the signal
- `string WriteAccessLevel { get; set; }`: Access level required to write the signal, for example "None". Only reported by IoService.SearchSignalsExtended().

**IoSignalType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iosignaltype))

- AnalogInput: Analog input
- AnalogOutput: Analog output
- DigitalInput: Digital input
- DigitalOutput: Digital output
- GroupInput: Group input
- GroupOutput: Group output
- Unknown: The signal type could not be determined

**IoSignalConfiguration** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iosignalconfiguration))

- `IoSignalConfiguration()`: Initializes a new instance of the Data.IoSignalConfiguration class
- `bool? LocalAuto { get; set; }`: Whether a local client can write the signal in auto mode
- `bool? LocalManual { get; set; }`: Whether a local client can write the signal in manual mode
- `bool? Rapid { get; set; }`: Whether a RAPID client can write the signal in both manual and auto mode
- `bool? RemoteAuto { get; set; }`: Whether a remote client can write the signal in auto mode
- `bool? RemoteManual { get; set; }`: Whether a remote client can write the signal in manual mode
- `bool? SetByDeviceTransfer { get; set; }`: Whether the bits of this signal are set by a device transfer operation. Not reported by every controller, null when absent from the response.
- `int? SignalBits { get; set; }`: Number of bits of the signal, null when not reported
- `string SignalName { get; set; }`: Name of the signal, for example "DRV1CHAIN2"

**IoSignalSearchCriteria** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iosignalsearchcriteria))

- `IoSignalSearchCriteria()`: Initializes a new instance of the Data.IoSignalSearchCriteria class
- `bool? Blocked { get; set; }`: Whether only the blocked (simulated) signals are searched
- `string Category { get; set; }`: Category of the searched signals, for example "safety"
- `string CategoryPrefix { get; set; }`: Category prefix of the searched signals
- `string DeviceName { get; set; }`: Name of the device the searched signals are connected to
- `bool? Invert { get; set; }`: Whether the criteria is inverted: the signals matching it are excluded from the result
- `string Name { get; set; }`: Name of the searched signals
- `string NetworkName { get; set; }`: Name of the network the searched signals belong to
- `IoSignalType? Type { get; set; }`: Type of the searched signals, null to search every type
