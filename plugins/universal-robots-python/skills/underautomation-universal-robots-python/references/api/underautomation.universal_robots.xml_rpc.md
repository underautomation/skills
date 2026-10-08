# underautomation.universal_robots.xml_rpc

## XmlRpcArrayValue

`from underautomation.universal_robots.xml_rpc.xml_rpc_array_value import XmlRpcArrayValue`

Represents an array of XmlRpcValue that can be exchange with the robot via XML-RPC

- `XmlRpcArrayValue(value: typing.Any)`: Initializes a new array value with the specified elements.
- `type: XmlRpcType (read only)`: Gets the XML-RPC type of this value.
- `value: typing.Any`: The list of XML-RPC values contained in this array.
- Inherited from [XmlRpcValue](underautomation.universal_robots.xml_rpc.md#xmlrpcvalue): `xml`

## XmlRpcBooleanValue

`from underautomation.universal_robots.xml_rpc.xml_rpc_boolean_value import XmlRpcBooleanValue`

Represents a boolean value that can be exchange with the robot via XML-RPC

- `XmlRpcBooleanValue(value: bool)`: Initializes a new instance with the specified boolean value.
- `type: XmlRpcType (read only)`: Gets the XML-RPC type of this value.
- `value: bool`: The boolean value.
- Inherited from [XmlRpcValue](underautomation.universal_robots.xml_rpc.md#xmlrpcvalue): `xml`

## XmlRpcDoubleValue

`from underautomation.universal_robots.xml_rpc.xml_rpc_double_value import XmlRpcDoubleValue`

Represents a double value that can be exchange with the robot via XML-RPC

- `XmlRpcDoubleValue(value: float)`: Initializes a new instance with the specified double value.
- `type: XmlRpcType (read only)`: Gets the XML-RPC type of this value.
- `value: float`: The double-precision floating-point value.
- Inherited from [XmlRpcValue](underautomation.universal_robots.xml_rpc.md#xmlrpcvalue): `xml`

## XmlRpcEventArg

`from underautomation.universal_robots.xml_rpc.xml_rpc_event_arg import XmlRpcEventArg`

Represents a request that has just been received from the robot

- `xml_request: typing.Any`: The XML document received via HTTP
- `method_name: str`: The method called by the robot
- `arguments: typing.List[XmlRpcValue]`: The arguments of the method called
- `end_point: typing.Any`: IP address of the robot
- `answer: XmlRpcValue`: Response to be provided to the robot by the user

## XmlRpcIntegerValue

`from underautomation.universal_robots.xml_rpc.xml_rpc_integer_value import XmlRpcIntegerValue`

Represents an integer value that can be exchange with the robot via XML-RPC

- `XmlRpcIntegerValue(value: int)`: Initializes a new instance with the specified integer value.
- `type: XmlRpcType (read only)`: Gets the XML-RPC type of this value.
- `value: int`: The integer value.
- Inherited from [XmlRpcValue](underautomation.universal_robots.xml_rpc.md#xmlrpcvalue): `xml`

## XmlRpcPoseValue

`from underautomation.universal_robots.xml_rpc.xml_rpc_pose_value import XmlRpcPoseValue`

Represents a pose value that can be exchange with the robot via XML-RPC

- `XmlRpcPoseValue(pose: Pose)`: Creates a new pose Value
- `value: Pose (read only)`: Pose Value
- `type: XmlRpcType (read only)`: Returns type : XmlRpcType.Pose
- Inherited from [XmlRpcValue](underautomation.universal_robots.xml_rpc.md#xmlrpcvalue): `xml`

## XmlRpcServer

`from underautomation.universal_robots.xml_rpc.xml_rpc_server import XmlRpcServer`

XML-RPC server that receives remote procedure calls from the robot's URScript programs.

- `XmlRpcServer()`
- Inherited from [XmlRpcServerBase](underautomation.universal_robots.xml_rpc.internal.md#xmlrpcserverbase-robotxml_rpc): `start`, `stop`, `enabled`, `port`, `xml_rpc_server_request`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## XmlRpcStringValue

`from underautomation.universal_robots.xml_rpc.xml_rpc_string_value import XmlRpcStringValue`

Represents a string value that can be exchange with the robot via XML-RPC

- `XmlRpcStringValue(value: str)`: Initializes a new instance with the specified string value.
- `type: XmlRpcType (read only)`: Gets the XML-RPC type of this value.
- `value: str`: The string value.
- Inherited from [XmlRpcValue](underautomation.universal_robots.xml_rpc.md#xmlrpcvalue): `xml`

## XmlRpcStructMember

`from underautomation.universal_robots.xml_rpc.xml_rpc_struct_member import XmlRpcStructMember`

Member of a structure exchanged via XML-RPC

- `XmlRpcStructMember(name: str, value: XmlRpcValue)`: Initializes a new struct member with the specified name and value.
- `name: str`: The name of this struct member.
- `value: XmlRpcValue`: The value of this struct member.

## XmlRpcStructValue

`from underautomation.universal_robots.xml_rpc.xml_rpc_struct_value import XmlRpcStructValue`

Represents a structure that can be exchange with the robot via XML-RPC

- `XmlRpcStructValue(value: typing.Any)`: Initializes a new struct value with the specified members.
- `type: XmlRpcType (read only)`: Gets the XML-RPC type of this value.
- `value: typing.Any`: The list of key-value members in this structure.
- Inherited from [XmlRpcValue](underautomation.universal_robots.xml_rpc.md#xmlrpcvalue): `xml`

## XmlRpcType

`from underautomation.universal_robots.xml_rpc.xml_rpc_type import XmlRpcType`

All supported types that can be transmitted by XML-RPC

- Unknown: Type is not supported
- Array: The RPC type is a XmlRpcArrayValue
- Boolean: The RPC type is a XmlRpcBooleanValue
- Double: The RPC type is a XmlRpcDoubleValue
- Integer: The RPC type is a XmlRpcIntegerValue
- String: The RPC type is a XmlRpcStringValue
- Struct: The RPC type is a XmlRpcStructValue
- Pose: The RPC type is a XmlRpcPoseValue

## XmlRpcUnknownValue

`from underautomation.universal_robots.xml_rpc.xml_rpc_unknown_value import XmlRpcUnknownValue`

Represents an unknown XML-RPC argument that has been received from the robot You can decode it yourself with the XML property

- `type: XmlRpcType (read only)`: Gets the XML-RPC type of this value.
- `additional_information: str`: Additional information about why this value could not be decoded.
- Inherited from [XmlRpcValue](underautomation.universal_robots.xml_rpc.md#xmlrpcvalue): `xml`

## XmlRpcValue

`from underautomation.universal_robots.xml_rpc.xml_rpc_value import XmlRpcValue`

Base class of all elements transmitted by XML-RPC. The type property indicates the type into which this object can be cast to obtain the value.

- `type: XmlRpcType (read only)`: Determines the class of this message
- `xml: typing.Any (read only)`: The XML description of the message that has been received from the robot or will be sent to the robot
