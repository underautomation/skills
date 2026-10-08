# Read and write variables

Exchange data with a Yaskawa job from C# or Python: integer, real, byte and string variables, which type to choose, and the frequent errors.

Web page: https://underautomation.com/yaskawa/documentation/how-to-read-write-variables

This article shows how to exchange data between a PC and a job of a Yaskawa Motoman controller, in C# or Python, with the variables of the controller. It gives a complete program that reads a counter and writes offsets, a recipe number and a reference.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- The job uses the variables that the PC reads and writes. Agree on the numbers of these variables with the author of the job.

## Which variable to choose

| Data                                  | Variable | Methods                                         |
| ------------------------------------- | -------- | ----------------------------------------------- |
| A flag, a small number (0 to 255)     | `B`      | `ReadByte`, `WriteByte`                         |
| A counter, an index (-32768 to 32767) | `I`      | `ReadInteger`, `WriteInteger`                   |
| A large integer                       | `D`      | `ReadDoubleInteger`, `WriteDoubleInteger`       |
| A measure, an offset in mm            | `R`      | `ReadReal`, `WriteReal`                         |
| A text, a reference                   | `S`      | `Read16BytesChar`, `Write16BytesChar`           |
| A position                            | `P`      | `ReadPositionVariable`, `WritePositionVariable` |

Each method reads or writes several variables in a row, in one request.

## Example

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Integer I000: a part counter written by the job
count = robot.high_speed_e_server.read_integer(0, 1).value[0]
print(f"Parts: {count}")

# Real R000 and R001: offsets used by the job, in mm
robot.high_speed_e_server.write_real(0, [2.5, -1.0])

# Byte B000 and B001: a recipe number and a flag
robot.high_speed_e_server.write_byte(0, [7, 1])

# String S000: the reference of the part
robot.high_speed_e_server.write16_bytes_char(0, ["REF-2026-118"])

# Check what the controller stored
b = robot.high_speed_e_server.read_byte(0, 2).value
r = robot.high_speed_e_server.read_real(0, 2).value
print(f"B000={b[0]} B001={b[1]} R000={r[0]} R001={r[1]}")

robot.disconnect()
```

The program:

1. reads `I000`, a counter of the job;
2. writes two offsets in `R000` and `R001`;
3. writes a recipe number and a flag in `B000` and `B001`;
4. writes a reference in `S000`;
5. reads the variables back to check them.

## A handshake with the job

A job and a PC read and write the same variables at the same time. Use one variable as a flag: the PC writes the data, then sets the flag. The job waits for the flag, reads the data, then clears the flag. The PC waits for the cleared flag before it writes again.

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) reads and writes the B, I, D, R and S variables with the same method names, over TCP. It returns the values directly, as arrays. The P variables are not available through the Ethernet Server.

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

## Troubleshooting

- **`InvalidDataAnswerException` on a variable number:** the number is out of the range of the controller. The ranges depend on the controller and on its settings.
- **A text is cut:** a 16 byte string keeps 16 characters. Use the 32 byte strings when the controller has them.

## What to read next

- [Variables and registers](hses-variables.md): all the variable types, including positions.
- [Run a job](how-to-run-program.md).
