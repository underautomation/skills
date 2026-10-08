# Read and write I/O

Find the I/O names, wait for an input and switch an output of a Staubli CS8 or CS9 controller from C# or Python.

Web page: https://underautomation.com/staubli/documentation/how-to-read-write-io

This article shows how to read and write the inputs and outputs of a Staubli CS8 or CS9 controller from a PC, in C# or Python. It gives a complete program that finds the I/O names, waits for an input and switches an output on, without any VAL 3 program on the controller.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- To write an output, the user of the connection has the right to write it.

## Three calls

| Step                  | Method                    | Returns                                      |
| --------------------- | ------------------------- | -------------------------------------------- |
| Find the names        | `GetAllPhysicalIos()`     | Name, type and description of every I/O      |
| Read one or more I/O  | `ReadIos(names)`          | One state per name: value, locked, simulated |
| Write one or more I/O | `WriteIos(names, values)` | One answer per name: found, success          |

`ReadIos` and `WriteIos` take arrays: read or write several I/O in one request instead of one request per I/O.

## Example

```python
import time

from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# 1. Find the exact names of the I/O
for io in controller.soap.get_all_physical_ios():
    print(f"{io.name} [{io.type_str}] {io.description}")

input_name = r"BasicIO-1\%I0"
output_name = r"BasicIO-1\%Q0"

# 2. Wait for the input, at most 10 seconds
timeout = time.monotonic() + 10
while controller.soap.read_ios([input_name])[0].value == 0:
    if time.monotonic() > timeout:
        raise TimeoutError(f"{input_name} stayed off")
    time.sleep(0.05)

# 3. Switch the output on, and check the answer of the controller
response = controller.soap.write_ios([output_name], [1.0])[0]
if not response.found or not response.success:
    print(f"Write of {output_name} failed: found={response.found}")

controller.disconnect()
```

The program:

1. prints the name of every I/O, to copy the exact names into the code;
2. reads the input every 50 ms until it is on, with a timeout of 10 s;
3. writes the output, and checks that the controller found it and accepted the value.

## I/O names

A name contains the board and the I/O, separated by a backslash: `BasicIO-1\%I0`. The boards depend on the configuration of the controller, so the names of your cell can differ from the ones of this example. Always take them from `GetAllPhysicalIos()`.

Write the backslash as it is: with a verbatim string in C# (`@"BasicIO-1\%I0"`) and a raw string in Python (`r"BasicIO-1\%I0"`).

## Troubleshooting

- **`State` is `Undefined` or `InvalidName`:** the name does not exist on this controller. Compare it with the output of `GetAllPhysicalIos()`, including the case and the backslash.
- **`Found` is `true` but `Success` is `false`:** the controller refused the write. Check that the I/O is an output, and the rights of the user.
- **The value changes back:** a VAL 3 program writes the same output. Stop it, or agree on which side owns each output.

## What to read next

- [Inputs and outputs](soap-io.md): the reference of the I/O methods.
- [Monitor the state of the robot](how-to-monitor-state.md).
