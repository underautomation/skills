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

`LogicalValue` is the value seen by the RAPID programs, `PhysicalValue` the one on the hardware. They differ when the signal is simulated. `LogicalState` says whether it is simulated, `PhysicalState` whether the physical value is valid.

A controller usually declares several hundreds of signals, so `GetSignals` returns a large answer. Prefer `SearchSignals` when you only need part of them.

### Write a signal

`SetSignalValue` writes the logical value of a signal. The value is a `float`, which covers the digital, the analog and the group signals with one method.

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

Writing a signal needs no mastership, but the user account needs the write access on it, and the signal must accept a write from a remote client in the current operating mode. That is what `GetSignalConfiguration` reports, see below. The controller refuses the write with an `RwsException` when the signal is read only or when the value is outside its range.

`SetSignalValueDelayed` asks the controller to apply the value after a delay in milliseconds. The call returns immediately, the controller does the waiting.

### Pulse, toggle and invert

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

Only the digital and the group signals can be pulsed, toggled or inverted, an analog signal is refused. The three methods take a value even though they compute the written value themselves, because the controller rejects a write that carries none. Leave the two pulse lengths null to use the ones configured on the controller.

### Simulate a signal

A simulated signal keeps the value written by the client and stops following its device. This is how an input is forced during a test, without any wiring.

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

`SetSignalState` only turns the simulation on and off, the value is still written with `SetSignalValue`. `UnblockSignals` stops the simulation of every simulated signal of the controller at once, which is a good thing to call at the end of a test run.

### Search signals

`SearchSignals` narrows the result down with an `IoSignalSearchCriteria`. Every property of the criteria is optional, and an empty criteria matches every signal.

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

`SearchSignalsExtended` returns the same signals with their physical value, their time stamps, their quality and their write access level. It costs more on the controller, so use the simple search when the logical value is enough.

A second criteria can be passed. A signal is returned only when it matches both. Set `Invert` on one of the two to exclude what it matches, otherwise the result is the same as with a single criteria. `start` and `limit` page through a long result.

### Signal configuration

`GetSignalConfiguration` reports how the signal was declared in the I/O configuration of the controller: its width in bits, and who is allowed to write it.

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

`Rapid`, `LocalManual`, `LocalAuto`, `RemoteManual` and `RemoteAuto` are the write rights. Your application is a remote client, so `RemoteAuto` and `RemoteManual` are the two to check before a write. A write refused by the configuration gives an `RwsException`, not a silent failure.

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

**IoSignalType** ([reference](../api/underautomation.abb.rws.data.md#iosignaltype))

- Unknown: The signal type could not be determined
- DigitalOutput: Digital output
- DigitalInput: Digital input
- AnalogOutput: Analog output
- AnalogInput: Analog input
- GroupInput: Group input
- GroupOutput: Group output

**IoSignalLogicalState** ([reference](../api/underautomation.abb.rws.data.md#iosignallogicalstate))

- Unknown: The logical state could not be determined
- Simulated: The signal is simulated: its logical value is forced and no longer follows the physical value
- NotSimulated: The signal is not simulated

**IoSignalPhysicalState** ([reference](../api/underautomation.abb.rws.data.md#iosignalphysicalstate))

- Unknown: The physical state could not be determined
- Valid: The physical value of the signal is valid
- Invalid: The physical value of the signal is not valid

## I/O devices

A device is a physical or a virtual I/O board. `GetDevices` lists them all, `GetDevice` reads one with its input and output data.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.io_device_logical_state import IoDeviceLogicalState

robot = AbbController()
robot.connect("192.168.0.1")

# Every device of every network
devices = robot.rws.io.get_devices()

for item in devices:
    print(f"{item.path} ({item.type}) {item.physical_state} {item.logical_state}")

# One device, with its input and output data
device = robot.rws.io.get_device("Local", "Board10")
print(device.address)
print(device.input_data)
print(device.output_data)

# Number of bits and write rights of the device
config = robot.rws.io.get_device_configuration("Local", "Board10")
print(f"{config.input_bits} input bits, {config.output_bits} output bits")

# Disable a device, then enable it again
robot.rws.io.set_device_state("Local", "Board10", IoDeviceLogicalState.Disabled)
robot.rws.io.set_device_state("Local", "Board10", IoDeviceLogicalState.Enabled)

# Search by name, by logical state, or by both, optionally inside one network
enabled = robot.rws.io.search_devices(None, IoDeviceLogicalState.Enabled, "Local")

# Force the first input byte of a device, on a virtual controller only.
# The mask selects the written bits, here the two lowest ones.
robot.rws.io.set_device_input_data("Local", "Board10", 0, 0x03, 0x03)
robot.rws.io.set_device_output_data("Local", "Board10", 0, 0x01, 0x01)

# Firmware state of a device and of its modules, on a real controller only
upgrade = robot.rws.io.get_device_upgrade_info("EtherNetIP", "Local_IO")
print(f"{upgrade.state} {upgrade.status} {upgrade.module_count} modules")

for module in upgrade.modules:
    print(f"{module.index} {module.program_name} {module.serial_number}")

# Send a command to a device, on a real controller only.
# The last two arguments are the length of the value and the timeout in milliseconds.
robot.rws.io.send_device_command("EtherNetIP", "Local_IO", "FIRMWARE_INFO", "", 0, 5000)

robot.disconnect()
```

`PhysicalState` is the state of the hardware: `Running`, `Error`, `Unconnected`, `Unconfigured`, `Deactivated`, `Startup`, `Init` or `Halted`. `LogicalState` is what the controller was asked to do with the device, `Enabled` or `Disabled`, and `SetDeviceState` changes it. Disabling a device stops its signals from being updated.

`GetDeviceConfiguration` reports the number of input and output bits of the device and the same write rights as for a signal.

Three methods depend on the kind of controller:

- `SetDeviceInputData` and `SetDeviceOutputData` force one byte of the data of a device, on a virtual controller only. The mask selects the written bits, a bit at zero is left unchanged. A real controller refuses the request.
- `GetDeviceUpgradeInfo` reports the firmware state of a device and of its modules, on a real controller only.
- `SendDeviceCommand` sends a command to a device, on a real controller only. `valueLength` is used on an IRC5, an OmniCore computes it from the value itself and ignores the argument.

**Methods of IoService** ([reference](../api/underautomation.abb.rws.services.md#ioservice-robotrwsio))

- `get_devices() -> typing.List[IoDeviceItem]`: Gets every I/O device defined in the controller (synchronous)
- `get_device(network: str, device: str) -> IoDeviceItem`: Gets a single I/O device, including its input and output data (synchronous)
- `search_devices(name: str=None, logicalState: IoDeviceLogicalState | None=None, network: str=None) -> typing.List[IoDeviceItem]`: Searches the I/O devices matching a name and/or a logical state (synchronous)
- `get_device_configuration(network: str, device: str) -> IoDeviceConfiguration`: Gets the runtime configuration properties of an I/O device (synchronous)
- `get_device_upgrade_info(network: str, device: str) -> IoDeviceUpgradeInfo`: Gets the firmware upgrade status of an I/O device and of each of its modules (synchronous) Only available on a real controller.
- `set_device_state(network: str, device: str, logicalState: IoDeviceLogicalState) -> None`: Enables or disables an I/O device (synchronous)
- `set_device_input_data(network: str, device: str, startByte: int, signalData: int, dataMask: int) -> None`: Writes one byte of the input data of an I/O device (synchronous) Only supported on a virtual controller.
- `set_device_output_data(network: str, device: str, startByte: int, signalData: int, dataMask: int) -> None`: Writes one byte of the output data of an I/O device (synchronous) Only supported on a virtual controller.
- `send_device_command(network: str, device: str, commandName: str, value: str, valueLength: int, timeout: int) -> None`: Sends a command to an I/O device (synchronous) Only available on a real controller.

**IoDeviceItem** ([reference](../api/underautomation.abb.rws.data.md#iodeviceitem))

- `IoDeviceItem()`: Initializes a new instance of the IoDeviceItem class
- `name: str`: Name of the device, for example "DRV_1" or "PANEL"
- `network_name: str`: Name of the network the device is connected to, for example "Local"
- `path: str`: Full path of the device, "{network}/{device}" (for example "Local/DRV_1")
- `type: str`: Type of the device, for example "DRV_1_TYPE". Not reported by every controller, null when absent. A virtual controller leaves it out.
- `physical_state: IoDevicePhysicalState`: Physical state of the device
- `logical_state: IoDeviceLogicalState`: Logical state of the device
- `address: str`: Address of the device on its network, "-" when the network has no addressing
- `input_data: str`: Input data of the device, as an hexadecimal string (for example "1FFFE063"). Only reported when reading a single device with IoService.GetDevice().
- `input_mask: str`: Input mask of the device, as an hexadecimal string. A bit set to zero is an input bit that is not written. Only reported when reading a single device with IoService.GetDevice().
- `output_data: str`: Output data of the device, as an hexadecimal string (for example "0000000E"). Only reported when reading a single device with IoService.GetDevice().
- `output_mask: str`: Output mask of the device, as an hexadecimal string. A bit set to zero is an output bit that is not written. Only reported when reading a single device with IoService.GetDevice().

**IoDeviceConfiguration** ([reference](../api/underautomation.abb.rws.data.md#iodeviceconfiguration))

- `IoDeviceConfiguration()`: Initializes a new instance of the IoDeviceConfiguration class
- `device_name: str`: Name of the device, for example "DN_Internal_Device"
- `network_name: str`: Name of the industrial network the device belongs to, for example "DeviceNet"
- `input_bits: int | None`: Number of input bits of the device, null when not reported
- `output_bits: int | None`: Number of output bits of the device, null when not reported
- `rapid: bool | None`: Whether a RAPID client can access the device in both manual and auto mode
- `local_manual: bool | None`: Whether a local client can access the device in manual mode
- `local_auto: bool | None`: Whether a local client can access the device in auto mode
- `remote_manual: bool | None`: Whether a remote client can access the device in manual mode
- `remote_auto: bool | None`: Whether a remote client can access the device in auto mode
- `device_address: str`: Address of the device on its network, "-" when the network has no addressing
- `deny_deactivate: bool | None`: Whether deactivating the device is denied

**IoDeviceUpgradeInfo** ([reference](../api/underautomation.abb.rws.data.md#iodeviceupgradeinfo))

- `IoDeviceUpgradeInfo()`: Initializes a new instance of the IoDeviceUpgradeInfo class
- `state: IoFirmwareUpgradeState`: Overall progress of the firmware upgrade of the device
- `status: IoFirmwareUpgradeStatus`: Overall result of the firmware upgrade of the device
- `modules: typing.List[IoFirmwareModuleInfo]`: Firmware status of each module of the device, empty when the controller reported none
- `module_count: int (read only)`: Number of modules reported by the controller

**IoFirmwareModuleInfo** ([reference](../api/underautomation.abb.rws.data.md#iofirmwaremoduleinfo))

- `IoFirmwareModuleInfo()`: Initializes a new instance of the IoFirmwareModuleInfo class
- `index: str`: Index of the module inside the device ("0", "1", ...)
- `state: IoFirmwareUpgradeState`: Progress of the firmware upgrade of this module
- `status: IoFirmwareUpgradeStatus`: Result of the firmware upgrade of this module
- `program_name: str`: Name of the program installed on the module, for example "A_HYPIOM_B_3_8"
- `serial_number: str`: Serial number of the module
- `hardware_revision: str`: Hardware revision of the module, for example "C.1"
- `latest_program_name_available: str`: Name of the latest program available for the module

**IoDeviceLogicalState** ([reference](../api/underautomation.abb.rws.data.md#iodevicelogicalstate))

- Unknown: The logical state could not be determined
- Enabled: The device is enabled
- Disabled: The device is disabled

**IoDevicePhysicalState** ([reference](../api/underautomation.abb.rws.data.md#iodevicephysicalstate))

- Unknown: The physical state could not be determined
- Deactivated: The device is deactivated
- Running: The device is running
- Error: The device reports an error
- Unconnected: The device is not connected
- Unconfigured: The device is not configured
- Startup: The device is starting up
- Init: The device is initializing
- Halted: The device is halted

**IoFirmwareUpgradeState** ([reference](../api/underautomation.abb.rws.data.md#iofirmwareupgradestate))

- Unknown: The state is unknown, or could not be parsed
- Automatic: The upgrade is performed automatically
- Manual: The upgrade has to be started manually
- Info: The firmware information is being collected
- Allocate: The upgrade resources are being allocated
- Start: The upgrade is starting
- Running: The upgrade is running
- RunningStartReceived: The device acknowledged the start of the upgrade
- RunningCheckInProgress: The firmware is being checked
- RunningEraseInProgress: The device memory is being erased
- RunningBurnInProgress: The firmware is being written to the device
- RunningEndReceived: The device acknowledged the end of the upgrade
- Check: The upgraded firmware is being verified
- Deallocate: The upgrade resources are being released
- Finished: The upgrade is finished

**IoFirmwareUpgradeStatus** ([reference](../api/underautomation.abb.rws.data.md#iofirmwareupgradestatus))

- Unknown: The controller did not report a status, or it could not be parsed
- Error: The upgrade failed
- Ok: The upgrade finished, the firmware was already up to date
- Upgraded: The upgrade finished, the firmware was updated
- Pending: The upgrade is pending

## I/O networks

A network groups the devices connected the same way. `Local` is the internal network of the controller, a fieldbus such as EtherNet/IP or PROFINET is another one.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.io_client_action import IoClientAction
from underautomation.abb.rws.data.io_network_configuration_type import IoNetworkConfigurationType
from underautomation.abb.rws.data.io_network_logical_state import IoNetworkLogicalState
from underautomation.abb.rws.data.io_network_physical_state import IoNetworkPhysicalState

robot = AbbController()
robot.connect("192.168.0.1")

# Every network of the controller
networks = robot.rws.io.get_networks()

for item in networks:
    print(f"{item.name}: {item.physical_state}, {item.logical_state}")

network = robot.rws.io.get_network("Local")

config = robot.rws.io.get_network_configuration("Local")
print(f"{config.network_name} {config.network_type} {config.network_address}")

# Stop a network, then start it again. Every device of the network follows.
robot.rws.io.set_network_state("Local", IoNetworkLogicalState.Stopped)
robot.rws.io.set_network_state("Local", IoNetworkLogicalState.Started)

# Search by name, by physical state, or by both
running = robot.rws.io.search_networks(None, IoNetworkPhysicalState.Running)

# Run the auto configuration of a fieldbus network.
# This rewrites the I/O configuration and cannot be undone.
action = robot.rws.io.set_network_configuration_type("DeviceNet", IoNetworkConfigurationType.Scan)

if action == IoClientAction.Restart:
    print("Restart the controller to apply the new configuration")

# Names of the I/O resources the controller exposes
resources = robot.rws.io.get_resources()

robot.disconnect()
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

**Methods of IoService** ([reference](../api/underautomation.abb.rws.services.md#ioservice-robotrwsio))

- `get_networks() -> typing.List[IoNetworkItem]`: Gets every I/O network defined in the controller (synchronous)
- `get_network(network: str) -> IoNetworkItem`: Gets a single I/O network (synchronous)
- `search_networks(name: str=None, physicalState: IoNetworkPhysicalState | None=None) -> typing.List[IoNetworkItem]`: Searches the I/O networks matching a name and/or a physical state (synchronous)
- `get_network_configuration(network: str) -> IoNetworkConfiguration`: Gets the runtime configuration properties of an I/O network (synchronous)
- `set_network_configuration_type(network: str, configurationType: IoNetworkConfigurationType) -> IoClientAction`: Runs the auto configuration of an I/O network (synchronous)
- `set_network_state(network: str, logicalState: IoNetworkLogicalState) -> None`: Starts or stops an I/O network (synchronous)

**IoNetworkItem** ([reference](../api/underautomation.abb.rws.data.md#ionetworkitem))

- `IoNetworkItem()`: Initializes a new instance of the IoNetworkItem class
- `name: str`: Name of the network, for example "Local", "Virtual" or "EtherNetIP"
- `path: str`: Full path of the network, which is its name for a network (for example "Local")
- `physical_state: IoNetworkPhysicalState`: Physical state of the network
- `logical_state: IoNetworkLogicalState`: Logical state of the network

**IoNetworkConfiguration** ([reference](../api/underautomation.abb.rws.data.md#ionetworkconfiguration))

- `IoNetworkConfiguration()`: Initializes a new instance of the IoNetworkConfiguration class
- `network_name: str`: Name of the network, for example "Local"
- `network_type: str`: Type of the network, for example "Local" or "LOC"
- `network_address: str`: Industrial network address, "-" when the network has no addressing

**IoNetworkLogicalState** ([reference](../api/underautomation.abb.rws.data.md#ionetworklogicalstate))

- Unknown: The logical state could not be determined
- Started: The network is started
- Stopped: The network is stopped

**IoNetworkPhysicalState** ([reference](../api/underautomation.abb.rws.data.md#ionetworkphysicalstate))

- Unknown: The physical state could not be determined
- Halted: The network is halted
- Running: The network is running
- Error: The network reports an error
- Startup: The network is starting up
- Init: The network is initializing

**IoNetworkConfigurationType** ([reference](../api/underautomation.abb.rws.data.md#ionetworkconfigurationtype))

- Bits: Configure the signals of the network
- Groups: Configure the signal groups of the network
- Both: Configure both the signals and the signal groups
- Scan: Scan the network for connected devices
- Units: Configure the devices of the network

**IoClientAction** ([reference](../api/underautomation.abb.rws.data.md#ioclientaction))

- Unknown: The controller did not report any client action. Always returned when connected with version 1, which does not report this information.
- None_: Nothing to do
- Info: The user should be informed of the configuration result
- Restart: The controller has to be restarted for the configuration to take effect

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).
