# UnderAutomation.UniversalRobots.XmlRpc

## XmlRpcArrayValue

`class XmlRpcArrayValue : XmlRpcValue`

Represents an array of XmlRpcValue that can be exchange with the robot via XML-RPC

- `XmlRpcArrayValue()`: Initializes a new empty array value.
- `XmlRpcArrayValue(IEnumerable<XmlRpcValue> value)`: Initializes a new array value with the specified elements.
- `XmlRpcType Type { get; }`: Gets the XML-RPC type of this value.
- `readonly List<XmlRpcValue> Value`: The list of XML-RPC values contained in this array.
- Inherited from [XmlRpcValue](UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpcvalue): `Xml`

## XmlRpcBooleanValue

`class XmlRpcBooleanValue : XmlRpcValue`

Represents a boolean value that can be exchange with the robot via XML-RPC

- `XmlRpcBooleanValue(bool value)`: Initializes a new instance with the specified boolean value.
- `XmlRpcType Type { get; }`: Gets the XML-RPC type of this value.
- `bool Value`: The boolean value.
- Inherited from [XmlRpcValue](UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpcvalue): `Xml`

## XmlRpcDoubleValue

`class XmlRpcDoubleValue : XmlRpcValue`

Represents a double value that can be exchange with the robot via XML-RPC

- `XmlRpcDoubleValue(double value)`: Initializes a new instance with the specified double value.
- `XmlRpcType Type { get; }`: Gets the XML-RPC type of this value.
- `double Value`: The double-precision floating-point value.
- Inherited from [XmlRpcValue](UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpcvalue): `Xml`

## XmlRpcEventArg

`class XmlRpcEventArg : EventArgs`

Represents a request that has just been received from the robot

- `XmlRpcValue Answer`: Response to be provided to the robot by the user
- `readonly XmlRpcValue[] Arguments`: The arguments of the method called
- `readonly IPEndPoint EndPoint`: IP address of the robot
- `readonly string MethodName`: The method called by the robot
- `readonly XDocument XmlRequest`: The XML document received via HTTP

## XmlRpcIntegerValue

`class XmlRpcIntegerValue : XmlRpcValue`

Represents an integer value that can be exchange with the robot via XML-RPC

- `XmlRpcIntegerValue(int value)`: Initializes a new instance with the specified integer value.
- `XmlRpcType Type { get; }`: Gets the XML-RPC type of this value.
- `int Value`: The integer value.
- Inherited from [XmlRpcValue](UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpcvalue): `Xml`

## XmlRpcPoseValue

`class XmlRpcPoseValue : XmlRpcStructValue`

Represents a pose value that can be exchange with the robot via XML-RPC

- `XmlRpcPoseValue(Pose pose)`: Creates a new pose Value
- `XmlRpcType Type { get; }`: Returns type : XmlRpcType.Pose
- `Pose Value { get; }`: Pose Value
- Inherited from [XmlRpcValue](UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpcvalue): `Xml`

## XmlRpcServer

`class XmlRpcServer : XmlRpcServerBase`

XML-RPC server that receives remote procedure calls from the robot's URScript programs.

- `XmlRpcServer()`
- Inherited from [XmlRpcServerBase](UnderAutomation.UniversalRobots.XmlRpc.Internal.md#xmlrpcserverbase-robotxmlrpc): `Start`, `Stop`, `Enabled`, `Port`, `XmlRpcServerRequest`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## XmlRpcStringValue

`class XmlRpcStringValue : XmlRpcValue`

Represents a string value that can be exchange with the robot via XML-RPC

- `XmlRpcStringValue(string value)`: Initializes a new instance with the specified string value.
- `XmlRpcType Type { get; }`: Gets the XML-RPC type of this value.
- `string Value`: The string value.
- Inherited from [XmlRpcValue](UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpcvalue): `Xml`

## XmlRpcStructMember

`class XmlRpcStructMember`

Member of a structure exchanged via XML-RPC

- `XmlRpcStructMember()`: Initializes a new empty struct member.
- `XmlRpcStructMember(string name, XmlRpcValue value)`: Initializes a new struct member with the specified name and value.
- `string Name`: The name of this struct member.
- `XmlRpcValue Value`: The value of this struct member.

## XmlRpcStructValue

`class XmlRpcStructValue : XmlRpcValue`

Represents a structure that can be exchange with the robot via XML-RPC

- `XmlRpcStructValue()`: Initializes a new empty struct value.
- `XmlRpcStructValue(IEnumerable<XmlRpcStructMember> value)`: Initializes a new struct value with the specified members.
- `XmlRpcType Type { get; }`: Gets the XML-RPC type of this value.
- `readonly List<XmlRpcStructMember> Value`: The list of key-value members in this structure.
- Inherited from [XmlRpcValue](UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpcvalue): `Xml`

## XmlRpcType

`enum XmlRpcType`

All supported types that can be transmitted by XML-RPC

- Array: The RPC type is a XmlRpcArrayValue
- Boolean: The RPC type is a XmlRpcBooleanValue
- Double: The RPC type is a XmlRpcDoubleValue
- Integer: The RPC type is a XmlRpcIntegerValue
- Pose: The RPC type is a XmlRpcPoseValue
- String: The RPC type is a XmlRpcStringValue
- Struct: The RPC type is a XmlRpcStructValue
- Unknown: Type is not supported

## XmlRpcUnknownValue

`class XmlRpcUnknownValue : XmlRpcValue`

Represents an unknown XML-RPC argument that has been received from the robot You can decode it yourself with the XML property

- `readonly string AdditionalInformation`: Additional information about why this value could not be decoded.
- `XmlRpcType Type { get; }`: Gets the XML-RPC type of this value.
- Inherited from [XmlRpcValue](UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpcvalue): `Xml`

## XmlRpcValue

`abstract class XmlRpcValue`

Base class of all elements transmitted by XML-RPC. The XmlRpcValue.Type property indicates the type into which this object can be cast to obtain the value.

- `abstract XmlRpcType Type { get; }`: Determines the class of this message
- `XElement Xml { get; }`: The XML description of the message that has been received from the robot or will be sent to the robot
- `static implicit operator XmlRpcValue(bool value)`: Implicitly converts a System.Boolean to an XmlRpc.XmlRpcBooleanValue.
- `static implicit operator XmlRpcValue(bool[] value)`: Implicitly converts a System.Boolean array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator XmlRpcValue(double value)`: Implicitly converts a System.Double to an XmlRpc.XmlRpcDoubleValue.
- `static implicit operator XmlRpcValue(double[] value)`: Implicitly converts a System.Double array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator XmlRpcValue(int value)`: Implicitly converts an System.Int32 to an XmlRpc.XmlRpcIntegerValue.
- `static implicit operator XmlRpcValue(int[] value)`: Implicitly converts an System.Int32 array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator XmlRpcValue(string value)`: Implicitly converts a System.String to an XmlRpc.XmlRpcStringValue.
- `static implicit operator XmlRpcValue(string[] value)`: Implicitly converts a System.String array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator XmlRpcValue(Pose value)`: Implicitly converts a Common.Pose to an XmlRpc.XmlRpcPoseValue.
- `static implicit operator XmlRpcValue(Pose[] value)`: Implicitly converts a Common.Pose array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator bool(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.Boolean.
- `static implicit operator bool[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.Boolean array.
- `static implicit operator double(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.Double.
- `static implicit operator double[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.Double array.
- `static implicit operator int(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to an System.Int32.
- `static implicit operator int[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to an System.Int32 array.
- `static implicit operator string(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.String.
- `static implicit operator string[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.String array.
- `static implicit operator Pose(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a Common.Pose.
- `static implicit operator Pose[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a Common.Pose array.
- `static implicit operator XmlRpcValue(XmlRpcValue[] value)`: Implicitly converts an array of XmlRpc.XmlRpcValue to an XmlRpc.XmlRpcArrayValue.
