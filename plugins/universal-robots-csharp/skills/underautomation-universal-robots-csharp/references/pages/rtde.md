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

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.Rtde;

class Rtde
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // RTDE is disabled by default
    parameters.Rtde.Enable = true;
    parameters.Rtde.Frequency = 500; // Hz

    // Outputs: the data that the robot sends
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ActualTcpPose);
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.OutputDoubleRegisters, 24);

    // Inputs: the data that your application writes
    parameters.Rtde.InputSetup.Add(RtdeInputData.StandardAnalogOutputMask);
    parameters.Rtde.InputSetup.Add(RtdeInputData.StandardAnalogOutput0);
    parameters.Rtde.InputSetup.Add(RtdeInputData.InputIntRegisters, 24);

    robot.Connect(parameters);

    // Raised at each package, 500 times per second here
    robot.Rtde.OutputDataReceived += (sender, e) =>
    {
      Pose pose = e.OutputDataValues.ActualTcpPose;
      double register24 = e.OutputDataValues.OutputDoubleRegisters.X24;
    };

    // Write inputs
    var inputs = new RtdeInputValues();
    inputs.StandardAnalogOutputMask = 0b01; // analog output 0
    inputs.StandardAnalogOutput0 = 0.2;
    inputs.InputIntRegisters.X24 = 12;
    robot.Rtde.WriteInputs(inputs);

    // Close RTDE only
    robot.Rtde.Disconnect();
  }
}
```

The same client works without `UR`:

```csharp
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.Rtde;

class RtdeDirect
{
  static void Main(string[] args)
  {
    // An RTDE client, without a UR instance
    var client = new RtdeClient();

    var outputSetup = new RtdeOutputSetup();
    outputSetup.Add(RtdeOutputData.ActualCurrent);

    var inputSetup = new RtdeInputSetup();
    inputSetup.Add(RtdeInputData.InputIntRegisters, 24);

    client.Connect("192.168.0.1", outputSetup, inputSetup, RtdeVersions.V2, frequency: 500);

    client.OutputDataReceived += (sender, e) =>
    {
      JointsDoubleValues currents = e.OutputDataValues.ActualCurrent; // A
    };

    var inputs = new RtdeInputValues();
    inputs.InputIntRegisters.X24 = 12;
    client.WriteInputs(inputs);

    client.Disconnect();
  }
}
```

## Choose the data

RTDE is disabled by default: set `Rtde.Enable` in `ConnectParameters`. Then add the outputs to `OutputSetup` and the inputs to `InputSetup`, with the enumerations `RtdeOutputData` and `RtdeInputData`.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Rtde;

class RtdeSetup
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    parameters.Rtde.Enable = true;

    // 10 Hz by default, up to 500 Hz on e-Series. 0 is the maximum of the robot
    parameters.Rtde.Frequency = 500;

    // V2 by default. The SDK uses V1 when the robot does not support V2
    parameters.Rtde.Version = RtdeVersions.V2;

    // Inputs, written by your application
    parameters.Rtde.InputSetup.Add(RtdeInputData.StandardDigitalOutputMask);
    parameters.Rtde.InputSetup.Add(RtdeInputData.StandardDigitalOutput);
    parameters.Rtde.InputSetup.Add(RtdeInputData.InputBitRegisters, 64);

    // Outputs, sent by the robot. A register needs its number
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ActualTcpPose);
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ToolOutputVoltage);
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.OutputDoubleRegisters, 24);

    robot.Connect(parameters);

    // Version used on this connection
    RtdeVersions version = robot.Rtde.Version;

    robot.Disconnect();
  }
}
```

### Frequency

`Frequency` is 10 Hz by default. The maximum is 500 Hz on e-Series and 125 Hz on CB-Series. `0` asks for the maximum of the robot. `AppliedFrequency` gives the frequency used.

### Registers

A register type (`InputIntRegisters`, `OutputDoubleRegisters`...) needs the number of the register as second argument of `Add`. The registers 0 to 23 are for the fieldbus of the robot, 24 to 47 for RTDE clients. See [Read and write registers](registers.md).

### Protocol version

`Version` is `V2` by default: it is the version that takes the frequency into account. When the robot does not support V2, the SDK uses V1. `robot.Rtde.Version` gives the version used.

## Receive data

`OutputDataValues` holds the last values received. The event `OutputDataReceived` is raised at each package, with the values and `MeasuredFrequency`, the frequency computed from the timestamps of the robot.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.Rtde;

class RtdeReceive
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");
    parameters.Rtde.Enable = true;
    parameters.Rtde.Frequency = 500;
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ActualTcpPose);
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ToolOutputVoltage);
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.OutputDoubleRegisters, 24);

    robot.Connect(parameters);

    // Last values received
    Pose pose = robot.Rtde.OutputDataValues.ActualTcpPose;
    int toolVoltage = robot.Rtde.OutputDataValues.ToolOutputVoltage;
    double register24 = robot.Rtde.OutputDataValues.OutputDoubleRegisters.X24;

    // Or an event, raised at each package
    robot.Rtde.OutputDataReceived += (sender, e) =>
    {
      // Frequency computed from the timestamps of the robot
      double frequency = e.MeasuredFrequency;

      Pose tcp = e.OutputDataValues.ActualTcpPose;
    };

    robot.Disconnect();
  }
}
```

The event runs in the thread that receives the data. Keep it short: a slow handler delays the next packages.

## Write inputs

Create an `RtdeInputValues`, set its fields, and send it with `WriteInputs`. Give a value to every input of the setup: the robot writes them all.

The digital and analog outputs have a mask: only the outputs of the mask change.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.Rtde;

class RtdeSend
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");
    parameters.Rtde.Enable = true;
    parameters.Rtde.InputSetup.Add(RtdeInputData.StandardDigitalOutputMask);
    parameters.Rtde.InputSetup.Add(RtdeInputData.StandardDigitalOutput);
    parameters.Rtde.InputSetup.Add(RtdeInputData.ExternalForceTorque);
    parameters.Rtde.InputSetup.Add(RtdeInputData.StandardAnalogOutputMask);
    parameters.Rtde.InputSetup.Add(RtdeInputData.StandardAnalogOutput1);
    parameters.Rtde.InputSetup.Add(RtdeInputData.InputBitRegisters, 64);

    robot.Connect(parameters);

    // Every input of the setup is written: give a value to each one
    var inputs = new RtdeInputValues();

    // Digital output 7: the mask selects the outputs to change, the value sets them
    inputs.StandardDigitalOutputMask = 0b1000_0000;
    inputs.StandardDigitalOutput = 0b1000_0000;

    inputs.ExternalForceTorque = new CartesianCoordinates(0, 0, 1, 0, 0, 0.1);

    // Analog output 1
    inputs.StandardAnalogOutputMask = 0b10;
    inputs.StandardAnalogOutput1 = 0.1;

    inputs.InputBitRegisters.X64 = true;

    robot.Rtde.WriteInputs(inputs);

    robot.Disconnect();
  }
}
```

## Pause and resume

`Pause` stops the stream without closing the connection. `Resume` starts it again. The robot answers each request with `PauseReceived` and `StartReceived`.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Rtde;

class RtdePauseResume
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");
    parameters.Rtde.Enable = true;
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ActualTcpPose);

    robot.Connect(parameters);

    // The robot answers each request
    robot.Rtde.PauseReceived += (sender, e) => Console.WriteLine("Paused: " + e.Accepted);
    robot.Rtde.StartReceived += (sender, e) => Console.WriteLine("Started: " + e.Accepted);

    // Stop the stream, the connection stays open
    robot.Rtde.Pause();

    // Start the stream again
    robot.Rtde.Resume();

    robot.Disconnect();
  }
}
```

## State of the connection

`Connected` and `State` give the state of the connection. The robot sends text messages about the RTDE session: the last one is in `LastTextMessage`, and `TextMessageReceived` is raised for each one. `InternalErrorOccured` is raised when the SDK meets an error.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Rtde;

class RtdeOther
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");
    parameters.Rtde.Enable = true;
    parameters.Rtde.Frequency = 500;
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ActualTcpPose);

    robot.Connect(parameters);

    // Frequency accepted by the robot (V2)
    double appliedFrequency = robot.Rtde.AppliedFrequency;

    // The connection is open
    bool connected = robot.Rtde.Connected;

    // Started, paused...
    bool paused = robot.Rtde.State == RTDEStates.Paused;

    // Messages of the robot about the RTDE session. The last one is kept
    robot.Rtde.TextMessageReceived += (sender, e) =>
    {
      Console.WriteLine(e.WarningLevel + " " + e.Source + ": " + e.Message);
    };
    RtdeTextMessageEventArgs lastMessage = robot.Rtde.LastTextMessage;

    // Errors of the SDK in the background
    robot.Rtde.InternalErrorOccured += (sender, e) => Console.WriteLine(e.Message);

    robot.Disconnect();
  }
}
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**RtdeClientBase** ([reference](../api/UnderAutomation.UniversalRobots.Rtde.Internal.md#rtdeclientbase-robotrtde))

- `double AppliedFrequency { get; }`: Output data frequency requested to the robot, only for RTDE version 2
- `bool Connected { get; }`: Gets a value indicating if RTDE client is connected to the robot
- `void Disconnect()`: Close the RTDE connection to the robot
- `string IP { get; }`: IP address of the robot
- `byte InputRecipeId { get; }`: Recipe Identifier of input sent data
- `bool InputRecipeIsValid { get; }`: Indicates that the recipe is valid, i.e. that all the registers have been found and are not already reserved for writing by another RTDE client. Check event SetupInputsReceived to see which registers are NOT_FOUND or IN_USE
- `RtdeInputSetupItem[] InputSetup { get; }`: List of all data the PC can write to the robot (robot point of view)
- `RtdeTextMessageEventArgs LastTextMessage { get; }`: Last text received from the robot
- `double MeasuredFrequency { get; }`: Measured output data packet frequency. "Timestamp" output data shoud be part of output setup to measure frequency.
- `event EventHandler<RtdeDataPackageEventArgs> OutputDataReceived`: Event raised when data from the robot is comming at specified frequency
- `RtdeOutputValues OutputDataValues { get; }`: Last data received from the robot
- `byte OutputRecipeId { get; }`: Recipe Identifier of output received data
- `RtdeOutputSetupItem[] OutputSetup { get; }`: List of all data sent from the robot to the PC (robot point of view)
- `event EventHandler<PackageEventArgs> PackageReceived`: Generic event raised each time a RTDE package is received
- `void Pause()`: Pause data streaming without disconnecting client
- `event EventHandler<RtdeBasicRequestEventArgs> PauseReceived`: Event raised when streaming is paused
- `event EventHandler<RtdeProtocolVersionEventArgs> ProtocolVersionReceived`: Event raised during connection when the robot specifies if asked protocol version is supported
- `void Resume()`: Restart data streaming after a Pause
- `event EventHandler<RtdeControlPackageSetupInputsEventArgs> SetupInputsReceived`: Event raised during connection when the robot acknowledges input setup
- `event EventHandler<RtdeControlPackageSetupOutputsEventArgs> SetupOutputsReceived`: Event raised during connection when the robot acknowledges output setup
- `event EventHandler<RtdeBasicRequestEventArgs> StartReceived`: Event raised as soon as data streaming starts
- `RTDEStates State { get; }`: Current RTDE state
- `event EventHandler<RtdeTextMessageEventArgs> TextMessageReceived`: Event raised when a RTDE message is received
- `RtdeVersions Version { get; }`: Current protocol version used to stream data
- `void WriteInputs(RtdeInputValues inputValues)`: Write data to controller. Data must be those selected in connect parameters
- Inherited from [URServiceBase](../api/UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

**RtdeParametersBase** ([reference](../api/UnderAutomation.UniversalRobots.Rtde.Internal.md#rtdeparametersbase))

- `const int DEFAULT_PORT = 30004`: Default RTDE TCP port used (30004)
- `double Frequency { get; set; }`: For RTDE version 2, you can specify a frequency for output received data. Maximum frequency depends on your robot version. If you set frequency to 0, maximum frequency will be choosen Default value is 10Hz
- `RtdeInputSetup InputSetup { get; set; }`: List of all input data you can send to the robot
- `RtdeOutputSetup OutputSetup { get; set; }`: List of all output data the robot will send to your application
- `int Port { get; set; }`: TCP port used for RTDE connection. Default : 30004
- `RtdeVersions Version { get; set; }`: RTDE version. If set to Auto, the most recent version will be choosen according to your robot version Default value is V2

**RtdeVersions** ([reference](../api/UnderAutomation.UniversalRobots.Rtde.md#rtdeversions-robotrtdeversion))

- V1: Rtde version 1
- V2: Rtde version 2

**RtdeOutputData** ([reference](../api/UnderAutomation.UniversalRobots.Rtde.md#rtdeoutputdata))

- ActualCurrent: Actual joint currents
- ActualDigitalInputBits: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- ActualDigitalOutputBits: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- ActualExecutionTime: Controller real-time thread execution time
- ActualJointVoltage: Actual joint voltages
- ActualMainVoltage: Safety Control Board: Main voltage
- ActualMomentum: Norm of Cartesian linear momentum
- ActualQ: Actual joint positions
- ActualQd: Actual joint velocities
- ActualRobotCurrent: Safety Control Board: Robot current
- ActualRobotVoltage: Safety Control Board: Robot voltage (48V)
- ActualTcpForce: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- ActualTcpPose: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- ActualTcpSpeed: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- ActualToolAccelerometer: Tool x, y and z accelerometer values
- AnalogIOTypes: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- ElbowPosition: Position of robot elbow in Cartesian Base Coordinates
- ElbowVelocity: Velocity of robot elbow in Cartesian Base Coordinates
- Euromap67InputBits: Euromap67 input bits
- Euromap67OutputBits: Euromap67 output bits
- Euromap67_24VCurrent: Euromap 24V current [mA]
- Euromap67_24VVoltage: Euromap 24V voltage [V]
- FTRawWrench: Raw force and torque measurement, not compensated for forces and torques caused by the payload
- IOCurrent: I/O current [mA]
- InputBitRegisters: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- InputBitRegisters0To31: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- InputBitRegisters32To63: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- InputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- InputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- JointControlOutput: Joint control currents
- JointMode: Joint control modes
- JointTemperatures: Temperature of each joint in degrees Celsius
- OutputBitRegisters: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- OutputBitRegisters0To31: General purpose bits
- OutputBitRegisters32To63: General purpose bits
- OutputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- OutputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- Payload: Payload mass Kg
- PayloadCOG: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- PayloadInertia: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- RobotMode: Robot mode
- RobotStatusBits: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- RuntimeState: Program state
- SafetyMode: Safety mode
- SafetyStatus: Safety status
- SafetyStatusBits: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- ScriptControlLine: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- SpeedScaling: Speed scaling of the trajectory limiter
- StandardAnalogInput0: Standard analog input 0 [mA or V]
- StandardAnalogInput1: Standard analog input 1 [mA or V]
- StandardAnalogOutput0: Standard analog output 0 [mA or V]
- StandardAnalogOutput1: Standard analog output 1 [mA or V]
- TargetCurrent: Target joint currents
- TargetMoment: Target joint moments (torques)
- TargetQ: Target joint positions
- TargetQd: Target joint velocities
- TargetQdd: Target joint accelerations
- TargetSpeedFraction: Target speed fraction
- TargetTcpPose: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- TargetTcpSpeed: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- TcpForceScalar: TCP force scalar [N]
- Timestamp: Time elapsed since the controller was started [s]
- ToolAnalogInput0: Tool analog input 0 [mA or V]
- ToolAnalogInput1: Tool analog input 1 [mA or V]
- ToolAnalogInputTypes: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- ToolDigitalOutput0mode: The current mode of digital output 0
- ToolDigitalOutput1Mode: The current mode of digital output 1
- ToolMode: Tool mode
- ToolOutputCurrent: Tool current [mA]
- ToolOutputMode: The current output mode
- ToolOutputVoltage: Tool output voltage [V]
- ToolTemperature: Tool temperature in degrees Celsius

**RtdeInputData** ([reference](../api/UnderAutomation.UniversalRobots.Rtde.md#rtdeinputdata))

- ConfigurableDigitalOutput: Configurable digital outputs
- ConfigurableDigitalOutputMask: Configurable digital output bit mask
- ExternalForceTorque: Input external wrench when using ft_rtde_input_enable builtin.
- InputBitRegisters: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- InputBtRegisters0To31: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- InputBtRegisters32To63: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- InputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- InputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- SpeedSliderFraction: new speed slider value
- SpeedSliderMask: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- StandardAnalogOutput0: Standard analog output 0 (ratio) [0..1]
- StandardAnalogOutput1: Standard analog output 1 (ratio) [0..1]
- StandardAnalogOutputMask: Standard analog output mask
- StandardAnalogOutputType: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- StandardDigitalOutput: Standard digital outputs
- StandardDigitalOutputMask: Standard digital output bit mask

**RtdeInputValues** ([reference](../api/UnderAutomation.UniversalRobots.Rtde.md#rtdeinputvalues))

- `RtdeInputValues()`: Initializes a new instance with default values for all input variables.
- `byte ConfigurableDigitalOutput { get; set; }`: Configurable digital outputs
- `byte ConfigurableDigitalOutputMask { get; set; }`: Configurable digital output bit mask
- `CartesianCoordinates ExternalForceTorque { get; set; }`: Input external wrench when using ft_rtde_input_enable builtin.
- `object GetValue(RtdeInputSetupItem item)`: Gets the current value for the input variable described by a setup item.
- `RtdeBitRegistersValue InputBitRegisters { get; }`: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- `uint InputBtRegisters0To31 { get; set; }`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `uint InputBtRegisters32To63 { get; set; }`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `RtdeDoubleRegistersValue InputDoubleRegisters { get; }`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeIntRegistersValue InputIntRegisters { get; }`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `void Reset()`: Resets all input values to their defaults.
- `void SetValue(RtdeInputData data, int index, object value)`: Sets the value for the specified RTDE input variable at a given register index.
- `void SetValue(RtdeInputData data, object value)`: Sets the value for the specified RTDE input variable.
- `void SetValue(RtdeInputSetupItem item, object value)`: Sets the value for the input variable described by a setup item.
- `double SpeedSliderFraction { get; set; }`: new speed slider value
- `uint SpeedSliderMask { get; set; }`: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- `double StandardAnalogOutput0 { get; set; }`: Standard analog output 0 (ratio) [0..1]
- `double StandardAnalogOutput1 { get; set; }`: Standard analog output 1 (ratio) [0..1]
- `byte StandardAnalogOutputMask { get; set; }`: Standard analog output mask
- `byte StandardAnalogOutputType { get; set; }`: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- `byte StandardDigitalOutput { get; set; }`: Standard digital outputs
- `byte StandardDigitalOutputMask { get; set; }`: Standard digital output bit mask
- Inherited from [RtdeBaseValues](../api/UnderAutomation.UniversalRobots.Rtde.md#rtdebasevalues-robotrtdeoutputdatavalues): `Values`

**RtdeOutputValues** ([reference](../api/UnderAutomation.UniversalRobots.Rtde.md#rtdeoutputvalues-robotrtdeoutputdatavalues))

- `JointsDoubleValues ActualCurrent { get; set; }`: Actual joint currents
- `ulong ActualDigitalInputBits { get; set; }`: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `ulong ActualDigitalOutputBits { get; set; }`: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `double ActualExecutionTime { get; set; }`: Controller real-time thread execution time
- `JointsDoubleValues ActualJointVoltage { get; set; }`: Actual joint voltages
- `double ActualMainVoltage { get; set; }`: Safety Control Board: Main voltage
- `double ActualMomentum { get; set; }`: Norm of Cartesian linear momentum
- `JointsDoubleValues ActualQ { get; set; }`: Actual joint positions
- `JointsDoubleValues ActualQd { get; set; }`: Actual joint velocities
- `double ActualRobotCurrent { get; set; }`: Safety Control Board: Robot current
- `double ActualRobotVoltage { get; set; }`: Safety Control Board: Robot voltage (48V)
- `CartesianCoordinates ActualTcpForce { get; set; }`: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- `Pose ActualTcpPose { get; set; }`: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `Pose ActualTcpSpeed { get; set; }`: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `Vector3D ActualToolAccelerometer { get; set; }`: Tool x, y and z accelerometer values
- `uint AnalogIOTypes { get; set; }`: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- `Vector3D ElbowPosition { get; set; }`: Position of robot elbow in Cartesian Base Coordinates
- `Vector3D ElbowVelocity { get; set; }`: Velocity of robot elbow in Cartesian Base Coordinates
- `uint Euromap67InputBits { get; set; }`: Euromap67 input bits
- `uint Euromap67OutputBits { get; set; }`: Euromap67 output bits
- `double Euromap67_24VCurrent { get; set; }`: Euromap 24V current [mA]
- `double Euromap67_24VVoltage { get; set; }`: Euromap 24V voltage [V]
- `CartesianCoordinates FTRawWrench { get; set; }`: Raw force and torque measurement, not compensated for forces and torques caused by the payload
- `object GetValue(RtdeOutputSetupItem item)`: Gets the current value for the output variable described by a setup item.
- `double IOCurrent { get; set; }`: I/O current [mA]
- `RtdeBitRegistersValue InputBitRegisters { get; }`: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `uint InputBitRegisters0To31 { get; set; }`: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `uint InputBitRegisters32To63 { get; set; }`: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `RtdeDoubleRegistersValue InputDoubleRegisters { get; }`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeIntRegistersValue InputIntRegisters { get; }`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `JointsDoubleValues JointControlOutput { get; set; }`: Joint control currents
- `JointsIntValues JointMode { get; set; }`: Joint control modes
- `JointsDoubleValues JointTemperatures { get; set; }`: Temperature of each joint in degrees Celsius
- `RtdeBitRegistersValue OutputBitRegisters { get; }`: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `uint OutputBitRegisters0To31 { get; set; }`: General purpose bits
- `uint OutputBitRegisters32To63 { get; set; }`: General purpose bits
- `RtdeDoubleRegistersValue OutputDoubleRegisters { get; }`: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeIntRegistersValue OutputIntRegisters { get; }`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- `double Payload { get; set; }`: Payload mass Kg
- `Vector3D PayloadCOG { get; set; }`: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- `CartesianCoordinates PayloadInertia { get; set; }`: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- `int RobotMode { get; set; }`: Robot mode
- `uint RobotStatusBits { get; set; }`: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- `uint RuntimeState { get; set; }`: Program state
- `int SafetyMode { get; set; }`: Safety mode
- `int SafetyStatus { get; set; }`: Safety status
- `uint SafetyStatusBits { get; set; }`: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- `uint ScriptControlLine { get; set; }`: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- `double SpeedScaling { get; set; }`: Speed scaling of the trajectory limiter
- `double StandardAnalogInput0 { get; set; }`: Standard analog input 0 [mA or V]
- `double StandardAnalogInput1 { get; set; }`: Standard analog input 1 [mA or V]
- `double StandardAnalogOutput0 { get; set; }`: Standard analog output 0 [mA or V]
- `double StandardAnalogOutput1 { get; set; }`: Standard analog output 1 [mA or V]
- `JointsDoubleValues TargetCurrent { get; set; }`: Target joint currents
- `JointsDoubleValues TargetMoment { get; set; }`: Target joint moments (torques)
- `JointsDoubleValues TargetQ { get; set; }`: Target joint positions
- `JointsDoubleValues TargetQd { get; set; }`: Target joint velocities
- `JointsDoubleValues TargetQdd { get; set; }`: Target joint accelerations
- `double TargetSpeedFraction { get; set; }`: Target speed fraction
- `Pose TargetTcpPose { get; set; }`: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `Pose TargetTcpSpeed { get; set; }`: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `double TcpForceScalar { get; set; }`: TCP force scalar [N]
- `double Timestamp { get; set; }`: Time elapsed since the controller was started [s]
- `double ToolAnalogInput0 { get; set; }`: Tool analog input 0 [mA or V]
- `double ToolAnalogInput1 { get; set; }`: Tool analog input 1 [mA or V]
- `uint ToolAnalogInputTypes { get; set; }`: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- `byte ToolDigitalOutput0mode { get; set; }`: The current mode of digital output 0
- `byte ToolDigitalOutput1Mode { get; set; }`: The current mode of digital output 1
- `uint ToolMode { get; set; }`: Tool mode
- `double ToolOutputCurrent { get; set; }`: Tool current [mA]
- `byte ToolOutputMode { get; set; }`: The current output mode
- `int ToolOutputVoltage { get; set; }`: Tool output voltage [V]
- `double ToolTemperature { get; set; }`: Tool temperature in degrees Celsius
- Inherited from [RtdeBaseValues](../api/UnderAutomation.UniversalRobots.Rtde.md#rtdebasevalues-robotrtdeoutputdatavalues): `Values`

## What to read next

- [Read and write registers](registers.md): exchange values with the robot program.
- [Get the robot position](how-to-get-position.md) and [Read and write I/O](how-to-read-write-io.md).
