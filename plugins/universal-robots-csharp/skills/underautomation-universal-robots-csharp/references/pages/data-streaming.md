# Primary Interface: data streaming

Receive the state of a UR cobot at 10 Hz with the Primary Interface: robot mode, joints, tool, I/O, Cartesian position, kinematics and configuration.

Web page: https://underautomation.com/universal-robots/documentation/data-streaming

The Primary Interface of a Universal Robots cobot sends the state of the robot 10 times per second: modes, joints, tool, I/O, Cartesian position, kinematics, configuration and messages. This page shows how to connect to it and read its data. The same connection sends URScript: see [Send URScript](remote-send-script.md).

## Connect

The Primary Interface is enabled by default: `Connect("192.168.0.1")` opens it. With a `ConnectParameters`, you can also choose the port:

| Port  | `Interfaces`                 | Data          | URScript |
| ----- | ---------------------------- | ------------- | -------- |
| 30001 | `PrimaryInterface` (default) | All packages  | yes      |
| 30002 | `SecondaryInterface`         | All packages  | yes      |
| 30011 | `PrimaryInterfaceReadOnly`   | All packages  | no       |
| 30012 | `SecondaryInterfaceReadOnly` | All packages  | no       |

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.PrimaryInterface;

class PrimaryInterface
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // The Primary Interface is enabled by default
    parameters.PrimaryInterface.Enable = true;

    // Port 30001 (default) accepts URScript. The read only ports do not
    parameters.PrimaryInterface.Port = Interfaces.PrimaryInterface;

    robot.Connect(parameters);

    // The last values received are in the properties of the client
    double baseSpeed = robot.PrimaryInterface.JointData.Base.ActualSpeed;

    // Close the Primary Interface only
    robot.PrimaryInterface.Disconnect();

    // Close every service
    robot.Disconnect();
  }
}
```

The same client works without `UR`:

```csharp
using UnderAutomation.UniversalRobots.PrimaryInterface;

class PrimaryInterfaceDirect
{
  static void Main(string[] args)
  {
    // A Primary Interface client, without a UR instance
    var client = new PrimaryInterfaceClient();

    client.Connect("192.168.0.1", Interfaces.PrimaryInterface);

    double baseSpeed = client.JointData.Base.ActualSpeed;

    client.Disconnect();
  }
}
```

The service `Primary Client Interface` must be enabled on the robot: see [Prepare the robot](connect.md#prepare_the_robot). For the data of the interface, see [Remote control via TCP/IP](https://www.universal-robots.com/articles/ur/interface-communication/remote-control-via-tcpip/) by Universal Robots.

## Read the data

Each package of the robot has a property, which holds the last values received, and an event, raised when the package arrives. A property is `null` until its first package: wait about 100 ms after the connection.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.PrimaryInterface;

class PrimaryInterfaceData
{
  static void Main(string[] args)
  {
    var robot = new UR();

    robot.Connect("192.168.0.1");

    // Last package received, read at any time
    JointDataPackageEventArgs joints = robot.PrimaryInterface.JointData;
    double shoulder = joints.Shoulder.Position; // rad

    CartesianInfoPackageEventArgs tool = robot.PrimaryInterface.CartesianInfo;
    double x = tool.X; // m

    // Or an event, raised when a package arrives (10 Hz)
    robot.PrimaryInterface.JointDataReceived += (sender, e) =>
    {
      double wrist3Speed = e.Wrist3.ActualSpeed; // rad/s
    };

    robot.PrimaryInterface.RobotModeDataReceived += (sender, e) =>
    {
      bool programRunning = e.ProgramRunning;
    };
  }
}
```

The sections below list the content of each package.

## State of the connection

`Connected` becomes `false` when the connection is lost (robot stopped, cable unplugged). No event is raised and there is no automatic reconnection: call `Connect` again. `InternalErrorOccured` is raised when the SDK meets an error.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;

class PrimaryInterfaceStatus
{
  static void Main(string[] args)
  {
    var robot = new UR();

    robot.Connect("192.168.0.1");

    // false after a loss of the connection. There is no automatic reconnection
    bool connected = robot.PrimaryInterface.Connected;

    if (!connected)
      robot.Connect("192.168.0.1");

    // Raised when an error happens in the background
    robot.PrimaryInterface.InternalErrorOccured += (sender, e) =>
    {
      Exception exception = e.Exception;
      string message = e.Message;
      StatusCode status = e.Status;
    };
  }
}
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Packages

### Robot mode

**C# : RobotModeData**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  RobotModeDataPackageEventArgs _value = ur.PrimaryInterface.RobotModeData;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.RobotModeDataReceived += Ur_RobotModeDataReceived;
}

private void Ur_RobotModeDataReceived(object sender, RobotModeDataPackageEventArgs e) {
  // e contains the incoming package
}
```

**RobotModeDataPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#robotmodedatapackageeventargs-robotprimaryinterfacerobotmodedata))

- `RobotModeDataPackageEventArgs()`
- `ControlModes ControlMode { get; set; }`: Current robot control mode
- `bool EmergencyStopped { get; set; }`: The button Emergency Stop is pressed
- `bool PhysicalRobotConnected { get; set; }`: Robot is connected to its controller
- `bool ProgramPaused { get; set; }`: The running program is paused
- `bool ProgramRunning { get; set; }`: A program is running
- `bool ProtectiveStopped { get; set; }`: A stop occured due to a fault detection
- `bool RealRobotEnabled { get; set; }`: Real robot mode active. False if robot is in simulation
- `RobotModes RobotMode { get; set; }`: Current robot running mode
- `bool RobotPowerOn { get; set; }`: Robot is powered on and boot is completed. If false, you need to press "ON" button to power it on
- `double SpeedScaling { get; set; }`: Speed scaling
- `double TargetSpeedFraction { get; set; }`: Overriden speed ratio between 0 (0%) and 1 (100%)
- `double TargetSpeedFractionLimit { get; set; }`: Maximum target speed fraction
- `TimeSpan Timestamp { get; set; }`: Timespan since the robot controller has started
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

**ControlModes** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#controlmodes-robotprimaryinterfacerobotmodedatacontrolmode))

- Force: Robot is force controlled. (For example : URScript force_mode() function is called)
- Position: Robot is position controlled
- Teach: The robot is hand guided by pushing teached button
- Torque: Robot is torque controlled

**RobotModes** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#robotmodes-robotprimaryinterfacerobotmodedatarobotmode))

- BackDrive: The robot is hand guided by pushing teached button
- Booting: The robot controller is booting
- ConfirmSafety: Robot has stopped due to a Safety Stop
- Disconnected: Robot is not connected to its controller
- Idle: Power is on but breaks are not released
- Other: Robot is in an obsolete CB2 mode
- PowerOff: The robot is powered off
- PowerOn: The robot is powered on
- Running: Robot is in normal mode
- UpdatingFirmware: Firmware is upgrading

### Joint data

**C# : JointData**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  JointDataPackageEventArgs _value = ur.PrimaryInterface.JointData;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.JointDataReceived += Ur_JointDataReceived;
}

private void Ur_JointDataReceived(object sender, JointDataPackageEventArgs e) {
  // e contains the incoming package
}
```

**JointDataPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#jointdatapackageeventargs-robotprimaryinterfacejointdata))

- `JointDataPackageEventArgs()`
- `JointData Base { get; set; }`: Base joint data
- `JointData Elbow { get; set; }`: Elbow joint data
- `JointData Shoulder { get; set; }`: Shoulder joint data
- `JointData Wrist1 { get; set; }`: Wrist1 joint data
- `JointData Wrist2 { get; set; }`: Wrist2 joint data
- `JointData Wrist3 { get; set; }`: Wrist3 (Tool) joint data
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

![Joints of a UR robot](https://underautomation.com/universal-robots/joints.png)

**JointData** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#jointdata-robotprimaryinterfacejointdatabase))

- `JointData()`
- `double ActualSpeed { get; set; }`: Joint rotation speed in rad/s
- `float Current { get; set; }`: Motor current in Amps
- `JointModes JointMode { get; set; }`: Joint mode
- `double Position { get; set; }`: Angular joint position in radian
- `double TargetPosition { get; set; }`: Angular target position in radian
- `float Temperature { get; set; }`: Joint temperature in °C
- `float Voltage { get; set; }`: Motor voltage in Volts

**JointModes** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#jointmodes-robotprimaryinterfacejointdatabasejointmode))

- Backdrive: Joint is in backdrive mode.
- Booting: Joint is booting.
- Bootloader: Joint is in bootloader mode.
- Calibration: Joint is calibrating.
- Fault: Joint is in a fault state.
- Idle: Joint is idle.
- MotorInitialisation: Joint motor is initializing.
- NotResponding: Joint is not responding.
- PartDCalibration: Joint is in part D calibration mode.
- PartDCalibrationError: Joint part D calibration encountered an error.
- PowerOff: Joint is powered off.
- Running: Joint is running normally.
- ShuttingDown: Joint is shutting down.

### Tool data

**C# : ToolData**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  ToolDataPackageEventArgs _value = ur.PrimaryInterface.ToolData;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.ToolDataReceived += Ur_ToolDataReceived;
}

private void Ur_ToolDataReceived(object sender, ToolDataPackageEventArgs e) {
  // e contains the incoming package
}
```

**ToolDataPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#tooldatapackageeventargs-robotprimaryinterfacetooldata))

- `ToolDataPackageEventArgs()`
- `double AnalogInput2 { get; set; }`: Value of Analog input 2 (analog_in[2])
- `double AnalogInput3 { get; set; }`: Value of Analog input 3 (analog_in[3])
- `AnalogRanges AnalogInputRange2 { get; set; }`: Unit of analog input 2 (analog_in[2])
- `AnalogRanges AnalogInputRange3 { get; set; }`: Unit of analog input 3 (analog_in[3])
- `float ToolCurrent { get; set; }`: Tool current in Amps
- `ToolModes ToolMode { get; set; }`: Tool mode
- `sbyte ToolOutputVoltage { get; set; }`: Tool output voltage
- `float ToolTemperature { get; set; }`: Tool Temperature in °C
- `float ToolVoltage48V { get; set; }`: Actual robot voltage power supply
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

**AnalogRanges** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#analogranges-robotprimaryinterfacetooldataanaloginputrange2))

- Current: The analog value is in Amps (A)
- Voltage: The analog value is in Volts (V)

**ToolModes** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#toolmodes-robotprimaryinterfacetooldatatoolmode))

- Bootloader: Bootloader
- Idle: Idle
- Running: Running

### Masterboard data

**C# : MasterboardData**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  MasterboardDataPackageEventArgs _value = ur.PrimaryInterface.MasterboardData;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.MasterboardDataReceived += Ur_MasterboardDataReceived;
}

private void Ur_MasterboardDataReceived(object sender, MasterboardDataPackageEventArgs e) {
  // e contains the incoming package
}
```

**MasterboardDataPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#masterboarddatapackageeventargs-robotprimaryinterfacemasterboarddata))

- `MasterboardDataPackageEventArgs()`
- `double AnalogInput0 { get; set; }`: Value of analog input 0 (analog_in[0])
- `double AnalogInput1 { get; set; }`: Value of analog input 1 (analog_in[1])
- `AnalogRanges AnalogInputRange0 { get; set; }`: Unit of analog input 0 (analog_in[0])
- `AnalogRanges AnalogInputRange1 { get; set; }`: Unit of analog input 1 (analog_in[1])
- `double AnalogOutput0 { get; set; }`: Value of analog output 0 (analog_out[0])
- `double AnalogOutput1 { get; set; }`: Value of analog output 1 (analog_out[1])
- `AnalogRanges AnalogOutputDomain0 { get; set; }`: Unit of analog output 0 (analog_out[0])
- `AnalogRanges AnalogOutputDomain1 { get; set; }`: Unit of analog output 1 (analog_out[1])
- `MasterboardDigitalIO DigitalInputs { get; set; }`: Register where each bit is a digital input value
- `MasterboardDigitalIO DigitalOutputs { get; set; }`: Register where each bit is a digital output value
- `sbyte Euromap67Installed { get; set; }`: The robot is interfaced to injection molding machines Euromap 67
- `float EuromapCurrent { get; set; }`: Euromap current
- `int EuromapInputBits { get; set; }`: Register where each bit is a digital Euromap input
- `int EuromapOutputBits { get; set; }`: Register where each bit is a digital Euromap output
- `float EuromapVoltage { get; set; }`: Euromap voltage
- `byte InReducedMode { get; set; }`: Robot is in reduced speed mode
- `float MasterIOCurrent { get; set; }`: Current of all digital and analog inputs and outputs
- `float MasterboardTemperature { get; set; }`: Temperature of masterboard in °C
- `byte OperationalModeSelectorInput { get; set; }`: Position of operational mode selector input switch
- `float RobotCurrent { get; set; }`: Robot current consumption in Amps
- `float RobotVoltage48V { get; set; }`: Voltage of internal 48V power supply
- `SafetyStatus Safetymode { get; set; }`: Masterboard safety mode
- `byte ThreePositionEnablingDeviceInput { get; set; }`: Position of the 3-position enabling device
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

**MasterboardDigitalIO** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#masterboarddigitalio-robotprimaryinterfacemasterboarddatadigitalinputs))

- `BitArray BitArray { get; }`: Register value seen as a bool array
- `bool Configurable0 { get; }`: State of configurable digital I/O pin 0.
- `bool Configurable1 { get; }`: State of configurable digital I/O pin 1.
- `bool Configurable2 { get; }`: State of configurable digital I/O pin 2.
- `bool Configurable3 { get; }`: State of configurable digital I/O pin 3.
- `bool Configurable4 { get; }`: State of configurable digital I/O pin 4.
- `bool Configurable5 { get; }`: State of configurable digital I/O pin 5.
- `bool Configurable6 { get; }`: State of configurable digital I/O pin 6.
- `bool Configurable7 { get; }`: State of configurable digital I/O pin 7.
- `bool Digital0 { get; }`: State of standard digital I/O pin 0.
- `bool Digital1 { get; }`: State of standard digital I/O pin 1.
- `bool Digital2 { get; }`: State of standard digital I/O pin 2.
- `bool Digital3 { get; }`: State of standard digital I/O pin 3.
- `bool Digital4 { get; }`: State of standard digital I/O pin 4.
- `bool Digital5 { get; }`: State of standard digital I/O pin 5.
- `bool Digital6 { get; }`: State of standard digital I/O pin 6.
- `bool Digital7 { get; }`: State of standard digital I/O pin 7.
- `bool ToolDigital0 { get; }`: State of tool digital I/O pin 0.
- `bool ToolDigital1 { get; }`: State of tool digital I/O pin 1.
- `int Value { get; }`: Register value

**SafetyStatus** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#safetystatus-robotprimaryinterfacemasterboarddatasafetymode))

- AutomaticModeSafeguardStop: Automatic mode safeguard stop is active.
- Fault: Safety is in fault mode
- Normal: Safety is in normal operating conditions
- ProtectiveStop: Protective safeguard Stop. This safety function is triggeredby an external protective device using safety inputs which will trigger a Cat 2 stop3per IEC 60204-1.
- Recovery: When a safety limit is violated, the safety system must be restarted.
- Reduced: Speed is reduced
- RobotEmergencyStop: (EA + EB + SBUS-&gt;Screen) Physical e-stop interface input activated
- SafeguardStop: (SI0 + SI1 + SBUS) Physical s-stop interface input
- SystemEmergencyStop: (EA + EB + SBUS-&gt;Euromap67) Physical e-stop interface input activated
- SystemThreePositionEnablingStop: System three-position enabling device stop is active.
- Violation: Safety is in violation mode (for example, violation of the allowed delay between redundant signals)

### Cartesian information

**C# : CartesianInfo**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  CartesianInfoPackageEventArgs _value = ur.PrimaryInterface.CartesianInfo;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.CartesianInfoReceived += Ur_CartesianInfoReceived;
}

private void Ur_CartesianInfoReceived(object sender, CartesianInfoPackageEventArgs e) {
  // e contains the incoming package
}
```

**CartesianInfoPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#cartesianinfopackageeventargs-robotprimaryinterfacecartesianinfo))

- `CartesianInfoPackageEventArgs()`
- `Pose AsPose()`: Returns the current cartesian position as a Pose object
- `Pose AsTCPOffsetPose()`: Returns the TCP offset as a Pose object
- `double Rx { get; set; }`: RX axis coordinate in rad of the TCP in the current frame
- `double Ry { get; set; }`: RY axis coordinate in rad of the TCP in the current frame
- `double Rz { get; set; }`: RZ axis coordinate in rad of the TCP in the current frame
- `double TCPOffsetRX { get; set; }`: RX position of the TCP in the flange frame in rad
- `double TCPOffsetRY { get; set; }`: RY position of the TCP in the flange frame in rad
- `double TCPOffsetRZ { get; set; }`: RZ position of the TCP in the flange frame in rad
- `double TCPOffsetX { get; set; }`: X position of the TCP in the flange frame in meter
- `double TCPOffsetY { get; set; }`: Y position of the TCP in the flange frame in meter
- `double TCPOffsetZ { get; set; }`: Z position of the TCP in the flange frame in meter
- `double X { get; set; }`: X axis coordinate in meter of the TCP in the current frame
- `double Y { get; set; }`: Y axis coordinate in meter of the TCP in the current frame
- `double Z { get; set; }`: Z axis coordinate in meter of the TCP in the current frame
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

![Flange frame](https://underautomation.com/universal-robots/flange-frame-3d.png)

![Flange frame, projection](https://underautomation.com/universal-robots/flange-frame-projection.png)

### Kinematics information

**C# : KinematicsInfo**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  KinematicsInfoPackageEventArgs _value = ur.PrimaryInterface.KinematicsInfo;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.KinematicsInfoReceived += Ur_KinematicsInfoReceived;
}

private void Ur_KinematicsInfoReceived(object sender, KinematicsInfoPackageEventArgs e) {
  // e contains the incoming package
}
```

**KinematicsInfoPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#kinematicsinfopackageeventargs-robotprimaryinterfacekinematicsinfo))

- `KinematicsInfoPackageEventArgs()`
- `double A2 { get; }`: DH parameter a2 (Shoulder.DHa)
- `double A3 { get; }`: DH parameter a3 (Elbow.DHa)
- `JointKinematicsInfo Base { get; set; }`: Base kinematics info
- `int CalibrationStatus { get; set; }`: Calibration status (0 : OK)
- `double D1 { get; }`: DH parameter d1 (Base.DHd)
- `double D4 { get; }`: DH parameter d4 (Wrist1.DHd)
- `double D5 { get; }`: DH parameter d5 (Wrist2.DHd)
- `double D6 { get; }`: DH parameter d6 (Wrist3.DHd)
- `JointKinematicsInfo Elbow { get; set; }`: Elbow kinematics info
- `JointKinematicsInfo Shoulder { get; set; }`: Shoulder kinematics info
- `JointKinematicsInfo Wrist1 { get; set; }`: Wrist1 kinematics info
- `JointKinematicsInfo Wrist2 { get; set; }`: Wrist2 kinematics info
- `JointKinematicsInfo Wrist3 { get; set; }`: Wrist3 (Tool) kinematics info
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

**JointKinematicsInfo** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#jointkinematicsinfo-robotprimaryinterfacekinematicsinfobase))

- `JointKinematicsInfo()`
- `int Checksum { get; set; }`: Joint checksum
- `double DHa { get; set; }`: DH convention a parameter
- `double DHd { get; set; }`: DH convention d parameter
- `double DHtheta { get; set; }`: DH convention theta parameter
- `double Dhalpha { get; set; }`: DH convention alpha parameter

These are the Denavit-Hartenberg parameters of the robot, with its calibration. See [Kinematics](kinematics.md) and the [DH parameters](https://www.universal-robots.com/articles/ur/application-installation/dh-parameters-for-calculations-of-kinematics-and-dynamics/) of each model.

### Configuration data

**C# : ConfigurationData**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  ConfigurationDataPackageEventArgs _value = ur.PrimaryInterface.ConfigurationData;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.ConfigurationDataReceived += Ur_ConfigurationDataReceived;
}

private void Ur_ConfigurationDataReceived(object sender, ConfigurationDataPackageEventArgs e) {
  // e contains the incoming package
}
```

**ConfigurationDataPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#configurationdatapackageeventargs-robotprimaryinterfaceconfigurationdata))

- `ConfigurationDataPackageEventArgs()`
- `double A2 { get; }`: DH parameter a2 (Shoulder.DHa)
- `double A3 { get; }`: DH parameter a3 (Elbow.DHa)
- `double AJointDefault { get; set; }`: Default joint acceleration speed in rad/s²
- `double AToolDefault { get; set; }`: Default TCP acceleration speed in m/s²
- `JointConfiguration Base { get; set; }`: Base joint configuration
- `ControllerBoxTypes ControllerBoxType { get; set; }`: Controller box type
- `double D1 { get; }`: DH parameter d1 (Base.DHd)
- `double D4 { get; }`: DH parameter d4 (Wrist1.DHd)
- `double D5 { get; }`: DH parameter d5 (Wrist2.DHd)
- `double D6 { get; }`: DH parameter d6 (Wrist3.DHd)
- `JointConfiguration Elbow { get; set; }`: Elbow joint configuration
- `double EqRadius { get; set; }`: Equipment radius in meter
- `int MasterboardVersion { get; set; }`: Masterboard version
- `RobotSubTypes RobotSubType { get; set; }`: Robot series (e-Series, CB-Series, etc.)
- `RobotModels RobotType { get; set; }`: Model of the robot (UR3, UR5, UR10, UR16, ...)
- `JointConfiguration Shoulder { get; set; }`: Shoulder joint configuration
- `double VJointDefault { get; set; }`: Default joint angular speed in rad/s
- `double VToolDefault { get; set; }`: Default TCP speed speed in m/s
- `JointConfiguration Wrist1 { get; set; }`: Wrist1 joint configuration
- `JointConfiguration Wrist2 { get; set; }`: Wrist2 joint configuration
- `JointConfiguration Wrist3 { get; set; }`: Wrist3 (Tool) joint configuration
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

**ControllerBoxTypes** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#controllerboxtypes-robotprimaryinterfaceconfigurationdatacontrollerboxtype))

- UR10: UR10 controller box
- UR16: UR16 controller box
- UR20: UR20 controller box
- UR3: UR3 controller box
- UR30: UR30 controller box
- UR5: UR5 controller box

**JointConfiguration** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#jointconfiguration-robotprimaryinterfaceconfigurationdatabase))

- `JointConfiguration()`
- `double DHa { get; set; }`: a parameter of Denavit–Hartenberg (DH) convention
- `double DHalpha { get; set; }`: Alpha parameter of Denavit–Hartenberg (DH) convention
- `double DHd { get; set; }`: d parameter of Denavit–Hartenberg (DH) convention
- `double DHtheta { get; set; }`: Theta parameter of Denavit–Hartenberg (DH) convention
- `double JointMaxAcceleration { get; set; }`: Maximum rotation speed in rad/s²
- `double JointMaxLimit { get; set; }`: Maximum angular position in rad
- `double JointMaxSpeed { get; set; }`: Maximum rotation speed in rad/s
- `double JointMinLimit { get; set; }`: Minimum angular position in rad

**RobotSubTypes** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#robotsubtypes-robotprimaryinterfaceconfigurationdatarobotsubtype))

- CB2Serie: CB2-series (Firmware 1.x)
- CB3Serie: CB3-series (Firmware 3.x)
- ESerie: e-series (Firmware 5.x)

**RobotModels** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#robotmodels-robotprimaryinterfaceconfigurationdatarobottype))

- UR10: UR10 robot model.
- UR16: UR16 robot model.
- UR18: UR18 robot model.
- UR20: UR20 robot model.
- UR3: UR3 robot model.
- UR30: UR30 robot model.
- UR5: UR5 robot model.
- UR8L: UR8 Long robot model.

### Force mode data

**C# : ForceModeData**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  ForceModeDataPackageEventArgs _value = ur.PrimaryInterface.ForceModeData;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.ForceModeDataReceived += Ur_ForceModeDataReceived;
}

private void Ur_ForceModeDataReceived(object sender, ForceModeDataPackageEventArgs e) {
  // e contains the incoming package
}
```

**ForceModeDataPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#forcemodedatapackageeventargs-robotprimaryinterfaceforcemodedata))

- `ForceModeDataPackageEventArgs()`
- `double RobotDexterity { get; set; }`: Dexterity of the robot
- `double Rx { get; set; }`: Rx torque in tool frame in Nm
- `double Ry { get; set; }`: Ry torque in tool frame in Nm
- `double Rz { get; set; }`: Rz torque in tool frame in Nm
- `double X { get; set; }`: X force in tool frame in N
- `double Y { get; set; }`: Y force in tool frame in N
- `double Z { get; set; }`: Z force in tool frame in N
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

### Additional information

**C# : AdditionalInfo**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  AdditionalInfoPackageEventArgs _value = ur.PrimaryInterface.AdditionalInfo;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.AdditionalInfoReceived += Ur_AdditionalInfoReceived;
}

private void Ur_AdditionalInfoReceived(object sender, AdditionalInfoPackageEventArgs e) {
  // e contains the incoming package
}
```

**AdditionalInfoPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#additionalinfopackageeventargs-robotprimaryinterfaceadditionalinfo))

- `AdditionalInfoPackageEventArgs()`
- `bool FreedriveButtonEnabled { get; set; }`: The free drive button is enabled
- `bool FreedriveButtonPressed { get; set; }`: The free drive button is pressed
- `bool IOEnabledFreedrive { get; set; }`: Free drive is enable via IO
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

### Calibration data

**C# : CalibrationData**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  CalibrationDataPackageEventArgs _value = ur.PrimaryInterface.CalibrationData;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.CalibrationDataReceived += Ur_CalibrationDataReceived;
}

private void Ur_CalibrationDataReceived(object sender, CalibrationDataPackageEventArgs e) {
  // e contains the incoming package
}
```

**CalibrationDataPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#calibrationdatapackageeventargs-robotprimaryinterfacecalibrationdata))

- `CalibrationDataPackageEventArgs()`
- `double Frx { get; set; }`: Frx calibration data
- `double Fry { get; set; }`: Fry calibration data
- `double Frz { get; set; }`: Frz calibration data
- `double Fx { get; set; }`: Fx calibration data
- `double Fy { get; set; }`: Fy calibration data
- `double Fz { get; set; }`: Fz calibration data
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

### Safety data

**C# : SafetyData**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  SafetyDataPackageEventArgs _value = ur.PrimaryInterface.SafetyData;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.SafetyDataReceived += Ur_SafetyDataReceived;
}

private void Ur_SafetyDataReceived(object sender, SafetyDataPackageEventArgs e) {
  // e contains the incoming package
}
```

**SafetyDataPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#safetydatapackageeventargs-robotprimaryinterfacesafetydata))

- `SafetyDataPackageEventArgs()`
- `byte[] Data { get; set; }`: Irrelevant (Internal use only)
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

### Tool communication information

**C# : ToolCommunicationInfo**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  ToolCommunicationInfoPackageEventArgs _value = ur.PrimaryInterface.ToolCommunicationInfo;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.ToolCommunicationInfoReceived += Ur_ToolCommunicationInfoReceived;
}

private void Ur_ToolCommunicationInfoReceived(object sender, ToolCommunicationInfoPackageEventArgs e) {
  // e contains the incoming package
}
```

**ToolCommunicationInfoPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#toolcommunicationinfopackageeventargs-robotprimaryinterfacetoolcommunicationinfo))

- `ToolCommunicationInfoPackageEventArgs()`
- `int BaudRate { get; set; }`: Baud rate for tool serial communication
- `int Parity { get; set; }`: Parity
- `float RxIdleChars { get; set; }`: RX Idle Chars
- `int StopBits { get; set; }`: Stop bits
- `bool ToolCommunicationIsEnabled { get; set; }`: Is the tool communication interface enabled
- `float TxIdleChars { get; set; }`: TX Idle Chars
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

### Tool mode

**C# : ToolModeInfo**
```csharp
private UR ur;

private void Start() {
  ur = new UR();
  ur.Connect("192.168.0.1");

  // Direct access to last received package
  ToolModeInfoPackageEventArgs _value = ur.PrimaryInterface.ToolModeInfo;

  // Attach a delegate to the event triggered when new package comes
  ur.PrimaryInterface.ToolModeInfoReceived += Ur_ToolModeInfoReceived;
}

private void Ur_ToolModeInfoReceived(object sender, ToolModeInfoPackageEventArgs e) {
  // e contains the incoming package
}
```

**ToolModeInfoPackageEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#toolmodeinfopackageeventargs-robotprimaryinterfacetoolmodeinfo))

- `ToolModeInfoPackageEventArgs()`
- `DigitalOutputConfigurations DigitalOutputMode0 { get; set; }`: Digital output 0 configuration
- `DigitalOutputConfigurations DigitalOutputMode1 { get; set; }`: Digital output 1 configuration
- `OutputModes OutputMode { get; set; }`: Digital output mode
- Inherited from [PackageEventArgs](../api/UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

**DigitalOutputConfigurations** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#digitaloutputconfigurations-robotprimaryinterfacetoolmodeinfodigitaloutputmode0))

- PushPull: Push / Pull
- SinkingNPN: Sinking (NOPN)
- SourcingPNP: Sourcing (PNP)

**OutputModes** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#outputmodes-robotprimaryinterfacetoolmodeinfooutputmode))

- DualPinPower: Dual Pin Power
- StandardOutput: Standard output

## What to read next

- [Send URScript](remote-send-script.md): run URScript from the PC.
- [Read and write variables](variables.md): the program and installation variables.
- [RTDE](rtde.md): the same data, up to 500 Hz.
