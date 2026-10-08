# Inputs and outputs

List the physical I/O of a Staubli controller, read several I/O in one request and write outputs, without a VAL 3 program.

Web page: https://underautomation.com/staubli/documentation/soap-io

This page shows how to list, read and write the physical inputs and outputs of a Staubli CS8 or CS9 controller with the SDK: digital, analog and the other I/O of the boards of the controller. No VAL 3 program is needed.

## List the I/O

`GetAllPhysicalIos()` returns every physical I/O of the controller, with its name, its type and its description.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# Every physical I/O of the controller
ios = controller.soap.get_all_physical_ios()

for io in ios:
    # type_str: din, dout, ain, serial...
    print(f"{io.name} [{io.type_str}] {io.description} lockable={io.lockable}")

controller.disconnect()
```

The name identifies the I/O in the read and write methods. It contains the board and the I/O, separated by a backslash, for example `BasicIO-1\%I0`. The boards depend on the configuration of each controller: read the names with `GetAllPhysicalIos()`, do not guess them. In C#, write the name as a verbatim string (`@"BasicIO-1\%I0"`), in Python as a raw string (`r"BasicIO-1\%I0"`).

`TypeStr` gives the type, for example `din` or `dout` for a digital input or output, `ain` for an analog input, `serial` for a serial line.

## Read I/O

`ReadIos(names)` reads several I/O in one request. It returns one `PhysicalIoState` per name, in the same order.

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.soap.data.physical_io_enum_state import PhysicalIoEnumState

controller = StaubliController()
controller.connect("192.168.0.254")

# Names as returned by get_all_physical_ios
names = [r"BasicIO-1\%I0", r"BasicIO-1\%Q0"]

# One state per name, in the same order
states = controller.soap.read_ios(names)

for name, state in zip(names, states):
    # state tells if the name exists on this controller
    if state.state != PhysicalIoEnumState.Defined:
        print(f"{name}: {state.state.name}")
        continue

    print(f"{name} = {state.value} locked={state.locked} simulated={state.simulated}")

controller.disconnect()
```

- `State` is `Defined` when the name exists, `Undefined` or `InvalidName` otherwise. Test it before you use the value.
- `Value` is a number: `0` or `1` for a digital I/O.
- `Locked` and `Simulated` tell if the I/O is locked or simulated on the controller.

## Write I/O

`WriteIos(names, values)` writes several outputs in one request. The two arrays have the same length.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

names = [r"BasicIO-1\%Q0", r"BasicIO-1\%Q1"]

# One value per name. Digital outputs: 1 is on, 0 is off
values = [1.0, 0.0]

responses = controller.soap.write_ios(names, values)

for name, response in zip(names, responses):
    if not response.found:
        print(f"{name}: unknown name")
    elif not response.success:
        print(f"{name}: write refused")

controller.disconnect()
```

The answer has one `PhysicalIoWriteResponse` per name:

- `Found` is `false` when the name does not exist.
- `Success` is `false` when the controller refused the write, for example for an input.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/underautomation.staubli.soap.internal.md#soapclientbase-controllersoap))

- `get_all_physical_ios() -> typing.List[PhysicalIo]`: Get all the physical I/O values of the controller
- `read_ios(ios: typing.List[str]) -> typing.List[PhysicalIoState]`: Read the state of specified physical I/Os
- `write_ios(ios: typing.List[str], values: typing.List[float]) -> typing.List[PhysicalIoWriteResponse]`: Write values to specified physical I/Os

**PhysicalIo** ([reference](../api/underautomation.staubli.soap.data.md#physicalio))

- `PhysicalIo()`
- `name: str`: Name of the physical I/O.
- `description: str`: Description of the physical I/O.
- `type_str: str`: Type of the physical I/O (e.g., din, dout, ain, serial, ...).
- `lockable: bool`: Indicates whether the physical I/O is lockable.

**PhysicalIoState** ([reference](../api/underautomation.staubli.soap.data.md#physicaliostate))

- `PhysicalIoState()`: Initializes a new instance of the PhysicalIoState class.
- `state: PhysicalIoEnumState`: Definition state of the I/O.
- `locked: bool`: Indicates whether the I/O is locked.
- `simulated: bool`: Indicates whether the I/O is in simulation mode.
- `value: float`: Current numeric value of the I/O.
- `attribute: PhysicalIoAttribute`: I/O type-specific attributes (analog or digital).

**PhysicalIoEnumState** ([reference](../api/underautomation.staubli.soap.data.md#physicalioenumstate))

- Defined: The I/O is defined and available.
- Undefined: The I/O is not defined.
- InvalidName: The I/O name is invalid.

**PhysicalIoWriteResponse** ([reference](../api/underautomation.staubli.soap.data.md#physicaliowriteresponse))

- `PhysicalIoWriteResponse()`: Initializes a new instance of the PhysicalIoWriteResponse class.
- `success: bool`: Indicates whether the write operation succeeded.
- `found: bool`: Indicates whether the specified I/O was found.

**PhysicalIoAttribute** ([reference](../api/underautomation.staubli.soap.data.md#physicalioattribute))

- `PhysicalIoAttribute()`: Initializes a new instance of the PhysicalIoAttribute class.
- `aio_attribute: PhysicalAioAttribute`: Analog I/O specific attributes (null if digital).
- `dio_attribute: PhysicalDioAttribute`: Digital I/O specific attributes (null if analog).
