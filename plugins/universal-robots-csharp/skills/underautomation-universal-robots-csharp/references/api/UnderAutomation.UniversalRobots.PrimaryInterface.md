# UnderAutomation.UniversalRobots.PrimaryInterface

## AdditionalInfoPackageEventArgs (robot.PrimaryInterface.AdditionalInfo)

`class AdditionalInfoPackageEventArgs : PackageEventArgs`

Additional information

- `AdditionalInfoPackageEventArgs()`
- `bool FreedriveButtonEnabled { get; set; }`: The free drive button is enabled
- `bool FreedriveButtonPressed { get; set; }`: The free drive button is pressed
- `bool IOEnabledFreedrive { get; set; }`: Free drive is enable via IO
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## CalibrationDataPackageEventArgs (robot.PrimaryInterface.CalibrationData)

`class CalibrationDataPackageEventArgs : PackageEventArgs`

Calibration data

- `CalibrationDataPackageEventArgs()`
- `double Frx { get; set; }`: Frx calibration data
- `double Fry { get; set; }`: Fry calibration data
- `double Frz { get; set; }`: Frz calibration data
- `double Fx { get; set; }`: Fx calibration data
- `double Fy { get; set; }`: Fy calibration data
- `double Fz { get; set; }`: Fz calibration data
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## CartesianInfoPackageEventArgs (robot.PrimaryInterface.CartesianInfo)

`class CartesianInfoPackageEventArgs : PackageEventArgs`

Contains current cartesian position of the robot, including its TCP offset

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
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## ConfigurationDataPackageEventArgs (robot.PrimaryInterface.ConfigurationData)

`class ConfigurationDataPackageEventArgs : PackageEventArgs, IUrDhParameters`

Joint configuration

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
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## ForceModeDataPackageEventArgs (robot.PrimaryInterface.ForceModeData)

`class ForceModeDataPackageEventArgs : PackageEventArgs`

Force mode data

- `ForceModeDataPackageEventArgs()`
- `double RobotDexterity { get; set; }`: Dexterity of the robot
- `double Rx { get; set; }`: Rx torque in tool frame in Nm
- `double Ry { get; set; }`: Ry torque in tool frame in Nm
- `double Rz { get; set; }`: Rz torque in tool frame in Nm
- `double X { get; set; }`: X force in tool frame in N
- `double Y { get; set; }`: Y force in tool frame in N
- `double Z { get; set; }`: Z force in tool frame in N
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## GlobalVariables (robot.PrimaryInterface.GlobalVariables)

`class GlobalVariables`

List of all global variables

- `GlobalVariablesFirmwareVersion FirmwareVersion { get; }`: Indicates which decoder is used used to read variables according to firmware version
- `GlobalVariable[] GetAll()`: Returns a list of all variables declared in the robot
- `GlobalVariable GetByName(string name)`: Get a variable by its name. Null is returned if the variable doesn't exist
- `event EventHandler<GlobalVariablesEventArgs> ListUpdated`: Event raised whan the variable list changed. For example, after a program starts
- `event EventHandler<GlobalVariablesEventArgs> ValuesUpdated`: Event raised at 10Hz when variable values are updated

## GlobalVariablesEventArgs

`class GlobalVariablesEventArgs : EventArgs`

Event args of variable update events

- `GlobalVariable[] Variables { get; }`: New list of all up to date variables

## GlobalVariablesFirmwareVersion (robot.PrimaryInterface.GlobalVariables.FirmwareVersion)

`enum GlobalVariablesFirmwareVersion`

Firmware version for variable decoding

- Latest: Recent firmware
- UpTo32: FW up to 3.2
- UpTo59: FW up to 5.9

## Interfaces (robot.PrimaryInterface.Port)

`enum Interfaces`

TCP ports to communicate with an UR controller

- PrimaryInterface: The default port that allow reading data and sending URScript
- PrimaryInterfaceReadOnly: This port can only read data. It is unable to send URScript.
- SecondaryInterface: The secondary port with same features as PrimaryClient
- SecondaryInterfaceReadOnly: A secondary port that can only read data. It is unable to send URScript.

## JointConfiguration (robot.PrimaryInterface.ConfigurationData.Base)

`class JointConfiguration`

Joint configuration

- `JointConfiguration()`
- `double DHa { get; set; }`: a parameter of Denavit–Hartenberg (DH) convention
- `double DHalpha { get; set; }`: Alpha parameter of Denavit–Hartenberg (DH) convention
- `double DHd { get; set; }`: d parameter of Denavit–Hartenberg (DH) convention
- `double DHtheta { get; set; }`: Theta parameter of Denavit–Hartenberg (DH) convention
- `double JointMaxAcceleration { get; set; }`: Maximum rotation speed in rad/s²
- `double JointMaxLimit { get; set; }`: Maximum angular position in rad
- `double JointMaxSpeed { get; set; }`: Maximum rotation speed in rad/s
- `double JointMinLimit { get; set; }`: Minimum angular position in rad

## JointData (robot.PrimaryInterface.JointData.Base)

`class JointData`

Joint data

- `JointData()`
- `double ActualSpeed { get; set; }`: Joint rotation speed in rad/s
- `float Current { get; set; }`: Motor current in Amps
- `JointModes JointMode { get; set; }`: Joint mode
- `double Position { get; set; }`: Angular joint position in radian
- `double TargetPosition { get; set; }`: Angular target position in radian
- `float Temperature { get; set; }`: Joint temperature in °C
- `float Voltage { get; set; }`: Motor voltage in Volts

## JointDataPackageEventArgs (robot.PrimaryInterface.JointData)

`class JointDataPackageEventArgs : PackageEventArgs`

Status of each joints

- `JointDataPackageEventArgs()`
- `JointData Base { get; set; }`: Base joint data
- `JointData Elbow { get; set; }`: Elbow joint data
- `JointData Shoulder { get; set; }`: Shoulder joint data
- `JointData Wrist1 { get; set; }`: Wrist1 joint data
- `JointData Wrist2 { get; set; }`: Wrist2 joint data
- `JointData Wrist3 { get; set; }`: Wrist3 (Tool) joint data
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## JointKinematicsInfo (robot.PrimaryInterface.KinematicsInfo.Base)

`class JointKinematicsInfo`

Joint kinematics info, Denavit–Hartenberg (DH) parameters

- `JointKinematicsInfo()`
- `int Checksum { get; set; }`: Joint checksum
- `double DHa { get; set; }`: DH convention a parameter
- `double DHd { get; set; }`: DH convention d parameter
- `double DHtheta { get; set; }`: DH convention theta parameter
- `double Dhalpha { get; set; }`: DH convention alpha parameter

## KeyMessageEventArgs (robot.PrimaryInterface.KeyMessage)

`class KeyMessageEventArgs : PackageEventArgs`

Internal robot events (such as starting or stopping a program)

- `KeyMessageEventArgs()`
- `string KeyTextMessage { get; set; }`: Message key
- `int RobotMessageArgument { get; set; }`: Message argument
- `int RobotMessageCode { get; set; }`: Message code
- `string RobotMessageTitle { get; set; }`: Message title
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## KinematicsInfoPackageEventArgs (robot.PrimaryInterface.KinematicsInfo)

`class KinematicsInfoPackageEventArgs : PackageEventArgs, IUrDhParameters`

Kinematics info

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
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## MasterboardDataPackageEventArgs (robot.PrimaryInterface.MasterboardData)

`class MasterboardDataPackageEventArgs : PackageEventArgs`

Masterboard data

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
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## MasterboardDigitalIO (robot.PrimaryInterface.MasterboardData.DigitalInputs)

`class MasterboardDigitalIO`

Represents the state of digital I/O pins on the UR controller masterboard, including standard digital, configurable, and tool digital pins.

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

## PackageDescriptionAttribute

`class PackageDescriptionAttribute : DescriptionAttribute`

Describes a field of a received package

- `PackageDescriptionAttribute(string description)`: Initializes a new instance with no physical unit.
- `PackageDescriptionAttribute(string description, PackageUnit unit)`: Initializes a new instance with a specified physical unit.
- `PackageUnit Unit { get; }`: Physical unit of the field

## PackageUnit

`enum PackageUnit`

Physical units of receives measures

- Amp: A
- CelsiusDegree: °C
- Meter: m
- MeterPerSecond: m/s
- MetersPerSecondSquared: m/s²
- NoUnit: No unit
- Radian: rad
- RadianPerSecond: rad/s
- RadianPerSecondSquared: rad/s²
- Volt: V

## PopupMessageEventArgs (robot.PrimaryInterface.PopupMessage)

`class PopupMessageEventArgs : PackageEventArgs`

Popup message that appears with the Assignment instruction or the URScript popup() function

- `PopupMessageEventArgs()`
- `bool Blocking { get; set; }`: Popup is blocking script execution
- `bool Error { get; set; }`: Popup is an error
- `string PopupMessageTitle { get; set; }`: Popup title
- `string PopupTextMessage { get; set; }`: Popup message, null for assignment popups
- `uint RequestId { get; set; }`: Each popup has a unique ID
- `RequestedTypes RequestedType { get; set; }`: Type for assignment popups
- `bool Warning { get; set; }`: Popup is a warning
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## PrimaryInterfaceClient

`class PrimaryInterfaceClient : PrimaryInterfaceClientBase`

Primary / Secondary interface implementation

- `PrimaryInterfaceClient()`: Creates a new Primary Interface client
- `void Connect(string ip)`: Connect to primary interface
- `void Connect(string ip, Interfaces port)`: Connect to a specific port
- Inherited from [PrimaryInterfaceClientBase](UnderAutomation.UniversalRobots.PrimaryInterface.Internal.md#primaryinterfaceclientbase-robotprimaryinterface): `Disconnect`, `RobotModeData`, `JointData`, `ToolData`, `MasterboardData`, `CartesianInfo`, `KinematicsInfo`, `ConfigurationData`, `ForceModeData`, `AdditionalInfo`, `CalibrationData`, `SafetyData`, `ToolCommunicationInfo`, `ToolModeInfo`, `SingularityInfo`, `ProgramThreads`, `Version`, `KeyMessage`, `PopupMessage`, `TextMessage`, `RuntimeExceptionMessage`, `GlobalVariables`, `Script`, `Commands`, `IP`, `Port`, `Connected`, `LocalEndPoint`, `RobotModeDataReceived`, `JointDataReceived`, `ToolDataReceived`, `MasterboardDataReceived`, `CartesianInfoReceived`, `KinematicsInfoReceived`, `ConfigurationDataReceived`, `ForceModeDataReceived`, `AdditionalInfoReceived`, `CalibrationDataReceived`, `SafetyDataReceived`, `ToolCommunicationInfoReceived`, `ToolModeInfoReceived`, `SingularityInfoReceived`, `PackageReceived`, `RawPackageReceived`, `ProgramThreadsReceived`, `VersionReceived`, `KeyMessageReceived`, `PopupMessageReceived`, `TextMessageReceived`, `RuntimeExceptionMessageReceived`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## ProgramThread

`class ProgramThread`

Represents a single running thread in a UR program.

- `ProgramThread()`
- `string LineName { get; set; }`: Name of the program line being executed.
- `int LineNumber { get; set; }`: Current line number being executed in the program.
- `string ThreadName { get; set; }`: Name of the thread.

## ProgramThreadsEventArgs (robot.PrimaryInterface.ProgramThreads)

`class ProgramThreadsEventArgs : PackageEventArgs`

Event data containing information about currently running program threads.

- `ProgramThreadsEventArgs()`
- `ProgramThread[] Threads { get; set; }`: Array of currently running program threads.
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## RequestValueMessageEventArgs

`class RequestValueMessageEventArgs : PackageEventArgs`

Event data for a request value message received from the robot (assignment popup requesting user input).

- `RequestValueMessageEventArgs()`
- `uint RequestId { get; set; }`: Unique identifier of the request.
- `string RequestTextMessage { get; set; }`: Message displayed to the user in the request popup.
- `RequestedTypes RequestedType { get; set; }`: Data type requested from the user.
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## RequestedTypes (robot.PrimaryInterface.PopupMessage.RequestedType)

`enum RequestedTypes`

Types for popup assignment

- Boolean: Popup for boolean value assignment
- Expression: Unused
- Float: Popup for float number value assignment
- Integer: Popup for integer number value assignment
- JointVector: Popup for joint vector value assignment
- None: It's a simple popup message
- Pose: Popup for pose value assignment
- String: Popup for string value assignment
- Waypoint: Unused

## RobotModeDataPackageEventArgs (robot.PrimaryInterface.RobotModeData)

`class RobotModeDataPackageEventArgs : PackageEventArgs`

Information about current robot mode

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
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## RuntimeExceptionMessageEventArgs (robot.PrimaryInterface.RuntimeExceptionMessage)

`class RuntimeExceptionMessageEventArgs : PackageEventArgs`

Reports an error in the execution of the program

- `RuntimeExceptionMessageEventArgs()`
- `string RuntimeExceptionTextMessage { get; set; }`: Information about exception
- `int ScriptColumnNumber { get; set; }`: Execution error column number
- `int ScriptLineNumber { get; set; }`: Execution error line number
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## SafetyDataPackageEventArgs (robot.PrimaryInterface.SafetyData)

`class SafetyDataPackageEventArgs : PackageEventArgs`

Safety internal data

- `SafetyDataPackageEventArgs()`
- `byte[] Data { get; set; }`: Irrelevant (Internal use only)
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## SingularityInfoPackageEventArgs (robot.PrimaryInterface.SingularityInfo)

`class SingularityInfoPackageEventArgs : PackageEventArgs`

Singularity info

- `SingularityInfoPackageEventArgs()`
- `byte SingularitySeverity { get; set; }`: Severity of the singularity
- `byte SingularityType { get; set; }`: Type of the singularity
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## TextMessageEventArgs (robot.PrimaryInterface.TextMessage)

`class TextMessageEventArgs : PackageEventArgs`

Describes a log message sent with URScript instruction textmsg()

- `TextMessageEventArgs()`
- `string TextMessage { get; set; }`: Log message sent with URScript instruction textmsg()
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## ToolCommunicationInfoPackageEventArgs (robot.PrimaryInterface.ToolCommunicationInfo)

`class ToolCommunicationInfoPackageEventArgs : PackageEventArgs`

Tool communication info

- `ToolCommunicationInfoPackageEventArgs()`
- `int BaudRate { get; set; }`: Baud rate for tool serial communication
- `int Parity { get; set; }`: Parity
- `float RxIdleChars { get; set; }`: RX Idle Chars
- `int StopBits { get; set; }`: Stop bits
- `bool ToolCommunicationIsEnabled { get; set; }`: Is the tool communication interface enabled
- `float TxIdleChars { get; set; }`: TX Idle Chars
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## ToolDataPackageEventArgs (robot.PrimaryInterface.ToolData)

`class ToolDataPackageEventArgs : PackageEventArgs`

Tool data

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
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## ToolModeInfoPackageEventArgs (robot.PrimaryInterface.ToolModeInfo)

`class ToolModeInfoPackageEventArgs : PackageEventArgs`

Tool mode info

- `ToolModeInfoPackageEventArgs()`
- `DigitalOutputConfigurations DigitalOutputMode0 { get; set; }`: Digital output 0 configuration
- `DigitalOutputConfigurations DigitalOutputMode1 { get; set; }`: Digital output 1 configuration
- `OutputModes OutputMode { get; set; }`: Digital output mode
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## VersionEventArgs (robot.PrimaryInterface.Version)

`class VersionEventArgs : PackageEventArgs`

Version information from the robot controller firmware

- `VersionEventArgs()`
- `int BugfixVersion { get; set; }`: Firmware bugfix number, for example 1 in 5.6.1.1234
- `string BuildDate { get; set; }`: Build date of the firmware, for example "DEC 2020"
- `int BuildNumber { get; set; }`: Firmware build number, for example 1234 in 5.6.1.1234
- `byte MajorVersion { get; set; }`: Major version number, for example 5 in 5.6.1.1234
- `byte MinorVersion { get; set; }`: Minor firmware version number, for example 6 in 5.6.1.1234
- `string ProjectName { get; set; }`: URControl project
- `Version Version { get; }`: Version of the firmware
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`
