# Variables and I/O

Read and write the B, I, D, R and S variables, read the I/O signals and write the network inputs of a Yaskawa controller through the Ethernet Server.

Web page: https://underautomation.com/yaskawa/documentation/eserver-variables-io

This page shows how to read and write the variables and the I/O of a Yaskawa Motoman controller through the Ethernet Server: B, I, D, R and S variables, I/O groups and network inputs. It covers the YRC1000 and YRC1000micro controllers.

## Variables

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Read 4 variables from index 0: B000 to B003, I000 to I003...
b = robot.e_server.read_byte(0, 4)
i = robot.e_server.read_integer(0, 4)
d = robot.e_server.read_double_integer(0, 4)
r = robot.e_server.read_real(0, 4)
s = robot.e_server.read16_bytes_char(0, 4)

# Write from index 10: B010 = 1, B011 = 2
robot.e_server.write_byte(10, [1, 2])
robot.e_server.write_integer(10, [-100])
robot.e_server.write_double_integer(10, [123456])
robot.e_server.write_real(10, [1.5])
robot.e_server.write16_bytes_char(10, ["PART-42"])

robot.disconnect()
```

| Variable | Read                    | Write                         | .NET type  | Range of a value                |
| -------- | ----------------------- | ----------------------------- | ---------- | ------------------------------- |
| `B`      | `ReadByte`              | `WriteByte`                   | `byte`     | 0 to 255                        |
| `I`      | `ReadInteger`           | `WriteInteger`                | `short`    | -32768 to 32767                 |
| `D`      | `ReadDoubleInteger`     | `WriteDoubleInteger`          | `int`      | -2147483648 to 2147483647       |
| `R`      | `ReadReal`              | `WriteReal`                   | `float`    | 32 bit floating point           |
| `S`      | `Read16BytesChar`       | `Write16BytesChar`            | `string`   | 16 characters                   |

Reads take `(firstIndex, count)` and return one value per variable. Writes take `(firstIndex, values)` and write the variables from `firstIndex`. The number of variables depends on the settings of the controller. An index that does not exist throws a `HostControlException`.

The position variables (P, BP, EX) are not available through the Ethernet Server: read them with the [High Speed Ethernet Server](hses-variables.md).

## Inputs and outputs

### Read the signals

`ReadIO(startAddress, count)` reads `count` bytes of signals. Each byte holds 8 signals. `startAddress` is the number of the first signal, as shown on the pendant: `10010` for `#10010`. Use a number that ends with 0, so that each byte is one group of 8 signals.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# 2 bytes from the signal #10010: #10010 to #10017, then #10020 to #10027
outputs = robot.e_server.read_io(10010, 2)
print(f"#10010: {outputs.get_bit(0)}, #10011: {outputs.get_bit(1)}")
print(f"#10020 to #10027: {outputs.data[1]}")

# Network inputs #27010 to #27017: bits 0 and 2 on (value 5)
robot.e_server.write_io(27010, [5])

robot.disconnect()
```

`Data[0]` holds `#10010` to `#10017`: bit 0 is `#10010`, bit 7 is `#10017`. `GetBit(n)` reads bit `n` of the result, from 0 for the first signal of the first byte.

| Signals            | Example number |
| ------------------ | -------------- |
| General inputs     | `#00010`       |
| General outputs    | `#10010`       |
| External inputs    | `#20010`       |
| Network inputs     | `#27010`       |
| Network outputs    | `#37010`       |
| Specific outputs   | `#50010`       |
| Auxiliary relays   | `#70010`       |

The numbers are the same as with the High Speed Ethernet Server: the full table is in [Inputs and outputs](hses-io.md#signals_groups_and_bits). The signals that exist depend on the I/O boards of the controller.

### Write the network inputs

`WriteIO(startAddress, values)` writes bytes of signals. By default, the controller accepts only the network inputs (`#27010` to `#29567`). They are the signals to use to send an order or a state to a job. A write to another signal throws a `HostControlException`.

## Reference

**Methods of HostControlClientBase** ([reference](../api/underautomation.yaskawa.host_control.internal.md#hostcontrolclientbase-robote_server))

- `read_io(startAddress: int, count: int) -> HostControlIOData`: Reads I/O signals from the robot controller. Each byte holds 8 signals.
- `write_io(startAddress: int, data: typing.List[int]) -> HostControlResponse`: Writes I/O signals to the robot controller. Each byte holds 8 signals. By default, the controller accepts only the network input signals (#27010 to #29567).
- `read_byte(firstIndex: int, count: int) -> typing.List[int]`: Reads byte (B) variables starting at the specified index.
- `write_byte(firstIndex: int, data: typing.List[int]) -> None`: Writes byte (B) variables starting at the specified index.
- `read_integer(firstIndex: int, count: int) -> typing.List[int]`: Reads integer (I) variables starting at the specified index.
- `write_integer(firstIndex: int, data: typing.List[int]) -> None`: Writes integer (I) variables starting at the specified index.
- `read_double_integer(firstIndex: int, count: int) -> typing.List[int]`: Reads double integer (D) variables starting at the specified index.
- `write_double_integer(firstIndex: int, data: typing.List[int]) -> None`: Writes double integer (D) variables starting at the specified index.
- `read_real(firstIndex: int, count: int) -> typing.List[float]`: Reads real (R) variables starting at the specified index.
- `write_real(firstIndex: int, data: typing.List[float]) -> None`: Writes real (R) variables starting at the specified index.
- `read16_bytes_char(firstIndex: int, count: int) -> typing.List[str]`: Reads 16-byte string (S) variables starting at the specified index.
- `write16_bytes_char(firstIndex: int, data: typing.List[str]) -> None`: Writes 16-byte string (S) variables starting at the specified index.

**HostControlIOData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontroliodata))

- `get_bit(bitOffset: int) -> bool`: Gets the bit value at the specified offset from the start address.
- `start_address: int (read only)`: Gets or sets the starting I/O contact number.
- `count: int (read only)`: Gets or sets the number of I/O bytes read.
- `data: typing.List[int] (read only)`: Gets or sets the I/O data bytes.
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## What to read next

- [Read and write variables](how-to-read-write-variables.md): which protocol and which variable type to choose.
- [Read and write I/O](how-to-read-write-io.md): switch a network input and wait for an output.
