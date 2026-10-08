# Read and write registers

Exchange values between a UR robot program and a PC with the boolean, integer and float registers, with RTDE up to 500 Hz.

Web page: https://underautomation.com/universal-robots/documentation/registers

This article shows how to exchange values between a program that runs on a Universal Robots cobot and a PC, with the general purpose registers, in C# or Python. The registers are read and written while the program runs, up to 500 times per second with RTDE.

## The registers

A UR controller has three types of registers, each as inputs and as outputs:

| Type    | Content                 | Numbers  | Fieldbus | RTDE      |
| ------- | ----------------------- | -------- | -------- | --------- |
| Boolean | `true` or `false`       | 0 to 127 | 0 to 63  | 64 to 127 |
| Integer | 32 bit signed integer   | 0 to 47  | 0 to 23  | 24 to 47  |
| Float   | Floating point number   | 0 to 47  | 0 to 23  | 24 to 47  |

The names are given from the point of view of the robot:

- **input registers:** written by an external system (RTDE, fieldbus), read by the program;
- **output registers:** written by the program, read by an external system.

Use the RTDE half (24 to 47, 64 to 127) when a fieldbus also uses the registers.

## In the robot program

| Task                     | URScript                                                                                                       |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Read an input register   | `read_input_boolean_register(n)`, `read_input_integer_register(n)`, `read_input_float_register(n)`             |
| Read an output register  | `read_output_boolean_register(n)`, `read_output_integer_register(n)`, `read_output_float_register(n)`          |
| Write an output register | `write_output_boolean_register(n, value)`, `write_output_integer_register(n, value)`, `write_output_float_register(n, value)` |

A program cannot write an input register.

## Which way to choose

| Way               | Reads           | Writes                         | Frequency          |
| ----------------- | --------------- | ------------------------------ | ------------------ |
| RTDE              | All registers   | Input registers                | Up to 500 Hz       |
| Primary Interface | no              | Output registers, with URScript | When you send it  |

RTDE is the way for both directions. The Primary Interface writes an output register with URScript: in a secondary program (`sec`), the running program does not stop.

## Read with RTDE

Add the registers to the outputs of the RTDE setup, with their number. The bits 0 to 63 are read as two 32 bit integers (`InputBitRegisters0To31`, `InputBitRegisters32To63`), the bits 64 to 127 one by one.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData

robot = UR()

parameters = ConnectParameters("192.168.0.1")
parameters.rtde.enable = True
parameters.rtde.frequency = 500

# Input registers
parameters.rtde.output_setup.add(RtdeOutputData.InputBitRegisters0To31)  # 32 bits in one integer
parameters.rtde.output_setup.add(RtdeOutputData.InputBitRegisters32To63)
parameters.rtde.output_setup.add(RtdeOutputData.InputBitRegisters, 64)  # one by one, 64 to 127
parameters.rtde.output_setup.add(RtdeOutputData.InputIntRegisters, 24)
parameters.rtde.output_setup.add(RtdeOutputData.InputDoubleRegisters, 24)

# Output registers
parameters.rtde.output_setup.add(RtdeOutputData.OutputBitRegisters0To31)
parameters.rtde.output_setup.add(RtdeOutputData.OutputBitRegisters32To63)
parameters.rtde.output_setup.add(RtdeOutputData.OutputBitRegisters, 64)
parameters.rtde.output_setup.add(RtdeOutputData.OutputIntRegisters, 24)
parameters.rtde.output_setup.add(RtdeOutputData.OutputDoubleRegisters, 24)

robot.connect(parameters)

def on_data(sender, e):
    values = robot.rtde.output_data_values

    input_bits_0_to_31 = values.input_bit_registers0_to31
    input_bit64 = values.input_bit_registers.x64
    input_int24 = values.input_int_registers.x24
    input_double24 = values.input_double_registers.x24

    output_bits_0_to_31 = values.output_bit_registers0_to31
    output_bit64 = values.output_bit_registers.x64
    output_int24 = values.output_int_registers.x24
    output_double24 = values.output_double_registers.x24

robot.rtde.output_data_received(on_data)
```

## Write with RTDE

Add the input registers to the inputs of the RTDE setup, then write them with `WriteInputs`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_input_data import RtdeInputData
from underautomation.universal_robots.rtde.rtde_input_values import RtdeInputValues

robot = UR()

parameters = ConnectParameters("192.168.0.1")
parameters.rtde.enable = True

# Only input registers can be written with RTDE
parameters.rtde.input_setup.add(RtdeInputData.InputBtRegisters32To63)
parameters.rtde.input_setup.add(RtdeInputData.InputBitRegisters, 64)
parameters.rtde.input_setup.add(RtdeInputData.InputIntRegisters, 24)
parameters.rtde.input_setup.add(RtdeInputData.InputDoubleRegisters, 24)

robot.connect(parameters)

inputs = RtdeInputValues()
inputs.input_bt_registers32_to63 = 0xCA  # bits 32 to 63 in one integer
inputs.input_bit_registers.x64 = True
inputs.input_int_registers.x24 = 2
inputs.input_double_registers.x24 = 3.14

robot.rtde.write_inputs(inputs)
```

## Write an output register with URScript

```python
from underautomation.universal_robots.ur import UR

robot = UR()

robot.connect("192.168.0.1")

# One line: the running program stops
robot.primary_interface.script.send("write_output_float_register(0, 1.5)")

# In a secondary program: the running program continues
robot.primary_interface.script.send(
    "sec writeRegister():\n"
    "  write_output_float_register(0, 1.5)\n"
    "end\n")
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## What to read next

- [RTDE](rtde.md): the setup, the frequency and the events.
- [Read and write variables](variables.md): the program and installation variables.
