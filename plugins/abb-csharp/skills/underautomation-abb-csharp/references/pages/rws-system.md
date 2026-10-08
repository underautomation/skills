# System information & energy

Read the RobotWare version, the installed options and products, the robot types of the system, and the energy consumption counters.

Web page: https://underautomation.com/abb/documentation/rws-system

`robot.Rws.System` describes the system installed on the controller: its name and software version, the options and the products it was built with, the type of robot it drives, its license, and the energy it consumes. Everything here is read only, except the reset of the energy counter.

Do not confuse this service with [Controller](rws-controller.md), which reports the identity of the controller hardware. `System` reports the software running on it.

## System information

`GetInfo` returns a `SystemInfo` with the name of the system, the robot software version and the installed options.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class SystemGetInfo
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        SystemInfo info = robot.Rws.System.GetInfo();

        Console.WriteLine(info.Name);          // name of the system
        Console.WriteLine(info.VersionName);   // readable robot software version
        Console.WriteLine(info.Version);
        Console.WriteLine(info.SystemId);      // unique identifier of the system
        Console.WriteLine(info.StartTime);     // last start, null on some controllers
        Console.WriteLine(info.OptionCount);

        // The options come with the description, no second call needed
        foreach (string option in info.Options)
            Console.WriteLine(option);

        robot.Disconnect();
    }
}
```

A virtual controller does not fill every field. The detailed version numbers, the build tag and the timestamps are usually empty on a simulated system, which is why they are nullable. The name, the version and the system identifier are always there.

The options are returned with the description, so `GetOptions` is not needed when you call `GetInfo`.

## Options, products, robot types and license

| Method              | Returns                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| `GetOptions()`      | `string[]`, the names of the installed options                         |
| `GetProducts(name)` | `SystemProduct[]`, the installed software products with their versions |
| `GetRobotTypes()`   | `string[]`, for example `IRB 120-3/0.6`                                |
| `GetLicense()`      | `string`, the license the robot software runs under                    |

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class SystemOptions
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Installed options
        foreach (string option in robot.Rws.System.GetOptions())
            Console.WriteLine(option);

        // Installed products and their versions
        foreach (SystemProduct product in robot.Rws.System.GetProducts())
            Console.WriteLine($"{product.Name} {product.VersionName}");

        // One product only. The name must match exactly
        SystemProduct[] robotWare = robot.Rws.System.GetProducts("RobotWare");

        // Type of every robot the controller drives
        foreach (string type in robot.Rws.System.GetRobotTypes())
            Console.WriteLine(type);

        // License the robot software runs under
        Console.WriteLine(robot.Rws.System.GetLicense());

        Console.WriteLine(robotWare.Length);
        robot.Disconnect();
    }
}
```

`GetProducts` takes an optional name to report a single product. The name has to match an installed product exactly, the controller rejects an unknown one with an error instead of returning an empty list. Call it without argument to get every product.

`GetRobotTypes` only reports standard ABB robots. Positioners, track motions and other mechanical units are left out. A controller that drives none of them returns an empty array, not an error. Use `robot.Rws.MotionSystem.GetMechanicalUnits()` when you need the complete list.

`GetLicense` returns `VIRTUAL_USE` on a RobotStudio virtual controller.

## Energy consumption

`GetEnergy` returns the energy the controller consumed, for the current measurement interval and since the last reset, broken down per mechanical unit and per axis. Values are in joules.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class SystemEnergyRead
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        SystemEnergy energy = robot.Rws.System.GetEnergy();

        // Always check this first, the other values mean nothing when it is false
        if (!energy.IsMeasurementValid)
        {
            Console.WriteLine($"No measurement available, state is {energy.State}");
            return;
        }

        Console.WriteLine($"Interval : {energy.IntervalEnergy} J over {energy.IntervalLength} s");
        Console.WriteLine($"Average power : {energy.AveragePower} W");
        Console.WriteLine($"Accumulated : {energy.AccumulatedEnergy} J since {energy.ResetTime}");

        // Breakdown per mechanical unit and per axis
        foreach (SystemEnergyMechanicalUnit unit in energy.MechanicalUnits)
        {
            Console.WriteLine(unit.Name);

            foreach (SystemEnergyAxis axis in unit.Axes)
                Console.WriteLine($"  axis {axis.Number} : {axis.IntervalEnergy} J");
        }

        robot.Disconnect();
    }
}
```

Check `IsMeasurementValid` first. The controller answers with a complete but meaningless measurement while it has nothing to report, and `State` then tells why. `AveragePower` is computed by the SDK from the interval energy and the interval length, in watts, and is null when one of the two is missing.

| `SystemEnergyState`             | Meaning                                                          |
| ------------------------------- | ---------------------------------------------------------------- |
| `NotPaused`                     | Measurement is running                                           |
| `Paused`, `Pausing`, `Resuming` | Measurement is stopped or changing state                         |
| `Blocked`                       | Measurement is blocked, no new value is produced                 |
| `GoingToSleep`, `Sleep`         | The controller is entering or in its low energy consumption mode |
| `Unknown`                       | The state could not be determined                                |

## Polling the energy

Reading the whole measurement is not cheap. `GetEnergyChangeCount` returns a single number the controller increments each time a new measurement is available. Poll that number, and read the measurement only when it moved.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class SystemEnergyPolling
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        int? lastCount = robot.Rws.System.GetEnergyChangeCount();

        while (true)
        {
            Thread.Sleep(1000);

            // One small request. Read the whole measurement only when the counter moved
            int? count = robot.Rws.System.GetEnergyChangeCount();

            if (count == lastCount) continue;

            lastCount = count;

            SystemEnergy energy = robot.Rws.System.GetEnergy();
            Console.WriteLine($"{energy.TimeStamp} : {energy.AccumulatedEnergy} J");
        }
    }
}
```

The same counter is also in `SystemEnergy.ChangeCount`. Both return null when the controller does not report it.

## Reset the accumulated energy

`ResetAccumulatedEnergy` sets the accumulated counter back to zero. The energy counted before is lost, the controller keeps no history. The reset moment becomes the new reference reported by `ResetTime`. The energy of the current interval is not affected.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class SystemEnergyReset
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The accumulated counter goes back to zero, the energy counted before is lost
        robot.Rws.System.ResetAccumulatedEnergy();

        SystemEnergy energy = robot.Rws.System.GetEnergy();

        // ResetTime is now the reference of the accumulated energy
        Console.WriteLine($"{energy.AccumulatedEnergy} J since {energy.ResetTime}");

        robot.Disconnect();
    }
}
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**Methods of SystemService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#systemservice-robotrwssystem))

- `SystemEnergy GetEnergy()`: Gets the energy the controller consumed, for the current interval and since the last reset (synchronous)
  - async: `Task<SystemEnergy> GetEnergyAsync(CancellationToken cancellationToken = default)`
- `int? GetEnergyChangeCount()`: Gets the counter the controller increments each time a new energy measurement is available (synchronous)
  - async: `Task<int?> GetEnergyChangeCountAsync(CancellationToken cancellationToken = default)`
- `SystemInfo GetInfo()`: Gets the name, the software version and the installed options of the system (synchronous)
  - async: `Task<SystemInfo> GetInfoAsync(CancellationToken cancellationToken = default)`
- `string GetLicense()`: Gets the license the robot software runs under (synchronous)
  - async: `Task<string> GetLicenseAsync(CancellationToken cancellationToken = default)`
- `string[] GetOptions()`: Gets the options installed on the system (synchronous)
  - async: `Task<string[]> GetOptionsAsync(CancellationToken cancellationToken = default)`
- `SystemProduct[] GetProducts(string name = null)`: Gets the software products installed on the controller, with their versions (synchronous)
  - async: `Task<SystemProduct[]> GetProductsAsync(string name = null, CancellationToken cancellationToken = default)`
- `string[] GetRobotTypes()`: Gets the type of every robot the controller drives (synchronous)
  - async: `Task<string[]> GetRobotTypesAsync(CancellationToken cancellationToken = default)`
- `void ResetAccumulatedEnergy()`: Sets the accumulated energy counter of the controller back to zero (synchronous)
  - async: `Task ResetAccumulatedEnergyAsync(CancellationToken cancellationToken = default)`

**SystemInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#systeminfo))

- `SystemInfo()`: Initializes a new instance of the Data.SystemInfo class
- `int? ApiCompatibilityRevision { get; set; }`: Revision of the programming interface the system is compatible with, null when the controller did not report it
- `int? Build { get; set; }`: Build number of the version, null when the controller did not report it
- `string BuildTag { get; set; }`: Free text describing the build the system was produced by, null when the controller did not report it
- `string ConfigurationTimestamp { get; set; }`: Timestamp of the configuration the system was built with, as the controller spells it. Null when the controller did not report it, which is the usual case on a virtual controller.
- `DateTime? Date { get; set; }`: Date the system was produced, null when the controller did not report it
- `string Description { get; set; }`: Description of the system, null when the controller did not report it
- `string DistributionVersion { get; set; }`: Version of the software distribution the system was installed from. Null when the controller does not report it.
- `int? Major { get; set; }`: Major number of the version, null when the controller did not report it
- `int? Minor { get; set; }`: Minor number of the version, null when the controller did not report it
- `string Name { get; set; }`: Name of the system installed on the controller
- `int OptionCount { get; }`: Number of options installed on the system
- `string[] Options { get; set; }`: Options installed on the system, in the order the controller reports them
- `int? Revision { get; set; }`: Revision number of the version, null when the controller did not report it
- `DateTime? StartTime { get; set; }`: Moment the system was last started, null when the controller did not report it
- `int? SubRevision { get; set; }`: Sub revision number of the version, null when the controller did not report it
- `string SystemId { get; set; }`: Unique identifier of the system
- `string Title { get; set; }`: Title of the system, null when the controller did not report it
- `string Type { get; set; }`: Type of the system, null when the controller did not report it
- `string Version { get; set; }`: Version of the robot software the system runs
- `string VersionName { get; set; }`: Human readable version of the robot software the system runs

**SystemProduct** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#systemproduct))

- `SystemProduct()`: Initializes a new instance of the Data.SystemProduct class
- `string Name { get; set; }`: Name of the product, for example "RobotWare" or "RobotControl"
- `string Version { get; set; }`: Full version of the product, build information included. Null when the controller only reports the version name.
- `string VersionName { get; set; }`: Human readable version of the product

**SystemEnergy** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#systemenergy))

- `SystemEnergy()`: Initializes a new instance of the Data.SystemEnergy class
- `double? AccumulatedEnergy { get; set; }`: Total energy consumed since the last reset, in joules, null when the controller did not report it
- `double? AveragePower { get; }`: Average power consumed during the current measurement interval, in watts. Null when the interval energy or the interval length is missing, or when the interval is empty.
- `int? ChangeCount { get; set; }`: Counter the controller increments every time a new measurement is available. Comparing it with the previous one tells whether the values changed without reading them all.
- `double? IntervalEnergy { get; set; }`: Total energy consumed during the current measurement interval, in joules, null when the controller did not report it
- `int? IntervalLength { get; set; }`: Length of the measurement interval in seconds, which the average power is computed from, null when the controller did not report it
- `bool IsMeasurementValid { get; set; }`: Whether the reported measurement is valid. When false, every energy value of this instance is meaningless and the measurement has to be read again later.
- `int MechanicalUnitCount { get; }`: Number of mechanical units the controller reported
- `SystemEnergyMechanicalUnit[] MechanicalUnits { get; set; }`: Energy consumed by each mechanical unit during the current measurement interval
- `DateTime? ResetTime { get; set; }`: Moment the accumulated energy was last reset, null when the controller did not report it
- `SystemEnergyState State { get; set; }`: State of the energy measurement
- `DateTime? TimeStamp { get; set; }`: Moment the measurement was taken, null when the controller did not report it

**SystemEnergyMechanicalUnit** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#systemenergymechanicalunit))

- `SystemEnergyMechanicalUnit()`: Initializes a new instance of the Data.SystemEnergyMechanicalUnit class
- `SystemEnergyAxis[] Axes { get; set; }`: Energy consumed by each axis of the mechanical unit during the current measurement interval
- `int AxisCount { get; }`: Number of axes the controller reported for this mechanical unit
- `string Name { get; set; }`: Name of the mechanical unit, for example "ROB_1"

**SystemEnergyAxis** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#systemenergyaxis))

- `SystemEnergyAxis()`: Initializes a new instance of the Data.SystemEnergyAxis class
- `double? IntervalEnergy { get; set; }`: Energy the axis consumed during the current measurement interval, in joules, null when the controller did not report it
- `int Number { get; set; }`: Number of the axis inside its mechanical unit, starting at 1

**SystemEnergyState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#systemenergystate))

- Blocked: Energy measurement is blocked and no new value is produced
- GoingToSleep: The controller is entering its low energy consumption mode
- NotPaused: Energy measurement is running
- Paused: Energy measurement is paused
- Pausing: Energy measurement is being paused
- Resuming: Energy measurement is being resumed
- Sleep: The controller is in its low energy consumption mode
- Unknown: The energy state could not be determined
