# UnderAutomation.UniversalRobots.Common

## AnalogRanges (robot.PrimaryInterface.ToolData.AnalogInputRange2)

`enum AnalogRanges`

Analog units of analog inputs and outputs

- Current: The analog value is in Amps (A)
- Voltage: The analog value is in Volts (V)

## CartesianCoordinates (robot.Rtde.OutputDataValues.ActualTcpForce)

`class CartesianCoordinates`

Represents a cartesian pose with 3 translations and 3 rotations

- `CartesianCoordinates()`: Create a new pose with null coordinates
- `CartesianCoordinates(double x, double y, double z)`: Creates a new pose with translation informations and null rotations
- `CartesianCoordinates(double x, double y, double z, double rx, double ry, double rz)`: Creates a new pose with translations and rotations information
- `double Rx { get; set; }`: RX rotation in radians or radians/s
- `double Ry { get; set; }`: RY rotation in radians or radians/s
- `double Rz { get; set; }`: RZ rotation in radians or radians/s
- `readonly double[] Values`: Underlying array of 6 double values storing X, Y, Z, Rx, Ry, Rz in that order.
- `double X { get; set; }`: X coordinate in meters or m/s
- `double Y { get; set; }`: Y coordinate in meters or m/s
- `double Z { get; set; }`: Z coordinate in meters or m/s

## ConnectException

`class ConnectException : Exception, ISerializable`

Exception thrown when connection to the robot fails

- `string RobotIp { get; }`: IP address of the robot that the connection was attempted to.
- `string Service { get; }`: Name of the robot service that failed to connect (e.g. Dashboard, RTDE, PrimaryInterface).

## ControlModes (robot.PrimaryInterface.RobotModeData.ControlMode)

`enum ControlModes`

Robot control modes

- Force: Robot is force controlled. (For example : URScript force_mode() function is called)
- Position: Robot is position controlled
- Teach: The robot is hand guided by pushing teached button
- Torque: Robot is torque controlled

## ControllerBoxTypes (robot.PrimaryInterface.ConfigurationData.ControllerBoxType)

`enum ControllerBoxTypes`

Controller box types

- UR10: UR10 controller box
- UR16: UR16 controller box
- UR20: UR20 controller box
- UR3: UR3 controller box
- UR30: UR30 controller box
- UR5: UR5 controller box

## DashboardConnectParameters

`class DashboardConnectParameters : DashboardClientParametersBase`

Setup Dashboard Client

- `bool Enable { get; set; }`: Enable Dashboard client communication. Default value is true.
- Inherited from [DashboardClientParametersBase](UnderAutomation.UniversalRobots.Dashboard.Internal.md#dashboardclientparametersbase): `DEFAULT_PORT`, `DEFAULT_RECEIVE_TIMEOUT_MS`, `DEFAULT_SEND_TIMEOUT_MS`, `Port`, `ReceiveTimeoutMs`, `SendTimeoutMs`

## DigitalOutputConfigurations (robot.PrimaryInterface.ToolModeInfo.DigitalOutputMode0)

`enum DigitalOutputConfigurations`

Digital output configuration (NPN, PNP, Push/Pull)

- PushPull: Push / Pull
- SinkingNPN: Sinking (NOPN)
- SourcingPNP: Sourcing (PNP)

## GlobalVariable

`class GlobalVariable : GlobalVariableValue`

Describes a global variable

- `GlobalVariable()`
- `string Name { get; }`: Variable name
- `TimeSpan Time { get; }`: Last time the variable was sampled
- Inherited from [GlobalVariableValue](UnderAutomation.UniversalRobots.Common.md#globalvariablevalue): `ToList`, `ToPose`, `ToBool`, `ToInt`, `ToFloat`, `ToMatrix`, `Parse`, `Type`, `Value`

## GlobalVariableTypes

`enum GlobalVariableTypes`

Possible types of a variable

- Bool: Variable value is bool
- Float: Variable value is float
- Int: Variable value is int
- List: Variable value is an array : GlobalVariableValue[]
- Matrix: Variable value is a matrix
- None: Variable value is null, the value has not been assigned yet
- Pose: Variable value is a UnderAutomation.UniversalRobots.Pose
- String: Variable value is a System.String

## GlobalVariableValue

`class GlobalVariableValue`

Describes a typed variable value

- `GlobalVariableValue()`
- `static GlobalVariableValue Parse(string message)`: Estimate variable value from its string representation
- `bool ToBool()`: Returns variable value if type is Bool. Il type is Float or Int, it returns True if value is not 0. Else, it returns false
- `float ToFloat()`: Returns variable value if type is Float. Il type is int, it casts it to float. If Type is bool, it returns 1 or 0. Else it returns NaN
- `int ToInt()`: Returns variable value if type is Int. Il type is Float, it tries to cast it to int. If Type is bool, it returns 1 or 0. Else it returns 0
- `GlobalVariableValue[] ToList()`: Returns an array of GlobalVariableValue if Type is List. Else, null is returned
- `Array ToMatrix()`: Return variable value GlobalVariable[,] if variable is a matrix. First dimension is row index and second dimension is column index. Use GetLength(0) to get row number and GetLength(1) to get column count
- `Pose ToPose()`: Returns a Pose if Type is Pose. Else, null is returned
- `GlobalVariableTypes Type { get; }`: Type of a variable
- `object Value { get; }`: Value of the variable

## IUrDhParameters

`interface IUrDhParameters`

Denavit–Hartenberg (DH) parameters for Universal Robots with only the relevant parameters

- `double A2 { get; }`: DH parameter a2 (Shoulder)
- `double A3 { get; }`: DH parameter a3 (Elbow)
- `double D1 { get; }`: DH parameter d1 (Base)
- `double D4 { get; }`: DH parameter d4 (Wrist1)
- `double D5 { get; }`: DH parameter d5 (Wrist2)
- `double D6 { get; }`: DH parameter d6 (Wrist3/Tool)

## InternalErrorEventArgs

`class InternalErrorEventArgs : EventArgs`

Describes an internal error

- `readonly Exception Exception`: The exception thrown that causes an internal error
- `readonly string Message`: Explicit message that explains what happened
- `readonly StatusCode Status`: Context status associated to this internal error

## InterpreterModeConnectParameters

`class InterpreterModeConnectParameters : InterpreterModeClientParametersBase`

Setup Interpreter Mode Client

- `bool Enable { get; set; }`: Enable Interpreter Mode client communication Default value is false
- Inherited from [InterpreterModeClientParametersBase](UnderAutomation.UniversalRobots.InterpreterMode.Internal.md#interpretermodeclientparametersbase): `DEFAULT_PORT`, `Port`

## JointModes (robot.PrimaryInterface.JointData.Base.JointMode)

`enum JointModes : byte`

Joint modes

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

## JointsDoubleValues (robot.Rtde.OutputDataValues.ActualCurrent)

`class JointsDoubleValues : JointsValues<double>`

Represents a set of 6 double-precision values, one per robot joint. Typically used for angles (radians), velocities, currents, etc.

- `JointsDoubleValues()`
- `readonly double[] Values`: Array of the 6 joint data
- `double Base { get; set; }`: Joint 1 out of 6
- `double Shoulder { get; set; }`: Joint 2 out of 6
- `double Elbow { get; set; }`: Joint 3 out of 6
- `double Wrist1 { get; set; }`: Joint 4 out of 6
- `double Wrist2 { get; set; }`: Joint 5 out of 6
- `double Wrist3 { get; set; }`: Joint 6 out of 6

## JointsIntValues (robot.Rtde.OutputDataValues.JointMode)

`class JointsIntValues : JointsValues<int>`

Represents a set of 6 integer values, one per robot joint. Typically used for joint modes, statuses, or other discrete joint data.

- `JointsIntValues()`
- `readonly int[] Values`: Array of the 6 joint data
- `int Base { get; set; }`: Joint 1 out of 6
- `int Shoulder { get; set; }`: Joint 2 out of 6
- `int Elbow { get; set; }`: Joint 3 out of 6
- `int Wrist1 { get; set; }`: Joint 4 out of 6
- `int Wrist2 { get; set; }`: Joint 5 out of 6
- `int Wrist3 { get; set; }`: Joint 6 out of 6

## JointsValues<T>

`class JointsValues<T>`

Vector 6 of double values representing each robot joint

- `JointsValues()`
- `T Base { get; set; }`: Joint 1 out of 6
- `T Elbow { get; set; }`: Joint 3 out of 6
- `T Shoulder { get; set; }`: Joint 2 out of 6
- `readonly T[] Values`: Array of the 6 joint data
- `T Wrist1 { get; set; }`: Joint 4 out of 6
- `T Wrist2 { get; set; }`: Joint 5 out of 6
- `T Wrist3 { get; set; }`: Joint 6 out of 6

## OutputModes (robot.PrimaryInterface.ToolModeInfo.OutputMode)

`enum OutputModes`

Digital output modes

- DualPinPower: Dual Pin Power
- StandardOutput: Standard output

## PackageEventArgs (robot.PrimaryInterface.RobotModeData)

`abstract class PackageEventArgs : EventArgs`

Base class of all received data packages

- `DateTime ReceiveDate`: The date the data has been received

## Pose (robot.Rtde.OutputDataValues.ActualTcpPose)

`class Pose : CartesianCoordinates`

Represents a UR pose

- `Pose()`: Creates a new pose with all coordinates set to zero.
- `Pose(double x, double y, double z)`: Creates a new pose with the specified translation and zero rotation.
- `Pose(double x, double y, double z, double rx, double ry, double rz)`: Creates a new pose with the specified translation and rotation.
- `Pose(Pose pose)`: Creates a new pose by copying values from another pose.
- `static Pose From4x4MatrixToRPY(double[,] matrixTransform)`: Convert a transformation 4x4 matrix to RPY pose
- `static Pose From4x4MatrixToRotationVector(double[,] matrixTransform)`: Convert a transformation 4x4 matrix to rotation vector
- `static Pose FromQuaternionToRotationVector(double x, double y, double z, double w)`: Converts a quaternion to UR rotation vector
- `double[,] FromRPYTo4x4Matrix()`: Consider this pose as a RPY (Roll-Pitch-Yaw) representation and return a 4x4 homogeneous transformation matrix.
- `Pose FromRPYToRotationVector()`: Consider this pose as RPY And convert it to a new Rotation Vector
- `double[,] FromRotationVectorTo4x4Matrix()`: Consider this pose as a rotation vector and return a 4x4 homogeneous transformation matrix.
- `void FromRotationVectorToQuaternion(out double x, out double y, out double z, out double w)`: Converts a rotation vector to quaternion
- `Pose FromRotationVectorToRPY()`: Consider this pose as a Rotation Vector And convert it to a new RPY position
- `double RxDegrees { get; set; }`: RX rotation in degrees or °/s
- `double RyDegrees { get; set; }`: RY rotation in degrees or °/s
- `double RzDegrees { get; set; }`: RZ rotation in degrees or °/s
- `static bool TryParse(string value, out Pose pose)`: Parse a pose from its string representation
- Inherited from [CartesianCoordinates](UnderAutomation.UniversalRobots.Common.md#cartesiancoordinates-robotrtdeoutputdatavaluesactualtcpforce): `Values`, `X`, `Y`, `Z`, `Rx`, `Ry`, `Rz`

## PrimaryInterfaceConnectParameters

`class PrimaryInterfaceConnectParameters : PrimaryInterfaceParametersBase`

Setup Primary Interface Client communication

- `bool Enable { get; set; }`: Choose to enable primary interface Default value is true
- Inherited from [PrimaryInterfaceParametersBase](UnderAutomation.UniversalRobots.PrimaryInterface.Internal.md#primaryinterfaceparametersbase): `Port`

## RestConnectParameters

`class RestConnectParameters : RestClientParametersBase`

Configuration parameters for REST API connection (PolyscopeX only)

- `bool Enable { get; set; }`: Enable REST API client communication. Default value is false because REST API is only available on PolyscopeX robots.
- Inherited from [RestClientParametersBase](UnderAutomation.UniversalRobots.Rest.Internal.md#restclientparametersbase): `DEFAULT_PORT`, `DEFAULT_TIMEOUT_MS`, `Port`, `Version`, `TimeoutMs`

## RobotModels (robot.PrimaryInterface.ConfigurationData.RobotType)

`enum RobotModels`

Model of a UR robot

- UR10: UR10 robot model.
- UR16: UR16 robot model.
- UR18: UR18 robot model.
- UR20: UR20 robot model.
- UR3: UR3 robot model.
- UR30: UR30 robot model.
- UR5: UR5 robot model.
- UR8L: UR8 Long robot model.

## RobotModelsExtended

`enum RobotModelsExtended`

Model of a UR robot (including e-Series and extended payload models)

- UR10: UR10 (CB-Series).
- UR10e: UR10e (e-Series).
- UR12e: UR12e (e-Series).
- UR15: UR15 robot model.
- UR16e: UR16e (e-Series).
- UR18: UR18 robot model.
- UR20: UR20 robot model.
- UR3: UR3 (CB-Series).
- UR30: UR30 robot model.
- UR3e: UR3e (e-Series).
- UR5: UR5 (CB-Series).
- UR5e: UR5e (e-Series).
- UR7e: UR7e (e-Series).
- UR8Long: UR8 Long robot model.

## RobotModes (robot.PrimaryInterface.RobotModeData.RobotMode)

`enum RobotModes`

Robot running modes

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

## RobotSubTypes (robot.PrimaryInterface.ConfigurationData.RobotSubType)

`enum RobotSubTypes`

Robot sub type (e-Serie or CB-Serie)

- CB2Serie: CB2-series (Firmware 1.x)
- CB3Serie: CB3-series (Firmware 3.x)
- ESerie: e-series (Firmware 5.x)

## RtdeConnectParameters

`class RtdeConnectParameters : RtdeParametersBase`

Setup RTDE (Real-Time Data Exchange) client communication

- `bool Enable { get; set; }`: Choose to enable RTDE (Real-Time Data Exchange) Default value is false
- Inherited from [RtdeParametersBase](UnderAutomation.UniversalRobots.Rtde.Internal.md#rtdeparametersbase): `DEFAULT_PORT`, `Frequency`, `Version`, `OutputSetup`, `InputSetup`, `Port`

## SafetyStatus (robot.PrimaryInterface.MasterboardData.Safetymode)

`enum SafetyStatus : byte`

Safety modes

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

## SocketCommunicationConnectParameters

`class SocketCommunicationConnectParameters : SocketCommunicationParametersBase`

Setup socket communication server

- `bool Enable { get; set; }`: Choose to enable socket communication server Default value is false
- Inherited from [SocketCommunicationParametersBase](UnderAutomation.UniversalRobots.SocketCommunication.Internal.md#socketcommunicationparametersbase): `Port`

## SshConnectParameters

`class SshConnectParameters : SshParametersBase`

Setup SSH client

- `SshConnectParameters()`
- `bool EnableSftp { get; set; }`: Choose to enable FTP Default value is false
- `bool EnableSsh { get; set; }`: Choose to enable SSH command line client Default value is false
- Inherited from [SshParametersBase](UnderAutomation.UniversalRobots.Ssh.Internal.md#sshparametersbase): `DEFAULT_PORT`, `Username`, `Password`, `Port`

## StatusCode

`enum StatusCode`

Status code that describes an internal error or an internal action

- DecodageError: The data received are inconsistent and it not possible to decode it.
- GlobalVariablesError: An error occured while decoding global variables
- OK: The action succeeded
- RTDEOverrun: RTDE Event handler takes longer to execute than the time between each RTDE packets
- RTDEThreadAborted: The RTDE read thread has stopped due to an internal exception. No more data event will be raised.
- ReadThreadAborted: The read thread has stopped due to an internal exception. No more data event will be raised.
- SendCommandInternalError: Unable to send URScript because of an internal error.
- SentCommandIsEmpty: Unable to send URScript because the script sent is empty.
- SocketInternalError: An error occured while handling socket packet
- StreamingInterfaceNotConnected: Streaming interface is not connected
- WriteInputsRtdeError: Error occured while writing RTDE input data
- XmlRpcInternalError: An error occured in the XML-RPC server

## ToolModes (robot.PrimaryInterface.ToolData.ToolMode)

`enum ToolModes : byte`

Tool modes

- Bootloader: Bootloader
- Idle: Idle
- Running: Running

## Vector3D (robot.Rtde.OutputDataValues.ActualToolAccelerometer)

`class Vector3D`

Represents a three-dimensional vector with X, Y, and Z components.

- `Vector3D()`
- `readonly double[] Values`: Underlying array of 3 double values storing X, Y, Z in that order.
- `double X { get; set; }`: X component of the vector.
- `double Y { get; set; }`: Y component of the vector.
- `double Z { get; set; }`: Z component of the vector.

## XmlRpcConnectParameters

`class XmlRpcConnectParameters : XmlRpcParametersBase`

Setup XML-RPC server

- `XmlRpcConnectParameters()`
- `bool Enable { get; set; }`: Enable XML-RPC server
- Inherited from [XmlRpcParametersBase](UnderAutomation.UniversalRobots.XmlRpc.Internal.md#xmlrpcparametersbase): `Port`
