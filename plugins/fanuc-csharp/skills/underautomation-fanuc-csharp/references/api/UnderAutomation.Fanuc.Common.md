# UnderAutomation.Fanuc.Common

## ArmFrontBack (robot.StreamMotion.QueueEndCartesianPosition.Configuration.ArmFrontBack)

`enum ArmFrontBack`

Arm configuration

- Back: Back : B
- Front: Front : T
- Unknown: Unknown

## ArmLeftRight (robot.StreamMotion.QueueEndCartesianPosition.Configuration.ArmLeftRight)

`enum ArmLeftRight`

Arm left right

- Left: Left : L
- Right: Right : R
- Unknown: Unknown

## ArmUpDown (robot.StreamMotion.QueueEndCartesianPosition.Configuration.ArmUpDown)

`enum ArmUpDown`

Arm configuration

- Down: Down : D
- Unknown: Unknown
- Up: Up : U

## CartesianPosition (robot.StreamMotion.QueueEndCartesianPosition)

`class CartesianPosition : XYZWPRPosition`

Fanuc cartesian position and rotations

- `CartesianPosition()`: Default constructor
- `CartesianPosition(double x, double y, double z, double w, double p, double r)`: Constructor with position and rotations
- `CartesianPosition(double x, double y, double z, double w, double p, double r, Configuration configuration)`: Constructor with position, rotations and configuration
- `CartesianPosition(CartesianPosition position)`: Copy constructor
- `CartesianPosition(XYZPosition position, double w, double p, double r)`: Constructor from an XYZ position with rotations
- `Configuration Configuration { get; set; }`: Position configuration
- `static CartesianPosition FromHomogeneousMatrix(double[,] R)`: Create a CartesianPosition with unknow configuration from a homogeneous rotation and translation 4x4 matrix
- `static bool IsNear(CartesianPosition a, CartesianPosition b, double mmTolerance, double degreesTolerance)`: Check if two Cartesian positions are near each other within specified tolerances
- `static double NormalizeAngle(double angle)`: Normalize an angle to the range ]-180, 180]
- `static void NormalizeAngles(CartesianPosition pose)`: Normalize the W, P, R angles to the range ]-180, 180]
- Inherited from [XYZWPRPosition](UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`

## CartesianPositionVariable

`class CartesianPositionVariable : CartesianPosition`

Represents a Cartesian position variable parsed from a Fanuc variable file

- `CartesianPositionVariable()`: Default constructor
- `CartesianPositionVariable(int group, CartesianPosition position)`: Creates a Cartesian position variable from Cartesian position values and a motion group number.
- `int Group { get; set; }`: Motion group number
- `static CartesianPositionVariable Parse(string value)`: Parses a Cartesian position from its string representation
- Inherited from [CartesianPosition](UnderAutomation.Fanuc.Common.md#cartesianposition-robotstreammotionqueueendcartesianposition): `FromHomogeneousMatrix`, `NormalizeAngle`, `NormalizeAngles`, `IsNear`, `Configuration`
- Inherited from [XYZWPRPosition](UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`

## CartesianPositionWithTool

`class CartesianPositionWithTool : ExtendedCartesianPosition`

A cartesian position with a tool ID

- `CartesianPositionWithTool()`: Default constructor
- `CartesianPositionWithTool(double x, double y, double z, double w, double p, double r, double e1, double e2, double e3, int tool)`: Constructor with position, rotations and tool ID
- `CartesianPositionWithTool(double x, double y, double z, double w, double p, double r, int tool)`: Constructor with position, rotations and tool ID
- `int Tool { get; set; }`: Tool ID
- Inherited from [ExtendedCartesianPosition](UnderAutomation.Fanuc.Common.md#extendedcartesianposition-robotstreammotionqueueendcartesianposition): `E1`, `E2`, `E3`
- Inherited from [CartesianPosition](UnderAutomation.Fanuc.Common.md#cartesianposition-robotstreammotionqueueendcartesianposition): `FromHomogeneousMatrix`, `NormalizeAngle`, `NormalizeAngles`, `IsNear`, `Configuration`
- Inherited from [XYZWPRPosition](UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`

## CartesianPositionWithUserFrame

`class CartesianPositionWithUserFrame : CartesianPositionWithTool`

A cartesian tool position with a user frame ID

- `CartesianPositionWithUserFrame()`: Default constructor
- `CartesianPositionWithUserFrame(double x, double y, double z, double w, double p, double r, int tool, int frame)`: Constructor with position, rotations, tool and frame IDs
- `int Frame { get; set; }`: Frame ID in the controller
- Inherited from [CartesianPositionWithTool](UnderAutomation.Fanuc.Common.md#cartesianpositionwithtool): `Tool`
- Inherited from [ExtendedCartesianPosition](UnderAutomation.Fanuc.Common.md#extendedcartesianposition-robotstreammotionqueueendcartesianposition): `E1`, `E2`, `E3`
- Inherited from [CartesianPosition](UnderAutomation.Fanuc.Common.md#cartesianposition-robotstreammotionqueueendcartesianposition): `FromHomogeneousMatrix`, `NormalizeAngle`, `NormalizeAngles`, `IsNear`, `Configuration`
- Inherited from [XYZWPRPosition](UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`

## CgtpConnectParameters

`class CgtpConnectParameters : CgtpConnectParametersBase`

CGTP Web Server connection parameters

- `CgtpConnectParameters()`
- `bool Enable { get; set; }`: Should enable CGTP Web Server for this connection (default: true)
- Inherited from [CgtpConnectParametersBase](UnderAutomation.Fanuc.Cgtp.Internal.md#cgtpconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_REQUEST_TIMEOUT_MS`, `Port`, `RequestTimeoutMs`, `Login`, `Password`

## Configuration (robot.StreamMotion.QueueEndCartesianPosition.Configuration)

`class Configuration`

Fanuc arm configuration

- `Configuration()`: Default constructor
- `Configuration(WristFlip wristFlip, ArmUpDown armUpDown, ArmLeftRight armLeftRight, ArmFrontBack armFrontBack, int turnAxis1, int turnAxis2, int turnAxis3)`: Constructor with all configuration parameters
- `ArmFrontBack ArmFrontBack { get; set; }`: Arm back/front configuration
- `ArmLeftRight ArmLeftRight { get; set; }`: Arm left/right configuration
- `ArmUpDown ArmUpDown { get; set; }`: Arm up/down configuration
- `void FromString(string value)`: Parse a Fanuc configuration string representation, like : "N U T, 0, 0, 0" or "R, 0, 0, 0"
- `bool IsUnknown { get; }`: Indicates if the configuration is unknown
- `static Configuration Parse(string value)`: Parse a Fanuc configuration from its string representation, like : "N U T, 0, 0, 0" or "R, 0, 0, 0"
- `int TurnAxis4 { get; set; }`: Turn number of axis J4 (1:180° to 539°, 0:-179° to 179°, -1:-539° to -180°)
- `int TurnAxis5 { get; set; }`: Turn number of axis J5 (1:180° to 539°, 0:-179° to 179°, -1:-539° to -180°)
- `int TurnAxis6 { get; set; }`: Turn number of axis J6 (1:180° to 539°, 0:-179° to 179°, -1:-539° to -180°)
- `WristFlip WristFlip { get; set; }`: Wrist configuration

## ConnectException

`class ConnectException : Exception, ISerializable, _Exception`

Exception thrown when connection to the robot fails

- `string RobotIp { get; }`: IP address of the robot
- `string Service { get; }`: Name of the service that failed to connect

## DigitalPorts

`enum DigitalPorts`

Fanuc digital port types

- DIN: Digital input
- DOUT: Digital outputs
- FLG: Flags
- RI: Robot inputs
- RO: Robot outputs
- SI: SI
- SO: SO
- UI: User inputs
- UO: User outputs

## ExtendedCartesianPosition (robot.StreamMotion.QueueEndCartesianPosition)

`class ExtendedCartesianPosition : CartesianPosition`

Cartesian position with extended axes (E1, E2, E3)

- `ExtendedCartesianPosition()`: Default constructor
- `ExtendedCartesianPosition(double x, double y, double z, double w, double p, double r, double e1, double e2, double e3)`: Constructor with position, rotations, and extended axes
- `double E1 { get; set; }`: Extended axis 1 value
- `double E2 { get; set; }`: Extended axis 2 value
- `double E3 { get; set; }`: Extended axis 3 value
- Inherited from [CartesianPosition](UnderAutomation.Fanuc.Common.md#cartesianposition-robotstreammotionqueueendcartesianposition): `FromHomogeneousMatrix`, `NormalizeAngle`, `NormalizeAngles`, `IsNear`, `Configuration`
- Inherited from [XYZWPRPosition](UnderAutomation.Fanuc.Common.md#xyzwprposition-robotstreammotionqueueendcartesianposition): `ToHomogeneousMatrix`, `GetQuaternion`, `SetQuaternion`, `Multiply`, `Inverse`, `FlangeToTcp`, `TcpToFlange`, `UserFrameToWorld`, `WorldToUserFrame`, `W`, `P`, `R`
- Inherited from [XYZPosition](UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`

## FtpConnectParameters

`class FtpConnectParameters : FtpConnectParametersBase`

Memory access parameters

- `FtpConnectParameters()`
- `bool Enable { get; set; }`: Should enable memory access for this connection (default: true)
- Inherited from [FtpConnectParametersBase](UnderAutomation.Fanuc.Ftp.Internal.md#ftpconnectparametersbase): `FtpUser`, `FtpPassword`, `FtpTimeoutMs`

## IOComments

`class IOComments`

Contains input and output comment arrays for an I/O type.

- `IOComments()`
- `string[] Inputs { get; set; }`: Array of input comments. Index 0 corresponds to Fanuc port 1.
- `string[] Outputs { get; set; }`: Array of output comments. Index 0 corresponds to Fanuc port 1.

## IOStatus

`class IOStatus`

A digital port status

- `IOStatus()`
- `int Id { get; }`: Digital port ID
- `string Name { get; }`: IO Name
- `DigitalPorts Port { get; }`: Digital port type
- `bool Value { get; }`: Digital port value

## JointPositionVariable

`class JointPositionVariable : JointsPosition`

Represents a joint position variable parsed from a Fanuc variable file

- `JointPositionVariable()`: Default constructor.
- `JointPositionVariable(int group, JointsPosition position)`: Creates a joint position variable from a group number and joint position values.
- `int Group { get; set; }`: Motion group number
- `static JointPositionVariable Parse(string value)`: Parses a joint position from its string representation
- Inherited from [JointsPosition](UnderAutomation.Fanuc.Common.md#jointsposition-robotstreammotionqueueendjointposition): `IsNear`, `Item`, `Values`, `J1`, `J2`, `J3`, `J4`, `J5`, `J6`, `J7`, `J8`, `J9`

## JointsPosition (robot.StreamMotion.QueueEndJointPosition)

`class JointsPosition`

Joints position in degrees

- `JointsPosition()`: Default constructor
- `JointsPosition(double j1Deg, double j2Deg, double j3Deg, double j4Deg, double j5Deg, double j6Deg)`: Constructor with 6 joint values in degrees
- `JointsPosition(double j1Deg, double j2Deg, double j3Deg, double j4Deg, double j5Deg, double j6Deg, double j7Deg, double j8Deg, double j9Deg)`: Constructor with 9 joint values in degrees
- `JointsPosition(double[] values)`: Constructor from an array of joint values in degrees
- `static bool IsNear(JointsPosition j1, JointsPosition j2, double degreesTolerance)`: Check if joints position is near to expected joints position with a tolerance value
- `double this[int i] { get; set; }`: Gets or sets the joint value at the specified index
- `double J1 { get; set; }`: Joint 1 in degrees
- `double J2 { get; set; }`: Joint 2 in degrees
- `double J3 { get; set; }`: Joint 3 in degrees
- `double J4 { get; set; }`: Joint 4 in degrees
- `double J5 { get; set; }`: Joint 5 in degrees
- `double J6 { get; set; }`: Joint 6 in degrees
- `double J7 { get; set; }`: Joint 7 in degrees
- `double J8 { get; set; }`: Joint 8 in degrees
- `double J9 { get; set; }`: Joint 9 in degrees
- `double[] Values { get; }`: Numeric values for each joints

## Languages (robot.Cgtp.Language)

`enum Languages`

Languages supported by the Fanuc robots

- Chinese: For robots set to Chinese language
- English: For robots set to English language
- Japanese: For robots set to Japanese language

## NumericRegister

`class NumericRegister`

Represents a numeric register value that can be either integer or real.

- `NumericRegister()`: Default constructor.
- `NumericRegister(double value)`: Creates a numeric register with a real (double) value.
- `NumericRegister(int value)`: Creates a numeric register with an integer value.
- `int IntegerValue { get; set; }`: Gets or sets the value as an integer. Internally stored as a double.
- `bool IsInteger { get; set; }`: Indicates whether the register holds an integer value (true) or a real value (false)
- `double RealValue { get; set; }`: Gets or sets the value as a double-precision floating-point number.

## NumericRegisterWithComment

`class NumericRegisterWithComment : NumericRegister`

Represents a numeric register with an associated comment.

- `NumericRegisterWithComment()`: Default constructor.
- `NumericRegisterWithComment(double value, string comment)`: Creates a numeric register with a real value and comment.
- `NumericRegisterWithComment(int value, string comment)`: Creates a numeric register with an integer value and comment.
- `NumericRegisterWithComment(string comment)`: Creates a numeric register with a comment.
- `string Comment { get; set; }`: Comment associated with this register.
- Inherited from [NumericRegister](UnderAutomation.Fanuc.Common.md#numericregister): `IsInteger`, `IntegerValue`, `RealValue`

## Position

`class Position`

Robot position with joints and cartesian representations

- `Position()`: Default constructor
- `Position(short userFrame, short userTool, JointsPosition jointsPosition, ExtendedCartesianPosition cartesianPosition)`: Constructor with user frame, tool, joints and cartesian position
- `ExtendedCartesianPosition CartesianPosition { get; set; }`: Cartesian position with extended axes
- `JointsPosition JointsPosition { get; set; }`: Joint values in degrees
- `short UserFrame { get; set; }`: User frame index
- `short UserTool { get; set; }`: User tool index

## PositionRegister

`class PositionRegister`

Represents a position register that can hold either a Cartesian or joint position

- `PositionRegister()`: Default constructor
- `PositionRegister(JointPositionVariable jointsPosition, CartesianPositionVariable cartesianPosition)`: Creates a position register from joint and Cartesian position values
- `CartesianPositionVariable CartesianPosition { get; set; }`: Cartesian position value, if available
- `JointPositionVariable JointsPosition { get; set; }`: Joint position value, if available
- `static PositionRegister Parse(string value)`: Parses a position register from its string representation

## PositionRegisterWithComment

`class PositionRegisterWithComment : PositionRegister`

Represents a position register with an associated comment.

- `PositionRegisterWithComment()`: Default constructor.
- `string Comment { get; set; }`: Comment associated with this position register.
- `static PositionRegisterWithComment Parse(string value)`: Parses a position register with comment from its string representation.
- Inherited from [PositionRegister](UnderAutomation.Fanuc.Common.md#positionregister): `JointsPosition`, `CartesianPosition`

## ProgramType

`enum ProgramType`

Represents the type of a program.

- Karel: The program is a Karel program, also known as PC (Programmable Control).
- TP: The program is a TP (Teach Pendant) program.
- Unknown: The program type is unknown.

## Quaternion

`class Quaternion`

Quaternion that represents an orientation (Qw + Qx.i + Qy.j + Qz.k). Use XYZWPRPosition.GetQuaternion and Common.Quaternion) to convert from and to W, P, R angles.

- `Quaternion()`: Creates the identity quaternion (no rotation)
- `Quaternion(double qw, double qx, double qy, double qz)`: Creates a quaternion from its components
- `double AngleTo(Quaternion other)`: Angle of the rotation between the two orientations, in degrees (0 to 180)
- `Quaternion Conjugate()`: Returns the conjugate of this quaternion. For a rotation, it is the inverse rotation.
- `double Dot(Quaternion other)`: Dot product of the two quaternions
- `static Quaternion FromAxisAngle(double x, double y, double z, double angle)`: Creates a rotation around an axis
- `static Quaternion FromRotationMatrix(double[,] matrix)`: Creates a quaternion from a rotation matrix (3x3, or 4x4 homogeneous matrix)
- `Quaternion Multiply(Quaternion other)`: Returns the product this x other: the rotation other applied after the rotation this, in the frame of this.
- `double Norm { get; }`: Norm of the quaternion (1 for a rotation)
- `Quaternion Normalize()`: Returns this quaternion with a norm of 1
- `double Qw { get; set; }`: Scalar part
- `double Qx { get; set; }`: X component of the vector part
- `double Qy { get; set; }`: Y component of the vector part
- `double Qz { get; set; }`: Z component of the vector part
- `static Quaternion Slerp(Quaternion start, Quaternion end, double t)`: Spherical linear interpolation between two orientations, on the shortest way
- `double[] ToAxisAngle()`: Returns the rotation axis and angle: [x, y, z, angle in degrees]. The axis is a unit vector and the angle is between 0 and 180.
- `double[,] ToRotationMatrix()`: Returns the 3x3 rotation matrix of this orientation

## RmiConnectParameters

`class RmiConnectParameters : RmiConnectParametersBase`

RMI parameters

- `RmiConnectParameters()`
- `bool Enable { get; set; }`: Should enable RMI for this connection (default: false)
- Inherited from [RmiConnectParametersBase](UnderAutomation.Fanuc.Rmi.Internal.md#rmiconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_READ_TIMEOUT_MS`, `Port`, `ReadTimeoutMs`

## SnpxConnectParameters

`class SnpxConnectParameters : SnpxConnectParametersBase`

SNPX parameters

- `SnpxConnectParameters()`
- `bool Enable { get; set; }`: Should enable SNPX for this connection (default: false)
- Inherited from [SnpxConnectParametersBase](UnderAutomation.Fanuc.Snpx.Internal.md#snpxconnectparametersbase): `DEFAULT_PORT`, `Port`

## StreamMotionConnectParameters

`class StreamMotionConnectParameters : StreamMotionConnectParametersBase`

Stream Motion connection parameters (J519 option)

- `StreamMotionConnectParameters()`
- `bool Enable { get; set; }`: Should enable Stream Motion for this connection (default: false)
- `string Ip { get; set; }`: IP address of the robot for standalone Stream Motion connections
- Inherited from [StreamMotionConnectParametersBase](UnderAutomation.Fanuc.StreamMotion.Internal.md#streammotionconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_PROTOCOL_VERSION`, `DEFAULT_BUFFER_LEAD_TIME`, `DEFAULT_PACKET_STACK_SIZE`, `DEFAULT_STATUS_TIMEOUT_MS`, `Port`, `ProtocolVersion`, `BufferLeadTime`, `PacketStackSize`, `StatusTimeoutMs`, `HighPriority`

## StringRegisterWithComment

`class StringRegisterWithComment`

Represents a string register with an associated comment.

- `StringRegisterWithComment()`
- `string Comment { get; set; }`: Comment associated with this register.
- `string Value { get; set; }`: String value of the register.

## StringUtils

`static class StringUtils`

Contains string related utility methods

- `static Encoding GetEncoding(Languages language)`: Gets the encoding for the specified controller language

## TaskStatus

`enum TaskStatus`

Represents the status of a task.

- Aborted: The task is aborted.
- Paused: The task is paused.
- Running: The task is running.
- Unknown: The task status is unknown.

## TelnetConnectParameters

`class TelnetConnectParameters : TelnetConnectParametersBase`

Connection parameters of the Telnet KCL client (remote commands). Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on the web server of the co...

- `TelnetConnectParameters()`
- `bool Enable { get; set; }`: Should use this service (default: false). Prefer robot.Cgtp.Kcl, enabled by default, for new developments.
- Inherited from [TelnetConnectParametersBase](UnderAutomation.Fanuc.Telnet.Internal.md#telnetconnectparametersbase): `TelnetKclPassword`

## UserAlarmDefinition

`class UserAlarmDefinition`

Represents a user alarm definition with a comment and severity level.

- `UserAlarmDefinition()`
- `string Comment { get; set; }`: Comment associated with this alarm.
- `int Severity { get; set; }`: Severity level of the alarm.

## VectorVariable

`class VectorVariable`

Represents a 3D vector variable with X, Y, Z components

- `VectorVariable()`
- `static VectorVariable Parse(string value)`: Parses a vector variable from its string representation
- `double X { get; set; }`: X component of the vector
- `double Y { get; set; }`: Y component of the vector
- `double Z { get; set; }`: Z component of the vector

## WristFlip (robot.StreamMotion.QueueEndCartesianPosition.Configuration.WristFlip)

`enum WristFlip`

Wrist configuration

- Flip: Flip : F
- NoFlip: No flip : N
- Unknown: Unknown

## XYZPosition (robot.StreamMotion.QueueEndCartesianPosition)

`class XYZPosition`

Cartesian position X, Y, Z

- `XYZPosition()`: Default constructor
- `XYZPosition(double x, double y, double z)`: Constructor with X, Y, Z coordinates in millimeters
- `double X { get; set; }`: X coordinate in millimeters
- `double Y { get; set; }`: Y coordinate in millimeters
- `double Z { get; set; }`: Z coordinate in millimeters

## XYZWPRPosition (robot.StreamMotion.QueueEndCartesianPosition)

`class XYZWPRPosition : XYZPosition`

Cartesian position X, Y, Z with W, P, R rotations

- `XYZWPRPosition()`: Default constructor
- `XYZWPRPosition(double x, double y, double z, double w, double p, double r)`: Constructor with position and rotations
- `XYZWPRPosition FlangeToTcp(XYZWPRPosition tool)`: Converts a flange position to the position of the tool center point (TCP)
- `Quaternion GetQuaternion()`: Returns the orientation W, P, R as a quaternion
- `XYZWPRPosition Inverse()`: Returns the inverse of this frame
- `XYZWPRPosition Multiply(XYZWPRPosition other)`: Returns the composition of this frame with another one: the pose other, expressed in this frame, converted to the frame where this position is expressed.
- `double P { get; set; }`: P rotation in degrees (Ry)
- `double R { get; set; }`: R rotation in degrees (Rz)
- `void SetQuaternion(Quaternion quaternion)`: Sets the orientation W, P, R from a quaternion. Angles are between -180 and 180 degrees.
- `XYZWPRPosition TcpToFlange(XYZWPRPosition tool)`: Converts a position of the tool center point (TCP) to the flange position
- `double[,] ToHomogeneousMatrix()`: Convert position to a homogeneous rotation and translation 4x4 matrix
- `XYZWPRPosition UserFrameToWorld(XYZWPRPosition userFrame)`: Converts this position, expressed in a user frame, to the world frame
- `double W { get; set; }`: W rotation in degrees (Rx)
- `XYZWPRPosition WorldToUserFrame(XYZWPRPosition userFrame)`: Converts this position, expressed in the world frame, to a user frame
- Inherited from [XYZPosition](UnderAutomation.Fanuc.Common.md#xyzposition-robotstreammotionqueueendcartesianposition): `X`, `Y`, `Z`
