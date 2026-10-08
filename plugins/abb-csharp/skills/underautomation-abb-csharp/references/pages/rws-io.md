# I/O signals, devices & networks

Read and write digital, analog and group signals, pulse or invert a signal, and browse the I/O devices and networks of the controller.

Web page: https://underautomation.com/abb/documentation/rws-io

`robot.Rws.Io` reads and writes the I/O of the controller. The I/O system has three levels: a network carries devices, a device carries signals. A signal is identified by the three names together, for example `Local`, `Board10` and `DO_Gripper`.

A shorter introduction with a complete example is given in [Read & write I/O signals](read-write-io-signals.md).

## Signals

`GetSignal` reads one signal, `GetSignals` reads every signal of the controller in one call.

| `IoSignalType`                  | Values                                                     |
| ------------------------------- | ---------------------------------------------------------- |
| `DigitalInput`, `DigitalOutput` | 0 or 1                                                     |
| `AnalogInput`, `AnalogOutput`   | A real value inside the range configured on the controller |
| `GroupInput`, `GroupOutput`     | An integer coded on several bits                           |
| `Unknown`                       | The controller reports a type this library does not know   |

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

`LogicalValue` is the value seen by the RAPID programs, `PhysicalValue` the one on the hardware. They differ when the signal is simulated. `LogicalState` says whether it is simulated, `PhysicalState` whether the physical value is valid.

A controller usually declares several hundreds of signals, so `GetSignals` returns a large answer. Prefer `SearchSignals` when you only need part of them.

### Write a signal

`SetSignalValue` writes the logical value of a signal. The value is a `float`, which covers the digital, the analog and the group signals with one method.

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

Writing a signal needs no mastership, but the user account needs the write access on it, and the signal must accept a write from a remote client in the current operating mode. That is what `GetSignalConfiguration` reports, see below. The controller refuses the write with an `RwsException` when the signal is read only or when the value is outside its range.

`SetSignalValueDelayed` asks the controller to apply the value after a delay in milliseconds. The call returns immediately, the controller does the waiting.

### Pulse, toggle and invert

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

Only the digital and the group signals can be pulsed, toggled or inverted, an analog signal is refused. The three methods take a value even though they compute the written value themselves, because the controller rejects a write that carries none. Leave the two pulse lengths null to use the ones configured on the controller.

### Simulate a signal

A simulated signal keeps the value written by the client and stops following its device. This is how an input is forced during a test, without any wiring.

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

`SetSignalState` only turns the simulation on and off, the value is still written with `SetSignalValue`. `UnblockSignals` stops the simulation of every simulated signal of the controller at once, which is a good thing to call at the end of a test run.

### Search signals

`SearchSignals` narrows the result down with an `IoSignalSearchCriteria`. Every property of the criteria is optional, and an empty criteria matches every signal.

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

`SearchSignalsExtended` returns the same signals with their physical value, their time stamps, their quality and their write access level. It costs more on the controller, so use the simple search when the logical value is enough.

A second criteria can be passed. A signal is returned only when it matches both. Set `Invert` on one of the two to exclude what it matches, otherwise the result is the same as with a single criteria. `start` and `limit` page through a long result.

### Signal configuration

`GetSignalConfiguration` reports how the signal was declared in the I/O configuration of the controller: its width in bits, and who is allowed to write it.

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

`Rapid`, `LocalManual`, `LocalAuto`, `RemoteManual` and `RemoteAuto` are the write rights. Your application is a remote client, so `RemoteAuto` and `RemoteManual` are the two to check before a write. A write refused by the configuration gives an `RwsException`, not a silent failure.

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

**IoSignalType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iosignaltype))

- AnalogInput: Analog input
- AnalogOutput: Analog output
- DigitalInput: Digital input
- DigitalOutput: Digital output
- GroupInput: Group input
- GroupOutput: Group output
- Unknown: The signal type could not be determined

**IoSignalLogicalState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iosignallogicalstate))

- NotSimulated: The signal is not simulated
- Simulated: The signal is simulated: its logical value is forced and no longer follows the physical value
- Unknown: The logical state could not be determined

**IoSignalPhysicalState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iosignalphysicalstate))

- Invalid: The physical value of the signal is not valid
- Unknown: The physical state could not be determined
- Valid: The physical value of the signal is valid

## I/O devices

A device is a physical or a virtual I/O board. `GetDevices` lists them all, `GetDevice` reads one with its input and output data.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class IoDevices
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Every device of every network
        IoDeviceItem[] devices = robot.Rws.Io.GetDevices();

        foreach (IoDeviceItem item in devices)
        {
            Console.WriteLine($"{item.Path} ({item.Type}) {item.PhysicalState} {item.LogicalState}");
        }

        // One device, with its input and output data
        IoDeviceItem device = robot.Rws.Io.GetDevice("Local", "Board10");
        Console.WriteLine(device.Address);
        Console.WriteLine(device.InputData);
        Console.WriteLine(device.OutputData);

        // Number of bits and write rights of the device
        IoDeviceConfiguration config = robot.Rws.Io.GetDeviceConfiguration("Local", "Board10");
        Console.WriteLine($"{config.InputBits} input bits, {config.OutputBits} output bits");

        // Disable a device, then enable it again
        robot.Rws.Io.SetDeviceState("Local", "Board10", IoDeviceLogicalState.Disabled);
        robot.Rws.Io.SetDeviceState("Local", "Board10", IoDeviceLogicalState.Enabled);

        // Search by name, by logical state, or by both, optionally inside one network
        IoDeviceItem[] enabled = robot.Rws.Io.SearchDevices(null, IoDeviceLogicalState.Enabled, "Local");

        // Force the first input byte of a device, on a virtual controller only.
        // The mask selects the written bits, here the two lowest ones.
        robot.Rws.Io.SetDeviceInputData("Local", "Board10", 0, 0x03, 0x03);
        robot.Rws.Io.SetDeviceOutputData("Local", "Board10", 0, 0x01, 0x01);

        // Firmware state of a device and of its modules, on a real controller only
        IoDeviceUpgradeInfo upgrade = robot.Rws.Io.GetDeviceUpgradeInfo("EtherNetIP", "Local_IO");
        Console.WriteLine($"{upgrade.State} {upgrade.Status} {upgrade.ModuleCount} modules");

        foreach (IoFirmwareModuleInfo module in upgrade.Modules)
        {
            Console.WriteLine($"{module.Index} {module.ProgramName} {module.SerialNumber}");
        }

        // Send a command to a device, on a real controller only.
        // The last two arguments are the length of the value and the timeout in milliseconds.
        robot.Rws.Io.SendDeviceCommand("EtherNetIP", "Local_IO", "FIRMWARE_INFO", "", 0, 5000);

        robot.Disconnect();
    }
}
```

`PhysicalState` is the state of the hardware: `Running`, `Error`, `Unconnected`, `Unconfigured`, `Deactivated`, `Startup`, `Init` or `Halted`. `LogicalState` is what the controller was asked to do with the device, `Enabled` or `Disabled`, and `SetDeviceState` changes it. Disabling a device stops its signals from being updated.

`GetDeviceConfiguration` reports the number of input and output bits of the device and the same write rights as for a signal.

Three methods depend on the kind of controller:

- `SetDeviceInputData` and `SetDeviceOutputData` force one byte of the data of a device, on a virtual controller only. The mask selects the written bits, a bit at zero is left unchanged. A real controller refuses the request.
- `GetDeviceUpgradeInfo` reports the firmware state of a device and of its modules, on a real controller only.
- `SendDeviceCommand` sends a command to a device, on a real controller only. `valueLength` is used on an IRC5, an OmniCore computes it from the value itself and ignores the argument.

**Methods of IoService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#ioservice-robotrwsio))

- `IoDeviceItem GetDevice(string network, string device)`: Gets a single I/O device, including its input and output data (synchronous)
  - async: `Task<IoDeviceItem> GetDeviceAsync(string network, string device, CancellationToken cancellationToken = default)`
- `IoDeviceConfiguration GetDeviceConfiguration(string network, string device)`: Gets the runtime configuration properties of an I/O device (synchronous)
  - async: `Task<IoDeviceConfiguration> GetDeviceConfigurationAsync(string network, string device, CancellationToken cancellationToken = default)`
- `IoDeviceUpgradeInfo GetDeviceUpgradeInfo(string network, string device)`: Gets the firmware upgrade status of an I/O device and of each of its modules (synchronous) Only available on a real controller.
  - async: `Task<IoDeviceUpgradeInfo> GetDeviceUpgradeInfoAsync(string network, string device, CancellationToken cancellationToken = default)`
- `IoDeviceItem[] GetDevices()`: Gets every I/O device defined in the controller (synchronous)
  - async: `Task<IoDeviceItem[]> GetDevicesAsync(CancellationToken cancellationToken = default)`
- `IoDeviceItem[] SearchDevices(string name = null, IoDeviceLogicalState? logicalState = null, string network = null)`: Searches the I/O devices matching a name and/or a logical state (synchronous)
  - async: `Task<IoDeviceItem[]> SearchDevicesAsync(string name = null, IoDeviceLogicalState? logicalState = null, string network = null, CancellationToken cancellationToken = default)`
- `void SendDeviceCommand(string network, string device, string commandName, string value, int valueLength, int timeout)`: Sends a command to an I/O device (synchronous) Only available on a real controller.
  - async: `Task SendDeviceCommandAsync(string network, string device, string commandName, string value, int valueLength, int timeout, CancellationToken cancellationToken = default)`
- `void SetDeviceInputData(string network, string device, int startByte, int signalData, int dataMask)`: Writes one byte of the input data of an I/O device (synchronous) Only supported on a virtual controller.
  - async: `Task SetDeviceInputDataAsync(string network, string device, int startByte, int signalData, int dataMask, CancellationToken cancellationToken = default)`
- `void SetDeviceOutputData(string network, string device, int startByte, int signalData, int dataMask)`: Writes one byte of the output data of an I/O device (synchronous) Only supported on a virtual controller.
  - async: `Task SetDeviceOutputDataAsync(string network, string device, int startByte, int signalData, int dataMask, CancellationToken cancellationToken = default)`
- `void SetDeviceState(string network, string device, IoDeviceLogicalState logicalState)`: Enables or disables an I/O device (synchronous)
  - async: `Task SetDeviceStateAsync(string network, string device, IoDeviceLogicalState logicalState, CancellationToken cancellationToken = default)`

**IoDeviceItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iodeviceitem))

- `IoDeviceItem()`: Initializes a new instance of the Data.IoDeviceItem class
- `string Address { get; set; }`: Address of the device on its network, "-" when the network has no addressing
- `string InputData { get; set; }`: Input data of the device, as an hexadecimal string (for example "1FFFE063"). Only reported when reading a single device with IoService.GetDevice().
- `string InputMask { get; set; }`: Input mask of the device, as an hexadecimal string. A bit set to zero is an input bit that is not written. Only reported when reading a single device with IoService.GetDevice().
- `IoDeviceLogicalState LogicalState { get; set; }`: Logical state of the device
- `string Name { get; set; }`: Name of the device, for example "DRV_1" or "PANEL"
- `string NetworkName { get; set; }`: Name of the network the device is connected to, for example "Local"
- `string OutputData { get; set; }`: Output data of the device, as an hexadecimal string (for example "0000000E"). Only reported when reading a single device with IoService.GetDevice().
- `string OutputMask { get; set; }`: Output mask of the device, as an hexadecimal string. A bit set to zero is an output bit that is not written. Only reported when reading a single device with IoService.GetDevice().
- `string Path { get; set; }`: Full path of the device, "{network}/{device}" (for example "Local/DRV_1")
- `IoDevicePhysicalState PhysicalState { get; set; }`: Physical state of the device
- `string Type { get; set; }`: Type of the device, for example "DRV_1_TYPE". Not reported by every controller, null when absent. A virtual controller leaves it out.

**IoDeviceConfiguration** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iodeviceconfiguration))

- `IoDeviceConfiguration()`: Initializes a new instance of the Data.IoDeviceConfiguration class
- `bool? DenyDeactivate { get; set; }`: Whether deactivating the device is denied
- `string DeviceAddress { get; set; }`: Address of the device on its network, "-" when the network has no addressing
- `string DeviceName { get; set; }`: Name of the device, for example "DN_Internal_Device"
- `int? InputBits { get; set; }`: Number of input bits of the device, null when not reported
- `bool? LocalAuto { get; set; }`: Whether a local client can access the device in auto mode
- `bool? LocalManual { get; set; }`: Whether a local client can access the device in manual mode
- `string NetworkName { get; set; }`: Name of the industrial network the device belongs to, for example "DeviceNet"
- `int? OutputBits { get; set; }`: Number of output bits of the device, null when not reported
- `bool? Rapid { get; set; }`: Whether a RAPID client can access the device in both manual and auto mode
- `bool? RemoteAuto { get; set; }`: Whether a remote client can access the device in auto mode
- `bool? RemoteManual { get; set; }`: Whether a remote client can access the device in manual mode

**IoDeviceUpgradeInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iodeviceupgradeinfo))

- `IoDeviceUpgradeInfo()`: Initializes a new instance of the Data.IoDeviceUpgradeInfo class
- `int ModuleCount { get; }`: Number of modules reported by the controller
- `IoFirmwareModuleInfo[] Modules { get; set; }`: Firmware status of each module of the device, empty when the controller reported none
- `IoFirmwareUpgradeState State { get; set; }`: Overall progress of the firmware upgrade of the device
- `IoFirmwareUpgradeStatus Status { get; set; }`: Overall result of the firmware upgrade of the device

**IoFirmwareModuleInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iofirmwaremoduleinfo))

- `IoFirmwareModuleInfo()`: Initializes a new instance of the Data.IoFirmwareModuleInfo class
- `string HardwareRevision { get; set; }`: Hardware revision of the module, for example "C.1"
- `string Index { get; set; }`: Index of the module inside the device ("0", "1", ...)
- `string LatestProgramNameAvailable { get; set; }`: Name of the latest program available for the module
- `string ProgramName { get; set; }`: Name of the program installed on the module, for example "A_HYPIOM_B_3_8"
- `string SerialNumber { get; set; }`: Serial number of the module
- `IoFirmwareUpgradeState State { get; set; }`: Progress of the firmware upgrade of this module
- `IoFirmwareUpgradeStatus Status { get; set; }`: Result of the firmware upgrade of this module

**IoDeviceLogicalState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iodevicelogicalstate))

- Disabled: The device is disabled
- Enabled: The device is enabled
- Unknown: The logical state could not be determined

**IoDevicePhysicalState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iodevicephysicalstate))

- Deactivated: The device is deactivated
- Error: The device reports an error
- Halted: The device is halted
- Init: The device is initializing
- Running: The device is running
- Startup: The device is starting up
- Unconfigured: The device is not configured
- Unconnected: The device is not connected
- Unknown: The physical state could not be determined

**IoFirmwareUpgradeState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iofirmwareupgradestate))

- Allocate: The upgrade resources are being allocated
- Automatic: The upgrade is performed automatically
- Check: The upgraded firmware is being verified
- Deallocate: The upgrade resources are being released
- Finished: The upgrade is finished
- Info: The firmware information is being collected
- Manual: The upgrade has to be started manually
- Running: The upgrade is running
- RunningBurnInProgress: The firmware is being written to the device
- RunningCheckInProgress: The firmware is being checked
- RunningEndReceived: The device acknowledged the end of the upgrade
- RunningEraseInProgress: The device memory is being erased
- RunningStartReceived: The device acknowledged the start of the upgrade
- Start: The upgrade is starting
- Unknown: The state is unknown, or could not be parsed

**IoFirmwareUpgradeStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#iofirmwareupgradestatus))

- Error: The upgrade failed
- Ok: The upgrade finished, the firmware was already up to date
- Pending: The upgrade is pending
- Unknown: The controller did not report a status, or it could not be parsed
- Upgraded: The upgrade finished, the firmware was updated

## I/O networks

A network groups the devices connected the same way. `Local` is the internal network of the controller, a fieldbus such as EtherNet/IP or PROFINET is another one.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class IoNetworks
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Every network of the controller
        IoNetworkItem[] networks = robot.Rws.Io.GetNetworks();

        foreach (IoNetworkItem item in networks)
        {
            Console.WriteLine($"{item.Name}: {item.PhysicalState}, {item.LogicalState}");
        }

        IoNetworkItem network = robot.Rws.Io.GetNetwork("Local");

        IoNetworkConfiguration config = robot.Rws.Io.GetNetworkConfiguration("Local");
        Console.WriteLine($"{config.NetworkName} {config.NetworkType} {config.NetworkAddress}");

        // Stop a network, then start it again. Every device of the network follows.
        robot.Rws.Io.SetNetworkState("Local", IoNetworkLogicalState.Stopped);
        robot.Rws.Io.SetNetworkState("Local", IoNetworkLogicalState.Started);

        // Search by name, by physical state, or by both
        IoNetworkItem[] running = robot.Rws.Io.SearchNetworks(null, IoNetworkPhysicalState.Running);

        // Run the auto configuration of a fieldbus network.
        // This rewrites the I/O configuration and cannot be undone.
        IoClientAction action = robot.Rws.Io.SetNetworkConfigurationType("DeviceNet", IoNetworkConfigurationType.Scan);

        if (action == IoClientAction.Restart)
        {
            Console.WriteLine("Restart the controller to apply the new configuration");
        }

        // Names of the I/O resources the controller exposes
        string[] resources = robot.Rws.Io.GetResources();

        robot.Disconnect();
    }
}
```

`SetNetworkState` starts and stops a network. Every device of the network follows, so stopping a network stops the signals of all its devices at once.

`GetNetworkConfiguration` returns the type and the address of the network. `GetResources` returns the names of the I/O resources the controller exposes, which is mostly useful to check what a given controller supports.

### Auto configuration

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. Only an OmniCore reports the action the client should take

`SetNetworkConfigurationType` runs the auto configuration of a fieldbus network. It rewrites part of the I/O configuration of the controller and cannot be undone, so keep it out of a production application.

| `IoNetworkConfigurationType` | Configures                                  |
| ---------------------------- | ------------------------------------------- |
| `Scan`                       | Scans the network for the connected devices |
| `Units`                      | The devices of the network                  |
| `Bits`                       | The signals of the network                  |
| `Groups`                     | The signal groups of the network            |
| `Both`                       | The signals and the signal groups           |

The returned `IoClientAction` says what to do next: `None` when nothing is needed, `Info` when the result should be shown to the user, `Restart` when the controller has to be restarted for the new configuration to take effect. An IRC5 does not report it, `Unknown` is then always returned.

**Methods of IoService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#ioservice-robotrwsio))

- `IoNetworkItem GetNetwork(string network)`: Gets a single I/O network (synchronous)
  - async: `Task<IoNetworkItem> GetNetworkAsync(string network, CancellationToken cancellationToken = default)`
- `IoNetworkConfiguration GetNetworkConfiguration(string network)`: Gets the runtime configuration properties of an I/O network (synchronous)
  - async: `Task<IoNetworkConfiguration> GetNetworkConfigurationAsync(string network, CancellationToken cancellationToken = default)`
- `IoNetworkItem[] GetNetworks()`: Gets every I/O network defined in the controller (synchronous)
  - async: `Task<IoNetworkItem[]> GetNetworksAsync(CancellationToken cancellationToken = default)`
- `string[] GetResources()`: Gets the names of the I/O sub resources exposed by the controller (synchronous)
  - async: `Task<string[]> GetResourcesAsync(CancellationToken cancellationToken = default)`
- `IoNetworkItem[] SearchNetworks(string name = null, IoNetworkPhysicalState? physicalState = null)`: Searches the I/O networks matching a name and/or a physical state (synchronous)
  - async: `Task<IoNetworkItem[]> SearchNetworksAsync(string name = null, IoNetworkPhysicalState? physicalState = null, CancellationToken cancellationToken = default)`
- `IoClientAction SetNetworkConfigurationType(string network, IoNetworkConfigurationType configurationType)`: Runs the auto configuration of an I/O network (synchronous)
  - async: `Task<IoClientAction> SetNetworkConfigurationTypeAsync(string network, IoNetworkConfigurationType configurationType, CancellationToken cancellationToken = default)`
- `void SetNetworkState(string network, IoNetworkLogicalState logicalState)`: Starts or stops an I/O network (synchronous)
  - async: `Task SetNetworkStateAsync(string network, IoNetworkLogicalState logicalState, CancellationToken cancellationToken = default)`

**IoNetworkItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#ionetworkitem))

- `IoNetworkItem()`: Initializes a new instance of the Data.IoNetworkItem class
- `IoNetworkLogicalState LogicalState { get; set; }`: Logical state of the network
- `string Name { get; set; }`: Name of the network, for example "Local", "Virtual" or "EtherNetIP"
- `string Path { get; set; }`: Full path of the network, which is its name for a network (for example "Local")
- `IoNetworkPhysicalState PhysicalState { get; set; }`: Physical state of the network

**IoNetworkConfiguration** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#ionetworkconfiguration))

- `IoNetworkConfiguration()`: Initializes a new instance of the Data.IoNetworkConfiguration class
- `string NetworkAddress { get; set; }`: Industrial network address, "-" when the network has no addressing
- `string NetworkName { get; set; }`: Name of the network, for example "Local"
- `string NetworkType { get; set; }`: Type of the network, for example "Local" or "LOC"

**IoNetworkLogicalState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#ionetworklogicalstate))

- Started: The network is started
- Stopped: The network is stopped
- Unknown: The logical state could not be determined

**IoNetworkPhysicalState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#ionetworkphysicalstate))

- Error: The network reports an error
- Halted: The network is halted
- Init: The network is initializing
- Running: The network is running
- Startup: The network is starting up
- Unknown: The physical state could not be determined

**IoNetworkConfigurationType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#ionetworkconfigurationtype))

- Bits: Configure the signals of the network
- Both: Configure both the signals and the signal groups
- Groups: Configure the signal groups of the network
- Scan: Scan the network for connected devices
- Units: Configure the devices of the network

**IoClientAction** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#ioclientaction))

- Info: The user should be informed of the configuration result
- None: Nothing to do
- Restart: The controller has to be restarted for the configuration to take effect
- Unknown: The controller did not report any client action. Always returned when connected with version 1, which does not report this information.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).
