# RTDE: Real-Time Data Exchange

Exchange data with a UR cobot up to 500 Hz with RTDE: choose the outputs and the inputs, receive the data, write the inputs, pause and resume.

Web page: https://underautomation.com/universal-robots/documentation/rtde

RTDE (Real-Time Data Exchange) exchanges data between a Universal Robots cobot and your application, up to 500 times per second on e-Series. This page shows how to choose the data, receive it, write inputs and follow the state of the connection.

## How it works

At the connection, you give two lists, named from the point of view of the robot:

- the **outputs**: the data that the robot sends (positions, speeds, currents, I/O, registers...);
- the **inputs**: the data that your application writes (digital and analog outputs, registers, speed slider...).

The robot then sends a package of the outputs at the frequency you set, and accepts the inputs at any time. RTDE runs on port 30004, next to the robot program: it does not stop it.

For the list of the data and their meaning, see the [RTDE guide](https://www.universal-robots.com/articles/ur/interface-communication/real-time-data-exchange-rtde-guide/) of Universal Robots.

## Prerequisites

- The service `RTDE` is enabled on the robot: see [Prepare the robot](connect.md#prepare_the_robot).
- To write inputs, the robot is in remote control.

## Example

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_input_data import RtdeInputData
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData
from underautomation.universal_robots.rtde.rtde_input_values import RtdeInputValues

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# RTDE is disabled by default
parameters.rtde.enable = True
parameters.rtde.frequency = 500  # Hz

# Outputs: the data that the robot sends
parameters.rtde.output_setup.add(RtdeOutputData.ActualTcpPose)
parameters.rtde.output_setup.add(RtdeOutputData.OutputDoubleRegisters, 24)

# Inputs: the data that your application writes
parameters.rtde.input_setup.add(RtdeInputData.StandardAnalogOutputMask)
parameters.rtde.input_setup.add(RtdeInputData.StandardAnalogOutput0)
parameters.rtde.input_setup.add(RtdeInputData.InputIntRegisters, 24)

robot.connect(parameters)

# Raised at each package, 500 times per second here
def on_data(sender, e):
    values = robot.rtde.output_data_values
    pose = values.actual_tcp_pose
    register24 = values.output_double_registers.x24

robot.rtde.output_data_received(on_data)

# Write inputs
inputs = RtdeInputValues()
inputs.standard_analog_output_mask = 0b01  # analog output 0
inputs.standard_analog_output0 = 0.2
inputs.input_int_registers.x24 = 12
robot.rtde.write_inputs(inputs)

# Close RTDE only
robot.rtde.disconnect()
```

The same client works without `UR`:

```python
from underautomation.universal_robots.rtde.rtde_client import RtdeClient
from underautomation.universal_robots.rtde.rtde_output_setup import RtdeOutputSetup
from underautomation.universal_robots.rtde.rtde_input_setup import RtdeInputSetup
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData
from underautomation.universal_robots.rtde.rtde_input_data import RtdeInputData
from underautomation.universal_robots.rtde.rtde_input_values import RtdeInputValues
from underautomation.universal_robots.rtde.rtde_versions import RtdeVersions

# An RTDE client, without a UR instance
client = RtdeClient()

output_setup = RtdeOutputSetup()
output_setup.add(RtdeOutputData.ActualCurrent)

input_setup = RtdeInputSetup()
input_setup.add(RtdeInputData.InputIntRegisters, 24)

client.connect("192.168.0.1", output_setup, input_setup, RtdeVersions.V2, 500)

def on_data(sender, e):
    currents = client.output_data_values.actual_current  # A

client.output_data_received(on_data)

inputs = RtdeInputValues()
inputs.input_int_registers.x24 = 12
client.write_inputs(inputs)

client.disconnect()
```

## Choose the data

RTDE is disabled by default: set `Rtde.Enable` in `ConnectParameters`. Then add the outputs to `OutputSetup` and the inputs to `InputSetup`, with the enumerations `RtdeOutputData` and `RtdeInputData`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_input_data import RtdeInputData
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData
from underautomation.universal_robots.rtde.rtde_versions import RtdeVersions

robot = UR()

parameters = ConnectParameters("192.168.0.1")

parameters.rtde.enable = True

# 10 Hz by default, up to 500 Hz on e-Series. 0 is the maximum of the robot
parameters.rtde.frequency = 500

# V2 by default. The SDK uses V1 when the robot does not support V2
parameters.rtde.version = RtdeVersions.V2

# Inputs, written by your application
parameters.rtde.input_setup.add(RtdeInputData.StandardDigitalOutputMask)
parameters.rtde.input_setup.add(RtdeInputData.StandardDigitalOutput)
parameters.rtde.input_setup.add(RtdeInputData.InputBitRegisters, 64)

# Outputs, sent by the robot. A register needs its number
parameters.rtde.output_setup.add(RtdeOutputData.ActualTcpPose)
parameters.rtde.output_setup.add(RtdeOutputData.ToolOutputVoltage)
parameters.rtde.output_setup.add(RtdeOutputData.OutputDoubleRegisters, 24)

robot.connect(parameters)

# Version used on this connection
version = robot.rtde.version

robot.disconnect()
```

### Frequency

`Frequency` is 10 Hz by default. The maximum is 500 Hz on e-Series and 125 Hz on CB-Series. `0` asks for the maximum of the robot. `AppliedFrequency` gives the frequency used.

### Registers

A register type (`InputIntRegisters`, `OutputDoubleRegisters`...) needs the number of the register as second argument of `Add`. The registers 0 to 23 are for the fieldbus of the robot, 24 to 47 for RTDE clients. See [Read and write registers](registers.md).

### Protocol version

`Version` is `V2` by default: it is the version that takes the frequency into account. When the robot does not support V2, the SDK uses V1. `robot.Rtde.Version` gives the version used.

## Receive data

`OutputDataValues` holds the last values received. The event `OutputDataReceived` is raised at each package, with the values and `MeasuredFrequency`, the frequency computed from the timestamps of the robot.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData

robot = UR()

parameters = ConnectParameters("192.168.0.1")
parameters.rtde.enable = True
parameters.rtde.frequency = 500
parameters.rtde.output_setup.add(RtdeOutputData.ActualTcpPose)
parameters.rtde.output_setup.add(RtdeOutputData.ToolOutputVoltage)
parameters.rtde.output_setup.add(RtdeOutputData.OutputDoubleRegisters, 24)

robot.connect(parameters)

# Last values received
pose = robot.rtde.output_data_values.actual_tcp_pose
tool_voltage = robot.rtde.output_data_values.tool_output_voltage
register24 = robot.rtde.output_data_values.output_double_registers.x24

# Or an event, raised at each package
def on_data(sender, e):
    # Frequency computed from the timestamps of the robot
    frequency = robot.rtde.measured_frequency

    tcp = robot.rtde.output_data_values.actual_tcp_pose

robot.rtde.output_data_received(on_data)

robot.disconnect()
```

The event runs in the thread that receives the data. Keep it short: a slow handler delays the next packages.

## Write inputs

Create an `RtdeInputValues`, set its fields, and send it with `WriteInputs`. Give a value to every input of the setup: the robot writes them all.

The digital and analog outputs have a mask: only the outputs of the mask change.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.common.cartesian_coordinates import CartesianCoordinates
from underautomation.universal_robots.rtde.rtde_input_data import RtdeInputData
from underautomation.universal_robots.rtde.rtde_input_values import RtdeInputValues

robot = UR()

parameters = ConnectParameters("192.168.0.1")
parameters.rtde.enable = True
parameters.rtde.input_setup.add(RtdeInputData.StandardDigitalOutputMask)
parameters.rtde.input_setup.add(RtdeInputData.StandardDigitalOutput)
parameters.rtde.input_setup.add(RtdeInputData.ExternalForceTorque)
parameters.rtde.input_setup.add(RtdeInputData.StandardAnalogOutputMask)
parameters.rtde.input_setup.add(RtdeInputData.StandardAnalogOutput1)
parameters.rtde.input_setup.add(RtdeInputData.InputBitRegisters, 64)

robot.connect(parameters)

# Every input of the setup is written: give a value to each one
inputs = RtdeInputValues()

# Digital output 7: the mask selects the outputs to change, the value sets them
inputs.standard_digital_output_mask = 0b1000_0000
inputs.standard_digital_output = 0b1000_0000

inputs.external_force_torque = CartesianCoordinates(0, 0, 1, 0, 0, 0.1)

# Analog output 1
inputs.standard_analog_output_mask = 0b10
inputs.standard_analog_output1 = 0.1

inputs.input_bit_registers.x64 = True

robot.rtde.write_inputs(inputs)

robot.disconnect()
```

## Pause and resume

`Pause` stops the stream without closing the connection. `Resume` starts it again. The robot answers each request with `PauseReceived` and `StartReceived`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData
from underautomation.universal_robots.rtde.rtde_basic_request_event_args import RtdeBasicRequestEventArgs

robot = UR()

parameters = ConnectParameters("192.168.0.1")
parameters.rtde.enable = True
parameters.rtde.output_setup.add(RtdeOutputData.ActualTcpPose)

robot.connect(parameters)

# The robot answers each request
def on_pause(sender, e):
    print("Paused:", RtdeBasicRequestEventArgs(e._instance).accepted)

def on_start(sender, e):
    print("Started:", RtdeBasicRequestEventArgs(e._instance).accepted)

robot.rtde.pause_received(on_pause)
robot.rtde.start_received(on_start)

# Stop the stream, the connection stays open
robot.rtde.pause()

# Start the stream again
robot.rtde.resume()

robot.disconnect()
```

## State of the connection

`Connected` and `State` give the state of the connection. The robot sends text messages about the RTDE session: the last one is in `LastTextMessage`, and `TextMessageReceived` is raised for each one. `InternalErrorOccured` is raised when the SDK meets an error.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData
from underautomation.universal_robots.rtde.rtde_states import RTDEStates
from underautomation.universal_robots.rtde.rtde_text_message_event_args import RtdeTextMessageEventArgs
from underautomation.universal_robots.common.internal_error_event_args import InternalErrorEventArgs

robot = UR()

parameters = ConnectParameters("192.168.0.1")
parameters.rtde.enable = True
parameters.rtde.frequency = 500
parameters.rtde.output_setup.add(RtdeOutputData.ActualTcpPose)

robot.connect(parameters)

# Frequency accepted by the robot (V2)
applied_frequency = robot.rtde.applied_frequency

# The connection is open
connected = robot.rtde.connected

# Started, paused...
paused = robot.rtde.state == RTDEStates.Paused

# Messages of the robot about the RTDE session. The last one is kept
def on_message(sender, e):
    message = RtdeTextMessageEventArgs(e._instance)
    print(message.warning_level, message.source, message.message)

robot.rtde.text_message_received(on_message)
last_message = robot.rtde.last_text_message

# Errors of the SDK in the background
def on_error(sender, e):
    print(InternalErrorEventArgs(e._instance).message)

robot.rtde.internal_error_occured(on_error)

robot.disconnect()
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**RtdeClientBase** ([reference](../api/underautomation.universal_robots.rtde.internal.md#rtdeclientbase-robotrtde))

- `protocol_version_received(handler)`: Event raised during connection when the robot specifies if asked protocol version is supported
- `text_message_received(handler)`: Event raised when a RTDE message is received
- `output_data_received(handler)`: Event raised when data from the robot is comming at specified frequency
- `setup_outputs_received(handler)`: Event raised during connection when the robot acknowledges output setup
- `setup_inputs_received(handler)`: Event raised during connection when the robot acknowledges input setup
- `start_received(handler)`: Event raised as soon as data streaming starts
- `pause_received(handler)`: Event raised when streaming is paused
- `package_received(handler)`: Generic event raised each time a RTDE package is received
- `pause() -> None`: Pause data streaming without disconnecting client
- `resume() -> None`: Restart data streaming after a Pause
- `write_inputs(inputValues: RtdeInputValues) -> None`: Write data to controller. Data must be those selected in connect parameters
- `disconnect() -> None`: Close the RTDE connection to the robot
- `last_text_message: RtdeTextMessageEventArgs (read only)`: Last text received from the robot
- `state: RTDEStates (read only)`: Current RTDE state
- `connected: bool (read only)`: Gets a value indicating if RTDE client is connected to the robot
- `ip: str (read only)`: IP address of the robot
- `applied_frequency: float (read only)`: Output data frequency requested to the robot, only for RTDE version 2
- `version: RtdeVersions (read only)`: Current protocol version used to stream data
- `output_setup: typing.List[RtdeOutputSetupItem] (read only)`: List of all data sent from the robot to the PC (robot point of view)
- `input_setup: typing.List[RtdeInputSetupItem] (read only)`: List of all data the PC can write to the robot (robot point of view)
- `output_recipe_id: int (read only)`: Recipe Identifier of output received data
- `input_recipe_id: int (read only)`: Recipe Identifier of input sent data
- `input_recipe_is_valid: bool (read only)`: Indicates that the recipe is valid, i.e. that all the registers have been found and are not already reserved for writing by another RTDE client. Check event SetupInputsReceived to see which registers are NOT_FOUND or IN_USE
- `measured_frequency: float (read only)`: Measured output data packet frequency. "Timestamp" output data shoud be part of output setup to measure frequency.
- `output_data_values: RtdeOutputValues (read only)`: Last data received from the robot
- Inherited from [URServiceBase](../api/underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

**RtdeParametersBase** ([reference](../api/underautomation.universal_robots.rtde.internal.md#rtdeparametersbase))

- `frequency: float`: For RTDE version 2, you can specify a frequency for output received data. Maximum frequency depends on your robot version. If you set frequency to 0, maximum frequency will be choosen Default value is 10Hz
- `version: RtdeVersions`: RTDE version. If set to Auto, the most recent version will be choosen according to your robot version Default value is V2
- `output_setup: RtdeOutputSetup`: List of all output data the robot will send to your application
- `input_setup: RtdeInputSetup`: List of all input data you can send to the robot
- `port: int`: TCP port used for RTDE connection. Default : 30004
- `static DEFAULT_PORT: int`: Default RTDE TCP port used (30004)

**RtdeVersions** ([reference](../api/underautomation.universal_robots.rtde.md#rtdeversions-robotrtdeversion))

- V1: Rtde version 1
- V2: Rtde version 2

**RtdeOutputData** ([reference](../api/underautomation.universal_robots.rtde.md#rtdeoutputdata))

- Timestamp: Time elapsed since the controller was started [s]
- TargetQ: Target joint positions
- TargetQd: Target joint velocities
- TargetQdd: Target joint accelerations
- TargetCurrent: Target joint currents
- TargetMoment: Target joint moments (torques)
- ActualQ: Actual joint positions
- ActualQd: Actual joint velocities
- ActualCurrent: Actual joint currents
- JointControlOutput: Joint control currents
- ActualTcpPose: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- ActualTcpSpeed: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- ActualTcpForce: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- TargetTcpPose: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- TargetTcpSpeed: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- ActualDigitalInputBits: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- JointTemperatures: Temperature of each joint in degrees Celsius
- ActualExecutionTime: Controller real-time thread execution time
- RobotMode: Robot mode
- JointMode: Joint control modes
- SafetyMode: Safety mode
- SafetyStatus: Safety status
- ActualToolAccelerometer: Tool x, y and z accelerometer values
- SpeedScaling: Speed scaling of the trajectory limiter
- TargetSpeedFraction: Target speed fraction
- ActualMomentum: Norm of Cartesian linear momentum
- ActualMainVoltage: Safety Control Board: Main voltage
- ActualRobotVoltage: Safety Control Board: Robot voltage (48V)
- ActualRobotCurrent: Safety Control Board: Robot current
- ActualJointVoltage: Actual joint voltages
- ActualDigitalOutputBits: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- RuntimeState: Program state
- ElbowPosition: Position of robot elbow in Cartesian Base Coordinates
- ElbowVelocity: Velocity of robot elbow in Cartesian Base Coordinates
- RobotStatusBits: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- SafetyStatusBits: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- AnalogIOTypes: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- StandardAnalogInput0: Standard analog input 0 [mA or V]
- StandardAnalogInput1: Standard analog input 1 [mA or V]
- StandardAnalogOutput0: Standard analog output 0 [mA or V]
- StandardAnalogOutput1: Standard analog output 1 [mA or V]
- IOCurrent: I/O current [mA]
- Euromap67InputBits: Euromap67 input bits
- Euromap67OutputBits: Euromap67 output bits
- Euromap67_24VVoltage: Euromap 24V voltage [V]
- Euromap67_24VCurrent: Euromap 24V current [mA]
- ToolMode: Tool mode
- ToolAnalogInputTypes: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- ToolAnalogInput0: Tool analog input 0 [mA or V]
- ToolAnalogInput1: Tool analog input 1 [mA or V]
- ToolOutputVoltage: Tool output voltage [V]
- ToolOutputCurrent: Tool current [mA]
- ToolTemperature: Tool temperature in degrees Celsius
- TcpForceScalar: TCP force scalar [N]
- OutputBitRegisters0To31: General purpose bits
- OutputBitRegisters32To63: General purpose bits
- OutputBitRegisters: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- OutputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- OutputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- InputBitRegisters0To31: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- InputBitRegisters32To63: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- InputBitRegisters: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- InputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- InputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- ToolOutputMode: The current output mode
- ToolDigitalOutput0mode: The current mode of digital output 0
- ToolDigitalOutput1Mode: The current mode of digital output 1
- Payload: Payload mass Kg
- PayloadCOG: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- PayloadInertia: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- ScriptControlLine: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- FTRawWrench: Raw force and torque measurement, not compensated for forces and torques caused by the payload

**RtdeInputData** ([reference](../api/underautomation.universal_robots.rtde.md#rtdeinputdata))

- SpeedSliderMask: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- SpeedSliderFraction: new speed slider value
- StandardDigitalOutputMask: Standard digital output bit mask
- ConfigurableDigitalOutputMask: Configurable digital output bit mask
- StandardDigitalOutput: Standard digital outputs
- ConfigurableDigitalOutput: Configurable digital outputs
- StandardAnalogOutputMask: Standard analog output mask
- StandardAnalogOutputType: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- StandardAnalogOutput0: Standard analog output 0 (ratio) [0..1]
- StandardAnalogOutput1: Standard analog output 1 (ratio) [0..1]
- InputBtRegisters0To31: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- InputBtRegisters32To63: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- InputBitRegisters: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- InputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- InputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- ExternalForceTorque: Input external wrench when using ft_rtde_input_enable builtin.

**RtdeInputValues** ([reference](../api/underautomation.universal_robots.rtde.md#rtdeinputvalues))

- `RtdeInputValues()`: Initializes a new instance with default values for all input variables.
- `reset() -> None`: Resets all input values to their defaults.
- `speed_slider_mask: int`: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- `speed_slider_fraction: float`: new speed slider value
- `standard_digital_output_mask: int`: Standard digital output bit mask
- `configurable_digital_output_mask: int`: Configurable digital output bit mask
- `standard_digital_output: int`: Standard digital outputs
- `configurable_digital_output: int`: Configurable digital outputs
- `standard_analog_output_mask: int`: Standard analog output mask
- `standard_analog_output_type: int`: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- `standard_analog_output0: float`: Standard analog output 0 (ratio) [0..1]
- `standard_analog_output1: float`: Standard analog output 1 (ratio) [0..1]
- `input_bt_registers0_to31: int`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `input_bt_registers32_to63: int`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `input_bit_registers: RtdeBitRegistersValue (read only)`: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- `input_int_registers: RtdeIntRegistersValue (read only)`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `input_double_registers: RtdeDoubleRegistersValue (read only)`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `external_force_torque: CartesianCoordinates`: Input external wrench when using ft_rtde_input_enable builtin.
- Inherited from [RtdeBaseValues](../api/underautomation.universal_robots.rtde.md#rtdebasevalues-robotrtdeoutput_data_values): `values`

**RtdeOutputValues** ([reference](../api/underautomation.universal_robots.rtde.md#rtdeoutputvalues-robotrtdeoutput_data_values))

- `timestamp: float`: Time elapsed since the controller was started [s]
- `target_q: JointsDoubleValues`: Target joint positions
- `target_qd: JointsDoubleValues`: Target joint velocities
- `target_qdd: JointsDoubleValues`: Target joint accelerations
- `target_current: JointsDoubleValues`: Target joint currents
- `target_moment: JointsDoubleValues`: Target joint moments (torques)
- `actual_q: JointsDoubleValues`: Actual joint positions
- `actual_qd: JointsDoubleValues`: Actual joint velocities
- `actual_current: JointsDoubleValues`: Actual joint currents
- `joint_control_output: JointsDoubleValues`: Joint control currents
- `actual_tcp_pose: Pose`: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `actual_tcp_speed: Pose`: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `actual_tcp_force: CartesianCoordinates`: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- `target_tcp_pose: Pose`: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `target_tcp_speed: Pose`: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `actual_digital_input_bits: int`: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `joint_temperatures: JointsDoubleValues`: Temperature of each joint in degrees Celsius
- `actual_execution_time: float`: Controller real-time thread execution time
- `robot_mode: int`: Robot mode
- `joint_mode: JointsIntValues`: Joint control modes
- `safety_mode: int`: Safety mode
- `safety_status: int`: Safety status
- `actual_tool_accelerometer: Vector3D`: Tool x, y and z accelerometer values
- `speed_scaling: float`: Speed scaling of the trajectory limiter
- `target_speed_fraction: float`: Target speed fraction
- `actual_momentum: float`: Norm of Cartesian linear momentum
- `actual_main_voltage: float`: Safety Control Board: Main voltage
- `actual_robot_voltage: float`: Safety Control Board: Robot voltage (48V)
- `actual_robot_current: float`: Safety Control Board: Robot current
- `actual_joint_voltage: JointsDoubleValues`: Actual joint voltages
- `actual_digital_output_bits: int`: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `runtime_state: int`: Program state
- `elbow_position: Vector3D`: Position of robot elbow in Cartesian Base Coordinates
- `elbow_velocity: Vector3D`: Velocity of robot elbow in Cartesian Base Coordinates
- `robot_status_bits: int`: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- `safety_status_bits: int`: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- `analog_io_types: int`: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- `standard_analog_input0: float`: Standard analog input 0 [mA or V]
- `standard_analog_input1: float`: Standard analog input 1 [mA or V]
- `standard_analog_output0: float`: Standard analog output 0 [mA or V]
- `standard_analog_output1: float`: Standard analog output 1 [mA or V]
- `io_current: float`: I/O current [mA]
- `euromap67_input_bits: int`: Euromap67 input bits
- `euromap67_output_bits: int`: Euromap67 output bits
- `euromap67_24_v_voltage: float`: Euromap 24V voltage [V]
- `euromap67_24_v_current: float`: Euromap 24V current [mA]
- `tool_mode: int`: Tool mode
- `tool_analog_input_types: int`: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- `tool_analog_input0: float`: Tool analog input 0 [mA or V]
- `tool_analog_input1: float`: Tool analog input 1 [mA or V]
- `tool_output_voltage: int`: Tool output voltage [V]
- `tool_output_current: float`: Tool current [mA]
- `tool_temperature: float`: Tool temperature in degrees Celsius
- `tcp_force_scalar: float`: TCP force scalar [N]
- `output_bit_registers0_to31: int`: General purpose bits
- `output_bit_registers32_to63: int`: General purpose bits
- `output_bit_registers: RtdeBitRegistersValue (read only)`: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `output_int_registers: RtdeIntRegistersValue (read only)`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- `output_double_registers: RtdeDoubleRegistersValue (read only)`: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- `input_bit_registers0_to31: int`: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `input_bit_registers32_to63: int`: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `input_bit_registers: RtdeBitRegistersValue (read only)`: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `input_int_registers: RtdeIntRegistersValue (read only)`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `input_double_registers: RtdeDoubleRegistersValue (read only)`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `tool_output_mode: int`: The current output mode
- `tool_digital_output0mode: int`: The current mode of digital output 0
- `tool_digital_output1_mode: int`: The current mode of digital output 1
- `payload: float`: Payload mass Kg
- `payload_cog: Vector3D`: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- `payload_inertia: CartesianCoordinates`: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- `script_control_line: int`: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- `ft_raw_wrench: CartesianCoordinates`: Raw force and torque measurement, not compensated for forces and torques caused by the payload
- Inherited from [RtdeBaseValues](../api/underautomation.universal_robots.rtde.md#rtdebasevalues-robotrtdeoutput_data_values): `values`

## What to read next

- [Read and write registers](registers.md): exchange values with the robot program.
- [Get the robot position](how-to-get-position.md) and [Read and write I/O](how-to-read-write-io.md).
