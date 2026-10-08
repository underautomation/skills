# Read and write I/O

Switch a network input and wait for an output of a Yaskawa controller from C# or Python, with the signal numbers, groups and bits explained.

Web page: https://underautomation.com/yaskawa/documentation/how-to-read-write-io

This article shows how to read and write the inputs and outputs of a Yaskawa Motoman controller from a PC, in C# or Python. It gives a complete program that sets a network input, waits for a general output, then clears the input.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- The job or the ladder of the controller uses the network inputs that the PC writes.

## Three calls

| Step                       | Method                                 | Note                                   |
| -------------------------- | -------------------------------------- | -------------------------------------- |
| Read one or more groups    | `ReadIO(IOType, group, count)`         | One byte per group, one bit per signal |
| Write network input groups | `WriteIoNetworkInput(group, bytes)`    | One byte per group                     |
| Number of a signal         | `IoHelpers.ConvertIOGroupToBitAddress` | `#10013` = group 1001, bit 3           |

The PC writes only the network inputs. To act on the cell, the job or the ladder of the controller reads them and switches its outputs.

## Example

```python
import time
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.common.io_type import IOType

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# 1. Signal #27013: bit 3 of group 1 of the network inputs
group = 1
bit = 3

# 2. Set the bit, keep the other bits of the group
current = robot.high_speed_e_server.read_io(IOType.NetworkInput, group, 1).value[0]
next_value = current | (1 << bit)
robot.high_speed_e_server.write_io_network_input(group, [next_value])

# 3. Wait for the general output #10010 (bit 0 of group 1), at most 10 seconds
timeout = time.monotonic() + 10
while (robot.high_speed_e_server.read_io(IOType.GeneralOutput, 1, 1).value[0] & 1) == 0:
    if time.monotonic() > timeout:
        raise TimeoutError("#10010 stayed off")
    time.sleep(0.05)

# 4. Clear the network input
robot.high_speed_e_server.write_io_network_input(group, [next_value & ~(1 << bit)])

robot.disconnect()
```

The program:

1. takes the signal `#27013`: bit 3 of the group 1 of the network inputs;
2. reads the group, sets the bit and writes the group back, so that the other bits keep their state;
3. reads the general output `#10010` every 50 ms until it is on, with a timeout of 10 s;
4. clears the bit.

## Signal numbers

A signal number has 5 digits: the group, then the bit. The group of a type starts at a fixed number: `1` for the general inputs, `1001` for the general outputs, `2701` for the network inputs. The table of every type is in [Inputs and outputs](hses-io.md#signals_groups_and_bits).

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) reads and writes the same signals over TCP. `ReadIO` and `WriteIO` take the number of the first signal, as shown on the pendant (`27010` for `#27010`), and a number of bytes.

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

## Troubleshooting

- **The write is refused:** the PC can write only the network inputs. Use a network input and let the ladder copy it to an output.
- **The bit does not change on the pendant:** check that you test the right bit. The bit 0 is the signal ending with `0`.

## What to read next

- [Inputs and outputs](hses-io.md): the I/O types and the reference.
- [Monitor the state of the robot](how-to-monitor-state.md).
