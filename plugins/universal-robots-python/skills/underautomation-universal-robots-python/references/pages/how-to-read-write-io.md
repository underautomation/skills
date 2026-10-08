# Read and write I/O

Read and write the digital and analog I/O of a UR cobot in C# or Python, with RTDE and its masks, or with the Primary Interface.

Web page: https://underautomation.com/universal-robots/documentation/how-to-read-write-io

This article shows how to read and write the digital and analog I/O of a Universal Robots cobot from a PC, in C# or Python. It compares RTDE, the Primary Interface and URScript, and gives a complete program.

## The I/O of the controller

| I/O                    | Numbers | RTDE bits |
| ---------------------- | ------- | --------- |
| Standard digital       | 0 to 7  | 0 to 7    |
| Configurable digital   | 0 to 7  | 8 to 15   |
| Tool digital           | 0 to 1  | 16 to 17  |
| Standard analog        | 0 to 1  |           |
| Tool analog            | 0 to 1  |           |

## Which way to choose

| Way               | Read                                                     | Write                                                              | Frequency     |
| ----------------- | -------------------------------------------------------- | ------------------------------------------------------------------ | ------------- |
| RTDE              | `ActualDigitalInputBits`, `ActualDigitalOutputBits`, `StandardAnalogInput0`... | `StandardDigitalOutput`, `ConfigurableDigitalOutput`, `StandardAnalogOutput0`..., with a mask | Up to 500 Hz |
| Primary Interface | `MasterboardData.DigitalInputs`, `DigitalOutputs`, `AnalogInput0`..., `ToolData` | URScript `set_standard_digital_out`... in a secondary program     | 10 Hz         |

RTDE is the way for a fast or frequent access. The Primary Interface needs no setup: it is enabled by default.

## Prerequisites

- The service `RTDE` (or `Primary Client Interface`) is enabled on the robot: see [Prepare the robot](connect.md#prepare_the_robot).
- To write, the robot is in remote control on e-Series and PolyScope X.
- When the robot program also writes an output, decide which side owns it: the last write wins.

## Example

The program reads the inputs with RTDE, sets output 2 and resets output 5, then does the same with URScript.

```python
import time
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_input_data import RtdeInputData
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData
from underautomation.universal_robots.rtde.rtde_input_values import RtdeInputValues

robot = UR()

parameters = ConnectParameters("192.168.0.1")
parameters.rtde.enable = True
parameters.rtde.frequency = 125

# Read: bits 0-7 standard, 8-15 configurable, 16-17 tool
parameters.rtde.output_setup.add(RtdeOutputData.ActualDigitalInputBits)
parameters.rtde.output_setup.add(RtdeOutputData.ActualDigitalOutputBits)
parameters.rtde.output_setup.add(RtdeOutputData.StandardAnalogInput0)

# Write: a mask selects the outputs, a value sets them
parameters.rtde.input_setup.add(RtdeInputData.StandardDigitalOutputMask)
parameters.rtde.input_setup.add(RtdeInputData.StandardDigitalOutput)

robot.connect(parameters)
time.sleep(0.2)

# Read the inputs and the outputs
inputs = robot.rtde.output_data_values.actual_digital_input_bits
di3 = (inputs >> 3) & 1 == 1
configurable_di0 = (inputs >> 8) & 1 == 1
ai0 = robot.rtde.output_data_values.standard_analog_input0  # A or V
print(f"DI3={di3} CI0={configurable_di0} AI0={ai0:.3f}")

# Set DO2 and reset DO5. The other outputs do not change
values = RtdeInputValues()
values.standard_digital_output_mask = (1 << 2) | (1 << 5)
values.standard_digital_output = 1 << 2
robot.rtde.write_inputs(values)

# The same with the Primary Interface, in a secondary program:
# the running program does not stop
robot.primary_interface.script.send(
    "sec setOutputs():\n"
    "  set_standard_digital_out(2, True)\n"
    "  set_standard_digital_out(5, False)\n"
    "end\n")

# Read with the Primary Interface, 10 times per second
di0 = robot.primary_interface.masterboard_data.digital_inputs.digital0
tool_di1 = robot.primary_interface.masterboard_data.digital_inputs.tool_digital1

robot.disconnect()
```

### Read a bit

`ActualDigitalInputBits` holds all the digital inputs in one integer: bit `n` is `(bits >> n) & 1`. The masterboard data of the Primary Interface gives each bit as a property: `Digital0` to `Digital7`, `Configurable0` to `Configurable7`, `ToolDigital0` and `ToolDigital1`.

### Write with a mask

An RTDE write changes only the outputs of the mask. `StandardDigitalOutputMask = 0b0010_0100` selects outputs 2 and 5; `StandardDigitalOutput = 0b0000_0100` sets 2 and resets 5. The analog outputs have their own mask, `StandardAnalogOutputMask`.

## Troubleshooting

- **The output does not change:** the robot is not in remote control, or the robot program writes the same output.
- **The output changes, then goes back:** the robot program, or an I/O action of the installation, writes it.
- **The running program stops:** URScript was sent without `sec`. A line or a `def` program replaces the running program.

## What to read next

- [RTDE](rtde.md): the setup and the masks.
- [Read and write registers](registers.md): exchange numbers with the robot program.
