# System information & energy

Read the RobotWare version, the installed options and products, the robot types of the system, and the energy consumption counters.

Web page: https://underautomation.com/abb/documentation/rws-system

`robot.Rws.System` describes the system installed on the controller: its name and software version, the options and the products it was built with, the type of robot it drives, its license, and the energy it consumes. Everything here is read only, except the reset of the energy counter.

Do not confuse this service with [Controller](rws-controller.md), which reports the identity of the controller hardware. `System` reports the software running on it.

## System information

`GetInfo` returns a `SystemInfo` with the name of the system, the robot software version and the installed options.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

info = robot.rws.system.get_info()

print(info.name)          # name of the system
print(info.version_name)  # readable robot software version
print(info.version)
print(info.system_id)     # unique identifier of the system
print(info.start_time)    # last start, None on some controllers
print(info.option_count)

# The options come with the description, no second call needed
for option in info.options:
    print(option)

robot.disconnect()
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

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Installed options
for option in robot.rws.system.get_options():
    print(option)

# Installed products and their versions
for product in robot.rws.system.get_products():
    print(f"{product.name} {product.version_name}")

# One product only. The name must match exactly
robot_ware = robot.rws.system.get_products("RobotWare")

# Type of every robot the controller drives
for robot_type in robot.rws.system.get_robot_types():
    print(robot_type)

# License the robot software runs under
print(robot.rws.system.get_license())

robot.disconnect()
```

`GetProducts` takes an optional name to report a single product. The name has to match an installed product exactly, the controller rejects an unknown one with an error instead of returning an empty list. Call it without argument to get every product.

`GetRobotTypes` only reports standard ABB robots. Positioners, track motions and other mechanical units are left out. A controller that drives none of them returns an empty array, not an error. Use `robot.Rws.MotionSystem.GetMechanicalUnits()` when you need the complete list.

`GetLicense` returns `VIRTUAL_USE` on a RobotStudio virtual controller.

## Energy consumption

`GetEnergy` returns the energy the controller consumed, for the current measurement interval and since the last reset, broken down per mechanical unit and per axis. Values are in joules.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

energy = robot.rws.system.get_energy()

# Always check this first, the other values mean nothing when it is false
if not energy.is_measurement_valid:
    print(f"No measurement available, state is {energy.state}")
    raise SystemExit(0)

print(f"Interval : {energy.interval_energy} J over {energy.interval_length} s")
print(f"Average power : {energy.average_power} W")
print(f"Accumulated : {energy.accumulated_energy} J since {energy.reset_time}")

# Breakdown per mechanical unit and per axis
for unit in energy.mechanical_units:
    print(unit.name)

    for axis in unit.axes:
        print(f"  axis {axis.number} : {axis.interval_energy} J")

robot.disconnect()
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

```python
import time

from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

last_count = robot.rws.system.get_energy_change_count()

while True:
    time.sleep(1)

    # One small request. Read the whole measurement only when the counter moved
    count = robot.rws.system.get_energy_change_count()

    if count == last_count:
        continue

    last_count = count

    energy = robot.rws.system.get_energy()
    print(f"{energy.time_stamp} : {energy.accumulated_energy} J")
```

The same counter is also in `SystemEnergy.ChangeCount`. Both return null when the controller does not report it.

## Reset the accumulated energy

`ResetAccumulatedEnergy` sets the accumulated counter back to zero. The energy counted before is lost, the controller keeps no history. The reset moment becomes the new reference reported by `ResetTime`. The energy of the current interval is not affected.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# The accumulated counter goes back to zero, the energy counted before is lost
robot.rws.system.reset_accumulated_energy()

energy = robot.rws.system.get_energy()

# reset_time is now the reference of the accumulated energy
print(f"{energy.accumulated_energy} J since {energy.reset_time}")

robot.disconnect()
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**Methods of SystemService** ([reference](../api/underautomation.abb.rws.services.md#systemservice-robotrwssystem))

- `get_info() -> SystemInfo`: Gets the name, the software version and the installed options of the system (synchronous)
- `get_options() -> typing.List[str]`: Gets the options installed on the system (synchronous)
- `get_license() -> str`: Gets the license the robot software runs under (synchronous)
- `get_robot_types() -> typing.List[str]`: Gets the type of every robot the controller drives (synchronous)
- `get_products(name: str=None) -> typing.List[SystemProduct]`: Gets the software products installed on the controller, with their versions (synchronous)
- `get_energy() -> SystemEnergy`: Gets the energy the controller consumed, for the current interval and since the last reset (synchronous)
- `get_energy_change_count() -> int | None`: Gets the counter the controller increments each time a new energy measurement is available (synchronous)
- `reset_accumulated_energy() -> None`: Sets the accumulated energy counter of the controller back to zero (synchronous)

**SystemInfo** ([reference](../api/underautomation.abb.rws.data.md#systeminfo))

- `SystemInfo()`: Initializes a new instance of the SystemInfo class
- `name: str`: Name of the system installed on the controller
- `version: str`: Version of the robot software the system runs
- `version_name: str`: Human readable version of the robot software the system runs
- `distribution_version: str`: Version of the software distribution the system was installed from. Null when the controller does not report it.
- `system_id: str`: Unique identifier of the system
- `start_time: datetime | None`: Moment the system was last started, null when the controller did not report it
- `major: int | None`: Major number of the version, null when the controller did not report it
- `minor: int | None`: Minor number of the version, null when the controller did not report it
- `build: int | None`: Build number of the version, null when the controller did not report it
- `revision: int | None`: Revision number of the version, null when the controller did not report it
- `sub_revision: int | None`: Sub revision number of the version, null when the controller did not report it
- `build_tag: str`: Free text describing the build the system was produced by, null when the controller did not report it
- `api_compatibility_revision: int | None`: Revision of the programming interface the system is compatible with, null when the controller did not report it
- `title: str`: Title of the system, null when the controller did not report it
- `type: str`: Type of the system, null when the controller did not report it
- `description: str`: Description of the system, null when the controller did not report it
- `date: datetime | None`: Date the system was produced, null when the controller did not report it
- `configuration_timestamp: str`: Timestamp of the configuration the system was built with, as the controller spells it. Null when the controller did not report it, which is the usual case on a virtual controller.
- `options: typing.List[str]`: Options installed on the system, in the order the controller reports them
- `option_count: int (read only)`: Number of options installed on the system

**SystemProduct** ([reference](../api/underautomation.abb.rws.data.md#systemproduct))

- `SystemProduct()`: Initializes a new instance of the SystemProduct class
- `name: str`: Name of the product, for example "RobotWare" or "RobotControl"
- `version: str`: Full version of the product, build information included. Null when the controller only reports the version name.
- `version_name: str`: Human readable version of the product

**SystemEnergy** ([reference](../api/underautomation.abb.rws.data.md#systemenergy))

- `SystemEnergy()`: Initializes a new instance of the SystemEnergy class
- `is_measurement_valid: bool`: Whether the reported measurement is valid. When false, every energy value of this instance is meaningless and the measurement has to be read again later.
- `state: SystemEnergyState`: State of the energy measurement
- `change_count: int | None`: Counter the controller increments every time a new measurement is available. Comparing it with the previous one tells whether the values changed without reading them all.
- `time_stamp: datetime | None`: Moment the measurement was taken, null when the controller did not report it
- `reset_time: datetime | None`: Moment the accumulated energy was last reset, null when the controller did not report it
- `interval_length: int | None`: Length of the measurement interval in seconds, which the average power is computed from, null when the controller did not report it
- `interval_energy: float | None`: Total energy consumed during the current measurement interval, in joules, null when the controller did not report it
- `accumulated_energy: float | None`: Total energy consumed since the last reset, in joules, null when the controller did not report it
- `mechanical_units: typing.List[SystemEnergyMechanicalUnit]`: Energy consumed by each mechanical unit during the current measurement interval
- `average_power: float | None (read only)`: Average power consumed during the current measurement interval, in watts. Null when the interval energy or the interval length is missing, or when the interval is empty.
- `mechanical_unit_count: int (read only)`: Number of mechanical units the controller reported

**SystemEnergyMechanicalUnit** ([reference](../api/underautomation.abb.rws.data.md#systemenergymechanicalunit))

- `SystemEnergyMechanicalUnit()`: Initializes a new instance of the SystemEnergyMechanicalUnit class
- `name: str`: Name of the mechanical unit, for example "ROB_1"
- `axes: typing.List[SystemEnergyAxis]`: Energy consumed by each axis of the mechanical unit during the current measurement interval
- `axis_count: int (read only)`: Number of axes the controller reported for this mechanical unit

**SystemEnergyAxis** ([reference](../api/underautomation.abb.rws.data.md#systemenergyaxis))

- `SystemEnergyAxis()`: Initializes a new instance of the SystemEnergyAxis class
- `number: int`: Number of the axis inside its mechanical unit, starting at 1
- `interval_energy: float | None`: Energy the axis consumed during the current measurement interval, in joules, null when the controller did not report it

**SystemEnergyState** ([reference](../api/underautomation.abb.rws.data.md#systemenergystate))

- Unknown: The energy state could not be determined
- Blocked: Energy measurement is blocked and no new value is produced
- Paused: Energy measurement is paused
- NotPaused: Energy measurement is running
- Resuming: Energy measurement is being resumed
- Pausing: Energy measurement is being paused
- GoingToSleep: The controller is entering its low energy consumption mode
- Sleep: The controller is in its low energy consumption mode
