# Read & write I/O signals

Read and write digital, analog and group I/O signals of an ABB controller, pulse a signal and simulate one during tests.

Web page: https://underautomation.com/abb/documentation/read-write-io-signals

Reading an I/O signal of an ABB controller is `robot.Rws.Io.GetSignal(network, device, signal)`, and writing one is `robot.Rws.Io.SetSignalValue(network, device, signal, value)`. Digital, analog and group signals all go through the same two methods, only the value changes. I/O needs no mastership, it needs a user account with the write grant.

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

## How a signal is identified

A signal has three parts: the network it belongs to, the device it is connected to, and its name. `Local` is the internal network of the controller, and the signals of the robot itself are usually on it.

`IoSignalItem.Path` gives the three parts joined, for example `Local/Board10/DO_Gripper`. If you only know the name of a signal, find its network and its device with `GetSignals()` or with a search.

## Read a signal

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# A signal is identified by its network, its device and its name
signal = robot.rws.io.get_signal("Local", "Board10", "DO_Gripper")

print(signal.path)            # Local/Board10/DO_Gripper
print(signal.type)            # DigitalOutput
print(signal.logical_value)   # 1
print(signal.logical_state)   # NotSimulated
print(signal.physical_value)  # 1
print(signal.physical_state)  # Valid

# Every signal of the controller, in one call
signals = robot.rws.io.get_signals()

for item in signals:
    print(f"{item.path} = {item.logical_value} ({item.type})")

robot.disconnect()
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

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# A digital signal takes 0 or 1
robot.rws.io.set_signal_value("Local", "Board10", "DO_Gripper", 1)

# An analog or a group signal takes any value inside its range
robot.rws.io.set_signal_value("Local", "Board10", "AO_Speed", 12.5)

# The last argument writes the change in the event log of the controller
robot.rws.io.set_signal_value("Local", "Board10", "DO_Gripper", 0, True)

# The controller applies the value 500 ms later, and answers immediately
robot.rws.io.set_signal_value_delayed("Local", "Board10", "DO_Gripper", 1, 500)

robot.disconnect()
```

## Pulse, toggle and invert

A pulse is done by the controller, which is more precise than two writes separated by a `Thread.Sleep` in your application.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Three pulses to 1, 200 ms active and 200 ms passive
robot.rws.io.pulse_signal("Local", "Board10", "DO_Gripper", 1, 3, 200, 200)

# Same, with the pulse lengths configured on the controller
robot.rws.io.pulse_signal("Local", "Board10", "DO_Gripper", 1, 1)

# toggle_signal pulses the signal by starting from the opposite of its current value
robot.rws.io.toggle_signal("Local", "Board10", "DO_Gripper", 1, 2, 200, 200)

# invert_signal writes the opposite of the current value, once
robot.rws.io.invert_signal("Local", "Board10", "DO_Gripper", 1)

robot.disconnect()
```

## Wait for a signal

There is no subscription in this SDK, a value is read by asking for it. To wait for an input, poll it with a period and a timeout. 200 ms is a reasonable period, a shorter one loads the controller for nothing.

```python
import time

from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Polls one signal until it reaches the expected value, or the timeout expires.
# 200 ms is a reasonable period : a shorter one loads the controller for nothing.
def wait_value(robot, network, device, signal, expected, timeout_ms):
    limit = time.time() + timeout_ms / 1000.0

    while time.time() < limit:
        item = robot.rws.io.get_signal(network, device, signal)

        if item.logical_value == expected:
            return True

        time.sleep(0.2)

    return False

# Ask the robot to work, then wait for its answer
robot.rws.io.set_signal_value("Local", "Board10", "DO_Start", 1)

if not wait_value(robot, "Local", "Board10", "DI_Done", 1, 10000):
    raise Exception("The robot did not answer in 10 seconds")

robot.rws.io.set_signal_value("Local", "Board10", "DO_Start", 0)

robot.disconnect()
```

When the reaction has to be faster than that, do the waiting in RAPID with a `WaitDI`, and use the SDK to give the program the order to start.

## Simulate a signal during a test

A simulated signal keeps the value written by the client and stops following its device. This is how an input is forced from a test bench, on a real controller as well as on a virtual one.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Simulate an input: it keeps the value written by the client
robot.rws.io.set_signal_state("Local", "Board10", "DI_PartPresent", True)
robot.rws.io.set_signal_value("Local", "Board10", "DI_PartPresent", 1)

signal = robot.rws.io.get_signal("Local", "Board10", "DI_PartPresent")
print(signal.logical_state)  # Simulated

# Give the signal back to its device
robot.rws.io.set_signal_state("Local", "Board10", "DI_PartPresent", False)

# Or stop simulating every simulated signal of the controller at once
robot.rws.io.unblock_signals()

robot.disconnect()
```

Do not leave a signal simulated at the end of a test. `UnblockSignals()` stops the simulation of every simulated signal of the controller at once.

## Who is allowed to write a signal

A signal can be write protected depending on who writes it and in which operation mode. When a write is refused and the mastership is not the reason, read the configuration of the signal.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

config = robot.rws.io.get_signal_configuration("Local", "Board10", "DO_Gripper")

print(config.signal_name)   # DO_Gripper
print(config.signal_bits)   # 1

# Who is allowed to write the signal, and in which operation mode
print(config.rapid)         # a RAPID program
print(config.local_manual)  # the teach pendant, in manual mode
print(config.local_auto)    # the teach pendant, in auto mode
print(config.remote_manual) # a remote client, in manual mode
print(config.remote_auto)   # a remote client, in auto mode

robot.disconnect()
```

## Find the signals you need

`SearchSignals` filters on the name, the device, the network, the type and the category. A second criteria can be inverted to exclude what it matches, which is how the safety signals are left out of a list.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.io_signal_search_criteria import IoSignalSearchCriteria
from underautomation.abb.rws.data.io_signal_type import IoSignalType

robot = AbbController()
robot.connect("192.168.0.1")

# Every digital output of one device
criteria = IoSignalSearchCriteria()
criteria.device_name = "Board10"
criteria.type = IoSignalType.DigitalOutput

outputs = robot.rws.io.search_signals(criteria)

for signal in outputs:
    print(f"{signal.name} = {signal.logical_value}")

# The extended search also reports the physical value and the write access level
extended = robot.rws.io.search_signals_extended(criteria, None, 0, 50)

print(extended[0].physical_value)
print(extended[0].quality)
print(extended[0].write_access_level)

# A second inverted criteria excludes what it matches, here the safety signals
exclude = IoSignalSearchCriteria()
exclude.category = "safety"
exclude.invert = True

without_safety = robot.rws.io.search_signals(criteria, exclude)

robot.disconnect()
```

## Going further

- [I/O signals, devices & networks](rws-io.md), the complete reference
- [Start & stop a RAPID program](start-stop-rapid-program.md), to trigger a program that reacts to your signals
- [Read & write RAPID variables](read-write-rapid-variables.md), the other way of exchanging data with a program

**Methods of IoService** ([reference](../api/underautomation.abb.rws.services.md#ioservice-robotrwsio))

- `get_signals() -> typing.List[IoSignalItem]`: Gets every I/O signal defined in the controller (synchronous) A controller usually exposes several hundreds of signals. Use to narrow the result down to a network, a device, a category or a signal type.
- `get_signal(network: str, device: str, signal: str) -> IoSignalItem`: Gets a single I/O signal, including its physical value and time stamps (synchronous)
- `get_signal_configuration(network: str, device: str, signal: str) -> IoSignalConfiguration`: Gets the runtime configuration properties of an I/O signal (synchronous)
- `set_signal_value(network: str, device: str, signal: str, value: float, logToEventLog: bool=False) -> None`: Writes the value of an I/O signal (synchronous)
- `set_signal_value_delayed(network: str, device: str, signal: str, value: float, delay: int, logToEventLog: bool=False) -> None`: Writes the value of an I/O signal in "queued delayed" mode (synchronous) The controller queues the write and applies it once the delay has elapsed.
- `invert_signal(network: str, device: str, signal: str, value: float, logToEventLog: bool=False) -> None`: Inverts the value of an I/O signal (synchronous) Only digital and group signals can be inverted.
- `pulse_signal(network: str, device: str, signal: str, value: float, pulses: int, activePulseLength: int | None=None, passivePulseLength: int | None=None, logToEventLog: bool=False) -> None`: Pulses the value of an I/O signal (synchronous) Only digital and group signals can be pulsed.
- `toggle_signal(network: str, device: str, signal: str, value: float, pulses: int, activePulseLength: int | None=None, passivePulseLength: int | None=None, logToEventLog: bool=False) -> None`: Pulses an I/O signal by toggling its current value (synchronous) Only digital and group signals can be toggled.
- `set_signal_state(network: str, device: str, signal: str, simulated: bool) -> None`: Simulates or stops simulating an I/O signal (synchronous) A simulated signal keeps the logical value written by the client and no longer follows its physical value.
- `search_signals(criteria: IoSignalSearchCriteria=None, secondCriteria: IoSignalSearchCriteria=None, start: int | None=None, limit: int | None=None) -> typing.List[IoSignalItem]`: Searches the I/O signals matching the given criteria (synchronous) The returned signals carry their name, type, category, logical value and logical state. Use to also get their physical value, time stamps and write access level.
- `search_signals_extended(criteria: IoSignalSearchCriteria=None, secondCriteria: IoSignalSearchCriteria=None, start: int | None=None, limit: int | None=None) -> typing.List[IoSignalItem]`: Searches the I/O signals matching the given criteria and returns their extended properties (synchronous) In addition to , the returned signals carry their physical value, quality, time stamps and write access level.
- `unblock_signals() -> None`: Removes the simulation of every simulated I/O signal of the controller (synchronous)

**IoSignalItem** ([reference](../api/underautomation.abb.rws.data.md#iosignalitem))

- `IoSignalItem()`: Initializes a new instance of the IoSignalItem class
- `name: str`: Name of the signal, for example "DRV1BRAKE"
- `network_name: str`: Name of the network the signal belongs to, for example "Local"
- `device_name: str`: Name of the device the signal is connected to, for example "DRV_1"
- `path: str`: Full path of the signal, "{network}/{device}/{signal}" (for example "Local/DRV_1/DRV1BRAKE")
- `type: IoSignalType`: Type of the signal
- `category: str`: Category the signal belongs to, for example "safety"
- `logical_value: float | None`: Logical value of the signal, null when the controller did not report it
- `logical_state: IoSignalLogicalState`: Logical state of the signal (simulated or not)
- `physical_state: IoSignalPhysicalState`: Physical state of the signal. Only reported when reading a single signal with IoService.GetSignal().
- `physical_value: float | None`: Physical value of the signal, null when the controller did not report it. Only reported by IoService.GetSignal() and IoService.SearchSignalsExtended().
- `logical_time_seconds: int | None`: Seconds part of the global time at which the logical value was updated, null when not reported
- `logical_time_microseconds: int | None`: Microseconds part of the global time at which the logical value was updated, null when not reported
- `physical_time_seconds: int | None`: Seconds part of the global time at which the physical value was updated, null when not reported
- `physical_time_microseconds: int | None`: Microseconds part of the global time at which the physical value was updated, null when not reported
- `quality: str`: Quality of the signal, reported as a numeric code by IoService.GetSignal() and as a textual value (for example "good") by IoService.SearchSignalsExtended()
- `write_access_level: str`: Access level required to write the signal, for example "None". Only reported by IoService.SearchSignalsExtended().

**IoSignalType** ([reference](../api/underautomation.abb.rws.data.md#iosignaltype))

- Unknown: The signal type could not be determined
- DigitalOutput: Digital output
- DigitalInput: Digital input
- AnalogOutput: Analog output
- AnalogInput: Analog input
- GroupInput: Group input
- GroupOutput: Group output

**IoSignalConfiguration** ([reference](../api/underautomation.abb.rws.data.md#iosignalconfiguration))

- `IoSignalConfiguration()`: Initializes a new instance of the IoSignalConfiguration class
- `signal_name: str`: Name of the signal, for example "DRV1CHAIN2"
- `signal_bits: int | None`: Number of bits of the signal, null when not reported
- `rapid: bool | None`: Whether a RAPID client can write the signal in both manual and auto mode
- `local_manual: bool | None`: Whether a local client can write the signal in manual mode
- `local_auto: bool | None`: Whether a local client can write the signal in auto mode
- `remote_manual: bool | None`: Whether a remote client can write the signal in manual mode
- `remote_auto: bool | None`: Whether a remote client can write the signal in auto mode
- `set_by_device_transfer: bool | None`: Whether the bits of this signal are set by a device transfer operation. Not reported by every controller, null when absent from the response.

**IoSignalSearchCriteria** ([reference](../api/underautomation.abb.rws.data.md#iosignalsearchcriteria))

- `IoSignalSearchCriteria()`: Initializes a new instance of the IoSignalSearchCriteria class
- `name: str`: Name of the searched signals
- `device_name: str`: Name of the device the searched signals are connected to
- `network_name: str`: Name of the network the searched signals belong to
- `category: str`: Category of the searched signals, for example "safety"
- `category_prefix: str`: Category prefix of the searched signals
- `type: IoSignalType | None`: Type of the searched signals, null to search every type
- `invert: bool | None`: Whether the criteria is inverted: the signals matching it are excluded from the result
- `blocked: bool | None`: Whether only the blocked (simulated) signals are searched
